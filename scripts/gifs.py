"""Generate the scientific GIFs for Thaleo's GitHub profile README.

Each GIF is rendered frame-by-frame with matplotlib and encoded with an
ffmpeg two-pass palette (palettegen/paletteuse) to keep files small.

Usage: python3 gifs.py <outdir> [ising|lorenz|zeta|all]
"""
import os
import shutil
import subprocess
import sys
import tempfile

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.colors import LinearSegmentedColormap, ListedColormap
import numpy as np

# ---- shared visual identity ----------------------------------------------
BG = "#0d1117"
PANEL = "#161b22"
GRID = "#21262d"
TEXT = "#e6edf3"
MUTED = "#8b949e"
ORANGE = "#ff7a45"
CYAN = "#58c4dc"
VIOLET = "#a58bff"

plt.rcParams.update({
    "font.family": "DejaVu Sans Mono",
    "text.color": TEXT,
    "axes.edgecolor": GRID,
    "axes.labelcolor": MUTED,
    "xtick.color": MUTED,
    "ytick.color": MUTED,
})

DPI = 100


def encode(frame_dir, out_path, fps, width, colors=128):
    palette = os.path.join(frame_dir, "palette.png")
    pattern = os.path.join(frame_dir, "f%04d.png")
    scale = f"fps={fps},scale={width}:-1:flags=lanczos"
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-framerate", str(fps), "-i", pattern,
                    "-vf", f"{scale},palettegen=max_colors={colors}:stats_mode=diff", palette], check=True)
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-framerate", str(fps), "-i", pattern, "-i", palette,
                    "-lavfi", f"{scale}[x];[x][1:v]paletteuse=dither=bayer:bayer_scale=4:diff_mode=rectangle",
                    "-loop", "0", out_path], check=True)
    print(f"{out_path}: {os.path.getsize(out_path)/1024:.0f} KiB")


def title(fig, text, sub):
    fig.text(0.045, 0.94, text, fontsize=15, color=TEXT, weight="bold", va="center")
    fig.text(0.045, 0.885, sub, fontsize=9.5, color=MUTED, va="center")


# ---- 1. 2D Ising model: Metropolis annealing through T_c ------------------
def ising(outdir):
    rng = np.random.default_rng(7)
    L = 150
    s = rng.choice([-1, 1], size=(L, L)).astype(np.int8)
    ii, jj = np.indices((L, L))
    masks = [((ii + jj) % 2 == p) for p in (0, 1)]
    Tc = 2.0 / np.log(1 + np.sqrt(2))

    def sweep(s, beta):
        for m in masks:
            nb = (np.roll(s, 1, 0) + np.roll(s, -1, 0) + np.roll(s, 1, 1) + np.roll(s, -1, 1))
            dE = 2 * s * nb
            acc = (dE <= 0) | (rng.random(s.shape) < np.exp(-beta * dE))
            s[m & acc] *= -1
        return s

    n_frames = 150
    temps = np.concatenate([np.linspace(3.6, Tc, 70), np.linspace(Tc, Tc, 25), np.linspace(Tc, 1.4, 55)])
    cmap = ListedColormap([PANEL, ORANGE])
    mags, Ts = [], []
    tmp = tempfile.mkdtemp()
    for k in range(n_frames):
        T = temps[k]
        for _ in range(3 if T > Tc + 0.05 else 8):
            s = sweep(s, 1.0 / T)
        m = abs(s.mean())
        mags.append(m); Ts.append(T)

        fig = plt.figure(figsize=(6.4, 4.0), dpi=DPI, facecolor=BG)
        title(fig, "2D Ising model", "Metropolis Monte Carlo · checkerboard updates · L = 150")
        ax = fig.add_axes([0.04, 0.05, 0.50, 0.78])
        ax.imshow(s, cmap=cmap, interpolation="nearest", vmin=-1, vmax=1)
        ax.set_xticks([]); ax.set_yticks([])
        for sp in ax.spines.values():
            sp.set_color(GRID)

        ax2 = fig.add_axes([0.66, 0.20, 0.31, 0.50], facecolor=BG)
        Tg = np.linspace(1.3, 3.7, 300)
        exact = np.where(Tg < Tc, np.clip(1 - np.sinh(2 / Tg) ** -4, 0, None) ** 0.125, 0)
        ax2.plot(Tg, exact, color=MUTED, lw=1, ls="--", label="Onsager")
        ax2.plot(Ts, mags, color=ORANGE, lw=1.6, label="simulation")
        ax2.scatter([T], [m], color=ORANGE, s=18, zorder=3)
        ax2.axvline(Tc, color=CYAN, lw=0.8, alpha=0.7)
        ax2.text(Tc + 0.05, 1.02, "T$_c$", color=CYAN, fontsize=9)
        ax2.set_xlim(1.3, 3.7); ax2.set_ylim(-0.03, 1.1)
        ax2.set_xlabel("T  (J / k$_B$)", fontsize=8.5); ax2.set_ylabel("|m|", fontsize=8.5, rotation=0, labelpad=10)
        ax2.tick_params(labelsize=7.5)
        ax2.legend(fontsize=7, frameon=False, loc="upper right", labelcolor=MUTED)
        for sp in ("top", "right"):
            ax2.spines[sp].set_visible(False)
        phase = "paramagnetic" if T > Tc + 0.03 else ("critical" if abs(T - Tc) <= 0.03 else "ferromagnetic")
        fig.text(0.66, 0.80, f"T = {T:5.3f}", fontsize=11, color=TEXT)
        fig.text(0.66, 0.75, phase, fontsize=9, color=CYAN if phase == "critical" else MUTED)
        fig.savefig(os.path.join(tmp, f"f{k:04d}.png"), facecolor=BG)
        plt.close(fig)
    # hold the last frame
    for extra in range(20):
        shutil.copy(os.path.join(tmp, f"f{n_frames-1:04d}.png"), os.path.join(tmp, f"f{n_frames+extra:04d}.png"))
    encode(tmp, os.path.join(outdir, "ising.gif"), fps=15, width=640)
    shutil.rmtree(tmp)


# ---- 2. Lorenz attractor ---------------------------------------------------
def lorenz(outdir):
    sigma, rho, beta = 10.0, 28.0, 8.0 / 3.0

    def f(v):
        x, y, z = v
        return np.array([sigma * (y - x), x * (rho - z) - y, x * y - beta * z])

    dt, N = 0.005, 9000
    trajs = []
    for eps in (0.0, 1e-5):  # two nearby initial conditions → sensitive dependence
        v = np.array([1.0 + eps, 1.0, 1.05])
        P = np.empty((N, 3))
        for i in range(N):
            k1 = f(v); k2 = f(v + dt / 2 * k1); k3 = f(v + dt / 2 * k2); k4 = f(v + dt * k3)
            v = v + dt / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
            P[i] = v
        trajs.append(P)

    cmaps = [LinearSegmentedColormap.from_list("a", [BG, ORANGE]),
             LinearSegmentedColormap.from_list("b", [BG, CYAN])]
    n_frames = 160
    tmp = tempfile.mkdtemp()
    for k in range(n_frames):
        end = int(300 + (N - 300) * (k / (n_frames - 1)) ** 1.15)
        ang = 0.35 + 1.4 * k / n_frames
        fig = plt.figure(figsize=(6.4, 4.0), dpi=DPI, facecolor=BG)
        title(fig, "Lorenz attractor", "σ = 10, ρ = 28, β = 8/3 · RK4 · Δx₀ = 10⁻⁵")
        ax = fig.add_axes([0.0, 0.0, 1.0, 0.84], facecolor=BG)
        for P, cm in zip(trajs, cmaps):
            seg = P[max(0, end - 2600):end]
            X = seg[:, 0] * np.cos(ang) - seg[:, 1] * np.sin(ang)
            Z = seg[:, 2]
            pts = np.column_stack([X, Z]).reshape(-1, 1, 2)
            segs = np.concatenate([pts[:-1], pts[1:]], axis=1)
            lc = LineCollection(segs, cmap=cm, linewidths=1.0)
            lc.set_array(np.linspace(0, 1, len(segs)))
            ax.add_collection(lc)
            ax.scatter([X[-1]], [Z[-1]], color=cm(1.0), s=14, zorder=3)
        ax.set_xlim(-30, 30); ax.set_ylim(-2, 52)
        ax.set_aspect("equal"); ax.axis("off")
        sep = np.linalg.norm(trajs[0][end - 1] - trajs[1][end - 1])
        fig.text(0.70, 0.94, f"t = {end*dt:5.1f}", fontsize=10, color=TEXT, va="center")
        fig.text(0.70, 0.885, f"|Δ| = {sep:9.2e}", fontsize=9, color=MUTED, va="center")
        fig.savefig(os.path.join(tmp, f"f{k:04d}.png"), facecolor=BG)
        plt.close(fig)
    encode(tmp, os.path.join(outdir, "lorenz.gif"), fps=16, width=640, colors=48)
    shutil.rmtree(tmp)


# ---- 3. Riemann zeta on the critical line ---------------------------------
def zeta(outdir):
    import mpmath as mp
    mp.mp.dps = 15
    ts = np.linspace(0.0, 42.0, 2600)
    Z = np.array([complex(mp.zeta(mp.mpc(0.5, t))) for t in ts])
    zeros = [float(mp.im(mp.zetazero(n))) for n in range(1, 7)]  # 14.13, 21.02, 25.01, 30.42, 32.94, 37.59

    n_frames = 150
    tmp = tempfile.mkdtemp()
    cm = LinearSegmentedColormap.from_list("z", [VIOLET, CYAN, ORANGE])
    for k in range(n_frames):
        end = max(2, int(len(ts) * (k + 1) / n_frames))
        t_now = ts[end - 1]
        fig = plt.figure(figsize=(6.4, 4.0), dpi=DPI, facecolor=BG)
        title(fig, "ζ(½ + it)", "Riemann zeta on the critical line · 0 ≤ t ≤ 42")
        ax = fig.add_axes([0.05, 0.05, 0.55, 0.78], facecolor=BG)
        ax.axhline(0, color=GRID, lw=0.8); ax.axvline(0, color=GRID, lw=0.8)
        pts = np.column_stack([Z[:end].real, Z[:end].imag]).reshape(-1, 1, 2)
        segs = np.concatenate([pts[:-1], pts[1:]], axis=1)
        lc = LineCollection(segs, cmap=cm, linewidths=1.3)
        lc.set_array(ts[:end - 1] / ts[-1]); lc.set_clim(0, 1)
        ax.add_collection(lc)
        ax.scatter([Z[end - 1].real], [Z[end - 1].imag], color=TEXT, s=14, zorder=4)
        ax.scatter([0], [0], color=ORANGE, s=22, marker="o", facecolors="none", lw=1.2, zorder=3)
        ax.set_xlim(-2.0, 4.2); ax.set_ylim(-2.6, 2.6)
        ax.set_aspect("equal"); ax.axis("off")

        fig.text(0.66, 0.76, f"t = {t_now:6.2f}", fontsize=11, color=TEXT)
        fig.text(0.66, 0.70, f"|ζ| = {abs(Z[end-1]):5.3f}", fontsize=9, color=MUTED)
        fig.text(0.66, 0.60, "non-trivial zeros", fontsize=9, color=MUTED)
        for i, z0 in enumerate(zeros):
            hit = t_now >= z0
            fig.text(0.66, 0.53 - i * 0.065, f"ρ{i+1} = ½ + {z0:7.4f} i",
                     fontsize=9, color=ORANGE if hit else "#3d444d")
        fig.savefig(os.path.join(tmp, f"f{k:04d}.png"), facecolor=BG)
        plt.close(fig)
    for extra in range(20):
        shutil.copy(os.path.join(tmp, f"f{n_frames-1:04d}.png"), os.path.join(tmp, f"f{n_frames+extra:04d}.png"))
    encode(tmp, os.path.join(outdir, "zeta.gif"), fps=15, width=640)
    shutil.rmtree(tmp)


if __name__ == "__main__":
    out = sys.argv[1]
    which = sys.argv[2] if len(sys.argv) > 2 else "all"
    os.makedirs(out, exist_ok=True)
    for name, fn in (("ising", ising), ("lorenz", lorenz), ("zeta", zeta)):
        if which in (name, "all"):
            fn(out)
