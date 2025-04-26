import re


# 在正则表达式中，\b 是一个特殊字符，表示单词边界（word boundary）。
# 它用于匹配单词的开始或结束位置，而不是匹配具体的字符。
# 具体来说，\b 匹配的位置是在单词字符（字母、数字、下划线）和非单词字符之间的位置。
# 使用 \b 可以确保匹配的是完整的单词，而不是单词的一部分

# 在正则表达式中，向前断言（Lookahead） 和 向后断言（Lookbehind） 是两种特殊的断言类型，它们允许你在匹配某个模式时，检查其前后是否存在特定的子模式，而不会将这些子模式包含在最终的匹配结果中。这两种断言在复杂的文本处理和模式匹配中非常有用。
# 向前断言（Lookahead）
# 向前断言用于检查当前位置后面是否匹配某个模式，但不包括该模式在最终的匹配结果中。向前断言分为两种：
# 正向向前断言（Positive Lookahead）：
# 语法：(?=...)
# 作用：确保当前位置后面跟着指定的模式，但不包含该模式在匹配结果中。
# 负向向前断言（Negative Lookahead）：
# 语法：(?!...)
# 作用：确保当前位置后面不跟着指定的模式。

# 向后断言（Lookbehind）
# 向后断言用于检查当前位置前面是否匹配某个模式，但不包括该模式在最终的匹配结果中。向后断言也分为两种：
# 正向向后断言（Positive Lookbehind）：
# 语法：(?<=...)
# 作用：确保当前位置前面跟着指定的模式，但不包含该模式在匹配结果中。
# 负向向后断言（Negative Lookbehind）：
# 语法：(?<!...)
# 作用：确保当前位置前面不跟着指定的模式。

# 注意事项
# 性能影响：断言操作可能会对性能产生一定影响，特别是在处理大规模文本时。
# 兼容性：并非所有正则表达式引擎都支持所有类型的断言，因此在使用时需要注意目标环境的支持情况。

def str_to_pattern(pattern) -> re.Pattern:
    return re.compile(pattern)


# ^：匹配字符串的开始。
# $：匹配字符串的结束。
def re_begin_with(key, want_pattern=".*"):
    """
    - r"^w\w+"
    - 字符串 "word" 匹配成功，整个匹配结果为 "word"。
    - r"^w(\w+)"
    - 字符串 "word" 匹配成功，整个匹配结果为 "word"，捕获组内容为 "ord"。
    - result = re.search(r"^w(\w+)","world")
    - print(result.group(0)) => "word"
    - print(result.group(1)) => "ord"
    """
    return f"^{key}{want_pattern}"


def re_finish_with(key, want_pattern=".*"):
    return f"{want_pattern}{key}$"


# re.search
# 功能：在字符串中搜索第一个匹配正则表达式的部分。
# 返回值：返回一个匹配对象（MatchObject），如果找不到匹配则返回 None。
# 适用场景：当你只需要知道是否存在匹配项，或者只需要找到第一个匹配项时使用

# re.findall
# 功能：在字符串中查找所有匹配正则表达式的部分。
# 返回值：返回一个列表，包含所有匹配的子字符串。如果没有找到匹配，则返回一个空列表。
# 适用场景：当你需要获取所有匹配项时使用。
def re_findall_word(want_pattern, text):
    return re.findall(rf"\b{want_pattern}\b", text)


def re_match_between(start, want, end):
    """
    完整匹配
    :param start:
    :param want:
    :param end:
    :return:
    """
    return f"^{start}({want}){end}$"


# ^：匹配字符串的开始。
# $：匹配字符串的结束。
# 一起用，是匹配完整字符串
def re_is_between(start, end, text):
    return re.match(f"^{start}.*{end}$", text)


def re_findall_between(start, want, end, text):
    return re.findall(f"{start}{want}{end}", text)


def re_findall_between_no_include(start, want, end, text):
    """
    查找所有start和end之间的want内容，不包括start和end
    """
    return re.findall(f"(?<={start}){want}(?={end})", text)


# 注意事项
# 性能影响：断言操作可能会对性能产生一定影响，特别是在处理大规模文本时。
# 兼容性：并非所有正则表达式引擎都支持所有类型的断言，因此在使用时需要注意目标环境的支持情况。


# 正向先行断言是一种正则表达式语法，用于匹配特定字符前面紧跟着的内容，但不包括这个字符本身。
# 正向先行断言使用 (?=...) 的格式来表示，其中 ... 是一个正则表达式，表示要匹配的“前面的内容”。
# 在正向先行断言中，(?=...) 中的 ... 通常是一个匹配后缀的正则表达式，用于指定“要匹配的带有后缀的内容”，例如 (?=abc) 表示匹配紧跟着 abc 的内容。需要注意的是，括号内的表达式与上下文要匹配的字符串中的实际内容是不匹配的，也就是说，这个表达式只起到一个限定匹配条件的作用。
# 例如，对于字符串 "hello, world"，可以使用 \w+(?=, ) 来匹配逗号前面的单词，这个正则表达式中的 (?=, ) 表示匹配之后必须有逗号和一个空格，\w+ 则表示匹配一个或多个单词字符。这个表达式的匹配结果是 "hello"。

# 正向先行断言（Positive Lookahead）
# 语法：(?=...)
# 作用：匹配某个位置，该位置后面跟着指定的模式，但不包括该模式本身。
def re_lookahead_positive(want_pattern, key_no_include):
    """
    - 用于匹配特定字符前面紧跟着的内容，但不包括这个字符本身。
    - 表示要匹配的“前面的内容”。
    :param key:
    :return:
    """
    return f"{want_pattern}(?={key_no_include})"


# 负向先行断言（Negative Lookahead）
# 语法：(?!...)
# 作用：匹配某个位置，该位置后面不跟着指定的模式
def re_lookahead_negative(want_pattern, key_no_include):
    """
    - 用于匹配特定字符前面非紧跟着的内容，但不包括这个字符本身。
    - 表示要匹配的“前面的内容”。

    :param key:
    :return:
    """
    return f"{want_pattern}(?!{key_no_include})"


# 正向后行断言（Positive Lookbehind）
# 语法：(?<=...)
# 作用：匹配某个位置，该位置前面跟着指定的模式，但不包括该模式本身。
#     """
#     - 用于匹配特定字符后面紧跟着的内容，但不包括这个字符本身。
#     - 表示要匹配的“后面的内容”。
#     - (?<=hellow}) hellow world =>world
#     :param key:
#     :return:
#     """
def re_lookbehind_positive(key_no_include, want_pattern):
    """
    - 匹配 key_no_include 紧跟着后面的内容，什么内容由 want_pattern 匹配
    - 想要的 want_pattern 前面紧跟着指定的模式 key_no_include。
    - (?<!,)\w+ => hellow,world -> ['world']
    :param want_pattern: 要匹配出的正则内容
    :param key_no_include: 关键字，匹配结果不包括
    :return:
    """
    return f"(?<={key_no_include}){want_pattern}"


# 负向向后断言（Negative Lookbehind）：
# 语法：(?<!...)
# 作用：确保当前位置前面不跟着指定的模式。
def re_lookbehind_negative(key_no_include, want_pattern):
    """
    - 匹配【不是】key_no_include 紧跟着后面的内容，什么内容由 want_pattern 匹配
    - 想要的 want_pattern 前面不跟着指定的模式 key_no_include。
    - (?<!,)\w+ => hellow, world -> ['hello', 'orld']
    :param want_pattern: 要匹配出的正则内容
    :param key_no_include: 关键字，匹配结果不包括
    :return:
    """
    return rf"(?<!{key_no_include}){want_pattern}"


def test_findall(pattern, text):
    # match = re.search(pattern, text)
    # if match:
    #     print("search.group(0):", match.group(0))
    print("pattern:", pattern)
    all = re.findall(pattern, text)
    if all:
        print("findall:", all)


if __name__ == '__main__':
    #  "hello, world"，可以使用 \w+(?=, )
    pattern = r'\w+(?=, )'
    text = "hello, world"
    # test_search(r"\w+(?=o)", text)
    # test_search("(?<=hellow}).*", text)
    # test_findall(lookbehind_positive(r"\w+", ","), text)
    # test_findall(lookbehind_negative(r"\w+", ","), text)
    result = re.match(re_finish_with("(log|dog)", ".*"), "git log.dog")
    print(result)
