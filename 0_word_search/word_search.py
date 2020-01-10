
def main():
    # word = 'ABCCED'
    word = 'SEEES'
    # board = [
    #     ['A', 'S', 'E', 'H'],
    #     ['N', 'F', 'E', 'D'],
    #     ['A', 'D', 'E', 'E'],
    # ]
    board = [
        ['S', 'E', 'E', 'S'],
        ['E', 'E', 'E', 'E'],
        ['A', 'D', 'E', 'S'],
    ]
    # board = [
    #     ['A', 'B', 'C', 'E'],
    #     ['S', 'F', 'C', 'S'],
    #     ['A', 'D', 'E', 'E'],
    # ]
    if word_search(word, board):
        print('FOUND')
    else:
        print('NOT FOUND')


def word_search(word, board):
    first_letter = word[0]
    for row_index, row in enumerate(board):
        for col_index, letter in enumerate(row):
            if letter == first_letter:
                if recursive_search(word[1:], board, build_fresh_visited_board(board), row_index, col_index):
                    return True
    return False


def recursive_search(word, board, visited, curr_row, curr_col):
    visited[curr_row][curr_col] = True
    print('Cur Row={}, Cur Col={}, word={}'.format(curr_row, curr_col, word))
    print(visited)
    if len(word) == 0:
        return True
    else:
        next_letter = word[0]
        rest_of_word = word[1:]
        found = False
        # Check up
        if curr_row > 0 and not visited[curr_row - 1][curr_col] and board[curr_row - 1][curr_col] == next_letter:
            found = recursive_search(rest_of_word, board, visited, curr_row - 1, curr_col)
        # Check down
        if not found and curr_row < len(board) - 1 and not visited[curr_row + 1][curr_col] and board[curr_row + 1][curr_col] == next_letter:
            found = recursive_search(rest_of_word, board, visited, curr_row + 1, curr_col)
        # Check left
        if not found and curr_col > 0 and not visited[curr_row][curr_col - 1] and board[curr_row][curr_col - 1] == next_letter:
            found = recursive_search(rest_of_word, board, visited, curr_row, curr_col - 1)
        # Check left
        if not found and curr_col < len(board[curr_row]) - 1 and not visited[curr_row][curr_col + 1] and board[curr_row][curr_col + 1] == next_letter:
            found = recursive_search(rest_of_word, board, visited, curr_row, curr_col + 1)
        return found


def build_fresh_visited_board(board):
    num_of_rows = len(board)
    num_of_cols = len(board[0])
    return [[False for x in range(num_of_cols)] for y in range(num_of_rows)]

if __name__ == '__main__':
    main()
