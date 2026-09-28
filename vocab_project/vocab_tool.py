# -*- coding: utf-8 -*-
"""vocab_tool.py —— 我的生词小测出题器（国际中文教育 HSK4 方向）。

和老师骨架的区别（不是照抄）：
  - CSV 列结构：词条/拼音/HSK等级/词性/英文释义/例句（老师骨架是 词汇/等级/词性/释义/备注）
  - 题型不照抄"用X造一个句子"，改成我教学里更常用的两类：
      题型一：看英文释义，从 4 个选项里选正确的中文词
      题型二：选词填空，把当天学的词填进句子里
  - 函数名也换了：read_wordbook / pick_level / tally_pos / build_quiz
仅用 Python 标准库。
"""
import csv
from collections import Counter

from weekpath import data_path, root_path

# 本周要出的等级，改这一个数就能出 HSK3 / HSK4 / HSK5 的题
TARGET_LEVEL = 4
# 题型一每题给几个干扰项（不含正确答案）
DISTRACTOR_N = 3


def read_wordbook(csv_file):
    """读 CSV，返回词表 list[dict]。"""
    with open(csv_file, "r", encoding="gbk") as f:
        return list(csv.DictReader(f))


def pick_level(wordbook, level):
    """按 HSK 等级筛出目标词。"""
    return [w for w in wordbook if w["HSK等级"].strip() == str(level)]


def tally_pos(target_words):
    """统计词性分布。"""
    return dict(Counter(w["词性"].strip() for w in target_words))


def group_by_pos(target_words):
    """作业2①：把词按词性分组，返回 {词性: [词条, ...]} 的字典。"""
    groups = {}
    for w in target_words:
        pos = w["词性"].strip()
        groups.setdefault(pos, []).append(w["词条"].strip())
    return groups


def build_quiz(target_words, all_words):
    """出一套小测：
    第零部分：按词性分组速览（作业2①）
    第一部分：看英文释义选中文词（四选一）
    第二部分：选词填空（从例句里把目标词挖掉）
    """
    lines = []
    lines.append("===== HSK4 课堂小测（自动生成） =====")
    lines.append(f"本次共出题 {len(target_words)} 道，请 10 分钟内完成。")
    lines.append("")

    # 第零部分：按词性分组速览
    lines.append("--- 第零部分：按词性分组速览（课前热身，5 分钟）---")
    groups = group_by_pos(target_words)
    for pos, words_in_group in groups.items():
        lines.append(f"【{pos}】共 {len(words_in_group)} 个：" + "、".join(words_in_group))
    lines.append("")

    # 第一部分：释义选择题
    lines.append("--- 第一部分：看英文释义，选出对应的中文词（每题 1 分）---")
    for i, w in enumerate(target_words, 1):
        right = w["词条"].strip()
        # 从词表里挑干扰项：不是这个词、且同等级或近等级的词
        distractors = []
        for cand in all_words:
            if cand["词条"].strip() == right:
                continue
            if cand["HSK等级"].strip() in {str(TARGET_LEVEL), "3", "5"}:
                distractors.append(cand["词条"].strip())
            if len(distractors) >= DISTRACTOR_N:
                break
        options = distractors + [right]
        options.sort()  # 打乱选项顺序
        opt_str = "  ".join(f"{chr(65+j)}. {opt}" for j, opt in enumerate(options))
        lines.append(f"{i}. {w['英文释义'].strip()}  （{w['拼音'].strip()}）")
        lines.append(f"   {opt_str}")
    lines.append("")

    # 第二部分：选词填空
    lines.append("--- 第二部分：选词填空（每题 1 分）---")
    bank = "、".join(w["词条"].strip() for w in target_words)
    lines.append(f"词库：{bank}")
    lines.append("")
    for i, w in enumerate(target_words, 1):
        # 把例句里的目标词挖掉
        sentence = w["例句"].strip()
        blank_sentence = sentence.replace(w["词条"].strip(), "______", 1)
        lines.append(f"{i}. {blank_sentence}")
    lines.append("")

    # 答案区（最后给老师用）
    lines.append("--- 答案（教师用，打印前请删除本部分）---")
    for i, w in enumerate(target_words, 1):
        lines.append(f"{i}. {w['词条']}（{w['词性']}）")
    return "\n".join(lines)


def main():
    all_words = read_wordbook(data_path("生词表.csv"))
    print(f"[1/3] 读入词表共 {len(all_words)} 个词。")

    target = pick_level(all_words, TARGET_LEVEL)
    print(f"[2/3] 筛出 HSK{TARGET_LEVEL} 词 {len(target)} 个，词性分布：{tally_pos(target)}")

    quiz_text = build_quiz(target, all_words)
    out_path = root_path() / "练习.txt"
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(quiz_text)
    print(f"[3/3] 练习已写入：{out_path}")


# 随堂小练（2'）：for w in words: if w["词性"]=="动词": print(w["词汇"])
# 答：打印所有词性为"动词"的词。对本词表：照顾、毕业、影响、调查、实现、交流、鼓励、吸引，共 8 个。
if __name__ == "__main__":
    main()
