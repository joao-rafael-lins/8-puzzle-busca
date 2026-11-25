import heapq
from puzzle.base_search import BaseSearch
from puzzle.state import State, GOAL_STATE
from puzzle.result import SearchResult


class AStar(BaseSearch):

    def heuristic(self, state: State) -> int:
        distance = 0
        for idx, tile in enumerate(state.tiles):
            if tile != 0:
                goal_idx = GOAL_STATE.index(tile)
                r1, c1 = divmod(idx, 3)
                r2, c2 = divmod(goal_idx, 3)
                distance += abs(r1 - r2) + abs(c1 - c2)
        return distance

    def search(self, initial: State) -> SearchResult:
        if initial.is_goal:
            return SearchResult(
                solution=initial,
                nodes_expanded=0,
                nodes_generated=1,
                max_frontier_size=1,
                depth=0,
            )

        tie_breaker = 0
        open_heap: list[tuple[int, int, State]] = [
            (self.heuristic(initial), tie_breaker, initial)
        ]
        best_g: dict[tuple[int, ...], int] = {initial.tiles: 0}
        closed_set: set[tuple[int, ...]] = set()

        nodes_expanded = 0
        nodes_generated = 1
        max_frontier_size = 1

        while open_heap:
            if len(open_heap) > max_frontier_size:
                max_frontier_size = len(open_heap)

            _, _, current = heapq.heappop(open_heap)

            if current.tiles in closed_set:
                continue

            if current.is_goal:
                return SearchResult(
                    solution=current,
                    nodes_expanded=nodes_expanded,
                    nodes_generated=nodes_generated,
                    max_frontier_size=max_frontier_size,
                    depth=current.cost,
                )

            closed_set.add(current.tiles)
            nodes_expanded += 1

            for child in current.neighbors():
                if child.tiles in closed_set:
                    continue

                tentative_g = child.cost
                if tentative_g < best_g.get(child.tiles, float("inf")):
                    best_g[child.tiles] = tentative_g
                    tie_breaker += 1
                    f_score = tentative_g + self.heuristic(child)
                    heapq.heappush(open_heap, (f_score, tie_breaker, child))
                    nodes_generated += 1

        return SearchResult(
            solution=None,
            nodes_expanded=nodes_expanded,
            nodes_generated=nodes_generated,
            max_frontier_size=max_frontier_size,
            depth=0,
        )