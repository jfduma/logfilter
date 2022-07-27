# This is a sample Python script.

# Press ⇧⌘F11 to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

import tkinter as tk
import tkinter.filedialog
from tkinter import messagebox
from typing import List, Dict

from conditionmanager import ConditionListWindow
from filterutils import filterFile, Condition, parseFile, StartLine
from timelinewindow import TimeLineWindow


def openFileDialog():
    global gl_condition_list, gl_start_list, gl_root
    filename = tk.filedialog.askopenfilename(initialdir='/Users/jiangfeng/log/scene')
    if filename is not None and filename != '':
        gl_root.title(filename)
        # filterFile(filename, condition_dict.values(), text)
        gl_start_list = parseFile(filename)
        TimeLineWindow(gl_root, gl_start_list).show(lambda startline, endline: filterFilePiece(startline, endline))
    else:
        gl_root.title(default_title)
    global gl_file_name
    gl_file_name = filename


def filterFilePiece(startline, endline):
    global text_main, gl_condition_list, gl_start_line, gl_end_line, gl_file_name
    gl_start_line = startline
    gl_end_line = endline
    if gl_file_name is None or gl_start_line is None:
        return
    text_main.delete(0.0, tk.END)
    filterFile(gl_file_name, startline, endline, gl_condition_list, lambda strline: text_main.insert('insert', strline))


def onFilterClick():
    global gl_file_name, gl_condition_list
    if gl_file_name is not None and gl_file_name != '':
        filterFile(gl_file_name, gl_condition_list, lambda strline: text_main.insert('insert', strline))


def onConditionChangedCallback(condition_list):
    global gl_condition_list, gl_start_line, gl_end_line
    gl_condition_list = condition_list
    filterFilePiece(gl_start_line, gl_end_line)


def closeWindowCallback():
    global gl_root
    gl_root.destroy()
    # if messagebox.askokcancel("Quit", "Do you really wish to quit?"):
    #     gl_root.destroy()


if __name__ == '__main__':
    default_title = '场景引擎log分析工具'

    gl_start_list: List[StartLine] = []
    gl_file_name: str = None
    gl_condition_list: List[Condition] = []
    gl_start_line: int = None
    gl_end_line: int = None

    # 添加主窗口，获取屏幕尺寸以计算布局参数，使窗口居屏幕中央
    gl_root = tk.Tk()
    gl_root.title(default_title)
    width = 1100
    height = 700
    screenwidth = gl_root.winfo_screenwidth()
    screenheight = gl_root.winfo_screenheight()
    size_geo = '%dx%d+%d+%d' % (width, height, 100, 100)
    gl_root.geometry(size_geo)

    # --------------  第一层 工具栏  --------------

    # 添加上部按钮容器
    first_frame = tk.LabelFrame(gl_root, relief='raised')
    first_frame.pack(side='top', fill='x')

    # 打开文件按钮
    btn_open = tk.Button(first_frame, text="open", command=openFileDialog)
    btn_open.pack(side='left')

    # filter 按钮
    # btn_filter = tk.Button(first_frame, text="filter", command=onFilterClick).pack(side='right')

    # --------------  第二层 工具栏  --------------
    second_frame = tk.LabelFrame(gl_root)
    second_frame.pack(side='top', fill='x')

    # --------------  文本显示区域  --------------

    # 用于显示log文本的文本框和滚动条
    hbar = tk.Scrollbar(gl_root, orient='horizontal')
    hbar.pack(side='bottom', fill='x')
    vbar = tk.Scrollbar(gl_root, orient='vertical')
    vbar.pack(side='right', fill='y')

    text_main = tk.Text(gl_root, width=1800, height=800, font=('Menlo Regular', 14), wrap='char', spacing1=5,
                        xscrollcommand=hbar.set, yscrollcommand=vbar.set)
    text_main.pack(side='left', fill='both')
    vbar.config(command=text_main.yview)
    hbar.config(command=text_main.xview)

    ConditionListWindow(gl_root, onConditionChangedCallback)

    gl_root.wm_protocol("WM_DELETE_WINDOW", lambda: closeWindowCallback())

    gl_root.mainloop()
