# Claude Code 便携配置包

## 一键恢复（推荐）

在项目根目录打开终端，运行：

**Windows PowerShell:**
```
powershell -ExecutionPolicy Bypass -File .claude-portable/restore.ps1
```

脚本自动处理：
1. 创建 `.claude` 目录
2. 恢复 `settings.json`（权限配置）
3. 合并全局 `CLAUDE.md`（不会覆盖你已有的内容）
4. 恢复项目记忆（本项目 8 个记忆文件）

## 手动恢复

```
xcopy ".claude-portable\*" "%USERPROFILE%\.claude\" /E /Y
```

## 包含内容

| 文件 | 说明 |
|------|------|
| `restore.ps1` | 一键恢复脚本 |
| `settings.json` | 用户设置和工具权限 |
| `CLAUDE.md` | 全局用户指令（gstack 使用规则等） |
| `projects/Euchio/memory/` | 本项目的 8 个记忆文件 |

## 恢复后

- 重启 Claude Code
- 如需 gstack skills: 在项目根目录运行 `gstack setup`
- 检查合并后的全局 `CLAUDE.md`（脚本会提示）
