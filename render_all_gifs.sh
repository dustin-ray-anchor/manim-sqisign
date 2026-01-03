#!/bin/bash

# Render all manim scenes as GIFs in medium quality
# Usage: ./render_all_gifs.sh

echo "Rendering all scenes as GIFs in medium quality (720p30)..."
echo "=========================================================="
echo ""

# Array of scene_file:ClassName pairs
scenes=(
    "scenes/degree.py:Degree"
    "scenes/kernels.py:Kernels"
    "scenes/endomorphisms.py:Endomorphisms"
    "scenes/isogeny_morphism.py:IsogenyMorphism"
    "scenes/ideal_reveal.py:IdealReveal"
    "scenes/deuring_correspondence.py:DeuringCorrespondence"
    "scenes/dimension2.py:Dimension2Lifting"
    "scenes/dimensional_lifting.py:DimensionalLifting"
    "scenes/elliptic_curve_algebra.py:EllipticCurveAlgebra"
    "scenes/maze_metaphor.py:MazeMetaphor"
    "scenes/path_hardness.py:PathFindingHardness"
    "scenes/sqisign_protocol.py:SQIsignProtocolOverview"
)

total=${#scenes[@]}
current=0

for scene_pair in "${scenes[@]}"; do
    current=$((current + 1))
    file="${scene_pair%%:*}"
    class="${scene_pair##*:}"

    echo "[$current/$total] Rendering $class from $file..."
    manim -qm --format gif "$file" "$class"

    if [ $? -eq 0 ]; then
        echo "✓ $class completed successfully"
    else
        echo "✗ $class failed"
    fi
    echo ""
done

echo "=========================================================="
echo "All renders complete!"
echo "GIFs are in: media/videos/*/720p30/*.gif"
