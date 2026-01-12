"""
Skill: Red Pen Mark Remover - Enhanced Version
"""

import cv2
import numpy as np


def remove_red_marks(
    input_path: str,
    output_path: str,
    radius: int = 5,
    method: str = "telea"
) -> str:
    """
    Remove red marks while preserving text.
    """
    img = cv2.imread(input_path)
    if img is None:
        raise ValueError(f"Could not read image: {input_path}")

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # 扩展红色范围，包含更多红色变体
    lower_red1 = np.array([0, 40, 40])
    upper_red1 = np.array([25, 255, 255])
    lower_red2 = np.array([155, 40, 40])
    upper_red2 = np.array([180, 255, 255])

    mask = cv2.inRange(hsv, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
    mask = cv2.bitwise_or(mask, mask2)

    # 饱和度阈值 - 只保留高饱和度颜色
    _, mask_sat = cv2.threshold(hsv[:, :, 1], 60, 255, cv2.THRESH_BINARY)
    mask = cv2.bitwise_and(mask, mask_sat)

    # 排除亮度太暗或太亮的区域（保护文字）
    # 文字通常是中等亮度
    _, mask_val = cv2.threshold(hsv[:, :, 2], 30, 255, cv2.THRESH_BINARY)
    _, mask_val2 = cv2.threshold(hsv[:, :, 2], 220, 255, cv2.THRESH_BINARY_INV)
    mask_val = cv2.bitwise_and(mask_val, mask_val2)
    mask = cv2.bitwise_and(mask, mask_val)

    # 形态学处理
    kernel = np.ones((7, 7), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    mask = cv2.dilate(mask, kernel, iterations=1)

    # 去除小区域噪点
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        area = cv2.contourArea(contour)
        if area < 500:
            cv2.drawContours(mask, [contour], -1, 0, -1)

    # 修复
    method = cv2.INPAINT_TELEA if method == "telea" else cv2.INPAINT_NS
    result = cv2.inpaint(img, mask, radius, flags=method)

    cv2.imwrite(output_path, result)
    return output_path


if __name__ == "__main__":
    import sys
    remove_red_marks(sys.argv[1], sys.argv[2])
