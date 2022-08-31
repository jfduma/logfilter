import tkinter as tk

import editconditionwindow
from configrecorder import loadConditions, saveConditions, loadFromFile


class ConditionListWindow:

    def __init__(self, root, callback):
        self.condition_dict = {}
        self.root = root
        self.callback = callback
        self.window = tk.Toplevel(root)
        self.window.title("conditions")
        self.window.geometry('280x320+1220+100')
        self.window.wm_protocol("WM_DELETE_WINDOW", lambda: self.closeCallback())

        first_frame = tk.LabelFrame(self.window, relief='raised')
        first_frame.pack(side='top', fill='x')

        # 从文件载入条件按钮
        btn_load_condition = tk.Button(first_frame,
                                       text="load",
                                       command=lambda: loadConditions(self.addAllConditions))
        btn_load_condition.pack(side='left')

        # 保存条件到文件按钮
        btn_save_condition = tk.Button(first_frame,
                                       text="save",
                                       command=lambda: saveConditions(self.condition_dict.values()))
        btn_save_condition.pack(side='left')

        # second_frame = tk.LabelFrame(self.window, relief='raised')
        # second_frame.pack(side='top', fill='x')

        # 添加条件按钮
        btn_add_condition = tk.Button(first_frame, text="add", command=self.showAddConditionDialog)
        btn_add_condition.pack(side='left')

        # 执行过滤按钮
        btn_add_condition = tk.Button(first_frame, text="done", command=lambda: self.callback(self.condition_dict.values()))
        btn_add_condition.pack(side='left')

        # 自动加载默认条件配置文件
        filename = '../sla/default.json'
        self.addAllConditions(loadFromFile(filename))

    def addAllConditions(self, condition_list):
        for cb in self.condition_dict.keys():
            cb.pack_forget()

        self.condition_dict.clear()

        for condition in condition_list:
            self.addCondition(condition)

    def addCondition(self, condition, tag=None):
        old_condition = None
        if tag is not None:
            old_condition = self.condition_dict[tag]
        if old_condition is not None:
            self.condition_dict[tag] = condition
            tag.config(variable=condition.available, text=condition.name)
        else:
            cb = tk.Checkbutton(self.window, text=condition.name, indicatoron=False, variable=condition.available)
            cb.bind('<Button-2>', lambda event: self.showPopupMenu(event, cb))
            cb.pack(side='top', fill='x')
            self.condition_dict[cb] = condition

    # 条件CheckButton的鼠标右键菜单
    def showPopupMenu(self, event, cb):
        menu = tk.Menu(self.root, tearoff=False)
        menu.add_command(label='edit', command=lambda: self.editCondition(cb))
        menu.add_command(label='delete', command=lambda: self.removeCondition(cb))
        menu.post(event.x_root, event.y_root)

    def editCondition(self, cb):
        condition = self.condition_dict[cb]
        condition_window = editconditionwindow.EditConditionDialog(self.root)
        condition_window.show(self.addCondition, condition, cb)

    def removeCondition(self, cb):
        del self.condition_dict[cb]
        cb.pack_forget()

    def showAddConditionDialog(self):
        condition_window = editconditionwindow.EditConditionDialog(self.root)
        condition_window.show(self.addCondition)

    def closeCallback(self):
        self.callback([])
        self.window.destroy()





