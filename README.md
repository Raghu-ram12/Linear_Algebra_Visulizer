# Linear Algebra Visualizer

An interactive desktop application for visualizing **3D vectors and linear transformations**, built with Python and Tkinter. Plot vectors in 3D space, rotate the camera freely, and apply transformations — all with zero external dependencies.

---

## Features

- **3D Vector Plotting** — Add vectors by entering (x, y, z) components; each is drawn as a color-coded arrow from the origin
- **Interactive Camera** — Rotate the scene along X, Y, and Z axes using sliders; zoom from 5 to 60 pixels per unit
- **Isometric Projection** — Scene renders in isometric view by default with color-coded axes (X: blue, Y: red, Z: green) and dashed negative-axis indicators
- **Toggle Grid** — Show or hide a reference grid on the XZ plane
- **Transformations** — Apply to one or multiple selected vectors at once:
  - **Rotate** — About the X, Y, or Z axis by any angle
  - **Scale** — Independent sx, sy, sz scale factors
  - **Reflect** — Across the XY, YZ, or XZ plane
- **Multiselect** — Ctrl+Click or Shift+Click to select multiple vectors and batch-transform them
- **Highlight on Select** — Selected vectors render with a white halo
- **Rename Vectors** — Rename any vector via a themed dialog
- **Info Panel** — Shows name, components, and magnitude of the selected vector in real time
- **Status Bar** — Contextual feedback for every action
- **Keyboard Shortcuts** — `Delete` removes selected vectors; `Escape` closes open input panels

---

## Project Structure

```
Linear_Algebra_Visulizer/
├── 3d_renderer.py       # Core app — Render (projection, drawing) and UI (all controls) classes
├── transformations.py   # 3D transformation logic (rotation, scale, reflect, Euler rotation)
├── vector_math.py       # Vector class and operations (add, sub, dot, cross, magnitude, normalize)
├── matrix_math.py       # Matrix class and operations (mul, add, sub, identity, determinant)
├── state.py             # Global constants (window size, panel width, draw scale)
├── logo.ico             # App icon
└── linear-algebra-visualizer-guide.pdf   # User guide
```

---

## Getting Started

### Prerequisites

- Python 3.7+
- Tkinter (bundled with standard Python on Windows and macOS; on Linux: `sudo apt install python3-tk`)

### Installation

```bash
git clone https://github.com/Raghu-ram12/Linear_Algebra_Visulizer.git
cd Linear_Algebra_Visulizer
```

No additional dependencies required.

### Running the App

```bash
python 3d_renderer.py
```

---

## Usage

### Adding a Vector

Enter X, Y, Z values in the **Add Vector** section and click **＋ Add Vector**.

### Transforming Vectors

1. Select one or more vectors from the **Vectors** list
2. Click **Scale**, **Rotate**, or **Reflect** in the **Transform Selected** section
3. Fill in the parameters and click Apply

### Camera Controls

Use the **Rotate X / Y / Z** sliders in the **View** section to orbit the scene. Click **Reset View** to return to the default isometric perspective (X: 35.26°, Y: 45°, Z: 0°).

### Keyboard Shortcuts

| Key | Action |
|---|---|
| `Delete` | Delete selected vector(s) |
| `Escape` | Close the open transform input panel |

---

## Math Reference

### Transformations (`transformations.py`)

All transformations are matrix–vector multiplications.

**Rotation about an axis by θ:**

| Axis | Matrix |
|---|---|
| X | `[[1,0,0], [0,cosθ,−sinθ], [0,sinθ,cosθ]]` |
| Y | `[[cosθ,0,sinθ], [0,1,0], [−sinθ,0,cosθ]]` |
| Z | `[[cosθ,−sinθ,0], [sinθ,cosθ,0], [0,0,1]]` |

Euler rotation (ZYX order) is also available via `rotate_vector_euler(v, gamma, beta, alpha)`.

**Scaling:**
```
[[sx, 0,  0 ],
 [0,  sy, 0 ],
 [0,  0,  sz]]
```

**Reflection:**

| Plane | Effect |
|---|---|
| XY | Negates Z |
| YZ | Negates X |
| XZ | Negates Y |

### Vector Operations (`vector_math.py`)

| Function | Description |
|---|---|
| `add_vectors(a, b)` | Component-wise addition |
| `sub_vectors(a, b)` | Component-wise subtraction |
| `multiply_scaler(a, k)` | Scalar multiplication |
| `dot_product(a, b)` | Dot product |
| `cross_product(a, b)` | Cross product (3D) |
| `magnitude(a)` | Euclidean length |
| `Vector_angle(a, b)` | Angle between two vectors (radians) |
| `normalize(a)` | Unit vector |

### Matrix Operations (`matrix_math.py`)

| Function | Description |
|---|---|
| `matrix_mul(a, b)` | Matrix multiplication |
| `add_matrices(a, b)` | Element-wise addition |
| `sub_matrices(a, b)` | Element-wise subtraction |
| `multiply_matrix_by_scaler(a, k)` | Scalar multiplication |
| `multiply_matrix_vector(v, m)` | Apply matrix to vector |
| `identity_matrix(n)` | n×n identity matrix |
| `zero_matrix(n)` | n×n zero matrix |
| `determinant_2x2(m)` | Determinant of a 2×2 matrix |

---

## Roadmap

- [ ] Display vector magnitude labels on canvas
- [ ] Draw resultant vector when adding two selected vectors
- [ ] Show angle and dot product between two selected vectors
- [ ] Animate scaling transformations
- [ ] Custom matrix input — apply any user-defined 3×3 transformation
- [ ] Show the span of a vector (full line through origin)
- [ ] Linear independence checker
- [ ] Grid transformation animation (3Blue1Brown style)
- [ ] Eigenvalue / eigenvector visualization

---

## Author

**Raghu Ram** — [github.com/Raghu-ram12](https://github.com/Raghu-ram12)

---

## License

This project is open source.
