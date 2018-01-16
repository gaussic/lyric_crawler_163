# coding: utf-8

import re
import os
import shutil

base_dir = "data"
new_dir = "data_clean"
if os.path.exists(new_dir):
    shutil.rmtree(new_dir)
os.mkdir(new_dir)


def open_file(filename, mode='r'):
    return open(filename, mode=mode, encoding='utf-8', errors='ignore')


def is_chinese(text):
    text = ''.join([x.strip() for x in text.split('\n')])
    res = ' '.join([r for r in re.findall(r"[\u4e00-\u9fa5]+", text)])  # 中文字符区间
    return len(res) >= 0.8 * len(text)  # 8成以上是中文


def clean_text(filename):
    text = open_file(filename).read()
    text = re.sub(r"\[.*\]", "", text)  # 过滤时间轴
    text = re.sub(r"作词.*\n", "", text)  # 过滤掉工作人员
    text = re.sub(r"作曲.*\n", "", text)
    text = re.sub(r"编曲.*\n", "", text)
    text = re.sub(r"演唱.*\n", "", text)
    text = re.sub(r"制作人.*\n", "", text).strip()
    return text


cnt = 0
for cur_dir in os.walk(base_dir):  # 遍历所有文档
    for filename in cur_dir[2]:
        try:
            file_dir = os.path.join(cur_dir[0], filename)
            data = clean_text(file_dir)
            if is_chinese(data) and len(data) >= 200:  # 中文，200字符以上
                open_file(os.path.join(new_dir, str(cnt) + ' - ' + filename), 'w').write(data)  # 汇总写入新目录
                cnt += 1  # 防止重名，打个编号
        except:
            pass
