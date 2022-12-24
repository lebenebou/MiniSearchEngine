
from tkinter import *
from tkinter import ttk
from tkinter import messagebox

import engine # from "./engine.py"
import os
import subprocess

# main window initiation ====================
mw = Tk()
mw.title("Seach Engine")
mw_width, mw_height = 750, 580
mw.minsize(mw_width, mw_height)
mw.geometry("+400+200")
mw.resizable(False, False)
mw.iconbitmap("./icon.ico")

# variables =================================
include_current_dir = BooleanVar()
include_current_dir.set(True)

include_txt_files = BooleanVar()
include_txt_files.set(False)

include_py_files = BooleanVar()
include_py_files.set(False)

include_cpp_files = BooleanVar()
include_cpp_files.set(False)

include_java_files = BooleanVar()
include_java_files.set(False)

valid_dirs = []
# functions =================================
def reset_window():

    folder_results_listbox.delete(0,END) # clear all list boxes
    file_results_listbox.delete(0,END)
    content_results_listbox.delete(0,END)
    words_listbox.delete(0,END)
    lines_listbox.delete(0,END)
    matches_listbox.delete(0,END)

    search_btn["state"]="enabled" # re-enable search button

    keyword_entry.focus_set()
    keyword_entry.select_range(0, "end")
    valid_dirs = []

def start_search():

    query: str = keyword_entry.get().strip().lower()
    if(query == ""):
        messagebox.showerror("Unable To Seach", "Please input a keyword")
        return
    if(not query.isalnum()):
        messagebox.showerror("Unable To Seach", "Please input an alphanumeric keyword.\nIt must be a single word.")
        return

    dir_candidates = list(set([dir_entry1.get(), dir_entry2.get(), dir_entry3.get()]))
    # get list of directories from entries and remove duplicates
    dir_candidates = [d.strip().lower() for d in dir_candidates if d!=""]
    # strip, lower, and remove empty inputs
    if include_current_dir.get(): dir_candidates.append(engine.CURRENT_DIR.strip().lower())

    if len(dir_candidates) == 0:
        messagebox.showerror("Unable To Search", "No directories were chosen for your search")
        return

    global valid_dirs
    valid_dirs = [d for d in dir_candidates if os.path.isdir(d)]
    if len(valid_dirs)==0: 
        messagebox.showerror("Unable to search", "None of the directories you chose are valid")
        return

    if len(valid_dirs)<len(dir_candidates):
        messagebox.showinfo("Invalid Directories", f"{len(dir_candidates)-len(valid_dirs)} out of {len(dir_candidates)} inputed directories are invalid, the search will not include results from those directories.")
    
    del dir_candidates # dereference candidates as they are no longer useful

    # Search Starts

    name_results = {
        "files":[],
        "dirs":[]
    }

    for _dir in valid_dirs:

        item_results = engine.item_results(_dir, query)
        name_results["files"] += item_results["files"] # concatenate file results with file results so far
        name_results["dirs"] += item_results["dirs"] # concatenate directory results with directory results so far
        del item_results


    extensions = []
    if include_txt_files.get(): extensions.append(".txt")
    if include_cpp_files.get(): extensions.append(".cpp")
    if include_py_files.get(): extensions.append(".py")
    if include_java_files.get(): extensions.append(".java")

    content_results = {}
    if len(extensions)==0: # no extensions were chosen
        show_results(name_results, {}) # only show name results
        return # end function

    for _dir in valid_dirs:
        # this merges two dictionaries together, overwriting values on duplicate keys
        content_results.update(engine.content_results(_dir, query, extensions))
        # but in this case the same key will never appear twice since a file path is unique

    # show results, with content results sorted by number of matches
    show_results(name_results, sorted(content_results.items(), key=lambda item : item[1][0], reverse=True))

def show_results(name_results: dict[str, list[str]], content_results: list[tuple]):

    if len(name_results["dirs"])==0:
        folder_results_listbox.insert(END, "No results")
    else:
        for folder_name in name_results["dirs"]:
            folder_results_listbox.insert(END, shorten_dir(folder_name))

    if len(name_results["files"])==0:
        file_results_listbox.insert(END, "No results")
    else:
        for file_name in name_results["files"]:
            file_results_listbox.insert(END, shorten_dir(file_name))

    if len(content_results)==0:
        content_results_listbox.insert(END, "No results")
    else:
        for match in content_results:
            content_results_listbox.insert(END, shorten_dir(match[0])) # file name (path)
            matches_listbox.insert(END, match[1][0]) # number of matches
            words_listbox.insert(END, " | ".join(match[1][1][:3])) # words that matched
            lines_listbox.insert(END, ", ".join(str(ln) for ln in match[1][2][:3])) # lines on which the matches occured

    search_btn["state"]="disabled" # disble search button after showing results

def clicked_listbox_item(event):

    index = -1
    try:
        index = content_results_listbox.curselection()[0]
    except IndexError: # nothing is selected
        return

    file_path = content_results_listbox.get(index)
    open_file(os.path.basename(file_path))

def open_file(file_name: str):

    for _dir in valid_dirs:

        print(os.path.isfile(os.path.join(_dir, file_name)))
        # subprocess.run(["notepad.exe", os.path.join(_dir, file_name)])

def quit_app():

    close_app = messagebox.askquestion("Exit","Are you sure you want to exit?")

    if close_app=="yes": mw.destroy()

def shorten_dir(_dir: str, limit: int = 55):
    if(len(_dir) <= limit): return _dir
    return "..." + _dir[len(_dir)-limit+3:]

def scrollbar_cmd(a, b, c=None):

    l = [content_results_listbox, matches_listbox, words_listbox, lines_listbox] # list of all listboxes

    if c:
        for box in l:
            box.yview(a,b,c) # change view for all listboxes

    else:
        for box in l:
            box.yview(a,b)

def listbox_cmd(a, b):

    l = [content_results_listbox, matches_listbox, words_listbox, lines_listbox] # list of all listboxes
    
    for box in l:
        box.yview_moveto(a) # change view for all listboxes

    content_sb.set(a, b)

# key bindings ==============================
def enter(event):

    if str(search_btn["state"])=="disabled": return

    start_search()

def escape(event):

    if str(search_btn["state"])=="disabled":
        reset_window()
        return

    quit_app()

mw.bind("<Return>", enter)
mw.bind("<Escape>", escape)

print("Mini Search Engine: A Project By Youssef Yammine")
# frames ====================================
keywords_frame = LabelFrame(mw,text="Keyword - Files",width=200, height=180,font=1)
keywords_frame.place(x=10, y=10)

directories_frame = LabelFrame(mw,text="Directories",width=mw_width-230, height=180,font=1)
directories_frame.place(x=220, y=10)

results_frame = LabelFrame(mw,text="Results",width=mw_width-20,height=335,font=1)
results_frame.place(x=10, y=200)

# keyword frame ===================================================================================
keyword_label = Label(keywords_frame, text="Keyword: ")
keyword_label.place(x=10,y=20)

keyword_entry = ttk.Entry(keywords_frame, width=16)
keyword_entry.place(x=80,y=20)

file_type_label = Label(keywords_frame, text="File Types:")
file_type_label.place(x=10,y=55)

txt_check = ttk.Checkbutton(keywords_frame, text=".txt",variable=include_txt_files)
txt_check.place(x=78,y=55)

py_check = ttk.Checkbutton(keywords_frame, text=".py",variable=include_py_files)
py_check.place(x=78,y=75)

cpp_check = ttk.Checkbutton(keywords_frame, text=".cpp",variable=include_cpp_files)
cpp_check.place(x=130,y=55)

java_check = ttk.Checkbutton(keywords_frame, text=".java",variable=include_java_files)
java_check.place(x=130,y=75)

file_types_note = Label(keywords_frame,text="Content of checked files will be\nsearched. All other file types will\nbe searched for by name only.")
file_types_note.place(x=8,y=100)

# directory labels ===============================================================================
dir1_label = Label(directories_frame, text="Directory 1: ")
dir1_label.place(x=10,y=20)

dir2_label = Label(directories_frame, text="Directory 2: ")
dir2_label.place(x=10,y=60)

dir3_label = Label(directories_frame, text="Directory 3: ")
dir3_label.place(x=10,y=100)

current_dir_checkbtn = ttk.Checkbutton(

    directories_frame,
    text="Include current directory:\t" + shorten_dir(engine.CURRENT_DIR),
    variable=include_current_dir
    )
current_dir_checkbtn.place(x=11, y=127)

# directory entries ===============================================================================
dir_entry1 = ttk.Entry(directories_frame, width=70)
dir_entry1.place(x=80,y=20)

dir_entry2 = ttk.Entry(directories_frame, width=70)
dir_entry2.place(x=80,y=60)

dir_entry3 = ttk.Entry(directories_frame, width=70)
dir_entry3.place(x=80,y=100)

# results =========================================================================================
folder_results_label = Label(results_frame, text="Folder Names")
folder_results_label.place(x=4, y=8)

folder_results_sb = ttk.Scrollbar(results_frame, orient="horizontal")
folder_results_sb.place(x=88,y=10,relwidth=0.35)

folder_results_listbox = Listbox(results_frame,width=58,height=7, yscrollcommand=folder_results_sb.set)
folder_results_listbox.place(x=5,y=30)

folder_results_sb.config(command=folder_results_listbox.yview)

file_results_label = Label(results_frame, text="File Names")
file_results_label.place(x=364, y=8)

file_results_sb = ttk.Scrollbar(results_frame, orient="horizontal")
file_results_sb.place(x=440,y=10,relwidth=0.35)

file_results_listbox = Listbox(results_frame,width=58,height=7, yscrollcommand=file_results_sb.set)
file_results_listbox.place(x=365,y=30)

file_results_sb.config(command=file_results_listbox.yview)

content_sb = ttk.Scrollbar(results_frame,orient="horizontal")
content_sb.place(x=88, y=158,relwidth=0.35)

content_results_label = Label(results_frame, text="File Content")
content_results_label.place(x=4, y=155)

content_results_listbox = Listbox(results_frame,width=58,height=7, yscrollcommand=listbox_cmd)
content_results_listbox.place(x=5,y=178)
content_results_listbox.bind("<Double-Button>", clicked_listbox_item)

matches_label = Label(results_frame, text="Matches")
matches_label.place(x=364, y=155)
matches_listbox = Listbox(results_frame, width=7, height=7, yscrollcommand=listbox_cmd)
matches_listbox.place(x=365, y=178)

words_label = Label(results_frame, text="Top 3 Matches")
words_label.place(x=420, y=155)
words_listbox = Listbox(results_frame, width=30, height=7, yscrollcommand=listbox_cmd)
words_listbox.place(x=421, y=178)

lines_label = Label(results_frame, text="Lines")
lines_label.place(x=610, y=155)
lines_listbox = Listbox(results_frame, width=17, height=7, yscrollcommand=listbox_cmd)
lines_listbox.place(x=611, y=178)

content_sb.config(command=scrollbar_cmd)

# buttons =========================================================================================
exit_btn = ttk.Button(mw,text="Exit", command=mw.destroy)
exit_btn.place(x=9,y=mw_height-35)

reset_button = ttk.Button(mw,text="Reset (ESC)", command=reset_window)
reset_button.place(x=mw_width - 177, y=mw_height-35)

search_btn = ttk.Button(mw,text="Search (Enter)", command=start_search)
search_btn.place(x=mw_width-93,y=mw_height-35)

reset_window()
# =================================================================================================
if __name__=="__main__": mw.mainloop()