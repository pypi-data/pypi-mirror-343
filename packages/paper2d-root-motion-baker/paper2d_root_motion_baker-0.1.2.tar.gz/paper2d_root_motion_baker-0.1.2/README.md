# Paper2D Root Motion Baker

A Python tool for baking root motion data from PNG sequence frames into JSON format.

## Requirements 
1. This tool is implemented in Python to bake sequential PNG frame data into JSON format.

## Implementation Principles 
1. PNG images arranged according to naming rules, with consistent resolution.
2. The first PNG image is designated as the baseline root motion image.
3. Detect a unique marker color point and set its coordinates as the root motion X/Y origin (0, 0).
4. Process each image in sequence and calculate X/Y coordinate changes based on the relative point.
5. Export a JSON file containing coordinates for each frame.



## Usage Example
```bash
python main.py --marker-color 251 242 54 "E:\KXHWL\Source" "E:\KXHWL\Source\motion_data.json"
```


## Installation

You can install the package via pip:

```bash
pip install paper2d-root-motion-baker
```

## Requirements

- Python 3.7+
- Pillow (PIL)
- NumPy

## Installation

1. Clone this repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

```bash
python main.py <input_directory> <output_json> [--marker-color R G B]
```

### Arguments

- `input_directory`: Directory containing PNG sequence frames
- `output_json`: Path for the output JSON file
- `--marker-color`: RGB values for the marker color (default: 255 0 0 for red)

### Example

```bash
prmb ./sprite_sequence output.json --marker-color 255 0 0
```

## Input Requirements

1. PNG sequence frames must:
   - Be in the same directory
   - Have consistent dimensions
   - Be named in a sortable sequence
2. Each frame must contain exactly one marker point of the specified color
3. The first frame is used as the reference frame (0,0)

## Output Format

The tool generates a JSON file with the following structure:

```json
{
  "frames": [
    {
      "frame": 0,
      "position": {
        "x": 0,
        "y": 0
      }
    },
    {
      "frame": 1,
      "position": {
        "x": 10,
        "y": 5
      }
    }
    // ... more frames
  ],
  "metadata": {
    "frame_count": 2,
    "version": "1.0"
  }
}
