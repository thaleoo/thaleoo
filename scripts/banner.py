"""Animated SVG header: name + a self-drawing Lorenz attractor (CSS stroke animation)."""
import sys

import numpy as np

out = sys.argv[1]
sigma, rho, beta, dt = 10.0, 28.0, 8.0 / 3.0, 0.006
v = np.array([1.0, 1.0, 1.05])
pts = []
for i in range(7000):
    x, y, z = v
    def f(v):
        x, y, z = v
        return np.array([sigma * (y - x), x * (rho - z) - y, x * y - beta * z])
    k1 = f(v); k2 = f(v + dt / 2 * k1); k3 = f(v + dt / 2 * k2); k4 = f(v + dt * k3)
    v = v + dt / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
    if i > 200 and i % 3 == 0:
        pts.append(v.copy())
P = np.array(pts)
# project (x, z) into the right side of the banner
cx, cy, s = 960, 168, 4.6
X = cx + P[:, 0] * s * 1.35
Y = cy + 125 - P[:, 2] * s * 1.0
d = "M" + " L".join(f"{a:.1f},{b:.1f}" for a, b in zip(X, Y))
seg = np.hypot(np.diff(X), np.diff(Y)).sum()

dots = "".join(
    f'<circle cx="{x}" cy="{y}" r="1" />' for x in range(40, 1200, 32) for y in range(24, 320, 32)
)

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="320" viewBox="0 0 1200 320" role="img" aria-label="Thaleo Osorio — mathematics, physics and systems programming">
  <defs>
    <linearGradient id="trail" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#a58bff"/>
      <stop offset="50%" stop-color="#58c4dc"/>
      <stop offset="100%" stop-color="#ff7a45"/>
    </linearGradient>
    <radialGradient id="glow" cx="80%" cy="50%" r="45%">
      <stop offset="0%" stop-color="#ff7a45" stop-opacity="0.10"/>
      <stop offset="100%" stop-color="#0d1117" stop-opacity="0"/>
    </radialGradient>
    <clipPath id="card"><rect width="1200" height="320" rx="18"/></clipPath>
  </defs>
  <style>
    .sans {{ font-family: Inter, "Segoe UI", -apple-system, Helvetica, Arial, sans-serif; }}
    .mono {{ font-family: "JetBrains Mono", "SFMono-Regular", Menlo, Consolas, "DejaVu Sans Mono", monospace; }}
    .trail {{ stroke-dasharray: {seg:.0f}; stroke-dashoffset: {seg:.0f}; animation: draw 14s ease-in-out infinite; }}
    .ghost {{ opacity: .10; }}
    .fade {{ opacity: 0; animation: in 1.2s ease-out forwards; }}
    .d1 {{ animation-delay: .2s; }} .d2 {{ animation-delay: .6s; }} .d3 {{ animation-delay: 1s; }} .d4 {{ animation-delay: 1.4s; }}
    .blink {{ animation: blink 1.1s steps(1) infinite; }}
    @keyframes draw {{ 0% {{ stroke-dashoffset: {seg:.0f}; }} 70% {{ stroke-dashoffset: 0; }} 88% {{ stroke-dashoffset: 0; opacity: 1; }} 100% {{ stroke-dashoffset: 0; opacity: 0; }} }}
    @keyframes in {{ from {{ opacity: 0; transform: translateY(6px); }} to {{ opacity: 1; transform: none; }} }}
    @keyframes blink {{ 50% {{ opacity: 0; }} }}
    @media (prefers-reduced-motion: reduce) {{ .trail {{ animation: none; stroke-dashoffset: 0; }} .fade {{ animation: none; opacity: 1; }} }}
  </style>
  <g clip-path="url(#card)">
    <rect width="1200" height="320" fill="#0d1117"/>
    <g fill="#21262d">{dots}</g>
    <rect width="1200" height="320" fill="url(#glow)"/>
    <path d="{d}" fill="none" stroke="#e6edf3" stroke-width="0.8" class="ghost"/>
    <path d="{d}" fill="none" stroke="url(#trail)" stroke-width="1.4" stroke-linecap="round" class="trail"/>
  </g>
  <rect x="0.5" y="0.5" width="1199" height="319" rx="18" fill="none" stroke="#30363d"/>

  <text x="64" y="88" class="mono fade d1" font-size="15" fill="#ff7a45">~/thaleo <tspan fill="#8b949e">$ whoami</tspan></text>
  <text x="62" y="152" class="sans fade d2" font-size="58" font-weight="800" fill="#e6edf3" letter-spacing="-1">Thaleo Osorio</text>
  <text x="64" y="190" class="sans fade d3" font-size="19" fill="#8b949e">Mathematics · Computational Physics · Systems Programming · Cryptography</text>
  <text x="64" y="252" class="mono fade d4" font-size="14" fill="#58c4dc">Biological Engineering @ UNAL · Rust · Python · Typst<tspan fill="#ff7a45" class="blink"> ▍</tspan></text>
  <text x="1136" y="292" class="mono" font-size="12" fill="#8b949e" text-anchor="end">dx/dt = σ(y−x) · dy/dt = x(ρ−z)−y · dz/dt = xy−βz</text>
</svg>
'''
open(out, "w").write(svg)
print(out, len(svg) // 1024, "KiB")
