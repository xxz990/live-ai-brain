from __future__ import annotations


def generate_live_script_pack(product_name: str, pain_point: str, benefit: str) -> str:
    return f"""# {product_name} 主播话术包

## 开场留人
各位家长，如果孩子现在{pain_point}，先别急着怪孩子不努力，很多时候是文言文学习方法还没有搭起来。

## 痛点放大
孩子只会背课文，但换一篇课外文言文就不会翻译、不会抓关键词、不会判断文章主旨，这说明需要补的是方法。

## 产品解释
{product_name} 会围绕经典篇目，帮助孩子梳理作者背景、文本理解、字词句式、翻译方法和常见题型。

## 异议处理
如果家长担心孩子基础薄弱，可以先看孩子是否存在读不懂、翻译靠猜、答题没思路的问题。这类孩子更需要系统方法。

## 成交转化
需要的家长可以根据孩子年级选择对应规格。下单后注意查收短信，按服务老师提示领取课程和资料。当前权益以商品页为准：{benefit}。

## 合规提醒
不要承诺分数结果、一定有效、永久有效；表达重点放在建立方法、提升理解能力和规范学习路径。
"""


def generate_short_video_script(product_name: str, pain_point: str) -> str:
    return f"""# {product_name} 短视频脚本

## 前 3 秒钩子
孩子文言文总是靠猜，不一定是笨，可能是方法没搭起来。

## 痛点场景
一到翻译题就卡住，背过的课文会，换一篇课外文言文就没思路。

## 产品植入
{product_name} 从经典篇目入手，带孩子学作者背景、重点字词、翻译方法和答题思路。

## 结尾行动
如果孩子{pain_point}，可以先把文言文学习方法补起来。
"""


def generate_overlay_copy(product_name: str, benefit: str) -> str:
    return f"""# {product_name} 贴片 / KT 板文案

主标题：文言文读不懂，先补方法

核心卖点：
1. 经典篇目带方法
2. 翻译、理解、答题一起梳理
3. 适合需要系统补文言文方法的孩子

权益提醒：{benefit}

下单提醒：拍下后注意查收短信，按服务老师提示完成领取。
"""
