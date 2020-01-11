# Word Search

## Description
Given a 2D board and a word, find if the word exists in the grid. The word can be constructed from letters of sequentially adjacent cell, where “adjacent” cells are those horizontally or vertically neighbouring.  
*Note: The same letter cell may not be used more than once.*


### Example
An example 2D board is shown as below:  

A B C E  
S F C S  
A D E E

Given a word “ABCCED” => `TRUE`;  
Given a word “SEE” => `TRUE`;  
Given a word “ABCB” => `FALSE`; 

## Running the program
Type the following command to run the program.

```bash
python word_search.py
```
You can edit the `word` and `board` variables in the `main()` method to test out different combinations.  

Optionally, you can include the `-t` flag to run the included tests, like so:

```bash
python word_search.py -t
```

## Algorithm Strategy

- We must first iterate over the board until we find a letter that matches the first letter of our word. 
- Once a match is found, we pop the first letter from the word, creating a new word of length - 1 of the original word. 
- We pass the new word, along with the board, a fresh matrix that matches the size of the board to keep track of visited letters, and the starting row and column indexes where the first letter match was found, to the function `recursive_search`.
- `recursive search` performs a few base case checks before proceeding:
     - If the current row or column indexes are invalid, return `False`.
     - If the letter at the current row and column has already been visited, return `False` as a letter cell may not be used more than once.
     - If the length of the word is 0, return `True`, as this means we have successfully found all letters in the word
- If all these checks fail, we pop the first letter from the word, and check to see if the letter cell at the current row and column match. If not, return `False`.
- If they match, mark the letter cell at the current row and column as visited, and create a new word of length - 1 of the current word with the first letter missing.
- Call `recursive_search` on the cells above, below, to the left, and to the right of the curren row and column.
- If all of the `recursive_search` calls return `False`, mark the current cell as not visited, as this is now considered a dead-end path and we are no longer using it.
- Return `True` if any of the `recursive_search` calls succeeded. Else, return `False`.