# OCR Watcher - pure ASCII (uses Unicode escape for Chinese paths)
$ErrorActionPreference = "Stop"

# Chinese path chars: 我=W, 资=D, 料=...
# Use Unicode escape for non-ASCII in $vars
$baseDir = "D:\" + [char]0x6211 + [char]0x7684 + [char]0x8D44 + [char]0x6599 + "\" + [char]0x4E66 + [char]0x7C4D
# 共同富裕 = 共同 + 富裕
$gongtongTxtName = [char]0x5171 + [char]0x540C + [char]0x5BCC + [char]0x88D5 + ".txt"
$gongtongPdfName = [char]0x5171 + [char]0x540C + [char]0x5BCC + [char]0x88D5 + ".pdf"
# 曼昆经济学
$mankiwTxtName = [char]0x66FC + [char]0x6606 + [char]0x7ECF + [char]0x6D4E + [char]0x5B66 + ".txt"
# 经济学原理(第8版) 微观经济学分册(曼昆著).pdf
$mankiwPdfName = [char]0x7ECF + [char]0x6D4E + [char]0x5B66 + [char]0x539F + [char]0x7406 + [char]0x0028 + [char]0x7B2C + "8" + [char]0x7248 + [char]0x0029 + " " + [char]0x5FAE + [char]0x89C2 + [char]0x7ECF + [char]0x6D4E + [char]0x5B66 + [char]0x5206 + [char]0x518C + [char]0x0028 + [char]0x66FC + [char]0x6606 + [char]0x8457 + [char]0x0029 + ".pdf"

$gongtongTmp = Join-Path $baseDir ($gongtongTxtName + ".tmp")
$gongtongFinal = Join-Path $baseDir $gongtongTxtName
$mankiwTmp = Join-Path $baseDir ($mankiwTxtName + ".tmp")
$mankiwFinal = Join-Path $baseDir $mankiwTxtName
$gongtongPdf = Join-Path $baseDir $gongtongPdfName
$mankiwPdf = Join-Path $baseDir $mankiwPdfName
$logFile = "D:\ocr_watch.log"
$script = "d:\常用脚本\skills\cangjie-skill\scripts\ocr_pdf.py"
$markerRegex = "===" + " " + [char]0x7B2C + " (\d+) " + [char]0x9875 + " " + "==="

# Pre-create log file
"" | Out-File -FilePath $logFile -Encoding utf8 -Append

function Log($msg) {
    $line = "[{0}] {1}" -f (Get-Date -Format "HH:mm:ss"), $msg
    Write-Host $line
    Add-Content -Path $logFile -Value $line -Encoding utf8
}

function Get-LastPage($tmp) {
    if (Test-Path $tmp) {
        try {
            $stream = [System.IO.File]::Open($tmp, 'Open', 'Read', 'ReadWrite')
            $stream.Seek(0, 'End') | Out-Null
            $tailSize = 8192
            $stream.Seek(-1 * [Math]::Min($tailSize, $stream.Length), 'End') | Out-Null
            $reader = New-Object System.IO.StreamReader($stream, [System.Text.Encoding]::UTF8)
            $text = $reader.ReadToEnd()
            $reader.Close()
            $stream.Close()
            $matches2 = [regex]::Matches($text, $markerRegex)
            if ($matches2.Count -gt 0) {
                return [int]$matches2[$matches2.Count - 1].Groups[1].Value
            }
        } catch {
            return 0
        }
    }
    return 0
}

function Get-FileSize($tmp) {
    if (Test-Path $tmp) {
        return [long](Get-Item $tmp).Length
    }
    return 0
}

Log "==== Watcher started ===="
Log "baseDir = $baseDir"
Log "Gongtong: $gongtongFinal"
Log "Mankiw: $mankiwFinal"

# Wait for Gongtong to complete
Log "Waiting for GongtongFuyu OCR..."
$stuckCount = 0
$maxStuck = 8  # 40 min

while ($true) {
    $page = Get-LastPage $gongtongTmp
    $size = Get-FileSize $gongtongTmp

    if ((Test-Path $gongtongFinal) -or ($page -ge 391)) {
        Log "GongtongFuyu DONE! page=$page size=$size"
        if (Test-Path $gongtongTmp) {
            Move-Item -Path $gongtongTmp -Destination $gongtongFinal -Force
            Log "Renamed to: $gongtongFinal"
        }
        break
    }

    $pyProc = Get-Process python -ErrorAction SilentlyContinue
    if (-not $pyProc) {
        $stuckCount++
        Log "WARN: python not running, stuck=$stuckCount"
        if ($stuckCount -ge 3) {
            Log "ERROR: GongtongFuyu dead, exit"
            exit 1
        }
    } else {
        $stuckCount = 0
    }

    if ($page -ge 1) { $stuckCount = 0 }  # reset if progress

    Log "GongtongFuyu: page=$page/391 size=$size"
    Start-Sleep 300
}

# Start Mankiw
Log "==== Starting Mankiw OCR (from 138) ===="
Start-Process -FilePath python -ArgumentList @(
    $script, $mankiwPdf, $mankiwFinal, "--dpi", "150"
) -WorkingDirectory "d:\常用脚本\skills\cangjie-skill" -RedirectStandardOutput "D:\ocr_mankiw.log" -RedirectStandardError "D:\ocr_mankiw_err.log" -WindowStyle Hidden
Log "Mankiw started"
Start-Sleep 30

# Wait for Mankiw
$stuckCount = 0

while ($true) {
    $page = Get-LastPage $mankiwTmp
    $size = Get-FileSize $mankiwTmp

    if ((Test-Path $mankiwFinal) -or ($page -ge 544)) {
        Log "Mankiw DONE! page=$page size=$size"
        if (Test-Path $mankiwTmp) {
            Move-Item -Path $mankiwTmp -Destination $mankiwFinal -Force
            Log "Renamed to: $mankiwFinal"
        }
        break
    }

    $pyProc = Get-Process python -ErrorAction SilentlyContinue
    if (-not $pyProc) {
        $stuckCount++
        if ($stuckCount -ge 3) { Log "ERROR: Mankiw dead"; exit 1 }
    } else { $stuckCount = 0 }

    if ($page -ge 1) { $stuckCount = 0 }

    Log "Mankiw: page=$page/544 size=$size"
    Start-Sleep 300
}

Log "==== ALL OCR DONE ===="
