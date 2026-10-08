# token-optimize

跨 Agent 的手动 Token 优化 Skill，使用当前 Agent 已有模型与本地能力，优化值得优化的任务后继续执行。

**仓库名称为 `jev-skill`，当前发布内容是独立的 `token-optimize`，不是官方 Jev，不调用 TypeSafe API，也不需要新的 API Key、模型或服务器。**

## 给朋友的安装步骤

1. 点击 **Code → Download ZIP**，解压。
2. 找到仓库内的 **`token-optimize/` 子目录**，将整个目录安装到你的 Agent Skill 目录。
3. 重新打开 Agent 会话，主动调用 Skill。

| Agent | Skill 安装路径 | 手动调用 |
|---|---|---|
| Codex | `~/.codex/skills/token-optimize` | `$token-optimize 你的任务` |
| Qwen Code | `~/.qwen/skills/token-optimize` | `/token-optimize 你的任务` |
| Kimi Code | `~/.agents/skills/token-optimize` | `/skill:token-optimize 你的任务` |
| OpenCode | `~/.agents/skills/token-optimize` | `/token-optimize 你的任务` |

OpenCode 还需复制 `token-optimize/adapters/opencode/token-optimize.md` 到 `~/.config/opencode/commands/token-optimize.md`，并重启 OpenCode。`~` 表示用户主目录；不要覆盖已有同名 Skill。

详细安装、共享目录、测试范围、成本估算与卸载方法见 **[token-optimize 使用说明](token-optimize/README.md)**。

不自动运行；原始任务与文件保持不变；不确定或无净收益时使用原文。没有固定节省率承诺。核心本地脚本使用已有 Python 3.9+，无 Python 时 Agent 按原文继续执行。

测试：12 项本地安全检查通过；Codex 与 Kimi 已有真实调用成功记录。OpenCode、Qwen 已确认加载/命令注册，原测试环境分别受现有凭据和额度限制，未验证模型任务执行成功。
