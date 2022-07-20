# This is a sample Python script.

# Press ⇧⌘F11 to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

import tkinter as tk
import tkinter.filedialog
from typing import List, Dict

import conditionwindow
from configrecorder import saveConditions, loadConditions
from filterutils import filterFile, Condition


def openFileDialog():
    global condition_dict
    filename = tk.filedialog.askopenfilename(initialdir='/Users/jiangfeng/log/scene')
    if filename is not None and filename != '':
        filterFile(filename, condition_dict.values(), text)
    else:
        root.title(default_title)
    global file_name
    file_name = filename


# 条件CheckButton的鼠标右键菜单
def showPopupMenu(event, check_button):
    menu = tk.Menu(root, tearoff=False)
    menu.add_command(label='edit', command=lambda: editCondition(check_button))
    menu.add_command(label='delete', command=lambda: removeCondition(check_button))
    menu.post(event.x_root, event.y_root)


def addCondition(condition, tag=None):
    global condition_dict
    old_condition = None
    if tag is not None:
        old_condition = condition_dict[tag]
    if old_condition is not None:
        condition_dict[tag] = condition
        tag.config(variable=condition.available)
    else:
        cb = tk.Checkbutton(bts_container, text=condition.name, indicatoron=False, variable=condition.available)
        cb.bind('<Button-2>', lambda event: showPopupMenu(event, cb))
        cb.pack(side='right')
        condition_dict[cb] = condition


def refreshConditions(condition_list):
    for cb in condition_dict:
        cb.pack_forget()

    condition_dict.clear()

    for condition in condition_list:
        cb = tk.Checkbutton(bts_container, text=condition.name, indicatoron=False, variable=condition.available)
        cb.bind('<Button-2>', lambda event: showPopupMenu(event, cb))
        cb.pack(side='right')
        condition_dict[cb] = condition


def editCondition(check_button):
    condition = condition_dict[check_button]
    condition_window = conditionwindow.ConditionDialog(root)
    condition_window.show(addCondition, condition, check_button)


def removeCondition(check_button):
    del condition_dict[check_button]
    check_button.pack_forget()


def showAddConditionDialog():
    condition_window = conditionwindow.ConditionDialog(root)
    condition_window.show(addCondition)


def onFilterClick():
    global file_name, condition_dict
    if file_name is not None and file_name != '':
        filterFile(file_name, condition_dict.values(), text)


if __name__ == '__main__':
    default_title = '场景引擎log分析工具'

    condition_dict: Dict[tk.Checkbutton, Condition] = {}
    file_name: str = None

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

    # 打开文件按钮
    btn_open = tk.Button(bts_container, text="open", command=openFileDialog)
    btn_open.pack(side='left')

    # 保存条件到文件按钮
    btn_save_condition = tk.Button(bts_container,
                                   text="save",
                                   command=lambda: saveConditions(condition_dict.values()))
    btn_save_condition.pack(side='left')

    # 从文件载入条件按钮
    btn_load_condition = tk.Button(bts_container,
                                   text="load",
                                   command=lambda: loadConditions(refreshConditions))
    btn_load_condition.pack(side='left')

    # 添加条件按钮
    btn_add_condition = tk.Button(bts_container, text="add", command=showAddConditionDialog)
    btn_add_condition.pack(side='left')

    # filter 按钮
    btn_filter = tk.Button(bts_container, text="filter", command=onFilterClick).pack(side='right')

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
