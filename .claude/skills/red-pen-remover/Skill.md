# Red Pen Mark Remover

Removes red handwritten marks from scanned documents and images using color detection and inpainting algorithms.

## Installation

```bash
pip install opencv-python pillow numpy
```

## Usage

### Python API

```python
from red_pen_remover import remove_red_marks, batch_remove_red_marks, preview_masks

# Single image
remove_red_marks("document.jpg", "clean_document.jpg")

# Adjust sensitivity (0.0-1.0, lower = more aggressive)
remove_red_marks("document.jpg", "clean.jpg", sensitivity=0.2)

# Batch processing
batch_remove_red_marks("input_folder/", "output_folder/")

# Preview mask detection
preview_masks("document.jpg", "preview.jpg")
```

### Command Line

```bash
python red_pen_remover.py input.jpg output.jpg [sensitivity]
```

## Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| input_path | str | - | Path to input image |
| output_path | str | - | Path to save output |
| sensitivity | float | 0.3 | Color detection sensitivity (0.0-1.0) |
| radius | int | 3 | Inpainting radius |
| method | str | "telea" | Inpainting method: "telea" or "ns" |

## Tips

- **High sensitivity (0.4-0.5)**: Better for bright, clear scans
- **Low sensitivity (0.1-0.2)**: Better for dark or noisy images
- Use `preview_masks()` to tune sensitivity before processing
- Works best on documents with clear contrast between text and marks

## How It Works

1. **Color Detection**: Converts image to HSV color space and identifies red pixels
2. **Mask Processing**: Applies morphological operations to clean up the mask
3. **Inpainting**: Uses OpenCV's inpainting algorithm to fill in removed regions
