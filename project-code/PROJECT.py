from pytesseract import pytesseract
from PIL import Image as IMG
from fuzzywuzzy import fuzz

import bs4
import tempfile
import cv2
import numpy as np


try:
    from Tkinter import *
    from tkinter import filedialog
    from tkinter import messagebox
    from ast import literal_eval

except ImportError:
    from tkinter import *
    from tkinter import filedialog
    from tkinter import messagebox
    from ast import literal_eval


######GUI BUILD##########


def vp_start_gui():
    '''Starting point when module is the main routine.'''
    global val, w, root, KEYWORD_STR, ABOVE, BELOW, LEFT, RIGHT, WEIGHT, REGEX_STR, SAMELINE_WEIGHT, KW_ATT, RE_ATT, word, candidates, context, groupcontext, results, BINARY_THREHOLD, fp
    root = Tk()
    KEYWORD_STR = StringVar(root, value="")
    REGEX_STR = StringVar(root, value="")
    ABOVE = StringVar(root, value=0.0)
    BELOW = StringVar(root, value=0.0)
    LEFT = StringVar(root, value=0.0)
    RIGHT = StringVar(root, value=0.0)
    WEIGHT = StringVar(root, value=0.0)
    SAMELINE_WEIGHT = StringVar(root, value=0.0)

    word = {1: {'Value': '', 'Confidence': '', 'Left': '', 'Top': '', 'Right': '', 'Bottom': ''}}
    candidates = {1: {'Value': '', 'Confidence': '', 'Left': '', 'Top': '', 'Right': '', 'Bottom': ''}}
    context = {1: {'Value': '', 'Candidates': '', 'Word': '', 'Confidence': '', 'Left': '', 'Top': '', 'Right': '',
                   'Bottom': '', 'Line': '', 'SameLine': ''}}
    groupcontext = {1: {'Value': '', 'Candidates': '', 'Word': '', 'Confidence': '', 'Left': '', 'Top': '', 'Right': '',
                        'Bottom': '', 'Line': '', 'SameLine': '', 'Weight': ''}}
    results = {'TEST': 0.0}

    fp = ""

    RE_ATT = list()
    KW_ATT = dict()
    BINARY_THREHOLD = 180

    top = Extraction(root)

    root.mainloop()


w = None


def create_Extraction(root, *args, **kwargs):
    '''Starting point when module is imported by another program.'''
    global w, w_win, rt
    rt = root
    w = Toplevel(root)
    top = Extraction(w)

    return (w, top)


def destroy_Extraction():
    global w
    w.destroy()
    w = None


class Extraction:
    def __init__(self, top=None):
        '''This class configures and populates the toplevel window.
           top is the toplevel containing window.'''
        _bgcolor = '#d9d9d9'  # X11 color: 'gray85'
        _fgcolor = '#000000'  # X11 color: 'black'
        _compcolor = '#d9d9d9'  # X11 color: 'gray85'
        _ana1color = '#d9d9d9'  # X11 color: 'gray85'
        _ana2color = '#d9d9d9'  # X11 color: 'gray85'
        font9 = "-family Rockwell -size 8 -weight normal -slant roman " \
                "-underline 0 -overstrike 0"

        top.geometry("544x459+752+115")
        top.title("Extraction")
        top.configure(background="#d9d9d9")
        top.configure(highlightbackground="#d9d9d9")
        top.configure(highlightcolor="black")

        self.ListBox_RegEx = Listbox(top)
        self.ListBox_RegEx.place(relx=0.02, rely=0.22, relheight=0.52, relwidth=0.3)
        self.ListBox_RegEx.bind('<<ListboxSelect>>', self.select_RegEx)
        self.ListBox_RegEx.configure(background="white")
        self.ListBox_RegEx.configure(disabledforeground="#a3a3a3")
        self.ListBox_RegEx.configure(font="TkFixedFont")
        self.ListBox_RegEx.configure(foreground="#000000")
        self.ListBox_RegEx.configure(highlightbackground="#d9d9d9")
        self.ListBox_RegEx.configure(highlightcolor="black")
        self.ListBox_RegEx.configure(selectbackground="#c4c4c4")
        self.ListBox_RegEx.configure(selectforeground="black")
        self.ListBox_RegEx.configure(width=164)
        self.ListBox_RegEx.configure(selectmode=SINGLE)

        self.ListBox_Keyword = Listbox(top)
        self.ListBox_Keyword.place(relx=0.68, rely=0.22, relheight=0.52, relwidth=0.3)
        self.ListBox_Keyword.bind('<<ListboxSelect>>', self.select_Keyword)
        self.ListBox_Keyword.configure(background="white")
        self.ListBox_Keyword.configure(disabledforeground="#a3a3a3")
        self.ListBox_Keyword.configure(font="TkFixedFont")
        self.ListBox_Keyword.configure(foreground="#000000")
        self.ListBox_Keyword.configure(highlightbackground="#d9d9d9")
        self.ListBox_Keyword.configure(highlightcolor="black")
        self.ListBox_Keyword.configure(selectbackground="#c4c4c4")
        self.ListBox_Keyword.configure(selectforeground="black")
        self.ListBox_Keyword.configure(width=164)
        self.ListBox_RegEx.configure(selectmode=SINGLE)

        ##################################BUTTONS#################################################

        self.Button_AddRegEx = Button(top)
        self.Button_AddRegEx.place(relx=0.02, rely=0.74, height=24, width=164)
        self.Button_AddRegEx.configure(activebackground="#d9d9d9")
        self.Button_AddRegEx.configure(activeforeground="#000000")
        self.Button_AddRegEx.configure(background="#d9d9d9")
        self.Button_AddRegEx.configure(command=self.add_RegEx)
        self.Button_AddRegEx.configure(disabledforeground="#a3a3a3")
        self.Button_AddRegEx.configure(foreground="#000000")
        self.Button_AddRegEx.configure(highlightbackground="#d9d9d9")
        self.Button_AddRegEx.configure(highlightcolor="black")
        self.Button_AddRegEx.configure(pady="0")
        self.Button_AddRegEx.configure(text='''Add/Update RegEx''')

        self.Button_DeleteRegEx = Button(top)
        self.Button_DeleteRegEx.place(relx=0.02, rely=0.8, height=24, width=164)
        self.Button_DeleteRegEx.configure(activebackground="#d9d9d9")
        self.Button_DeleteRegEx.configure(activeforeground="#000000")
        self.Button_DeleteRegEx.configure(background="#d9d9d9")
        self.Button_DeleteRegEx.configure(command=self.delete_RegEx)
        self.Button_DeleteRegEx.configure(disabledforeground="#a3a3a3")
        self.Button_DeleteRegEx.configure(foreground="#000000")
        self.Button_DeleteRegEx.configure(highlightbackground="#d9d9d9")
        self.Button_DeleteRegEx.configure(highlightcolor="black")
        self.Button_DeleteRegEx.configure(pady="0")
        self.Button_DeleteRegEx.configure(text='''Delete RegEx''')

        self.Button_AddKeyword = Button(top)
        self.Button_AddKeyword.place(relx=0.68, rely=0.74, height=24, width=164)
        self.Button_AddKeyword.configure(activebackground="#d9d9d9")
        self.Button_AddKeyword.configure(activeforeground="#000000")
        self.Button_AddKeyword.configure(background="#d9d9d9")
        self.Button_AddKeyword.configure(command=self.add_Keyword)
        self.Button_AddKeyword.configure(disabledforeground="#a3a3a3")
        self.Button_AddKeyword.configure(foreground="#000000")
        self.Button_AddKeyword.configure(highlightbackground="#d9d9d9")
        self.Button_AddKeyword.configure(highlightcolor="black")
        self.Button_AddKeyword.configure(pady="0")
        self.Button_AddKeyword.configure(text='''Add/Update RegEx''')

        self.Button_DeleteKeyword = Button(top)
        self.Button_DeleteKeyword.place(relx=0.68, rely=0.8, height=24, width=164)
        self.Button_DeleteKeyword.configure(activebackground="#d9d9d9")
        self.Button_DeleteKeyword.configure(activeforeground="#000000")
        self.Button_DeleteKeyword.configure(background="#d9d9d9")
        self.Button_DeleteKeyword.configure(command=self.delete_Keyword)
        self.Button_DeleteKeyword.configure(disabledforeground="#a3a3a3")
        self.Button_DeleteKeyword.configure(foreground="#000000")
        self.Button_DeleteKeyword.configure(highlightbackground="#d9d9d9")
        self.Button_DeleteKeyword.configure(highlightcolor="black")
        self.Button_DeleteKeyword.configure(pady="0")
        self.Button_DeleteKeyword.configure(text='''Delete RegEx''')

        self.Button_Run = Button(top)
        self.Button_Run.place(relx=0.02, rely=0.92, height=24, width=524)
        self.Button_Run.configure(activebackground="#d9d9d9")
        self.Button_Run.configure(activeforeground="#000000")
        self.Button_Run.configure(background="#d9d9d9")
        self.Button_Run.configure(command=self.Run)
        self.Button_Run.configure(disabledforeground="#a3a3a3")
        self.Button_Run.configure(foreground="#000000")
        self.Button_Run.configure(highlightbackground="#d9d9d9")
        self.Button_Run.configure(highlightcolor="black")
        self.Button_Run.configure(pady="0")
        self.Button_Run.configure(text='Run')
        self.Button_Run.configure(width=524)

        #########################LABEL###################################################

        self.Label_RegExList = Label(top)
        self.Label_RegExList.place(relx=0.02, rely=0.16, height=21, width=164)
        self.Label_RegExList.configure(activebackground="#f9f9f9")
        self.Label_RegExList.configure(activeforeground="black")
        self.Label_RegExList.configure(background="#d9d9d9")
        self.Label_RegExList.configure(disabledforeground="#a3a3a3")
        self.Label_RegExList.configure(foreground="#000000")
        self.Label_RegExList.configure(highlightbackground="#d9d9d9")
        self.Label_RegExList.configure(highlightcolor="black")
        self.Label_RegExList.configure(text='''Candidate RegEx List''')

        self.Label_KeywordSearchArea = Label(top)
        self.Label_KeywordSearchArea.place(relx=0.35, rely=0.38, height=21, width=164)
        self.Label_KeywordSearchArea.configure(activebackground="#f9f9f9")
        self.Label_KeywordSearchArea.configure(activeforeground="black")
        self.Label_KeywordSearchArea.configure(background="#d9d9d9")
        self.Label_KeywordSearchArea.configure(disabledforeground="#a3a3a3")
        self.Label_KeywordSearchArea.configure(foreground="#000000")
        self.Label_KeywordSearchArea.configure(highlightbackground="#d9d9d9")
        self.Label_KeywordSearchArea.configure(highlightcolor="black")
        self.Label_KeywordSearchArea.configure(text='''Keyword Search Area (pixels)''')

        self.Label_Candidate = Label(top)
        self.Label_Candidate.place(relx=0.45, rely=0.52, height=21, width=52)
        self.Label_Candidate.configure(activebackground="#f9f9f9")
        self.Label_Candidate.configure(activeforeground="black")
        self.Label_Candidate.configure(background="#d9d9d9")
        self.Label_Candidate.configure(disabledforeground="#a3a3a3")
        self.Label_Candidate.configure(font=font9)
        self.Label_Candidate.configure(foreground="#000000")
        self.Label_Candidate.configure(highlightbackground="#d9d9d9")
        self.Label_Candidate.configure(highlightcolor="black")
        self.Label_Candidate.configure(text='''Candidate''')

        self.Label_Above = Label(top)
        self.Label_Above.place(relx=0.45, rely=0.42, height=21, width=50)
        self.Label_Above.configure(activebackground="#f9f9f9")
        self.Label_Above.configure(activeforeground="black")
        self.Label_Above.configure(background="#d9d9d9")
        self.Label_Above.configure(disabledforeground="#a3a3a3")
        self.Label_Above.configure(foreground="#000000")
        self.Label_Above.configure(highlightbackground="#d9d9d9")
        self.Label_Above.configure(highlightcolor="black")
        self.Label_Above.configure(text='''Above''')

        self.Label_Left = Label(top)
        self.Label_Left.place(relx=0.35, rely=0.47, height=21, width=50)
        self.Label_Left.configure(activebackground="#f9f9f9")
        self.Label_Left.configure(activeforeground="black")
        self.Label_Left.configure(background="#d9d9d9")
        self.Label_Left.configure(disabledforeground="#a3a3a3")
        self.Label_Left.configure(foreground="#000000")
        self.Label_Left.configure(highlightbackground="#d9d9d9")
        self.Label_Left.configure(highlightcolor="black")
        self.Label_Left.configure(text='''Left''')

        self.Label_Right = Label(top)
        self.Label_Right.place(relx=0.56, rely=0.48, height=21, width=50)
        self.Label_Right.configure(activebackground="#f9f9f9")
        self.Label_Right.configure(activeforeground="black")
        self.Label_Right.configure(background="#d9d9d9")
        self.Label_Right.configure(disabledforeground="#a3a3a3")
        self.Label_Right.configure(foreground="#000000")
        self.Label_Right.configure(highlightbackground="#d9d9d9")
        self.Label_Right.configure(highlightcolor="black")
        self.Label_Right.configure(text='''Right''')

        self.Label_Below = Label(top)
        self.Label_Below.place(relx=0.45, rely=0.63, height=21, width=50)
        self.Label_Below.configure(activebackground="#f9f9f9")
        self.Label_Below.configure(activeforeground="black")
        self.Label_Below.configure(background="#d9d9d9")
        self.Label_Below.configure(disabledforeground="#a3a3a3")
        self.Label_Below.configure(foreground="#000000")
        self.Label_Below.configure(highlightbackground="#d9d9d9")
        self.Label_Below.configure(highlightcolor="black")
        self.Label_Below.configure(text='''Below''')

        self.Label_Weight = Label(top)
        self.Label_Weight.place(relx=0.35, rely=0.22, height=21, width=164)
        self.Label_Weight.configure(activebackground="#f9f9f9")
        self.Label_Weight.configure(activeforeground="black")
        self.Label_Weight.configure(background="#d9d9d9")
        self.Label_Weight.configure(disabledforeground="#a3a3a3")
        self.Label_Weight.configure(foreground="#000000")
        self.Label_Weight.configure(highlightbackground="#d9d9d9")
        self.Label_Weight.configure(highlightcolor="black")
        self.Label_Weight.configure(text='''Keyword Weight Ratio''')

        self.Label_RegEx = Label(top)
        self.Label_RegEx.place(relx=0.02, rely=0.02, height=21, width=164)
        self.Label_RegEx.configure(activebackground="#f9f9f9")
        self.Label_RegEx.configure(activeforeground="black")
        self.Label_RegEx.configure(background="#d9d9d9")
        self.Label_RegEx.configure(disabledforeground="#a3a3a3")
        self.Label_RegEx.configure(foreground="#000000")
        self.Label_RegEx.configure(highlightbackground="#d9d9d9")
        self.Label_RegEx.configure(highlightcolor="black")
        self.Label_RegEx.configure(text='''Candidate RegEx''')

        self.Label_Keyword = Label(top)
        self.Label_Keyword.place(relx=0.68, rely=0.02, height=21, width=164)
        self.Label_Keyword.configure(activebackground="#f9f9f9")
        self.Label_Keyword.configure(activeforeground="black")
        self.Label_Keyword.configure(background="#d9d9d9")
        self.Label_Keyword.configure(cursor="fleur")
        self.Label_Keyword.configure(disabledforeground="#a3a3a3")
        self.Label_Keyword.configure(foreground="#000000")
        self.Label_Keyword.configure(highlightbackground="#d9d9d9")
        self.Label_Keyword.configure(highlightcolor="black")
        self.Label_Keyword.configure(text='''Keyword/Context''')

        self.Label_KeywordList = Label(top)
        self.Label_KeywordList.place(relx=0.68, rely=0.15, height=21, width=164)
        self.Label_KeywordList.configure(activebackground="#f9f9f9")
        self.Label_KeywordList.configure(activeforeground="black")
        self.Label_KeywordList.configure(background="#d9d9d9")
        self.Label_KeywordList.configure(disabledforeground="#a3a3a3")
        self.Label_KeywordList.configure(foreground="#000000")
        self.Label_KeywordList.configure(highlightbackground="#d9d9d9")
        self.Label_KeywordList.configure(highlightcolor="black")
        self.Label_KeywordList.configure(text='''Keyword/Context List''')

        self.Label_SameLine = Label(top)
        self.Label_SameLine.place(relx=0.35, rely=0.69, height=21, width=164)
        self.Label_SameLine.configure(activebackground="#f9f9f9")
        self.Label_SameLine.configure(activeforeground="black")
        self.Label_SameLine.configure(background="#d9d9d9")
        self.Label_SameLine.configure(disabledforeground="#a3a3a3")
        self.Label_SameLine.configure(foreground="#000000")
        self.Label_SameLine.configure(highlightbackground="#d9d9d9")
        self.Label_SameLine.configure(highlightcolor="black")
        self.Label_SameLine.configure(text='''Same Line Boost''')

        ###################ENTRY#########################################################

        self.Location_Above = Entry(top)
        self.Location_Above.place(relx=0.45, rely=0.48, height=20, relwidth=0.09)
        self.Location_Above.configure(textvariable=ABOVE)
        self.Location_Above.configure(background="white")
        self.Location_Above.configure(disabledforeground="#a3a3a3")
        self.Location_Above.configure(font="TkFixedFont")
        self.Location_Above.configure(foreground="#000000")
        self.Location_Above.configure(highlightbackground="#d9d9d9")
        self.Location_Above.configure(highlightcolor="black")
        self.Location_Above.configure(insertbackground="black")
        self.Location_Above.configure(selectbackground="#c4c4c4")
        self.Location_Above.configure(selectforeground="black")

        self.Location_Left = Entry(top)
        self.Location_Left.place(relx=0.35, rely=0.52, height=20, relwidth=0.09)
        self.Location_Left.configure(textvariable=LEFT)
        self.Location_Left.configure(background="white")
        self.Location_Left.configure(disabledforeground="#a3a3a3")
        self.Location_Left.configure(font="TkFixedFont")
        self.Location_Left.configure(foreground="#000000")
        self.Location_Left.configure(highlightbackground="#d9d9d9")
        self.Location_Left.configure(highlightcolor="black")
        self.Location_Left.configure(insertbackground="black")
        self.Location_Left.configure(selectbackground="#c4c4c4")
        self.Location_Left.configure(selectforeground="black")

        self.Location_Right = Entry(top)
        self.Location_Right.place(relx=0.56, rely=0.52, height=20, relwidth=0.09)
        self.Location_Right.configure(textvariable=RIGHT)
        self.Location_Right.configure(background="#ffffff")
        self.Location_Right.configure(disabledbackground="#f0f0f0f0f0f0")
        self.Location_Right.configure(disabledforeground="#a3a3a3")
        self.Location_Right.configure(font="TkFixedFont")
        self.Location_Right.configure(foreground="#000000")
        self.Location_Right.configure(highlightbackground="#d9d9d9")
        self.Location_Right.configure(highlightcolor="black")
        self.Location_Right.configure(insertbackground="black")
        self.Location_Right.configure(selectbackground="#c4c4c4")
        self.Location_Right.configure(selectforeground="black")

        self.Location_Below = Entry(top)
        self.Location_Below.place(relx=0.45, rely=0.58, height=20, relwidth=0.09)
        self.Location_Below.configure(textvariable=BELOW)
        self.Location_Below.configure(background="white")
        self.Location_Below.configure(disabledforeground="#a3a3a3")
        self.Location_Below.configure(font="TkFixedFont")
        self.Location_Below.configure(foreground="#000000")
        self.Location_Below.configure(highlightbackground="#d9d9d9")
        self.Location_Below.configure(highlightcolor="black")
        self.Location_Below.configure(insertbackground="black")
        self.Location_Below.configure(selectbackground="#c4c4c4")
        self.Location_Below.configure(selectforeground="black")

        self.RegEx = Entry(top)
        self.RegEx.place(relx=0.02, rely=0.09, height=20, relwidth=0.3)
        self.RegEx.configure(textvariable=REGEX_STR)
        self.RegEx.configure(background="white")
        self.RegEx.configure(disabledforeground="#a3a3a3")
        self.RegEx.configure(font="TkFixedFont")
        self.RegEx.configure(foreground="#000000")
        self.RegEx.configure(highlightbackground="#d9d9d9")
        self.RegEx.configure(highlightcolor="black")
        self.RegEx.configure(insertbackground="black")
        self.RegEx.configure(selectbackground="#c4c4c4")
        self.RegEx.configure(selectforeground="black")

        self.Keyword = Entry(top)
        self.Keyword.place(relx=0.68, rely=0.09, height=20, relwidth=0.3)
        self.Keyword.configure(textvariable=KEYWORD_STR)
        self.Keyword.configure(background="white")
        self.Keyword.configure(disabledforeground="#a3a3a3")
        self.Keyword.configure(font="TkFixedFont")
        self.Keyword.configure(foreground="#000000")
        self.Keyword.configure(highlightbackground="#d9d9d9")
        self.Keyword.configure(highlightcolor="black")
        self.Keyword.configure(insertbackground="black")
        self.Keyword.configure(selectbackground="#c4c4c4")
        self.Keyword.configure(selectforeground="black")

        ###################SCALE###############################################

        self.Scale_Weight = Scale(top)
        self.Scale_Weight.place(relx=0.35, rely=0.27, relwidth=0.3, relheight=0.0, height=42)
        self.Scale_Weight.configure(activebackground="#d9d9d9")
        self.Scale_Weight.configure(background="#d9d9d9")
        self.Scale_Weight.configure(font="TkTextFont")
        self.Scale_Weight.configure(foreground="#000000")
        self.Scale_Weight.configure(from_="-100")
        self.Scale_Weight.configure(highlightbackground="#d9d9d9")
        self.Scale_Weight.configure(highlightcolor="black")
        self.Scale_Weight.configure(orient="horizontal")
        self.Scale_Weight.configure(sliderrelief="ridge")
        self.Scale_Weight.configure(to="100")
        self.Scale_Weight.configure(troughcolor="#d9d9d9")
        self.Scale_Weight.configure(variable=WEIGHT)

        self.Scale_SameLine = Scale(top)
        self.Scale_SameLine.place(relx=0.35, rely=0.74, relwidth=0.3, relheight=0.0, height=42)
        self.Scale_SameLine.configure(activebackground="#d9d9d9")
        self.Scale_SameLine.configure(background="#d9d9d9")
        self.Scale_SameLine.configure(font="TkTextFont")
        self.Scale_SameLine.configure(foreground="#000000")
        self.Scale_SameLine.configure(from_="-100")
        self.Scale_SameLine.configure(highlightbackground="#d9d9d9")
        self.Scale_SameLine.configure(highlightcolor="black")
        self.Scale_SameLine.configure(orient="horizontal")
        self.Scale_SameLine.configure(sliderrelief="ridge")
        self.Scale_SameLine.configure(to="100")
        self.Scale_SameLine.configure(troughcolor="#d9d9d9")
        self.Scale_SameLine.configure(variable=SAMELINE_WEIGHT)

        self.Frame1 = Frame(top)
        self.Frame1.place(relx=0.02, rely=0.87, relheight=0.01, relwidth=0.97)
        self.Frame1.configure(relief=GROOVE)
        self.Frame1.configure(borderwidth="2")
        self.Frame1.configure(relief=GROOVE)
        self.Frame1.configure(background="#d9d9d9")
        self.Frame1.configure(highlightbackground="#d9d9d9")
        self.Frame1.configure(highlightcolor="black")
        self.Frame1.configure(width=525)

    def add_Keyword(self):

        to_add = KEYWORD_STR.get()
        iscontain = to_add in self.ListBox_Keyword.get(0, "end");
        if not iscontain:
            self.ListBox_Keyword.insert('end', to_add)

            self.ListBox_Keyword.selection_clear(0, 'end')
            self.ListBox_Keyword.selection_set(self.ListBox_Keyword.get(0, "end").index(to_add))

        KW_ATT[to_add] = (
            WEIGHT.get(), ABOVE.get(), LEFT.get(), RIGHT.get(), BELOW.get(), SAMELINE_WEIGHT.get())

    def delete_Keyword(self):

        to_add = KEYWORD_STR.get()
        index = self.ListBox_Keyword.get(0, "end").index(to_add)

        iscontain = to_add in self.ListBox_Keyword.get(0, "end");
        if iscontain:
            self.ListBox_Keyword.delete(index, index)
        else:
            print("KW not in the list, cannot delete")
        del KW_ATT[to_add]
        print(KW_ATT)

    def add_RegEx(self):

        to_add = REGEX_STR.get()

        iscontain = to_add in self.ListBox_RegEx.get(0, "end");

        if not iscontain:
            self.ListBox_RegEx.insert('end', to_add)
            self.ListBox_RegEx.selection_clear(0, 'end')
            self.ListBox_RegEx.selection_set(self.ListBox_RegEx.get(0, "end").index(to_add))
            RE_ATT.append(to_add)

        REGEX_STR.set("")
        print(RE_ATT)

    def delete_RegEx(self):

        to_delete = REGEX_STR.get()

        index = self.ListBox_RegEx.get(0, "end").index(to_delete)

        iscontain = to_delete in self.ListBox_RegEx.get(0, "end");
        if iscontain:
            self.ListBox_RegEx.delete(index, index)
            RE_ATT.remove(to_delete)
        else:
            print("REGEX not in the list, cannot delete")

        REGEX_STR.set("")

    def select_Keyword(self, event):
        w = event.widget

        if len(w.curselection()) > 0:
            index = int(w.curselection()[0])

            value = w.get(index)
            KEYWORD_STR.set(value)
            WEIGHT.set(KW_ATT[value][0])
            ABOVE.set(KW_ATT[value][1])
            LEFT.set(KW_ATT[value][2])
            RIGHT.set(KW_ATT[value][3])
            BELOW.set(KW_ATT[value][4])
            SAMELINE_WEIGHT.set(KW_ATT[value][5])

    def select_RegEx(self, event):
        w = event.widget
        if len(w.curselection()) > 0:
            index = int(w.curselection()[0])
            value = w.get(index)
            REGEX_STR.set(value)

    def load_screen(self, KW_ATT):

        for key in KW_ATT:
            self.ListBox_Keyword.insert('end', key)
            WEIGHT.set(KW_ATT[key][0])
            ABOVE.set(KW_ATT[key][1])
            LEFT.set(KW_ATT[key][2])
            RIGHT.set(KW_ATT[key][3])
            BELOW.set(KW_ATT[key][4])
            SAMELINE_WEIGHT.set(KW_ATT[key][5])

    def Run(self):

        #Select image file to be processed
        file_path_string = filedialog.askopenfilename()

        #Run selected image thru preprocessor for clean up
        image = processimage(file_path_string)

        #Store file name to be used to generate output text file
        fp = file_path_string
        fp = fp[fp.rfind('/') + 1:]
        fp = fp[:fp.find('.')]

        #Clear all data before each run
        word.clear()
        candidates.clear()
        context.clear()
        groupcontext.clear()
        results.clear()

        #Send cleaned up image thru OCR process
        DATA = pytesseract.image_to_pdf_or_hocr(image, lang=None, config='hocr', nice=0, extension='hocr')

        #Parse OCR Data, keeping only the word data
        soup = bs4.BeautifulSoup(DATA, 'html.parser')
        words = soup.find_all('span', class_='ocrx_word')

        #Load HOCR into word dictionary objects
        transform_hocr(self, words)

        #Finding candidates based on regular expression provided by user
        find_candidates(self, RE_ATT)

        #Set context around each candidate found
        set_context(self, candidates, word)

        #Group context based on word sequence and line number
        define_groupcontext(self, context)

        #Score each candidate based on context found and context provided by user
        weightcontext(self, KW_ATT)

        #Output results to text file
        outputresults(self, groupcontext, fp)

        messagebox.showinfo("Output Generated", "Process Complete, please review output file.")

def transform_hocr(self, words):
    # Convert HOCR to usable structure
    # Storing all word variables into a word dictionary with the following data:
    # value, confidence, positioning(left, top, right and bottom)

    for x in range(len(words)):
        word[int(words[x]['id'].split('_')[2])] = {}
        word[int(words[x]['id'].split('_')[2])]['Value'] = words[x].get_text()
        word[int(words[x]['id'].split('_')[2])]['Confidence'] = words[x]['title'].split(';')[1].split(' ')[2]
        word[int(words[x]['id'].split('_')[2])]['Left'] = words[x]['title'].split(';')[0].split(' ')[1]
        word[int(words[x]['id'].split('_')[2])]['Top'] = words[x]['title'].split(';')[0].split(' ')[2]
        word[int(words[x]['id'].split('_')[2])]['Right'] = words[x]['title'].split(';')[0].split(' ')[3]
        word[int(words[x]['id'].split('_')[2])]['Bottom'] = words[x]['title'].split(';')[0].split(' ')[4]



def find_candidates(self, RE_ATT):
    # Looping thru each regular expression provided by user and identifying matches on the image
    # Storing all candidates into the candidate dictionary with the following data:
    # value, confidence, positioning(left, top, right and bottom)
    y = 1
    for z in RE_ATT:

        for x in range(len(word)):

            m = re.match(r'' + z + '', word[x + 1]['Value'], )

            if m:
                candidates[y] = {}
                candidates[y]['Value'] = word[x + 1]['Value']
                candidates[y]['Confidence'] = word[x + 1]['Confidence']
                candidates[y]['Left'] = word[x + 1]['Left']
                candidates[y]['Top'] = word[x + 1]['Top']
                candidates[y]['Right'] = word[x + 1]['Right']
                candidates[y]['Bottom'] = word[x + 1]['Bottom']

                y = y + 1


def set_context(self, candidates, word):
    # Looping thru each candidate and assigning context by using the search area provided by user
    # Storing all context into the context dictionary with the following data:
    # value, confidence, positioning(left, top, right and bottom), line and same line as candidate
    line = 1
    z = 1
    for x in range(len(candidates)):

        for y in range(len(word)):

            if (int(word[y + 1]['Bottom']) > int(candidates[x + 1]['Bottom']) - float(ABOVE.get())) and \
                    (int(word[y + 1]['Bottom']) < int(candidates[x + 1]['Bottom']) + (float(BELOW.get())) +10.0) and \
                    (int(word[y + 1]['Right']) > int(candidates[x + 1]['Left']) - float(LEFT.get())) and \
                    (int(word[y + 1]['Right']) < int(candidates[x + 1]['Left']) + (float(RIGHT.get()) + 10.0)):

                context[z] = {}
                context[z]['Value'] = word[y + 1]['Value']
                context[z]['Candidates'] = candidates[x + 1]['Value']
                context[z]['Word'] = str(y + 1)
                context[z]['Confidence'] = word[y + 1]['Confidence']
                context[z]['Left'] = word[y + 1]['Left']
                context[z]['Top'] = word[y + 1]['Top']
                context[z]['Right'] = word[y + 1]['Right']
                context[z]['Bottom'] = word[y + 1]['Bottom']

                if z == 1:
                    context[z]['Line'] = line
                elif context[z - 1]['Bottom'] == word[y + 1]['Bottom']:
                    context[z]['Line'] = line
                else:
                    line = line + 1
                    context[z]['Line'] = line

                if int(word[y + 1]['Bottom']) > int(candidates[x + 1]['Bottom']) - 15 and \
                        int(word[y + 1]['Bottom']) < int(candidates[x + 1]['Bottom']) + 15:
                    context[z]['SameLine'] = "1"
                else:
                    context[z]['SameLine'] = "0"

                z = z + 1


def define_groupcontext(self, context):
    # Looping thru the context and grouping the context based on proximity and word sequence
    #  Storing all grouped context is stored in the group context dictionary with the following data:
    # value, confidence, word, weight, positioning(left, top, right and bottom), and same line as candidate

    z = 1
    for x in range(len(context)):

        if x == 0:
            groupcontext[z] = {}
            groupcontext[z]['Value'] = context[x + 1]['Value']
            groupcontext[z]['Word'] = context[x + 1]['Word']
            groupcontext[z]['Candidates'] = context[x + 1]['Candidates']
            groupcontext[z]['Weight'] = '0'
            groupcontext[z]['Confidence'] = context[x + 1]['Confidence']
            groupcontext[z]['Left'] = context[x + 1]['Left']
            groupcontext[z]['Top'] = context[x + 1]['Top']
            groupcontext[z]['Right'] = context[x + 1]['Right']
            groupcontext[z]['Bottom'] = context[x + 1]['Bottom']
            groupcontext[z]['SameLine'] = context[x + 1]['SameLine']

        elif int(groupcontext[z]['Word']) + 1 == int(context[x + 1]['Word']):

            groupcontext[z]['Value'] = groupcontext[z]['Value'] + ' ' + context[x + 1]['Value']
            groupcontext[z]['Word'] = context[x + 1]['Word']
            groupcontext[z]['Confidence'] = context[x + 1]['Confidence']
            groupcontext[z]['Top'] = context[x + 1]['Top']
            groupcontext[z]['Right'] = context[x + 1]['Right']
            groupcontext[z]['Bottom'] = context[x + 1]['Bottom']

        else:
            z = z + 1
            groupcontext[z] = {}
            groupcontext[z]['Value'] = context[x + 1]['Value']
            groupcontext[z]['Word'] = context[x + 1]['Word']
            groupcontext[z]['Candidates'] = context[x + 1]['Candidates']
            groupcontext[z]['Weight'] = 0
            groupcontext[z]['Confidence'] = context[x + 1]['Confidence']
            groupcontext[z]['Left'] = context[x + 1]['Left']
            groupcontext[z]['Top'] = context[x + 1]['Top']
            groupcontext[z]['Right'] = context[x + 1]['Right']
            groupcontext[z]['Bottom'] = context[x + 1]['Bottom']
            groupcontext[z]['SameLine'] = context[x + 1]['SameLine']


def weightcontext(self, KW_ATT):
    # Match Context and Weighting

    for z, value in KW_ATT.items():

        for x in range(len(groupcontext)):

            if int(groupcontext[x + 1]['Weight']) < fuzz.WRatio(groupcontext[x + 1]['Value'], z):
                groupcontext[x + 1]['Weight'] = float(fuzz.WRatio(groupcontext[x + 1]['Value'], z)) * float(
                    value[0]) / 100

                if groupcontext[x + 1]['SameLine'] == '1':
                    groupcontext[x + 1]['Weight'] = groupcontext[x + 1]['Weight'] + float(value[5])


def outputresults(self, groupcontext, fp):
    # Output Results
    for x in range(len(groupcontext)):

        if groupcontext[x + 1]['Candidates'] in results:

            if int(results[groupcontext[x + 1]['Candidates']]) < int(groupcontext[x + 1]['Weight']):
                results[groupcontext[x + 1]['Candidates']] = groupcontext[x + 1]['Weight']

        else:
            results[groupcontext[x + 1]['Candidates']] = groupcontext[x + 1]['Weight']

    if (len(results.keys()) == 0):

        f = open(fp + '.txt', 'w')
        f.write("Could not find any valid candidates")
        f.close()

    else:
        sorted_by_value = sorted(results.items(), key=lambda kv: kv[1], reverse=True)
        f = open(fp + '.txt', 'w')
        f.write("WINNING CANDIDATE (CANDIDATE , WEIGHT): " + str(sorted_by_value[0]) + "\n")
        f.write("ALL CANDIDATES: \n")

        for x in sorted_by_value[:]:
            print(x)
            f.write(str(x) + "\n")

        f.close()


def processimage(path):
    # TODO : Implement using opencv
    temp_fn = set_dpi(path)
    new_image = remove_noise(temp_fn)
    return new_image


def set_dpi(path):
    image = IMG.open(path)
    len_x, wid_y = image.size
    factor = max(1, int(1800 / len_x))
    size = factor * len_x, factor * wid_y
    # size = (1800, 1800)
    image_resized = image.resize(size, IMG.ANTIALIAS)
    temp_f = tempfile.NamedTemporaryFile(delete=False, suffix='.jpg')
    temp_fn = temp_f.name
    image_resized.save(temp_fn, dpi=(300, 300))
    return temp_fn


def smooth(image):
    ret1, th1 = cv2.threshold(image, BINARY_THREHOLD, 255, cv2.THRESH_BINARY)
    ret2, th2 = cv2.threshold(th1, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    blur = cv2.GaussianBlur(th2, (1, 1), 0)
    ret3, th3 = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return th3


def remove_noise(name):
    image = cv2.imread(name, 0)
    filtered = cv2.adaptiveThreshold(image.astype(np.uint8), 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 41, 3)
    core = np.ones((1, 1), np.uint8)
    opening = cv2.morphologyEx(filtered, cv2.MORPH_OPEN, core)
    closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, core)
    image = smooth(image)
    original_image = cv2.bitwise_or(image, closing)
    return original_image


if __name__ == '__main__':
    vp_start_gui()
