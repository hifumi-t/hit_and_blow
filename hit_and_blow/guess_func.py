import random
from typing import Tuple
# hit and blow の判定用関数
def hit_blow(guess, answer):
    hit = 0
    blow = 0
    for i in range(5):
        if guess[i] == answer[i]:
            hit += 1
        elif guess[i] in answer:
                blow += 1
    return {"guess":guess, "hit":hit, "blow":blow}

def make_init1(num_list, answer, guess="", cost=0):
    # まずランダムに数字を入れて, hit:0, blow:0の状況にする
    while True:
        # num_listをシャッフルして, 先頭5文字をguessとして利用
        random.shuffle(num_list)
        guess = "".join(map(str, num_list[0:5]))
        # postして
        info = hit_blow(guess, answer)
        cost+=1
        # getした情報がhit:0, blow:0 なら, 推測に移行
        if info["hit"] == 0 and info["blow"] == 0:
            print("~~~ 推測スタート ~~~\n正解:", answer, "\n初期数列:", guess, info, "\n<0番目の数字を探索>\n候補", num_list[5:])
            break
    return(guess, cost)

# 推測スタート
# blowを完全無視した方法
def guess_func1(num_list, guess, answer, cost=0):
    for i, num in enumerate(guess):
        for j in range(5,16):
            # 愚直に候補の数字を入れていく
            guess1 = guess.replace(num, num_list[j])
            # postして
            info = hit_blow(guess1, answer)
            cost+=1
            # getの結果, hit:+1 されていたら
            if info["hit"] == i+1:
                # guessを更新して
                guess = guess.replace(num, num_list[j])
                # 候補の数字リストからhitした数字を消す
                num_list.pop(j)
                if i < 4:
                    print(guess, "{'hit': "+str(i+1)+", 'blow': 0}\n<"+str(i+1)+"番目の数字を探索>\n候補", num_list[5:])
                else:
                    print(guess, "{'hit': "+str(i+1)+", 'blow': 0}")
                break
            else: 
                print(guess1)
    return(guess, cost)


def make_init2(answer) -> list:
    num_list = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "a", "b", "c", "d", "e", "f"]
    guess=""
    memo=[]
    for i in range(0,11,5): #5個ずらし
        guess = "".join(map(str, num_list[i:i+5]))
        # post, getして
        info = hit_blow(guess, answer)
        print("初期数列作成", info)
        memo.append(info)
    return(memo)

def guess_func2(memo, answer) -> Tuple:
    init_hit=0
    init_blow=0
    cost=0
    hit_list=[[] for _ in range(5)]
    blow_list=[]
    for info in memo:
        init_hit += info["hit"]
        init_blow += info["blow"]

    # fはもう考えなくていい場合
    if init_hit + init_blow == 5:
        print("fが答えにない場合です")
        for dicts in memo:
            for j in range(5):
                guess = dicts["guess"].replace(dicts["guess"][j], "f") # 絶対に当たらないfを入れて検証
                # post, get
                info = hit_blow(guess, answer)
                cost+=1
                print(info)
                # 条件でhitとblowの数字を発見して格納
                if info["hit"] == dicts["hit"] - 1:
                    hit_list[j] = dicts["guess"][j]
                elif info["blow"] == dicts["blow"] - 1:
                    blow_list.append(dicts["guess"][j])
                else:
                    pass
        print(hit_list, blow_list)
    # fは答えの中にある場合
    else:
        print("fが答えにある場合です")
        for dicts in memo:
            for j in range(5):
                guess = dicts["guess"].replace(dicts["guess"][j], "f") # 基本blow, たまにhitするfを入れて検証
                # post, get
                info = hit_blow(guess, answer)
                cost+=1
                print(info)
                # 条件でhitとblowの数字を発見して格納
                if info["hit"] == dicts["hit"] - 1:
                    hit_list[j] = dicts["guess"][j]
                elif info["hit"] == dicts["hit"] + 1:    # fがhitして
                    hit_list[j] = "f"
                    if info["blow"] == dicts["blow"] - 1:   #blowが一つ消えたら
                        blow_list.append(dicts["guess"][j])
                    else:
                        pass
                elif info["blow"] == dicts["blow"]:
                    blow_list.append(dicts["guess"][j])
                else:
                    pass
        print(hit_list, blow_list)

    # hitとblowの数字を探し終わって
    # hit_listに[]があれば（ほぼこっちになるはず）
    if [] in hit_list:
        ind = [i for i, x in enumerate(hit_list) if x == [] ]   #hit_listの[]を見つける
        while True:
            random.shuffle(blow_list)   # この並び替え -> 改善の余地あり
            for j in range(len(blow_list)):
                hit_list[ind[j]] = blow_list[j]
            # post, get
            info = hit_blow(hit_list, answer)
            cost+=1
            print(info)
            if info["hit"] == 5:
                final_guess = "".join(map(str, hit_list))
                return(final_guess, cost)
    # もうhit＿listが埋まっていれば
    else:
        final_guess = "".join(map(str, hit_list))
        return(final_guess, cost)

# アルゴリズム１
# def main():
#     answer = "2de5a"
#     num_list = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "a", "b", "c", "d", "e", "f"]
#     init_guess, cost1 = make_init1(num_list, answer)
#     final_guess, cost2 = guess_func1(num_list, init_guess, answer)
#     print("~~~ 結果 ~~~\n試行回数:", cost1+cost2, "{ 推測結果:", final_guess, ",  正解:", answer, "}")
# if __name__ == "__main__":
#     main()

# アルゴリズム２
answer = "2de5a"
num_list = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "a", "b", "c", "d", "e", "f"]
init_num = make_init2(num_list)
guess_func2(init_num, answer)
# memo  5blowだとシャッフルで300かかることもある...