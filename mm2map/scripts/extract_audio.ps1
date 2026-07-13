param(
    [Parameter(Mandatory=$true)]
    [string]$VideoPath,

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
    $OutputDir = [System.IO.Path]::GetDirectoryName($VideoPath)
}

$baseName = [System.IO.Path]::GetFileNameWithoutExtension($VideoPath)
$outputAudio = Join-Path $OutputDir "$baseName.extracted_audio.wav"

Write-Output "Extracting audio from: $VideoPath"
Write-Output "Output audio file: $outputAudio"

ffmpeg -i $VideoPath -vn -acodec pcm_s16le -ar 16000 -ac 1 $outputAudio -y 2>$null

if (Test-Path -LiteralPath $outputAudio) {
    $fileSize = (Get-Item $outputAudio).Length / (1024 * 1024)
    Write-Output "Audio extracted successfully. Size: $($fileSize.ToString('F1'))MB"
    Write-Output "OUTPUT: $outputAudio"
} else {
    Write-Output "ERROR: Audio extraction failed."
    exit 1
}
