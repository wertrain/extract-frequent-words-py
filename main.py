import sys
import os
import MeCab
import collections
import argparse
# MeCabリソースファイルへのパスを通す
os.environ['MECABRC'] = r'.\venv\Scripts\etc\mecabrc'

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("file", help="target file path", type=str)
    parser.add_argument("--output", type=str)
    args = parser.parse_args()
    print (args)

    if(not os.path.exists(args.file)):
        sys.exit(1)

    fileobj = open(args.file)
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

if __name__ == "__main__":
    # execute only if run as a script
    main()
