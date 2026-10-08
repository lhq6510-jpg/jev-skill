---
name: token-optimize
description: Reduce avoidable task and tool-context overhead, then complete the task using this Agent's existing model. Use only on explicit invocation; retain uncertain requirements and skip work without positive estimated net benefit.
metadata:
  version: "1.0.0"
---

# Token optimize

Runtime: Python 3.9+ and local commands. No added API, key or service.

Only act on explicit invocation. Use the current Agent and its existing tools; never create a separate model call, background hook, or intercept other requests.

1. Identify the user's actual task. For short/clear input, code-heavy input, or doubtful payoff, continue directly with the original; do not repeat it or produce an optimization-only answer.
2. For a long task supplied in a local file, run `python <this-skill>/scripts/optimize.py --file <task-file> --unseen` before reading that file into model context. For text already in the conversation, its input cost is sunk: do not count shortening it as saved tokens. The helper defaults to original text unless estimated net benefit is positive. It never changes the input file.
3. Preserve goals, explicit requirements, identifiers, numbers/units, dependencies, sequence, negations and output format. Use local exact-duplicate/blank-line cleanup first. If complex prose could justify semantic compression, read [the semantic workflow](references/semantic.md); use your existing reasoning, inventory requirements, check the candidate, and revert on uncertainty. Do not merely assert equivalence.
4. Continue the original task within its authorized scope using the selected text. Preserve the original as authority. Avoid rereading unchanged files and duplicating bulky tool output; retrieve targeted excerpts and retain errors, decisions and dependencies. Never modify projects or files merely to compress context.
5. Report optimization costs only when useful/requested. Label estimates, include loaded instructions, tool/report overhead and semantic reasoning/output, and distinguish hypothetical future reuse from savings already incurred. Do not claim provider billing savings without actual Usage. See [measurement](references/measurement.md) only for detailed accounting.

On any helper failure, malformed result, uncertain intent, possible constraint loss, unsafe code rewrite or insufficient net benefit, use the original and keep working. If the host cannot execute commands, follow this workflow directly and disclose that local validation was unavailable. Never stop after presenting a compact prompt when you can execute the task.
