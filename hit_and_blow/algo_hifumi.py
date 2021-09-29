from matplotlib import pyplot as plt
import itertools
import random
import numpy as np
num_list = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "a", "b", "c", "d", "e", "f"]

def hit_blow(guess, answer):
    hit = 0
    blow = 0
    for i in range(5):
        if guess[i] == answer[i]:
            hit += 1
        elif guess[i] in answer:
                blow += 1
    return [hit, blow]

def make_ans_list(num_list):
    ans_list_tuple = list(itertools.permutations(num_list, 5))
    ans_list = []
    for i in ans_list_tuple:
        ans_list.append(i[0]+i[1]+i[2]+i[3]+i[4])
    return ans_list

def narrow_ans_list(guess, result, ans_list):
    new_ans_list = []
    length = len(ans_list)
    for ans in ans_list[:length+1]:
        h_b = hit_blow(guess, ans)
        if h_b == result: # もし3hit 2blowなら
            new_ans_list.append(ans) # 候補リストに加える
        else: # 3hit 2blowじゃないなら
            pass # なにもしない
    ans_list = new_ans_list # できた正解候補をもとのリストと置き換える
    return ans_list


# 実行してみる
ans = random.sample(num_list, 5) # 答えをランダムに決める
ans = ans[0]+ans[1]+ans[2]+ans[3]+ans[4]
print(f"正解は{ans}")
print("----------------------")
guess = "12345" # 初期予測（適当）

ans_list = make_ans_list(num_list) # いったん全候補をリストにぶちこむ
count = 0
while True:
    count += 1
    result = hit_blow(guess, ans)
    ans_list = narrow_ans_list(guess, result, ans_list)
    print(guess + "と予想して残り" + str(len(ans_list)) + "パターン" + "---------" + "{}hit{}blow".format(result[0],result[1]))
    guess = ans_list[0] # 正解候補の中から適当に（とりあえず最初の項）次の予測を決める
    if result == [5, 0]:
        break

print("----------------------")
print(f"{count}回で正解！")


# めっちゃ実行する(100回やるのに2分くらいかかった...)
# count_list = []
# for i in range(100):
#     ans = random.sample(num_list, 5) # 答えをランダムに決める
#     ans = ans[0]+ans[1]+ans[2]+ans[3]+ans[4]
#     guess = "12345" # 初期予測（適当）

#     ans_list = make_ans_list(num_list) # いったん全候補をリストにぶちこむ
#     count = 0
#     while True:
#         count += 1
#         result = hit_blow(guess, ans)
#         ans_list = narrow_ans_list(guess, result, ans_list)
#         guess = ans_list[0] # 正解候補の中から適当に（とりあえず最初の項）次の予測を決める
#         if result == [5, 0]:
#             break
#     count_list.append(count)


# # 後処理
# print(np.mean(count_list))
# print(np.std(count_list))
# plt.hist(count_list)