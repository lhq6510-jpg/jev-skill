# Accounting

The Python helper estimates CJK characters as one token each and other characters as one token per four. This is a heuristic, not a tokenizer or billing measurement. English code and Chinese can differ substantially; values are labeled estimates, with a sensitivity range of ±30% for text counts. Do not equate this range with a calibrated confidence interval.

For an unseen local task, input reduction may reduce the first model read. For a task already in the conversation, those tokens have already been consumed: recoverable first-read savings are zero. This skill cannot rewrite the host's history. Future retained context could still include the original, so default reuse savings are also zero.

Cost includes the instructions loaded for optimization, tool roundtrip/report overhead, and explicit semantic analysis/output. Unobserved reasoning is uncertain: estimate it conservatively, or skip. A helper estimate is a budget decision, not a measured result. Initial skill discovery metadata also has overhead, shared by normal and skill runs after installation; the helper's default reserve includes it approximately, not exactly.

Net = recoverable avoided input tokens minus extra optimization tokens. For hypothetical future reads, report `(original - candidate) * reuse_count` separately; never add this to realized savings. Output task-execution tokens are not compression savings; paired real runs include all inputs/outputs and elapsed time.

The benchmark compares two independent invocations of the same existing Agent on the same 10 tasks. A/B usage may vary because reasoning and tools are nondeterministic. One pair is an observation, not statistical proof. Cached tokens are still included in total consumed tokens; costs may differ from totals. When Usage is not available, record null for actual totals and separate estimates. Never substitute text-length ratios for total model consumption.
