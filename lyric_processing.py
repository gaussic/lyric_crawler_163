# coding: utf-8

import os
import random
from collections import Counter


def open_file(filename, mode='r'):
    return open(filename, mode=mode, encoding='utf-8', errors='ignore')


def read_vocab(vocab_path):
    words = open_file(vocab_path).read().strip().split('\n')
    word_to_id = dict(zip(words, range(len(words))))
    return words, word_to_id


def build_vocab(data_path, vocab_path, vocab_size):
    tokens = ['<sos>', '<eos>', '<unk>']  # 词汇表中的几个重要标记
    all_words = open_file(data_path).read().strip().replace('\n', ' ').split()
    count_pairs = Counter(all_words).most_common(vocab_size)
    words, _ = list(zip(*count_pairs))
    tokens += words
    open_file(vocab_path, 'w').write('\n'.join(tokens) + '\n')


def text_to_id(text, w2id, unk_token):
    return [w2id[x] if x in w2id else unk_token for x in text.split()]


def id_to_text(ids, words):
    return ' '.join([words[x] for x in ids])


class Corpus(object):
    def __init__(self, data_path, vocab_path, vocab_size=10000):
        assert os.path.exists(data_path)

        if not os.path.exists(vocab_path):
            build_vocab(data_path, vocab_path, vocab_size - 3)

        self.words, self.word_to_id = read_vocab(vocab_path)

        self.tokenize(data_path)

    def tokenize(self, data_path):
        eos_token = self.word_to_id['<eos>']
        unk_token = self.word_to_id['<unk>']
        lines = []
        data = []
        for line in open_file(data_path):
            if len(line.strip()) == 0:
                data.extend(list(zip(lines[:-1], lines[1:])))
                lines = []
            line_ids = text_to_id(line + ' <eos>', self.word_to_id, unk_token)
            if line_ids.count(unk_token) < len(line_ids) * 0.2:
                lines.append(line_ids)

        # 打乱，分离数据集
        random.shuffle(data)
        data_len = len(data)
        self.data_train = data[:int(0.7 * data_len)]
        self.data_val = data[int(0.7 * data_len):int(0.8 * data_len)]
        self.data_test = data[int(0.8 * data_len):]

    def __repr__(self):
        return "Vocab size: {}\nTrain len: {}\nValidation len: {}\nTest len: {}".format(len(self.words),
                                                                                        len(self.data_train),
                                                                                        len(self.data_val),
                                                                                        len(self.data_test))


if __name__ == '__main__':
    corpus = Corpus('lyric_full.txt', 'lyric_vocab.txt')
    print(corpus)
    r_t = random.choice(corpus.data_train)
    print(id_to_text(r_t[0], corpus.words))
    print(id_to_text(r_t[1], corpus.words))
