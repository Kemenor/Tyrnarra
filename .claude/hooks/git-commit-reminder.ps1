# git-commit-reminder.ps1
# ---------------------------------------------------------------------------
# PostToolUse (Write|Edit) reminder hook for the Tyrnarra project.
#
# When a file under lore/ or any .html page is edited, this injects a
# NON-BLOCKING reminder into the model's context that completed lore-writes
# and HTML publishes should be committed (with a descriptive message) and
# pushed, per CLAUDE.md's "commit + push per completed phase" workflow.
#
# It ONLY reminds. It never runs `git add`/`commit`/`push` itself; the commit
# decision, the message, and the push stay with Claude (and respect the
# surface-before-publish pause: no committing mid-phase or un-reviewed drafts).
#
# Modelled on the gm-vetted-check.ps1 reminder pattern referenced in CLAUDE.md.
# ---------------------------------------------------------------------------

$ErrorActionPreference = 'SilentlyContinue'

# The hook payload arrives as JSON on stdin.
$raw = [Console]::In.ReadToEnd()
if ([string]::IsNullOrWhiteSpace($raw)) { exit 0 }

try { $payload = $raw | ConvertFrom-Json } catch { exit 0 }

$path = $payload.tool_input.file_path
if ([string]::IsNullOrWhiteSpace($path)) { exit 0 }

# Normalise separators so the same match works for Windows and POSIX paths.
$p = ($path -replace '\\', '/')

$isLore = $p -match '/lore/'
$isHtml = $p -match '\.html$'
if (-not ($isLore -or $isHtml)) { exit 0 }

$kind = if ($isLore) { 'lore file' } else { 'HTML page' }

$msg = "Tyrnarra workflow reminder: you edited a $kind. Per CLAUDE.md, once this lore-write or HTML-publish phase is complete and surfaced, commit it with a descriptive message and push. Do not commit mid-phase or un-reviewed drafts. (This hook only reminds; it never runs git.)"

$out = @{
  hookSpecificOutput = @{
    hookEventName     = 'PostToolUse'
    additionalContext = $msg
  }
} | ConvertTo-Json -Depth 5 -Compress

Write-Output $out
exit 0
