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

$timestamp = [int](Get-Date -UFormat %s)
$outputTemplate = Join-Path $OutputDir "mm2map_$timestamp.%(ext)s"

yt-dlp -f "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best" --merge-output-format mp4 -o $outputTemplate $Url 2>&1

$videoFile = Get-ChildItem -LiteralPath $OutputDir -Filter "mm2map_$timestamp*" | Sort-Object Length -Descending | Select-Object -First 1

if ($videoFile) {
    $fileSize = $videoFile.Length / (1024 * 1024)

    $titleRaw = yt-dlp --print title $Url 2>$null
    if ($titleRaw) {
        $safeTitle = $titleRaw -replace '[^\w\s\u4e00-\u9fff\-]', ''
        $safeTitle = $safeTitle.Trim()
        if ($safeTitle.Length -gt 50) { $safeTitle = $safeTitle.Substring(0, 50) }
        $newName = $safeTitle + ".mp4"
        $newPath = Join-Path $OutputDir $newName
        try {
            Rename-Item -LiteralPath $videoFile.FullName -NewName $newName -ErrorAction Stop
            $videoFile = Get-Item -LiteralPath $newPath
        } catch {
            Write-Output "NOTE: Could not rename to title-based name, keeping timestamp name."
        }
    }

    Write-Output "Download successful."
    Write-Output "File: $($videoFile.FullName)"
    Write-Output "Size: $($fileSize.ToString('F1'))MB"
    Write-Output "OUTPUT: $($videoFile.FullName)"

    $descPath = Join-Path $OutputDir "description.txt"
    yt-dlp --print description $Url 2>$null | Out-File -FilePath $descPath -Encoding utf8
} else {
    Write-Output "ERROR: Download failed. Possible reasons:"
    Write-Output "  - URL is not a valid video link"
    Write-Output "  - Platform requires authentication (cookie)"
    Write-Output "  - Network connection issue"
    Write-Output "  - yt-dlp version outdated (try: pip install --upgrade yt-dlp)"
    exit 1
}
