from dataclasses import dataclass
from typing import Optional


@dataclass
class Node:
    col_id: int = -1
    nodes_count: int = 0
    # value: int = 0
    left: Optional["Node"] = None
    right: Optional["Node"] = None
    top: Optional["Node"] = None
    bottom: Optional["Node"] = None
    head: Optional["Node"] = None
    row_id: int = -1


N_COLS, N_ROWS = 7, 8
MATRIX = [[Node()] * N_COLS] * N_ROWS

def get_neighbor_index_at_direction(direction: str, index: int) -> int:
    match direction:
        case "left":
            return index - 1 if index > 0 else N_COLS - 1
        case "right":
            return index + 1 if index < N_COLS - 1 else 0
        case "top":
            return index - 1 if index > 0 else N_ROWS - 1
        case "bottom":
            return index + 1 if index < N_ROWS - 1 else 0
        case _:
            return 0


def create_matrix(problem: list[list[bool]]) -> Node:
    for i, row in enumerate(problem):
        for j, value in enumerate(row):
            if value:
                if i:
                    MATRIX[0][j].nodes_count += 1

                MATRIX[i][j] = Node()

                MATRIX[i][j].head = MATRIX[0][j]
                MATRIX[i][j].row_id = i
                MATRIX[i][j].col_id = j

                left = get_neighbor_index_at_direction("left", j)

                while not problem[i][left] and left != j:
                    left = get_neighbor_index_at_direction("left", left)

                right = get_neighbor_index_at_direction("right", j)
                
                while not problem[i][right] and right != j:
                    right = get_neighbor_index_at_direction("right", right)
               
                top = get_neighbor_index_at_direction("top", i)
                
                while not problem[top][j] and top != i:
                    top = get_neighbor_index_at_direction("top", top)

                bottom = get_neighbor_index_at_direction("bottom", i)

                while not problem[bottom][j] and bottom != i:
                    bottom = get_neighbor_index_at_direction("bottom", bottom)
                
                MATRIX[i][j].left = MATRIX[i][left]
                MATRIX[i][j].right = MATRIX[i][right]
                MATRIX[i][j].top = MATRIX[top][j]
                MATRIX[i][j].bottom = MATRIX[bottom][j]

    header = Node(right=MATRIX[0][0], left=MATRIX[0][N_COLS - 1])
    MATRIX[0][0].left = header
    MATRIX[0][N_COLS - 1] = header

    return header


def main() -> None:
    # fmt: off
    problem_matrix = [
        [True, True, True, True, True, True, True],      # Header
        [True, False, False, True, False, False, True],  # 1
        [True, False, False, True, False, False, False], # 2
        [False, False, False, True, True, False, True],  # 3
        [False, False, True, False, True, True, False],  # 4
        [False, True, True, False, False, True, True],   # 5
        [False, True, False, True, False, False, True],  # 6
        [False, False, True, False, True, True, False],  # 7
    ]
    # fmt: on
    header = create_matrix(problem_matrix)


if __name__ == "__main__":
    main()
