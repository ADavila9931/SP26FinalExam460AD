# Development Log – The Torchbearer

**Student Name:** Angel Davila
**Student ID:** 130670316

---

## Entry 1 – 5/6: Initial Plan

My plan is to tackle this in three phases: precomputation first, then the search, then pruning. I expect the trickiest part to be the backtracking in `_explore`. I'll start by getting `run_dijkstra` working and verifying it on the small spec graph by hand before touching the search logic. For testing I'll use the four provided cases as a goal line.

---

## Entry 2 – 5/7: Wrong source set, missed relic-to-relic distances

I initially only ran Dijkstra from the spawn node, assuming that would be enough to find costs to every relic. This broke Test 1 immediately because once you're at relic B you need the distance from B to C or D, and those values weren't in the table. I realized `dist_table` needs a row for every node you might *depart from*, which means spawn plus every relic. Adding each relic to `select_sources` fixed it. The exit node doesn't need its own row because we never travel outward from there.

---

## Entry 3 – 5/8: Worked through pruning logic on paper

Before coding the pruning I drew the search tree for the spec graph on paper and traced which branches should get cut. This way I found it easier to map the coding algorithms and get a clearer understanding of what I'm trying to achieve. Usually on smaller algorithms I'll just program and fix as needed, but I figured this could be complicated enough that I should think it out a little bit more.

---

## Entry 4 – 5/14: Post-Implementation Reflection

The implementation works correctly on all provided tests. I honestly was focused on doing making sure it passed the tests and filling out the README that I forgot about this and am doing it last, sorry! But everything worked and I think it is pretty good as is as most problems that I found were fixed as spotted.

---

## Final Entry – May 7: Time Estimate

| Part | Estimated Hours |
|---|---|
| Part 1: Problem Analysis | 0.5 |
| Part 2: Precomputation Design | 1.0 |
| Part 3: Algorithm Correctness | 0.75 |
| Part 4: Search Design | 0.5 |
| Part 5: State and Search Space | 0.5 |
| Part 6: Pruning | 1.0 |
| Part 7: Implementation | 2.5 |
| README and DEVLOG writing | 1.25 |
| **Total** | **8.0** (Was definitely more...) |
