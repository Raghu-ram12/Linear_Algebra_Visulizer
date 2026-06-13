# Linear Algebra Visualizer

An interactive desktop application for visualizing 2D vectors and linear transformations, built with Python and Tkinter.

---

## Features

- **Vector Management** — Create and delete 2D vectors on a coordinate plane
- **Multiselect** — Select multiple vectors simultaneously using Ctrl+Click or Shift+Click to apply transformations to all at once
- **Transformations** — Apply common linear transformations to one or more vectors interactively:
  - Rotation by an arbitrary angle (animated)
  - Scaling (independent x and y factors)
  - Reflection across the x-axis or y-axis
  - Custom 2×2 transformation matrix input
- **Zoom Control** — Adjustable zoom slider to inspect vectors at any scale
- **Color-coded Vectors** — Each vector is rendered with a distinct color for easy identification
- **Scrollable Vector List** — A styled listbox displays all vectors with color labels and supports scrolling when many vectors are present

---

## Project Structure

```
Linear_Algebra_Visulizer/
├── main.py            # Entry point; builds the Tkinter UI and wires up controls
├── state.py           # Shared constants and global state (colors, scale, counters)
├── renderer.py        # Canvas drawing — coordinate plane, vectors
├── ui_handlers.py     # UI event handlers — vector creation, transformation inputs, deletion
├── transformations.py # Linear transformation logic (rotation, scale, reflect, shear)
├── vector_math.py     # Vector class and operations (add, subtract, dot product, magnitude, normalize)
└── matrix_math.py     # Matrix class and matrix–vector multiplication
```

---

## Getting Started

### Prerequisites

- Python 3.7+
- Tkinter (included with most standard Python installations)

### Installation

```bash
git clone https://github.com/Raghu-ram12/Linear_Algebra_Visulizer.git
cd Linear_Algebra_Visulizer
```

No additional dependencies are required.

### Running the App

```bash
python main.py
```

---

## Usage

| Control | Description |
|---|---|
| **Create Vector** | Enter x and y components to add a new vector to the canvas |
| **Delete Vector** | Select one or more vectors in the list, then click to remove them |
| **Rotate Vector** | Select vectors, enter an angle (degrees), and watch the animated rotation |
| **Scale Vector** | Scale selected vectors using independent x and y scale factors |
| **Reflect Vector** | Reflect selected vectors across the x-axis or y-axis |
| **Input Transform Matrix** | Apply any custom 2×2 transformation matrix to selected vectors |
| **Zoom Slider** | Adjust the canvas scale from 5 to 50 units |
| **Vector List** | Scrollable, color-coded list — Ctrl+Click or Shift+Click to multiselect |

---

## Math Overview

### Vector Operations (`vector_math.py`)

- Addition and subtraction
- Scalar multiplication
- Dot product
- Magnitude
- Angle between two vectors
- Normalization

### Transformations (`transformations.py`)

All transformations are implemented as matrix–vector multiplications:

| Transformation | Matrix |
|---|---|
| Rotation by θ | `[[cos θ, -sin θ], [sin θ, cos θ]]` |
| Scale (sx, sy) | `[[sx, 0], [0, sy]]` |
| Reflect on x-axis | `[[1, 0], [0, -1]]` |
| Reflect on y-axis | `[[-1, 0], [0, 1]]` |
| Shear x by k | `[[1, k], [0, 1]]` |
| Shear y by k | `[[1, 0], [k, 1]]` |

---

## Contributing

Pull requests are welcome! If you'd like to add new transformations (e.g., projection, shear) or extend to 3D, feel free to open an issue first to discuss the approach.

---

## License

This project is open source.

---

## Author

**Raghu Ram** — [github.com/Raghu-ram12](https://github.com/Raghu-ram12)