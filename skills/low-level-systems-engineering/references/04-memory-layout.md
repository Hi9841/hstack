# Memory hierarchy, layout and bytes moved

## Think in cache lines, not just objects

CPUs fetch nearby data in cache lines. Effective performance depends on *where* data resides (register, L1, L2, LLC, local/remote DRAM), load dependencies, miss handling, TLB reach and write ownership. Accessing 1 byte of each far-flung allocation can be much slower than scanning contiguous bytes.

## Data layout decisions

- **Array of Structures (AoS):** convenient for per-object operations. **Structure of Arrays (SoA):** often better for scanning one field or vectorizing; profile mixed access patterns.
- **Hot/cold splitting:** separate frequently touched state from rare metadata to increase cache-line useful density.
- **Packing and alignment:** smaller structures can improve cache capacity, but unaligned access, SIMD load constraints, and false sharing may negate benefits.
- **Tiling/blocking:** reuse inputs and weights within a cache level before eviction; choose tile by target chip/registers and actual tensor shapes.
- **Cache-line padding:** isolate independently written per-thread counters when coherence traffic is measured; indiscriminate padding bloats memory.
- **NUMA:** prefer first-touch placement and locality for large multithreaded working sets; pinning can make scheduling or load balance worse.

## Count physical traffic

For a pipeline `A -> normalize -> quantize -> matmul -> activation`, identify each full read/write pass and any intermediate copy. An extra 100 MB materialization is costly even when the arithmetic is fast. Eliminate the data structure/pass first if downstream kernels can consume a different layout. Measure L1/L2/LLC traffic when counters allow; do not equate `malloc` count with memory bandwidth.

## Allocation ownership

Reserve capacities where growth is predictable, reuse scratch buffers only when lifetimes don't overlap, and initialize every byte before it is read. Buffer pools can worsen memory footprint or locality if they hold excess capacity, so test reuse versus retention. In-place work is safe only with dependency and alias invariants documented.

## Prefetch cautiously

Modern hardware prefetchers are effective on predictable streams. Manual prefetch can add overhead and pollute caches. Prefetch distance depends on latency, bandwidth, computation per iteration and access pattern; measure with representative working sets.

## Cache troubleshooting worksheet

- Actual shape and dtype of the data?
- Spatial and temporal locality? Access stride?
- Unique bytes and repeated reads/writes per stage?
- TLB footprint and page size? Huge pages relevant?
- Are different threads sharing read-only data or bouncing written cache lines?
- Are copies due to interface mismatch between two kernels?
- Does performance change when input fits L2, LLC, or DRAM?

See [Drepper's memory guide](https://www.akkadia.org/drepper/cpumemory.pdf) (older platform data; concepts remain valuable), [Roofline](https://escholarship.org/uc/item/78h8v7mr), and [Intel optimization](https://www.intel.com/content/www/us/en/developer/articles/technical/intel64-and-ia32-architectures-optimization.html).
