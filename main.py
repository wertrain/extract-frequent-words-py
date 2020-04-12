import sys
import os
import MeCab
import collections
import argparse
import json
import pickle
# MeCabリソースファイルへのパスを通す
#os.environ['MECABRC'] = r'.\etc\mecabrc'
os.environ['MECABRC'] = r'.\venv\Scripts\etc\mecabrc'

def pickle_dump(file, data):
    f = open(file, 'wb')
    pickle.dump(data, f)
    f.close()

def pickle_load(file):
    f = open(file, 'rb')
    data = pickle.load(f)
    f.close()
    return data

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("target", help="target file or text", type=str)
    parser.add_argument("--format", help="'text' or 'json'", type=str)
    parser.add_argument("--input", type=str)
    parser.add_argument("--output", type=str)
    args = parser.parse_args()

    text = args.target
    if (os.path.exists(args.target)):
        fileobj = open(args.target)
        text = fileobj.read()
        fileobj.close()

    mecab = MeCab.Tagger("-Ochasen")
    node = mecab.parseToNode(text)

    words = {}
    while node:
        nodes = node.feature.split(',')
        category = nodes[0]
        lemma = nodes[6]
        if not lemma == '*':
            if category in ['名詞', '動詞', '形容詞']:
                token = {
                    'category': category,
                    'lemma': lemma,
                    'count': 1
                }

                word_list = []
                new_word = True
                if (lemma in words):
                    word_list = words[lemma]
                    for item in word_list:
                        if category == item['category']:
                            item['count'] = item['count'] + 1
                            new_word = False
                            break
                if new_word:
                    word_list.append(token)
                    words[lemma] = word_list
        node = node.next

    # マージ
    if (args.input != None and os.path.exists(args.input)):
         data_list = pickle_load(args.input)
         for data in data_list:
            new_word = True
            word_list = []
            # 辞書に既に登録されているか調べる
            if (data['lemma'] in words):
                # 辞書にはリストで保存されている
                word_list = words[data['lemma']]
                for word in word_list:
                    # カテゴリが一致するなら同一と見なす
                    if data['category'] == word['category']:
                        word['count'] = data['count'] + word['count']
                        new_word = False
                        break
            if new_word:
                word_list.append(data)
                words[data['lemma']] = word_list
            
    result = []
    for word in list(words.values()):
        result.extend(word)

    if (args.format == 'json'):
        print(json.dumps (result))
    elif (args.format == 'text' or args.format == None):
        print(result)

    if (args.output != None):
        pickle_dump(args.output, result)

if __name__ == "__main__":
    # execute only if run as a script
    main()