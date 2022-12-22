
import os

CURRENT_DIR = os.path.dirname(__file__)
os.chdir(CURRENT_DIR)

def item_results(query:str):

    for item in os.listdir():
        print(item)

if __name__=="__main__":

    print(CURRENT_DIR)