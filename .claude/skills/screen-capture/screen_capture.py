#!/usr/bin/env python3
"""
屏幕捕获工具
支持 macOS screencapture 和 Python 截图库
"""

import argparse
import subprocess
import sys
from pathlib import Path


def capture_fullscreen(output_path: str = "screenshot.png") -> str:
    """使用 macOS screencapture 捕获全屏"""
    output = Path(output_path).expanduser().absolute()
    subprocess.run(["screencapture", "-S", str(output)], check=True)
    return str(output)


def capture_window(output_path: str = "window.png") -> str:
    """捕获当前窗口"""
    output = Path(output_path).expanduser().absolute()
    subprocess.run(["screencapture", "-w", str(output)], check=True)
    return str(output)


def capture_interactive(output_path: str = "selection.png") -> str:
    """交互式选择区域截图"""
    output = Path(output_path).expanduser().absolute()
    subprocess.run(["screencapture", "-i", "-s", str(output)], check=True)
    return str(output)


def capture_with_python(output_path: str = "screenshot.png") -> str:
    """使用 Python pyautogui 截图"""
    try:
        import pyautogui
        output = Path(output_path).expanduser().absolute()
        pyautogui.screenshot(str(output))
        return str(output)
    except ImportError:
        print("请安装 pyautogui: pip3 install pyautogui", file=sys.stderr)
        sys.exit(1)


def ocr_recognize(image_path: str) -> str:
    """使用 Tesseract OCR 识别文字"""
    try:
        from PIL import Image
        import pytesseract

        image = Image.open(image_path)
        text = pytesseract.image_to_string(image, lang="chi_sim+eng")
        return text.strip() if text else "未识别到文字"
    except ImportError:
        print("请安装依赖: pip3 install pytesseract pillow", file=sys.stderr)
        sys.exit(1)


def list_screenshots(directory: str = ".") -> list:
    """列出目录中的截图文件"""
    dir_path = Path(directory).expanduser()
    patterns = ["*.png", "*.jpg", "*.jpeg"]
    files = []
    for pattern in patterns:
        files.extend(dir_path.glob(pattern))
    return sorted(files)


def main():
    parser = argparse.ArgumentParser(description="屏幕捕获工具")
    parser.add_argument("-o", "--output", default="screenshot.png", help="输出文件路径")
    parser.add_argument("-w", "--window", action="store_true", help="捕获窗口")
    parser.add_argument("-i", "--interactive", action="store_true", help="交互式选择区域")
    parser.add_argument("-p", "--python", action="store_true", help="使用 Python pyautogui")
    parser.add_argument("--ocr", metavar="IMAGE", help="识别图片文字")
    parser.add_argument("--list", metavar="DIR", nargs="?", const=".", help="列出截图文件")

    args = parser.parse_args()

    if args.ocr:
        text = ocr_recognize(args.ocr)
        print(f"识别结果:\n{text}")
        return

    if args.list is not None:
        files = list_screenshots(args.list)
        print(f"截图文件 ({len(files)}):")
        for f in files:
            print(f"  - {f}")
        return

    if args.python:
        path = capture_with_python(args.output)
    elif args.window:
        path = capture_window(args.output)
    elif args.interactive:
        path = capture_interactive(args.output)
    else:
        path = capture_fullscreen(args.output)

    print(f"截图已保存: {path}")


if __name__ == "__main__":
    main()
