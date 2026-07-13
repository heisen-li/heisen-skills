param(
    [Parameter(Mandatory=$true)]
    [string]$Url,

    [string]$OutputDir = ""
)

$ErrorActionPreference = "Stop"

$ytDlpCmd = Get-Command yt-dlp -ErrorAction SilentlyContinue
if (-not $ytDlpCmd) {
    Write-Output "ERROR: yt-dlp not installed. Run install_deps.ps1 -Install first."
    exit 1
}

if (-not $OutputDir) {
    $OutputDir = Join-Path $env:TEMP "mm2map_downloads"
}

if (-not (Test-Path -LiteralPath $OutputDir)) {
    New-Item -ItemType Directory -Path $OutputDir -Force | Out-Null
}

Write-Output "Downloading video from: $Url"
Write-Output "Output directory: $OutputDir"

$beforeFiles = Get-ChildItem -LiteralPath $OutputDir -File

yt-dlp -f "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best" --merge-output-format mp4 -o "$OutputDir\%(title)s.%(ext)s" $Url 2>&1

$afterFiles = Get-ChildItem -LiteralPath $OutputDir -File
$newFiles = $afterFiles | Where-Object { $beforeFiles -notcontains $_ }

if ($newFiles.Count -gt 0) {
    $videoFile = $newFiles | Sort-Object Length -Descending | Select-Object -First 1
    $fileSize = $videoFile.Length / (1024 * 1024)
    Write-Output "Download successful."
    Write-Output "File: $($videoFile.FullName)"
    Write-Output "Size: $($fileSize.ToString('F1'))MB"
    Write-Output "OUTPUT: $($videoFile.FullName)"
} else {
    Write-Output "ERROR: Download failed. Possible reasons:"
    Write-Output "  - URL is not a valid video link"
    Write-Output "  - Platform requires authentication (cookie)"
    Write-Output "  - Network connection issue"
    Write-Output "  - yt-dlp version outdated (try: pip install --upgrade yt-dlp)"
    exit 1
}
