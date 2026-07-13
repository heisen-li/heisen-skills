param(
    [switch]$Install,
    [switch]$CheckOnly
)

$ErrorActionPreference = "Continue"

function Test-Command {
    param([string]$Name)
    try { Get-Command $Name -ErrorAction SilentlyContinue | Select-Object -First 1 } catch { $null }
}

function Test-PythonPackage {
    param([string]$Name)
    $result = python -c "import $Name; print('OK')" 2>$null
    if ($result -match "OK") { return $true } else { return $false }
}

$deps = @(
    @{ Name = "ffmpeg"; Type = "command"; Desc = "ffmpeg - 音频提取与关键帧截取" },
    @{ Name = "python"; Type = "command"; Desc = "Python 3.x" },
    @{ Name = "yt-dlp"; Type = "command"; Desc = "yt-dlp - 视频URL下载（YouTube/Bilibili等）" },
    @{ Name = "pptx"; Type = "python_package"; Desc = "python-pptx - PPT文件解析" },
    @{ Name = "faster_whisper"; Type = "python_package"; Desc = "faster-whisper - 本地语音转录（无需API Key）" },
    @{ Name = "openai"; Type = "python_package"; Desc = "openai - Whisper API转录（可选，需API Key）" }
)

Write-Output "=========================================="
Write-Output "  mm2map 依赖检测与安装"
Write-Output "=========================================="
Write-Output ""

$missing = @()
$installed = @()

foreach ($dep in $deps) {
    $found = $false
    if ($dep.Type -eq "command") {
        $cmd = Test-Command $dep.Name
        if ($cmd) {
            $found = $true
            Write-Output "[OK] $($dep.Desc)"
        }
    } elseif ($dep.Type -eq "python_package") {
        if (Test-PythonPackage $dep.Name) {
            $found = $true
            Write-Output "[OK] $($dep.Desc)"
        }
    }

    if (-not $found) {
        Write-Output "[MISS] $($dep.Desc)"
        $missing += $dep
    } else {
        $installed += $dep
    }
}

Write-Output ""
Write-Output "已安装: $($installed.Count) / 总计: $($deps.Count)"

if ($missing.Count -eq 0) {
    Write-Output ""
    Write-Output "所有依赖已就绪，可正常使用 /mm2map"
    exit 0
}

if ($CheckOnly) {
    Write-Output ""
    Write-Output "缺少 $($missing.Count) 个依赖。请运行 install_deps.ps1 -Install 安装。"
    exit 1
}

if (-not $Install) {
    Write-Output ""
    Write-Output "缺少 $($missing.Count) 个依赖。使用 -Install 参数自动安装："
    Write-Output "  powershell -ExecutionPolicy Bypass -File install_deps.ps1 -Install"
    exit 1
}

Write-Output ""
Write-Output "开始自动安装缺少的依赖..."
Write-Output ""

foreach ($dep in $missing) {
    Write-Output "正在安装: $($dep.Desc) ..."

    if ($dep.Name -eq "ffmpeg") {
        $ffmpegCmd = Test-Command "ffmpeg"
        if (-not $ffmpegCmd) {
            Write-Output "  尝试通过 winget 安装 ffmpeg ..."
            winget install --id Gyan.FFmpeg -e --accept-source-agreements --accept-package-agreements 2>$null
            if ($LASTEXITCODE -ne 0) {
                Write-Output "  winget 安装失败，尝试 choco ..."
                choco install ffmpeg -y 2>$null
            }
        }
    } elseif ($dep.Name -eq "python") {
        $pyCmd = Test-Command "python"
        if (-not $pyCmd) {
            Write-Output "  尝试通过 winget 安装 Python ..."
            winget install --id Python.Python.3.12 -e --accept-source-agreements --accept-package-agreements 2>$null
        }
    } elseif ($dep.Name -eq "yt-dlp") {
        Write-Output "  pip install yt-dlp ..."
        python -m pip install yt-dlp --quiet 2>$null
    } elseif ($dep.Name -eq "faster_whisper") {
        Write-Output "  pip install faster-whisper ..."
        python -m pip install faster-whisper --quiet 2>$null
    } elseif ($dep.Name -eq "pptx") {
        Write-Output "  pip install python-pptx ..."
        python -m pip install python-pptx --quiet 2>$null
    } elseif ($dep.Name -eq "openai") {
        Write-Output "  pip install openai ..."
        python -m pip install openai --quiet 2>$null
    }

    $verifyFound = $false
    if ($dep.Type -eq "command") {
        if (Test-Command $dep.Name) { $verifyFound = $true }
    } elseif ($dep.Type -eq "python_package") {
        if (Test-PythonPackage $dep.Name) { $verifyFound = $true }
    }

    if ($verifyFound) {
        Write-Output "  [OK] $($dep.Desc) 安装成功"
    } else {
        Write-Output "  [FAIL] $($dep.Desc) 安装失败，请手动安装"
    }
}

Write-Output ""
Write-Output "=========================================="
Write-Output "  安装完成，重新检测依赖状态"
Write-Output "=========================================="
Write-Output ""

$finalMissing = @()
foreach ($dep in $deps) {
    $found = $false
    if ($dep.Type -eq "command") {
        if (Test-Command $dep.Name) { $found = $true }
    } elseif ($dep.Type -eq "python_package") {
        if (Test-PythonPackage $dep.Name) { $found = $true }
    }
    if ($found) {
        Write-Output "[OK] $($dep.Desc)"
    } else {
        Write-Output "[MISS] $($dep.Desc)"
        $finalMissing += $dep
    }
}

if ($finalMissing.Count -eq 0) {
    Write-Output ""
    Write-Output "所有依赖已就绪！"
    exit 0
} else {
    Write-Output ""
    Write-Output "仍有 $($finalMissing.Count) 个依赖未安装，请手动处理。"
    Write-Output "手动安装指南："
    foreach ($d in $finalMissing) {
        if ($d.Name -eq "ffmpeg") {
            Write-Output "  ffmpeg: winget install Gyan.FFmpeg 或从 https://ffmpeg.org 下载"
        } elseif ($d.Name -eq "python") {
            Write-Output "  Python: winget install Python.Python.3.12 或从 https://python.org 下载"
        } elseif ($d.Name -eq "yt-dlp") {
            Write-Output "  yt-dlp: pip install yt-dlp 或从 https://github.com/yt-dlp/yt-dlp 下载"
        } elseif ($d.Name -eq "faster_whisper") {
            Write-Output "  faster-whisper: pip install faster-whisper（本地转录，无需API Key）"
        } elseif ($d.Name -eq "pptx") {
            Write-Output "  python-pptx: pip install python-pptx"
        } elseif ($d.Name -eq "openai") {
            Write-Output "  openai: pip install openai"
        }
    }
    exit 1
}
