# token-optimize

一个可迁移的 [Agent Skills](https://agentskills.io/specification) Skill。主动调用后，使用当前 Agent 已有的大模型与本地能力，减少重复任务说明和无益工具上下文，然后继续完成任务。

**无需新 API Key、模型、Provider 或服务器。** 不自动拦截请求，不修改原始任务文件；不确定是否完整、代码难以安全改写或收益太小时使用原文。

## 安装与调用

下载本仓库（Code → Download ZIP），解压，找到仓库内的 `token-optimize/` 子目录，将这个包含 `SKILL.md` 的完整文件夹放入对应目录。不要覆盖已有同名 Skill；安装后重新打开 Agent 会话。

| Agent | 用户 Skill 目录 | 主动调用 |
|---|---|---|
| Codex | `~/.codex/skills/token-optimize` | `$token-optimize 你的任务` |
| Qwen Code | `~/.qwen/skills/token-optimize` | `/token-optimize 你的任务` |
| Kimi Code | `~/.agents/skills/token-optimize` | `/skill:token-optimize 你的任务` |
| OpenCode | `~/.agents/skills/token-optimize` | `/token-optimize 你的任务`，需下面的命令入口 |

`~` 表示你的用户主目录，Windows 通常为 `%USERPROFILE%`。需要执行本地脚本时使用已有 Python 3.9+；没有 Python 时 Agent 保留原文并继续任务。

### OpenCode 命令入口

把 `adapters/opencode/token-optimize.md` 复制到 `~/.config/opencode/commands/token-optimize.md`，然后退出并重新启动 OpenCode。它只调用同一个 Skill，没有独立的优化引擎，也不设置模型。

### 多个 Agent 共用一份文件

保留一份完整源目录，将上表中的目录用符号链接或 Windows Junction 指向它即可。OpenCode 和 Kimi 可共用 `~/.agents/skills/token-optimize`；Qwen 可从自己的 Skill 目录链接到同一源目录。请勿移动或删除链接指向的源目录。

其他支持 Agent Skills 的客户端：按其官方规定安装整个目录，使用原生 Skill 语法。文件结构符合规范并不保证所有宿主、版本、权限或模型均兼容。

## 工作方式与保护

- 本地脚本只处理高置信度的相邻完全重复段落和多余空行。
- 必要的语义分析使用当前 Agent 已有能力，核对要求清单；不调用额外远程模型。
- 保留目标、数字、单位、路径、URL、代码、技术标识、否定条件、格式和执行顺序。
- 原文已经进入模型上下文时，压缩不能追回已消耗 Token。
- 短任务直接执行；优化不应成为每个任务必须经过的额外调用。
- 优化后继续完成用户任务，不能只交付一份改写 Prompt。

## Token 数据

没有真实 Usage 时标注估算。统计包含原始输入、优化后输入、优化额外成本和预计净收益；加载 Skill、工具往返、语义分析也有成本，净收益可能为负。详细规则见 [measurement.md](references/measurement.md)。不承诺固定节省百分比。

## 验证范围

Windows 环境已完成 12 个本地安全测试；Codex 有真实 Skill 调用及任务完成记录，Kimi Code 2.1.1 有实际 Skill 工具加载与约束保留测试。OpenCode 1.18.31 已验证加载与命令注册，但原测试环境现有凭据返回 401；Qwen Code 0.23.2 已验证命令注册，但原测试环境套餐额度耗尽。因此后两项尚未验证模型执行成功。未验证其他客户端；上述结果不保证其他环境一定成功。

```sh
python -X utf8 -m unittest discover -s tests -p test_optimize.py -v
```

`tests/tasks.txt` 包含 10 项有明确验收结果的任务；`tests/evaluate.py` 可评价真实 Agent 答案。测试素材中的路径均是合成案例。这里不包含作者电脑的配置、凭据或原始模型会话日志。

## 卸载

移走你安装的 `token-optimize` Skill 文件夹或目录链接；OpenCode 用户另移走上述命令入口。不要删除共享源目录，除非其他 Agent 已经不再引用它。无需更改模型、Provider 或环境变量。

## 官方宿主文档

[OpenCode Skills](https://opencode.ai/docs/skills/) · [OpenCode Commands](https://opencode.ai/docs/commands/) · [Qwen Code Skills](https://qwenlm.github.io/qwen-code-docs/en/users/features/skills/) · [Kimi Code Skills](https://moonshotai.github.io/kimi-code/en/customization/skills)
