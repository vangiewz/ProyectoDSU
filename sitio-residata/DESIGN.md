---
name: Residata
description: Sitio corporativo de Residata S.R.L., impreso como el ticket térmico que emite una báscula.
colors:
  mostrador: "#17191c"
  mostrador-2: "#22252a"
  mostrador-3: "#2e3238"
  sobre-mostrador: "#ecebe6"
  sobre-mostrador-2: "#a9adb3"
  papel: "#fbfbf8"
  papel-2: "#f1f1ec"
  tinta: "#17191c"
  tinta-2: "#565b62"
  tinta-3: "#8a8f96"
  pauta: "#c9cbc6"
  sello: "#0b6b4f"
  sello-claro: "#d8ece4"
  sello-sobre-mostrador: "#5fc29d"
  alerta: "#c42f17"
  alerta-hondo: "#a12512"
  alerta-sobre-mostrador: "#ff8a73"
  foco: "#f2b705"
typography:
  display:
    fontFamily: "Barlow Condensed, Arial Narrow, sans-serif"
    fontSize: "clamp(2.6rem, 6vw, 4.6rem)"
    fontWeight: 800
    lineHeight: 1.02
    letterSpacing: "-0.01em"
  headline:
    fontFamily: "Barlow Condensed, Arial Narrow, sans-serif"
    fontSize: "clamp(2rem, 4vw, 3.1rem)"
    fontWeight: 800
    lineHeight: 1.02
    letterSpacing: "-0.01em"
  title:
    fontFamily: "Barlow Condensed, Arial Narrow, sans-serif"
    fontSize: "1.45rem"
    fontWeight: 600
    lineHeight: 1.02
  figure:
    fontFamily: "Doto, Martian Mono, ui-monospace, monospace"
    fontSize: "clamp(3.4rem, 8.6vw, 6rem)"
    fontWeight: 900
    lineHeight: 0.9
    letterSpacing: "-0.02em"
  body:
    fontFamily: "Public Sans, system-ui, sans-serif"
    fontSize: "1.0625rem"
    fontWeight: 400
    lineHeight: 1.6
    fontFeature: "tnum"
  data:
    fontFamily: "Martian Mono, ui-monospace, monospace"
    fontSize: "0.86rem"
    fontWeight: 400
    letterSpacing: "0.01em"
    fontVariation: "'wdth' 87.5"
  label:
    fontFamily: "Martian Mono, ui-monospace, monospace"
    fontSize: "0.74rem"
    fontWeight: 700
    lineHeight: 1.2
    letterSpacing: "0.07em"
rounded:
  hair: "1px"
  sm: "2px"
  md: "3px"
  lg: "4px"
spacing:
  xs: "6px"
  sm: "10px"
  md: "14px"
  lg: "24px"
  xl: "36px"
  gutter: "clamp(16px, 4vw, 48px)"
  section: "clamp(72px, 10vw, 128px)"
  section-dense: "clamp(48px, 7vw, 80px)"
components:
  button-primary:
    backgroundColor: "{colors.alerta}"
    textColor: "#ffffff"
    typography: "{typography.label}"
    rounded: "{rounded.md}"
    padding: "12px 24px"
    height: "52px"
  button-primary-hover:
    backgroundColor: "{colors.alerta-hondo}"
  button-outline:
    backgroundColor: "transparent"
    textColor: "currentColor"
    rounded: "{rounded.md}"
    padding: "12px 24px"
    height: "52px"
  field-counter:
    backgroundColor: "{colors.mostrador-2}"
    textColor: "{colors.sobre-mostrador}"
    rounded: "{rounded.md}"
    padding: "10px 12px"
    height: "46px"
  field-paper:
    backgroundColor: "#ffffff"
    textColor: "{colors.tinta}"
    rounded: "{rounded.md}"
    padding: "10px 12px"
    height: "46px"
  nav-link:
    textColor: "{colors.tinta-2}"
    rounded: "{rounded.sm}"
    padding: "10px 12px"
  nav-link-hover:
    backgroundColor: "{colors.papel-2}"
    textColor: "{colors.tinta}"
  nav-access:
    backgroundColor: "{colors.tinta}"
    textColor: "{colors.papel}"
    rounded: "{rounded.sm}"
    padding: "10px 12px"
  stamp:
    textColor: "{colors.sello}"
    rounded: "{rounded.md}"
    padding: "6px 9px 5px"
  stamp-alert:
    textColor: "{colors.alerta}"
  ticket:
    backgroundColor: "{colors.papel}"
    textColor: "{colors.tinta}"
    padding: "28px clamp(20px, 3vw, 36px) 40px"
---

# Design System: Residata

## Overview

**Creative North Star: "El Ticket de Báscula"**

Every kilo weighed is a receipt. The site is a graphite counter with strips of white thermal paper laid on it: the header is printed at the top of the strip, the hero is a weighing ticket, plans are a price list, the Random Forest explanation is the instructions printed on the back, and the footer is the closing line with a barcode. Kilogram figures in dot-matrix carry the hierarchy; photographs never do. The only imagery is real product screenshots, annotated with leader lines.

Density is that of a receipt: tight dotted rows, label left and value right, monospaced data, condensed uppercase headings. Off the paper, on the counter, the page breathes with wide section padding. Color is almost absent: ink on paper, light text on graphite, a green verification stamp for confirmed states and one red for alerts and the primary action.

The system rejects the split hero with a dashboard mockup and the row of feature cards. Every content block that would be a card is a paper strip with a torn edge instead.

**Key Characteristics:**
- Two grounds only: graphite counter (body) and thermal paper strips (content that is "printed").
- Torn zig-zag edges cut with CSS masks, never borders or rounded cards.
- Every number in Doto (figures) or Martian Mono (data lines); tabular numerals everywhere.
- Dashed and dotted rules as the only dividers on paper.
- Green stamp, red alert, yellow focus: three functional colors, no decorative ones.

## Colors

Thermal ink on thermal paper, laid on a graphite counter; color appears only where the scale would stamp or warn.

### Primary
- **Sello verde** (sello): the verification stamp. Confirmed states ("Registrado", "Publicada"), success messages, the checkmark in plan tables, callout titles on screenshots, the forecast slider accent. On the counter it switches to its light counterpart (sello-sobre-mostrador) for contrast.

### Secondary
- **Rojo alerta** (alerta): the primary action button and error/alert states, plus the hatched forecast bar. Hover deepens to alerta-hondo. On the counter, error text uses alerta-sobre-mostrador.

### Tertiary
- **Amarillo foco** (foco): focus outlines, the focused field ring, text selection and the skip link. Never used as decoration.

### Neutral
- **Mostrador grafito** (mostrador, mostrador-2, mostrador-3): page background, dark field fill, and the rules/borders that live on the counter (screenshot frames, release-log dividers, footer top rule).
- **Texto sobre mostrador** (sobre-mostrador, sobre-mostrador-2): headings and body on graphite; secondary copy, footer links, captions.
- **Papel térmico** (papel, papel-2): ticket strips, the printed header, the assistant panel, screenshot callouts; papel-2 is the nav hover tint and a hairline inside the assistant.
- **Tinta** (tinta, tinta-2, tinta-3): ink on paper. tinta for figures and headings, tinta-2 for secondary lines and captions, tinta-3 only for non-text marks (receso bars in the calendar) and the scissor glyph.
- **Pauta** (pauta): the dashed and dotted rules on paper, light field borders on paper.

### Named Rules
**The Stamp And Alarm Rule.** Green means confirmed, red means act or beware. Red is never a decorative accent and never sits on two elements of the same block unless one is the primary button.

**The Two Grounds Rule.** Every element lives either on the counter or on paper, and takes its colors from that ground's set: sobre-mostrador on graphite, tinta on papel. Paper colors are never used as text on the counter except the paper itself.

## Typography

**Display Font:** Barlow Condensed (with Arial Narrow)
**Figure Font:** Doto (with Martian Mono)
**Data/Label Font:** Martian Mono at 87.5% width (with ui-monospace)
**Body Font:** Public Sans (with system-ui)

**Character:** A condensed industrial grotesque shouts headings in uppercase like a printed letterhead; a dot-matrix face prints the kilograms; a narrow mono sets every ticket line and label; a sober public-sector sans carries the prose.

### Hierarchy
- **Display** (800, clamp(2.6rem, 6vw, 4.6rem), 1.02, uppercase): page h1.
- **Headline** (800, clamp(2rem, 4vw, 3.1rem), 1.02, uppercase): section h2. Inside a paper strip it steps down (about 1.6–2.2rem).
- **Title** (600, 1.45rem): h3 in prose; inside the instructions and the footer h3 becomes a mono label.
- **Figure** (Doto 900, clamp(3.4rem, 8.6vw, 6rem) on the hero ticket, clamp(3rem, 7vw, 5rem) in the calendar reading, 2.2rem for prices; line-height 0.9): kilogram totals and prices only.
- **Body** (400, 1.0625rem, 1.6, max 68ch): prose; lead paragraphs at 1.15rem, max 60ch.
- **Data** (Martian Mono 400–600, 0.86rem, width 87.5%): ticket lines, captions in print, dates, versions, status rows.
- **Label** (Martian Mono 600–700, 0.74rem, 0.07em tracking, uppercase): form labels, table heads, callout titles, footer column heads, buttons (0.95rem).

### Named Rules
**The Dot-Matrix Kilo Rule.** A quantity that is the point of a block (kg, Bs) is set in Doto 900; no other text uses Doto.

**The Printed Line Rule.** Any label/value pair is a ticket line: mono, label left, value right in 600 weight, dotted rule below. Never a badge or a card grid of stats.

## Layout

A single centered column of max 1180px with a fluid gutter of clamp(16px, 4vw, 48px). Sections pad clamp(72px, 10vw, 128px) vertically, or clamp(48px, 7vw, 80px) for dense ones. The hero is a two-column grid (1.25fr ticket, 1fr hook and form); the pilot block is 1fr paper, 1.3fr screenshot. Paper strips pad roughly 28–40px inside and add extra bottom padding for the torn edge. The annotated screenshot reserves the left 32% for callouts joined by SVG leader lines.

Breakpoints: at 980px two-column grids stack, callouts drop under the screenshot as a list and leader lines hide, the footer goes to two columns. At 760px the menu collapses behind a "Menú" button, the floating assistant trigger moves into the printed header ("Asistente"), the closing barcode takes its own full-width row, price tables reflow into stacked ticket lines (label left from data-rotulo, value right), and paired fields stack.

## Elevation & Depth

Depth is physical: paper lies on the counter. Paper strips and floating panels cast a soft, low, downward shadow; nothing on the counter itself is lifted, and nothing on paper casts a shadow on paper. No hard offset shadows, no glows.

### Shadow Vocabulary
- **Strip on counter** (`box-shadow: 0 18px 40px -18px rgba(0,0,0,.55)`): every paper strip.
- **Screenshot on counter** (`box-shadow: 0 30px 60px -30px rgba(0,0,0,.7)`): annotated product screenshots.
- **Callout slip** (`box-shadow: 0 10px 24px -12px rgba(0,0,0,.6)`): paper callouts over screenshots.
- **Floating panel** (`box-shadow: 0 30px 70px -20px rgba(0,0,0,.75)`, trigger `0 14px 34px -10px rgba(0,0,0,.7)`): the assistant.

### Named Rules
**The Paper Lies Flat Rule.** Shadow belongs to the paper resting on graphite, never to UI chrome on the paper.

## Shapes

Almost square. Corners run 1–4px: 3px for buttons, fields and stamps, 2px for menu items and callouts, 4px for screenshots and the assistant panel. The signature silhouette is the torn thermal edge: a 9px zig-zag (6px on the sticky header) cut with a CSS mask at the bottom, top or both ends of a strip. Dividers on paper are 2px dashed (section breaks inside a ticket) or 1px dotted (between lines). The stamp is outlined in 2px and rotated −3°. Barcodes are repeating linear gradients in ink.

### Named Rules
**The Torn Edge Rule.** Paper ends in teeth, never in a rounded corner or a border box.

## Components

### Buttons
Blunt, uppercase, mono, and tall enough for a thumb.
- **Shape:** gently squared (3px), min-height 52px, 12px 24px padding, Martian Mono 700 0.95rem at 87.5% width, 0.06em tracking.
- **Primary:** rojo alerta with white text; one per block.
- **Hover / Focus:** hover deepens to alerta-hondo; active nudges down 1px; focus is the global 3px yellow outline offset 3px. Transitions 0.2s on the curva easing.
- **Outline:** transparent with a 1.5px currentColor border, inheriting ink or light text from its ground.

### Stamps
- **Style:** inline mono 700 0.78rem uppercase, 2px outline in sello, rotated −3°. Alert variant in alerta; on the counter the green lightens to sello-sobre-mostrador.
- **Use:** confirmed or published states only.

### Cards / Containers (paper strips)
- **Corner Style:** none; torn edge mask.
- **Background:** papel with tinta text.
- **Shadow Strategy:** strip on counter (see Elevation).
- **Border:** none; inner structure by dashed header rule and dotted lines.
- **Internal Padding:** about 28–40px, with extra bottom space for the teeth.

### Inputs / Fields
- **Style:** 46px min-height, 3px corners, 1.5px border, Public Sans 1rem. On the counter: mostrador-2 fill, mid-grey border, yellow caret. On paper: white fill, pauta border, red caret.
- **Focus:** border turns foco with a 3px foco ring at 35% opacity.
- **Error / Disabled:** user-invalid borders turn alerta; disabled buttons drop to 55% opacity with a progress cursor. Labels are mono uppercase labels above the field.

### Navigation
- **Style:** printed on a sticky paper strip with a 6px torn edge. Brand in Barlow Condensed 800; links in mono 0.84rem uppercase, tinta-2.
- **States:** hover tints papel-2; current page is a dashed underline; "Acceso clientes" is inverted (tinta fill, papel text).
- **Mobile:** at 760px a "Menú" outline button opens the list as a graphite drop panel; the assistant trigger sits in the header.

### Ticket line
The atomic unit: a flex row, label left, value right in 600, 5px vertical padding, 1px dotted pauta rule beneath, no rule under the last line. Used for hero data, pilot facts, contact details and live service status.

### Annotated screenshot
A real product screenshot with a thin graphite frame and 4px corners; paper callouts with a sello mono title sit to its left, joined by SVG leader lines drawn on scroll (1.1s). Below 980px the callouts become a list under the image.

### Price list
A table on a paper strip: mono label heads over a 2px ink rule, dotted row rules, plan names in condensed 800 uppercase, prices in Doto. Included features carry a green check; excluded ones read "No". On mobile each row becomes a stacked ticket.

### Motion
One easing, `cubic-bezier(.16,1,.3,1)`. The hero ticket prints line by line (0.35s each, 90ms stagger); leader lines draw once when seen. Under reduced motion everything is already printed and transitions are off.

## Do's and Don'ts

### Do:
- **Do** put content that is "issued" (data, prices, instructions, forms, status) on a papel strip with torn edges, and leave headings and prose on the graphite counter.
- **Do** set every kilogram total and price in Doto 900, and every label/value pair as a dotted ticket line in Martian Mono.
- **Do** keep red for the primary action and alerts, and green for confirmed states, each switching to its light counterpart on the counter.
- **Do** use only real product screenshots as imagery, framed and annotated with leader lines.
- **Do** keep focus visible with the 3px foco outline on every interactive element.

### Don't:
- **Don't** build a split hero with a dashboard mockup or a row of feature cards.
- **Don't** round paper strips or box them with borders; they end in the torn edge.
- **Don't** use hard offset shadows or glows; depth is only paper resting on the counter.
- **Don't** use tinta-3 for text that must be read; it is for marks.
- **Don't** add decorative colors beyond sello, alerta and foco.
