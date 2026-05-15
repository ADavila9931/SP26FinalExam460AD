"""
CS 460 – Algorithms: Final Programming Assignment
The Torchbearer

Student Name: Angel Davila
Student ID:   130670316

INSTRUCTIONS
------------
- Implement every function marked TODO.
- Do not change any function signature.
- Do not remove or rename required functions.
- You may add helper functions.
- Variable names in your code must match what you define in README Part 5a.
- The pruning safety comment inside _explore() is graded. Do not skip it.

Submit this file as: torchbearer.py
"""

import heapq


# =============================================================================
# PART 1
# =============================================================================

def explain_problem():
    """
    Returns
    -------
    str
        Your Part 1 README answers, written as a string.
        Must match what you wrote in README Part 1.
    """
    return (
        "Why a single shortest-path run from S is not enough: "
        "Running Dijkstra once from S gives the cheapest way to reach each node individually, "
        "but it does not tell us the cheapest way to visit ALL relics in some order before "
        "reaching the exit—inter-relic travel costs depend on which relic we visit next.\n\n"

        "What decision remains after all inter-location costs are known: "
        "Even with all pairwise distances in hand, we must still decide the ORDER in which "
        "to visit the relics, since different orderings yield different total fuel costs.\n\n"

        "Why this requires a search over orders: "
        "There is no greedy rule that always picks the locally cheapest next relic and "
        "guarantees the globally cheapest full route, so we must explore the space of "
        "relic orderings (up to k! permutations) and prune branches that cannot improve "
        "on the best solution found so far."
    )


# =============================================================================
# PART 2
# =============================================================================

def select_sources(spawn, relics, exit_node):
    """
    Parameters
    ----------
    spawn : node
    relics : list[node]
    exit_node : node

    Returns
    -------
    list[node]
        No duplicates. Order does not matter.
    """
    # Sources are: spawn + every relic node.
    # We run Dijkstra from each so that dist_table[u][v] is available
    # for every (u -> next_relic) and (relic -> exit) leg.
    # exit_node is NOT a source because we never travel *from* the exit.
    sources = set()
    sources.add(spawn)
    for r in relics:
        sources.add(r)
    return list(sources)


def run_dijkstra(graph, source):
    """
    Parameters
    ----------
    graph : dict[node, list[tuple[node, int]]]
        graph[u] = [(v, cost), ...]. All costs are nonnegative integers.
    source : node

    Returns
    -------
    dict[node, float]
        Minimum cost from source to every node in graph.
        Unreachable nodes map to float('inf').
    """
    dist = {node: float('inf') for node in graph}
    dist[source] = 0
    # min-heap: (cost, node)
    heap = [(0, source)]

    while heap:
        d, u = heapq.heappop(heap)
        if d > dist[u]:
            continue  # stale entry
        for v, w in graph.get(u, []):
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                heapq.heappush(heap, (nd, v))

    return dist


def precompute_distances(graph, spawn, relics, exit_node):
    """
    Parameters
    ----------
    graph : dict[node, list[tuple[node, int]]]
    spawn : node
    relics : list[node]
    exit_node : node

    Returns
    -------
    dict[node, dict[node, float]]
        Nested structure supporting dist_table[u][v] lookups
        for every source u your design requires.
    """
    sources = select_sources(spawn, relics, exit_node)
    dist_table = {}
    for s in sources:
        dist_table[s] = run_dijkstra(graph, s)
    return dist_table


# =============================================================================
# PART 3
# =============================================================================

def dijkstra_invariant_check():
    """
    Returns
    -------
    str
        Your Part 3 README answers, written as a string.
        Must match what you wrote in README Part 3.
    """
    return (
        "Invariant – finalized nodes (in S): "
        "The current distance in the node represents the best global path and there is not anything else to improve\n\n"

        "Invariant – non-finalized nodes (not in S): "
        "The current distance isn't yet confirmed to be the best option and could still be improved based on other finalized nodes.\n\n"

        "Initialization: "
        "why the invariant holds before iteration 1: The source starts at distance 0 (correct, since there's no path yet) and every other node starts at infinity, so the invariant is trivially satisfied.\n\n"

        "Maintenance: "
        "why finalizing the min-dist node is always correct: When we extract node u with the current minimum distance, any alternative path to u through an unrealized node must pass through at least one unrealized edge. Because all edge weights are non negative, other options costs at least as much as dist[u], so dist[u] is already optimal.\n\n"

        "Termination: "
        "what the invariant guarantees when the algorithm ends: Once the heap is empty every node is finalized, so the invariant guarantees that every recorded distance is the true shortest-path cost from the source.\n\n"

        "Why this matters for the route planner: "
        "Because Dijkstra returns exact shortest-path distances, every value in dist_table is a correct inter-location cost, which ensures the route planner's pruning decisions and final optimal claim are also correct."
    )


# =============================================================================
# PART 4
# =============================================================================

def explain_search():
    """
    Returns
    -------
    str
        Your Part 4 README answers, written as a string.
        Must match what you wrote in README Part 4.
    """
    return (
        "Greedy picks the nearest uncollected relic at each node can result in a more expensive and longer path making it not optimal.\n\n"

        "Counter-example setup (from spec illustration): "
        "Using the spec illustration: S->B (cost 1), S->C (cost 2), S->D (cost 2); B->D (cost 1), B->T (cost 1); C->B (cost 1), C->T (cost 1); D->B (cost 1), D->C (cost 1). Relics = {B, C, D}, exit = T.\n\n"

        "What greedy picks: "
        "Greedy selects B first (cheapest from S at cost 1), then D (cost 1), then C (cost 1), then T (cost 1) = total 4. In configurations where greedy's first choice leads to a worse sequence, total cost exceeds the optimum.\n\n"

        "What optimal picks: "
        "Exhaustive search over all orderings finds the minimum-cost permutation; in this example it also yields cost 4, but correctness is guaranteed by thoroughness.\n\n"

        "Why greedy loses: "
        "Greedy commits to the locally cheapest next step without accounting for how that choice affects all subsequent branches. The global optimum can only be found by considering every possible order.\n\n"

        "What the algorithm must explore: "
        "The algorithm must explore every possible order in which the relics can be visited, pruning any partial order whose accumulated cost already matches or exceeds the best complete order found so far."
    )


# =============================================================================
# PARTS 5 + 6
# =============================================================================

def find_optimal_route(dist_table, spawn, relics, exit_node):
    """
    Parameters
    ----------
    dist_table : dict[node, dict[node, float]]
        Output of precompute_distances.
    spawn : node
    relics : list[node]
        Every node in this list must be visited at least once.
    exit_node : node
        The route must end here.

    Returns
    -------
    tuple[float, list[node]]
        (minimum_fuel_cost, ordered_relic_list)
        Returns (float('inf'), []) if no valid route exists.
    """
    # best[0] = best cost so far, best[1] = best ordering so far
    best = [float('inf'), []]

    # relics_remaining is a set (see README Part 5b)
    relics_remaining = set(relics)

    _explore(
        dist_table=dist_table,
        current_loc=spawn,
        relics_remaining=relics_remaining,
        relics_visited_order=[],
        cost_so_far=0.0,
        exit_node=exit_node,
        best=best
    )

    return (best[0], best[1])


def _explore(dist_table, current_loc, relics_remaining, relics_visited_order,
             cost_so_far, exit_node, best):
    """
    Recursive helper for find_optimal_route.

    Parameters
    ----------
    dist_table : dict[node, dict[node, float]]
    current_loc : node
    relics_remaining : set
        Relics not yet collected (mutable; we add/remove for backtracking).
    relics_visited_order : list[node]
        Relics collected so far, in visit order.
    cost_so_far : float
        Fuel spent to reach current_loc after collecting relics_visited_order.
    exit_node : node
    best : list
        best[0] = best total cost found, best[1] = best ordering found.

    Returns
    -------
    None  –  updates best in place.
    """

    # ------------------------------------------------------------------
    # BASE CASE: all relics collected – try to reach the exit
    # ------------------------------------------------------------------
    if not relics_remaining:
        cost_to_exit = dist_table[current_loc].get(exit_node, float('inf'))
        total = cost_so_far + cost_to_exit
        if total < best[0]:
            best[0] = total
            best[1] = list(relics_visited_order)
        return

    # ------------------------------------------------------------------
    # PRUNING – lower-bound check
    #
    # cost_so_far is already the exact fuel burned to reach current_loc.
    # The cheapest any remaining relic can be reached from current_loc is
    # min_next_cost (the cheapest single step to any remaining relic).
    # Therefore cost_so_far + min_next_cost is a valid lower bound on the
    # total fuel for any completion of this partial route.
    #
    # This prune is SAFE (cannot discard the optimal solution) because
    # every edge weight is nonnegative: the true cost of any completion
    # is at least cost_so_far + min_next_cost, so if that already meets
    # or exceeds the best known solution, no completion down this branch
    # can possibly improve best[0].
    # ------------------------------------------------------------------
    min_next_cost = min(
        dist_table[current_loc].get(r, float('inf'))
        for r in relics_remaining
    )
    if cost_so_far + min_next_cost >= best[0]:
        return

    # ------------------------------------------------------------------
    # RECURSIVE CASE: try visiting each remaining relic next
    # ------------------------------------------------------------------
    for relic in list(relics_remaining):
        leg_cost = dist_table[current_loc].get(relic, float('inf'))
        if leg_cost == float('inf'):
            continue  # relic unreachable from here; skip

        new_cost = cost_so_far + leg_cost

        # Prune early before recursing if partial cost already too high
        if new_cost >= best[0]:
            continue

        # Choose this relic next
        relics_remaining.remove(relic)
        relics_visited_order.append(relic)

        _explore(
            dist_table=dist_table,
            current_loc=relic,
            relics_remaining=relics_remaining,
            relics_visited_order=relics_visited_order,
            cost_so_far=new_cost,
            exit_node=exit_node,
            best=best
        )

        # Backtrack
        relics_visited_order.pop()
        relics_remaining.add(relic)


# =============================================================================
# PIPELINE
# =============================================================================

def solve(graph, spawn, relics, exit_node):
    """
    Parameters
    ----------
    graph : dict[node, list[tuple[node, int]]]
    spawn : node
    relics : list[node]
    exit_node : node

    Returns
    -------
    tuple[float, list[node]]
        (minimum_fuel_cost, ordered_relic_list)
        Returns (float('inf'), []) if no valid route exists.
    """
    dist_table = precompute_distances(graph, spawn, relics, exit_node)
    return find_optimal_route(dist_table, spawn, relics, exit_node)


# =============================================================================
# PROVIDED TESTS (do not modify)
# Graders will run additional tests beyond these.
# =============================================================================

def _run_tests():
    print("Running provided tests...")

    # Test 1: Spec illustration. Optimal cost = 4.
    graph_1 = {
        'S': [('B', 1), ('C', 2), ('D', 2)],
        'B': [('D', 1), ('T', 1)],
        'C': [('B', 1), ('T', 1)],
        'D': [('B', 1), ('C', 1)],
        'T': []
    }
    cost, order = solve(graph_1, 'S', ['B', 'C', 'D'], 'T')
    assert cost == 4, f"Test 1 FAILED: expected 4, got {cost}"
    print(f"  Test 1 passed  cost={cost}  order={order}")

    # Test 2: Single relic. Optimal cost = 5.
    graph_2 = {
        'S': [('R', 3)],
        'R': [('T', 2)],
        'T': []
    }
    cost, order = solve(graph_2, 'S', ['R'], 'T')
    assert cost == 5, f"Test 2 FAILED: expected 5, got {cost}"
    print(f"  Test 2 passed  cost={cost}  order={order}")

    # Test 3: No valid path to exit. Must return (inf, []).
    graph_3 = {
        'S': [('R', 1)],
        'R': [],
        'T': []
    }
    cost, order = solve(graph_3, 'S', ['R'], 'T')
    assert cost == float('inf'), f"Test 3 FAILED: expected inf, got {cost}"
    print(f"  Test 3 passed  cost={cost}")

    # Test 4: Relics reachable only through intermediate rooms.
    # Optimal cost = 6.
    graph_4 = {
        'S': [('X', 1)],
        'X': [('R1', 2), ('R2', 5)],
        'R1': [('Y', 1)],
        'Y': [('R2', 1)],
        'R2': [('T', 1)],
        'T': []
    }
    cost, order = solve(graph_4, 'S', ['R1', 'R2'], 'T')
    assert cost == 6, f"Test 4 FAILED: expected 6, got {cost}"
    print(f"  Test 4 passed  cost={cost}  order={order}")

    # Test 5: Explanation functions must return non-placeholder strings.
    for fn in [explain_problem, dijkstra_invariant_check, explain_search]:
        result = fn()
        assert isinstance(result, str) and result != "TODO" and len(result) > 20, \
            f"Test 5 FAILED: {fn.__name__} returned placeholder or empty string"
    print("  Test 5 passed  explanation functions are non-empty")

    print("\nAll provided tests passed.")


if __name__ == "__main__":
    _run_tests()
