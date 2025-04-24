# lgsv

LuoGu problem/training SaVer.

爬取洛谷题目。
尚未完工。

目前实现的功能：
- 爬取题单
- 将题目的 markdown 保存下来，存到当前目录的 out.md 中

使用方式：将仓库克隆下来，用 python 运行 `src/lgsv/cli.py`。

命令行选项：
```
usage: lgsv [-h] [-p PROBLEM] [-t TRAINING] [--pandoc-args PANDOC_ARGS] [--order ORDER] [-c COOKIE] [-o OUTPUT]

爬取洛谷题目并且进行格式转化

options:
  -h, --help            show this help message and exit
  -p PROBLEM, --problem PROBLEM
                        题目列表
  -t TRAINING, --training TRAINING
                        题单列表
  --pandoc-args PANDOC_ARGS
                        传给pandoc的参数（未实现）
  --order ORDER         指定题目部分的顺序，用逗号分隔。
                            b/background 对应题目背景
                            s/samples 对应样例
                            if/inputFormat 对应输入格式
                            of/outputFormat 对应输出格式
                            h/hint 对应说明/提示
                            d/description 对应题目描述
                            tr/translation 对应题目翻译。

  -c COOKIE, --cookie COOKIE
                        洛谷cookie
  -o OUTPUT, --output OUTPUT
                        输出 markdown 的位置
```

例子：
例如，要将保存编号为 `100,101` 的题单和 `P11233` 按顺序保存题目背景，描述，输入格式，输出格式，将结果保存到 `a.md` ，使用 `lgsv -t 100 -t 101 -p P11233 --order=b,d,if,of -o a.md`。

待办：
1. 编写pytest
2. 处理各类异常
3. 添加更多功能
4. 完善文档
5. 其它格式