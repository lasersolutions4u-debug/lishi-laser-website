# Claude Code 环境一键恢复脚本
# 用法: 在项目根目录右键 → "使用 PowerShell 运行"，或在终端输入:
#   powershell -ExecutionPolicy Bypass -File .claude-portable/restore.ps1

$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$TargetDir = "$env:USERPROFILE\.claude"

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Claude Code 环境恢复" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 1. 确保目标目录存在
if (-not (Test-Path $TargetDir)) {
    Write-Host "[1/5] 创建 .claude 目录..." -ForegroundColor Yellow
    New-Item -ItemType Directory -Path $TargetDir -Force | Out-Null
    Write-Host "       已创建: $TargetDir" -ForegroundColor Green
} else {
    Write-Host "[1/5] .claude 目录已存在" -ForegroundColor Gray
}

# 2. 恢复 settings.json
Write-Host "[2/5] 恢复 settings.json..." -ForegroundColor Yellow
$SourceSettings = Join-Path $ScriptDir "settings.json"
$TargetSettings = Join-Path $TargetDir "settings.json"

if (Test-Path $SourceSettings) {
    if (Test-Path $TargetSettings) {
        $backup = $TargetSettings + ".backup." + (Get-Date -Format "yyyyMMddHHmmss")
        Copy-Item $TargetSettings $backup
        Write-Host "       已备份旧文件: $backup" -ForegroundColor DarkYellow
    }
    Copy-Item $SourceSettings $TargetSettings -Force
    Write-Host "       settings.json 已恢复" -ForegroundColor Green
} else {
    Write-Host "       跳过 (源文件不存在)" -ForegroundColor Gray
}

# 3. 合并全局 CLAUDE.md
Write-Host "[3/5] 合并全局 CLAUDE.md..." -ForegroundColor Yellow
$SourceClaude = Join-Path $ScriptDir "CLAUDE.md"
$TargetClaude = Join-Path $TargetDir "CLAUDE.md"

if (Test-Path $SourceClaude) {
    $sourceContent = Get-Content $SourceClaude -Raw -Encoding UTF8

    if (Test-Path $TargetClaude) {
        $targetContent = Get-Content $TargetClaude -Raw -Encoding UTF8

        if ($sourceContent.Trim() -ne $targetContent.Trim()) {
            # 内容不同 → 合并
            $backup = $TargetClaude + ".backup." + (Get-Date -Format "yyyyMMddHHmmss")
            Copy-Item $TargetClaude $backup

            $merged = @"
$sourceContent

---

## Merged from previous computer ($(Get-Date -Format "yyyy-MM-dd"))

$targetContent
"@
            Set-Content -Path $TargetClaude -Value $merged -Encoding UTF8
            Write-Host "       已合并 (旧文件备份: $backup)" -ForegroundColor Green
            Write-Host "       请检查 $TargetClaude 确认合并结果" -ForegroundColor DarkYellow
        } else {
            Write-Host "       内容相同，跳过" -ForegroundColor Gray
        }
    } else {
        Copy-Item $SourceClaude $TargetClaude
        Write-Host "       已创建新文件" -ForegroundColor Green
    }
} else {
    Write-Host "       跳过 (源文件不存在)" -ForegroundColor Gray
}

# 4. 恢复项目记忆
Write-Host "[4/5] 恢复项目记忆..." -ForegroundColor Yellow
$SourceProjects = Join-Path $ScriptDir "projects"
$TargetProjects = Join-Path $TargetDir "projects"

if (Test-Path $SourceProjects) {
    if (-not (Test-Path $TargetProjects)) {
        New-Item -ItemType Directory -Path $TargetProjects -Force | Out-Null
    }
    Copy-Item "$SourceProjects\*" $TargetProjects -Recurse -Force
    Write-Host "       项目记忆已恢复" -ForegroundColor Green
} else {
    Write-Host "       跳过 (源目录不存在)" -ForegroundColor Gray
}

# 5. 完成
Write-Host "[5/5] 完成!" -ForegroundColor Yellow
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  恢复完成。请重启 Claude Code。" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 列出已恢复的内容
Write-Host "已恢复的内容:" -ForegroundColor White
if (Test-Path (Join-Path $TargetDir "settings.json")) {
    Write-Host "  ✓ settings.json" -ForegroundColor Green
}
if (Test-Path (Join-Path $TargetDir "CLAUDE.md")) {
    Write-Host "  ✓ CLAUDE.md (全局)" -ForegroundColor Green
}
if (Test-Path (Join-Path $TargetDir "projects\Euchio")) {
    Write-Host "  ✓ projects/Euchio/ (项目记忆)" -ForegroundColor Green
}
