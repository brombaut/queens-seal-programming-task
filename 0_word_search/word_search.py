import sys

def main(test_mode):
    if test_mode:
        run_tests()
    else:
        word = 'ABCCED'
        board = [
            ['A', 'B', 'C', 'E'],
            ['S', 'F', 'C', 'S'],
            ['A', 'D', 'E', 'E'],
        ]
        result = word_search(word, board)


def word_search(word, board):
    print("Word: {}".format(word))
    print("Board:")
    print_board(board)
    if word is None or len(word) == 0:
        print("Empty Word Exists\n")
        return True
    if not board:
        print("Empty Board does not contain {}\n".format(word))
        return False
    first_letter = word[0]
    for row_index, row in enumerate(board):
        for col_index, letter in enumerate(row):
            if letter == first_letter:
                if recursive_search(word, board, build_fresh_visited_board(board), row_index, col_index):
                    print("Exists\n")
                    return True
    print("Does Not Exist\n")
    return False


def recursive_search(word, board, visited, curr_row, curr_col):
    if len(word) == 0:
        return True
    if indexes_are_invalid(board, curr_row, curr_col):
        return False
    if visited[curr_row][curr_col]:
        return False
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
    if not board:
        print('[]')
        return
    for row in board:
        row_string = ""
        for letter in row:
            row_string += str(letter) + ", "
        print(row_string)


def run_tests():
    test_exists()
    test_does_not_exist()
    test_visiting_letters()
    test_single_row_col()
    test_mismatched_columns()
    test_no_word()
    test_empty_board()
    print('All tests pass')


def test_exists():
    print('Testing Found Words...')
    word1 = 'ABCCED'
    word2 = 'SEE'
    board = [
        ['A', 'B', 'C', 'E'],
        ['S', 'F', 'C', 'S'],
        ['A', 'D', 'E', 'E'],
    ]
    assert word_search(word1, board), 'test_exists failed: {}'.format(word1)
    assert word_search(word2, board), 'test_exists failed: {}'.format(word2)


def test_does_not_exist():
    print('Testing Not Found Words...')
    word1 = 'ABCB'
    word2 = 'EEA'
    board = [
        ['A', 'B', 'C', 'E'],
        ['S', 'F', 'C', 'S'],
        ['A', 'D', 'E', 'E'],
    ]
    assert not word_search(word1, board), 'test_does_not_exist failed: {}'.format(word1)
    assert not word_search(word2, board), 'test_does_not_exist failed: {}'.format(word2)


def test_visiting_letters():
    print('Testing Visiting Letters...')
    word1 = 'SEEES'
    word2 = 'SEEEEES'
    board1 = [
        ['S', 'E', 'E', 'S'],
        ['E', 'E', 'E', 'E'],
        ['E', 'E', 'E', 'S'],
    ]
    assert word_search(word1, board1), 'test_visiting_letters failed: {}'.format(word1)
    assert word_search(word2, board1), 'test_visiting_letters failed: {}'.format(word2)

    word3 = 'ABCESEEDASA'
    board2 = [
        ['A', 'B', 'C', 'E'],
        ['S', 'F', 'C', 'S'],
        ['A', 'D', 'E', 'E'],
    ]
    assert not word_search(word3, board2), 'test_visiting_letters failed: {}'.format(word3)

def test_single_row_col():
    print('Testing Single Row/Col Combinations')
    word1 = 'A'
    board1 = [
        ['A'],
    ]

    word2 = 'AAASA'
    board2 = [
        ['A'],
        ['S'],
        ['A'],
        ['A'],
        ['A'],
    ]

    word3 = 'AAASA'
    board3 = [
        ['A', 'S', 'A', 'A', 'A'],
    ]
    
    assert word_search(word1, board1), 'test_single_row_col failed: {}'.format(word1)
    assert word_search(word2, board2), 'test_single_row_col failed: {}'.format(word2)
    assert word_search(word3, board3), 'test_single_row_col failed: {}'.format(word3)


def test_mismatched_columns():
    print('Testing Mismatched Columns...')
    word1 = 'EECCE'
    board1 = [
        ['A', 'B', 'C', 'E'],
        ['S', 'F', 'C'],
        ['A', 'D', 'E', 'E'],
    ]

    word2 = 'EDASABCE'
    board2 = [
        ['A', 'B', 'C', 'E'],
        ['S'],
        ['A', 'D', 'E', 'E'],
    ]

    assert word_search(word1, board1), 'test_mismatched_columns failed: {}'.format(word1)
    assert word_search(word2, board2), 'test_mismatched_columns failed: {}'.format(word2)


def test_no_word():
    print('Testing No Word...')
    word1 = ''
    word2 = None
    board = [
        ['A', 'B', 'C', 'E'],
        ['S', 'F', 'C', 'S'],
        ['A', 'D', 'E', 'E'],
    ]
    assert word_search(word1, board), 'test_no_word failed: {}'.format(word1)
    assert word_search(word2, board), 'test_no_word failed: {}'.format(word2)


def test_empty_board():
    print('Testing No Board...')
    word1 = 'a'
    board1 = None
    board2 = []
    board3 = [
        [],
    ]
    assert not word_search(word1, board1), 'test_empty_board failed: {}'.format(word1)
    assert not word_search(word1, board2), 'test_empty_board failed: {}'.format(word1)
    assert not word_search(word1, board3), 'test_empty_board failed: {}'.format(word1)


if __name__ == '__main__':
    test_mode = False
    if len(sys.argv) > 1 and sys.argv[1] == '-t':
        test_mode = True
    main(test_mode)
