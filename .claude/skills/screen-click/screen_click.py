#!/usr/bin/env python3
"""
屏幕点击工具
支持单击、双击、右键点击和拖拽操作
"""

import sys
import re
import time
import argparse

try:
    import pyautogui
    import pytesseract
    from PIL import Image
except ImportError:
    print("需要安装依赖: pip3 install pyautogui pytesseract pillow")
    sys.exit(1)


def parse_coordinates(text):
    """解析坐标文本，返回 (x, y) 元组"""
    # 匹配 "100, 200" 或 "100 200" 格式
    pattern = r'(\d+)\s*,\s*(\d+)'
    match = re.search(pattern, text)
    if match:
        return int(match.group(1)), int(match.group(2))
    return None


def parse_drag_command(text):
    """解析拖拽命令，返回起始和结束坐标"""
    # 匹配 "拖拽从 100, 100 到 500, 500"
    pattern = r'拖拽从\s*(\d+)\s*,\s*(\d+)\s*到\s*(\d+)\s*,\s*(\d+)'
    match = re.search(pattern, text)
    if match:
        start = (int(match.group(1)), int(match.group(2)))
        end = (int(match.group(3)), int(match.group(4)))
        return start, end
    return None


def parse_click_type(text):
    """解析点击类型"""
    text = text.lower()
    if '双击' in text or 'double' in text:
        return 'double'
    elif '右键' in text or 'right' in text:
        return 'right'
    elif '中键' in text or 'middle' in text:
        return 'middle'
    else:
        return 'single'


def click(x, y, click_type='single'):
    """执行点击操作"""
    pyautogui.FAILSAFE = True
    pyautogui.PAUSE = 0.1

    # 移动到指定位置
    pyautogui.moveTo(x, y, duration=0.2)

    # 执行点击
    if click_type == 'single':
        pyautogui.click(x, y)
    elif click_type == 'double':
        pyautogui.doubleClick(x, y)
    elif click_type == 'right':
        pyautogui.rightClick(x, y)
    elif click_type == 'middle':
        pyautogui.middleClick(x, y)

    print(f"✓ 已{click_type}点击坐标 ({x}, {y})")


def drag(start_pos, end_pos):
    """执行拖拽操作"""
    pyautogui.FAILSAFE = True
    pyautogui.PAUSE = 0.1

    # 移动到起始位置
    pyautogui.moveTo(start_pos[0], start_pos[1], duration=0.2)

    # 按下鼠标
    pyautogui.mouseDown()

    # 移动到结束位置
    pyautogui.moveTo(end_pos[0], end_pos[1], duration=0.5)

    # 释放鼠标
    pyautogui.mouseUp()

    print(f"✓ 已拖拽从 {start_pos} 到 {end_pos}")


def scroll(amount, x=None, y=None):
    """执行滚动操作"""
    if x is not None and y is not None:
        pyautogui.moveTo(x, y, duration=0.1)

    pyautogui.scroll(amount)
    direction = "上" if amount > 0 else "下"
    print(f"✓ 已滚动 {direction} {abs(amount)} 刻度")


def get_screen_size():
    """获取屏幕尺寸"""
    width, height = pyautogui.size()
    print(f"屏幕尺寸: {width} x {height}")
    return width, height


def show_cursor_position():
    """显示当前鼠标位置（用于获取坐标）"""
    print("移动鼠标到目标位置，3秒后显示坐标...")
    time.sleep(3)
    x, y = pyautogui.position()
    print(f"当前鼠标坐标: ({x}, {y})")
    return x, y


def main():
    parser = argparse.ArgumentParser(description='屏幕点击工具')
    parser.add_argument('--x', type=int, help='X坐标')
    parser.add_argument('--y', type=int, help='Y坐标')
    parser.add_argument('--double', action='store_true', help='双击')
    parser.add_argument('--right', action='store_true', help='右键点击')
    parser.add_argument('--drag', type=str, help='拖拽: start_x,start_y:end_x,end_y')
    parser.add_argument('--scroll', type=int, help='滚动: 正数向上，负数向下')
    parser.add_argument('--get-size', action='store_true', help='获取屏幕尺寸')
    parser.add_argument('--get-pos', action='store_true', help='获取当前鼠标位置')
    parser.add_argument('--text', type=str, help='自然语言命令')

    args = parser.parse_args()

    if args.get_size:
        get_screen_size()
        return

    if args.get_pos:
        show_cursor_position()
        return

    if args.drag:
        # 解析拖拽参数
        try:
            parts = args.drag.split(':')
            start = tuple(map(int, parts[0].split(',')))
            end = tuple(map(int, parts[1].split(',')))
            drag(start, end)
        except Exception as e:
            print(f"拖拽参数格式错误: {args.drag}")
            print("正确格式: --drag 100,100:500,500")
        return

    if args.scroll is not None:
        scroll(args.scroll, args.x, args.y)
        return

    if args.x is not None and args.y is not None:
        click_type = 'double' if args.double else 'right' if args.right else 'single'
        click(args.x, args.y, click_type)
        return

    # 如果有文本命令，解析它
    if args.text:
        # 解析拖拽命令
        drag_result = parse_drag_command(args.text)
        if drag_result:
            start, end = drag_result
            drag(start, end)
            return

        # 解析点击命令
        coords = parse_coordinates(args.text)
        if coords:
            click_type = parse_click_type(args.text)
            click(coords[0], coords[1], click_type)
            return

        # 解析滚动命令
        if '滚屏' in args.text or '滚动' in args.text or 'scroll' in args.text.lower():
            if '上' in args.text or 'up' in args.text.lower():
                scroll(300)
            elif '下' in args.text or 'down' in args.text.lower():
                scroll(-300)
            else:
                scroll(300)
            return

    # 无参数时显示帮助
    print("屏幕点击工具 - 用法:")
    print("  python3 screen_click.py --x 100 --y 200          # 单击 (100, 200)")
    print("  python3 screen_click.py --x 100 --y 200 --double # 双击")
    print("  python3 screen_click.py --x 100 --y 200 --right  # 右键点击")
    print("  python3 screen_click.py --drag 100,100:500,500   # 拖拽")
    print("  python3 screen_click.py --get-size               # 获取屏幕尺寸")
    print("  python3 screen_click.py --get-pos                # 获取当前鼠标位置")
    print("\n自然语言命令:")
    print("  python3 screen_click.py --text '点击 100, 200'")
    print("  python3 screen_click.py --text '双击 500, 300'")
    print("  python3 screen_click.py --text '右键点击 800, 600'")
    print("  python3 screen_click.py --text '拖拽从 100, 100 到 500, 500'")


if __name__ == '__main__':
    main()
