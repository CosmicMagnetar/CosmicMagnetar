# 🖥️ CosmicMagnetar Dashboard UI Design Specification

## Visual Design Brief

**Theme:** Solo Leveling RPG System Dashboard  
**Aesthetic:** Dark-mode cyberpunk with holographic elements  
**Primary Colors:** Black (#0a0e27), Charcoal (#1a1f3a), Electric Neon Green (#00ff88), Deep Purple (#2d1b69)  
**Style:** Sharp lines, holographic glows, pixel-perfect UI, hyper-detailed  
**Resolution:** 3840×2160 (4K) or 1920×1080 (1080p)  
**Aspect Ratio:** 16:9

---

## Layout Structure: 3-Column Grid

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  [LEFT COLUMN]        [CENTER COLUMN]          [RIGHT COLUMN] │
│  40% width            45% width                 15% width      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🎯 COLUMN 1: PROFILE (LEFT - 40% WIDTH)

### Character Portrait Section

- **Main Element:** Full-body character portrait of Krishna
  - Sharp anime/manhwa features (Solo Leveling style)
  - Dark tech-wear jacket with holographic accents
  - Character is standing 3/4 view facing viewer
  - Confident, commanding posture
- **Background Environment:**
  - Swirling black hole accretion disk (rotating, pulsing)
  - Electric neon green energy streams spiraling around
  - Luminous pulsar symbol overlay (rotating hologram)
  - Depth of field effect with particle effects
  - Glow halo around the entire figure

### Status Information Panel

**Position:** Below character portrait  
**Style:** Framed with rounded corners, glowing border (neon green)

```
╔════════════════════════════════════╗
║          PLAYER STATUS             ║
╠════════════════════════════════════╣
║ HP          [■■■■■■■■■■] 100%    ║
║                                    ║
║ INTELLECT   [■■■■■■■■..] 7.9     ║
║ (GPA)           (Current)          ║
╚════════════════════════════════════╝
```

### Stats List

**Position:** Directly below status bars  
**Font:** Monospace, neon green text on dark background

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  ✦ RANK: C (ASCENDING)
  ✦ LEVEL: 19
  ✦ TITLE: President, Game Dev Club
  ✦ ROLES: Alfaleus Tech Intern
           WhoVR Manager
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 🎮 COLUMN 2: MAIN CONTENT (CENTER - 45% WIDTH)

### Holographic Radar Chart

**Title:** "CURRENT PURSUIT: Multiverse Portfolio"  
**Position:** Top section (40% of center column)

- **Shape:** Glowing green hexagon with 6 data points
- **Labels (clockwise from top):**
  - AI/ML (filled to 95%)
  - GameDev (filled to 85%)
  - Leadership (filled to 80%)
  - Space (filled to 75%)
  - OpenSource (filled to 85%)
  - Product (filled to 70%)

- **Visual Effects:**
  - Pulsing green glow
  - Holographic scan-line animation
  - Data points connected with glowing lines
  - Semi-transparent background panel
  - Rotating subtle animation

### Active Skills Section

**Position:** Below radar chart  
**Style:** Compact list with skill tags

```
ACTIVE SKILLS:
[Generative AI S-RANK]
[Open Source A-RANK]
[Visual Arts B-RANK]
[Theoretic SPECIAL]
```

### Quest Cards Grid (2x2)

**Position:** Lower section (60% of center column)  
**Layout:** 2 rows × 2 columns  
**Card Dimensions:** 350×250px each (with gaps)

#### Card 1 (Top-Left): OpenTriage (Pulsar)

- **Title:** "OpenTriage (Pulsar)"
- **Visual:** Terminal window with glowing pulsar star rotating inside
- **Color Accent:** Neon green with cyan highlights
- **Border:** Holographic glow effect
- **Text:** Small description: "Autonomous GitHub Issue Management"

#### Card 2 (Top-Right): A.S.P.I.R.E.

- **Title:** "A.S.P.I.R.E."
- **Visual:** Cybernetic brain (neural network pattern) merging with a binary tree
- **Color Accent:** Neon green with purple accents
- **Border:** Holographic glow effect
- **Text:** Small description: "Autonomous NPC Sentience Engine"

#### Card 3 (Bottom-Left): Flexp

- **Title:** "Flexp"
- **Visual:** Silhouette of a person running on a glowing neon athletic track
- **Color Accent:** Neon green with orange accents
- **Border:** Holographic glow effect
- **Text:** Small description: "Gamified Fitness Revolution"

#### Card 4 (Bottom-Right): Koren (YouTube)

- **Title:** "Koren (YouTube)"
- **Visual:** Recording camera icon overlaid on a lofi nebula landscape (stars, distant galaxies)
- **Color Accent:** Neon green with violet accents
- **Border:** Holographic glow effect
- **Text:** Small description: "Life Stories & Animation Channel"

---

## 📋 COLUMN 3: SYSTEM LOGS (RIGHT - 15% WIDTH)

### Mini Panels (Stacked Vertically)

#### Panel 1: GSoC 2026 Path

```
╔══════════════════════════╗
║ 🎯 GSoC 2026 PATH       ║
╠══════════════════════════╣
║ Target Orgs:            ║
║ ✓ Metaflow             ║
║ ✓ OpenVINO             ║
║ ○ GMOD                 ║
║ ○ MLLAM                ║
║                        ║
║ STATUS: PREPARING      ║
║ ████████░░ 80%         ║
╚══════════════════════════╝
```

#### Panel 2: EV Agent Capstone

```
╔══════════════════════════╗
║ ⚡ EV AGENT CAPSTONE    ║
╠══════════════════════════╣
║ Focus: Predictive       ║
║        Infrastructure   ║
║                        ║
║ Progress:              ║
║ ██████░░░░ 60%         ║
║                        ║
║ ACTIVE                 ║
╚══════════════════════════╝
```

#### Panel 3: Side Quest - Koren

```
╔══════════════════════════╗
║ 📹 SIDE QUEST: KOREN   ║
╠══════════════════════════╣
║ Channel Launch         ║
║ Platform: YouTube      ║
║ Content: Animation     ║
║          & Stories     ║
║                        ║
║ ███░░░░░░░ 30%         ║
╚══════════════════════════╝
```

---

## 🎨 COLOR PALETTE

| Element          | Color           | Hex     | Usage                              |
| ---------------- | --------------- | ------- | ---------------------------------- |
| Background       | Pure Black      | #0a0e27 | Main backdrop                      |
| Panel Background | Charcoal        | #1a1f3a | Card backgrounds                   |
| Primary Accent   | Neon Green      | #00ff88 | Glows, highlights, active elements |
| Secondary Accent | Electric Purple | #2d1b69 | Depth, secondary elements          |
| Tertiary Accent  | Cyan            | #00d4ff | Tertiary highlights                |
| Text Primary     | Neon Green      | #00ff88 | Main text                          |
| Text Secondary   | Light Gray      | #b0b0b0 | Secondary text                     |
| Glow Effect      | Neon Green      | #00ff88 | Bloom, shadows                     |

---

## ✨ Visual Effects & Animations

### Global Effects

- **Scan-line effect:** Horizontal lines moving top-to-bottom slowly
- **Ambient glow:** Subtle pulsing around holographic elements
- **Particle system:** Floating green particles with depth
- **Static noise:** Extremely subtle (5% opacity) for cyberpunk feel

### Interactive Elements

- **Hover effects:** Cards glow brighter on hover
- **Pulse animation:** Radar chart and status bars pulse on 2-second cycle
- **Rotation:** Pulsar symbol rotates continuously
- **Scan effect:** Radar chart has rotating sweep animation

### Lighting & Shadows

- **Glow bloom:** All neon elements have slight bloom
- **Depth shadows:** Darker shadows beneath cards for 3D effect
- **Ambient lighting:** Subtle scene-wide rim lighting from green neon

---

## Typography

- **Primary Font:** Monospace (Courier New, JetBrains Mono, or Roboto Mono)
- **Heading Size:** 32-48px (bold)
- **Body Text Size:** 14-18px
- **Accent Text:** ALL CAPS for emphasis
- **Letter Spacing:** +2-4% for cyberpunk feel

---

## Asset Specifications

### Image Dimensions

- **Full Dashboard:** 1920×1080 (1080p) or 3840×2160 (4K)
- **Quest Cards:** 350×250px each
- **Character Portrait:** 400×600px
- **Radar Chart:** 500×500px
- **Log Panels:** 250×150px each

### File Format

- **Export as:** PNG (transparent) or JPG (flattened)
- **Compression:** Optimized for web (max 500KB)

---

## Generation Prompt (for AI Image Generators)

```
Create a high-fidelity RPG system dashboard UI in Solo Leveling manhwa aesthetic.
Dark-mode interface with black, charcoal, and electric neon green color palette.
Three-column layout: (Left) Character portrait of a young man in tech-wear with
swirling black hole and pulsar energy behind him, status bars, and stat info;
(Center) Large glowing green hexagon radar chart titled "CURRENT PURSUIT:
Multiverse Portfolio," below it a 2×2 grid of quest cards (OpenTriage: terminal
with pulsar; A.S.P.I.R.E: cybernetic brain tree; Flexp: neon athletic figure;
Koren: camera over nebula); (Right) Stacked system log panels showing GSoC 2026
progress. Sharp lines, holographic glows, scan-line effects, particle effects.
4K resolution, hyper-detailed, cyberpunk-futuristic aesthetic.
```

---

## Integration into GitHub README

Once the dashboard image is generated, add it to your README with:

```markdown
## 🎮 SYSTEM DASHBOARD

<div align="center">
  <img src="./assets/dashboard-ui.png" alt="CosmicMagnetar RPG Dashboard" width="100%">
</div>

**System Status:** Online  
**Player Mode:** Active  
**Last Update:** April 2026
```

---

**Design Version:** 1.0  
**Last Updated:** April 7, 2026  
**Created for:** CosmicMagnetar GitHub Profile
