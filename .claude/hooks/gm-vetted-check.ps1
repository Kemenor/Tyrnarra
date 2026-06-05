# gm-vetted-check.ps1
# PostToolUse hook (Edit|Write|MultiEdit).
# When the edited file is an .html page that still carries a GM-Vetted badge,
# remind Claude to judge whether the edit just made was more than minor and,
# if so, strip the badge. Claude makes the minor-vs-major call; this hook only
# flags, never edits. A trivial fix keeps the badge; a real change drops it.

try {
  $raw = [Console]::In.ReadToEnd()
  if (-not $raw) { exit 0 }
  $payload = $raw | ConvertFrom-Json
} catch { exit 0 }

$fp = $null
if ($payload.tool_input) { $fp = $payload.tool_input.file_path }
if (-not $fp) { exit 0 }
if ($fp -notmatch '\.html$') { exit 0 }
if (-not (Test-Path -LiteralPath $fp)) { exit 0 }

$content = Get-Content -LiteralPath $fp -Raw
if (-not $content) { exit 0 }
if ($content -notmatch 'gm-vetted') { exit 0 }

$name = Split-Path $fp -Leaf
$msg = "GM-VETTED PAGE: '$name' carries a GM-Vetted badge (a page the GM personally read and corrected). You just edited it. Judge whether that edit was MORE THAN MINOR (a real prose, structural, or canon change) or trivial (typo, single word, whitespace, one punctuation swap). If MORE THAN MINOR, strip the badge so the page is no longer marked vetted: delete the gm-vetted HTML comment line and the gm-vetted div. If trivial, leave the badge in place. Do not add or re-add a badge yourself; only the GM vets pages."

$out = @{
  hookSpecificOutput = @{
    hookEventName     = "PostToolUse"
    additionalContext = $msg
  }
}
$out | ConvertTo-Json -Compress -Depth 5
exit 0
