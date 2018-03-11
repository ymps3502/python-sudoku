#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os.path
from random import shuffle
from random import randint
from Tkinter import *
import tkMessageBox
# import time


class solver():
    """docstring for solver"""

    def __init__(self, board):
        if type(board) is not list:
            self.board = list(board)
        else:
            self.board = board
        self.startTime = None
        # self.solve()

    def solve(self, index=None, number=None):
        # if self.startTime is None:
        #     self.startTime = time.clock()
        # takeTime = time.clock() - self.startTime
        # if takeTime > 1000:  # time out
        #     print "Time out!"
        #     self.startTime = None
        #     return False
        i = self.getEmptyGrid()
        if i is None:
            return True
        for num in range(1, 10):
            if i == index and str(num) == number:
                continue
            if self.checkNum(i, num):
                self.board[i] = str(num)
                if self.solve():
                    return True
                self.board[i] = '0'
        return False

    def getEmptyGrid(self):
        for i in range(81):
            if self.board[i] == '0':
                return i
        return None

    def checkNum(self, index, possibleNum):
        row = index / 9
        col = index % 9
        for i in range(9):
            if str(possibleNum) in {
                self.board[row * 9 + i],
                self.board[i * 9 + col],
                self.board[
                    (row - row % 3 + i / 3) * 9 + (col - col % 3 + i % 3)]
            }:
                return False
        return True


class generator():
    """docstring for generator"""

    def __init__(self):
        self.board = list('0' * 81)
        self.index = [i for i in range(81)]
        shuffle(self.index)
        self.indexCount = 0

    def generatePuzzle(self):
        while True:
            clue = 81
            shuffle(self.index)
            for i in self.index:
                # a valid sudoku puzzle must have at least 17 non-empty grids
                if clue <= 17:
                    break
                tempNum = self.board[i]
                self.board[i] = '0'
                copyBoard = list(self.board)
                sol = solver(copyBoard)
                if not sol.solve(i, tempNum):
                    # this is the only one answer puzzle
                    clue -= 1
                else:
                    self.board[i] = tempNum
            if clue <= 51:
                break

    def generateSolvedPuzzle(self):
        index = self.getIndex()
        if index is None:
            return True
        possibleNum = [num for num in range(1, 10)]
        for i in range(1, 10):
            if not self.checkNum(index, i):
                possibleNum.remove(i)
        if len(possibleNum) == 0:
            return False
        shuffle(possibleNum)
        for num in possibleNum:
            self.board[index] = str(num)
            copyBoard = list(self.board)
            sol = solver(copyBoard)
            # print "Try solving board: ",
            # print ''.join(num for num in self.board)
            if self.indexCount < 17 or sol.solve():
                # print "Generating board with number: {0}, in index: {1}" \
                # " ({2} / 81)".format(num, index, self.indexCount)
                if self.generateSolvedPuzzle():
                    return True
        # can't solved
        self.board[index] = '0'
        self.indexCount -= 1
        return False

    def getIndex(self):
        if self.indexCount > 80:
            return None
        else:
            self.indexCount += 1
            return self.index[self.indexCount - 1]

    def checkNum(self, index, possibleNum):
        row = index / 9
        col = index % 9
        for i in range(9):
            if str(possibleNum) in {
                self.board[row * 9 + i],
                self.board[i * 9 + col],
                self.board[
                    (row - row % 3 + i / 3) * 9 + (col - col % 3 + i % 3)]
            }:
                return False
        return True

    def printBoard(self):
        for i, num in enumerate(self.board):
            if i % 9 == 8:
                print num
            else:
                print num + " ",
        print


class sudokuHelper(object):
    """docstring for sudokuHelper"""

    def __init__(self):
        self.index = None
        self.puzzle = None
        self.level = None
        self.answer = None
        self.file_puzzle = "puzzle.txt"
        self.file_answer = "answer.txt"
        self.file_record = "record.txt"
        self.file_save = "save.txt"

    def getPuzzle(self, level):
        puzzleList = list()
        with open(self.file_puzzle, 'r') as file:
            for i, line in enumerate(file):
                puzzleData = line.strip().split(",")
                if puzzleData[2] == level:
                    puzzleData.append(i)
                    puzzleList.append(puzzleData)
        data = puzzleList[randint(0, len(puzzleList) - 1)]
        self.index = data[3]
        self.puzzle = data[0]
        self.level = data[2]
        with open(self.file_answer, 'r') as file:
            for i, line in enumerate(file):
                if i == self.index:
                    self.answer = line.strip()

    def getRecord(self):
        '''answer, time'''
        record = None
        if not os.path.isfile(self.file_record):
            return record
        with open(self.file_record, 'r') as file:
            for line in file:
                data = line.strip().split(',')
                if self.answer == data[0]:
                    record = data[1]
        return record

    def savaRecord(self, time):
        with open(self.file_record, 'a') as file:
            line = self.index + "," + time + "\n"
            file.write(line)

    def savePuzzle(self, current_puzzle, time, note):
        line = ""
        with open(self.file_save, 'w') as file:
            line += str(self.index) + ","
            line += self.puzzle + ","
            line += self.level + ","
            line += self.answer + ","
            line += current_puzzle + ","
            line += time + ","
            line += note + "\n"
            file.write(line)

    def loadPuzzle(self):
        data = None
        if not os.path.isfile(self.file_save):
            return data
        with open(self.file_save, 'r') as file:
            for line in file:
                data = line.strip().split(",")
                self.index = data[0]
                self.puzzle = data[1]
                self.level = data[2]
                self.answer = data[3]
                data = data[4:]
        return data


class App():
    """docstring for sudokuForm"""

    def __init__(self, master):
        self.master = master
        # widget width, height, and font size
        self.candidate_grid_width = 18
        self.candidate_grid_height = self.candidate_grid_width
        self.grid_width = self.candidate_grid_width * 3
        self.grid_height = self.grid_width
        self.line_width = 1
        self.line_bold_width = self.line_width * 3
        self.puzzleframe_width = self.line_bold_width * \
            4 + self.line_width * 6 + self.grid_width * 9
        self.puzzleframe_height = self.puzzleframe_width
        self.numberframe_width = self.puzzleframe_width
        self.numberframe_height = self.grid_height
        self.numberButton_width = float(self.numberframe_width) / 13
        self.numberButton_height = self.numberframe_height
        self.padding = 5
        self.statusframe_width = 80
        self.statusframe_height = self.puzzleframe_height + \
            self.numberframe_height + self.padding * 2
        self.WINDOW_WIDTH = self.puzzleframe_width + \
            self.statusframe_width + self.padding * 4
        self.WINDOW_HEIGHT = self.statusframe_height + self.padding * 2 + 20
        self.gridFontSize = 25
        self.candidateGridFontSize = 8
        # end of widget width, height, and font size
        # initial setting
        self.level = "Gentle/Very"
        self.helper = sudokuHelper()
        self.gridList = list()
        self.rectList = list()
        self.candidateGridList = list()
        self.previousClick = None
        self.note = False
        self.pause = False
        self.storeCandidateGrid = list()
        self.sec = 0
        self.timer = None
        # bind keyboard
        master.bind("<Key>", self.numberKey)
        master.bind("<Left>", self.arrowKey)
        master.bind("<Up>", self.arrowKey)
        master.bind("<Right>", self.arrowKey)
        master.bind("<Down>", self.arrowKey)
        master.bind("<BackSpace>", self.deleteKey)
        master.bind("<Delete>", self.deleteKey)
        master.bind("<n>", self.noteKey)
        master.bind("<N>", self.noteKey)
        master.bind("<space>", self.pauseKey)
        master.bind("<Escape>", self.exitKey)
        # icon
        master.iconbitmap('Icon.ico')
        # title
        master.title("Sudoku")
        # window size and set to center
        x = master.winfo_screenwidth() / 2 - self.WINDOW_WIDTH / 2
        y = master.winfo_screenheight() / 2 - self.WINDOW_HEIGHT / 2
        master.geometry(
            '{}x{}+{}+{}'.format(self.WINDOW_WIDTH, self.WINDOW_HEIGHT, x, y))
        # menu
        menubar = Menu(master)
        self.filemenu = Menu(menubar, tearoff=0)
        self.filemenu.add_command(label="開新遊戲", command=self.newGame)
        self.filemenu.add_command(label="上次遊戲", command=self.loadGame)
        self.filemenu.add_command(label="儲存遊戲", command=self.saveGame)
        self.filemenu.add_separator()
        self.filemenu.add_command(label="離開", command=master.quit)
        menubar.add_cascade(label="檔案", menu=self.filemenu)
        if self.helper.loadPuzzle() is None:
            self.filemenu.entryconfig(1, state="disable")
        self.filemenu.entryconfig(2, state="disable")

        levelmenu = Menu(menubar, tearoff=0)
        self.varLevel = StringVar()
        levelmenu.add_radiobutton(
            variable=self.varLevel, value="1",
            label="初學", command=lambda: self.changeLevel(1))
        levelmenu.add_radiobutton(
            variable=self.varLevel, value="2",
            label="簡單", command=lambda: self.changeLevel(2))
        levelmenu.add_radiobutton(
            variable=self.varLevel, value="3",
            label="進階", command=lambda: self.changeLevel(3))
        levelmenu.add_radiobutton(
            variable=self.varLevel, value="4",
            label="中等", command=lambda: self.changeLevel(4))
        levelmenu.add_radiobutton(
            variable=self.varLevel, value="5",
            label="困難", command=lambda: self.changeLevel(5))
        levelmenu.add_radiobutton(
            variable=self.varLevel, value="6",
            label="艱深", command=lambda: self.changeLevel(6))
        levelmenu.add_radiobutton(
            variable=self.varLevel, value="7",
            label="登峰造極", command=lambda: self.changeLevel(7))
        menubar.add_cascade(label="難度", menu=levelmenu)
        self.varLevel.set(1)

        menubar.add_cascade(label="幫助", command=self.helpDialog)
        menubar.add_cascade(label="關於", command=self.aboutDialog)

        master.config(menu=menubar)
        # end of menu

        # puzzle frame
        puzzleframe = Frame(width=self.puzzleframe_width,
                            height=self.puzzleframe_height)
        self.canvas = Canvas(puzzleframe, bg='white',
                             width=self.puzzleframe_width,
                             height=self.puzzleframe_height)
        self.drawLine()
        self.generateGrid()
        self.canvas.create_text(
            self.puzzleframe_width / 2, self.puzzleframe_height / 2,
            text="暫停",
            font=("Purisa", self.gridFontSize * 2),
            state="hidden",
            tag="pauseText")
        self.canvas.pack()
        # end of puzzle frame

        # number frame
        numberframe = Frame(width=self.numberframe_width,
                            height=self.numberframe_height, bg='white')
        numberframe1 = Frame(
            numberframe,
            width=self.numberButton_width, height=self.numberButton_height)
        numberframe2 = Frame(
            numberframe,
            width=self.numberButton_width, height=self.numberButton_height)
        numberframe3 = Frame(
            numberframe,
            width=self.numberButton_width, height=self.numberButton_height)
        numberframe4 = Frame(
            numberframe,
            width=self.numberButton_width, height=self.numberButton_height)
        numberframe5 = Frame(
            numberframe,
            width=self.numberButton_width, height=self.numberButton_height)
        numberframe6 = Frame(
            numberframe,
            width=self.numberButton_width, height=self.numberButton_height)
        numberframe7 = Frame(
            numberframe,
            width=self.numberButton_width, height=self.numberButton_height)
        numberframe8 = Frame(
            numberframe,
            width=self.numberButton_width, height=self.numberButton_height)
        numberframe9 = Frame(
            numberframe,
            width=self.numberButton_width, height=self.numberButton_height)
        deleteframe = Frame(
            numberframe,
            width=self.numberButton_width * 2, height=self.numberButton_height)
        noteframe = Frame(
            numberframe,
            width=self.numberButton_width * 2, height=self.numberButton_height)
        numberButton1 = Button(numberframe1, text="1",
                               command=lambda: self.numberButtonOnClick(1))
        numberButton2 = Button(numberframe2, text="2",
                               command=lambda: self.numberButtonOnClick(2))
        numberButton3 = Button(numberframe3, text="3",
                               command=lambda: self.numberButtonOnClick(3))
        numberButton4 = Button(numberframe4, text="4",
                               command=lambda: self.numberButtonOnClick(4))
        numberButton5 = Button(numberframe5, text="5",
                               command=lambda: self.numberButtonOnClick(5))
        numberButton6 = Button(numberframe6, text="6",
                               command=lambda: self.numberButtonOnClick(6))
        numberButton7 = Button(numberframe7, text="7",
                               command=lambda: self.numberButtonOnClick(7))
        numberButton8 = Button(numberframe8, text="8",
                               command=lambda: self.numberButtonOnClick(8))
        numberButton9 = Button(numberframe9, text="9",
                               command=lambda: self.numberButtonOnClick(9))
        deleteButton = Button(deleteframe, text="刪除",
                              command=self.deleteButtonOnClick)
        self.noteButton = Checkbutton(
            noteframe, text="筆記", indicatoron=False,
            command=self.noteButtonOnClick)
        numberframe1.pack_propagate(0)
        numberframe2.pack_propagate(0)
        numberframe3.pack_propagate(0)
        numberframe4.pack_propagate(0)
        numberframe5.pack_propagate(0)
        numberframe6.pack_propagate(0)
        numberframe7.pack_propagate(0)
        numberframe8.pack_propagate(0)
        numberframe9.pack_propagate(0)
        deleteframe.pack_propagate(0)
        noteframe.pack_propagate(0)
        numberframe1.pack(side=LEFT)
        numberframe2.pack(side=LEFT)
        numberframe3.pack(side=LEFT)
        numberframe4.pack(side=LEFT)
        numberframe5.pack(side=LEFT)
        numberframe6.pack(side=LEFT)
        numberframe7.pack(side=LEFT)
        numberframe8.pack(side=LEFT)
        numberframe9.pack(side=LEFT)
        deleteframe.pack(side=LEFT)
        noteframe.pack(side=LEFT)
        numberButton1.pack(fill=X, expand=1)
        numberButton2.pack(fill=X, expand=1)
        numberButton3.pack(fill=X, expand=1)
        numberButton4.pack(fill=X, expand=1)
        numberButton5.pack(fill=X, expand=1)
        numberButton6.pack(fill=X, expand=1)
        numberButton7.pack(fill=X, expand=1)
        numberButton8.pack(fill=X, expand=1)
        numberButton9.pack(fill=X, expand=1)
        deleteButton.pack(fill=X, expand=1)
        self.noteButton.pack(fill=X, expand=1)
        # end of number frame

        # status frame
        statusframe = Frame(
            width=self.statusframe_width, height=self.statusframe_height)
        BestRecordLabel = Label(statusframe, text="最佳紀錄")
        self.recordLabel = Label(statusframe, text="")
        gameTimeLabel = Label(statusframe, text="遊戲時間")
        self.timeLabel = Label(statusframe, text="00:00:00")
        gameLevelLabel = Label(statusframe, text="難度")
        self.levelLabel = Label(statusframe, text="")
        buttonFrame = Frame(
            statusframe,
            width=self.statusframe_width, height=self.numberButton_height)
        pauseFrame = Frame(
            buttonFrame,
            width=self.statusframe_width, height=self.numberButton_height)
        hintFrame = Frame(
            buttonFrame,
            width=self.statusframe_width, height=self.numberButton_height)
        answerFrame = Frame(
            buttonFrame,
            width=self.statusframe_width, height=self.numberButton_height)
        BestRecordLabel.grid(row=0, column=0, sticky=W)
        self.recordLabel.grid(row=1, column=0)
        gameTimeLabel.grid(row=2, column=0, sticky=W)
        self.timeLabel.grid(row=3, column=0)
        gameLevelLabel.grid(row=4, column=0, sticky=W)
        self.levelLabel.grid(row=5, column=0)
        pauseFrame.pack_propagate(0)
        hintFrame.pack_propagate(0)
        answerFrame.pack_propagate(0)
        pauseFrame.pack()
        hintFrame.pack()
        answerFrame.pack()
        buttonFrame.grid(row=6, column=0, sticky="S")
        self.pauseButton = Button(
            pauseFrame, text="暫停", command=self.pauseButtonOnClick)
        hintButton = Button(
            hintFrame, text="提示", command=self.hintButtonOnClick)
        answerButton = Button(
            answerFrame, text="解答", command=self.answerButtonOnClick)
        self.pauseButton.pack(fill=X, expand=1)
        hintButton.pack(fill=X, expand=1)
        answerButton.pack(fill=X, expand=1)
        statusframe.grid_rowconfigure(6, weight=1)
        statusframe.grid_propagate(False)
        # end of status frame

        # main frame
        puzzleframe.grid(row=0, column=0, padx=self.padding, pady=self.padding)
        numberframe.grid(row=1, column=0, pady=self.padding)
        statusframe.grid(row=0, column=1, rowspan=2,
                         padx=self.padding, pady=self.padding)

    def drawLine(self):
        x = 0
        y = 0
        h = self.puzzleframe_height
        w = self.puzzleframe_width
        for i in range(10):
            if i % 3 == 0:
                x += self.line_bold_width
                self.canvas.create_line(
                    x, y, x, h,
                    width=self.line_bold_width)
            else:
                x += self.line_width
                self.canvas.create_line(x, y, x, h)
            x += self.grid_width
        x = 0
        for i in range(10):
            if i % 3 == 0:
                y += self.line_bold_width
                self.canvas.create_line(
                    x, y, w, y,
                    width=self.line_bold_width)
            else:
                y += self.line_width
                self.canvas.create_line(x, y, w, y)
            y += self.grid_width

    def generateGrid(self):
        for i in range(81):
            row = i / 9
            col = i % 9
            x = (self.grid_width + self.line_width) * col + \
                self.grid_width / 2 + self.line_bold_width * \
                (col / 3 + 1) - self.line_width * (col / 3)
            y = (self.grid_height + self.line_width) * row + \
                self.grid_height / 2 + self.line_bold_width * \
                (row / 3 + 1) - self.line_width * (row / 3)
            grid = self.canvas.create_text(x, y, font=(
                "Purisa", self.gridFontSize), text="", tag="grid" + str(i))
            self.canvas.tag_bind(grid, '<ButtonPress-1>', self.gridOnClick)
            self.gridList.append(grid)
            if col == 0:
                rx1 = x - self.grid_width / 2 + 2
            else:
                rx1 = x - self.grid_width / 2 + 1
            if row == 0:
                ry1 = y - self.grid_height / 2 + 2
            else:
                ry1 = y - self.grid_height / 2 + 1
            if col % 3 == 2:
                rx2 = x + self.grid_width / 2 + 1
            else:
                rx2 = x + self.grid_width / 2
            if row % 3 == 2:
                ry2 = y + self.grid_height / 2 + 1
            else:
                ry2 = y + self.grid_height / 2
            rect = self.canvas.create_rectangle(
                rx1, ry1, rx2, ry2,
                outline="white", fill="white", tag="rect" + str(i))
            self.canvas.tag_bind(rect, '<ButtonPress-1>', self.gridOnClick)
            self.rectList.append(rect)

    def generateCandidateGrid(self, id):
        xOffset = self.canvas.coords(id)[0] - self.candidate_grid_width
        yOffset = self.canvas.coords(id)[1] - self.candidate_grid_height
        name = self.canvas.gettags(id)[0]
        for i in range(9):
            row = i / 3
            col = i % 3
            x = xOffset + self.candidate_grid_width * col
            y = yOffset + self.candidate_grid_height * row
            tag = name + "_" + str(i + 1)
            grid = self.canvas.create_text(
                x, y,
                font=("Purisa", self.candidateGridFontSize),
                text=str(i + 1),
                tag=tag,
                state="hidden")
            self.canvas.tag_bind(
                tag, '<ButtonPress-1>', self.candidateGridOnClick)
            self.candidateGridList.append(grid)

    def setRecordLabel(self):
        r = self.helper.getRecord()
        if r is not None:
            self.recordLabel.config(text=r)
        else:
            self.recordLabel.config(text="無")

    def setLevelLabel(self):
        if self.level == "Gentle/Very":
            self.varLevel.set(1)
            self.levelLabel.config(text="初學")
        elif self.level == "Gentle/Easy":
            self.varLevel.set(2)
            self.levelLabel.config(text="簡單")
        elif self.level == "Moderate":
            self.varLevel.set(3)
            self.levelLabel.config(text="進階")
        elif self.level == "Tough":
            self.varLevel.set(4)
            self.levelLabel.config(text="中等")
        elif self.level == "Diabolical":
            self.varLevel.set(5)
            self.levelLabel.config(text="困難")
        elif self.level == "Extreme":
            self.varLevel.set(6)
            self.levelLabel.config(text="艱深")
        elif self.level == "!!!!!":
            self.varLevel.set(7)
            self.levelLabel.config(text="登峰造極")

    def setTimer(self):
        if self.timer is not None and not self.pause:
            self.timeLabel.after_cancel(self.timer)
            self.sec += 1
            s = str(self.sec % 60)
            h = str(self.sec / 3600)
            m = str(self.sec / 60)
            self.timeLabel.config(
                text="{}:{}:{}".format(h.zfill(2), m.zfill(2), s.zfill(2)))
            self.timeLabel.after(1000, self.setTimer)

    def reset(self):
        if self.helper.loadPuzzle() is None:
            self.filemenu.entryconfig(1, state="disable")
        self.filemenu.entryconfig(2, state="normal")
        self.canvas.delete(ALL)
        del self.gridList[:]
        del self.rectList[:]
        del self.candidateGridList[:]
        self.drawLine()
        self.generateGrid()
        self.canvas.create_text(
            self.puzzleframe_width / 2, self.puzzleframe_height / 2,
            text="暫停",
            font=("Purisa", self.gridFontSize * 2),
            state="hidden",
            tag="pauseText")
        self.previousClick = None
        self.note = False
        self.pause = False
        self.timer = None
        self.sec = 0

    def newGame(self):
        self.reset()
        self.helper.getPuzzle(self.level)
        for index, (i, num) in enumerate(
                zip(self.gridList, self.helper.puzzle)):
            if int(num) != 0:
                rect = "rect" + str(index)
                self.canvas.itemconfigure(rect, fill="gainsboro")
                self.canvas.itemconfigure(i, text=num)
                self.canvas.tag_raise(i)
            else:
                self.canvas.itemconfigure(i, text="")
                self.generateCandidateGrid(i)
        self.setRecordLabel()
        self.timer = self.timeLabel.after(1000, self.setTimer)
        self.setLevelLabel()

    def loadGame(self):
        self.reset()
        data = self.helper.loadPuzzle()  # current puzzle, time,note
        current_puzzle = data[0]
        time = data[1]
        note = data[2:]
        self.level = self.helper.level
        self.sec = int(time)
        for index, (i, num) in enumerate(
                zip(self.gridList, self.helper.puzzle)):
            rect = "rect" + str(index)
            if int(num) != 0:
                self.canvas.itemconfigure(rect, fill="gainsboro")
                self.canvas.itemconfigure(i, text=num)
                self.canvas.tag_raise(i)
            else:
                self.canvas.itemconfigure(i, text="")
                self.generateCandidateGrid(i)
                if current_puzzle[index] != "0":
                    self.canvas.itemconfigure(rect, fill="")
                    self.canvas.itemconfigure(i, text=current_puzzle[index])
                for j in range(1, 10):
                    tag = "grid" + str(index) + "_" + str(j)
                    if note[index][j - 1] == "1":
                        self.canvas.itemconfigure(tag, state="normal")
        self.setRecordLabel()
        self.timer = self.timeLabel.after(1000, self.setTimer)
        self.setLevelLabel()
        self.pauseButtonOnClick()
        tkMessageBox.showinfo("訊息", "載入成功")
        self.pauseButtonOnClick()

    def saveGame(self):
        self.pauseButtonOnClick()
        current_puzzle = ""
        note = ""
        for i, t in enumerate(self.gridList):
            num = self.canvas.itemcget(t, "text")
            num = num if num != "" else "0"
            current_puzzle += num
            cnum = ""
            for j in range(1, 10):
                tag = "grid" + str(i) + "_" + str(j)
                if self.canvas.itemcget(tag, "state") == "normal":
                    cnum += "1"
                else:
                    cnum += "0"
            if i + 1 != len(self.gridList):
                note += cnum + ","
            else:
                note += cnum
        time = str(self.sec)
        self.helper.savePuzzle(current_puzzle, time, note)
        tkMessageBox.showinfo("訊息", "儲存成功")
        self.pauseButtonOnClick()

    def changeLevel(self, level):
        if level == 1:
            self.level = "Gentle/Very"
        elif level == 2:
            self.level = "Gentle/Easy"
        elif level == 3:
            self.level = "Moderate"
        elif level == 4:
            self.level = "Tough"
        elif level == 5:
            self.level = "Diabolical"
        elif level == 6:
            self.level = "Extreme"
        elif level == 7:
            self.level = "!!!!!"
        else:
            pass
        self.newGame()

    def helpDialog(self):
        tkMessageBox.showinfo(
            "幫助",
            "每行、列、九宮格填入1~9且不可重複\n" +
            "可使用方向鍵或滑鼠選取格子\n使用數字鍵盤或下方數字按鈕填入數字\n" +
            "筆記：n/N\n" +
            "刪除：backspace/delete\n" +
            "暫停：whitespace\n" +
            "提示：t/T\n" +
            "解答：\n" +
            "離開：Esc")

    def aboutDialog(self):
        tkMessageBox.showinfo("關於", "python final project")

    def numberButtonOnClick(self, num):
        if self.previousClick is not None and not self.pause:
            if self.note:
                tag = "grid" + self.previousClick[4:]
                if self.canvas.itemcget(tag, "text") != "":
                    self.canvas.itemconfig(tag, text="")
                tag = tag + "_" + str(num)
                print tag
                if self.canvas.itemcget(tag, "state") == "hidden":
                    self.canvas.itemconfig(tag, state="normal")
                else:
                    self.canvas.itemconfig(tag, state="hidden")
                # self.canvas.tag_raise(tag)
            else:
                for i in range(1, 10):
                    candidate = "grid" + self.previousClick[4:] + "_" + str(i)
                    if self.canvas.itemcget(candidate, "state") == "normal":
                        self.canvas.itemconfig(candidate, state="hidden")
                self.canvas.itemconfig(self.previousClick, fill="")
                tag = "grid" + self.previousClick[4:]
                if self.canvas.itemcget(tag, "text") == str(num):
                    self.canvas.itemconfig(tag, text="")
                else:
                    self.canvas.itemconfig(tag, text=str(num))
                    index = int(self.previousClick[4:])
                    self.deleteCandidateNumber(index, num)
                self.checkFinish()

    def deleteButtonOnClick(self):
        if self.previousClick is not None and not self.pause:
            tag = "grid" + self.previousClick[4:]
            self.canvas.itemconfig(self.previousClick, fill="white")
            self.canvas.itemconfig(tag, text="")
            for i in range(1, 10):
                candidate = tag + "_" + str(i)
                if self.canvas.itemcget(candidate, "state") == "normal":
                    self.canvas.itemconfig(candidate, state="hidden")

    def noteButtonOnClick(self):
        self.note = False if self.note else True
        if self.note:
            self.noteButton.select()
        else:
            self.noteButton.deselect()

    def pauseButtonOnClick(self):
        self.pause = False if self.pause else True
        if self.pause:
            self.pauseButton.config(text="繼續")
            for i, (g, r) in enumerate(zip(self.gridList, self.rectList)):
                self.canvas.itemconfig(g, state="hidden")
                self.canvas.itemconfig(r, state="hidden")
                for j in range(1, 10):
                    tag = "grid" + str(i) + "_" + str(j)
                    if self.canvas.itemcget(tag, "state") == "normal":
                        self.canvas.itemconfig(tag, state="hidden")
                        self.storeCandidateGrid.append(tag)
            self.canvas.itemconfig("pauseText", state="normal")
        else:
            self.pauseButton.config(text="暫停")
            for g, r in zip(self.gridList, self.rectList):
                self.canvas.itemconfig(g, state="normal")
                self.canvas.itemconfig(r, state="normal")
            for i in self.storeCandidateGrid:
                self.canvas.itemconfig(i, state="normal")
            del self.storeCandidateGrid[:]
            self.timer = self.timeLabel.after(1000, self.setTimer)
            self.canvas.itemconfig("pauseText", state="hidden")

    def hintButtonOnClick(self):
        if self.previousClick is not None and not self.pause:
            index = int(self.previousClick[4:])
            tag = "grid" + self.previousClick[4:]
            self.canvas.itemconfig(tag, text=self.helper.answer[index])
            tag = "rect" + tag[4:]
            if self.canvas.itemcget(tag, "fill") == "white":
                self.canvas.itemconfig(tag, fill="")

    def answerButtonOnClick(self):
        if not self.pause:
            for i, t in enumerate(self.gridList):
                if self.helper.puzzle is not None:
                    self.canvas.itemconfig(t, text=self.helper.answer[i])
                    tag = "rect" + str(i)
                    if self.canvas.itemcget(tag, "fill") == "white":
                        self.canvas.itemconfig(tag, fill="")
                for i in range(1, 10):
                    tag = self.canvas.itemcget(t, "tag") + "_" + str(i)
                    if self.canvas.itemcget(tag, "state") == "normal":
                        self.canvas.itemconfig(tag, state="hidden")
            self.checkFinish()

    def gridOnClick(self, Event):
        item = self.canvas.find_closest(Event.x, Event.y)
        try:
            tag = self.canvas.gettags(item)[0]
        except Exception:
            return
        self.gridSelect(tag)

    def gridSelect(self, tag):
        # print tag, self.canvas.itemcget(tag, "fill")
        if tag[:4] == "rect":
            gridtag = "grid" + tag[4:]
            if self.canvas.itemcget(gridtag, "text") == "":
                if self.previousClick is not None:
                    self.canvas.itemconfig(self.previousClick, outline="white")
                self.canvas.itemconfig(tag, outline="blue")
                self.previousClick = tag
        elif tag[:4] == "grid":
            recttag = "rect" + tag[4:]
            if self.canvas.itemcget(recttag, "fill") == "":
                if self.previousClick is not None:
                    self.canvas.itemconfig(self.previousClick, outline="white")
                self.canvas.itemconfig(recttag, outline="blue")
                self.previousClick = recttag

    def candidateGridOnClick(self, Event):
        item = self.canvas.find_closest(Event.x, Event.y)
        tag = self.canvas.gettags(item)[0]
        gridtag = tag.split('_')[0]
        recttag = "rect" + gridtag[4:]
        if self.previousClick is not None:
            self.canvas.itemconfig(self.previousClick, outline="white")
        self.canvas.itemconfig(recttag, outline="blue")
        self.previousClick = recttag

    def deleteCandidateNumber(self, index, number):
        row = index / 9
        col = index % 9
        # check col
        for i in range(9):
            newindex = i * 9 + col
            tag = "grid" + str(newindex) + "_" + str(number)
            if self.canvas.itemcget(tag, "state") == "normal":
                self.canvas.itemconfig(tag, state="hidden")
        # check row
        for i in range(9):
            newindex = row * 9 + i
            tag = "grid" + str(newindex) + "_" + str(number)
            if self.canvas.itemcget(tag, "state") == "normal":
                self.canvas.itemconfig(tag, state="hidden")
        # check box
        box_row = row - row % 3
        box_col = col - col % 3
        for i in range(9):
            newindex = (box_row + i / 3) * 9 + (box_col + i % 3)
            tag = "grid" + str(newindex) + "_" + str(number)
            if self.canvas.itemcget(tag, "state") == "normal":
                self.canvas.itemconfig(tag, state="hidden")

    def checkFinish(self):
        puzzle = ""
        for i, t in enumerate(self.gridList):
            num = self.canvas.itemcget(t, "text")
            if num == "":
                return
            puzzle += num
        if puzzle == self.helper.answer:  # finished
            self.timer = None
            tkMessageBox.showinfo(
                "遊戲結束",
                "題目編號：{}\n難度：{}\n遊戲時間：{}".format(
                    self.helper.index,
                    self.helper.level,
                    self.timeLabel.cget("text")))
            if tkMessageBox.askyesno("訊息", "再玩一局?"):
                self.newGame()

    def numberKey(self, event):
        # print "pressed", repr(event.char)
        try:
            num = int(event.char)
            if num != 0:
                self.numberButtonOnClick(num)
        except Exception:
            pass

    def deleteKey(self, event):
        self.deleteButtonOnClick()

    def arrowKey(self, event):
        key = event.keysym
        if self.previousClick is not None:
            tag = self.previousClick[:4]
            index = int(self.previousClick[4:])
        else:
            index = 0
            tag = "rect"
        index = self.move(key, index)
        tag = tag + str(index)
        while self.canvas.itemcget(tag, "fill") == "gainsboro":
            index = self.move(key, index)
            tag = tag[:4] + str(index)
        gridTag = "grid" + tag[4:]
        if self.canvas.itemcget(gridTag, "text") != "":
            tag = gridTag
        self.gridSelect(tag)

    def move(self, key, index):
        if key == "Left":
            if index % 9 == 0:
                index += 8
            else:
                index -= 1
        elif key == "Right":
                if index % 9 == 8 and index != 0:
                    index -= 8
                else:
                    index += 1
        elif key == "Up":
                if index / 9 == 0:
                    index += 72
                else:
                    index -= 9
        elif key == "Down":
                if index / 9 == 8:
                    index -= 72
                else:
                    index += 9
        return index

    def noteKey(self, event):
        self.noteButtonOnClick()

    def pauseKey(self, event):
        self.pauseButtonOnClick()

    def exitKey(self, event):
        import sys
        sys.exit()


if __name__ == "__main__":
    root = Tk()
    game = App(root)
    root.mainloop()
    # s = solver("000051006650000021000003500" \
    # "940300360000000900000000506000007020040070750027000001")
    # print "waiting for solving..."
    # if s.solve():
    #     print s.board
    # else:
    #     print "can not solve!"
    # g = generator()
    # print "Generating solved puzzle..."
    # if g.generateSolvedPuzzle():
    #     print "Successed!"
    #     print "Generating puzzle..."
    #     g.generatePuzzle()
    #     g.printBoard()
    # else:
    #     print "failed"
