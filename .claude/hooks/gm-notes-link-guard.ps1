# gm-notes-link-guard.ps1
# ---------------------------------------------------------------------------
# PostToolUse (Write|Edit) guard hook for the Tyrnarra project.
#
# The published worldbuilding site (/setting/) is player-facing, and the player
# campaign companion (/player-campaigns/) ships with all GM-tier content
# stripped. Neither may link into /gm-notes/ (the GM-only, sidebar-unlinked
# table layer). This hook fires when an .html/.js/.css file under
# published/setting/ or published/player-campaigns/ is written or edited and
# warns (non-blocking) if the file now contains an actual LINK to /gm-notes/.
#
# It distinguishes a link from a prose/comment mention: only a /gm-notes path
# sitting immediately behind a quote or url( opener trips it. Both nav files
# (site-nav.js, pc-nav.js) carry deliberate comments explaining that gm-notes
# is NOT linked here; those bare mentions must not fire.
#
# It ONLY warns. It never edits the file or strips the link; the fix stays with
# Claude. Modelled on the gm-vetted-check.ps1 / git-commit-reminder.ps1 hooks.
# ---------------------------------------------------------------------------

$ErrorActionPreference = 'SilentlyContinue'

# Hook payload arrives as JSON on stdin.
$raw = [Console]::In.ReadToEnd()
if ([string]::IsNullOrWhiteSpace($raw)) { exit 0 }

try { $payload = $raw | ConvertFrom-Json } catch { exit 0 }

$path = $payload.tool_input.file_path
if ([string]::IsNullOrWhiteSpace($path)) { exit 0 }

# Normalise separators so the same match works for Windows and POSIX paths.
$p = ($path -replace '\\', '/')

# Guard only the two published, player-facing trees. The GM layer itself
# (/published/gm-notes/) links to itself freely and is intentionally skipped.
$inSetting = $p -match '/published/setting/'
$inPlayer  = $p -match '/published/player-campaigns/'
if (-not ($inSetting -or $inPlayer)) { exit 0 }

# Only the text page assets that can carry a link are worth scanning.
if ($p -notmatch '\.(html|js|css)$') { exit 0 }

if (-not (Test-Path -LiteralPath $path)) { exit 0 }
$content = Get-Content -LiteralPath $path -Raw
if ([string]::IsNullOrWhiteSpace($content)) { exit 0 }

# A real link to the GM layer puts the /gm-notes path right behind a quote or a
# url( opener: href="/gm-notes/...", src='/gm-notes/...', url(/gm-notes/...),
# "../gm-notes/...". A bare prose/comment mention (". The GM-only /gm-notes/
# tree") has a space, not a delimiter, in front of the path, so it is skipped.
# The char class is ["'(] (the doubled '' is one literal single-quote inside
# this single-quoted PowerShell string).
if ($content -notmatch '(?i)["''(]\s*[./\\]*gm-notes') { exit 0 }

$name = Split-Path $path -Leaf
$tree = if ($inSetting) {
  'the player-facing worldbuilding site (/setting/)'
} else {
  'the player campaign companion (/player-campaigns/)'
}

$msg = "GM-NOTES LINK LEAK: '$name' belongs to $tree, which must never link into /gm-notes/ (the GM-only, sidebar-unlinked table layer; player-facing pages ship with all GM-tier content stripped). The file you just wrote contains a link or path reference to /gm-notes/. Search the file for 'gm-notes', then either delete that href/src/path or repoint it at a published /setting/ or /player-campaigns/ target before committing. (This hook only warns; it never edits the file. A bare prose mention of the path will not trip it, so this is an actual link.)"

$out = @{
  systemMessage = "GM-notes link guard: '$name' under $tree links into the GM-only /gm-notes/ layer. Player-facing pages must not. Remove or repoint the link before committing."
  hookSpecificOutput = @{
    hookEventName     = 'PostToolUse'
    additionalContext = $msg
  }
} | ConvertTo-Json -Depth 5 -Compress

Write-Output $out
exit 0
