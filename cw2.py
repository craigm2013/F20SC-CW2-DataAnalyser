import pandas as pd
import numpy as np
import sys, getopt
from views_by_location import *
from views_by_browser import *
from avid_readers import *
from also_likes import *
from tkinter import *
from tkinter import ttk
import histogram_display

import multiprocess as mp
import graphviz



# Base file value granted one is not passed in
file = "sample_100k_lines.json"
try:
    df = pd.read_json(file, lines=True)
except Exception as e:
    None

# functions to retrieve the file for the GUI
def setFile():
    outputText = fileEntry.get()
    global df
    df = pd.read_json(outputText, lines=True)

# 2a Histogram displaying the countries of the document's viewers
def countriesHistogram(doc_id=None):
    if doc_id is None:
        doc_id = docIdEntry.get()
    histogram_display.histogram(
        process_data(df, lambda x: views_by_country(x, doc_id)), "Country",
        "Views by country")


# 2b Histogram displaying the continent of the document's viewers
def continentsHistogram(doc_id=None):
    if doc_id is None:
        doc_id = docIdEntry.get()
    def process(df):
        return views_by_continent(views_by_country(df, doc_id))

    histogram_display.histogram(process_data(df, process), "Continent",
                                "Views by continent")

# 3a Displays histogram of all browser identities
def browserHistogram():
    histogram_display.histogram(process_data(df, views_by_browser), "Browser",
                            "Views by browser")

# 3b Simplifies the browser output to only the main browser name
def browserParsedHistogram():
    histogram_display.histogram(process_data(df, views_by_browser_parsed), "Browser",
                            "Views by browser")
    
    
# 4 GUI implementation of the top readers, displaying a histogram instead of the console output
def topAvidReadersHistogram():
    time_spent = process_data(df, time_spent_by_users)

    histogram_display.histogram(top_ten_readers(time_spent),
                                "User",
                                "Reading time",
                                x_rotation=30)

# 4 Console implementation of the top readers, printing the users into the console instead of a histogram
def printTopTenReaders():
    time_spent = process_data(df, time_spent_by_users)
    top_ten = top_ten_readers(time_spent)
    for user in top_ten.index:
        print(user)

# 5a Prints the user IDs of those that have read the document
def printReaders(df, doc_id):
    def process(df):
        return get_readers(df, doc_id)
    readers = process_data(df, process, lambda a, b: list(set(list(a) + list(b))))
    for reader in readers:
        print(reader)

# 5b Prints the doucment IDs that have been read by the user
def printDocumentsRead(df, user_id):
    def process(df):
        return get_documents_read(df, user_id)
    documents = process_data(df, process, add_lists_uniquely)
    for document in documents:
        print(document)

def add_lists_uniquely(a, b): 
    return list(set(list(a) + list(b)))

# 5c - Returns a list of liked documents
def alsoLikes(dataframe=None, doc_id=None, sorting_function=None, user_id=None):
    # Don't know what to do with the user id
    if dataframe is None:
        dataframe = df
    if doc_id is None:
        doc_id = docIdEntry.get()
    if sorting_function is None:
        sorting_function = sortByNumberOfReaders
    def process_readers(df):
        return get_readers(df, doc_id)

    readers = process_data(dataframe, process_readers, add_lists_uniquely)

    also_liked = {}
    for reader in readers:
        documents_read = process_data(dataframe, 
                lambda x: get_documents_read(x, reader), add_lists_uniquely)
        for document in documents_read:
            if not document == doc_id:
                also_liked[document] = also_liked.get(document, 0) + 1

    for document in sorting_function(also_liked):
        print(document)


    return sorting_function(also_liked)

# 5d - Returns an also like list of documents 
def sortByNumberOfReaders(also_liked):
    return [k for k, _ in sorted(also_liked.items(), key=lambda x: x[1])]



# Duplicating for now for ease of figuring it out
def alsoLikesGraph(dataframe=None, doc_id=None, user_id=None):
    if dataframe is None:
        dataframe = df
    if doc_id == None:
        doc_id = docIdEntry.get()

    if user_id == None:
        user_id = userIdEntry.get()
    readers = process_data(dataframe, lambda x: get_readers(x, doc_id), add_lists_uniquely) 
    also_liked = {}
    users_read = {}
    for reader in readers:
        if not reader == user_id:
            users_read[reader] = process_data(dataframe, 
                    lambda x: get_documents_read(x, reader), add_lists_uniquely)
            for document in users_read[reader]:
                if not document == doc_id:
                    also_liked[document] = also_liked.get(document, 0) + 1
    dot = graphviz.Digraph()
    dot.node(doc_id[-4:], shape="circle", style="filled", fillcolor="green")
    dot.node(user_id[-4:], shape="box", style="filled", fillcolor="green")
    dot.edge(user_id[-4:], doc_id[-4:])
    for document in also_liked.keys():
        dot.node(document[-4:], shape="circle", style="filled", fillcolor="blue")
    for reader in users_read.keys():
        dot.node(reader[-4:], shape="box")
        for document in users_read[reader]:
            dot.edge(reader[-4:], document[-4:])
    dot.render("also_like.gv")
    dot.view()
    

def add_series(a, b): 
    return a.add(b, fill_value=0)


# Abstract out the running of the processing function in case
# we need to parallelize in future for performance
def process_data(df, func, merge_func=add_series):
    pool = mp.Pool(mp.cpu_count())
    split_dfs = np.array_split(df, mp.cpu_count())
    results = pool.map(func, split_dfs)
    pool.close()
    pool.join()
    df = results[0]
    
    for result in results[1:]:
        df = merge_func(df, result)

    return df

# Function for presenting a popout box to display data from
def popoutBox(list = [1,2,3], title = "Popout"):

    popout = Tk()
    popout.title(title)

    for x in range(len(list)):
        Label(popout, text=list[x]).grid(row=x+1, column=1)



# Variables to be used in the window
fileName = ""
doc_id = ""
user_id = ""

fileEntry = None
docIdEntry = None
userIdEntry = None
def run_gui():

    # Creates base window
    window = Tk()
    # Sets window to be height
    frame = ttk.Frame(
        window,
        width=300,
        height=300,
    )
    # Title
    window.title("CW2 Python - Craig MacGregor")

    # Label (window, text ="Cw2 python gshrtsdhrsd").grid(row=1, column = 0, sticky=W)
    # Button (window, text = "Start", command = hello).grid(row=2, column=0, sticky=W)

    # Button(window, text = "View visits by country").grid(row=3, column=5, sticky=W)
    # Label(window, text="").grid(row=10, column=10, sticky=W)

    # fileEntry = Entry(window, width = 25, textvariable = fileName)
    # fileEntry.grid(row=5, column=5, sticky=W)
    # <br> but Python
    Label(window, text="").grid(row=1, column=1)

    Label(window, text="File name:").grid(row=2, column=1)  # Label before text box
    # Text box for the user to put in document name
    global fileEntry
    fileEntry = Entry(window, width=25, textvariable=fileName)
    fileEntry.grid(row=2, column=2, sticky=W)

    Label(window, text="Document ID:").grid(row=3,
                                            column=1)  # Label before text box
    # Text box for the user to put in document name
    global docIdEntry
    docIdEntry = Entry(window, width=25, textvariable=doc_id)
    docIdEntry.grid(row=3, column=2, sticky=W)
    global userIdEntry
    Label(window, text="User ID:").grid(row=4, column=1)
    userIdEntry = Entry(window, width=25, textvariable=user_id)
    userIdEntry.grid(row=4, column = 2, sticky=W)


    Label(window, text="").grid(row=6, column=1)  # <br>
    Label(window, text="Commands:").grid(row=7, column=1)


    #Label(window, text="").grid(row=5, column=1)

    Button(window, text="Set file input", command=setFile).grid(row=8,
                                                                column=1,
                                                                sticky=W)
    Button(window, text="2a - View countries",
        command=countriesHistogram).grid(row=10, column=1, sticky=W)
    Button(window, text="2b - View continents",
        command=continentsHistogram).grid(row=11, column=1, sticky=W)
    Button(window, text="3b - View browsers plainly", command=browserParsedHistogram).grid(row=13,
                                                                        column=1,
                                                                        sticky=W)
    Button(window, text="3a - View browsers", command=browserHistogram).grid(row=12,column=1, sticky=W)
    Button(window, text="4  - View avid readers",
        command=topAvidReadersHistogram).grid(row=14, column=1, sticky=W)

    Button(window, text="5d - See also likes",
        command=alsoLikes).grid(row=15, column=1, sticky=W)
    Button(window, text="6  - See also likes graph",
        command=alsoLikesGraph).grid(row=16, column=1, sticky=W)

    window.mainloop()
    # Runs GUI \/

# Task 8 Functionality 
# Command-line usage

def showCommands():
    print("Possible commands: 2a, 2b, 3a, 3b, 4, 5a, 5b, 5c/5d, 6, 7")
    print("2a - Display a histogram of the countries of the document visitors")
    print("2b - Display a histogram of the continents of the document visitors")
    print("3a - Display a histogram of the browser identities of the users")
    print("3b - Display a histogram of the main browser identity of the user")
    print("4  - Print out the top 10 users in the terminal and their time spent")
    print("5a - Print out the user IDs that visited the specified document")
    print("5b - Print out the document IDs that the specified user has visitied")
    print("5d - Produce an also like list of documents based on userID and docID")
    print("6  - Produce an also likes graph")
    print("7  - Produce a GUI to analyse documents with")

if __name__ == "__main__":
    plainArguments = sys.argv      # Sets arguments passed in to variable cmdArgs
    plainArguments = plainArguments[1:]   # Ignores cw2.py

    # Splits it into command line options and the parameters
    argList, argValues = getopt.getopt(plainArguments, "u:d:t:f:")
    argsList = {}


    for arg, value in argList:
        argsList[arg] = value

    if "-f" in argsList:
        df = pd.read_json(argsList["-f"], lines=True)

    try: 
        if (argsList["-t"] == "2a"):

            countriesHistogram(doc_id=argsList["-d"])
        elif(argsList["-t"] == "2b"):
            continentsHistogram(doc_id=argsList["-d"])
        elif(argsList["-t"] == "3a"):
            browserHistogram()
        elif(argsList["-t"] == "3b"):
            browserParsedHistogram()
        elif(argsList["-t"] == "4"):
            printTopTenReaders()
        elif(argsList["-t"] == "5a"):
            printReaders(df, doc_id=argsList["-d"])
        elif(argsList["-t"] == "5b"):
            printDocumentsRead(df, user_id=argsList["-u"])
        elif(argsList["-t"] in ["5c", "5d"]):
            alsoLikes(df, argsList["-d"], sortByNumberOfReaders, argsList["-u"])
        elif(argsList["-t"] == "6"):
            alsoLikesGraph(df, argsList["-d"], argsList["-u"])
        elif(argsList["-t"] == "7"):
            run_gui()
        else:
            print("Command doesn't exist")
            showCommands()
            
    except Exception as e:
        pass
