import random
# hit and blow の判定用関数
def hit_blow(guess, answer):
    hit = 0
    blow = 0
    for i in range(5):
        if guess[i] == answer[i]:
            hit += 1
        elif guess[i] in answer:
                blow += 1
    return {"hit":hit, "blow":blow}

def make_init(num_list, answer, guess="", cost=0):
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
def guess_func(num_list, guess, answer, cost=0):
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

def main():
    answer = "2de5a"
    num_list = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "a", "b", "c", "d", "e", "f"]
    init_guess, cost1 = make_init(num_list, answer)
    final_guess, cost2 = guess_func(num_list, init_guess, answer)
    print("~~~ 結果 ~~~\n試行回数:", cost1+cost2, "{ 推測結果:", final_guess, ",  正解:", answer, "}")

if __name__ == "__main__":
    main()