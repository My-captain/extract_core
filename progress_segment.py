# -*- coding: utf-8 -*-
# @Time    : 2019/4/8 17:57
# @Author  : Mr.Robot
# @Site    : 
# @File    : progress_segment.py
# @Software: PyCharm


import pynlpir

pynlpir.open()


if __name__ == "__main__":
    s = "服药便溏,大便呈糊状,大便日2次,胸闷胸痛,最近胸腔积液2次抽取,干咳少痰,难咯,口干欲饮,纳差,形瘦面灰,鼻准红赤,尿少色黄,有乙肝,肝硬化病史,"
    segment = pynlpir.segment(s, pos_tagging=False)
    print(segment)
    key_words = pynlpir.get_key_words(s)
    print(key_words)
    pynlpir
