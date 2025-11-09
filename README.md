# Sulekhak-code

A comprehensive Python toolkit for processing handwritten character images, designed to help create custom fonts from handwritten samples. This project automates the workflow of extracting, classifying, and vectorizing handwritten characters.

## Overview

Sulekhak-code provides a three-step pipeline for converting handwritten text images into individual character vector files:

1. **Character Extraction** - Automatically crop individual characters from handwritten text images
2. **Character Classification** - Interactive GUI for labeling and organizing character images
3. **Vector Conversion** - Convert PNG character images to scalable SVG format

## Features

- 🖼️ **Intelligent Character Cropping**: Automatically detects and extracts individual characters from handwritten text with smart merging of diacritical marks
- 🏷️ **Interactive Classification**: User-friendly GUI for labeling characters with support for multi-character cropping
- 📐 **SVG Vectorization**: Converts raster images to clean vector graphics suitable for font creation
- 🔄 **Batch Processing**: Process multiple images and characters efficiently
- 🎯 **Quality Control**: Built-in binning system for separating unclear or unwanted characters

## Prerequisites

- Python 3.6 or higher
- pip (Python package manager)

## Dependencies

The project requires the following Python packages:

- **OpenCV (cv2)** - For image processing and character detection
- **Pillow (PIL)** - For image handling and manipulation
- **tkinter** - For GUI (usually comes pre-installed with Python)
- **svgwrite** - For SVG file generation

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/VardaanCodes/Sulekhak-code.git
   cd Sulekhak-code
   ```

2. **Install required packages**:
   ```bash
   pip install opencv-python pillow svgwrite
   ```

3. **Verify installation**:
   ```bash
   python --version  # Should be 3.6+
   ```

## Usage

### Step 1: Crop Characters (`1_crop.py`)

This script extracts individual characters from an image containing handwritten text.

**How to use:**
```bash
python 1_crop.py
```

**What it does:**
- Opens a file dialog to select an image file
- Detects individual characters using contour detection
- Intelligently merges diacritical marks (like dots) with their base characters
- Saves cropped character images to a folder named `cropped_[filename]_characters/`

**Tips:**
- Use high-contrast images for best results
- Ensure characters are clearly separated
- The script automatically adds padding around each character

### Step 2: Classify and Rename (`2_rename.py`)

An interactive GUI application for labeling and organizing cropped character images.

**How to use:**
```bash
python 2_rename.py
```

**Features:**
- **Single Character Labeling**: Type a single character and press Enter to rename the image
- **Multi-Character Cropping**: Type multiple characters to enable crop mode for splitting images
- **Binning**: Press Enter without typing to move unclear images to a `temp_bin` folder
- **Navigation**: Automatically moves to the next image after processing

**Keyboard Controls:**
- Enter key: Process current input and move to next image
- Type character(s) in the text field to label
- Click and drag on image to crop (in multi-character mode)

**Workflow:**
1. Click "Select Image Folder" and choose your cropped characters folder
2. For each image:
   - Type the character it represents and press Enter (e.g., 'a', 'b', 'क', 'ख')
   - OR type multiple characters and crop each one separately
   - OR press Enter without typing to move to temp_bin

### Step 3: Convert to SVG (`3_png2svg.py`)

Converts PNG character images to SVG vector format.

**How to use:**

1. **Edit the input directory** in the script:
   ```python
   input_directory = "cropped_test2_characters"  # Change to your folder name
   ```

2. **Run the script**:
   ```bash
   python 3_png2svg.py
   ```

**What it does:**
- Processes all PNG files in the specified input directory
- Applies image preprocessing (grayscale, blur, threshold, morphological operations)
- Detects contours and converts them to polygon paths
- Saves SVG files to an `svg/` output directory

**Output:**
- Clean, vectorized SVG files ready for font creation tools
- Each SVG maintains the character shape with optimized paths

## Complete Workflow Example

Here's a typical workflow for creating a font from handwritten samples:

1. **Prepare Your Sample**:
   - Write all characters neatly on paper
   - Take a high-resolution, well-lit photo

2. **Extract Characters**:
   ```bash
   python 1_crop.py
   # Select your handwriting image
   # Characters saved to: cropped_[filename]_characters/
   ```

3. **Label Characters**:
   ```bash
   python 2_rename.py
   # Select the cropped_[filename]_characters folder
   # Label each character or bin unclear ones
   ```

4. **Convert to Vectors**:
   - Edit `3_png2svg.py` to point to your labeled characters folder
   ```bash
   python 3_png2svg.py
   # SVG files created in svg/ directory
   ```

5. **Create Your Font**:
   - Use the SVG files with font creation software like FontForge or Glyphr Studio

## Project Structure

```
Sulekhak-code/
│
├── 1_crop.py              # Character extraction script
├── 2_rename.py            # Interactive classification GUI
├── 3_png2svg.py           # PNG to SVG converter
└── README.md              # This file
```

## Contributing

Contributions are welcome! Here are some ways you can contribute:

- Report bugs or suggest features by opening an issue
- Improve documentation
- Submit pull requests with enhancements
- Share your experience and results

## Tips and Best Practices

- **Image Quality**: Use high-resolution images (300 DPI or higher) for best cropping results
- **Contrast**: Ensure good contrast between text and background
- **Spacing**: Write characters with adequate spacing to improve automatic detection
- **Consistency**: Try to maintain consistent character size and baseline alignment
- **Testing**: Test with a small sample first before processing large batches

## Troubleshooting

**Issue: Characters not detected properly**
- Solution: Adjust the threshold value in `1_crop.py` (line 32)

**Issue: GUI not displaying images**
- Solution: Ensure tkinter is properly installed and image files are valid

**Issue: SVG output looks rough**
- Solution: Adjust the epsilon value in `3_png2svg.py` (line 22) for smoother or more detailed paths

## License

This project is open source. Please check with the repository owner for specific license terms.

## Acknowledgments

- Built for the Sulekhak project
- Uses OpenCV for computer vision tasks
- SVG generation powered by svgwrite library

## Contact

For questions, suggestions, or feedback, please open an issue on the GitHub repository.

---

**Happy Font Creating! ✍️**