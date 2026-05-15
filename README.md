# The Torchbearer

**Student Name:** Angel Davila
**Student ID:** 130670316
**Course:** CS 460 – Algorithms | Spring 2026

---

## Part 1: Problem Analysis

- **Why a single shortest-path run from S is not enough:**
  Dijkstra from S gives us the cheapest way to reach each node in isolation, but it does not consider the cost of traveling between relics in sequence.

- **What decision remains after all inter-location costs are known:**
  Even with all pairwise shortest-path distances considered, we must still choose the order in which to visit the relics, since the way we put things together result in different fuel costs.

- **Why this requires a search over orders:**
  No greedy rule guarantees the globally cheapest sequence, so we must search over relic orderings and prune branches that cannot beat the best solution found so far.

---

## Part 2: Precomputation Design

### Part 2a: Source Selection

| Source Node Type | Why it is a source |
|---|---|
| Spawn node (S) | The route begins here, so we need shortest distances from S to every relic. |
| Each relic node | After visiting a relic we travel to the next relic or to the exit, so we need shortest distances from every relic to every other node. |

### Part 2b: Distance Storage

| Property | Your answer |
|---|---|
| Data structure name | Nested dictionary (dict of dicts) |
| What the keys represent | Source node (outer key), destination node (inner key) |
| What the values represent | Minimum fuel cost (shortest-path distance) from the outer-key node to the inner-key node |
| Lookup time complexity | O(1) average |
| Why O(1) lookup is possible | Python dicts use hash tables, so both the outer and inner key lookups are O(1) average. |

### Part 2c: Precomputation Complexity

- **Number of Dijkstra runs:** 1 + k (one from spawn, one from each of the k relics)
- **Cost per run:** O((V + E) log V) using a binary min-heap
- **Total complexity:** O((1 + k)(V + E) log V)
- **Justification:** We run one Dijkstra per source node, and each run costs O((V + E) log V), so the total can be simplified to the amount of sources times their run cost.

---

## Part 3: Algorithm Correctness

### Part 3a: What the Invariant Means

- **For nodes already finalized (in S):**
  The current distance in the node represents the best global path and there is not anything else to improve

- **For nodes not yet finalized (not in S):**
  The current distance isn't yet confirmed to be the best option and could still be improved based on other finalized nodes.

### Part 3b: Why Each Phase Holds

- **Initialization – why the invariant holds before iteration 1:**
  The source starts at distance 0 (correct, since there's no path yet) and every other node starts at infinity, so the invariant is trivially satisfied.

- **Maintenance – why finalizing the min-dist node is always correct:**
  When we extract node u with the current minimum distance, any alternative path to u through an unrealized node must pass through at least one unrealized edge. Because all edge weights are non negative, other options costs at least as much as dist[u], so dist[u] is already optimal.

- **Termination – what the invariant guarantees when the algorithm ends:**
  Once the heap is empty every node is finalized, so the invariant guarantees that every recorded distance is the true shortest-path cost from the source.

### Part 3c: Why This Matters for the Route Planner

Because Dijkstra returns exact shortest-path distances, every value in `dist_table` is a correct inter-location cost, which ensures the route planner's pruning decisions and final optimal claim are also correct.

---

## Part 4: Search Design

### Why Greedy Fails

- **The failure mode:** Greedy picks the nearest uncollected relic at each node can result in a more expensive and longer path making it not optimal.
- **Counter-example setup:** Using the spec illustration: S->B (cost 1), S->C (cost 2), S->D (cost 2); B->D (cost 1), B->T (cost 1); C->B (cost 1), C->T (cost 1); D->B (cost 1), D->C (cost 1). Relics = {B, C, D}, exit = T.
- **What greedy picks:** Greedy selects B first (cheapest from S at cost 1), then D (cost 1), then C (cost 1), then T (cost 1) = total 4. In configurations where greedy's first choice leads to a worse sequence, total cost exceeds the optimum.
- **What optimal picks:** Exhaustive search over all orderings finds the minimum-cost permutation; in this example it also yields cost 4, but correctness is guaranteed by thoroughness.
- **Why greedy loses:** Greedy commits to the locally cheapest next step without accounting for how that choice affects all subsequent branches. The global optimum can only be found by considering every possible order.

### What the Algorithm Must Explore

- The algorithm must explore every possible **order** in which the relics can be visited, pruning any partial order whose accumulated cost already matches or exceeds the best complete order found so far.

---

## Part 5: State and Search Space

### Part 5a: State Representation

| Component | Variable name in code | Data type | Description |
|---|---|---|---|
| Current location | `current_loc` | node (any hashable) | The node the agent is currently at |
| Relics already collected | `relics_visited_order` | list[node] | Ordered list of relics collected so far |
| Fuel cost so far | `cost_so_far` | float | Total fuel burned to reach `current_loc` via `relics_visited_order` |

### Part 5b: Data Structure for Visited Relics

| Property | Your answer |
|---|---|
| Data structure chosen | set (Python `set`) |
| Operation: check if relic already collected | Time complexity: O(1) average |
| Operation: mark a relic as collected | Time complexity: O(1) average |
| Operation: unmark a relic (backtrack) | Time complexity: O(1) average |
| Why this structure fits | Hash-set membership, insertion, and deletion are all O(1) average, making the per-step overhead minimal during recursive backtracking. |

### Part 5c: Worst-Case Search Space

- **Worst-case number of orders considered:** O(k!)
- **Why:** In the worst case there are k choices for the first relic, k−1 for the second, and so on, yielding k! distinct orderings. And without pruning every ordering must be evaluated.

---

## Part 6: Pruning

### Part 6a: Best-So-Far Tracking

- **What is tracked:** `best[0]` — the minimum total fuel cost of any complete valid route found so far. `best[1]` — the relic ordering that achieved it.
- **When it is used:** At the start of each recursive call (before branching) and at the base case when a complete route is evaluated.
- **What it allows the algorithm to skip:** Any partial route whose `cost_so_far` plus the cheapest possible next step already meets or exceeds `best[0]`. These branches cannot yield a new optimum.

### Part 6b: Lower Bound Estimation

- **What information is available at the current state:** `cost_so_far` (exact fuel burned so far) and `dist_table[current_loc][r]` for every remaining relic r.
- **What the lower bound accounts for:** The minimum possible cost of a single additional branch — `min(dist_table[current_loc][r] for r in relics_remaining)` — representing the cheapest relic we could visit next.
- **Why it never overestimates:** Dijkstra distances are exact shortest-path costs; using the minimum over all remaining relics cannot exceed the actual next-leg cost regardless of which relic is chosen.

### Part 6c: Pruning Correctness

- Pruning is safe because the lower bound `cost_so_far + min_next_cost` is a true lower bound, Every edge weight is non negative, so the current partial path needs to cost at least this much.
- Therefore, if `cost_so_far + min_next_cost >= best[0]`, no descendant state can improve `best[0]`, and the entire sub tree can be discarded without missing the optimal solution.

---

## References

- Lecture notes and course slides for CS 460, Spring 2026.

