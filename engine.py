
import os

CURRENT_DIR = os.path.dirname(__file__)
os.chdir(CURRENT_DIR)

def item_results(_dir: str, query: str):

    return [item for item in os.listdir(_dir)

        if item.lower().startswith(query.lower())
        and
        (os.path.isfile(item) or os.path.isdir(item))
    ]
    # returns items that start with the query string and are either a file or folder

def file_results(items: list[str]):

    return [item for item in items

        if os.path.isfile(item)
    ]
    # returns files results only

def directory_results(items: list[str]):

    return [item for item in items

        if os.path.isdir(item)
    ]
    # returns directory results only



if __name__=="__main__":

    print(directory_results(item_results(CURRENT_DIR, ".")))