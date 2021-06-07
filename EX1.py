import numpy as np

Keyword = ["if", "main", "else", "void", "return", "while", "for", "do", "break", "continue", "int", "char", "double",
           "float", "case", "const"]  # 关键字
operator = ["=", "+", "-", "*", "/", "%", "==", "!=", "<", ">", "<=", ">=", "!", "&&", "||"]  # 运算符
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
