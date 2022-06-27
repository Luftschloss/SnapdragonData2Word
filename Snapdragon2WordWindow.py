from enum import Enum
import WordOutput
import FrameDataOutput
import tkinter as tk
from tkinter import ttk
import tkinter.filedialog

frameResourcePath = "\\FrameCapture"


class CSVType(Enum):
    RealTime = 1        # RealTime
    Frame = 2           # Frame


class TKLayout:
    def __init__(self, x, y, anchor):
        self.x = x
        self.y = y
        self.anchor = anchor

    x = 0
    y = 0
    anchor = 'w'


tkLayoutDic = {}


cur_csv_type = CSVType.RealTime


def OpenFileSelectWindow():
    filename = tk.filedialog.askopenfilename()
    if filename != '' and filename.endswith('.csv'):
        selectFileLb.config(text=filename)
    else:
        tkinter.messagebox.showinfo(title='Warning', message='您没有选择任何文件/文件非csv格式')


def SwitchRealTime():
    topDCLb.place_forget()
    topDCInput.place_forget()
    sortMatrixLb.place_forget()
    selectMatrixDb.pack_forget()

    timePeriodLb.place(x=tkLayoutDic[timePeriodLb].x, y=tkLayoutDic[timePeriodLb].y, anchor=tkLayoutDic[timePeriodLb].anchor)
    timePeriodInput.place(x=tkLayoutDic[timePeriodInput].x, y=tkLayoutDic[timePeriodInput].y, anchor=tkLayoutDic[timePeriodInput].anchor)
    slicedPeriodLB.place(x=tkLayoutDic[slicedPeriodLB].x, y=tkLayoutDic[slicedPeriodLB].y, anchor=tkLayoutDic[slicedPeriodLB].anchor)
    slicedPeriodInput.place(x=tkLayoutDic[slicedPeriodInput].x, y=tkLayoutDic[slicedPeriodInput].y, anchor=tkLayoutDic[slicedPeriodInput].anchor)

    global cur_csv_type
    cur_csv_type = CSVType.RealTime


def SwitchFrame():
    timePeriodLb.place_forget()
    timePeriodInput.place_forget()
    slicedPeriodLB.place_forget()
    slicedPeriodInput.place_forget()

    sortMatrixLb.place(x=tkLayoutDic[sortMatrixLb].x, y=tkLayoutDic[sortMatrixLb].y, anchor=tkLayoutDic[sortMatrixLb].anchor)
    selectMatrixDb.pack(padx=tkLayoutDic[selectMatrixDb].x, pady=tkLayoutDic[selectMatrixDb].y)
    topDCLb.place(x=tkLayoutDic[topDCLb].x, y=tkLayoutDic[topDCLb].y, anchor=tkLayoutDic[topDCLb].anchor)
    topDCInput.place(x=tkLayoutDic[topDCInput].x, y=tkLayoutDic[topDCInput].y, anchor=tkLayoutDic[topDCInput].anchor)

    global cur_csv_type
    cur_csv_type = CSVType.Frame


def ConvertWord():
    csv_path = selectFileLb.cget("text")
    if cur_csv_type == CSVType.RealTime:
        try:
            timeP = None
            text1 = timePeriodInput.get()
            if text1 != '':
                timeP = eval("[%s]" % text1)
            text2 = slicedPeriodInput.get()
            timeS = None
            if text2 != '':
                timeS = list(map(int, text2.split(',')))
            word = WordOutput.createSnapDragonDataDocx(csv_path, "SDPRealTime.docx", timeP, timeS)
        except Exception as err:
            tkinter.messagebox.showinfo(title='Warning', message=err)
        else:
            if word is not None:
                tkinter.messagebox.showinfo(title='Succeed', message='生成成功！' + word)
    else:
        try:
            topCount = 10
            if not topDCInput.get() == "":
                topCount = int(topDCInput.get())
            word, retStr = FrameDataOutput.getTopDrawCall(csv_path, "SDPFrame.docx", topCount, "Read Total (Bytes)", frameResourcePath)
        except Exception as err:
            tkinter.messagebox.showinfo(title='Warning', message=err)
        else:
            if retStr is not None:
                tkinter.messagebox.showinfo(title='Succeed', message='生成成功！' + word + "\n " + retStr)


windowWidth = 600
windowHeight = 400
defaultTimePeriodStr = "输入数据时间段，格式如：(x1,x2),...,(n1,n2)"
defaultSlicedPeriodStr = "输入分割线时间结点，格式如：x1,..,xn"
defaultTopStr = "输入Top DrawCall数量"

window = tk.Tk()
window.title("Snapdragon2Word")
window.geometry(str.format('{0}x{1}', windowWidth, windowHeight))
window.resizable(0, 0)

# 菜单栏
menuToolBar = tk.Menu(window)
modelMenu = tk.Menu(menuToolBar, tearoff=0)
menuToolBar.add_cascade(label='CSV数据类型', menu=modelMenu)
modelMenu.add_command(label='RealTimeData', command=SwitchRealTime)
modelMenu.add_command(label='FrameData', command=SwitchFrame)
window.config(menu=menuToolBar)

# Window主体内容
selectFileLb = tk.Label(window, text='*请选择文件*')
selectFileLb.place(x=10, y=20, anchor='w')
tkLayoutDic[selectFileLb] = TKLayout(10, 20, 'w')
selectFileBtn = tk.Button(window, text="选择文件", command=OpenFileSelectWindow)
selectFileBtn.place(x=580, y=20, anchor='e')
tkLayoutDic[selectFileBtn] = TKLayout(580, 20, 'e')

# Realtime特有的
timePeriodLb = tk.Label(window, text=defaultTimePeriodStr)
timePeriodLb.place(x=20, y=50, anchor='w')
tkLayoutDic[timePeriodLb] = TKLayout(20, 50, 'w')

timePeriodInput = tk.Entry(window, show=None, width=50, font=('Arial', 12))
timePeriodInput.place(x=20, y=80, anchor='w')
tkLayoutDic[timePeriodInput] = TKLayout(20, 80, 'w')

slicedPeriodLB = tk.Label(window, text=defaultSlicedPeriodStr)
slicedPeriodLB.place(x=20, y=110, anchor='w')
tkLayoutDic[slicedPeriodLB] = TKLayout(20, 110, 'w')

slicedPeriodInput = tk.Entry(window, show=None, width=50, font=('Arial', 12))
slicedPeriodInput.place(x=20, y=140, anchor='w')
tkLayoutDic[slicedPeriodInput] = TKLayout(20, 140, 'w')

# Frame特有的
sortMatrixLb = tk.Label(window, text="选择排序的GPU数据列")
sortMatrixLb.place(x=20, y=50, anchor='w')
tkLayoutDic[sortMatrixLb] = TKLayout(20, 50, 'w')

selectMatrixDb = ttk.Combobox(window, values=["Read Total (Bytes)", "Clocks"])
selectMatrixDb.grid(column=0, row=0)
selectMatrixDb.current(0)
tkLayoutDic[selectMatrixDb] = TKLayout(20, 80, 'w')
selectMatrixDb.pack_forget()

topDCLb = tk.Label(window, text=defaultTopStr)
topDCLb.place(x=20, y=110, anchor='w')
tkLayoutDic[topDCLb] = TKLayout(20, 110, 'w')

topDCInput = tk.Entry(window, show=None, width=140, font=('Arial', 12))
topDCInput.place(x=20, y=140, anchor='w')
tkLayoutDic[topDCInput] = TKLayout(20, 140, 'w')

covertBtn = tk.Button(window, text="生成Word", command=ConvertWord)
covertBtn.place(x=580, y=110, anchor='e')

window.mainloop()
