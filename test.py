# -*- coding: utf-8 -*-
# @Time    : 2019/4/9 14:47
# @Author  : Mr.Robot
# @Site    : 
# @File    : test.py
# @Software: PyCharm

from PyDocExtractor import *
from PyKeyExtractor import *
from PyNewWordFinder import *
import pynlpir


if __name__ == "__main__":
    # de_init()
    # result, score = doc_extract("左肺癌一年,化疗一疗程,因白细胞减低停用,病理：左下肺腺癌,放疗27次,3月后CT发现纵隔淋巴左胸膜转移,目前仍见贫血,手足浮肿,低血压,既往有高血压,有痰不多色黄,口干,心中有火热感,尿黄,大便干结,2日1行,面浮黄,")
    # for i in result:
    #     print(i)
    # print(score)
    #
    # ke_init()
    # result = get_key_words("左肺癌一年,化疗一疗程,因白细胞减低停用,病理：左下肺腺癌,放疗27次,3月后CT发现纵隔淋巴左胸膜转移,目前仍见贫血,手足浮肿,低血压,既往有高血压,有痰不多色黄,口干,心中有火热感,尿黄,大便干结,2日1行,面浮黄,")
    # print(result)
    # ke_exit()
    #
    nwf_init()
    result = get_file_new_words("左肺癌一年,化疗一疗程,因白细胞减低停用,病理：左下肺腺癌,放疗27次,3月后CT发现纵隔淋巴左胸膜转移,目前仍见贫血,手足浮肿,低血压,既往有高血压,有痰不多色黄,口干,心中有火热感,尿黄,大便干结,2日1行,面浮黄,")
    print(result)

    # pynlpir.open()
    # result = pynlpir.segment("左肺癌一年,化疗一疗程,因白细胞减低停用,病理：左下肺腺癌,放疗27次,3月后CT发现纵隔淋巴左胸膜转移,目前仍见贫血,手足浮肿,低血压,既往有高血压,有痰不多色黄,口干,心中有火热感,尿黄,大便干结,2日1行,面浮黄,")
    # res = ["#".join(i) for i in result]
    # print(" ".join(res))
