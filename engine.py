
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

        result["dirs"] += [os.path.join(root, item) for item in dirs if os.path.basename(item).lower().startswith(query)]
        result["files"] += [os.path.join(root, item) for item in files if os.path.basename(item).lower().startswith(query)]

    return result

def word_occurences(file_path: str, query: str) -> tuple[int, list[str], list[int]]:

    # returns a tuple (number_of_occurences, [words that matched], [line numbers])

    lines = [] # lines of given file
    occ = 0 # number of occurences of the word
    match_results = [] # words that matched
    line_results = [] # line numbers on which the word occurs

    try:
        with open(file_path, 'r', encoding="utf8") as file: lines = file.readlines()
        # extract lines from file

    except(UnicodeDecodeError, FileNotFoundError):
        # case of weird decoding, returns no results on no lines
        return (0, [])

    for i in range(len(lines)):

        words = lines[i].split(" ") # list of words in the line

        for word in words:

            if not word.lower().startswith(query): continue
            # skip word if it doesn't match

            occ += 1
            match_results.append(word)
            line_results.append(i+1)

    return (occ, match_results, line_results)

def content_results(_dir: str, query: str, extensions: list[str]) -> dict[str, tuple[int, list[int]]]:

    result = {} # dictionary with file names as keys, and tuples as values
    # tuple[0] is the number of occurences of the query
    # tuple[1] is the list of matches (strings)
    # tuple[2] is a list of the lines of these occurences

    # for example, file_content_results(CURRENT_DIR, "example") returns {".../engine.py": (1, [55])}
    
    if len(extensions)==0: return result # empty result if no extensions are chosen

    for root, dirs, files in os.walk(_dir): # walks through folders and subfolders

        if os.path.basename(root).startswith('.'): continue
        # skip hidden folders

        for file in files:

            skip = True
            for ext in extensions:
                if file.endswith(ext):
                    skip = False
                    break

            if skip: continue
            # skip the file if it does not end with any of the given extensions

            file_path = os.path.join(root, file)

            tuple_result = word_occurences(file_path, query)
            if(tuple_result[0] < 1): continue # skip files with 0 matches

            result[file_path] = tuple_result

    return result


if __name__=="__main__":

    print(content_results(CURRENT_DIR, "example", [".py"]))