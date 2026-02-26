# muFX Signal Check — Production Guide v2

## Content Tiers (Active)

| Tier | Type | Cadence | Template | Owner |
|------|------|---------|----------|-------|
| 1 | Signal Check | Daily (trading days) | `signal-template-v2.html` | Matt → Sara → Hao |
| 2 | Thematic | Weekly/biweekly | `thematic-template.html` (TBD) | Matt → Sara → Hao |
| 3 | Quarterly Outlook | Start of quarter | `quarterly-template.html` (TBD) | Matt → Sara → Hao |
| 0 | Flash Note | Event-driven | `flash-template.html` (TBD) | **PAUSED** — pending Mac Mini agent |

---

## Signal Check v2 — Section Map

The template is structured top-to-bottom in order of scan priority.
A PM at 6:45am London reads this in under 2 minutes.

### 1. Editorial Line
**One sentence.** What changed overnight and what it means for the thesis.
- Example: *"SOTU delivered no tariff surprises — dollar fades to 97.70, gold rebounds above 5,170."*
- This is NOT a summary of the full note. It's the single takeaway.

### 2. Price Strip (4 cells)
Primary instruments: **DXY, EUR/USD, XAU/USD, USD/JPY**
- Close price, daily change (%), directional arrow
- Color-coded: teal (up), pink (down), gold (flat)

### 3. Extended Price Table
Secondary instruments that matter for the day. Standard set:
- GBP/USD, AUD/USD, USD/CHF, US 10Y, Brent
- Add/remove rows based on what's relevant (e.g., USD/CNH if China is the story)
- "Note" column: one-line context (e.g., "BOE hold priced in", "Iran talks risk premium")

### 4. Regime Strip
Three regime tags, unchanged unless the regime actually shifts:
- **DXY Regime**: Ranging / Trending / Breakout + direction
- **Trend**: Bearish Structure / Bullish Structure / Neutral
- **Gold**: Structural Bid / Consolidating / Correcting

### 5. DXY Chart (SVG)
8-month range view. Updated daily with new close plotted.
- Resistance/support zones shaded
- Key technical levels annotated
- Current price with pulsing dot

### 6. Key Levels (4 boxes)
Two resistance, two support. For DXY unless gold or EUR/USD is the story.
- Level value + one-line note explaining significance

### 7. Gold Chart (SVG)
Same treatment as DXY. Structural view showing trend since Oct 2025.

### 8. Positioning Snapshot
CFTC COT data. Updated weekly (Friday release, reflected in Monday signal).
- Net USD, EUR, JPY, GBP as horizontal bars
- Direction (long/short) color-coded
- Value in billions

### 9. Body Commentary
**2-3 paragraphs MAX.** This is the analytical meat but kept tight.
- Paragraph 1: What happened in the last session
- Paragraph 2: Why it matters structurally
- Paragraph 3 (optional): Any notable data or events that shift the view
- Tone: factual, precise, institutional. No exclamation marks. No "buckle up."

### 10. Thesis Status Box
One-line status: Unchanged / Strengthening / Under Review / Revised
- Brief explanation connecting today's action to the Q2 thesis

### 11. Calendar: Next 24 Hours
Upcoming events with time (EST), description, and impact flag (High/Medium).
- Sources: Forex Factory, Bloomberg economic calendar, central bank schedules

### 12. Key Watch
1-2 sentences on the single most important thing to watch next.
- Should be specific and actionable
- Example: *"Friday PPI above 3.2% solidifies hawkish pause and gives dollar bulls room to retest 98.4."*

### 13. Disclaimer (static)
### 14. Publication Integrity (hash generated at publish)

---

## Data Requirements

Matt needs these before writing. If not available via web search, request from Hao.

| Data | Source | Frequency |
|------|--------|-----------|
| Spot levels (DXY, G10 pairs, XAU) | TradingView / Bloomberg | Daily |
| US 10Y yield | TradingView | Daily |
| Brent crude | TradingView | Daily |
| CFTC COT positioning | CFTC / Bloomberg | Weekly (Friday) |
| Economic calendar | Forex Factory / Bloomberg | Daily |
| Central bank decisions | Central bank sites | As scheduled |

**Rule: No number gets published without a source. If Matt can't verify it, it doesn't go in.**

---

## File Naming Convention

```
signal-YYYYMMDD.html     (e.g., signal-20260226.html)
thematic-YYYYMMDD.html   (e.g., thematic-20260228.html)  
q[N]-YYYY-outlook.html   (e.g., q2-2026-outlook.html)
flash-YYYYMMDD.html      (e.g., flash-20260301.html)
```

---

## Publishing Checklist (Sara)

Before handing to Hao:
- [ ] All `{{VARIABLES}}` replaced with real data
- [ ] OG title, description, URL match page content
- [ ] Canonical URL correct
- [ ] JSON-LD datePublished matches actual date
- [ ] Keywords relevant to the day's content
- [ ] `mailto:research@mufx.io` in nav and footer (no Cloudflare artifacts)
- [ ] Signals nav link points to THIS signal page
- [ ] All prices verified against Matt's copy
- [ ] SVG charts updated with current day's close
- [ ] Responsive check: 768px and 480px breakpoints
- [ ] Publication integrity box date matches
- [ ] `<link rel="stylesheet" href="mufx.css">` present (not inline CSS)
- [ ] Favicon and apple-touch-icon links present

---

## Workflow

```
Matt writes → Matt says "ready to publish" → Sara templates → Sara says "final" → Hao reviews & pushes to GitHub → Live on mufx.io
```

Target: < 30 minutes end-to-end once templates are locked.
Bottleneck should always be analysis quality, never publishing mechanics.

---

## Style Notes (Matt)

- **Institutional tone**: No exclamation marks. No "buckle up." No "huge."
- **State the position, show the evidence, let the reader decide.**
- **Voice**: Calm, precise, occasionally dry. Someone who's seen this before.
- **Attribution**: "Sources report..." / "According to CFTC data..." / "JP Morgan raised..."
- **Numbers**: Always with source. Prices to standard decimal (DXY: 2 decimals, EUR/USD: 4, Gold: integer, 10Y: 3)
- **Length**: Signal checks ~600-800 words total prose. Visuals do the heavy lifting.
