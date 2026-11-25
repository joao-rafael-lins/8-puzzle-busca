from puzzle.base_search import BaseSearch
from puzzle.state import State
from puzzle.result import SearchResult

DEFAULT_DEPTH_LIMIT = 50


class DFS(BaseSearch):

    def __init__(self, depth_limit: int = DEFAULT_DEPTH_LIMIT):
        self.depth_limit = depth_limit

    def search(self, initial: State) -> SearchResult:
        if initial.is_goal:
            return SearchResult(
                solution=initial,
                nodes_expanded=0,
                nodes_generated=1,
                max_frontier_size=1,
                depth=0,
            )

        stack: list[State] = [initial]
        best_depth_seen: dict[tuple[int, ...], int] = {initial.tiles: 0}

        nodes_expanded = 0
        nodes_generated = 1
        max_frontier_size = 1

        while stack:
            if len(stack) > max_frontier_size:
                max_frontier_size = len(stack)

            current = stack.pop()

            if current.is_goal:
                return SearchResult(
                    solution=current,
                    nodes_expanded=nodes_expanded,
                    nodes_generated=nodes_generated,
                    max_frontier_size=max_frontier_size,
                    depth=current.cost,
                )

            if current.cost >= self.depth_limit:
                continue

            nodes_expanded += 1

            # Reverte para manter a ordem natural ao dar pop() da pilha
            for child in reversed(current.neighbors()):
                prev_depth = best_depth_seen.get(child.tiles)
                if prev_depth is None or child.cost < prev_depth:
                    best_depth_seen[child.tiles] = child.cost
                    nodes_generated += 1
                    stack.append(child)

        return SearchResult(
            solution=None,
            nodes_expanded=nodes_expanded,
            nodes_generated=nodes_generated,
            max_frontier_size=max_frontier_size,
            depth=0,
        )