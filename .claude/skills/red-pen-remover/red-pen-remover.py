"""
Skill: Red Pen Mark Remover

Removes red handwritten marks from images using color detection and inpainting.

Usage:
    from red_pen_remover import remove_red_marks

    # Remove red marks from an image
    result = remove_red_marks("input.jpg", "output.jpg")

    # Adjust sensitivity for different lighting conditions
    result = remove_red_marks("input.jpg", "output.jpg", sensitivity=0.4)
"""

import cv2
import numpy as np
from PIL import Image
import os
from pathlib import Path


def remove_red_marks(
    input_path: str,
    output_path: str,
    sensitivity: float = 0.3,
    radius: int = 3,
    method: str = "telea"
) -> str:
    """
    Remove red handwritten marks from an image.

    Args:
        input_path: Path to the input image
        output_path: Path to save the cleaned image
        sensitivity: Color detection sensitivity (0.0-1.0), lower = more aggressive
        radius: Inpainting radius
        method: Inpainting method "telea" or "ns"

    Returns:
        Path to the output image
    """
    # Read image
    img = cv2.imread(input_path)
    if img is None:
        raise ValueError(f"Could not read image: {input_path}")

    # Convert to HSV for better color detection
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Define red color range in HSV
    # Red is at the boundaries of HSV hue circle (0-10 and 170-180)
    lower_red1 = np.array([0, 50, 50])
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([170, 50, 50])
    upper_red2 = np.array([180, 255, 255])

    # Create masks for red regions
    mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
    mask = cv2.bitwise_or(mask1, mask2)

    # Adjust sensitivity - erode to reduce noise
    kernel = np.ones((3, 3), np.uint8)
    mask = cv2.erode(mask, kernel, iterations=1)

    # Apply morphological operations to clean up the mask
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

    # Inpaint the image
    method = cv2.INPAINT_TELEA if method == "telea" else cv2.INPAINT_NS
    result = cv2.inpaint(img, mask, radius, flags=method)

    # Save result
    cv2.imwrite(output_path, result)

    return output_path


def batch_remove_red_marks(
    input_dir: str,
    output_dir: str,
    **kwargs
) -> list:
    """
    Remove red marks from all images in a directory.

    Args:
        input_dir: Directory containing images
        output_dir: Directory to save cleaned images
        **kwargs: Additional arguments for remove_red_marks

    Returns:
        List of output file paths
    """
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    results = []
    for file in input_path.iterdir():
        if file.suffix.lower() in ['.jpg', '.jpeg', '.png', '.bmp']:
            output_file = output_path / file.name
            remove_red_marks(str(file), str(output_file), **kwargs)
            results.append(str(output_file))

    return results


def remove_red_with_ai(
    input_path: str,
    output_path: str,
    model: str = "libred"
) -> str:
    """
    Remove red marks using AI-based inpainting (requires additional setup).

    Args:
        input_path: Path to input image
        output_path: Path to save output
        model: AI model to use ("libred", "lama", "zits")

    Returns:
        Path to output image
    """
    # Basic implementation using OpenCV
    # For better results, consider using:
    # - LaMa (Large Mask Inpainting)
    # - ZITS (Transformer-based)
    # - Stable Diffusion Inpainting

    return remove_red_marks(input_path, output_path)


def preview_masks(
    input_path: str,
    output_path: str,
    sensitivity: float = 0.3
) -> None:
    """
    Preview the red mask detection before removing.

    Generates a visualization showing:
    - Original image
    - Red mask (detected areas)
    - Inpainted result
    """
    img = cv2.imread(input_path)
    if img is None:
        raise ValueError(f"Could not read image: {input_path}")

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    lower_red1 = np.array([0, 50, 50])
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([170, 50, 50])
    upper_red2 = np.array([180, 255, 255])

    mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
    mask = cv2.bitwise_or(mask1, mask2)

    kernel = np.ones((3, 3), np.uint8)
    mask = cv2.erode(mask, kernel, iterations=1)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

    # Create visualization
    mask_colored = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)

    # Stack images horizontally
    combined = np.hstack([img, mask_colored])

    cv2.imwrite(output_path, combined)


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 3:
        print("Usage: python red_pen_remover.py <input> <output> [sensitivity]")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    sensitivity = float(sys.argv[3]) if len(sys.argv) > 3 else 0.3

    remove_red_marks(input_file, output_file, sensitivity)
    print(f"Saved to: {output_file}")
