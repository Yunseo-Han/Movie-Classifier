import math
from wordcounter import WordCounter
from preprocess import pre_process


def mutual_info(_fxy, _N, _fx, _fy):
    """
    Calculate mutual information.
    """
    a = _fxy * _N / (_fx * _fy)
    m_info = math.log(a, 2)
    return m_info


def print_result(alist, pos_or_neg):
    flag = 'P' if pos_or_neg == 'positive' else 'N'
    print(f"The top 5 {pos_or_neg} words:")
    counter = 1
    for word, mi in alist:
        print(f"{flag}{counter}:  {word}")
        counter += 1


def output_result(alist, pos_or_neg):
    flag = 'P' if pos_or_neg == 'positive' else 'N'
    counter = 1
    with open('output.txt', 'a') as f:
        f.writelines(f"\nThe top 5 {pos_or_neg} words:")
        for key, value in alist:
            f.write('\n')
            f.write(f"{flag}{counter}:  {key}")
            counter += 1


def main():
    pre_process()

    test = WordCounter("./pos_train.csv", "./neg_train.csv")
    test.prepare_data()

    mi_dict_pos = {}
    for word in test.vocab:
        if test.pos_dict.get(word) is None:
            continue
        else:
            fxy = test.pos_dict.get(word)

        N = test.neg_review_num + test.pos_review_num
        fx = test.freq_dict.get(word)
        fy = test.pos_review_num
        mi = mutual_info(fxy, N, fx, fy)
        mi_dict_pos.update({word: mi})

    # sort words based on MI value
    mi_list_pos = sorted(mi_dict_pos.items(), key=lambda x: x[1], reverse=True)
    # filter out the words with MI = 1.0
    mi_list = list(filter(lambda x: x[1]<1, mi_list_pos))

    top_pos = mi_list[:5]
    print_result(top_pos, 'positive')
    output_result(top_pos, 'positive')

    top_neg = mi_list[-5:]
    print_result(top_neg, 'negative')
    output_result(top_neg, 'negative')


if __name__ == '__main__':
    main()
