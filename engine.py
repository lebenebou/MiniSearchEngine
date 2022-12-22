
import os

CURRENT_DIR = os.path.dirname(__file__)
os.chdir(CURRENT_DIR)

def item_results(_dir: str, query: str) -> dict[str, list[str]]:
    
    # returns dictionary of files and folders which names start with the query
    # result["files"] contains the list of matching files
    # result["dirs"] contains the list of matching dirs

    query = query.lower() # use lower case query to broaden matching

    result = {
        "files":[],
        "dirs":[]
    }

    for root, dirs, files in os.walk(_dir): # walks through folders and subfolders

        if(os.path.basename(root).startswith('.')): continue
        # skip hidden folders

        result["dirs"] += [item for item in dirs if os.path.basename(item).lower().startswith(query)]
        result["files"] += [item for item in files if os.path.basename(item).lower().startswith(query)]

    return result

def word_occurences(file_path: str, word: str) -> tuple[int, list[int]]:

    # returns a tuple (number_of_occurences, [line_number, line_number, ...])

    lines = [] # lines of given file
    occ = 0 # number of occurences of the word
    line_results = [] # line numbers on which the word occurs

    try:
        with open(file_path, 'r', encoding="utf8") as file: lines = file.readlines()
        # extract lines from file

    except(UnicodeDecodeError, FileNotFoundError):
        # case of weird decoding, returns no results on no lines
        return (0, [])

    for i in range(len(lines)):

        if word in lines[i]:
            occ += 1
            line_results.append(i+1) # line indexing starts at 0
            continue

    return (occ, line_results)

def file_content_results(_dir: str, query: str) -> dict[str, tuple[int, list[int]]]:

    result = {} # dictionary with file names as keys, and tuples as values
    # tuple[0] is the number of occurences of the query
    # tuple[1] is a list of the lines of this occurences

    # for example, file_content_results(CURRENT_DIR, "example") returns {"engine.py": (1, [55])}

    for root, dirs, files in os.walk(_dir): # walks through folders and subfolders

        if os.path.basename(root).startswith('.'): continue
        # skip hidden folders

        for file in files:

            tuple_result = word_occurences(file, query)
            if(tuple_result[0] < 1): continue # skip files with no occurences

            result[file] = tuple_result

    return result


if __name__=="__main__":

    print(file_content_results(CURRENT_DIR, "example"))