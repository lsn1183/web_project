import difflib

text1 = """text1:   #定义字符串1
This module provides classes and functions for comparing sequences.
including HTML and context and unified diffs.
difflib document v7.4
add string"""

text1_lines = text1.splitlines()                #以行进行分割，以便进行对比
text2 = """text2:           #定义字符串2
This module provides classes and functions for comparing sequences.
including HTML and context and unified diffs.
difflib document v7.5
add string"""

text2_lines = text2.splitlines()
# d = difflib.HtmlDiff()             # 创建HtmlDiffer()对象
# html = d.make_file(text1_lines, text2_lines)        #采用make_file方法对字符串进行比较
#
# import sys, os
# # fd = os.open('test.html', mode='rw')
# # os.write(fd, html)
# sys.stdout.writelines(html)

import wdiffhtml
#
wdiffhtml.generate_wdiff(text1_lines, text2_lines)
#
from simplediff import string_diff, html_diff
s1 = """
<s>this is strike through text</s>
|column1|column2|column3|
|-|-|-|
|*Content Cell*|content2|content3|
![alternate text](https://sourceforge.net/images/icon_linux.gif)"""

s2 = """
<s>this is strikeaa through text</s>
|col1|col2|col3|
|-|-|-|
|*Content*|content2|content3|
![alternate text](https://sourceforge.net/images/icon_linux.gif)"""
# r = (string_diff(s1, s2))
# for n in r:
#     print(n)
# print(s1)

import diff_match_patch as dmp_module
t1 = """I am the very model of a modern Major-General,\n
I've information vegetable, animal, and mineral,\n
I know the kings of England, and I quote the fights historical,\n
From Marathon to Waterloo, in order categorical."""
t2 = """I am the very model of a cartoon individual,\n
My animation's comical, unusual, and whimsical,\n
I'm quite adept at funny gags, comedic theory I have read,\n
From wicked puns and stupid jokes to anvils that drop on your head."""

t1 = "公元 2018-12-10. 中华民族"
t2 = "公元 2018-12-11. 中华新国"
dmp = dmp_module.diff_match_patch()
diffs = dmp.diff_main(t1, t2)
print(diffs)
for diff in diffs:
    print(diff)
print('==============================================')
dmp.diff_cleanupSemantic(diffs)
# dmp.diff_lineMode()
for diff in diffs:
    print(diff)

import os
os.mkdir()
