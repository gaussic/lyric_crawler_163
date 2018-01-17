# coding: utf-8

import os
import jieba

jieba.enable_parallel(10)  # 并行分词

base_dir = 'data_unique'


def open_file(filename, mode='r'):
    return open(filename, mode=mode, encoding='utf-8', errors='ignore')


def lyric_group():
    lyric_full = open_file('lyric_full.txt', 'w')
    for fname in sorted(os.listdir(base_dir)):
        data = open_file(os.path.join(base_dir, fname)).readlines()
        if len(data) <= 6:  # 歌词太短，不要
            continue
        lyric = []
        for line in data[3:-3]:  # 前3行后三行都不要
            cur_line = list(jieba.cut(line.strip().lower()))
            if len(cur_line) >= 30:  # 太长不要
                continue
            lyric.extend(' '.join(cur_line).split())
            if len(lyric) >= 5:
                lyric_full.write(' '.join(lyric) + '\n')
                lyric = []
        lyric_full.write('\n')  # 每首歌词用空行隔开

    lyric_full.close()
