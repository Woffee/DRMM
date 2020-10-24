from gensim.models.keyedvectors import KeyedVectors

model = KeyedVectors.load_word2vec_format('wordembedding/rob04.wv.cbow.d300.w10.n10.m10.i10.W.bin', binary=True)

# 转换成 txt 格式
model.save_word2vec_format('wordembedding/rob04.wv.cbow.d300.w10.n10.m10.i10.W.txt', binary=False)

# 另存为 bin 文件
model.save_word2vec_format('wordembedding/rob04.wv.cbow.d300.w10.n10.m10.i10.W22.bin', binary=True)