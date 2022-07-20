# This is a sample Python script.

# Press ⇧⌘F11 to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

import tkinter as tk
import tkinter.filedialog

import conditionwindow
from filterutils import filterFile, Condition


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⇧⌘B to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    default_title = '场景引擎log分析工具'

    # 添加主窗口，获取屏幕尺寸以计算布局参数，使窗口居屏幕中央
    root = tk.Tk()
    root.title(default_title)
    width = 800
    height = 500
    screenwidth = root.winfo_screenwidth()
    screenheight = root.winfo_screenheight()
    size_geo = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
    root.geometry(size_geo)

    # 添加上部按钮容器
    bts_container = tk.LabelFrame(root, relief='raised')
    bts_container.pack(side='top', fill='x')

    # 添加打开文件按钮
    def askFile():
        filename = tk.filedialog.askopenfilename(initialdir='$HOME/log/scene')
        if filename != '':
            root.title(filename)
            con1 = Condition()
            con1.addIncludeKey('aaa')
            con2 = Condition()
            con2.addIncludeKey('111')

            filterFile(filename, [con1, con2], text)
        else:
            root.title(default_title)

    btn_open = tk.Button(bts_container, text="open", command=askFile)
    btn_open.pack(side='left')

    # 添加新增条件按钮
    condition_window = conditionwindow.ConditionDialog(root)

    def addCondition():
        condition_window.show()

    btn_add_condition = tk.Button(bts_container, text="add", command=addCondition).pack(side='left')

    # checkbutton 关键字选择
    cb_master = tk.Checkbutton(bts_container, text="Main", indicatoron=False).pack(side='left')
    cb_master = tk.Checkbutton(bts_container, text="Message", indicatoron=False).pack(side='left')
    cb_master = tk.Checkbutton(bts_container, text="Trigger", indicatoron=False).pack(side='left')

    # 用于显示log文本的文本框和滚动条
    hbar = tk.Scrollbar(root, orient='horizontal')
    hbar.pack(side='bottom', fill='x')
    vbar = tk.Scrollbar(root, orient='vertical')
    vbar.pack(side='right', fill='y')

    text = tk.Text(root, width=1800, height=800, font=('Menlo Regular', 14), wrap='char', spacing1=5,
                   xscrollcommand=hbar.set, yscrollcommand=vbar.set)
    text.pack(side='left', fill='both')
    vbar.config(command=text.yview)
    hbar.config(command=text.xview)

    root.mainloop()
