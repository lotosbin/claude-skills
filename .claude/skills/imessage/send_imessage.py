#!/usr/bin/env python3
"""
发送iMessage的脚本
使用macOS的AppleScript通过Messages应用发送iMessage
"""

import subprocess
import sys
import re


def validate_phone_number(phone: str) -> bool:
    """验证手机号格式"""
    pattern = r'^\+?[1-9]\d{1,14}$'
    return bool(re.match(pattern, phone.replace(' ', '').replace('-', '')))


def validate_email(email: str) -> bool:
    """验证邮箱格式（可用于Apple ID）"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def send_imessage(recipient: str, message: str) -> bool:
    """
    使用AppleScript发送iMessage

    Args:
        recipient: 收件人手机号或Apple ID
        message: 消息内容

    Returns:
        发送是否成功
    """
    # 清理收件人信息
    recipient = recipient.strip()

    # 构建AppleScript命令
    script = f'''
tell application "Messages"
    activate
    set targetService to first service whose service type = iMessage
    set targetBuddy to buddy "{recipient}" of targetService
    send "{message}" to targetBuddy
end tell
'''

    try:
        # 执行AppleScript
        result = subprocess.run(
            ['osascript', '-e', script],
            capture_output=True,
            text=True,
            timeout=30
        )

        if result.returncode == 0:
            return True
        else:
            print(f"发送失败: {result.stderr}", file=sys.stderr)
            return False

    except subprocess.TimeoutExpired:
        print("发送超时", file=sys.stderr)
        return False
    except Exception as e:
        print(f"发送出错: {e}", file=sys.stderr)
        return False


def main():
    if len(sys.argv) < 3:
        print("用法: send_imessage.py <收件人> <消息内容>", file=sys.stderr)
        sys.exit(1)

    recipient = sys.argv[1]
    message = sys.argv[2]

    # 验证输入
    phone_valid = validate_phone_number(recipient)
    email_valid = validate_email(recipient)

    if not phone_valid and not email_valid:
        print("错误: 收件人格式不正确，应为手机号或有效的Apple ID", file=sys.stderr)
        sys.exit(1)

    # 发送消息
    if send_imessage(recipient, message):
        print(f"成功: iMessage已发送给 {recipient}")
        sys.exit(0)
    else:
        print(f"失败: 无法发送iMessage给 {recipient}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
