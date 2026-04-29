#!/usr/bin/env python3
"""
CosmicMagnetar — GitHub Profile Dashboard Generator
Generates an RPG-style SVG dashboard with live GitHub data.
Run via GitHub Actions on a schedule; outputs profile-card.svg
"""

import json
import os
import math
import urllib.request
import urllib.error
import base64
from datetime import datetime, timezone

# ─────────────────────────────────────────────────────────────────────────────
# Config
# ─────────────────────────────────────────────────────────────────────────────
USERNAME  = "CosmicMagnetar"
TOKEN     = os.environ.get("GITHUB_TOKEN", "")
OUT_FILE  = "profile-card.svg"

W, H = 960, 600

# ─────────────────────────────────────────────────────────────────────────────
# Palette
# ─────────────────────────────────────────────────────────────────────────────
BG        = "#0d1117"
PANEL     = "#0d1a0f"
BORDER    = "#1c3820"
GREEN     = "#00ff88"
GREEN_MID = "#00cc66"
GREEN_DIM = "#0a3a1a"
TEXT      = "#c0f0cc"
TEXT_DIM  = "#3d6b4a"
TEXT_HI   = "#ffffff"
RED       = "#ff4466"
BLUE      = "#448aff"
TEAL      = "#00ccaa"
GOLD      = "#ffcc44"
AMBER     = "#ff9922"

# ─────────────────────────────────────────────────────────────────────────────
# GitHub helpers
# ─────────────────────────────────────────────────────────────────────────────
def api(path, params=""):
    url = f"https://api.github.com{path}{params}"
    req = urllib.request.Request(url)
    req.add_header("User-Agent", "profile-card-generator/1.0")
    req.add_header("Accept", "application/vnd.github.v3+json")
    if TOKEN:
        req.add_header("Authorization", f"Bearer {TOKEN}")
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            return json.loads(r.read())
    except Exception as e:
        print(f"  [warn] API {path}: {e}")
        return None

def fetch_b64(url, media="image/png"):
    try:
        req = urllib.request.Request(url)
        req.add_header("User-Agent", "profile-card-generator/1.0")
        with urllib.request.urlopen(req, timeout=10) as r:
            raw  = r.read()
            # detect jpeg vs png from magic bytes
            mime = "image/jpeg" if raw[:2] == b"\xff\xd8" else "image/png"
            return mime, base64.b64encode(raw).decode()
    except Exception as e:
        print(f"  [warn] fetch_b64 {url}: {e}")
        return None, None

# ─────────────────────────────────────────────────────────────────────────────
# Fetch data
# ─────────────────────────────────────────────────────────────────────────────
print("Fetching GitHub profile…")
user   = api(f"/users/{USERNAME}") or {}
repos  = api(f"/users/{USERNAME}/repos", "?per_page=100&sort=pushed&type=owner") or []
events = api(f"/users/{USERNAME}/events", "?per_page=100") or []

# Language bytes across non-fork repos (capped at 25 to avoid rate limits)
print("Fetching language data…")
lang_bytes: dict[str, int] = {}
for repo in [r for r in repos if not r.get("fork")][:25]:
    langs = api(f"/repos/{USERNAME}/{repo['name']}/languages") or {}
    for lang, b in langs.items():
        lang_bytes[lang] = lang_bytes.get(lang, 0) + b

total_bytes = sum(lang_bytes.values()) or 1
total_stars = sum(r.get("stargazers_count", 0) for r in repos)
owned_repos = [r for r in repos if not r.get("fork")]
total_repos = len(owned_repos)
followers   = user.get("followers", 0)

# Skill scores  (0 – 500 scale, matching image aesthetic)
def score(num, base=80, scale=800, cap=480):
    return min(cap, int(num / total_bytes * scale + base))

ts  = lang_bytes.get("TypeScript",  0)
py  = lang_bytes.get("Python",      0)
cpp = lang_bytes.get("C++",         0)
cs  = lang_bytes.get("C#",          0)
js  = lang_bytes.get("JavaScript",  0)

skills = {
    "Code":     score(ts + cpp + py,    120, 900),
    "Build":    score(ts + js,          100, 800),
    "AI":       score(py,               80,  1200),
    "Craft":    score(cs,               65,  1500, cap=380),
    "Research": min(500, total_stars * 11 + followers * 7 + 100),
    "Deploy":   min(500, total_repos  * 18 + 120),
}

# Commit activity — last 30 days (index 0 = 29 days ago, 29 = today)
print("Building activity series…")
commit_days: dict[int, int] = {}
now = datetime.now(timezone.utc)
for ev in events:
    if ev.get("type") != "PushEvent":
        continue
    try:
        d     = datetime.fromisoformat(ev["created_at"].replace("Z", "+00:00"))
        delta = (now - d).days
        if 0 <= delta < 30:
            n_commits = len(ev.get("payload", {}).get("commits", []))
            commit_days[delta] = commit_days.get(delta, 0) + n_commits
    except Exception:
        pass

activity = [commit_days.get(29 - i, 0) for i in range(30)]   # oldest → newest

# Avatar
print("Fetching avatar…")
avatar_mime, avatar_b64 = fetch_b64(user.get("avatar_url", ""))

# Top 6 languages for bar chart
top_langs = sorted(lang_bytes.items(), key=lambda x: x[1], reverse=True)[:6]
top_bytes  = sum(b for _, b in top_langs) or 1

# Recent non-fork repos
recent_repos = owned_repos[:6]

total_xp = sum(skills.values())
level    = max(1, total_xp // 150)

# ─────────────────────────────────────────────────────────────────────────────
# SVG helpers
# ─────────────────────────────────────────────────────────────────────────────
parts: list[str] = []

def add(s: str):
    parts.append(s)

def rect(x, y, w, h, fill=PANEL, rx=3, stroke=BORDER, sw=1, opacity=None):
    op = f' fill-opacity="{opacity}"' if opacity else ""
    add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" rx="{rx}" stroke="{stroke}" stroke-width="{sw}"{op}/>')

def text(x, y, s, fill=TEXT, size=10, weight="400", anchor="start", italic=False,
         dominant="auto", clip=None, letter=None):
    st = f' font-style="italic"'     if italic else ""
    cl = f' clip-path="url(#{clip})"' if clip  else ""
    ls = f' letter-spacing="{letter}"' if letter else ""
    add(f'<text x="{x}" y="{y}" fill="{fill}" font-size="{size}" font-weight="{weight}"'
        f' text-anchor="{anchor}" dominant-baseline="{dominant}"{st}{cl}{ls}>{s}</text>')

def line(x1, y1, x2, y2, stroke=BORDER, sw=1):
    add(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{stroke}" stroke-width="{sw}"/>')

def hbar(x, y, w, h, pct, fill_grad, bg=GREEN_DIM, rx=2):
    add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{bg}" rx="{rx}"/>')
    add(f'<rect x="{x}" y="{y}" width="{int(w*pct)}" height="{h}" fill="url(#{fill_grad})" rx="{rx}"/>')

# ─────────────────────────────────────────────────────────────────────────────
# SVG root + defs
# ─────────────────────────────────────────────────────────────────────────────
add(f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">')

add("""<defs>
  <clipPath id="av"><rect x="14" y="14" width="188" height="232" rx="3"/></clipPath>
  <clipPath id="cc"><rect x="222" y="0" width="438" height="600"/></clipPath>
  <linearGradient id="gGreen" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0%"   stop-color="#00ff88"/>
    <stop offset="100%" stop-color="#00cc66"/>
  </linearGradient>
  <linearGradient id="gRed" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0%"   stop-color="#ff4466"/>
    <stop offset="100%" stop-color="#cc2244"/>
  </linearGradient>
  <linearGradient id="gBlue" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0%"   stop-color="#448aff"/>
    <stop offset="100%" stop-color="#2255cc"/>
  </linearGradient>
  <linearGradient id="gTeal" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0%"   stop-color="#00ccaa"/>
    <stop offset="100%" stop-color="#009977"/>
  </linearGradient>
  <linearGradient id="gGold" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0%"   stop-color="#ffcc44"/>
    <stop offset="100%" stop-color="#cc9922"/>
  </linearGradient>
  <filter id="glow" x="-20%" y="-20%" width="140%" height="140%">
    <feGaussianBlur stdDeviation="2.5" result="blur"/>
    <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
  </filter>
  <filter id="softglow" x="-10%" y="-10%" width="120%" height="120%">
    <feGaussianBlur stdDeviation="1.5" result="blur"/>
    <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
  </filter>
</defs>""")

# Root background
add(f'<rect width="{W}" height="{H}" fill="{BG}"/>')

# Subtle grid texture overlay
add(f'<pattern id="grid" x="0" y="0" width="20" height="20" patternUnits="userSpaceOnUse">'
    f'<path d="M20 0 L0 0 0 20" fill="none" stroke="{BORDER}" stroke-width="0.3" opacity="0.4"/>'
    f'</pattern>')
add(f'<rect width="{W}" height="{H}" fill="url(#grid)" opacity="0.5"/>')

# ─────────────────────────────────────────────────────────────────────────────
# LEFT PANEL  (x: 8 → 215)
# ─────────────────────────────────────────────────────────────────────────────
LP_X, LP_W = 8, 206
rect(LP_X, 8, LP_W, H - 16, fill=PANEL)

# Avatar
if avatar_b64:
    add(f'<image x="14" y="14" width="188" height="232" href="data:{avatar_mime};base64,{avatar_b64}" '
        f'clip-path="url(#av)" preserveAspectRatio="xMidYMid slice"/>')
    # dim overlay at bottom of avatar for text readability
    add(f'<rect x="14" y="190" width="188" height="56" fill="{PANEL}" opacity="0.7" '
        f'clip-path="url(#av)"/>')
else:
    rect(14, 14, 188, 232, fill=GREEN_DIM, rx=3, stroke=BORDER)
    text(108, 130, USERNAME[:12], fill=GREEN, size=11, anchor="middle")

# Level badge — top-left corner of avatar
add(f'<rect x="14" y="14" width="94" height="18" fill="#00000088" rx="2"/>')
text(18, 25, f"LV. {level}   E-Rank", fill=GREEN, size=9, weight="600")

# Rank badge — top-right corner
add(f'<rect x="108" y="14" width="94" height="18" fill="#00000088" rx="2"/>')
text(200, 25, f"XP {total_xp}", fill=GOLD, size=9, weight="600", anchor="end")

# Section label
y = 256
text(LP_X + 8, y, "Daily Energy", fill=TEXT_DIM, size=9)
line(LP_X + 8, y + 3, LP_X + LP_W - 8, y + 3)

y += 18
bars_cfg = [
    ("HP",    "gRed",   0.78),
    ("Flow",  "gGreen", 0.84),
    ("Focus", "gBlue",  0.62),
    ("Drive", "gTeal",  0.71),
]
for label, grad, pct in bars_cfg:
    text(LP_X + 8, y + 9, label, fill=TEXT, size=9)
    hbar(LP_X + 46, y + 2, 128, 7, pct, grad)
    y += 20

# Stats table
y += 6
text(LP_X + 8, y, "Stats", fill=GREEN, size=10, weight="700")
line(LP_X + 8, y + 3, LP_X + LP_W - 8, y + 3)
y += 16

for name, val in skills.items():
    pct = val / 500
    text(LP_X + 8, y + 8,   name,     fill=TEXT_DIM, size=9)
    text(LP_X + 74, y + 8,  str(val), fill=TEXT_HI,  size=9)
    hbar(LP_X + 108, y + 2, 86, 5, pct, "gGreen")
    y += 17

line(LP_X + 8, y + 2, LP_X + LP_W - 8, y + 2)
y += 12
add(f'<text x="{LP_X + 8}" y="{y}" fill="{TEXT_DIM}" font-size="9" font-family="monospace">'
    f'SUM  <tspan fill="{TEXT_HI}" font-weight="700">{total_xp}</tspan></text>')

# ─────────────────────────────────────────────────────────────────────────────
# CENTER PANEL  (x: 222 → 659)
# ─────────────────────────────────────────────────────────────────────────────
CP_X, CP_W = 222, 438
rect(CP_X, 8, CP_W, H - 16, fill=PANEL)

# Title
add(f'<text x="441" y="36" fill="{GREEN}" font-size="22" font-weight="700" font-style="italic" '
    f'text-anchor="middle" dominant-baseline="middle" filter="url(#glow)" font-family="monospace">'
    f'{user.get("name") or USERNAME}</text>')
add(f'<text x="441" y="54" fill="{TEXT_DIM}" font-size="9" text-anchor="middle" '
    f'font-family="monospace" letter-spacing="1">KRISHNA  ·  AI ARCHITECT  ·  NEWTON SCHOOL OF TECHNOLOGY</text>')

line(CP_X + 16, 62, CP_X + CP_W - 16, 62)

# ── Radar chart ──────────────────────────────────────────────────────────────
RCX, RCY, RCR = 441, 215, 118
axes = list(skills.keys())
vals = list(skills.values())
N    = len(axes)
MAX  = 500

# Grid rings
for ring_val in [100, 200, 300, 400, 500]:
    pts = []
    for i in range(N):
        ang = (2 * math.pi * i / N) - math.pi / 2
        r   = RCR * ring_val / MAX
        pts.append(f"{RCX + r*math.cos(ang):.2f},{RCY + r*math.sin(ang):.2f}")
    alpha = "0.25" if ring_val < 500 else "0.45"
    add(f'<polygon points="{" ".join(pts)}" fill="none" stroke="{GREEN_DIM}" '
        f'stroke-width="1" opacity="{alpha}"/>')
# Ring label (lower-right quadrant)
    ang0 = -math.pi / 4
    lx   = RCX + (RCR * ring_val / MAX + 6) * math.cos(ang0)
    ly   = RCY + (RCR * ring_val / MAX + 4) * math.sin(ang0)
    add(f'<text x="{lx:.1f}" y="{ly:.1f}" fill="{TEXT_DIM}" font-size="7" '
        f'text-anchor="middle" font-family="monospace">{ring_val}</text>')

# Axis spokes
for i in range(N):
    ang = (2 * math.pi * i / N) - math.pi / 2
    x2  = RCX + RCR * math.cos(ang)
    y2  = RCY + RCR * math.sin(ang)
    add(f'<line x1="{RCX}" y1="{RCY}" x2="{x2:.2f}" y2="{y2:.2f}" '
        f'stroke="{BORDER}" stroke-width="1"/>')

# Data polygon fill
data_pts = []
for i, v in enumerate(vals):
    ang = (2 * math.pi * i / N) - math.pi / 2
    r   = RCR * v / MAX
    data_pts.append(f"{RCX + r*math.cos(ang):.2f},{RCY + r*math.sin(ang):.2f}")
add(f'<polygon points="{" ".join(data_pts)}" fill="{GREEN}" fill-opacity="0.20" '
    f'stroke="{GREEN}" stroke-width="2" filter="url(#softglow)"/>')

# Data nodes + value labels
for i, v in enumerate(vals):
    ang = (2 * math.pi * i / N) - math.pi / 2
    r   = RCR * v / MAX
    nx  = RCX + r * math.cos(ang)
    ny  = RCY + r * math.sin(ang)
    add(f'<circle cx="{nx:.2f}" cy="{ny:.2f}" r="3.5" fill="{GREEN}" '
        f'stroke="{BG}" stroke-width="1.5"/>')

# Axis labels (outside the ring)
LABEL_OFF = RCR + 20
for i, label in enumerate(axes):
    ang  = (2 * math.pi * i / N) - math.pi / 2
    lx   = RCX + LABEL_OFF * math.cos(ang)
    ly   = RCY + LABEL_OFF * math.sin(ang)
    add(f'<text x="{lx:.2f}" y="{ly:.2f}" fill="{TEXT}" font-size="9.5" '
        f'text-anchor="middle" dominant-baseline="middle" font-family="monospace" '
        f'font-weight="600">{label}</text>')

# "Powered by" label
add(f'<text x="{CP_X + CP_W - 12}" y="337" fill="{TEXT_DIM}" font-size="8" '
    f'text-anchor="end" font-family="monospace">github.com/{USERNAME}</text>')

line(CP_X + 16, 343, CP_X + CP_W - 16, 343)

# ── Activity chart ────────────────────────────────────────────────────────────
AX, AY, AW, AHT = CP_X + 20, 365, CP_W - 40, 90
text(AX, AY - 10, "Commit Activity — Last 30 Days", fill=TEXT, size=9, weight="600")

# Chart background
add(f'<rect x="{AX}" y="{AY}" width="{AW}" height="{AHT}" '
    f'fill="{GREEN_DIM}" fill-opacity="0.18" rx="2" stroke="{BORDER}" stroke-width="1"/>')

max_c = max(activity) if max(activity) > 0 else 1

# Gridlines (y-axis)
for i in range(1, 4):
    gy = AY + AHT - int(AHT * i / 4 * 0.9)
    add(f'<line x1="{AX}" y1="{gy}" x2="{AX + AW}" y2="{gy}" '
        f'stroke="{BORDER}" stroke-width="1" stroke-dasharray="3,3"/>')

# Area + line
pts_line = []
for i, c in enumerate(activity):
    px = AX + (i / 29) * AW
    py = AY + AHT - (c / max_c) * AHT * 0.88 - 4
    pts_line.append((px, py))

area_pts = (f"{AX},{AY + AHT} " +
            " ".join(f"{px:.1f},{py:.1f}" for px, py in pts_line) +
            f" {AX + AW},{AY + AHT}")
add(f'<polygon points="{area_pts}" fill="{GREEN}" fill-opacity="0.12"/>')
add(f'<polyline points="{" ".join(f"{px:.1f},{py:.1f}" for px,py in pts_line)}" '
    f'fill="none" stroke="{GREEN}" stroke-width="1.8" stroke-linejoin="round"/>')

# X-axis labels
for i in range(0, 30, 5):
    px = AX + (i / 29) * AW
    add(f'<text x="{px:.1f}" y="{AY + AHT + 13}" fill="{TEXT_DIM}" font-size="7.5" '
        f'text-anchor="middle" font-family="monospace">{30 - i}d</text>')

# Y-axis peak label
add(f'<text x="{AX + AW - 2}" y="{AY + 10}" fill="{GREEN}" font-size="7.5" '
    f'text-anchor="end" font-family="monospace">{max_c} commits</text>')

# ─────────────────────────────────────────────────────────────────────────────
# RIGHT PANEL  (x: 662 → 952)
# ─────────────────────────────────────────────────────────────────────────────
RP_X, RP_W = 662, 290
rect(RP_X, 8, RP_W - 8, H - 16, fill=PANEL)

ry = 28

# XP display
add(f'<text x="{RP_X + 12}" y="{ry}" fill="{TEXT_DIM}" font-size="9" font-family="monospace">'
    f'XPs: <tspan fill="{GREEN}" font-weight="700" font-size="15">{total_xp}</tspan></text>')
ry += 18
next_level_xp = (level + 1) * 150
xp_progress   = min(1.0, (total_xp % 150) / 150)
add(f'<text x="{RP_X + 12}" y="{ry}" fill="{TEXT_DIM}" font-size="8" font-family="monospace">'
    f'To reach Level {level + 1} attain {next_level_xp - total_xp} XP</text>')
ry += 10
hbar(RP_X + 12, ry, RP_W - 30, 6, xp_progress, "gGold")
ry += 16

line(RP_X + 8, ry, RP_X + RP_W - 12, ry)
ry += 14

# Stats row
add(f'<text x="{RP_X + 12}" y="{ry}" fill="{TEXT_DIM}" font-size="9" font-family="monospace">'
    f'Stars: <tspan fill="{GOLD}">{total_stars}</tspan>   '
    f'Repos: <tspan fill="{TEXT_HI}">{total_repos}</tspan>   '
    f'Followers: <tspan fill="{TEXT_HI}">{followers}</tspan></text>')
ry += 20

line(RP_X + 8, ry, RP_X + RP_W - 12, ry)
ry += 14

# Languages
add(f'<text x="{RP_X + 12}" y="{ry}" fill="{GREEN}" font-size="10" '
    f'font-weight="700" font-family="monospace">Languages</text>')
ry += 16

lang_colors = ["gGreen", "gBlue", "gTeal", "gRed", "gGold", "gGreen"]
for idx, (lang, b) in enumerate(top_langs):
    pct = b / top_bytes
    bar_w = int((RP_W - 80) * pct)
    add(f'<text x="{RP_X + 12}" y="{ry + 9}" fill="{TEXT}" font-size="9" '
        f'font-family="monospace">{lang[:13]}</text>')
    add(f'<text x="{RP_X + RP_W - 14}" y="{ry + 9}" fill="{TEXT_DIM}" font-size="8" '
        f'text-anchor="end" font-family="monospace">{pct*100:.0f}%</text>')
    hbar(RP_X + 12, ry + 13, RP_W - 32, 5, pct, lang_colors[idx % len(lang_colors)])
    ry += 26

line(RP_X + 8, ry, RP_X + RP_W - 12, ry)
ry += 14

# Recent Repos
add(f'<text x="{RP_X + 12}" y="{ry}" fill="{GREEN}" font-size="10" '
    f'font-weight="700" font-family="monospace">Recent Projects</text>')
ry += 16

for repo in recent_repos:
    name  = repo["name"][:21]
    stars = repo.get("stargazers_count", 0)
    lang  = (repo.get("language") or "")[:10]
    add(f'<text x="{RP_X + 12}" y="{ry}" fill="{TEXT}" font-size="9" '
        f'font-family="monospace">{name}</text>')
    add(f'<text x="{RP_X + RP_W - 14}" y="{ry}" fill="{TEXT_DIM}" font-size="8" '
        f'text-anchor="end" font-family="monospace">{lang}  *{stars}</text>')
    line(RP_X + 12, ry + 3, RP_X + RP_W - 12, ry + 3, stroke=BORDER, sw=1)
    ry += 20

# Footer identity
line(RP_X + 8, H - 56, RP_X + RP_W - 12, H - 56)
add(f'<text x="{RP_X + 12}" y="{H - 43}" fill="{TEXT_DIM}" font-size="8" '
    f'font-family="monospace" letter-spacing="0.5">Newton School of Technology  ·  B.Tech AI  ·  2024-2028</text>')
add(f'<text x="{RP_X + 12}" y="{H - 29}" fill="{TEXT_DIM}" font-size="8" '
    f'font-family="monospace" letter-spacing="0.5">President, Game Development Club  ·  GSoC 2026 Aspirant</text>')
add(f'<text x="{RP_X + 12}" y="{H - 15}" fill="{TEXT_DIM}" font-size="8" '
    f'font-family="monospace" letter-spacing="0.5">Alfaleus Technology (SDI Intern, 2025)  ·  IIT Hyderabad</text>')

# ─────────────────────────────────────────────────────────────────────────────
# Column separators (subtle)
# ─────────────────────────────────────────────────────────────────────────────
line(220, 8, 220, H - 8)
line(660, 8, 660, H - 8)

add("</svg>")

# ─────────────────────────────────────────────────────────────────────────────
# Write output
# ─────────────────────────────────────────────────────────────────────────────
svg_content = "\n".join(parts)
with open(OUT_FILE, "w", encoding="utf-8") as f:
    f.write(svg_content)

print(f"Generated {OUT_FILE}  ({len(svg_content):,} bytes)")
print(f"Skills: {skills}")
print(f"Total XP: {total_xp}  Level: {level}")
print(f"Stars: {total_stars}  Repos: {total_repos}  Followers: {followers}")