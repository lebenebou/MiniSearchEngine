
import os

CURRENT_DIR = os.path.dirname(__file__)
os.chdir(CURRENT_DIR)

def item_results(_dir: str, query: str) -> dict[str, list[str]]:

    query = query.lower() # use lower case query to broaden matching

    result = {
        "files":[],
        "dirs":[]
    }

    for root, dirs, files in os.walk(_dir): # walks through folders and subfolders

        if(os.path.basename(root).startswith('.')): continue
        # ignore hidden folders

        result["dirs"] += [item for item in dirs if os.path.basename(item).lower().startswith(query)]
        result["files"] += [item for item in files if os.path.basename(item).lower().startswith(query)]

    return result
    # returns dictionary of files and folders which names start with the query


if __name__=="__main__":

    print(item_results(CURRENT_DIR, "head")["files"])