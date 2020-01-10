
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
        ['E', 'E', 'E', 'S'],
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
                if recursive_search(word, board, build_fresh_visited_board(board), row_index, col_index):
                    return True
    return False


def recursive_search(word, board, visited, curr_row, curr_col):
    if indexes_are_invalid(board, curr_row, curr_col):
        return False
    if visited[curr_row][curr_col]:
        return False
    print('Cur Row={}, Cur Col={}, word={}'.format(curr_row, curr_col, word))
    print_board(visited)
    if len(word) == 0:
        return True
    else:
        curr_letter = word[0]
        if board[curr_row][curr_col] != curr_letter:
            return False
        visited[curr_row][curr_col] = True
        rest_of_word = word[1:]
        found = recursive_search(rest_of_word, board, visited, curr_row - 1, curr_col)\
            or recursive_search(rest_of_word, board, visited, curr_row + 1, curr_col)\
            or recursive_search(rest_of_word, board, visited, curr_row, curr_col - 1)\
            or recursive_search(rest_of_word, board, visited, curr_row, curr_col + 1)
        if not found:
            visited[curr_row][curr_col] = False
        return found


def build_fresh_visited_board(board):
    num_of_rows = len(board)
    num_of_cols = len(board[0])
    return [[False for x in range(num_of_cols)] for y in range(num_of_rows)]


def indexes_are_invalid(board, x, y):
    return x < 0 or x >= len(board) or y < 0 or y >= len(board[x])


def print_board(board):
    for row in board:
        row_string = ""
        for letter in row:
            row_string += str(letter) + ", "
        print(row_string)
    print()

if __name__ == '__main__':
    main()
