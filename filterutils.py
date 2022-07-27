import tkinter as tk
from typing import List
import re


class StartLine:
    TAG_START = 0
    TAG_END = 1

    def __init__(self, line_num, start_time):
        self.line_num = line_num
        self.start_time = start_time


class Condition:

    def __init__(self, name):
        self.name = name
        self.available = tk.IntVar(value=0)
        # 包含数组为 &&，即：包含a且包含b
        self.includeCondition = []
        # 排除数组为 ||，即：不包含c或d
        self.excludeCondition = []

    def addIncludeKey(self, key):
        self.includeCondition.append(key)
        return self

    def addExcludeKey(self, key):
        self.excludeCondition.append(key)
        return self

    def getIncludePattern(self):
        if len(self.includeCondition) == 0:
            return None
        ptstr = '|'
        return re.compile(ptstr.join(self.includeCondition), re.IGNORECASE)

    def getExcludePattern(self):
        if len(self.excludeCondition) == 0:
            return None
        ptstr = '|'
        return re.compile(ptstr.join(self.excludeCondition), re.IGNORECASE)

    def getIncludeKeys(self):
        return self.includeCondition

    def getExcludeKeys(self):
        return self.excludeCondition


KEY_START = "init version: "
# 记录程序启动log的所在行
gl_start_list: [StartLine] = []


def filterFile(filename, condition: Condition, text):
    text.delete(0.0, tk.END)
    with open(filename) as f:
        for line in f:
            success = True
            incpatt = condition.getIncludeKeys()
            if incpatt is not None:
                for key in incpatt:
                    if 0 == len(re.findall(key, line, re.IGNORECASE)):
                        success = False
                        break

            if success:
                excpatt = condition.getExcludeKeys()
                if excpatt is not None:
                    for key in excpatt:
                        if len(re.findall(key, line, re.IGNORECASE)) > 0:
                            success = False
                            break

            if success:
                text.insert('insert', line)


def filterFile(filename, conditionlist: List[Condition], text):
    text.delete(0.0, tk.END)
    with open(filename, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            success = True
            for condition in conditionlist:
                if condition.available.get() == 0:
                    continue
                success = True
                incpatt = condition.getIncludeKeys()
                if incpatt is not None:
                    for key in incpatt:
                        if 0 == len(re.findall(key, line, re.IGNORECASE)):
                            success = False
                            break

                if success:
                    excpatt = condition.getExcludeKeys()
                    if excpatt is not None:
                        for key in excpatt:
                            if len(re.findall(key, line, re.IGNORECASE)) > 0:
                                success = False
                                break
                # conditionList中满足其中任意一个condition即可
                if success:
                    break

            if success:
                text.insert('insert', line)


def parseFile(filename):
    global gl_start_list
    start_list = gl_start_list
    line_num = 0
    lastline = ""
    recordfirst = True
    start_list.clear()
    # 07-21 18:00:07.121 -> [0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}\.[0-9]{3}
    timePattern = re.compile(r'[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}')
    with open(filename, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            line_num += 1
            # 记录程序启动起始点行号
            if len(re.findall(KEY_START, line)) > 0 or recordfirst:
                time = timePattern.findall(line)
                if time is not None and len(time) > 0:
                    recordfirst = False
                    start_list.append(StartLine(line_num, time[0]))
            lastline = line
        # 记录最后一行
        time = timePattern.findall(lastline)
        if time is None or len(time) == 0:
            time = ['???']
        start_list.append(StartLine(line_num, time[0]))

    return start_list


def filterFile(filename, startline, endline, conditionlist, callback):
    global gl_start_list

    linenum = 0
    with open(filename, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            linenum += 1
            if linenum < startline:
                continue
            if linenum > endline:
                break

            success = True
            for condition in conditionlist:
                if condition.available.get() == 0:
                    continue
                success = True
                incpatt = condition.getIncludeKeys()
                if incpatt is not None:
                    for key in incpatt:
                        if 0 == len(re.findall(key, line, re.IGNORECASE)):
                            success = False
                            break

                if success:
                    excpatt = condition.getExcludeKeys()
                    if excpatt is not None:
                        for key in excpatt:
                            if len(re.findall(key, line, re.IGNORECASE)) > 0:
                                success = False
                                break
                # conditionList中满足其中任意一个condition即可
                if success:
                    break

            if success:
                callback(line)
