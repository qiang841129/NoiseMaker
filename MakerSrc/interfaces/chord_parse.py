from settings import *


def noteset2chord(note_set, saved_chord=0, tone=DEF_TONE_MAJOR, accompany_note_set=None):
    """
    获取一个音符组合对应的和弦
    处理和弦的思路
    a.寻找合适三和弦
    b.在寻找合适的七和弦（当同一时间的音符数量大于4的时候，a和b的顺序反过来）
    c.当音符组合不足3个时，与伴随音符相组合寻找和弦
    d.记为未知和弦

    :param note_set: 音符组合
    :param saved_chord: 保存的和弦（如果当前音符组合数量不多于2，且音符组合适用保存和弦，则直接认定这一拍的和弦为保存和弦）
    :param tone: 调式（影响选取的优先级）
    :param accompany_note_set: 伴随音符组合
    :return: 当前时刻的和弦
    """
    if tone == DEF_TONE_MAJOR:  # 推荐和弦列表
        recommend_chord_list = [{0, 4, 7}, {5, 9, 0}, {7, 11, 2}, {9, 0, 4}, {2, 5, 9}, {4, 7, 11}]
    elif tone == DEF_TONE_MINOR:
        recommend_chord_list = [{0, 4, 9}, {2, 5, 9}, {4, 7, 11}, {0, 4, 7}, {5, 9, 0}, {7, 11, 2}]
    else:
        recommend_chord_list = []
    # 1.把所有的音符全部转化到0-11
    new_note_set = set()
    for note in note_set:
        new_note_set.add(note % 12)
    # 2.note_set只有一个音符的情况
    if len(new_note_set) == 1:
        # 2.1.如果这一个音符属于上一个和弦 那么返回上一个和弦
        if new_note_set.issubset(CHORD_LIST[saved_chord]):
            return saved_chord
        # 2.2.除此以外的其他情况 考虑两拍的全部音符 如果在此情况下能找到对应的和弦 则返回该和弦 否则返回0
        if accompany_note_set:
            return noteset2chord(note_set | accompany_note_set, saved_chord, tone, None)
        else:
            return 0
    # 3.note_set中有两个音符的情况
    if len(new_note_set) == 2:
        # 3.1.如果这两个音符属于上一个和弦 那么返回上一个和弦
        if new_note_set.issubset(CHORD_LIST[saved_chord]):
            return saved_chord
        # 3.2.如果这两个音符属于推荐和弦 返回该推荐和弦在和弦字典中的位置
        for chord_it in range(len(recommend_chord_list)):
            if new_note_set.issubset(recommend_chord_list[chord_it]):
                return CHORD_LIST.index(recommend_chord_list[chord_it])
        # 3.3.除此以外的其他情况 考虑两拍的全部音符 如果在此情况下能找到对应的和弦 则返回该和弦 否则返回0
        if accompany_note_set:
            return noteset2chord(note_set | accompany_note_set, saved_chord, tone, None)
        else:
            return 0
    # 4.note_set中有三个音符的情况 如果这个和弦在CHORD_DICT列表中 泽返回他在列表中的位置 否则返回未知和弦
    if len(new_note_set) == 3:
        try:
            return CHORD_LIST.index(new_note_set)
        except ValueError:
            return note_set_to_7chord(new_note_set)  # 如果没有合适的三和弦可供选择 看看有没有可供选择的七和弦
    # 5.note_set中有多余三个音符的情况
    if len(new_note_set) >= 4:
        # 5.1.如果有七和弦是它的子集 返回该七和弦在和弦字典中的位置
        choose_7chord = note_set_to_7chord(new_note_set)
        if choose_7chord != 0:
            # print('\t%d', choose_7chord)
            return choose_7chord
        # 5.2.如果上一个和弦是它的子集 那么返回上一个和弦
        if CHORD_LIST[saved_chord].issubset(new_note_set):
            return saved_chord
        # 5.3.如果推荐和弦中有和弦是它的子集 那么返回该推荐和弦在和弦字典中的位置
        for chord_it in range(len(recommend_chord_list)):
            if recommend_chord_list[chord_it].issubset(new_note_set):
                return CHORD_LIST.index(recommend_chord_list[chord_it])
        # 5.4.如果和弦字典中有和弦是它的子集 那么返回它在列表中的位置
        for chord_it in range(1, 73):  # 1-72号位是三和弦
            if CHORD_LIST[chord_it].issubset(new_note_set):
                return chord_it
        # 5.5.其他情况 返回未知和弦
        return 0
    return 0


def note_set_to_7chord(note_set):
    """
    寻找音符列表对应的七和弦(音符组合至少要有3个音)
    :param note_set: 音符列表 这里的音符列表已经全部转化到0-11之中
    :return: 七和弦在CHORD_LIST中的编号
    """
    if len(note_set) == 3:  # 有三个音的情况
        for chord_it in range(73, 109):
            if note_set.issubset(CHORD_LIST[chord_it]):  # 在CHORD_DICT中，73-108是七和弦
                return chord_it
        return 0
    elif len(note_set) >= 4:  # 大于等于四个音的情况
        for chord_it in range(73, 109):
            if CHORD_LIST[chord_it].issubset(note_set):
                return chord_it
        return 0
    else:
        return 0


def chord_to_3(chord_dx):
    """
    将一个和弦转化为三和弦
    :param chord_dx: 和弦在CHORD_LIST中的位置
    :return: 转化之后的三和弦在CHORD_LIST中的位置
    """
    if chord_dx <= 72 and chord_dx % 6 in range(1, 5):  # 输入和弦为大三/小三/增三/减三
        return chord_dx
    if chord_dx <= 72 and chord_dx % 6 in [0, 5]:  # 输入和弦为挂二/挂四
        return -1
    if chord_dx >= 72:  # 输入和弦为七和弦
        if chord_dx % 3 in [0, 1]:
            return ((chord_dx - 73) // 3) * 6 + 1
        else:
            return ((chord_dx - 73) // 3) * 6 + 2


def get_chord_root_pitch(chord_dx, last_root, expect_root_base):
    """
    确定一个和弦的根音。如果不能确定当前和弦则根音沿用上一个。
    方法是将根音调整至离预期根音均值与上一个根音的平均值最近的点
    :param expect_root_base: 预期的根音平均值
    :param chord_dx: 和弦编号
    :param last_root: 上一拍的根音
    :return: 这一拍的根音
    """
    if chord_dx == 0:  # 这一拍没有和弦 沿用上一拍的根音
        return last_root
    # 1.根据和弦在CHORD_LIST的位置获取根音
    if chord_dx <= 72:
        chord_root = (chord_dx - 1) // 6
    else:
        chord_root = (chord_dx - 73) // 3
    # 2.调整根音的音高
    if last_root == 0:
        expect_root = expect_root_base
    else:
        expect_root = last_root * 0.55 + expect_root_base * 0.45  # 预期的根音高度
    pitch_diff = chord_root - expect_root
    pitch_adj = 12 * round(pitch_diff / 12)  # 要调整的数值
    return chord_root - pitch_adj


def chord_row_in_list(chord_dx):
    """chord位于settings中的chord_list的第几行"""
    if chord_dx == 0:
        return 0
    elif chord_dx <= 72:
        return (chord_dx - 1) // 6 + 1
    elif chord_dx <= 108:
        return (chord_dx - 73) // 3 + 1
