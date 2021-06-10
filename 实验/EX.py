from collections import defaultdict

article = []
infer = defaultdict(list)
this_ender = set()
ender = ['$', 'id', 'a', 'b', 'c', '+', "-", '*', '/', '%', '==', '!=', '<', '>', '<=', '>=', '!', '&&', '||', 'i', '_',
         "(", ')', '[', ']', 'a', 'b', 'c']
First = defaultdict(set)
empty_flag = defaultdict(int)
include_follow = defaultdict(set)
followed = defaultdict(set)
predict_table = {}
Follow = defaultdict(set)
not_ender = set()
left_index = 0
empty_set = set()
Select = defaultdict(set)


def first(start):
    lis = set()
    if start in infer:
        for nexts in infer[start]:
            if nexts[0] in ender:  # 找到了终结符
                th = set()
                th.add(nexts[0])
                First[nexts[0]] = th
                lis.add(nexts[0])
            else:
                # 没找到终结符
                for index in range(len(nexts)):
                    d = first(nexts[index])
                    if '_' not in d:  # 不能推出空
                        lis = lis | d
                        break
                    else:
                        for data in d:
                            if d != '_':
                                lis = lis | d
    First[start] = First[start] | lis
    return lis


# 判断某个单词能不能推出空
def judge_empty(words) -> bool:
    for word in words:
        if word in ender and word != '_':
            return False
        elif word not in ender:
            if not infer_empty(word):
                return False
    return True


# 判断某行的文法是不是能推出空
def infer_empty(start) -> bool:
    if start not in infer:
        return
    for nexts in infer[start]:
        if judge_empty(nexts):
            return True
    return False


def who_follow(start):
    for nexts in infer[start]:
        if nexts[-1] in ender:
            return
        include_follow[nexts[-1]].add(start)
        for index in range(len(nexts) - 2, -1, -1):
            if infer_empty(nexts[index + 1]) == True:
                include_follow[nexts[index]].add(start)
            else:
                break


def topo_sort() -> list:  # 拓扑排序，求出follow包含的follow
    lis = []

    for key in include_follow:
        if key in include_follow[key]:
            include_follow[key].discard(key)
    while len(lis) != len(infer):
        for key in infer:
            if (key not in include_follow or len(include_follow[key]) == 0) and key not in lis:
                lis.append(key)
                for key2 in infer:
                    if key2 in include_follow and key in include_follow[key2]:
                        include_follow[key2].discard(key)
                if key in include_follow:
                    del include_follow[key]
    return lis


def follow():
    flag = 0
    for key in infer:
        if flag == 0:
            Follow[key] = set('$')
        flag = 1
        for nexts in infer[key]:
            for index in range(len(nexts) - 2, -1, -1):
                if nexts[index] not in ender:
                    if nexts[index + 1] in ender:
                        Follow[nexts[index]] = Follow[nexts[index]] | set(nexts[index + 1])
                    else:
                        Follow[nexts[index]] = Follow[nexts[index]] | First[nexts[index + 1]]


def findleftrecrusion(key):
    flag = 0
    for nexts in infer[key]:
        if nexts[0] == key:  # 左递归存在
            s1 = []
            s2 = []
            s1, s2 = del_leftrecursion(key)
            infer[key] = s1
            infer[key + "'"] = s2
            flag = 1
    while (flag == 1):
        flag = 0
        for nexts in infer[key]:
            if nexts[0] == key:  # 左递归存在
                s1 = []
                s2 = []
                s1, s2 = del_leftrecursion(key)
                infer[key] = s1
                infer[key + "'"] = s2
                flag = 1
    return


def del_leftrecursion(key):
    # 消除左递归
    s1 = []
    s2 = []
    not_ender.add(key + "'")
    for nextss in infer[key]:
        if nextss[0] == key:
            st = nextss[1:]
            st.append(key + "'")
            s2.append(st)

        else:
            st = nextss[:]
            st.append(key + "'")
            s1.append(st)

    s2.append(['_'])
    return s1, s2


# 找到含有左公因子的几个式子
def get_left(key):
    global left_index
    for index1 in range(len(infer[key])):
        for index2 in range(index1):
            try:
                if infer[key][index1][0] == infer[key][index2][0]:
                    ch = infer[key][index1][0]
                    lis = []
                    removelis = []
                    for judge_index in range(len(infer[key])):
                        if infer[key][judge_index][0] == ch:
                            if len(infer[key][judge_index][1:]) == 0:
                                lis.append(["_"])
                            else:
                                lis.append(infer[key][judge_index][1:])
                            removelis.append(infer[key][judge_index])
                    for data in removelis:
                        infer[key].remove(data)
                    infer[key].append([ch, "Z" + str(left_index)])
                    infer["Z" + str(left_index)] = lis
                    not_ender.append("Z" + str(left_index))
                    left_index = left_index + 1
            finally:
                return


def create_dire_recru():
    # 按照书本P65的方式消除
    lis = []
    for key in infer:  # (1)
        lis.append(key)
    for index1 in range(len(lis)):  # 遍历每个非终结符
        nexts = infer[lis[index1]]  # 取出
        for nexts_index in range(len(nexts)):  # 对这个非终结符能推出的表达式
            for index2 in range(index1):  # 遍历每个之前的非终结符
                if nexts[nexts_index][0] == lis[index2]:  # 如果形如（4）的形式
                    insertlist = []  # 存储
                    for nexts2 in infer[lis[index2]]:  # 指每个出的表达式
                        insert1 = []
                        for data in nexts2:
                            insert1.append(data)
                        for index3 in range(1, len(nexts[nexts_index])):
                            insert1.append(nexts[nexts_index][index3])
                        insertlist.append(insert1)
                    infer[lis[index1]].remove(nexts[nexts_index])
                    for data in insertlist:
                        infer[lis[index1]].append(data)


def find_empty_lis():
    for key in not_ender:
        for nexts in infer[key]:
            if nexts == ['_']:
                empty_set.add(key)
                break
    is_add = True
    while is_add == True:
        is_add = False
        for key in not_ender:
            for nexts in infer[key]:
                flag = 1
                for data in nexts:
                    if data not in empty_set:
                        flag = 0
                if flag == 1:
                    empty_set.add(key)
                    is_add = True


def find_select(key, nexts):
    sentence = key + " ->"
    for nextss in nexts:
        sentence = sentence + " " + nextss
    is_empty = True
    for nextss in nexts:
        if nextss not in empty_set:
            is_empty = False
    if is_empty == False:
        Select[sentence] = First[nexts[0]]

    else:
        Select[sentence] = (Follow[key]) | (First[nexts[0]] - set("_"))
    return "haha"


# 制作预测分析表
def create_table():
    for sentence in Select:
        left = sentence.split(" ")[0]
        if left not in predict_table:
            predict_table[left] = defaultdict(str)
        for data in Select[sentence]:
            predict_table[left][data] = sentence


def judge_LL1() -> bool:
    for sentence1 in Select:
        for sentence2 in Select:
            ch1 = sentence1.split(" ")[0]
            ch2 = sentence2.split(" ")[0]
            if sentence1 != sentence2 and ch1 == ch2:
                if Select[sentence1] & Select[sentence2] != set():
                    return False
    return True


def start_any(words):
    tdjg = ['E']
    p1 = 0
    p2 = 0
    while "" in words:
        words.remove("")
    # try:
    cs = 0
    while p2 < len(words) and cs < 1e3:
        cs = cs + 1
        if tdjg[p1] == words[p2]:
            p1 = p1 + 1
            p2 = p2 + 1
        if p1 >= len(tdjg):
            return
        if tdjg[p1] == '_':
            tdjg.remove("_")
        nextword = words[p2]
        flag = 0

        for sentence in Select:
            left1 = sentence.split(" ")[0]
            if p1 >= len(tdjg):
                return
            if left1 == tdjg[p1]:
                st = set()
                st.add(nextword)
                if len(Select[sentence] & st) != 0:
                    print("%-60s     %-30s      {%-20s}      {%-20s}     {%-20s}" % (
                    tdjg, words, words[p2], sentence, str(words[p2]) + " ∈ " + "SELECT({})".format(sentence)))
                    next1 = sentence.split(" ")
                    tdjg.pop(p1)
                    for index in range(len(next1) - 1, 1, -1):
                        tdjg.insert(p1, next1[index])
                    d = 1
        # finally:
        if cs >= 1e3:
            print("此处有问题，跳过(%s)" % tdjg[p1])

            tdjg.pop(p1)
            # p1=p1+1
            print("%-60s     %-30s      {%-20s}      {%-20s}     {%-20s}" % (
                tdjg, words, words[p2], sentence, str(words[p2]) + " ∈ " + "SELECT({})".format(sentence)))
            cs = 0

    print("%-60s     %-30s" % (tdjg, words))


if __name__ == '__main__':
    file = open("input2.sy")
    str1 = file.readline()
    while str1:
        left, right = str1.split("->")
        left = left.strip(" ")
        infer[left] = right.split("|")
        for index in range(len(infer[left])):
            infer[left][index] = infer[left][index].split(" ")
            infer[left][index] = [x.strip(" ") for x in infer[left][index] if x.strip(" ") != ""]  # 去掉空格
            infer[left][index] = [x.strip("\n") for x in infer[left][index] if x.strip("\n") != ""]  # 去换行符
        not_ender.add(left)
        str1 = file.readline()
    # 消除间接左递归
    create_dire_recru()

    # 消除左递归
    for data in not_ender:
        findleftrecrusion(data)

    # 提取左公因子
    for key in not_ender:
        get_left(key)
    find_empty_lis()
    empty_set.add("_")

    for key in infer:
        for lists in infer[key]:
            for ede in lists:
                if ede not in not_ender:
                    this_ender.add(ede)
    this_ender.add("$")
    for key in infer:  # 求出first集
        # if not First[key]:
        # for nexts in infer[key]:
        first(key)
    # 去空
    # for data in not_ender:
    #     if data not in First:
    #         First[data]="_"
    #     else:
    #         if "_" in First[data] and len(First[data])>1:
    #             First[data].discard('_')
    for key in infer:
        who_follow(key)
    for key in include_follow:
        followed[key] = include_follow[key].copy()
    # followed=include_follow.copy()

    # 求出follow集
    topo_lis = topo_sort()
    follow()
    for tp in topo_lis:
        for fl in followed[tp]:
            Follow[tp] = Follow[tp] | Follow[fl]
    for key in Follow:
        if "_" in Follow[key] and len(Follow[key]) != 1:
            Follow[key].discard('_')

    lis = []
    for key in First:
        if len(First[key]) == 0:
            lis.append(key)
    for data in lis:
        First.pop(data)

    # 求出select集

    for key in infer:
        for nexts in infer[key]:
            find_select(key, nexts)

    create_table()

    print(judge_LL1())

    file.close()

    sentence_file = open("sentence1.sy")
    str1 = sentence_file.readline()
    words = str1.split(" ")
    if judge_LL1():
        start_any(words)
