#  Hint:  You may not need all of these.  Remove the unused functions.
from hashtables import (HashTable,
                        hash_table_insert,
                        hash_table_retrieve)


def get_indices_of_item_weights(weights, length, limit):
    ht = HashTable(length)

    for i in range(len(weights)):
        hash_table_insert(ht, weights[i], i)

    answer = None

    for w in range(len(weights)):
        weight = weights[w]
        secondWeight = hash_table_retrieve(ht, limit - weight)
        if secondWeight is not None and secondWeight is not w:
            if w < secondWeight:
                answer = (secondWeight, w)
            else:
                answer = (w, secondWeight)

    return answer


def print_answer(answer):
    if answer is not None:
        print(str(answer[0]) + " " + str(answer[1]))
    else:
        print("None")
