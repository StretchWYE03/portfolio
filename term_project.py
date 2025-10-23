import random
import matplotlib.pyplot as plt
import time

def initialize_puzzle(n):
    """
    Initializes a random position for the queens with no initial row conflicts.
    """
    queens = list(range(n))  # Place one queen per row
    random.shuffle(queens)  # Shuffle to randomize initial positions
    return queens


def visualize_solution(queens, N):
    """
    Visualizes the final N-Queens solution using a scatter plot.
    """
    cols = range(N)  # Columns
    rows = queens    # Corresponding rows

    plt.figure(figsize=(10, 10))
    plt.scatter(cols, rows, c='red', s=20 if N <= 50 else 2)  # Adjust size for readability
    plt.title(f"N-Queens Solution for N = {N}", fontsize=14)
    plt.xlabel("Columns")
    plt.ylabel("Rows")
    plt.xlim(-1, N)
    plt.ylim(-1, N)
    plt.gca().invert_yaxis()  # Match chessboard orientation
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.show()


def is_valid(assignment):
    """
    Validates whether the assignment has no conflicts.
    """
    rows = set()
    major_diag = set()
    minor_diag = set()
    for col, row in enumerate(assignment):
        if row in rows or (row - col) in major_diag or (row + col) in minor_diag:
            return False
        rows.add(row)
        major_diag.add(row - col)
        minor_diag.add(row + col)
    return True


def build_conflicts(queens, N):
    """
    Initializes the conflict counters for rows and diagonals.
    """
    rows = [0] * N
    maj_diag = [0] * (2 * N - 1)
    min_diag = [0] * (2 * N - 1)
    conflicts = [0] * N

    for col, row in enumerate(queens):
        rows[row] += 1
        maj_diag[row - col + N - 1] += 1
        min_diag[row + col] += 1

    for col, row in enumerate(queens):
        conflicts[col] = (
            rows[row] - 1 +
            maj_diag[row - col + N - 1] - 1 +
            min_diag[row + col] - 1
        )

    return conflicts, rows, maj_diag, min_diag

def save_solution(queens, N):
    """
    Saves the N-Queens solution to a text file.
    parameters-
    queens: List of queen positions (row for each column).
    N: Size of the chessboard (NxN).
    """
    with open(f"nqueens_solution_{N}.txt", "w") as f:
        for col, row in enumerate(queens):
            f.write(f"Column {col + 1}, Row {row + 1}\n")
    print(f"Solution saved to nqueens_solution_{N}.txt")

def update_conflicts(queens, conflicts, rows, maj_diag, min_diag, col, new_row, N):
    """
    Incrementally updates conflicts when a queen is moved.
    """
    old_row = queens[col]
    if old_row == new_row:
        return  # No need to update if the position is unchanged

    # Remove the old position's conflicts
    rows[old_row] -= 1
    maj_diag[old_row - col + N - 1] -= 1
    min_diag[old_row + col] -= 1

    # Add the new position's conflicts
    rows[new_row] += 1
    maj_diag[new_row - col + N - 1] += 1
    min_diag[new_row + col] += 1

    # Update the specific column's conflict count
    conflicts[col] = (
        rows[new_row] - 1 +
        maj_diag[new_row - col + N - 1] - 1 +
        min_diag[new_row + col] - 1
    )

    # Update conflicts for other columns affected by the move
    for col2, row2 in enumerate(queens):
        if col2 == col:
            continue
        if row2 == old_row or abs(row2 - old_row) == abs(col2 - col):
            conflicts[col2] -= 1
        if row2 == new_row or abs(row2 - new_row) == abs(col2 - col):
            conflicts[col2] += 1

    # Update the queen's position
    queens[col] = new_row


def pick_position(arr, condition):
    """
    Returns a random position in the array based on a given condition.
    """
    candidates = [i for i, val in enumerate(arr) if condition(val)]
    return random.choice(candidates)


def min_conflict(N, max_steps):
    """
    Implementation of the min_conflict algorithm to solve the n-queens problem.
    """
    queens = initialize_puzzle(N)
    conflicts, rows, maj_diag, min_diag = build_conflicts(queens, N)

    # Print the number of conflicts at the first step
    print(f"Initial number of conflicts: {sum(conflicts)}")

    for step in range(max_steps):
        if sum(conflicts) == 0:  # Check if solved
            # Print the number of conflicts at the last step
            print(f"Final number of conflicts: {sum(conflicts)}")
            return queens, step

        if step%100==0:
            print(f"Step {step}; Number of Conflicts Remaining: {sum(conflicts)}")
        # Pick a random conflicting column
        col = pick_position(conflicts, lambda x: x > 0)

        # Calculate row conflicts for the selected column
        min_conf = float('inf')
        best_rows = []
        for row in range(N):
            conflict_count = (
                rows[row] +
                maj_diag[row - col + N - 1] +
                min_diag[row + col] -
                3  # Subtract current queen's own conflicts
            )
            if conflict_count < min_conf:
                min_conf = conflict_count
                best_rows = [row]
            elif conflict_count == min_conf:
                best_rows.append(row)

        # Choose one of the best rows randomly
        new_row = random.choice(best_rows)

        # Update conflicts and move the queen
        update_conflicts(queens, conflicts, rows, maj_diag, min_diag, col, new_row, N)

    return queens, max_steps  # Return final state if max_steps reached


def main(N):
    """
    Main function to solve the N-Queens problem and visualize the final solution.
    """
    try:
        N = int(N)
        if N <= 0:
            print("Error: N must be a positive integer greater than 0.")
            return
        if N in [2, 3]:
            print(f"Error: N = {N} has no solutions. Please try a different value.")
            return

        max_steps = min(10 * N, 10**6)
        print("\nStarting MIN-CONFLICTS algorithm...")
        start_time = time.perf_counter()
        queens, steps = min_conflict(N, max_steps)
        end_time = time.perf_counter()
        elapsed_time = end_time - start_time

        if not is_valid(queens):
            print("N-Queens not solved.")
            return
        print(f"N-Queens solved for N = {N} in {steps} steps.")
        print(f"Time taken = {elapsed_time:.4f}")
        visualize_solution(queens, N)
        
        # output to text file
        save_solution(queens, N)

    except ValueError:
        print("Error: Please enter a valid integer value for N.")


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python term_project.py <N as int>")
    else:
        main(sys.argv[1])