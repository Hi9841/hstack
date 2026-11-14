# Performance by Design: A C++ Guide

This document is a practical guide for writing native code that starts
close to the desired performance shape instead of requiring a long cleanup pass
after the prototype works.

The short version:

```text
Design hot paths as C-style code so costs, data flow, and algorithmic shape remain explicit.
Use C++ only where it gives real safety, clarity, or compile-time structure.
Do not rely on the compiler to erase bad data structures, allocations, copies,
string formatting, dynamic dispatch, or bad algorithmic complexity.
```

This is not an argument for rewriting the codebase in C. C++ gives useful tools:
namespaces, references, `nullptr`, `enum class`, `constexpr`, small template
specialization families, RAII at ownership boundaries, and operator overloads
for the public symbolic API. Those are worth keeping.

This is close in spirit to Branimir Karadžić's
[*Orthodox C++*](https://bkaradzic.github.io/posts/orthodoxc%2B%2B/) and the
broader C-like C++ mindset, but it is not a mechanical adoption of any external
style guide. The rule is practical: keep the C++ features that make our code
safer or clearer, reject the ones that hide work, and prove performance with
benchmarks.

The rule is narrower and more important:

```text
The public API may be expressive.
The internal implementation must be explicit.
```

In systems such as parametric CAD and computational geometry, evaluation paths
are not isolated utility code. Symbolic values, nonlinear solving, profile CSG,
selection, measurement layout, document export, meshing, and future simulation
all compose. Through composition, even a "minor" routine can run inside a solver
inner loop or CSG retry step, or become a browser interaction or export
bottleneck. Treat every routine as potentially performance-sensitive.
Measurement determines where to spend optimization effort, not where disciplined
design begins.

## Why This Document Exists

One early profile CSG implementation proved semantics: profile graphs, generated
boundaries, provenance, tolerance diagnostics, selection, export, and several
boolean cases. That work was useful. It also accumulated prototype-grade C++:

```cpp
std::vector<std::vector<SplitPoint>> split_points;
std::vector<SplitPoint> unique;
Segment fragment = segment;
std::ostringstream out;
std::string topology_id = ...;
```

That style made the implementation easy to extend locally, but expensive to
make fast later. It created several classes of avoidable cost:

- quadratic all-pairs intersection before broadphase pruning;
- nested heap allocations;
- per-fragment allocation and deep copies;
- strings and provenance carried through numeric topology passes;
- resampling during split instead of preserving analytic intervals;
- repeated sorting and deduplication of tiny heap-backed vectors;
- runtime kind branching inside inner loops;
- hidden deep copies of objects containing containers, strings, optional heavy
  payloads, symbolic values, and provenance records.

In one measured case study, targeted rewrites moved the gold scripting-layer
DXF fixtures from:

```text
constrained_mounting_plate    18.766 ms  ->  10.054 ms
dense_drill_pattern         3381.881 ms  ->  16.481 ms  (~205x faster)
stepped_boolean_bracket       31.516 ms  ->  10.048 ms
```

In that case study, the three-fixture total went from `3432.163 ms` to
`36.583 ms` in one repeat-5 sample. That is about `94x` faster overall, with one
fixture crossing a `200x` movement. The measurements come from the same gold
DXF workflow.

This is serious. A `2x` improvement might be ordinary tuning. A `10x`
improvement usually means the algorithm or data layout was wrong. A `100x` to
`200x` improvement is not "C++ got optimized"; it is proof that the original
architecture was doing the wrong work. That gap is larger than the ordinary
performance difference people expect between native C++ and Python for many
real workloads. In other words, writing native C++ in a heap-heavy,
object-heavy, string-heavy style can erase the advantage of choosing C++ in the
first place.

Bad C++ can be slower than Python for the operation the user actually cares
about. That does not mean Python loops are faster than native loops. It means a
pure-Python implementation can beat C++ code that repeatedly allocates, formats
strings, walks hash tables, copies rich objects, misses caches, and runs the
wrong algorithmic shape. Language choice does not rescue bad architecture.

The lesson is uncomfortable but important: prototype-grade C++ can be slow
enough that the language choice stops mattering. The winning change was not one
clever intrinsic or one compiler flag. It was removing avoidable work: fewer
containers, fewer allocations, fewer copies, less string/provenance traffic in
numeric loops, better pruning, and data shaped around the computation.

That improvement proves the original shape was wrong. It would have been
cheaper to build the fast shape first.

The purpose of this guide is to make that first implementation style more
repeatable.

## What Would Have Been Cheaper

Within the same case study, the dense drill fixture did not become about `205x`
faster because of a single magic trick. It moved because many pieces of
prototype C++ were removed or reshaped:

- all-pairs work was pruned before expensive routines where possible;
- rich copied `Segment` objects were replaced or bypassed in hot paths;
- nested scratch vectors were moved toward flat retained buffers;
- source/provenance strings were moved out of topology identity and hot
  comparison paths;
- small ID lookups moved to specialized ID tables instead of generic maps;
- repeated temporary allocation was replaced with retained scratch storage;
- diagnostic formatting stopped being paid on the success path;
- exact end-to-end gold benchmarks made regressions visible.

The important point is not that every individual change was large. Many were
small and some were rejected after benchmarking. The large speedup came from
the accumulated removal of avoidable work from a path that ran many times.

A later CSG slice from the same case study is a useful example of how to choose
the right level of attack. The split-heavy edge-notch gold fixture still took
about `24.894 ms` after many local CSG cleanups. A local in-place
segment-reversal cleanup was tested and rejected because it did not move the
gold run. The real win was one level higher: `difference(base, *cutters)` was
still executing as many sequential binary booleans even when the cutters were
independent. Batching those independent cutters into one multi-loop cutter
region moved the focused edge-notch benchmark from roughly `28-29 ms` to
`5.633 ms`, and the gold fixture from `24.894 ms` to `10.887 ms`.

The lesson is direct: when the profile says a phase is being repeated, first
ask whether the whole phase can be removed, batched, or reordered under a clear
invariant. Only tune the local loop after the algorithmic shape is right.

Writing the fast shape first would have meant:

1. Lower user-facing geometry into compact numeric arrays before boolean work.
2. Keep names, provenance, Python-visible dictionaries, and diagnostic strings
   in cold side tables.
3. Use integer topology/source keys during computation.
4. Allocate one retained workspace for split points, pair candidates,
   fragments, classification scratch, and validation scratch.
5. Add broadphase before pair intersections.
6. Write specialized line/arc/parametric kernels instead of carrying rich
   generic objects through every pair.
7. Attach provenance only after topology survives filtering and assembly.
8. Put gold end-to-end fixtures in place before optimizing so every slice has a
   guardrail.

That is the expected first-pass shape for similar implementations. A correctness
prototype that intentionally violates it must be labeled temporary and have a
rewrite plan. Otherwise it will become production debt.

## The Most Common Agent Failure Mode

Agents tend to write "canonical modern C++" because it looks safe, idiomatic,
and locally correct:

```cpp
std::vector<T> out;
std::unordered_map<Key, Value> map;
std::string name;
std::optional<Metadata> metadata;
std::function<void(...)> callback;
std::ostringstream message;
```

These are convenient default tools, and for tests, scripts, bindings, and cold
API glue they can be fine. They are the wrong default for code that performs
the underlying computation.

The failure pattern is usually:

1. Implement a feature with rich objects because that is locally easy.
2. Put everything needed by any consumer into one record.
3. Use standard containers because they make ownership easy.
4. Use strings because they are human-readable and stable.
5. Add correctness tests.
6. Extend the feature repeatedly.
7. Discover that the "small" path is now called thousands of times.
8. Benchmark and find that the cost is allocation, copying, lookup, formatting,
   and topology shape, not the actual math.
9. Spend multiple iterations undoing the original data model.

That is what happened in parts of the codebase. Do not repeat it.

## The Compiler Will Not Fix This

The "zero-overhead abstraction" phrase is often misused. The compiler can
inline simple functions, remove dead stores, fold constants, and optimize
obvious loops. It cannot turn an unsuitable architecture into a good one.

The compiler generally cannot remove:

- heap allocation required by container growth;
- allocator bookkeeping;
- cache misses caused by pointer-heavy object graphs;
- branchy runtime dispatch selected by stored kinds or virtual calls;
- string formatting;
- hash-table probes with unpredictable memory access;
- deep copies that are semantically observable;
- poor broadphase or no broadphase;
- O(n^2) pair generation when the algorithm asked for every pair;
- debug-build overhead from layered templates and standard-library iterators;
- compile-time cost from abstraction stacks.

Even when optimized builds recover some overhead, debug builds remain important.
The codebase is developed, tested, debugged, and benchmarked in local debug builds.
Slow debug builds reduce iteration speed and hide algorithmic thinking behind
toolchain patience.

Design for explicit work. Then let the compiler optimize that.

## Design The Computation First

Before writing a new native subsystem, answer these questions:

```text
What is the hot loop?
How many times can it run per user action?
Can it run inside nonlinear solve retries?
Can it run once per segment, pair, residual, sample, cell, or element?
What data does the hot loop actually need?
What data is only needed for diagnostics, API identity, selection, or export?
Where is memory allocated?
Can the same workspace be reused between evaluations?
What is the expected tiny, medium, large, and pathological size?
What benchmark will catch a regression?
```

Do this before choosing public-facing class shapes or standard containers.

The public object model can remain ergonomic:

```text
Circle
Rectangle
Profile
Boundary
Solution
Selection
Document
```

The implementation should lower those objects into compact arrays and side
tables:

```text
HotSegment[]
HotVertex[]
HotLoop[]
PairCandidate[]
SplitPoint[]
FragmentRecord[]
ColdSourceTable
ColdDiagnosticTable
```

The conversion boundary is deliberate. Public objects exist for UX. Hot records
exist for computation.

## Hot Data And Cold Data

Hot data is the minimum numeric state needed by the algorithm:

```text
kind tags
numeric coordinates
parameter interval endpoints
orientation
tolerance
source integer ids
loop ids
compact topology keys
```

Cold data is everything needed later:

```text
strings
debug paths
names
symbolic Value handles
Python objects
rich provenance lists
docstrings
sample buffers
human-readable topology ids
selection descriptions
```

The hot record should carry integer handles into cold tables, not cold payloads.

Bad shape:

```cpp
struct Segment {
    SegmentKind kind;
    NumPoint a;
    NumPoint b;
    SymbolicPoint sa;
    SymbolicPoint sb;
    std::vector<SourceRef> a_sources;
    std::vector<SourceRef> b_sources;
    std::vector<FragmentSourceProvenance> provenance;
    std::optional<ParametricCurveSegment> parametric;
    std::vector<NumPoint> parametric_samples;
    std::string topology_id;
};
```

Better shape:

```cpp
struct HotSegment {
    uint32_t source_id;
    uint32_t loop_id;
    uint32_t first_cold_ref;
    uint16_t kind;
    uint16_t flags;
    double p0[2];
    double p1[2];
    double data[4];
    double t0;
    double t1;
    double tolerance;
};
```

The second record is not the final exact record. It shows the direction:
copy-cheap numeric fields in the hot path, rich information elsewhere.

## Ownership Rules

Hot records should usually be POD or close to POD. A record that is repeatedly
scanned, sorted, split, copied, or written into workspace should not own:

- `std::string`;
- `std::vector`;
- `std::unordered_map`;
- `std::optional` with heavy payloads;
- `std::shared_ptr`;
- Python/pybind objects;
- arbitrary callbacks;
- rich provenance objects.

If a hot record cannot be safely copied with `memcpy`, treat that as a design
smell. There are exceptions, but they need a clear reason.

Use ownership at the edges:

```text
Public API object owns user-visible structure.
Lowering step writes compact records into workspace.
Computation operates on pointer/size ranges.
Result assembly writes retained output and cold metadata.
Diagnostics expand ids into readable messages only on failure or output.
```

## Allocation Rules

Prefer explicit workspaces and arenas built on C allocation primitives:

```text
malloc
calloc when zeroing is truly needed
realloc for retained capacity growth
free
aligned_alloc for alignment-sensitive arrays
alloca only for tiny bounded scratch
```

Do not allocate in loops that run per:

```text
segment
vertex
pair
split point
fragment
residual
solver iteration
mesh element
sample
selection candidate
```

Preferred workspace shape:

```cpp
struct CsgWorkspace {
    HotSegment* segments;
    SegmentAabb* bounds;
    PairCandidate* pairs;
    SplitPoint* split_points;
    uint32_t* split_offsets;
    FragmentRecord* fragments;

    uint32_t segment_count;
    uint32_t pair_count;
    uint32_t split_count;
    uint32_t fragment_count;

    uint32_t segment_capacity;
    uint32_t pair_capacity;
    uint32_t split_capacity;
    uint32_t fragment_capacity;
};
```

Reset should normally set counts to zero. It should not free capacity.

Avoid this shape:

```cpp
std::vector<std::vector<SplitPoint>> splits(segment_count);
for (...) {
    std::vector<SplitPoint> local;
    ...
}
```

Write this shape instead:

```text
split_counts[segment_count]
prefix sum -> split_offsets[segment_count + 1]
split_points[total_split_points]
sort/dedupe each segment range in place
```

If total counts are not known upfront, use a retained append buffer with
explicit capacity growth. The growth is visible and can be benchmarked.

## Small Fixed Storage

For small fixed numeric storage, use plain arrays or fields:

```cpp
struct SmallValue {
    int dim;
    double lane[4];
};
```

Do not use a standard-library type just to avoid writing `[4]`.

Plain arrays have advantages:

- layout is obvious;
- generated code is easy to inspect;
- debug builds do less abstraction work;
- initialization is explicit;
- copying cost is visible;
- the code looks like the data the CPU sees.

Use `std::array` only when it clearly solves a problem that plain arrays do not.
For hot records, that is uncommon.

## Avoid Eager Writes

Removing allocation is not enough. Writes also cost time, cache bandwidth, and
debug-build overhead.

The symbolic evaluation scratch rewrite only became a broad win after removing
unnecessary initialization:

```cpp
eval_slot.value = zero_value(value.dimension()); // overwritten before read
eval_slot.grad = SmallValue{};                   // initialized lazily
for (...) { eval_slot.input_slot[i] = 0; }        // unused slots never read
```

The accepted version writes only fields needed before evaluation:

```cpp
EvaluationSlot& slot = scratch.slots.push();
slot.id = id;
slot.source = &value;
slot.has_grad = false;
```

This is a useful lesson. A C-like design is not only about avoiding STL. It is
about knowing exactly which bytes are written and why.

## ID Tables, Not Generic Hash Maps

The codebase uses specialized ID-keyed tables under
`sources/id_tables`. They are not a generic hash map library.
They are a family of narrow, specialized data structures:

```text
IdSet64
SmallIdSet16
IdRevisionMemo64
TouchedIdSlotIndex
```

The reason for keeping variants is performance. Different call sites need
different storage:

- insert-only duplicate suppression;
- tiny traversal dedupe;
- ID-to-revision memoization;
- retained ID-to-slot indexing with touched-bucket reset.

Do not merge variants for aesthetic deduplication if benchmarks get worse.
Common style, common field names, and common tests are valuable. Shared code is
only valuable when it does not cost performance.

When adding a new ID table:

1. Place it alongside related specialized ID structures.
2. Define its exact call-site purpose.
3. Add tests at inline capacity, first table promotion, growth, duplicate
   behavior, zero/sentinel handling, and clear/reuse behavior.
4. Add benchmarks at tiny, transition, medium, large, and extra-large sizes.
5. Keep it only if the target call-site benchmark wins or stays neutral where
   allocator pressure matters.

## Strings Are Presentation Data

Do not use strings as hot topology identity.

Bad:

```cpp
std::string source_stable_key(const SourceRef& source);
std::string fragment_source_identity(const FragmentSourceProvenance& source);
std::string vertex_source_identity(const VertexSourceProvenance& source);
```

String identity is expensive:

- formatting floats is slow;
- `std::ostringstream` is especially slow;
- strings allocate;
- string hashing and comparison walk bytes;
- string lifetime creates ownership questions;
- human-readable formatting leaks into numeric algorithms.

Use compact numeric identity instead:

```text
uint64_t source_id
uint64_t topology_id
TopologyKey128
source_t0/source_t1 as numeric fields
```

Build public strings only as a formatting view over numeric identity and cold
provenance tables. If diagnostics need human-readable text, expand it after the
computation has already identified the failing operation or retained output
element.

## Algorithm Beats Micro-Optimization

Data layout matters. Algorithmic shape matters more.

One production-proven CSG pipeline shape is:

1. Lower profile graph into compact numeric segment arrays and cold side tables.
2. Compute AABBs once.
3. Use broadphase pruning before pairwise intersection.
4. Dispatch into specialized pair kernels.
5. Store split points in flat buffers.
6. Sort/dedupe per-segment ranges in place.
7. Build compact fragment interval records.
8. Classify compact fragments.
9. Assemble loops.
10. Attach provenance and diagnostics after topology is settled.

Do not write all-pairs first and plan to "optimize later" unless the bounded
input size is part of the contract. For profile CSG, it is not.

The nonlinear solver has the same rule. It can polish roots; it cannot be the
only mechanism for enumerating all intersections. Candidate enumeration,
interval pruning, and certified topology belong to the CSG algorithm.

## Specialized Routines Over Runtime Branching

This is better at the top level:

```cpp
switch (pair_kind) {
    case LineLine: intersect_line_line(...); break;
    case LineArc: intersect_line_arc(...); break;
    case ArcArc: intersect_arc_arc(...); break;
}
```

This is worse inside the deepest loop:

```cpp
for (Pair p : pairs) {
    if (a.kind == Line && b.kind == Arc) { ... }
    else if (...) { ... }
}
```

The best shape depends on pair counts and code locality, but the principle is:
sort, bucket, or dispatch work so the expensive math loops are specialized and
predictable. Avoid carrying generic objects through every operation if the kind
is known.

## Rich Public APIs, Explicit Internals

It is good for users to write:

```python
plate = circle(origin2, 50) - circle(origin2, 8)
edge = plate.boundary.select(source=rect.right_side).only()
```

That does not mean the CSG implementation should operate on Python-like objects,
inheritance trees, strings, or rich `Segment` records.

Public and internal APIs serve different goals:

```text
Public API: readable, compositional, ergonomic, debuggable.
Internal API: compact, typed, allocation-aware, benchmarked, portable.
```

Bridge them explicitly. Do not blur the layers.

## Error Handling And Diagnostics

The system needs rich diagnostics. Rich diagnostics do not belong in hot records.

The internal implementation should return compact issue codes and IDs:

```text
operation_id
segment_id
vertex_id
loop_id
issue_code
retryable flag
tolerance snapshot id
```

After failure or output retention, expand those IDs into:

```text
human-readable path
source names
topology ids
formatted parameter intervals
diagnostic strings
Python objects
```

Do not format strings or allocate diagnostic payloads while scanning every
candidate pair. That is paying failure-reporting cost on the success path.

Avoid exceptions as normal control flow. Existing code still uses exceptions at
API boundaries and some legacy paths. New implementations should
prefer explicit status objects, issue buffers, and retryable failure codes,
especially for solver-driven CSG where a failure may simply mean "try another
initialization or step."

## Tests Are Not Enough

Correctness tests prove behavior. They do not prove performance shape.

Every performance-sensitive change needs:

- correctness tests;
- microbenchmarks for the affected routine;
- small, medium, and large benchmark regimes;
- transition-point benchmarks for inline-to-heap or table-promotion thresholds;
- at least one representative end-to-end benchmark when the affected code
  participates in a larger workflow.

Do not trust one benchmark size. A change can win for 64 items and lose for 4,
256, or 4096. This has already been seen with ID-table threshold experiments and
CSG visited-set variants.

Benchmark documentation should record rejected attempts. Rejections are useful
architecture data.

## Debug Builds Matter

Local development currently measures many paths in debug builds. Debug
performance matters because:

- tests run in debug builds;
- benchmark iteration often starts in debug builds;
- browser/demo integration needs responsive local development;
- abstractions that are "free in release" can make debug work painful;
- slow debug builds hide architecture problems until late.

Do not dismiss a debug-build regression if the path is important. First ask why
the debug path got slower. The answer often exposes real excess abstraction or
memory traffic.

## Review Pattern For Agents

After each nontrivial implementation step, stop and ask at two levels.

Local level:

```text
Does the code pass tests?
Does the measured target improve?
Did I preserve semantics?
Did I stage only task-owned files?
```

Architecture level:

```text
Did I put the code in the right subsystem?
Did I add another local ad-hoc implementation that should be isolated?
Did I mix hot numeric data with cold metadata?
Did I introduce ownership or allocation into a future hot path?
Did I choose standard containers because they were convenient?
Did I design for the long-run target or only this patch?
Would I be comfortable copying this pattern into the next subsystem?
```

This matters. It is possible to make a local benchmark better while making the
codebase worse. It is also possible to make a cleaner abstraction that costs
performance. Neither is acceptable.

The right result is both:

```text
cleaner composition
measured performance win or justified neutral allocator reduction
```

## Practical Recipe For New Components

Use this sequence when adding a new core subsystem.

### 1. Define the hot operation

Write down the operation in terms of counts:

```text
N segments
M candidate pairs
K split points
R residual rows
C constraint rows
E mesh elements
```

If there is no count model, the implementation is not ready.

### 2. Define hot records

Create compact records with numeric fields and IDs. Avoid owning containers.
Make the copy cost obvious.

### 3. Define cold side tables

Put names, strings, provenance, symbolic values, language-runtime or binding
references, and debug payloads outside the hot record. Refer to them by integer
IDs.

### 4. Define workspace ownership

Decide where scratch memory lives and how it is reused. Do not let allocation
appear organically inside loops.

### 5. Define algorithms before code

For CSG, this means broadphase and specialized pair kernels. For solving, this
means residual/Jacobian assembly and linear solver strategy. For meshing, this
means spatial indexing and element-quality loops.

### 6. Add tests and benchmarks first or with the slice

Tests should cover correctness and edge cases. Benchmarks should cover size
regimes and transition points.

### 7. Implement the smallest coherent slice

Small is good, but not at the cost of architecture. Sometimes the smallest
coherent slice is a new private header or subsystem, not a local struct inside
a very large implementation file.

### 8. Measure before and after

Record results. If the change is mixed, do not hand-wave. Either tune it,
restrict it to the winning call site, or reject it.

### 9. Commit only a complete measured slice

The commit should include code, relevant tests and benchmarks, and the measured
results.

## What To Use From C++

Use:

- `namespace`;
- `enum class`;
- `constexpr`;
- references for required inputs;
- `nullptr`;
- simple templates for fixed-size variants;
- operator overloads for public symbolic/user-facing math where they improve
  readability;
- RAII wrappers at ownership boundaries;
- `static_assert` when it protects a layout contract.

Use carefully:

- `std::vector` as a top-level retained owner outside a hot loop;
- `std::string` in API/binding/diagnostic layers;
- `std::optional` for cold configuration or small scalar payloads;
- exceptions at API boundaries and tests;
- templates when they reduce real duplication without harming compile/debug
  cost.

Avoid by default:

- `std::vector<std::vector<T>>`;
- `std::unordered_map` and `std::map`;
- `std::string` and `std::ostringstream`;
- `std::function`;
- virtual dispatch per element;
- inheritance-heavy geometry kernels;
- hidden ownership in records scanned by numeric passes;
- `new`/`delete` per item;
- broad "generic reusable" containers that erase call-site-specific performance.

## How To Decide If An Abstraction Is Good

An abstraction is good when it:

- removes real complexity;
- keeps ownership and allocation visible;
- preserves or improves measured performance;
- has a narrow contract;
- has tests and benchmarks;
- makes the next similar implementation easier without forcing it through a
  slower shape.

An abstraction is bad when it:

- hides allocation;
- hides copies;
- generalizes across call sites with different performance needs;
- mixes hot and cold data;
- adds dynamic dispatch;
- exists only to make code look idiomatic;
- makes debug builds much slower;
- forces future code to inherit a poor data layout.

The codebase should prefer a small family of specialized routines over one generic
"elegant" abstraction that costs performance.

## How To Reflect After Each Slice

Every performance iteration should end with this audit:

```text
Did the target benchmark improve?
Did adjacent benchmarks stay neutral or improve?
Did small, medium, and large regimes hold?
Did representative end-to-end benchmarks stay healthy?
Did allocation pressure go down?
Did code composition improve?
Did I move local infrastructure into the right subsystem?
Did I avoid creating a generic library where specialized routines are better?
Did I document rejected attempts?
```

If the answer is mixed, do not force the patch through. Tune it, narrow it, or
reject it.

## The Real Standard

The standard is not "never use STL" and not "write everything in C." The
standard is:

```text
Every byte moved, every allocation, every branch, every lookup, and every
algorithmic pass should be intentional.
```

Write code that makes the work visible. Then benchmark it.
