# SQIsign Visualization Library

This repository contains educational animations explaining the SQIsign post-quantum signature scheme using the [Manim](https://www.manim.community/) animation library.

**Purpose:** These visualizations are designed for expert review to ensure mathematical accuracy and pedagogical effectiveness. Each animation breaks down complex cryptographic concepts into intuitive visual representations.

---

## Table of Contents

- [Foundation: Elliptic Curves and Isogenies](#foundation-elliptic-curves-and-isogenies)
- [Quaternion Algebra](#quaternion-algebra)
- [Advanced Theory](#advanced-theory)
- [The SQIsign Protocol](#the-sqisign-protocol)
- [Running the Scenes](#running-the-scenes)

---

## Foundation: Elliptic Curves and Isogenies

### Elliptic Curves as Algebraic Objects

**File:** `scenes/elliptic_curve_algebra.py`
**Class:** `EllipticCurveAlgebra`

Introduces elliptic curves beyond simple node graphs, emphasizing their algebraic structure as objects with a group law. Shows how points combine under addition and demonstrates the geometric interpretation of the group operation.

![Elliptic Curve Algebra](media/videos/elliptic_curve_algebra/480p15/EllipticCurveAlgebra_ManimCE_v0.19.1.gif)

**Run:** `manim -pql scenes/elliptic_curve_algebra.py EllipticCurveAlgebra`

---

### Isogenies as Structure-Preserving Maps

**File:** `scenes/isogeny_morphism.py`
**Class:** `IsogenyMorphism`

Demonstrates how isogenies respect the group law: φ(P + Q) = φ(P) + φ(Q). Visualizes isogenies as morphisms between elliptic curves that preserve the algebraic structure.

![Isogeny Morphism](media/videos/isogeny_morphism/480p15/IsogenyMorphism_ManimCE_v0.19.1.gif)

**Run:** `manim -pql scenes/isogeny_morphism.py IsogenyMorphism`

---

### Kernels: What Determines an Isogeny

**File:** `scenes/kernels.py`
**Class:** `Kernels`

Explains how the kernel uniquely determines an isogeny. Shows that knowing which points map to the identity on the target curve completely specifies the isogeny (Vélu's formulas).

![Kernels](media/videos/kernels/480p15/Kernels_ManimCE_v0.19.1.gif)

**Run:** `manim -pql scenes/kernels.py Kernels`

---

### Degree: The Fundamental Measure of an Isogeny

**File:** `scenes/degree.py`
**Class:** `Degree`

Introduces the degree of an isogeny as the size of its kernel. Explains how degree measures the "size" or "complexity" of the map between curves.

![Degree](media/videos/degree/480p15/Degree_ManimCE_v0.19.1.gif)

**Run:** `manim -pql scenes/degree.py Degree`

---

### Endomorphisms: Self-Maps of Elliptic Curves

**File:** `scenes/endomorphisms.py`
**Class:** `Endomorphisms`

Visualizes endomorphisms as isogenies from a curve to itself. Shows how the endomorphism ring captures the symmetries of an elliptic curve.

![Endomorphisms](media/videos/endomorphisms/480p15/Endomorphisms_ManimCE_v0.19.1.gif)

**Run:** `manim -pql scenes/endomorphisms.py Endomorphisms`

---

## Quaternion Algebra

### Quaternion Sphere: Visualizing i, j, k

**File:** `scenes/quaternion_sphere.py`
**Class:** `QuaternionSphere`

Interactive visualization of Hamilton's quaternions on the unit sphere. Shows how quaternion units i, j, k form orthogonal axes and how any unit quaternion can be represented as a point on the sphere.

![Quaternion Sphere](media/videos/quaternion_sphere/480p15/QuaternionSphere_ManimCE_v0.19.1.gif)

**Run:** `manim -pql scenes/quaternion_sphere.py QuaternionSphere`

---

### Quaternion Algebra B_{p,∞}

**File:** `scenes/quaternion_algebra.py`
**Class:** `QuaternionAlgebra`

Demonstrates the transformation from Hamilton's quaternions to the ramified quaternion algebra B_{p,∞} used in SQIsign. Visualizes how changing j² = -1 to j² = -p compresses the sphere into an ellipsoid.

![Quaternion Algebra](media/videos/quaternion_algebra/720p30/QuaternionAlgebra_ManimCE_v0.19.1.gif)

**Run:** `manim -pql scenes/quaternion_algebra.py QuaternionAlgebra`

---

### Maximal Orders: Lattices in Quaternion Algebras

**File:** `scenes/maximal_order.py`
**Class:** `MaximalOrder`

Visualizes maximal orders as discrete lattices within the quaternion algebra. Shows the analogy to Gaussian integers ℤ[i] ⊂ ℂ and introduces the concept of ideals as sub-lattices.

![Maximal Order](media/videos/maximal_order/720p30/MaximalOrder_ManimCE_v0.19.1.gif)

**Run:** `manim -pql scenes/maximal_order.py MaximalOrder`

---

### Torsion Points: E[N] as a Coordinate Grid

**File:** `scenes/torsion_points.py`
**Class:** `TorsionPoints`

Represents N-torsion subgroups E[N] ≅ (ℤ/Nℤ)² as a 2D grid with basis {P, Q}. Shows how cyclic subgroups form lines through this grid and how they correspond to isogeny kernels. Explains the compact encoding of isogenies via kernel generators.

![Torsion Points](media/videos/torsion_points/480p15/TorsionPoints_ManimCE_v0.19.1.gif)

**Run:** `manim -pql scenes/torsion_points.py TorsionPoints`

---

## Advanced Theory

### The Deuring Correspondence

**File:** `scenes/deuring_correspondence.py`
**Class:** `DeuringCorrespondence`

Visualizes the Deuring correspondence: the bijection between left ideals of maximal orders in the quaternion algebra and isogenies between supersingular elliptic curves.

![Deuring Correspondence](media/videos/deuring_correspondence/480p15/DeuringCorrespondence_ManimCE_v0.19.1.gif)

**Run:** `manim -pql scenes/deuring_correspondence.py DeuringCorrespondence`

---

### Dimensional Lifting: SQIsign v2.0

**File:** `scenes/dimensional_lifting.py`
**Class:** `DimensionalLifting`

Explains the dimensional lifting optimization in SQIsign 2.0 that reduces signature size by working with higher-dimensional isogenies.

![Dimensional Lifting](media/videos/dimensional_lifting/480p15/DimensionalLifting_ManimCE_v0.19.1.gif)

**Run:** `manim -pql scenes/dimensional_lifting.py DimensionalLifting`

---

## The SQIsign Protocol

### The Maze Metaphor: 30-Second Overview

**File:** `scenes/maze_metaphor.py`
**Class:** `MazeMetaphor`

A high-level intuitive explanation of SQIsign using a maze metaphor: secret knowledge is a "magic thread" through a complex isogeny graph, while verification only requires checking endpoints.

![Maze Metaphor](media/videos/maze_metaphor/480p15/MazeMetaphor_ManimCE_v0.19.1.gif)

**Run:** `manim -pql scenes/maze_metaphor.py MazeMetaphor`

---

### Path Finding Hardness

**File:** `scenes/path_hardness.py`
**Class:** `PathFindingHardness`

Demonstrates why finding paths in the isogeny graph is computationally hard without additional structure, forming the basis of SQIsign's security.

![Path Finding Hardness](media/videos/path_hardness/480p15/PathFindingHardness_ManimCE_v0.19.1.gif)

**Run:** `manim -pql scenes/path_hardness.py PathFindingHardness`

---

### Secret Ideal Reveal: Making Path-Finding Tractable

**File:** `scenes/ideal_reveal.py`
**Class:** `IdealReveal`

Shows how revealing the secret ideal (quaternion algebra element) makes path computation tractable. Demonstrates the key insight that knowledge of the corresponding ideal enables efficient isogeny evaluation.

![Ideal Reveal](media/videos/ideal_reveal/720p30/IdealReveal_ManimCE_v0.19.1.gif)

**Run:** `manim -pql scenes/ideal_reveal.py IdealReveal`

---

### Complete SQIsign Protocol

**File:** `scenes/sqisign_protocol.py`
**Class:** `SQIsignProtocolOverview`

Complete visualization of the SQIsign sigma protocol showing the commitment, challenge, and response phases. Demonstrates how the protocol achieves special soundness and honest-verifier zero-knowledge.

![SQIsign Protocol](media/videos/sqisign_protocol/720p30/SQIsignProtocolOverview_ManimCE_v0.19.1.gif)

**Run:** `manim -pql scenes/sqisign_protocol.py SQIsignProtocolOverview`

---

## Running the Scenes

### Prerequisites

```bash
pip install manim
```

### Render Commands

**Low quality (fast preview):**
```bash
manim -pql scenes/<filename>.py <ClassName>
```

**High quality (publication):**
```bash
manim -pqh scenes/<filename>.py <ClassName>
```

**Generate GIF:**
```bash
manim -ql --format=gif scenes/<filename>.py <ClassName>
```

### Output Location

Rendered videos and GIFs are saved to:
```
media/videos/<scene_name>/<quality>/
```

---

## Project Structure

```
manim-sqisign/
├── scenes/              # All animation scenes
├── media/              # Generated videos and GIFs
│   └── videos/
├── SCENE_CREATION_GUIDE.md  # Style guide for creating new scenes
└── README.md           # This file
```

---

## Contributing

When creating new scenes, please follow the conventions in `SCENE_CREATION_GUIDE.md`:
- Use the standard color scheme
- Minimum font sizes (24+ for indicators, 28-32+ for main text)
- No titles at the top (use step indicators in upper-left corner)
- Prefer edit operations over creating new files

---

## Feedback and Review

This library is intended for expert review. We welcome feedback on:
- **Mathematical accuracy:** Corrections to any conceptual errors
- **Pedagogical clarity:** Suggestions for improving explanations
- **Visual effectiveness:** Ideas for better visual representations
- **Technical details:** Missing nuances or oversimplifications

---

## References

- [SQIsign Paper](https://eprint.iacr.org/2020/1240)
- [Manim Community Documentation](https://docs.manim.community/)
