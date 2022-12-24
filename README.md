# MiniSearchEngine
Mini search engine coded with Python that let's you search for folders, files, and file contents. Made with Tkinter.

## engine.py
### This file constitutes the backend of the project.

- ```item_results(_dir, query)``` gets file and folder names in a directory that match the given query.

- ```word_occurences(file_path, query)``` returns the number of occurences of words that matched the query inside the given file contents, a list of which the words that matched the query, and the line numbers on which the matches occured.

- ```content_results(_dir, query, extensions)``` uses **word_occurences()** to return the full list of files inside the given directory that match the query and end with one of the given extensions.

## window.py
### This file constitutes the frontend of the project.

It is a windows application made with [Python's tkinter](https://docs.python.org/3/library/tk.html). The minimalistic design includes:

- A _query_ frame where the user can type their query and choose which type of files they wish to expand the file content search to.

- A _directories_ frame where the user inputs up to 3 directories to be included in the search space.

- A _results_ frame that takes up most of the lower-half of the window and is dedicated to showing the results that matched the inputed query. 3 types of results are displayed:
    - Folder results (matching names only)
    - File results (matching names only)
    - File content results which displays the number of matches, matching words and on which lines these matching words occured in the file. These results are also sorted by descending number of matches.