# This is a sample Python script.

# Press ⇧⌘F11 to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

import tkinter as tk
import tkinter.filedialog
from typing import List

from conditionmanager import ConditionListWindow
from eventwindow import EventSelectWindow
from filterutils import filterFile, Condition, parseFile, StartLine
from realtimelogfilter import RealTimeLogFilter
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
    filterFile(gl_file_name, startline, endline, gl_condition_list, lambda strline: text_main.insert(tk.INSERT, strline))


def onFilterClick():
    global gl_file_name, gl_condition_list
    if gl_file_name is not None and gl_file_name != '':
        filterFile(gl_file_name, gl_condition_list, lambda strline: text_main.insert(tk.INSERT, strline))


def onConditionChangedCallback(condition_list):
    global gl_condition_list, gl_start_line, gl_end_line, gl_real_time_log_filter
    gl_condition_list = condition_list
    filterFilePiece(gl_start_line, gl_end_line)
    if gl_real_time_log_filter is not None:
        gl_real_time_log_filter.setConditions(condition_list)


def openFilterDialog():
    ConditionListWindow(gl_root, onConditionChangedCallback)


def openEventDialog():
    EventSelectWindow(gl_root, onConditionChangedCallback)


def appendTextCallback(strline):
    global text_main, gl_vbar
    text_main.insert(tk.END, strline)
    yview = text_main.yview()[1]
    if yview > 0.999:
        text_main.yview(tk.MOVETO, 1.0)


def startRealTimeLog():
    global text_main, gl_condition_list, gl_real_time_log_filter, gl_btn_real_time_log
    if gl_real_time_log_filter is None:
        text_main.delete(0.0, tk.END)
        realfilter = RealTimeLogFilter(lambda strline: appendTextCallback(strline))
        realfilter.setConditions(gl_condition_list)
        realfilter.start()
        gl_real_time_log_filter = realfilter
        gl_btn_real_time_log.config(text='停止log')
    else:
        gl_real_time_log_filter.stop()
        gl_real_time_log_filter = None
        gl_btn_real_time_log.config(text='实时log')


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
    btn_open_log_file = tk.Button(first_frame, text="log文件", command=openFileDialog)
    btn_open_log_file.pack(side='left')

    # 条件窗口 按钮
    btn_filter_dialog = tk.Button(first_frame, text="条件窗口", command=openFilterDialog)
    btn_filter_dialog.pack(side='left')

    # 事件窗口 按钮
    btn_event_dialog = tk.Button(first_frame, text="事件窗口", command=openEventDialog)
    btn_event_dialog.pack(side='left')

    # 实时log 按钮
    gl_real_time_log_filter: RealTimeLogFilter = None
    gl_btn_real_time_log = tk.Button(first_frame, text="实时log", command=startRealTimeLog)
    gl_btn_real_time_log.pack(side='left')

    # --------------  第二层 工具栏  --------------
    second_frame = tk.LabelFrame(gl_root)
    second_frame.pack(side='top', fill='x')

    # --------------  文本显示区域  --------------

    # 用于显示log文本的文本框和滚动条
    hbar = tk.Scrollbar(gl_root, orient='horizontal')
    hbar.pack(side='bottom', fill='x')
    gl_vbar = tk.Scrollbar(gl_root, orient='vertical')
    gl_vbar.pack(side='right', fill='y')

    text_main = tk.Text(gl_root, width=1800, height=800, font=('Menlo Regular', 14), wrap='char', spacing1=5,
                        xscrollcommand=hbar.set, yscrollcommand=gl_vbar.set)
    text_main.pack(side='left', fill='both')
    gl_vbar.config(command=text_main.yview)
    hbar.config(command=text_main.xview)

    gl_root.wm_protocol("WM_DELETE_WINDOW", lambda: closeWindowCallback())

    gl_root.mainloop()
