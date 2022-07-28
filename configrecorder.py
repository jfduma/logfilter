import json
import tkinter as tk
from typing import List

from filterutils import Condition


def saveConditions(condition_list: List[Condition]):
    data_list = []
    for condi in condition_list:
        dict_condi = {'name': condi.name, 'include': condi.getIncludeKeys(), 'exclude': condi.getExcludeKeys()}
        data_list.append(dict_condi)
    jsonStr = json.dumps(data_list)

    filename = tk.filedialog.asksaveasfilename(title='保存条件',
                                               filetypes=[('JSON', '*.json')],
                                               defaultextension='.json',
                                               initialdir='/Users/jiangfeng/work/py/tk/sla/')
    if filename is not None and filename != '':
        with open(filename, 'w') as f:
            f.write(jsonStr)


def loadConditions(callback):
    filename = tk.filedialog.askopenfilename(title='载入条件',
                                             filetypes=[('JSON', '*.json')],
                                             defaultextension='.json',
                                             initialdir='/Users/jiangfeng/work/py/tk/sla/')
    if filename is None or filename == '':
        return None

    condition_list = []
    with open(filename) as f:
        for line in f:
            jsonData = json.loads(line)
            if jsonData is not None:
                for jsonItem in jsonData:
                    name = jsonItem['name']
                    if name is None or name == '':
                        continue
                    condition = Condition(name)
                    condition_list.append(condition)
                    includeList = jsonItem['include']
                    for key in includeList:
                        condition.addIncludeKey(key)
                    excludeList = jsonItem['exclude']
                    for key in excludeList:
                        condition.addExcludeKey(key)
    callback(condition_list)
