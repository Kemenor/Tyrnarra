# Audio Library: ambience and music for Foundry playlists

`audio.py` searches free table audio by words, downloads the picks, uploads them to
the Foundry server and writes a playlist macro. It exists so that **Claude chooses
the tracks**: the GM names the scene ("Veldtmark basement"), Claude searches
`cult ritual chant crypt`, reads the flavour text and picks. Nobody hunts tags by hand.

| Source | Ref | What | Needs |
|---|---|---|---|
| **Tabletop Audio** | `tta:<n>` | ~530 ten-minute ambiences and music tracks, each with tags, genres and a flavour line. Free for home games (CC BY-NC-ND 4.0). | nothing; the catalogue is cached in `_cache/` and refreshed every 14 days |
| **Freesound** | `fs:<n>` | Short CC-licensed loops and effects: rain, surf, crowds, forges, bells. Layer them under a Tabletop Audio track. | a free API key in `tools/keys/freesound.key` |
| **Local packs** | `local:<path>` | Anything else dropped into `_full/<pack>/` (a bought pack, a Patreon download), matched on folder and file names. | the files |

## Where the files live

- **Local:** `_full/` is a link into the sync folder's `audio-library/` (`python3 tools/check_setup.py --link`), with `tta/` and `freesound/` inside. Audio never goes into git.
- **Server:** the shared `Data/assets/audio/<source>/`, reached in Foundry as `assets/audio/tta/376_Voyage_Begins.mp3`. One copy serves every world; the upload never deletes anything already there.
- **Per quest:** `<quest>.audio.json` (the spec) and `<quest>.audio.macro.js` (the macro) sit beside the quest page, like the token map and the journal macro.

## Usage

```bash
cd tools/audio-library
python3 audio.py search docks harbor night            # every source (Freesound when a key is set)
python3 audio.py search tavern -crowded --type ambience --source tta
python3 audio.py search "rain on canvas" --source fs --min-dur 30 --cc0
python3 audio.py show tta:376 fs:123456               # full metadata, local + server paths, credit
python3 audio.py fetch tta:376                        # download only
python3 audio.py refresh                              # re-read the Tabletop Audio catalogue
```

Search notes:
- A `-word` excludes tracks that carry it.
- Common near-synonyms count at a discount (tavern finds inn, pub; dock finds harbor, pier, wharf), and *harbour* reads as *harbor*.
- `--setting fantasy` is the default and drops Tabletop Audio tracks that are only sci-fi or modern. `--setting any` keeps them.
- `--type ambience|music` keeps only ambience-led or music-led tracks.
- `--json` returns machine-readable output. `✓` marks a track already downloaded.

## Playlists

The spec, one playlist per scene or location:

```json
{
  "folder": "The Veldtmark Invitation",
  "playlists": [
    { "name": "4 · The Basement", "mode": "sequential", "scene": "Veldtmark Basement",
      "sounds": [
        { "ref": "tta:39", "name": "Ritual chamber (Temple of the Eye)" },
        { "ref": "fs:123456", "name": "Dripping water", "volume": 0.3 } ] }
  ]
}
```

| Field | Meaning |
|---|---|
| `folder` | The Playlist folder in Foundry. |
| `mode` | `sequential` (default), `shuffle`, `simultaneous` (every sound at once: an ambience bed plus a loop) or `disabled` (a soundboard). |
| `scene` *(optional)* | Link the playlist to that scene by name, so activating the scene starts it. |
| `sounds[]` | `ref`, plus optional `name` (defaults to the track title), `volume` (0–1 slider position, default 0.5), `repeat` (default true), `fade` (ms, default 2000). A bare ref string works too. |

```bash
python3 tools/audio-library/audio.py playlist --spec <quest>.audio.json --upload --out <quest>.audio.macro.js
```

`--upload` downloads anything missing and rsyncs it to the server, using the same
`~/.config/tyrnarra/foundry-remote` address as `foundryExport/upload_foundry.py`.
In Foundry, run the macro as GM (Create Macro, type `script`, paste, run). It is
**add-only**: an existing playlist keeps its sounds, order and volumes, and only
sounds missing by name are added. Each sound's credit goes into its description.

## Freesound key

1. Make a free account at freesound.org.
2. Apply for an API key at `freesound.org/apiv2/apply` (any name and description; the
   "Client secret/Api key" value is the one to use).
3. Save it as the only line of `~/Sync/Tyrnarra/keys/freesound.key`, then run
   `python3 tools/check_setup.py --link`.

The key covers searching and the high-quality MP3 preview of each sound, which is
what gets downloaded. That's enough for table ambience; the original WAV files
would need a second login step that this tool skips.
