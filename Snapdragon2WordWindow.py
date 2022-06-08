from enum import Enum
import WordOutput
import FrameDataOutput
import tkinter as tk
import tkinter.filedialog

frameResourcePath = "..\\Snapdragon2Word\\FrameCapture"

class CSVType(Enum):
    RealTime = 1        # RealTime
    Frame = 2           # Frame


cur_csv_type = CSVType.RealTime


def OpenFileSelectWindow():
    filename = tk.filedialog.askopenfilename()
    if filename != '' and filename.endswith('.csv'):
        filelb.config(text=filename)
    else:
        tkinter.messagebox.showinfo(title='Warning', message='您没有选择任何文件/文件非csv格式')


def SwitchRealTime():
    toplb.place_forget()
    topCountInput.place_forget()

    lb1.place(x=20, y=50, anchor='w')
    timePeriodInput.place(x=20, y=80, anchor='w')
    lb2.place(x=20, y=110, anchor='w')
    slicedPeriodInput.place(x=20, y=140, anchor='w')

    global cur_csv_type
    cur_csv_type = CSVType.RealTime


def SwitchFrame():
    lb1.place_forget()
    timePeriodInput.place_forget()
    lb2.place_forget()
    slicedPeriodInput.place_forget()

    toplb.place(x=20, y=50, anchor='w')
    topCountInput.place(x=20, y=80, anchor='w')

    global cur_csv_type
    cur_csv_type = CSVType.Frame


def ConvertWord():
    csv_path = filelb.cget("text")
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
            if not topCountInput.get() == "":
                topCount = int(topCountInput.get())
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
filelb = tk.Label(window, text='*请选择文件*')
filelb.place(x=10, y=20, anchor='w')
fileBtn = tk.Button(window, text="选择文件", command=OpenFileSelectWindow)
fileBtn.place(x=580, y=20, anchor='e')

lb1 = tk.Label(window, text=defaultTimePeriodStr)
lb1.place(x=20, y=50, anchor='w')
timePeriodInput = tk.Entry(window, show=None, width=50, font=('Arial', 12))
timePeriodInput.place(x=20, y=80, anchor='w')
lb2 = tk.Label(window, text=defaultSlicedPeriodStr)
lb2.place(x=20, y=110, anchor='w')
slicedPeriodInput = tk.Entry(window, show=None, width=50, font=('Arial', 12))
slicedPeriodInput.place(x=20, y=140, anchor='w')
covertBtn = tk.Button(window, text="生成Word", command=ConvertWord)
covertBtn.place(x=580, y=110, anchor='e')

toplb = tk.Label(window, text=defaultTopStr)
toplb.place(x=20, y=50, anchor='w')
topCountInput = tk.Entry(window, show=None, width=50, font=('Arial', 12))
topCountInput.place(x=20, y=80, anchor='w')

window.mainloop()
