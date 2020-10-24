
# ./NN4IR -config config.ini > NN4IR.log &
./NN4IR -config config.ini

#note that NN4IR.log will produce the test result, for rob04-title, the test result will be: MAP:0.2805, nDCG@20:0.4369, P@20: 0.3863.
# tail -f -n 1000 NN4IR.log


## evaluation of the ranklist
#./trec_eval ./rob04-title/qrels.rob04.txt DRMM-LCH-IDF-rob04-title.ranklist -m all_trec

