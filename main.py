
from tkinter import *
from tkinter import ttk
from tkinter import messagebox

import os

current_directory = os.path.dirname(__file__).capitalize()
os.chdir(current_directory)

#================================= Window Initiation
mw=Tk()
mw.title('Search Engine')
mw_width, mw_height = 750, 580
mw.minsize(mw_width,mw_height)
mw.resizable(False, False)
mw.geometry('+400+150')
mw.iconbitmap('search1.ico')
#====================================== Variables
include_current_dir = BooleanVar()
include_current_dir.set(True)

include_txt_files = BooleanVar()
include_txt_files.set(True)

include_py_files = BooleanVar()
include_py_files.set(False)

include_js_files = BooleanVar()
include_js_files.set(False)

include_m_files = BooleanVar()
include_m_files.set(False)
# 01000011 01101111 01100100 01100101 01100100 00100000 01100010 01111001 00100000 01011001 01101111 01110101 01110011 01110011 01100101 01100110 00100000 01011001 01100001 01101101 01101101 01101001 01101110 01100101
#========================================= Functions
def search():

    start_search = False

    #===Clean directories list==============================================================================================
    list_dir_to_search = [dir_entry1.get().strip(),dir_entry2.get().strip(),dir_entry3.get().strip(),current_directory]
    list_dir_to_search = list(set(list_dir_to_search)) # remove duplicates

    for directory in list_dir_to_search: # remove all empty directories
        if directory=='':
            list_dir_to_search.remove(directory)

    if include_current_dir.get()==False: # remove current directory if checkbox isn't checked
        list_dir_to_search.remove(current_directory)

    
    #===Case Handeling=======================================================================
    keyword = keyword_entry.get().lower()
    
    valid_keyword = False

    i=0
    while valid_keyword==False and i<len(keyword): # check if keyword is valid
        if keyword[i].isalnum():
            valid_keyword=True
        i+=1

    if valid_keyword==True: # keyword is valid

        if len(list_dir_to_search)==0: # user didn't input any directories
            messagebox.showinfo('Unable to search','You haven\'t chosen any directories.')
            start_search = False

        else: # user inputed at least 1 directory

            candidate_number = len(list_dir_to_search) # number of all possible directory candidates
            valid_directories = [d for d in list_dir_to_search if os.path.exists(d)] # all directories that actually exist
            
            invalid_directories = candidate_number - len(valid_directories) # number of directories that don't exist
            
            if len(valid_directories)==0: # All candidates are unvalid directories
                messagebox.showinfo('Unable to search','None of the given directories exist.')
                start_search = False
                
            elif invalid_directories>0: # some directories are invalid, but not all of them
                messagebox.showinfo('Discarded directories','{} out of {} chosen directories won\'t be searched\nbecause they don\'t exist.'.format(invalid_directories,candidate_number))
                start_search = True

            else: # all directories are valid
                start_search = True

    else: # keyword is not valid or empty
        messagebox.showinfo('Unable to search','Invalid Keyword')
        start_search = False
        
    #===Search Algorithm==================================================
    if start_search==True:

        file_results = []
        folder_results = []
        files_to_look_inside = []

        file_types = [] # list containing file types from checkboxes
        if include_txt_files.get()==True: # check box true
            file_types.append('txt')

        if include_py_files.get()==True:
            file_types.append('py')

        if include_m_files.get()==True:
            file_types.append('m')

        if include_js_files.get()==True:
            file_types.append('js')


        def search_folder(folder_path): # looks in folder_path for macthing folders and files and distributes them in the appropriate lists (recursive for folders)

            os.chdir(folder_path)
            for f in os.listdir(folder_path): # loop through files and folders of folder_path

                f_path = folder_path + '\\' + f    # f_path is the complete path of f

                #===Name matches===========================================================
                if f.lower().startswith(keyword): # f starts with the keyword

                    if os.path.isfile(f_path): # f is a file
                        file_results.append(f_path)

                    else: # f is a folder
                        folder_results.append(f_path)
                #===========================================================================

                if os.path.isfile(f_path) and (f.split('.')[-1] in file_types): # f is a file and is a file type to look inside
                    files_to_look_inside.append(f_path)
                
                if os.path.isdir(f_path): # f is a folder
                    search_folder(f_path) # recursion

                os.chdir(current_directory) #  finally, return to current directory


        for d in valid_directories:
            search_folder(d)

        # all 3 lists now have the matching files and folders
        file_results, folder_results, files_to_look_inside

        


        def matches_in_file(file_path): # returns how many times the keyword occurs inside a file

            matches = 0
            line_number = 0
            words_found = []
            lines_found = []

            with open(file_path,'r') as f:
                for line in f:
                    line_number+=1
                    words = line.split()

                    for word in words:
                        if word.lower().startswith(keyword):
                            
                            matches+=1
                            words_found.append(word)
                            lines_found.append(line_number)

            return (matches, words_found, lines_found)

        
        files_with_matches = [file for file in files_to_look_inside if matches_in_file(file)[0]!=0] # files woth matching words inside

        files_matches_dict = {}     # dictionary that contains all files with matches as keys, and (matches, words, lines) as values
        for file in files_with_matches:
            files_matches_dict[file]=matches_in_file(file)

        files_matches_dict = sorted(files_matches_dict.items(), key = lambda t:t[1][0], reverse=True) # sort dictionary by number of matches
    

        #===Displaying Results===========================================
        if len(folder_results)==0:
            folder_results_listbox.insert(END, 'No results')
        else:
            for folder in folder_results:
                folder_results_listbox.insert(END, shorten_dir_left(folder))


        if len(file_results)==0:
            file_results_listbox.insert(END, 'No results')
        else:
            for file in file_results:
                file_results_listbox.insert(END, shorten_dir_left(file))

        # content
        if len(files_with_matches)==0:
            content_results_listbox.insert(END, 'No results')
        else:
            for bigt in files_matches_dict:

                content_results_listbox.insert(END, shorten_dir_left(bigt[0]))
                matches_listbox.insert(END, ' '+str(bigt[1][0]))
                words_listbox.insert(END, bigt[1][1][:3])
                lines_listbox.insert(END , ' '+str(bigt[1][2][:3]))



        search_btn['state']='disabled'



def reset():

    folder_results_listbox.delete(0,END) # clear all list boxes
    file_results_listbox.delete(0,END)
    content_results_listbox.delete(0,END)
    words_listbox.delete(0,END)
    lines_listbox.delete(0,END)
    matches_listbox.delete(0,END)

    search_btn['state']='enabled' # re-enable search button


def shorten_dir_right(d): # shortens a directory from the right side

    if len(d)>58:
        return d[:57]+'...'
    return d

def shorten_dir_left(d): # shortens a directory from the left side

    if len(d)>55:
        out=len(d)-55
        return ' ...'+d[out+3:]
    return d
#=============================== Scrollbars and Listboxes commands
# 01000011 01101111 01100100 01100101 01100100 00100000 01100010 01111001 00100000 01011001 01101111 01110101 01110011 01110011 01100101 01100110 00100000 01011001 01100001 01101101 01101101 01101001 01101110 01100101
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

        

#================================================ Key Bindings

def enter_key(event): # Runs when Enter key is pressed

    if str(search_btn['state'])!='disabled':
        search()

def esc_key(event): # Runs when Esc key is pressed

    if str(search_btn['state'])!='disabled':
        
        close_app = messagebox.askquestion('Exit','Are you sure you want to exit?')

        if close_app=='yes':
            mw.destroy()
    else:
        reset()

mw.bind('<Return>', enter_key)
mw.bind('<Escape>', esc_key)
# 01000011 01101111 01100100 01100101 01100100 00100000 01100010 01111001 00100000 01011001 01101111 01110101 01110011 01110011 01100101 01100110 00100000 01011001 01100001 01101101 01101101 01101001 01101110 01100101
#========================================================================================= Frames - Widgetss
#=========================================================================================
keywords_frame = LabelFrame(mw,text='Keyword - Files',width=200, height=180,font=1)
keywords_frame.place(x=10, y=10)

directories_frame = LabelFrame(mw,text='Directories',width=mw_width-230, height=180,font=1)
directories_frame.place(x=220, y=10)

results_frame = LabelFrame(mw,text='Results',width=mw_width-20,height=335,font=1)
results_frame.place(x=10, y=200)
#========================================================================================= Folder Results
folder_results_label = Label(results_frame, text='Folder Names')
folder_results_label.place(x=4, y=8)

folder_results_sb = ttk.Scrollbar(results_frame, orient='horizontal')
folder_results_sb.place(x=88,y=10,relwidth=0.35)

folder_results_listbox = Listbox(results_frame,width=58,height=7, yscrollcommand=folder_results_sb.set)
folder_results_listbox.place(x=5,y=30)

folder_results_sb.config(command=folder_results_listbox.yview)
#======================================================================================== File Results
file_results_label = Label(results_frame, text='File Names')
file_results_label.place(x=364, y=8)

file_results_sb = ttk.Scrollbar(results_frame, orient='horizontal')
file_results_sb.place(x=440,y=10,relwidth=0.35)

file_results_listbox = Listbox(results_frame,width=58,height=7, yscrollcommand=file_results_sb.set)
file_results_listbox.place(x=365,y=30)

file_results_sb.config(command=file_results_listbox.yview)
#======================================================================================== Content Results
# 01000011 01101111 01100100 01100101 01100100 00100000 01100010 01111001 00100000 01011001 01101111 01110101 01110011 01110011 01100101 01100110 00100000 01011001 01100001 01101101 01101101 01101001 01101110 01100101
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
# 01000011 01101111 01100100 01100101 01100100 00100000 01100010 01111001 00100000 01011001 01101111 01110101 01110011 01110011 01100101 01100110 00100000 01011001 01100001 01101101 01101101 01101001 01101110 01100101
#========================================================================================= Labels - Checkboxes
keyword_label = Label(keywords_frame, text='Keyword: ')
keyword_label.place(x=10,y=20)

file_type_label = Label(keywords_frame, text='File Types:')
file_type_label.place(x=10,y=55)

txt_check = ttk.Checkbutton(keywords_frame, text='.txt',variable=include_txt_files)
txt_check.place(x=78,y=55)

py_check = ttk.Checkbutton(keywords_frame, text='.py',variable=include_py_files)
py_check.place(x=78,y=75)

m_check = ttk.Checkbutton(keywords_frame, text='.m',variable=include_m_files)
m_check.place(x=130,y=55)

js_check = ttk.Checkbutton(keywords_frame, text='.js',variable=include_js_files)
js_check.place(x=130,y=75)

file_types_note = Label(keywords_frame,text='Content of checked files will be\nsearched. All other file types will\nbe searched for by name only.')
file_types_note.place(x=8,y=100)
#=========================================================================================
keyword_entry = ttk.Entry(keywords_frame, width=16)
keyword_entry.place(x=80,y=20)
#=========================================================================================
directory1 = Label(directories_frame, text='Directory 1: ')
directory1.place(x=10,y=20)

directory2 = Label(directories_frame, text='Directory 2: ')
directory2.place(x=10,y=60)

directory3 = Label(directories_frame, text='Directory 3: ')
directory3.place(x=10,y=100)
#========================================================================================= Directory entries
dir_entry1 = ttk.Entry(directories_frame, width=70)
dir_entry1.place(x=80,y=20)

dir_entry2 = ttk.Entry(directories_frame, width=70)
dir_entry2.place(x=80,y=60)

dir_entry3 = ttk.Entry(directories_frame, width=70)
dir_entry3.place(x=80,y=100)
#========================================================================================= # Buttons
current_dir_checkbtn = ttk.Checkbutton(directories_frame, text='Include current directory: '+shorten_dir_right(current_directory),variable=include_current_dir)
current_dir_checkbtn.place(x=11, y=127)

reset_btn = ttk.Button(mw,text='Reset (Esc)', command=reset)
reset_btn.place(x=mw_width-177,y=mw_height-35)

search_btn = ttk.Button(mw,text='Search (Enter)', command=search)
search_btn.place(x=mw_width-93,y=mw_height-35)

exit_btn = ttk.Button(mw,text='Exit', command=mw.destroy)
exit_btn.place(x=9,y=mw_height-35)
#==========================================
mw.mainloop()

# ================================================== Coded By Youssef Yammine ================================================== #