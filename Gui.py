import tkinter as tk
from tkinter import *
from tkinter import ttk
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import matplotlib.pyplot as plt
import os
from Roller import *
import re

class MyApp(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.config(width=1430, height=800)
        self.master.title("Dice Probability calculator")
        self.FirstDiceFlage = 1
        Dirname = os.path.dirname(__file__)
        self.CloseIcon = PhotoImage(file = os.path.join(Dirname, 'Close.png'))
        self.main()

    ######################################################################
    # Function: __BuildDiceTupleList
    #
    # Description:
    #    Build Dice TupleList.
    #
    # Parameters:
    #    Query      - the request query.
    #    HttpMethod - Http method, POST or GET.
    #
    # Return: 
    #    DiceTupleList - Dice Tuple List.
    ######################################################################
    def __BuildDiceTupleList(self):
        DiceTupleList = []
        LeftSideFrame = self.master.nametowidget("left_side_frame")
        DicesFrame = LeftSideFrame.nametowidget('dices_frame')
        DicesCanvas = DicesFrame.nametowidget('dices_canvas')
        InnerDicesFrame = DicesCanvas.nametowidget('inner_dices_frame')
        InnerDicesFrameChildren = InnerDicesFrame.winfo_children()
    
        for i in range(2, len(InnerDicesFrameChildren)):
            NumDice = InnerDicesFrameChildren[i].nametowidget("num_dice").get()

            # Check if numdice is not empy and is numeric and the number is bigger then 0
            if len(NumDice) > 0:
                if NumDice.isnumeric():
                    if int(NumDice) > 0:
                        DicePattern = re.compile("^[0-9]+(,[0-9]+)*$")
                        RegularDice = re.compile("^(d|D)([0-9]+)$")
                        Dice = InnerDicesFrameChildren[i].nametowidget("dice").get()
                        Dice = Dice.replace(" ", "")
                        if DicePattern.match(Dice):
                            DiceType = Dice.split(',')
        
                            # Convert the text to list of integers
                            IntDiceType = [int(x) for x in DiceType]
                            DiceTupleList.append((int(NumDice), IntDiceType))
                            InnerDicesFrameChildren[i].nametowidget("error_labe")["text"] = ""
                        elif RegularDice.match(Dice):
                            DiceTupleList.append((int(NumDice), Dice))
                            InnerDicesFrameChildren[i].nametowidget("error_labe")["text"] = ""
                        else:
                            InnerDicesFrameChildren[i].nametowidget("error_labe")["text"] = "incorrect format"
                    else:
                        InnerDicesFrameChildren[i].nametowidget("error_labe")["text"] = "num dice must be positive"
                else:
                    InnerDicesFrameChildren[i].nametowidget("error_labe")["text"] = "num dice must be int"
    
        return DiceTupleList

    ######################################################################
    # Function: __AddPercentage
    #
    # Description:
    #    Add Percentage to graph bars.
    #
    # Parameters:
    #    ax - the figure axes.
    ######################################################################
    def __AddPercentage(self, ax):
        TestSize = 100
        for p in ax.patches:
            percentage = '{:.2f}%'.format(100 * p.get_height()/TestSize)
            x = p.get_x() + p.get_width() - 0.4
            y = p.get_height()
            ax.annotate(percentage, (x, y), ha='center')

    ######################################################################
    # Function: __ClearFrame
    #
    # Description:
    #    Clear Frame from all children object.
    #
    # Parameters:
    #    frame - the frame.
    ######################################################################
    def __ClearFrame(self, frame):
        for widget in frame.winfo_children():
            widget.destroy()

    ######################################################################
    # Function: __ClearFrame
    #
    # Description:
    #    Clear all Frame from all children object.
    #
    # Parameters:
    #    frame - the frame list.
    ######################################################################
    def __ClearFrames(self, frames):
        for frame in frames:
            self.__ClearFrame(frame)
        self 

    ######################################################################
    # Function: __DeleteFrame
    #
    # Description:
    #    Delete the frame itsalfe and update the scroll bar.
    #
    # Parameters:
    #    frame  - the frame.
    #    canvas - the canvas To update the scroll bar.
    ######################################################################
    def __DeleteFrame(self, frame, canvas):
        self.__ClearFrame(frame)
        frame.destroy()
        
        # Update the Scrollbar
        canvas.configure(scrollregion=canvas.bbox("all"))

    ######################################################################
    # Function: __BuildGraphSide
    #
    # Description:
    #    Build the graph side.
    ######################################################################
    def __BuildGraphSide(self):
        # Add Main Gruph Frame
        MainGraphFrame = LabelFrame(self.master, height=800, width=1040, name="main_graph_frame")
        MainGraphFrame.grid(row=0, column=1, sticky="nsew")

        # Add canvas
        canvas = Canvas(self.master, name="graph_canvas")
        canvas.grid(row=0, column=1, sticky="nsew")
        #self.grid_columnconfigure(1, weight=7)

        # Add Scroll bar
        my_Scrollbar = ttk.Scrollbar(canvas, orient=VERTICAL, command=canvas.yview )
        my_Scrollbar.pack(side = RIGHT, fill = Y)

        # Binde Scrollbar function to Canvas
        canvas.configure(yscrollcommand=my_Scrollbar.set)
        canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        # Add Left and Right Graph Frames to Canvas
        LeftGraphFrame = Frame(canvas, name="left_graph_frame")
        RightGraphFrame = Frame(canvas, name="right_graph_frame")
        canvas.create_window((0, 0), window=LeftGraphFrame, anchor="nw")
        canvas.create_window((1020, 0), window=RightGraphFrame, anchor="ne")

    ######################################################################
    # Function: __BuildGraph
    #
    # Description:
    #    Build the graph.
    ######################################################################
    def __BuildGraph(self):
        GraphCanvas = self.master.nametowidget("graph_canvas")
        # Chose Between left and right frame
        LeftGraphFrame = GraphCanvas.nametowidget("left_graph_frame")
        RightGraphFrame =  GraphCanvas.nametowidget("right_graph_frame")
        SizeL = len(LeftGraphFrame.winfo_children())
        SizeR = len(RightGraphFrame.winfo_children())
        if SizeL > SizeR:
            MainFrame = RightGraphFrame
        else:
            MainFrame =  LeftGraphFrame

        # Add inner frame to the Main Frame
        frameIn = Frame(MainFrame, padx=5, pady = 5)
        frameIn.pack()

        # Add Close button to specific graph
        CloseButton = Button(frameIn, image = self.CloseIcon, command=lambda:self.__DeleteFrame(frameIn, GraphCanvas))
        CloseButton.pack(side=TOP, anchor=NE)

        # Get Dice Tuple List
        DiceTupleList = self.__BuildDiceTupleList()
        if len(DiceTupleList):

            # Get Requested funcation
            Function = self.v.get()
            
            # Get Graph data
            rol = Roller()
            rols = rol.GetRols(DiceTupleList, Function)

            # Build Graph
            fig = plt.figure(constrained_layout=False)
            fig.set_size_inches(5, 3)
            a = fig.add_subplot()
            a.axes.bar(list(rols.keys()), list(rols.values()), edgecolor='black', )
            self.__AddPercentage(a.axes)
            canvas = FigureCanvasTkAgg(fig, frameIn)
            canvas.draw()
            canvas.get_tk_widget()
            toolbar = NavigationToolbar2Tk(canvas, frameIn)
            toolbar.update()
            canvas.get_tk_widget().pack(side=TOP)

            # Update the Scrollbar
            GraphCanvas.configure(scrollregion=GraphCanvas.bbox("all"))

    ######################################################################
    # Function: __BuildLeftSide
    #
    # Description:
    #    Build the left side.
    ######################################################################
    def __BuildLeftSide(self):
        # Add Left Frame
        LeftFrame = Frame(self.master, height=800, name="left_side_frame")
        LeftFrame.grid(row=0, column=0, rowspan=5, sticky="nsew")

        # Add Build Graph Button
        BuildGraphButton = Button(LeftFrame, text="Build Graph!", command=lambda:self.__BuildGraph())
        BuildGraphButton.grid(row=0, column=0, sticky="w")

        # Add Clear Frame Button
        canvas = self.master.nametowidget("graph_canvas")
        LeftGraphFrame = canvas.nametowidget("left_graph_frame")
        RightGraphFrame = canvas.nametowidget("right_graph_frame")
        ClearFrameBt = Button(LeftFrame, text="Clear Frame", command=lambda:self.__ClearFrames([LeftGraphFrame, RightGraphFrame]))
        ClearFrameBt.grid(row=0, column=1, sticky="e")

        self.__BuildDicesFrame(LeftFrame)

        # Add Radio buttons
        self.v = StringVar(value="Max")
        Radiobutton1 = Radiobutton(LeftFrame, text = "Max", variable = self.v, value = "Max", name="radio_button1")
        Radiobutton1.grid(row=6, column=0, sticky="w")
        Radiobutton2 = Radiobutton(LeftFrame, text = "Sum", variable = self.v, value = "Sum")
        Radiobutton2.grid(row=6, column=1, sticky="w")
        Radiobutton3 = Radiobutton(LeftFrame, text = "Min", variable = self.v, value = "Min")
        Radiobutton3.grid(row=6, column=2, sticky="w")
        
        lable = Label(LeftFrame, text="")
        lable.grid(row=7 ,column=0, sticky="w")
        lable = Label(LeftFrame, text="Regular dice Format:")
        lable.grid(row=8 ,column=0, sticky="w", columnspan=2)
        lable1 = Label(LeftFrame, text="d2, d3, d4 ...")
        lable1.grid(row=9 ,column=0, sticky="w", columnspan=3)
        lable2 = Label(LeftFrame, text="Custom dice format:")
        lable2.grid(row=10 ,column=0, sticky="w", columnspan=3)
        lable2 = Label(LeftFrame, text="1,2,3,4,6,6")
        lable2.grid(row=11 ,column=0, sticky="w", columnspan=3)

    ######################################################################
    # Function: __BuildDicesFrame
    #
    # Description:
    #    Build the dices frame.
    #
    # Parameters:
    #    frame  - the frame.
    ######################################################################
    def __BuildDicesFrame(self, frame):
        lable = Label(frame, text="")
        lable.grid(row=1 ,column=0, sticky="w")
        
        # Add "Add Dice Button"
        AddDiceButton = Button(frame, text="Add Dice", command=lambda:self.__AddDice(DicesCanvas))
        AddDiceButton.grid(row=2, column=0, sticky="W")

        # Add Dices Frame
        DicesFrame = LabelFrame(frame, text="Dices", name="dices_frame")
        DicesFrame.grid(row=3, column=0, columnspan=6, rowspan=2)

        # Add Dices Canvas
        DicesCanvas = Canvas(DicesFrame, name="dices_canvas")
        DicesCanvas.grid()

        # Add Scrollbar
        my_Scrollbar = ttk.Scrollbar(DicesFrame, orient=VERTICAL, command=DicesCanvas.yview)
        my_Scrollbar.grid(row=0, sticky="nse")

        # Binde Scrollbar function to Canvas
        DicesCanvas.configure(yscrollcommand=my_Scrollbar.set)
        DicesCanvas.bind('<Configure>', lambda e: DicesCanvas.configure(scrollregion=DicesCanvas.bbox("all")))

        # Add Inner Dices Frame
        InnerDicesFrame = Frame(DicesCanvas, name="inner_dices_frame")
        DicesCanvas.create_window((0, 0), window=InnerDicesFrame, anchor="nw")

        # Add Hedars to Inner Dices Frame
        self.entry = Entry(InnerDicesFrame, width=27, bg='LightSteelBlue',fg='Black', font=('Arial', 10, 'bold'))
        self.entry.grid(row=0,column=0)
        self.entry.insert(END, "Dice type")
        self.entry = Entry(InnerDicesFrame, width=15, bg='LightSteelBlue',fg='Black', font=('Arial', 10, 'bold'))
        self.entry.grid(row=0,column=1)
        self.entry.insert(END, "Number of dices")

        ## Add lables to Inner Dices Frame
        #lable1 = Label(InnerDicesFrame, text="Dice type")
        #lable1.grid(column=0, row=0, sticky="n")
        #lable2 = Label(InnerDicesFrame, text="Number of dices")
        #lable2.grid(column=1, row=0)

        self.__AddDice(DicesCanvas)

    ######################################################################
    # Function: __AddDice
    #
    # Description:
    #    Add the Dice to the canvas.
    #
    # Parameters:
    #    canvas - the canvas.
    ######################################################################
    def __AddDice(self, canvas):
        InnerDicesFrame = canvas.nametowidget("inner_dices_frame")

        # Add Dice Frame
        DiceFrame = Frame(InnerDicesFrame)
        DiceFrame.grid(column=0, columnspan=2, sticky="w")
        
        # Add elemant to dice side
        Dice = Entry(DiceFrame, width=30, name="dice")
        Dice.grid(column=0, row=0, padx=(0, 10))
        NumDice = Entry(DiceFrame, width=5, name="num_dice")
        NumDice.grid(column=1, row=0)

        # Add First Dice with no option to delete 
        if self.FirstDiceFlage:
            self.FirstDiceFlage = 0
            # Default dice
            Dice.insert(0, "d6")
            NumDice.insert(0, "1")
        else:
            myButton = Button(DiceFrame, image = self.CloseIcon, command=lambda:self.__DeleteFrame(DiceFrame, canvas))
            myButton.grid(column=2, row=0, padx=(0, 10))
            
        lable = Label(DiceFrame, text="", name="error_labe", fg="red")
        lable.grid(column=3, row=0)

        # Update the Scrollbar
        canvas.configure(scrollregion=canvas.bbox("all"))

    def main(self):
        self.__BuildGraphSide()
        self.__BuildLeftSide()

if __name__ == '__main__':
    MyApp().mainloop()



