---
name: low-level-systems-engineering
description: Evidence-first optimization of native systems software. Use for performance, memory, concurrency, allocator, networking, CPU-kernel, SIMD, compiler, or inference work in Rust, C, C++, Zig, x86-64, or AArch64 when correctness, portability, or resource budgets matter.
---

# Low-level systems engineering

Use an evidence-first loop to improve a real workload. Preserve behavior,
memory safety, numerical policy, concurrency guarantees, supported targets, and
maintenance limits. A microbenchmark or an elegant patch is evidence only when
it explains a product-level result.

## Workflow

1. **Set the contract.** Read the repository instructions and current test and
   benchmark harnesses. Record the exact end-to-end boundary and target metric, representative inputs,
   correctness and numerical rules, safety and concurrency invariants, resource ownership, supported CPUs and
   operating systems, resource budgets, and unacceptable regressions. Define
   the minimum useful change, tail and footprint budgets, a sample plan, and one
   uncertainty or stop rule before the baseline run. Choose the rule. Do not
   write "use the repository rule or a bootstrap" without selecting one. If a required value is unknown,
   mark the work as a proposal and list the missing decision input.

   Done means a written pass/fail gate exists for every required metric and
   correctness rule, or each missing gate is named.

2. **Measure the baseline.** Rebuild the current revision with the intended
   release settings. Run a representative workload and record the revision,
   compiler, flags, CPU and ISA, operating system, thread count, frequency or
   thermal state when available, input distribution, cache state, raw samples,
   and summary statistics. Do not report measurements that you did not run.

   Done means another engineer can identify the binary, workload, environment,
   and raw baseline data.

3. **Find the bottleneck.** Use end-to-end timing plus a suitable profile,
   trace, counter set, allocation record, scaling test, or I/O evidence. Prove
   that the suspected work affects the target metric. Classify the limit as
   algorithmic, serial, compute, front end, back end, cache, memory traffic,
   allocation, I/O, synchronization, scheduling, or dispatch. Load only the
   reference that matches the observed limit.

   Done means the artifact names the bottleneck, its evidence, and the part of
   the product path that it can affect. A hot function alone is not enough.

4. **State one hypothesis.** Write one causal sentence: change X because
   mechanism Y should reduce cost Z. Add the expected measurement or counter
   movement, an upper-bound estimate when useful, and the main regression risk.
   Treat Amdahl, Roofline, cache, and instruction models as estimates with
   stated assumptions.

   Done means the hypothesis can fail, and the experiment names what would
   falsify it.

5. **Run one controlled experiment.** Make the smallest change that tests the
   hypothesis. Keep baseline and candidate comparable. Use warmups and a
   representative workload. Interleave or randomize A/B runs when drift can
   matter. Prevent dead-code elimination, constant folding, accidental input
   changes, and unguarded ISA use. Inspect generated code or counters only when
   they test the stated mechanism. Record every raw result, not only the best.

   Done means the diff, build, workload, run order, sample count, and raw data
   are recorded.

6. **Verify correctness and portability.** Run the repository's functional
   tests and the checks that fit the change: differential or exact-output tests,
   edge and tail cases, randomized or property tests, stress tests, numerical
   checks, sanitizers, race or model checks, memory checks, and every supported
   ISA fallback. Check aliasing, initialization, lifetime, overflow, error
   paths, cancellation, and resource ownership when they apply. For shared state, unsafe code, or resource lifetime changes, state the invariant and its acceptance test. Otherwise mark those checks not applicable. Do not weaken
   a correctness or safety check to obtain a speedup.

   Done means each applicable gate has a pass result or an explicit unavailable
   or not-run result with its risk.

7. **Compare and decide.** Compare the predeclared primary metric and secondary
   budgets with the same workload and environment. Report medians and relevant
   tails, spread or confidence method, sample count, and raw-data location.
   Keep the change only when the product-level result clears the predeclared
   threshold, the selected uncertainty rule supports the claim, and all required
   correctness gates pass. Otherwise revert it or label the result inconclusive
   and state the next measurement. A proposal with no measurements is always
   inconclusive. Never convert a missing threshold into an invented pass.

   Done means the report says **keep**, **revert**, or **inconclusive**, and
   cites the evidence for that status.

Order governs presentation, not disclosure. Report a discovered safety or
correctness blocker as soon as you find it. If a tool, counter, fixture, or
target is unavailable, name the gap and use a defensible alternative.

## Reference routing

- Workflow, baselines, experiment records: [performance workflow](references/01-performance-workflow.md)
- Bounds and bottleneck models: [performance models](references/02-performance-models.md)
- Pipelines, counters, branches, and code generation: [CPU architecture](references/03-cpu-architecture.md)
- Layout, locality, cache, TLB, NUMA, and traffic: [memory layout](references/04-memory-layout.md)
- Kernels, SIMD, tails, and ISA dispatch: [SIMD and kernels](references/05-simd-and-kernels.md)
- Compiler choices, LTO, PGO, and assembly: [compilers and assembly](references/06-compilers-and-assembly.md)
- Threads, atomics, ordering, and reclamation: [concurrency](references/07-concurrency.md)
- Files, sockets, syscalls, scheduling, and backpressure: [I/O and systems](references/08-io-and-systems.md)
- Benchmark design, profilers, and statistical comparison: [benchmarking and profiling](references/09-benchmarking-profiling.md)
- UB, fuzzing, sanitizers, and security: [correctness and security](references/10-correctness-and-security.md)
- Inference, quantization, decoding, and numerical policy: [inference and numerics](references/11-inference-and-numerics.md)
- Primary-source index and evidence order: [SOURCES.md](SOURCES.md)
- Reusable records: [experiment template](templates/experiment.md) and [performance report](templates/performance-report.md)

## Response contract

For an optimization task, report these items in order:

1. target, constraints, and predeclared gates;
2. baseline and bottleneck evidence;
3. hypothesis, mechanism, and risk;
4. changed code or proposal;
5. correctness and portability results;
6. before and after data with uncertainty;
7. limitations;
8. keep, revert, or inconclusive decision.

If no code changed, say **proposal**. If no measurement ran, say **unmeasured**.
Never invent performance numbers, test results, or tool output.



