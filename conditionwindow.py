import tkinter as tk


class ConditionDialog:

    def __init__(self, root):
        self.root = root

    def show(self):
        top = tk.Toplevel(self.root)
        top.title("add condition")
        top.geometry('530x280+400+200')

        # OK Cancel按钮
        frame_bottom = tk.Frame(top)
        frame_bottom.pack(side='bottom', fill='x')
        btn_ok = tk.Button(frame_bottom, text='OK').pack(side='right')
        btn_cancel = tk.Button(frame_bottom, text='Cancel', command=top.destroy).pack(side='left')

        # 左侧 包含条件
        frame_inc = tk.Frame(top)
        frame_inc.pack(side='left', fill='both')
        frame_label_inc = tk.Frame(frame_inc)
        frame_label_inc.pack(side='top', fill='x')
        label_inc = tk.Label(frame_label_inc, text='包含关键字：').pack(side='left')

        frame_inc_top = tk.Frame(frame_inc)
        frame_inc_top.pack(side='top', fill='x')
        btn_del_inc = tk.Button(frame_inc_top, text='-').pack(side='left')
        space_inc = tk.Frame(frame_inc_top, width=15).pack(side='left')
        btn_add_inc = tk.Button(frame_inc_top, text='+', command=self.addIncludeKeyword).pack(side='right')
        self.entry_inc = tk.Entry(frame_inc_top, width=15)
        self.entry_inc.bind('<Return>', self.addIncludeKeywordByEnterKey)
        self.entry_inc.pack(side='right')
        self.box_inc = tk.Listbox(frame_inc)
        self.box_inc.pack(fill='both')

        # 右侧 不包含条件
        frame_exc = tk.Frame(top)
        frame_exc.pack(side='right', fill='both')
        frame_label_exc = tk.Frame(frame_exc)
        frame_label_exc.pack(side='top', fill='x')
        label_exc = tk.Label(frame_label_exc, text='不包含关键字：').pack(side='left')

        frame_exc_top = tk.Frame(frame_exc)
        frame_exc_top.pack(side='top', fill='x')
        btn_del_exc = tk.Button(frame_exc_top, text='-').pack(side='left')
        space_exc = tk.Frame(frame_exc_top, width=15).pack(side='left')
        btn_add_exc = tk.Button(frame_exc_top, text='+', command=self.addExcludeKeyword).pack(side='right')
        self.entry_exc = tk.Entry(frame_exc_top, width=15)
        self.entry_exc.bind('<Return>', self.addExcludeKeywordByEnterKey)
        self.entry_exc.pack(side='right')
        self.box_exc = tk.Listbox(frame_exc)
        self.box_exc.pack(fill='both')

    def addIncludeKeywordByEnterKey(self, event):
        self.addIncludeKeyword()

    def addIncludeKeyword(self):
        keyword = self.entry_inc.get()
        self.box_inc.insert('end', keyword)
        self.entry_inc.delete(0, len(keyword))

    def addExcludeKeywordByEnterKey(self, event):
        self.addExcludeKeyword()

    def addExcludeKeyword(self):
        keyword = self.entry_exc.get()
        self.box_exc.insert('end', keyword)
        self.entry_exc.delete(0, len(keyword))

    def removeIncludeKeyword(self):
        selected = self.box_inc.curselection()
        for index in selected:
            self.box_inc.delete(index, index)

    def removeExcludeKeyword(self):
        pass