# Operating systems, system calls and I/O

## Look outside the CPU hotspot

A request can be dominated by I/O waits, syscall overhead, scheduler interactions, page faults, file-system cache behavior, networking, serialization or queueing. Profile actual elapsed request time and traces before changing CPU arithmetic.

## Workload-specific techniques

- **Batching:** amortize syscalls, locks and per-request bookkeeping. Tradeoff: larger batches can worsen individual latency and p99.
- **Nonblocking/async I/O:** use when waiting on many independent operations; the runtime/event loop has overhead and is not needed for simple CPU-bound work.
- **Readiness models:** epoll (Linux), kqueue (BSD/macOS), IOCP (Windows) have different registration, lifecycle and cancellation semantics.
- **io_uring:** powerful Linux interface with kernel/version/security constraints; verify its concrete supported operations and benchmark against epoll/read/write paths.
- **Zero-copy:** only when measuring saved copies against ownership, pinning, alignment, page and API costs; 'zero-copy' APIs can still move bytes elsewhere.
- **Memory mapping:** helps some read-heavy workflows but introduces page-fault latency and storage-lifetime semantics; warm/cold tests required.
- **Buffering:** right-size buffers for expected message sizes and avoid synchronous logging/allocations on critical paths.

## What to record

Request latency distribution, syscall counts, scheduler waits, context switches, page faults, read/write bytes, queue depth, file-cache warm/cold state, network packet rates, dropped packets, CPU usage and error behavior.

## Correctness considerations

Partial reads/writes, EINTR, short buffers, cancellation races, resource lifetime, backpressure, shutdown, blocking in an event loop, file truncation during mmap, and untrusted packet/input parsing. Never trade error handling or memory safety for marginal throughput.

References: [Brendan Gregg, Systems Performance](https://www.brendangregg.com/systems-performance-2nd-edition-book.html), [Linux kernel docs](https://www.kernel.org/doc/html/latest/), [Microsoft WPR/WPA](https://learn.microsoft.com/en-us/windows-hardware/test/wpt/windows-performance-analyzer), [Apple Instruments](https://developer.apple.com/tutorials/instruments).
