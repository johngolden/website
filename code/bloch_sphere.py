"""Render a labeled Bloch sphere with a sample state vector.

This is a standalone, production-style script. It does not depend on any
notebook environment. Run it from the repo root:

    python code/bloch_sphere.py

It writes ``figures/bloch_sphere.svg``. The script is the single source of
truth for the figure used in the Bloch-sphere post.

Dependencies are pinned in ``requirements.txt`` (numpy, matplotlib).
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401  (registers 3d projection)


# A sample pure state |psi> = cos(theta/2)|0> + e^{i*phi} sin(theta/2)|1>
# placed at (theta, phi) = (pi/3, pi/4) on the sphere.
THETA = np.pi / 3
PHI = np.pi / 4


def bloch_vector(theta: float, phi: float) -> np.ndarray:
    """Return the Bloch-sphere coordinates (x, y, z) for a pure qubit state."""
    return np.array(
        [
            np.sin(theta) * np.cos(phi),
            np.sin(theta) * np.sin(phi),
            np.cos(theta),
        ]
    )


def draw_sphere(ax) -> None:
    u, v = np.mgrid[0 : 2 * np.pi : 60j, 0 : np.pi : 30j]
    x = np.cos(u) * np.sin(v)
    y = np.sin(u) * np.sin(v)
    z = np.cos(v)
    ax.plot_surface(
        x, y, z,
        color="#cfd8dc",
        alpha=0.15,
        linewidth=0,
        antialiased=True,
        rstride=2,
        cstride=2,
    )
    # Wireframe for depth cues.
    ax.plot_wireframe(
        x, y, z,
        color="#90a4ae",
        alpha=0.35,
        linewidth=0.4,
        rstride=6,
        cstride=6,
    )


def draw_axes(ax) -> None:
    arrow_kw = dict(arrow_length_ratio=0.07, linewidth=1.2, color="#37474f")
    ax.quiver(0, 0, 0, 1.25, 0, 0, **arrow_kw)
    ax.quiver(0, 0, 0, 0, 1.25, 0, **arrow_kw)
    ax.quiver(0, 0, 0, 0, 0, 1.25, **arrow_kw)
    ax.text(1.35, 0, 0, r"$x$", fontsize=12, ha="center")
    ax.text(0, 1.35, 0, r"$y$", fontsize=12, ha="center")
    ax.text(0, 0, 1.38, r"$z$", fontsize=12, ha="center")

    # Computational-basis labels.
    ax.text(0, 0, 1.10, r"$|0\rangle$", fontsize=12, ha="center", color="#0b5394")
    ax.text(0, 0, -1.22, r"$|1\rangle$", fontsize=12, ha="center", color="#0b5394")


def draw_state(ax, theta: float, phi: float) -> None:
    v = bloch_vector(theta, phi)
    ax.quiver(
        0, 0, 0, v[0], v[1], v[2],
        arrow_length_ratio=0.10,
        linewidth=2.2,
        color="#c0392b",
    )
    ax.text(
        v[0] * 1.15, v[1] * 1.15, v[2] * 1.15,
        r"$|\psi\rangle$",
        fontsize=13,
        color="#c0392b",
        ha="center",
    )


def main() -> Path:
    fig = plt.figure(figsize=(5.5, 5.5))
    ax = fig.add_subplot(111, projection="3d")
    ax.set_box_aspect((1, 1, 1))

    draw_sphere(ax)
    draw_axes(ax)
    draw_state(ax, THETA, PHI)

    # Cosmetics.
    ax.set_axis_off()
    ax.view_init(elev=18, azim=35)
    ax.set_xlim(-1, 1)
    ax.set_ylim(-1, 1)
    ax.set_zlim(-1, 1)
    fig.tight_layout(pad=0.2)

    out_dir = Path(__file__).resolve().parent.parent / "figures"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "bloch_sphere.svg"
    fig.savefig(out_path, format="svg", bbox_inches="tight")
    plt.close(fig)
    print(f"wrote {out_path}")
    return out_path


if __name__ == "__main__":
    main()
