param(
    [Parameter(Mandatory=$true)]
    [string]$VideoPath,

    [int]$Interval = 30,

    [string]$OutputDir = ""
)

$ErrorActionPreference = "Stop"

if (-not (Test-Path -LiteralPath $VideoPath)) {
    Write-Output "ERROR: Video file not found: $VideoPath"
    exit 1
}

$ffmpegCmd = Get-Command ffmpeg -ErrorAction SilentlyContinue
if (-not $ffmpegCmd) {
    Write-Output "ERROR: ffmpeg not installed. Run install_deps.ps1 -Install first."
    exit 1
}

if (-not $OutputDir) {
    $OutputDir = Join-Path ([System.IO.Path]::GetDirectoryName($VideoPath)) "frames"
}

if (-not (Test-Path -LiteralPath $OutputDir)) {
    New-Item -ItemType Directory -Path $OutputDir -Force | Out-Null
}

$baseName = [System.IO.Path]::GetFileNameWithoutExtension($VideoPath)

Write-Output "Extracting key frames from: $VideoPath"
Write-Output "Interval: every $Interval seconds"
Write-Output "Output directory: $OutputDir"

ffmpeg -i $VideoPath -vf "fps=1/$Interval" -q:v 2 (Join-Path $OutputDir "$baseName_frame_%04d.jpg") -y 2>$null

$frames = Get-ChildItem -LiteralPath $OutputDir -Filter "$baseName_frame_*.jpg"
$count = $frames.Count

if ($count -gt 0) {
    Write-Output "Frames extracted successfully. Total frames: $count"
    Write-Output "OUTPUT_DIR: $OutputDir"
    foreach ($f in $frames) {
        Write-Output "FRAME: $($f.FullName)"
    }
} else {
    Write-Output "ERROR: No frames extracted. Video may be too short or format unsupported."
    exit 1
}
