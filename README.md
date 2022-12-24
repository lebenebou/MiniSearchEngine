# MiniSearchEngine
Mini search engine coded with Python that let's you search for folders, files, and file contents. Made with Tkinter.

## engine.py
### This file constitutes the backend of the project.

- ```item_results(_dir, query)``` gets file and folder names in a directory that match the given query.

- ```word_occurences(file_path, query)``` returns the number of occurences of words that matched the query inside the given file contents, a list of which the words that matched the query, and the line numbers on which the matches occured

- ```content_results(_dir, query, extensions)``` uses _word_occurences()_ to return the full list of files that match the query and end with one of the given extensions.