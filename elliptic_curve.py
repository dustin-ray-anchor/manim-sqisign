"""
Elliptic Curve visualization classes for Manim

Provides:
- EllipticCurveIcon: Stylized closed curve for diagrams (recommended for most uses)
- EllipticCurveIconWithFill: Same with fill support
- EllipticCurve: Mathematically accurate curve with separate branches
- EllipticCurveWithFill: Same with fill support
"""

from manim import *
import numpy as np


def preset_curve(name: str) -> tuple[float, float]:
    """Return (a, b) parameters for common curves."""
    presets = {
        "secp256k1": (0, 7),
        "simple": (-1, 1),
        "smooth": (-2, 2),
    }
    return presets.get(name, (-1, 1))


# =============================================================================
# STYLIZED ICON CLASSES (Recommended for diagrams)
# =============================================================================


class EllipticCurveIcon(VMobject):
    """
    A stylized elliptic curve icon for diagrams.

    Draws a smooth, closed curve that captures the characteristic
    elliptic curve shape without any gaps or connecting lines.
    Perfect for small diagram nodes where you want something that
    "looks like an elliptic curve" without mathematical accuracy.

    Parameters:
        shape: Controls curve appearance (0=circular, 1=classic, 2=elongated)
    """

    def __init__(
        self,
        color: str = BLUE,
        fill_color: str | None = None,
        fill_opacity: float = 0.0,
        stroke_width: float = 3,
        shape: float = 1.0,
        **kwargs
    ):
        self.base_fill_opacity = fill_opacity
        self.shape = shape
        super().__init__(
            color=color,
            fill_color=fill_color or color,
            fill_opacity=fill_opacity,
            stroke_width=stroke_width,
            **kwargs
        )

    def generate_points(self):
        """Generate a stylized elliptic curve shape."""
        t = np.linspace(0, 2 * np.pi, 300)
        s = self.shape

        # Asymmetric oval that evokes the classic elliptic curve look
        x = np.cos(t) - 0.2 * s * np.cos(2 * t)
        y = np.sin(t) * (1 + 0.3 * s * np.cos(t))

        points = np.column_stack([x, y, np.zeros_like(t)])
        self.set_points_smoothly(points)

        return self

    def set_opacity(self, opacity: float, family: bool = True):
        """Set opacity for stroke (and fill if present)."""
        self.set_stroke(opacity=opacity)
        if self.base_fill_opacity > 0:
            self.set_fill(opacity=opacity * self.base_fill_opacity)
        return self


class EllipticCurveIconWithFill(VMobject):
    """
    Stylized elliptic curve icon with fill support.
    Handles opacity properly for both stroke and fill.
    """

    def __init__(
        self,
        color: str = BLUE,
        fill_color: str | None = None,
        fill_opacity: float = 0.3,
        stroke_width: float = 3,
        shape: float = 1.0,
        **kwargs
    ):
        self.base_fill_opacity = fill_opacity
        self.shape = shape
        super().__init__(
            color=color,
            fill_color=fill_color or color,
            fill_opacity=fill_opacity,
            stroke_width=stroke_width,
            **kwargs
        )

    def generate_points(self):
        """Generate a stylized elliptic curve shape."""
        t = np.linspace(0, 2 * np.pi, 300)
        s = self.shape

        x = np.cos(t) - 0.2 * s * np.cos(2 * t)
        y = np.sin(t) * (1 + 0.3 * s * np.cos(t))

        points = np.column_stack([x, y, np.zeros_like(t)])
        self.set_points_smoothly(points)

        return self

    def set_opacity(self, opacity: float, family: bool = True):
        """Properly set opacity for BOTH stroke and fill."""
        self.set_stroke(opacity=opacity)
        self.set_fill(opacity=opacity * self.base_fill_opacity)
        return self


# =============================================================================
# MATHEMATICALLY ACCURATE CLASSES (Use when accuracy matters)
# =============================================================================


class EllipticCurve(VGroup):
    """
    Renders a mathematically accurate elliptic curve y² = x³ + ax + b.

    Creates separate branches where the curve exists (no connecting lines).
    Each branch (bounded oval or unbounded) is drawn independently.

    Use EllipticCurveIcon for diagrams; use this when you need the real curve.
    """

    def __init__(
        self,
        a: float = -1,
        b: float = 1,
        x_min: float = -3,
        x_max: float = 3,
        num_points: int = 200,
        color: str = BLUE,
        stroke_width: float = 3,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.a = a
        self.b = b
        self.x_min = x_min
        self.x_max = x_max
        self.num_points = num_points
        self.curve_color = color
        self.curve_stroke_width = stroke_width

        self._create_curve()

    def _f(self, x):
        """Compute x³ + ax + b."""
        return x**3 + self.a * x + self.b

    def _find_intervals(self) -> list[tuple[float, float]]:
        """Find x-intervals where the curve exists (where x³ + ax + b ≥ 0)."""
        x_test = np.linspace(self.x_min, self.x_max, 2000)
        y_vals = self._f(x_test)
        valid = y_vals >= 0

        transitions = np.where(np.diff(valid.astype(int)) != 0)[0]

        intervals = []
        in_valid = valid[0]
        start = self.x_min if in_valid else None

        for idx in transitions:
            x_transition = (x_test[idx] + x_test[idx + 1]) / 2
            if in_valid:
                intervals.append((start, x_transition))
                start = None
            else:
                start = x_transition
            in_valid = not in_valid

        if in_valid and start is not None:
            intervals.append((start, self.x_max))

        return intervals

    def _create_branch(self, x_start: float, x_end: float) -> VGroup:
        """Create one branch of the curve (separate upper and lower curves, NO connecting lines)."""
        x_vals = np.linspace(x_start, x_end, self.num_points)

        y_squared = self._f(x_vals)
        y_squared = np.maximum(y_squared, 0)
        y_vals = np.sqrt(y_squared)

        # Upper branch as separate curve
        upper_points = np.column_stack([x_vals, y_vals, np.zeros_like(x_vals)])
        upper_branch = VMobject(color=self.curve_color, stroke_width=self.curve_stroke_width)
        upper_branch.set_points_as_corners(upper_points)
        upper_branch.make_smooth()
        upper_branch.set_fill(opacity=0)  # NO FILL

        # Lower branch as separate curve
        lower_points = np.column_stack([x_vals, -y_vals, np.zeros_like(x_vals)])
        lower_branch = VMobject(color=self.curve_color, stroke_width=self.curve_stroke_width)
        lower_branch.set_points_as_corners(lower_points)
        lower_branch.make_smooth()
        lower_branch.set_fill(opacity=0)  # NO FILL

        # Return both curves together (but NOT connected)
        return VGroup(upper_branch, lower_branch)

    def _create_curve(self):
        """Create all branches of the curve."""
        intervals = self._find_intervals()

        for x_start, x_end in intervals:
            if x_end - x_start < 0.01:
                continue
            branch = self._create_branch(x_start, x_end)
            self.add(branch)

    def set_opacity(self, opacity: float, family: bool = True):
        """Set opacity for all branches (upper and lower)."""
        for branch_group in self.submobjects:
            for curve in branch_group.submobjects:
                curve.set_stroke(opacity=opacity)
        return self

    def set_color(self, color, family: bool = True):
        """Set color for all branches (upper and lower)."""
        self.curve_color = color
        for branch_group in self.submobjects:
            for curve in branch_group.submobjects:
                curve.set_stroke(color=color)
        return self


class EllipticCurveWithFill(VGroup):
    """
    Mathematically accurate elliptic curve with fill.
    Each branch is filled independently.
    """

    def __init__(
        self,
        a: float = -1,
        b: float = 1,
        x_min: float = -3,
        x_max: float = 3,
        num_points: int = 200,
        color: str = BLUE,
        fill_color: str | None = None,
        fill_opacity: float = 0.3,
        stroke_width: float = 3,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.a = a
        self.b = b
        self.x_min = x_min
        self.x_max = x_max
        self.num_points = num_points
        self.curve_color = color
        self.curve_fill_color = fill_color or color
        self.base_fill_opacity = fill_opacity
        self.curve_stroke_width = stroke_width

        self._create_curve()

    def _f(self, x):
        return x**3 + self.a * x + self.b

    def _find_intervals(self) -> list[tuple[float, float]]:
        x_test = np.linspace(self.x_min, self.x_max, 2000)
        y_vals = self._f(x_test)
        valid = y_vals >= 0

        transitions = np.where(np.diff(valid.astype(int)) != 0)[0]

        intervals = []
        in_valid = valid[0]
        start = self.x_min if in_valid else None

        for idx in transitions:
            x_transition = (x_test[idx] + x_test[idx + 1]) / 2
            if in_valid:
                intervals.append((start, x_transition))
                start = None
            else:
                start = x_transition
            in_valid = not in_valid

        if in_valid and start is not None:
            intervals.append((start, self.x_max))

        return intervals

    def _create_branch(self, x_start: float, x_end: float) -> VMobject:
        x_vals = np.linspace(x_start, x_end, self.num_points)

        y_squared = self._f(x_vals)
        y_squared = np.maximum(y_squared, 0)
        y_vals = np.sqrt(y_squared)

        upper_points = np.column_stack([x_vals, y_vals, np.zeros_like(x_vals)])
        lower_points = np.column_stack(
            [x_vals[::-1], -y_vals[::-1], np.zeros_like(x_vals)]
        )

        all_points = np.vstack([upper_points, lower_points])

        branch = VMobject(
            color=self.curve_color,
            fill_color=self.curve_fill_color,
            fill_opacity=self.base_fill_opacity,
            stroke_width=self.curve_stroke_width,
        )
        branch.set_points_smoothly(all_points)

        return branch

    def _create_curve(self):
        intervals = self._find_intervals()

        for x_start, x_end in intervals:
            if x_end - x_start < 0.01:
                continue
            branch = self._create_branch(x_start, x_end)
            self.add(branch)

    def set_opacity(self, opacity: float, family: bool = True):
        """Properly set opacity for BOTH stroke and fill on all branches."""
        for branch in self.submobjects:
            branch.set_stroke(opacity=opacity)
            branch.set_fill(opacity=opacity * self.base_fill_opacity)
        return self

    def set_color(self, color, family: bool = True):
        self.curve_color = color
        for branch in self.submobjects:
            branch.set_stroke(color=color)
        return self

    def set_fill(self, color=None, opacity=None, family=True):
        for branch in self.submobjects:
            branch.set_fill(color=color, opacity=opacity)
        return self

    def set_stroke(self, color=None, width=None, opacity=None, family=True):
        for branch in self.submobjects:
            branch.set_stroke(color=color, width=width, opacity=opacity)
        return self
