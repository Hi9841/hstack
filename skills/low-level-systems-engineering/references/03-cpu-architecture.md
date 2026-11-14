# CPU microarchitecture and hot loops

## Mechanical sympathy is processor-specific

An instruction is not 'one cycle.' On modern out-of-order processors, distinguish instruction *latency* along a dependency chain from reciprocal *throughput* across independent operations, and from overall kernel runtime. Decode/uop cache, rename/issue queues, load/store subsystem, branch predictor, vector units, cache and memory each can limit rate.

## Practical pipeline investigation

1. Profile full application and identify real hot instruction addresses.
2. Inspect optimized assembly (not debug build); confirm vector width, spills, call overhead, loop trip counts and memory access pattern.
3. Use hardware counters appropriate to the CPU: retired instructions/cycles, branches/misses, backend or frontend stalls, cache/TLB misses. Vendor event names and semantics vary; generic `cache-misses` is not an exact 'DRAM misses' counter.
4. Check whether arithmetic has a long chain; independent accumulators can allow more overlap until registers spill.
5. Check if loop unrolling bloats instruction-cache footprint or harms branch prediction.
6. Measure on the actual target CPU and compare more than one input shape.

## Branch prediction

Branches are not intrinsically slow; correctly predicted branches may be cheaper than extra instructions and data dependencies in a branchless rewrite. Prefer rearranging data or control flow to make common cases simple. Benchmark unpredictable inputs, not just sorted or uniform test data.

## SIMD width and frequency

Wider vectors are not an unconditional win. AVX-512 throughput, core frequency effects, lane occupancy, register pressure, gather/scatter behavior, and tail costs differ by microarchitecture. Feature-detect at runtime before using unsupported instructions. Align assumptions with Rust/C/C++ ABI and storage semantics; unaligned loads may be efficient but page crossings can matter.

## Useful diagnostic patterns

| Evidence | Suspect | Next test |
|---|---|---|
| High branch misses | unpredictable condition | sort/restructure data or compare branchless path |
| Low IPC + backend wait | dependencies, cache miss or port bottleneck | load latency, memory pattern, instruction mix |
| Large instruction count | unnecessary work or poor codegen | eliminate loops, inspect assembly |
| Throughput plateau under threads | memory/coherence/serialization | vary thread count and working set |
| Stack spills in inner loop | register pressure | shrink tile/unroll or change layout |

Vendor references: [Intel optimization](https://www.intel.com/content/www/us/en/developer/articles/technical/intel64-and-ia32-architectures-optimization.html), [AMD docs](https://docs.amd.com/), [Arm docs](https://developer.arm.com/documentation), [Agner Fog](https://www.agner.org/optimize/), [uops.info](https://uops.info/). Vendor and measurement are both necessary; neither a single IPC number nor generic folklore proves causality.
