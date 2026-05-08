---
name: Switch Computer — Claude Code Restore
description: One-liner to restore Claude Code environment when switching to a new computer
type: reference
originSessionId: d92658f1-5cfd-47cf-9e52-7135a4796411
---
# 换电脑恢复 Claude Code 环境

## 执行命令

在项目根目录运行：

```powershell
powershell -ExecutionPolicy Bypass -File .claude-portable/restore.ps1
```

## 前提条件
- 坚果云已同步，项目文件到位
- Claude Code 已安装
- 在项目根目录（`网站/`）执行

## 脚本做了什么
1. 恢复 `settings.json`（权限配置）
2. 合并全局 `CLAUDE.md`（不覆盖已有内容）
3. 恢复项目记忆

## 之后
- 重启 Claude Code
- 如需 gstack: 运行 `gstack setup`
