"""


@Time    : 10/25/20
@Author  : Wenbo
"""

def calc_auc(initrank_file, pred_file):
    # read ground truth file
    q_answers = {}
    with open(initrank_file, "r") as f:
        lines = f.readlines()

        for line in lines:
            line = line.strip()
            if line == "":
                continue

            arr = line.split(" ")
            qid = arr[0]
            did = arr[2]
            groud_truth = arr[4]
            if groud_truth == "1.0":
                if qid in q_answers.keys():
                    q_answers[qid].append(did)
                else:
                    q_answers[qid] = [did]

    # read pred file
    q_pred = {}
    with open(pred_file, "r") as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip()
            if line == "":
                continue

            arr = line.split("\t")
            qid = arr[0]
            did = arr[2]
            rank = int(arr[3])
            if qid in q_pred.keys():
                q_pred[qid].append( [did, rank] )
            else:
                q_pred[qid] = [ [did, rank] ]

    # auc
    ss = 0
    delta = 0
    for qid in q_pred.keys():
        tp = 0 # True Positive
        tn = 0 # True Negative
        fp = 0 # False Positive
        fn = 0 # False Negative

        ans = q_answers[qid]
        cnt = len(ans)
        for did, rank in q_pred[qid]:
            if did in ans:
                if rank < cnt:
                    tp += 1
                else:
                    fp += 1
            else:
                if rank < cnt:
                    fn += 1
                else:
                    tn += 1

        if tp + tn == 0:
            ss += 0
        elif fp + fn ==0:
            ss += 1
        else:
            ss += 1.0 / ( (tp + tn) * (fp + fn) )

        print("qid: %s  -  tp:%d, tn:%d , fp:%d, fn:%d" %(qid, tp, tn, fp, fn))
        if tp > 0:
            delta += 1
    auc = ss * delta / len(q_pred.keys())
    print("=== Evaluation results ===")
    print("Prediction file:",pred_file)
    # print("len(pred.keys):", len(q_pred.keys()))
    print("delta =", delta)
    print("auc =", auc)
    return auc


if __name__ == '__main__':
    initrank_file = "ebay/initrank.txt"
    pred_file = "DRMM-LCH-IDF-ebay.ranklist"

    calc_auc(initrank_file, pred_file)