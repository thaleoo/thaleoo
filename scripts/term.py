"""Render a terminal-session GIF of Cista from real captured CLI output.

Usage: python3 term.py <captured_dir> <out.gif>
"""
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

cap = Path(sys.argv[1])
out = sys.argv[2]

W, H = 800, 370
BG, BAR, TEXT, MUTED = "#0d1117", "#161b22", "#e6edf3", "#8b949e"
ORANGE, CYAN, GREEN = "#ff7a45", "#58c4dc", "#3fb950"
FONT = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", 14)
BOLD = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf", 14)
LH, X0, Y0 = 19, 20, 50
ROWS = (H - Y0 - 12) // LH
CW = FONT.getlength("M")

frames, durations = [], []
screen = []  # list of list[(text, color, font)]


def render(cursor=True):
    im = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, W, 34], fill=BAR)
    for i, c in enumerate(("#ff5f57", "#febc2e", "#28c840")):
        d.ellipse([16 + i * 22, 11, 28 + i * 22, 23], fill=c)
    t = "zsh — cista · encrypted local vaults"
    d.text(((W - FONT.getlength(t)) / 2, 9), t, font=FONT, fill=MUTED)
    rows = screen[-ROWS:]
    y = Y0
    for r_i, row in enumerate(rows):
        x = X0
        for text, color, font in row:
            d.text((x, y), text, font=font, fill=color)
            x += CW * len(text)
        if cursor and r_i == len(rows) - 1:
            d.rectangle([x + 1, y + 2, x + CW - 1, y + LH - 2], fill=ORANGE)
        y += LH
    return im


def snap(ms, cursor=True):
    frames.append(render(cursor))
    durations.append(ms)


def prompt():
    screen.append([("thaleo", CYAN, BOLD), (" in ", MUTED, FONT), ("~/vaults", TEXT, FONT), (" ❯ ", ORANGE, BOLD)])


def type_cmd(cmd):
    for ch in cmd:
        screen[-1].append((ch, TEXT, FONT))
        snap(45)
    snap(350)
    screen.append([])


def show(text, color=TEXT, pause=60):
    for line in text.rstrip("\n").split("\n"):
        if screen and screen[-1] == []:
            screen[-1] = [(line, color, FONT)]
        else:
            screen.append([(line, color, FONT)])
        snap(pause, cursor=False)


def ask(label, answer, secret=False):
    """Interactive prompt: label printed, then the user's answer typed."""
    if screen and screen[-1] == []:
        screen[-1] = [(label, TEXT, FONT)]
    else:
        screen.append([(label, TEXT, FONT)])
    snap(250)
    if not secret:
        for ch in answer:
            screen[-1].append((ch, CYAN, FONT))
            snap(40)
    else:
        snap(500)  # rpassword echoes nothing
    snap(200)
    screen.append([])


def clear():
    screen.clear()


def read(name):
    return (cap / name).read_text()


# ---- scene 1: create a vault ----------------------------------------------
prompt(); snap(600)
type_cmd("cista init personal")
ask("Master password: ", "", secret=True)
ask("Confirm master password: ", "", secret=True)
show("Vault created at ~/.local/share/cista/vaults/personal.cista", GREEN)
screen.append([]); prompt(); snap(1200)

# ---- scene 2: add an entry with a generated password ----------------------
clear(); prompt(); snap(300)
type_cmd("cista add personal --generate --length 24")
ask("Master password: ", "", secret=True)
ask("Service name: ", "github")
ask("Username (optional): ", "thaleoo")
ask("URL (optional): ", "https://github.com")
ask("Notes (optional): ", "")
show("Entry added.", GREEN)
screen.append([]); prompt(); snap(1200)

# ---- scene 3: list + health ------------------------------------------------
clear(); prompt(); snap(300)
type_cmd("cista list personal")
ask("Master password: ", "", secret=True)
screen.pop()
show(read("list.txt"), TEXT, 40)
screen.append([]); prompt(); snap(1800)

clear(); prompt(); snap(300)
type_cmd("cista health personal")
ask("Master password: ", "", secret=True)
screen.pop()
txt = read("health.txt").rstrip("\n").split("\n")
show("\n".join(txt[:-1]), TEXT, 40)
show(txt[-1], GREEN)
screen.append([]); prompt(); snap(1800)

# ---- scene 4: without the password it's just random bytes ------------------
clear(); prompt(); snap(300)
type_cmd("head -c 64 personal.cista | od -A x -t x1")
hexlines = [l.split(">")[0].rstrip() for l in read("hex.txt").rstrip("\n").split("\n")]
show("\n".join(hexlines), MUTED, 120)
show("# no master password → only an authenticated header + ciphertext", ORANGE)
screen.append([]); prompt(); snap(2600)

sample = frames[::max(1, len(frames)//12)]
mont = Image.new("RGB", (W * len(sample), H))
for i, f in enumerate(sample):
    mont.paste(f, (i * W, 0))
pal = mont.quantize(colors=64, method=Image.Quantize.MEDIANCUT)
q = [f.quantize(palette=pal, dither=Image.Dither.NONE) for f in frames]
q[0].save(out, save_all=True, append_images=q[1:], duration=durations, loop=0, optimize=True, disposal=1)
print(out, len(frames), "frames", Path(out).stat().st_size // 1024, "KiB")
