import tkinter as tk
from typing import List
import re


class Condition:

    def __init__(self):
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
    with open(filename) as f:
        for line in f:
            success = True
            for condition in conditionlist:
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
