if __name__ == "__main__":
    from csp import *
    # visualize solution
    partial_assignment = {(9,2):3, (9,3):5, (9,5):8, (9,9):9,
                          (8,7):6, (8,9):3,
                          (7,3):8, (7,4):3, (7,7):7,
                          (6,2):1, (6,4):4, (6,9):2,
                          (5,2):7, (5,4):9, (5,6):3, (5,8):6,
                          (4,1):3, (4,6):2, (4,8):5,
                          (3,3):3, (3,6):5, (3,7):2,
                          (2,1):7, (2,3):9,
                          (1,1):4, (1,5):7, (1,7):8, (1,8):3, (1,9):6}
    sudoku = SudokuCSP(partial_assignment)
    sol_assignment = backtracking(sudoku)
    visualize_sudoku_solution(sol_assignment, './sudoku1.png')
    plt.close()
    
    partial_assignment = {(9,2):2, (9,3):3, 
                          (8,5):2, (8,8):5,
                          (5,3):7, (5,8):4, 
                          (4,4):6, (4,8):1, (4,9):2,
                          (3,1):2, (3,3):1, (3,7):6,
                          (2,2):6, (2,9):4,
                          (1,1):5, (1,4):9, (1,6):8}
    sudoku = SudokuCSP(partial_assignment)
    sol_assignment = backtracking(sudoku)
    visualize_sudoku_solution(sol_assignment, './sudoku2.png')
    plt.close()