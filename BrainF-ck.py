"""
BrainF-ck.py

[ Compiler specification ]
Based on Brainfuck (bf20041219),
with some memory improvements and changes for Discord implementation.
Unfortunately, BrainCrash is not supported.

Reference:
http://www.muppetlabs.com/~breadbox/bf/
https://en.wikipedia.org/wiki/Brainfuck

Characteristic behavior
Incrementing 255 will set it to 0.
Decrementing 0 will set it to 255.

"""


# ----- Debug

import io
import sys
_INPUT = """\
++++++++++[>+>+++>+++++++>++++++++++<<<<-]>>>----.BISGOD
"""
sys.stdin = io.StringIO(_INPUT)

# ----- Main
# import re

class BrainFuck():

    # コンパイラ本体
    def bf(self, tx:str):
        """Exec BrainF*ck"""
        tx = BrainFuck.origin(self, tx)
        shift = 0 # 
        maxShift = 0
        arr = [0]
        out = []
        Error = ""
        i = 0
        while 1:
            vs = str(tx[i])
            if vs == '+': # 255未満ならインクリメント、255以上なら0
                arr[shift] += 1 if arr[shift] < 255 else 0
            elif vs == '-': # 0より大きい場合はデクリメント、0未満なら255
                arr[shift] -= 1 if arr[shift] > 0 else 255
            elif vs == '>': # ポインタをインクリメント (+)
                if len(arr) <= shift+1: arr.append(0)
                shift += 1
                if shift > maxShift : maxShift = shift
            elif vs == '<': # ポインタをデクリメント(-)
                shift -= 1
                if shift < 0:
                    Error = "Out of range of array Error"
                    break
            elif vs == '.': # 出力の追加
                out.append(arr[shift])
            elif vs == '[':
                if arr[shift] != 0:
                    c_cnt, res_loop = 0, "" # ループチェッカー, ループの展開した結果
                    s_ptr, e_ptr = i, 0 # 開始ポインタ, 終了ポインタ
                    l_cnt = 0 # ループカウンタ
                    while(c_cnt != 0 or l_cnt == 0):
                        vvs = tx[i+l_cnt]
                        if vvs == '[': c_cnt += 1
                        if vvs == ']': c_cnt -= 1
                        l_cnt += 1
                        if i+l_cnt >= len(tx):
                            Error = "Corresponding brackets are missing."
                            break
                    e_ptr = shift + l_cnt
                    if e_ptr > 0:
                        for j in range(arr[shift]):
                            res_loop += tx[(shift+1):(e_ptr-1)]
                    tx = str(tx[:(s_ptr-1)]) + str(res_loop) + str(tx[(e_ptr+1):])
                    print(s_ptr)
            i += 1
            if i >= len(tx): break
            # elif vs == ',':

        result = out
        return result, Error

    # コメント削除
    def origin(self, tx):
        return ''.join(filter(lambda x: x in ['.', ',', '[', ']', '>', '<', '+', '-'], tx))

# ----- Exec

inputs = str(input())

print(BrainFuck().bf(inputs))
