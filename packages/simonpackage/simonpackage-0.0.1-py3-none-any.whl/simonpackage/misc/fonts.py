import os

from kivy.core.text import LabelBase
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label


chinese_fonts_linux = {'ttf': ['unifont','仿宋字体','仿宋_GB2312','楷体_GB2312','GB_FS_GB18030','GB_ST_GB18030','GB_HT_GB18030','GB_XBS_GB18030','GB_KT_GB18030'],
                       'TTF': ['CESI_SS_GB18030', 'CESI_KT_GB2312', 'CESI_SS_GB13000', 'CESI_FS_GB13000', 'CESI_XBS_GB18030', 'CESI_KT_GB18030', 'CESI_HT_GB13000', 'CESI_KT_GB13000', 'CESI_XBS_GB13000', 'CESI_FS_GB2312', 'CESI_FS_GB18030', 'CESI_HT_GB18030', 'CESI_HT_GB2312', 'CESI_XBS_GB2312', 'CESI_SS_GB2312']
                       }
chinese_fonts_windows = {'ttf': ['Deng', 'Dengl', 'Dengb', 'simfang', 'simhei', 'simkai'],
                 'TTF': ['ARIALUNI', 'FZSTK', 'SIMLI', 'SIMYOU', 'STXINWEI', 'STKAITI', 'STLITI', 'STFANGSO',
                         'STZHONGS', 'STCAIYUN', 'STHUPO', 'STSONG', 'STXIHEI', 'STXINGKA'],
                 'ttc': ['msjh', 'msjhbd', 'msjhl', 'msyh', 'msyhbd', 'msyhl', 'simsun']}
def findSupportChineseFonts():
    support_chinese_fonts = []
    for k, v in chinese_fonts_linux.items():
        for i in v:
            font = f'{i}.{k}'
            support_chinese_fonts.append(font)
    for k, v in chinese_fonts_windows.items():
        for i in v:
            font = f'{i}.{k}'
            support_chinese_fonts.append(font)

    fonts_dirs = LabelBase.get_system_fonts_dir()

    # fonts on the system
    system_fonts = []
    for d in fonts_dirs:
        for i in os.listdir(d):
            if i.endswith(('.ttf', '.TTF', '.TTC')):
                system_fonts.append(i)

    # find the intersection of the two fonts list
    available_fonts = list(set(system_fonts) & set(support_chinese_fonts))
    return available_fonts


if __name__ == '__main__':
    print(findSupportChineseFonts())