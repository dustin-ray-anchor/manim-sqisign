"""
Elliptic Curve rendering for Manim
Renders actual elliptic curves (y² = x³ + ax + b) instead of circles
while maintaining compatibility with all Manim animations.
"""

from manim import *
import numpy as np


class EllipticCurve(VMobject):
    """
    Renders an elliptic curve defined by y² = x³ + ax + b.

    This class creates a VMobject that can be used with all standard Manim animations
    like Create(), FadeIn(), Transform(), etc.

    Parameters:
        a (float): Coefficient for x term (default: -1)
        b (float): Constant term (default: 1)
        x_range (tuple): Range for x values (default: (-2.5, 2.5))
        num_points (int): Number of sample points for smooth curve (default: 200)
        color: Manim color for the curve
        stroke_width: Width of the curve line
        **kwargs: Additional VMobject parameters

    Example:
        curve = EllipticCurve(a=-1, b=1, color=BLUE, stroke_width=3)
        self.play(Create(curve))
    """

    def __init__(
        self,
        a=-1,
        b=1,
        x_range=(-2.5, 2.5),
        num_points=200,
        color=BLUE_D,
        stroke_width=3,
        **kwargs
    ):
        super().__init__(**kwargs)

        # Store parameters
        self.a = a
        self.b = b
        self.x_range = x_range

        # Generate x values
        x_vals = np.linspace(x_range[0], x_range[1], num_points)

        # Calculate y² = x³ + ax + b
        y_squared = x_vals**3 + a * x_vals + b

        # Split into regions where curve is real (y² ≥ 0)
        valid_mask = y_squared >= 0

        # Create curve segments
        curves = VGroup()

        # Process continuous segments
        segments = self._get_continuous_segments(x_vals, y_squared, valid_mask)

        for x_seg, y_squared_seg in segments:
            if len(x_seg) > 1:
                # Upper branch - smooth curve through positive y values
                upper_points = np.array([
                    [x, np.sqrt(y2), 0]
                    for x, y2 in zip(x_seg, y_squared_seg)
                ])

                # Lower branch - smooth curve through negative y values
                lower_points = np.array([
                    [x, -np.sqrt(y2), 0]
                    for x, y2 in zip(x_seg, y_squared_seg)
                ])

                # Create one smooth curve for upper branch
                upper_curve = VMobject(color=color, stroke_width=stroke_width, fill_opacity=0)
                upper_curve.set_points_smoothly(upper_points)
                curves.add(upper_curve)

                # Create one smooth curve for lower branch
                lower_curve = VMobject(color=color, stroke_width=stroke_width, fill_opacity=0)
                lower_curve.set_points_smoothly(lower_points)
                curves.add(lower_curve)

        self.add(curves)

        # Center the curve
        self.move_to(ORIGIN)

    def _get_continuous_segments(self, x_vals, y_squared, valid_mask):
        """
        Split the curve into continuous segments where y² ≥ 0.
        Returns list of (x_segment, y_squared_segment) tuples.
        """
        segments = []
        current_x = []
        current_y2 = []

        for x, y2, valid in zip(x_vals, y_squared, valid_mask):
            if valid:
                current_x.append(x)
                current_y2.append(y2)
            else:
                # End of valid segment
                if len(current_x) > 0:
                    segments.append((
                        np.array(current_x),
                        np.array(current_y2)
                    ))
                    current_x = []
                    current_y2 = []

        # Add final segment
        if len(current_x) > 0:
            segments.append((
                np.array(current_x),
                np.array(current_y2)
            ))

        return segments


class EllipticCurveWithFill(EllipticCurve):
    """
    Elliptic curve with a filled region between the branches.
    Useful for replacing Circle objects that had fill_opacity.

    Example:
        curve = EllipticCurveWithFill(
            a=-1, b=1,
            color=BLUE_D,
            fill_opacity=0.3,
            stroke_width=3
        )
    """

    def __init__(
        self,
        a=-1,
        b=1,
        x_range=(-2.5, 2.5),
        num_points=200,
        color=BLUE_D,
        fill_opacity=0.3,
        stroke_width=3,
        **kwargs
    ):
        # Don't call super().__init__ yet, we'll build it ourselves
        VMobject.__init__(self, **kwargs)

        self.a = a
        self.b = b
        self.x_range = x_range

        # Generate points
        x_vals = np.linspace(x_range[0], x_range[1], num_points)
        y_squared = x_vals**3 + a * x_vals + b
        valid_mask = y_squared >= 0

        # Get the main segment (largest continuous region)
        segments = self._get_continuous_segments(x_vals, y_squared, valid_mask)

        if segments:
            # Use the largest segment
            x_seg, y_squared_seg = max(segments, key=lambda s: len(s[0]))

            # Create closed path: upper branch, then lower branch reversed
            upper_points = [
                [x, np.sqrt(y2), 0]
                for x, y2 in zip(x_seg, y_squared_seg)
            ]
            lower_points = [
                [x, -np.sqrt(y2), 0]
                for x, y2 in zip(reversed(x_seg), reversed(y_squared_seg))
            ]

            # Combine into closed shape
            all_points = upper_points + lower_points

            filled_curve = VMobject(
                color=color,
                fill_opacity=fill_opacity,
                stroke_width=stroke_width
            )
            filled_curve.set_points_as_corners(all_points)
            filled_curve.close_path()
            filled_curve.make_smooth()

            self.add(filled_curve)

        self.move_to(ORIGIN)

    def _get_continuous_segments(self, x_vals, y_squared, valid_mask):
        """Inherited from parent class logic"""
        segments = []
        current_x = []
        current_y2 = []

        for x, y2, valid in zip(x_vals, y_squared, valid_mask):
            if valid:
                current_x.append(x)
                current_y2.append(y2)
            else:
                if len(current_x) > 0:
                    segments.append((np.array(current_x), np.array(current_y2)))
                    current_x = []
                    current_y2 = []

        if len(current_x) > 0:
            segments.append((np.array(current_x), np.array(current_y2)))

        return segments


# Preset curves for common use cases
def preset_curve(preset="smooth", **kwargs):
    """
    Create elliptic curves with preset parameters.

    Presets:
        "smooth": Nice smooth curve, good for general use (y² = x³ - x + 1)
        "simple": Simple curve with clear shape (y² = x³ - 3x + 3)
        "wide": Wider curve suitable for labels (y² = x³ - 4x + 4)
        "tall": Taller curve (y² = x³ + 1)

    Example:
        curve = preset_curve("smooth", color=BLUE, stroke_width=3)
        self.play(Create(curve))
    """
    presets = {
        "smooth": {"a": -1, "b": 1, "x_range": (-2, 2.5)},
        "simple": {"a": -3, "b": 3, "x_range": (-2.5, 2.5)},
        "wide": {"a": -4, "b": 4, "x_range": (-2.5, 2.5)},
        "tall": {"a": 0, "b": 1, "x_range": (-2, 2)},
    }

    params = presets.get(preset, presets["smooth"])
    params.update(kwargs)

    return EllipticCurve(**params)
