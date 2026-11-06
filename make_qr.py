# -*- coding: utf-8 -*-
"""
二维码生成器（离线，不需要联网）

用法一：双击「生成二维码.cmd」，按提示粘贴网址。
用法二：命令行
    python make_qr.py https://你的网址/
    python make_qr.py https://你的网址/ 文件名前缀

产物（写到本文件所在目录）：
    二维码.png       1640×1640 白底深墨，拖进 PPT 用
    二维码.svg       矢量版，印海报放大到两米也不糊
    二维码_桌卡.png   一张可打印的 A5 竖版桌卡（二维码 + 说明），贴在黑板/摊位上
"""
import sys
import os
import segno
from PIL import Image, ImageDraw, ImageFont

DARK = "#17120F"
INK = (23, 18, 15)
GRAY = (107, 95, 80)
GRAY2 = (154, 141, 123)
RED = (176, 18, 24)
PAPER = (246, 242, 234)

CLUB = "中国共产主义青年团华南师范大学2025级网络工程专业01班支部委员会"


def font(size, bold=False, serif=False):
    if serif:
        path = r"C:\Windows\Fonts\simsun.ttc"
    else:
        path = r"C:\Windows\Fonts\msyhbd.ttc" if bold else r"C:\Windows\Fonts\msyh.ttc"
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        return ImageFont.load_default()


def make_card(qr_png, out, url):
    W, H = 1200, 1700
    im = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(im)

    # 顶部细线 + 红色短线
    d.rectangle([96, 120, 1104, 122], fill=INK)
    d.rectangle([96, 140, 240, 148], fill=RED)

    # 抬头
    d.text((96, 176), "华南师范大学 2026 年主题团日竞赛活动", font=font(26), fill=GRAY)

    # 大标题
    d.text((96, 250), "扫码，重走", font=font(96, serif=True), fill=INK)
    d.text((96, 372), "一回长征路", font=font(96, serif=True), fill=INK)

    # 二维码（白底，留静区）
    qr = Image.open(qr_png).convert("RGB")
    box = 720
    qr = qr.resize((box, box), Image.NEAREST)
    qx, qy = (W - box) // 2, 560
    d.rectangle([qx - 34, qy - 34, qx + box + 34, qy + box + 34], fill=(255, 255, 255))

    qr = qr.resize((box, box), Image.NEAREST)
    im.paste(qr, (qx, qy))
    d = ImageDraw.Draw(im)

    # 说明
    d.text((96, 1386), "七个节点 · 二十四道党史题 · 约八分钟", font=font(34), fill=INK)
    d.text((96, 1444), "手机随扫随开，不用下载、不用注册。", font=font(28), fill=GRAY)

    # 底部：单位 + 网址
    d.rectangle([96, 1530, 1104, 1532], fill=(216, 206, 190))
    d.text((96, 1556), CLUB, font=font(20), fill=GRAY2)
    shown = url if len(url) <= 56 else url[:53] + "…"
    d.text((96, 1592), shown, font=font(20), fill=GRAY2)
    d.text((96, 1628), "e 路长征 · 青春挺膺", font=font(20, bold=True), fill=RED)

    im.save(out)
    return out


def main():
    if len(sys.argv) < 2:
        print("用法: python make_qr.py <网址> [文件名前缀]")
        return 1

    url = sys.argv[1].strip()
    prefix = sys.argv[2].strip() if len(sys.argv) > 2 else "二维码"

    if not url.lower().startswith(("http://", "https://")):
        print("！网址必须以 http:// 或 https:// 开头。")
        print("  手机扫 file:///D:/... 这样的本地路径是打不开的。")
        return 1

    here = os.path.dirname(os.path.abspath(__file__))
    png = os.path.join(here, prefix + ".png")
    svg = os.path.join(here, prefix + ".svg")
    card = os.path.join(here, prefix + "_桌卡.png")

    qr = segno.make(url, error="h")   # 最高纠错等级，投影压缩、纸面脏点都还能扫
    qr.save(png, scale=40, border=4, dark=DARK, light="#FFFFFF")
    qr.save(svg, scale=1, border=4, dark=DARK, light="#FFFFFF")

    ok_card = True
    try:
        make_card(png, card, url)
    except Exception as e:
        ok_card = False
        print("桌卡生成失败（不影响二维码本身）：", e)

    print("已生成：")
    print("  " + png)
    print("  " + svg)
    if ok_card:
        print("  " + card)
    print("里面编码的网址是：")
    print("  " + url)
    return 0


if __name__ == "__main__":
    sys.exit(main())
