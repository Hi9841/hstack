# Concurrency, memory models and scheduling

## Threads do not equal free speed

Parallelism introduces scheduling, coordination and cache-coherence costs. Decide whether the goal is single-request latency, throughput at concurrency or energy efficiency. Choose task sizes that amortize dispatch and avoid many tiny jobs that merely occupy worker threads.

## Atomics and memory ordering

Memory safety is not established by 'it works under stress.' Identify the shared state, read/write operations, linearization point, happens-before edges, lifetime and reclamation protocol. Distinguish relaxed (atomicity, no synchronization), acquire/release (publication/synchronization with matching operations) and sequential consistency (stronger global ordering). Do not weaken ordering as an optimization without proof and concurrency model tests.

Common mistakes:

- Publishing a pointer without publishing initialized contents correctly.
- Freeing/reusing an object while another thread still accesses it.
- ABA effects in compare-and-swap loops.
- False sharing across independent counters or queues.
- Busy-waiting that steals CPU from the worker that must make progress.
- Spinlocks that fail under oversubscription or preemption.
- Sharing writable cache lines between many workers.

## Scheduling experiment

Test 1/2/4/... threads, short and long jobs, with SMT on/off if appropriate, under moderate competing load. Record wall time, total CPU time, context switches, actual CPU use, LLC misses and tail latency. Investigate NUMA locality only on machines with relevant topology. Evaluate bounded spin, park/unpark and inline small jobs; never assume a universal threshold.

## Parallel kernels

- Give each thread a contiguous block of the output, so that threads do not share written cache lines.
- Measure scaling at 1, 2, 4 and N threads. Compare physical cores with SMT threads.
- Check NUMA placement of the weights and the outputs on multi-socket machines.
- For small operations, thread-pool dispatch can cost more than the work. Measure the single-thread path; it is sometimes the fastest.

## Safer alternatives

Try immutable sharing, single-writer ownership, thread-local buffers and bounded channels before lock-free structures. Lock-free means a progress property, *not* automatically no contention or better latency. For lock-free queues, prove capacity/empty behavior, ordering, reclamation and fairness requirements.

## Correctness tests

Run deterministic schedule exploration for small Rust concurrency primitives with [Loom](https://github.com/tokio-rs/loom) (adapting synchronization types); use ThreadSanitizer where toolchain/runtime supports it; stress under varied thread counts. TSan does not prove correctness; exhaustive testing of all executions is generally infeasible.

Sources: [Rustonomicon atomics](https://doc.rust-lang.org/nomicon/atomics.html), [The Art of Multiprocessor Programming](https://shop.elsevier.com/books/the-art-of-multiprocessor-programming/herlihy/978-0-12-415950-1), [C++ Concurrency in Action](https://www.manning.com/books/c-plus-plus-concurrency-in-action-second-edition).
