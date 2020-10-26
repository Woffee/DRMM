"""


@Time    : 10/24/20
@Author  : Wenbo
"""

from nltk.tokenize import word_tokenize
import string
import os
from gensim.models import Word2Vec


# text = "God is Great! I won a lottery."
# print(word_tokenize(text))
# Output: ['God', 'is', 'Great', '!', 'I', 'won', 'a', 'lottery', '.']

"""
1 统计所有文档的单词
2 用 kstem 预处理每个单词，保存到一个文件里

./kstem /Users/woffee/www/emse-apiqa/baselines2/DRMM/Ebay/doc_tokens.txt >>  /Users/woffee/www/emse-apiqa/baselines2/DRMM/Ebay/doc_tokens_stemmed.txt
"""
def remove_punc(s):
    return s.translate(str.maketrans('', '', string.punctuation))

def get_all_tokens(filepath, to_file):
    if os.path.exists(to_file):
        print("File exists: ", to_file)
        return

    tokens = []
    ii = 0
    with open(filepath, "r") as f:
        for line in f.readlines():
            l = line.strip().lower()
            print("now %d" % ii)
            if l != "":
                l = remove_punc(l)
                words = word_tokenize(l)
                for w in words:
                    if len(w)<70 and w not in tokens:
                        tokens.append(w)
            ii += 1
    with open(to_file, "w") as f:
        for w in tokens:
            f.write(w+"\n")
    print("wrote all tokens to:", to_file)


"""
3 生成 document data file
"""
def get_doc_file(doc_filepath, doc_tokens_filepath, to_file):
    if os.path.exists(to_file):
        print("File exists: ", to_file)
        return

    dic_stem = {}
    with open(doc_tokens_filepath, "r") as f:
        for line in f.readlines():
            l = line.strip().lower()
            if l != "":
                arr = l.split(" ")
                dic_stem[ arr[0] ] = arr[1]

    lines = []
    with open(doc_filepath, "r") as f:
        lines = f.readlines()

    with open(to_file, "w") as f:
        ii = 1
        for line in lines:
            print("output now %d" % ii)
            doc = line.strip().lower()
            if doc != "":
                doc_id = "DOC-%d" % ii
                doc = remove_punc(doc)
                words = word_tokenize(doc)
                total = len(words)

                details = []
                words_count = {}
                for w in words:
                    if len(w)<70:
                        w2 = dic_stem[w]
                        if w2 in words_count.keys():
                            words_count[w2] += 1
                        else:
                            words_count[w2] = 1

                for w in words_count.keys():
                    details.append("%s:%d" % (w, words_count[w]) )

                str = "%s\t%d\t%s\n" % (doc_id, total, " ".join(details))
                f.write(str)
                ii = ii + 1
    print("saved to " + to_file)




"""
4 生成 df(document frequency) and cf(corpus frequence)

只有df被用到了。
"""
def get_df_cf(docset_file, to_file):
    if os.path.exists(to_file):
        print("File exists: ", to_file)
        return

    with open(docset_file, "r") as f:
        lines = f.readlines()

    words_df = {}
    # words_cf = {}

    for line in lines:
        line = line.strip()
        if line != "":
            arr = line.split("\t")
            details = arr[2].split(" ")
            for d in details:
                word, cnt = d.split(":")

                if word not in words_df.keys():
                    words_df[word] = 1
                else:
                    words_df[word] += 1
    with open(to_file, "w") as f:
        for w in words_df.keys():
            f.write("%s\t%d\t%d\n" % (w, words_df[w], words_df[w]))
    print("saved to " + to_file)
    return

"""
query files

./kstem /Users/woffee/www/emse-apiqa/baselines2/DRMM/Ebay/query_tokens.txt >>  /Users/woffee/www/emse-apiqa/baselines2/DRMM/Ebay/query_tokens_stemmed.txt
"""

def get_query_tokens(qa_file, to_file):
    if os.path.exists(to_file):
        print("File exists: ", to_file)
        return

    with open(qa_file, "r") as f:
        lines = f.readlines()

    tokens = []

    for i,line in enumerate(lines):
        line = line.strip().lower()
        if line != "":
            if i % 2 == 0:
                l = remove_punc(line)
                words = word_tokenize(l)
                for w in words:
                    if len(w) < 70 and w not in tokens:
                        tokens.append(w)

    with open(to_file, "w") as f:
        for w in tokens:
            f.write(w+"\n")
    print("saved to:", to_file)


def get_query_data(qa_file, doc_tokens_stemed_file, to_file):
    if os.path.exists(to_file):
        print("File exists: ", to_file)
        return

    dic_stem = {}
    with open(doc_tokens_stemed_file, "r") as f:
        for line in f.readlines():
            l = line.strip().lower()
            if l != "":
                arr = l.split(" ")
                dic_stem[arr[0]] = arr[1]

    with open(qa_file, "r") as f:
        lines = f.readlines()

    ii = 1
    with open(to_file, "w") as f:
        for i, line in enumerate(lines):
            line = line.strip().lower()
            if line != "" and i % 2 == 0:
                line = remove_punc(line)
                words = word_tokenize(line)
                to_words = []
                for w in words:
                    if len(w)<70 and w not in to_words:
                        to_words.append(dic_stem[w])
                f.write("%d\t%s\n" % (ii, "\t".join(to_words)))
                ii += 1

    print("saved to " + to_file)

"""
4. get init rank data
"""
def get_init_rankdata(qa_file, to_file, total_doc):
    if os.path.exists(to_file):
        print("File exists: ", to_file)
        return

    with open(qa_file, "r") as f:
        lines = f.readlines()

    ii = 1
    with open(to_file, "w") as f:
        for i, line in enumerate(lines):
            line = line.strip().lower()
            if line != "" :
                if i%2 ==1:
                    doc_ids = line.split(" ")
                    j = 1
                    for id in doc_ids:
                        id = id.strip()
                        if id != "":
                            f.write("%d Q0 DOC-%s %d 1.0 init\n" % (ii, id, j))
                            j += 1
                    for id in range(1, total_doc+1):
                        if str(id) not in doc_ids:
                            f.write("%d Q0 DOC-%s %d 0.0 init\n" % (ii, id, j))
                            j += 1
                    ii += 1

    print("saved to " + to_file)

"""
5. qrel
"""
def get_doc_count(doc_file):
    lines = []
    with open(doc_file, "r") as f:
        lines = f.readlines()
    res = 0
    for line in lines:
        if line.strip() != "":
            res += 1
    return res

def get_qrel_data(qa_file, to_file, total_doc):
    if os.path.exists(to_file):
        print("File exists: ", to_file)
        return

    with open(qa_file, "r") as f:
        lines = f.readlines()

    qid = 1
    with open(to_file, "w") as f:
        for i, line in enumerate(lines):
            line = line.strip().lower()
            if line != "" :
                if i%2 ==1:
                    arr = line.split(" ")
                    ids = []
                    for row in arr:
                        row = row.strip()
                        if row!="":
                            ids.append( int(row) )

                    for doc_ii in range(1,total_doc+1):
                        if doc_ii in ids:
                            f.write("%d 0 DOC-%d 1\n" % (qid, doc_ii))
                        else:
                            f.write("%d 0 DOC-%d 0\n" % (qid, doc_ii))
                    qid += 1

    print("saved to " + to_file)

"""
6. qrel_idcg
"""

def get_qrel_idcg(qa_file, to_file):
    if os.path.exists(to_file):
        print("File exists: ", to_file)
        return

    with open(qa_file, "r") as f:
        lines = f.readlines()

    qid = 1
    with open(to_file, "w") as f:
        for i, line in enumerate(lines):
            line = line.strip().lower()
            if line != "" :
                if i%2 ==0:
                    f.write("%d\t1.0\n" % qid)
                    qid += 1


    print("saved to " + to_file)


def get_embeddings(data_type, qa_file, doc_file, query_tokens_stemmed_file, doc_tokens_stemed_file):
    corpus = []

    dic_stem = {}
    with open(doc_tokens_stemed_file, "r") as f:
        for line in f.readlines():
            l = line.strip().lower()
            if l != "":
                arr = l.split(" ")
                dic_stem[arr[0]] = arr[1]

    with open(query_tokens_stemmed_file, "r") as f:
        for line in f.readlines():
            l = line.strip().lower()
            if l != "":
                arr = l.split(" ")
                dic_stem[arr[0]] = arr[1]

    with open(qa_file, "r") as f:
        lines = f.readlines()
        for i, line in enumerate(lines):
            line = line.strip().lower()
            if line != "" and i % 2 == 0:
                line = remove_punc(line)
                words = word_tokenize(line)
                to_words = []
                for w in words:
                    if len(w) < 70:
                        to_words.append(dic_stem[w])
                corpus.append(to_words)

    with open(doc_file, "r") as f:
        lines = f.readlines()
        for i, line in enumerate(lines):
            line = line.strip().lower()
            if line != "":
                line = remove_punc(line)
                words = word_tokenize(line)
                to_words = []
                for w in words:
                    if len(w) < 70:
                        to_words.append(dic_stem[w])
                corpus.append(to_words)


    data_type = data_type.lower()
    min_count = 1
    size = 300
    window = 10
    negative = 10
    sg = 0

    w2v_model = Word2Vec(corpus,
                         min_count=min_count,
                         size=size,
                         window=window,
                         negative=negative,
                         sg = sg)
    to_file = "wordembedding/%s.wv.cbow.d%d.w%d.n%d.bin" % (data_type, size, window,negative)
    w2v_model.wv.save_word2vec_format(to_file, binary=True)

if __name__ == '__main__':
    type = "adwords"

    doc_file = type + "/Doc_list.txt"
    doc_tokens_file = type + "/doc_tokens.txt"
    doc_tokens_stemed_file = type + "/doc_tokens_stemmed.txt"
    docset_file = type + "/docset.txt"
    dfcf_file = type + "/dfcf.txt"

    qa_file = type + "/QA_list.txt"
    query_tokens_file = type + "/query_tokens.txt"
    query_tokens_stemmed_file = type + "/query_tokens_stemmed.txt"
    query_file = type + "/query.txt"

    init_rankdata_file = type + "/initrank.txt"
    qrel_file=type + "/qrel.txt"
    qrel_idcg_file=type + "/qrel.idcg.txt"

    total_doc = get_doc_count(doc_file)


    # 1.
    get_all_tokens(filepath=doc_file, to_file=doc_tokens_file)

    kstem = "/Users/woffee/www/emse-apiqa/baselines2/DRMM/KrovetzStemmer-3.4/c++/kstem"
    cmd = "%s %s >> %s" % (kstem, doc_tokens_file, doc_tokens_stemed_file)
    os.system(cmd)

    get_doc_file(doc_file, doc_tokens_stemed_file, docset_file)

    # 2. df and cf
    get_df_cf(docset_file, dfcf_file)

    # 3.
    get_query_tokens(qa_file, query_tokens_file)
    cmd = "%s %s >> %s" % (kstem, query_tokens_file, query_tokens_stemmed_file)
    os.system(cmd)
    get_query_data(qa_file, query_tokens_stemmed_file, query_file)

    # 4.
    get_init_rankdata(qa_file, init_rankdata_file, total_doc)

    # 5.
    get_qrel_data(qa_file, qrel_file, total_doc)

    # 6.
    get_qrel_idcg(qa_file, qrel_idcg_file)

    # 7. embeddings
    get_embeddings(type, qa_file, doc_file, query_tokens_stemmed_file, doc_tokens_stemed_file)