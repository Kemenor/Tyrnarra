// Read and write Godot 3 FileAccessCompressed ("GCPF") files, FastLZ mode only,
// which is what Wonderdraft uses for .wonderdraft_map.
//   gcpf d in.gcpf  > out.bin     decompress to stdout
//   gcpf c out.gcpf < in.bin      compress from stdin
// Build: gcc -O2 -o gcpf gcpf.c
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>

#define BLOCK 4096

static long fastlz_decompress(const uint8_t *in, long len, uint8_t *out, long maxout) {
    const uint8_t *ip = in, *ip_limit = in + len;
    uint8_t *op = out, *op_limit = out + maxout;
    int level = (in[0] >> 5) + 1;
    uint32_t ctrl = (*ip++) & 31;
    int loop = 1;
    do {
        const uint8_t *ref = op;
        uint32_t l = ctrl >> 5;
        uint32_t ofs = (ctrl & 31) << 8;
        if (ctrl >= 32) {
            l--;
            ref -= ofs;
            if (level == 1) {
                if (l == 6) l += *ip++;
                ref -= *ip++;
            } else {
                uint8_t code;
                if (l == 6) do { code = *ip++; l += code; } while (code == 255);
                code = *ip++;
                ref -= code;
                if (code == 255 && ofs == (31u << 8)) {
                    ofs = (uint32_t)(*ip++) << 8;
                    ofs += *ip++;
                    ref = op - ofs - 8191;
                }
            }
            if (op + l + 3 > op_limit) return -1;
            if (ref - 1 < out) return -2;
            if (ip < ip_limit) ctrl = *ip++; else loop = 0;
            ref--;
            for (uint32_t i = 0; i < l + 3; i++) *op++ = *ref++;
        } else {
            ctrl++;
            if (op + ctrl > op_limit || ip + ctrl > ip_limit) return -3;
            memcpy(op, ip, ctrl);
            op += ctrl; ip += ctrl;
            loop = ip < ip_limit;
            if (loop) ctrl = *ip++;
        }
    } while (loop);
    return op - out;
}

static uint8_t *emit_literals(uint8_t *op, const uint8_t *src, long n) {
    while (n > 0) {
        long c = n > 32 ? 32 : n;
        *op++ = (uint8_t)(c - 1);
        memcpy(op, src, c);
        op += c; src += c; n -= c;
    }
    return op;
}

// FastLZ level 1 compressor (greedy, 13-bit hash). Output is decodable by any
// FastLZ decompressor, including the one bundled in Godot.
static long fastlz1_compress(const uint8_t *in, long n, uint8_t *out) {
    static int32_t htab[1 << 13];
    for (int i = 0; i < (1 << 13); i++) htab[i] = -1;
    const long ip_limit = n - 12;
    long ip = 0, anchor = 0;
    uint8_t *op = out;
    while (ip < ip_limit) {
        uint32_t seq = in[ip] | (in[ip + 1] << 8) | (in[ip + 2] << 16);
        uint32_t h = (seq * 2654435761u) >> 19;
        long ref = htab[h];
        htab[h] = (int32_t)ip;
        long dist = ip - ref;
        if (ref >= 0 && dist >= 1 && dist <= 8192 &&
            in[ref] == in[ip] && in[ref + 1] == in[ip + 1] && in[ref + 2] == in[ip + 2]) {
            op = emit_literals(op, in + anchor, ip - anchor);
            long m = 3;
            while (ip + m < n - 2 && m < 264 && in[ref + m] == in[ip + m]) m++;
            uint32_t l = (uint32_t)(m - 3), e = (uint32_t)(dist - 1);
            if (l < 6) {
                *op++ = (uint8_t)(((l + 1) << 5) | (e >> 8));
            } else {
                *op++ = (uint8_t)((7 << 5) | (e >> 8));
                *op++ = (uint8_t)(l - 6);
            }
            *op++ = (uint8_t)(e & 255);
            ip += m;
            anchor = ip;
        } else {
            ip++;
        }
    }
    op = emit_literals(op, in + anchor, n - anchor);
    return op - out;
}

static uint8_t *read_all(FILE *f, long *len) {
    long cap = 1 << 26, n = 0;
    uint8_t *buf = malloc(cap);
    size_t r;
    while ((r = fread(buf + n, 1, cap - n, f)) > 0) {
        n += r;
        if (n == cap) { cap *= 2; buf = realloc(buf, cap); }
    }
    *len = n;
    return buf;
}

static int decompress_file(const char *path) {
    FILE *f = fopen(path, "rb");
    if (!f) { perror(path); return 1; }
    long n;
    uint8_t *buf = read_all(f, &n);
    fclose(f);
    if (n < 16 || memcmp(buf, "GCPF", 4)) { fprintf(stderr, "%s: not a GCPF file\n", path); return 1; }
    uint32_t mode, bs, total;
    memcpy(&mode, buf + 4, 4); memcpy(&bs, buf + 8, 4); memcpy(&total, buf + 12, 4);
    if (mode != 0) { fprintf(stderr, "%s: compression mode %u, only FastLZ (0) supported\n", path, mode); return 1; }
    uint32_t nblocks = total / bs + 1;
    long pos = 16 + 4L * nblocks;
    uint8_t *blk = malloc(bs + 64);
    for (uint32_t i = 0; i < nblocks; i++) {
        uint32_t csize;
        memcpy(&csize, buf + 16 + 4L * i, 4);
        long want = (i == nblocks - 1) ? total - (long)bs * i : bs;
        if (pos + csize > n) { fprintf(stderr, "%s: truncated at block %u\n", path, i); return 2; }
        if (want > 0) {
            long got = fastlz_decompress(buf + pos, csize, blk, bs + 64);
            if (got < want) { fprintf(stderr, "%s: bad block %u\n", path, i); return 2; }
            fwrite(blk, 1, want, stdout);
        }
        pos += csize;
    }
    return 0;
}

// Same layout Godot's FileAccessCompressed::close() writes.
static int compress_file(const char *path) {
    long n;
    uint8_t *data = read_all(stdin, &n);
    if (n > 0xFFFFFFFFL) { fprintf(stderr, "input too large\n"); return 1; }
    uint32_t total = (uint32_t)n, bs = BLOCK, mode = 0;
    uint32_t nblocks = total / bs + 1;
    uint32_t *sizes = calloc(nblocks, 4);
    uint8_t *cbuf = malloc(bs + bs / 16 + 64), pad[16];
    FILE *f = fopen(path, "wb");
    if (!f) { perror(path); return 1; }
    fwrite("GCPF", 1, 4, f);
    fwrite(&mode, 4, 1, f); fwrite(&bs, 4, 1, f); fwrite(&total, 4, 1, f);
    fwrite(sizes, 4, nblocks, f);
    for (uint32_t i = 0; i < nblocks; i++) {
        long bl = (i == nblocks - 1) ? total % bs : bs;
        const uint8_t *src = data + (long)bs * i;
        if (bl < 16) {  // Godot pads tiny blocks to 16 bytes before FastLZ
            memset(pad, 0, 16);
            memcpy(pad, src, bl);
            src = pad; bl = 16;
        }
        long s = fastlz1_compress(src, bl, cbuf);
        fwrite(cbuf, 1, s, f);
        sizes[i] = (uint32_t)s;
    }
    fwrite("GCPF", 1, 4, f);
    fseek(f, 16, SEEK_SET);
    fwrite(sizes, 4, nblocks, f);
    if (fclose(f)) { perror(path); return 1; }
    return 0;
}

int main(int argc, char **argv) {
    if (argc == 3 && !strcmp(argv[1], "d")) return decompress_file(argv[2]);
    if (argc == 3 && !strcmp(argv[1], "c")) return compress_file(argv[2]);
    fprintf(stderr, "usage: %s d in.gcpf > out.bin | %s c out.gcpf < in.bin\n", argv[0], argv[0]);
    return 1;
}
