import numpy as np

Keyword = ["if", "main", "else", "void", "return", "while", "for", "do", "break", "continue", "int", "char", "double",
           "float", "case", "const"]  # 关键字
operator = ["=", "+", "-", "*", "/", "%", "==", "!=",
            "<", ">", "<=", ">=", "!", "&&", "||"]  # 运算符
separater = [";", ",", "[", "]", "{", "}", "(", ")"]  # 分隔符
identifier_alpha = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                    'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N',
                    'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '_']
digit = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
nonzero_digit = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
octal_digit = ['0', '1', '2', '3', '4', '5', '6', '7']
hexadecimal_digit = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f', 'A', 'B', 'C', 'D',
                     'E', 'F']
isError = 0  # 存在语法错误置1
ErrorWord = np.array([], [])  # 存放错误信息的数组
Output = np.array([], [])  # 存放输出信息的数组
ErrorNumber = 0
OutputNUm = 0


def inputError(word, line):  # 输入错误信息  单词  行号
    isError = 1
    if type(word) == str and type(line) == int:
        ErrorWord[ErrorNumber][0] = '非法字符'
        ErrorWord[ErrorNumber][1] = word
        ErrorWord[ErrorNumber][2] = str(line)
    else:
        ErrorWord[ErrorNumber][0] = '缺少*/'
        ErrorWord[ErrorNumber][1] = ''
        ErrorWord[ErrorNumber][2] = str(line)


def toChar():
    return 0


def isalpha(n):
    for i in range(53):
        if identifier_alpha[i] == n:
            return True
    return False


def isDigit(n):
    for i in range(10):
        if digit[0] == n:
            return True
    return False


def isIdent(word):  # 判断是否为标识符
    if not(isalpha(word[0])):
        return False
    for i in range(1, len(word)):
        if not(isalpha(word[i])) and isDigit(word[i]):
            return False
    return True


def isNonzero_digit(n):
    for i in range(9):
        if nonzero_digit[i] == n:
            return True
    return False


def isDeciamlConst(word):
    if not(isNonzero_digit(word[0])):
        return False
    for i in range(len(word)):
        if not(isDigit):
            return False
    return True


def isOctalDigit(n):
    for i in range(8):
        if octal_digit[i] == n:
            return True
    return False


def isOctalConst(word):
    if word[0] != '0':
        return False
    for i in range(len(word)):
        if not(isOctalDigit(word[i])):
            return False
    return True

def isHexadecimalDigit(n):
    for i in range(16):
        if hexadecimal_digit[i]==n:
            return True
    return False

def isHexadecimalPrefix(n1,n2):
    if n1=='0'and (n2=='x' or n2=='X'):
        return True
    return False

def isHexConst(word):
    if len(word)<2:
        return False
    elif not(isHexadecimalPrefix(word[0],word[1])):
        return False
    for i in range(2,len(word)):
        if not(isHexadecimalDigit(word[i])):
            return False
    return True

# 检测是否是 InstConst
def isInstConst(word):
    if not(isDeciamlConst(word)) and not(isOctalConst(word))and not(isHexConst):
        return False
    return True