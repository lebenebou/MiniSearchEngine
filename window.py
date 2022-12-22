
from tkinter import *
from tkinter import ttk
from tkinter import messagebox

import engine # from "./engine.py"

# main window initiation ====================
mw = Tk()
mw.title("Seach Engine")
mw_width, mw_height = 750, 580
mw.minsize(mw_width, mw_height)
mw.geometry('+400+200')
mw.resizable(False, False)
mw.iconbitmap("./icon.ico")


# variables =================================
include_current_dir = BooleanVar()
include_current_dir.set(False)

include_txt_files = BooleanVar()
include_txt_files.set(False)

include_py_files = BooleanVar()
include_py_files.set(False)

include_cpp_files = BooleanVar()
include_cpp_files.set(False)

include_java_files = BooleanVar()
include_java_files.set(False)


# functions =================================
def reset_window():

    pass

def start_search():

    query: str = keyword_entry.get().strip().lower()
    if(query == ""):
        messagebox.showerror("Unable To Seach", "Please input a keyword")
        return
    if(not query.isalnum()):
        messagebox.showerror("Unable To Seach", "Please input an alphanumeric keyword")
        return

    dir_candidates = list(set([dir_entry1.get(), dir_entry2.get(), dir_entry3.get()]))
    # get list of directories from entries and remove duplicates
    dir_candidates = [d.strip().lower() for d in dir_candidates if d!=""]
    # strip, lower, and remove empty inputs
    if include_current_dir.get(): dir_candidates.append(engine.CURRENT_DIR.strip().lower())

    if len(dir_candidates) == 0:
        messagebox.showerror("Unable To Search", "No directories were chosen for your search")
        return

    valid_dirs = [d for d in dir_candidates if engine.os.path.isdir(d)]
    if len(valid_dirs)==0: 
        messagebox.showerror("Unable to search", "None of the directories you chose are valid")
        return

    if len(valid_dirs)<len(dir_candidates):
        messagebox.showinfo("Invalid Directories", f"{len(dir_candidates)-len(valid_dirs)} out of {len(dir_candidates)} inputed directories are invalid, the search will not include results from those directories.")

    

    


    

def quit_app():

    pass

def shorten_dir_left(_dir: str):
    if(len(_dir) <= 50): return _dir
    return "..." + _dir[len(_dir)-47:]

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

    if str(search_btn['state'])!='disabled':
        start_search()

# frames ====================================
keywords_frame = LabelFrame(mw,text='Keyword - Files',width=200, height=180,font=1)
keywords_frame.place(x=10, y=10)

directories_frame = LabelFrame(mw,text='Directories',width=mw_width-230, height=180,font=1)
directories_frame.place(x=220, y=10)

results_frame = LabelFrame(mw,text='Results',width=mw_width-20,height=335,font=1)
results_frame.place(x=10, y=200)

# keyword frame ===================================================================================
keyword_label = Label(keywords_frame, text='Keyword: ')
keyword_label.place(x=10,y=20)

keyword_entry = ttk.Entry(keywords_frame, width=16)
keyword_entry.place(x=80,y=20)

file_type_label = Label(keywords_frame, text='File Types:')
file_type_label.place(x=10,y=55)

txt_check = ttk.Checkbutton(keywords_frame, text='.txt',variable=include_txt_files)
txt_check.place(x=78,y=55)

py_check = ttk.Checkbutton(keywords_frame, text='.py',variable=include_py_files)
py_check.place(x=78,y=75)

cpp_check = ttk.Checkbutton(keywords_frame, text='.cpp',variable=include_cpp_files)
cpp_check.place(x=130,y=55)

java_check = ttk.Checkbutton(keywords_frame, text='.java',variable=include_java_files)
java_check.place(x=130,y=75)

file_types_note = Label(keywords_frame,text='Content of checked files will be\nsearched. All other file types will\nbe searched for by name only.')
file_types_note.place(x=8,y=100)

# directory labels ===============================================================================
dir1_label = Label(directories_frame, text='Directory 1: ')
dir1_label.place(x=10,y=20)

dir2_label = Label(directories_frame, text='Directory 2: ')
dir2_label.place(x=10,y=60)

dir3_label = Label(directories_frame, text='Directory 3: ')
dir3_label.place(x=10,y=100)

current_dir_checkbtn = ttk.Checkbutton(

    directories_frame,
    text="Include current directory:\t" + shorten_dir_left(engine.CURRENT_DIR),
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
folder_results_label = Label(results_frame, text='Folder Names')
folder_results_label.place(x=4, y=8)

folder_results_sb = ttk.Scrollbar(results_frame, orient='horizontal')
folder_results_sb.place(x=88,y=10,relwidth=0.35)

folder_results_listbox = Listbox(results_frame,width=58,height=7, yscrollcommand=folder_results_sb.set)
folder_results_listbox.place(x=5,y=30)

folder_results_sb.config(command=folder_results_listbox.yview)

file_results_label = Label(results_frame, text='File Names')
file_results_label.place(x=364, y=8)

file_results_sb = ttk.Scrollbar(results_frame, orient='horizontal')
file_results_sb.place(x=440,y=10,relwidth=0.35)

file_results_listbox = Listbox(results_frame,width=58,height=7, yscrollcommand=file_results_sb.set)
file_results_listbox.place(x=365,y=30)

file_results_sb.config(command=file_results_listbox.yview)

content_sb = ttk.Scrollbar(results_frame,orient='horizontal')
content_sb.place(x=88, y=158,relwidth=0.35)

content_results_label = Label(results_frame, text='File Content')
content_results_label.place(x=4, y=155)

content_results_listbox = Listbox(results_frame,width=58,height=7, yscrollcommand=listbox_cmd)
content_results_listbox.place(x=5,y=178)

matches_label = Label(results_frame, text='Matches')
matches_label.place(x=364, y=155)
matches_listbox = Listbox(results_frame, width=7, height=7, yscrollcommand=listbox_cmd)
matches_listbox.place(x=365, y=178)

words_label = Label(results_frame, text='Top 3 Matches')
words_label.place(x=420, y=155)
words_listbox = Listbox(results_frame, width=30, height=7, yscrollcommand=listbox_cmd)
words_listbox.place(x=421, y=178)

lines_label = Label(results_frame, text='Line')
lines_label.place(x=610, y=155)
lines_listbox = Listbox(results_frame, width=17, height=7, yscrollcommand=listbox_cmd)
lines_listbox.place(x=611, y=178)

content_sb.config(command=scrollbar_cmd)

# buttons =========================================================================================
exit_btn = ttk.Button(mw,text='Exit', command=mw.destroy)
exit_btn.place(x=9,y=mw_height-35)

reset_button = ttk.Button(mw,text='Reset (ESC)', command=reset_window)
reset_button.place(x=mw_width - 177, y=mw_height-35)

search_btn = ttk.Button(mw,text='Search (Enter)', command=start_search)
search_btn.place(x=mw_width-93,y=mw_height-35)

# =================================================================================================
if __name__=="__main__": mw.mainloop()