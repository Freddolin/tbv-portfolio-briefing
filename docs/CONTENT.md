# content.yaml reference

Start from `templates/company/content.yaml` (copied by `python -m briefing new <slug>`). Paths are relative to the company folder.

## Film kind
`kind: investment` (default) or `kind: build_first` for a venture TBV built itself (e.g. walter).

Build First films tell their own story, voice-over only (no `interview`). Script sections and chapters:
`problem` (01 The problem) · `handover` (logo + origin) · `how` (02 What it does) · `team` (03 Built in-house) ·
`traction` (04 Traction) · `next` (05 Next steps) · `ds_d` (06 With Drees & Sommer, the `people` screen) · `close`.
`how`, `team`, `traction` and `next` take `panels` like `problem`. The intro ends "This one, we built ourselves."

## Without interview
Leave out the whole `interview` section (and `founders`, `portrait`) and the film is voice-over only: no interview segments,
no question cards (q_ds, q_founders, q_words), so script.md has no such sections. The handover shows logo and origin only.
About 2:45–3:00 instead of 3:30–4:15.

## Anchors
Everything that appears on screen is cued to the voice-over of its block:

| Anchor | Meaning |
|---|---|
| `retrofit`, `seven thousand` | start of the first matching word(s) in the block's voice-over |
| `s0`, `s1`, `s-1` | start of sentence 0, 1, last (sentences split at `.?!:` and `[pause]`) |
| `e1` | end of sentence 1 |
| `2.5` (number) | seconds; in founder cutaways and `f4` words: seconds from the cutaway / segment start |

If a text would disappear before it can be read, the build inserts a short pause into the voice-over
before the anchor that replaces it. You never set times by hand.

## Panels (`problem.panels`, `how.panels`, cutaway `panel`)

| type | fields | looks like |
|---|---|---|
| `statement` | `text`, `sub`, `sub_at` | big line (+ smaller line) |
| `words` | `head`, `words[]`, `word_at[]` | headline + up to 5 big words stacked |
| `tiles` | `head`, `items[]`, `item_at[]`, `mark: x/check/none` | pain points with ✕ |
| `flow` | `head`, `inputs[]`, `input_at[]`, `hub` (`logo` or text), `hub_caption`, `hub_at`, `outputs[]`, `output_at[]`, `caption` | inputs → company → outputs |
| `points` | `head`, `items[{label, value}]`, `item_at[]` | numbered rows with a value on the right |
| `beats` | `items[{label, head, text, image}]`, `item_at[]` | one feature at a time with a screenshot |
| `stat` | `head`, `value`, `prefix`, `suffix`, `label`, `value_at` | counting number |
| `image` | `src`, `caption`, `source` | screenshot with slow zoom |
| `screens` | `items[{src, caption}]`, `item_at[]` | several screenshots one after another |
| `steps` | `head`, `items[{title, text}]`, `item_at[]` | 3–4 numbered steps side by side |
| `kpis` | `head`, `items[{value, label}]`, `item_at[]`, `note` | 2–4 big numbers side by side (traction); `note` = small footnote such as "As of November 2026" |
| `people` | `head`, `items[{name, role, photo}]`, `item_at[]` | team list, name left, role right; optional round `photo` (media path) left of the name |
| `grid` | `head`, `items[{title, text}]`, `item_at[]` | up to 6 short items in 2–3 columns (features) |

**Visual panels** (`briefing/scenes/visual.py`): for films that should show instead of tell, above all
voice-over-only films without interview footage. Use them as the default for Build First films.

| Type | Fields | What it shows |
|---|---|---|
| `notify` | `items[{icon, title, meta, time, kind: error}]`, `item_at[]`, `caption` | notification cards piling up (the problem as an evening at the desk) |
| `skyline` | `heights[]`, `item_at[]` | buildings drawn one by one, each with its own small pile of tasks |
| `ui` | `src`, `size: [w, h]`, `url`, `window`, `start`, `steps[{at, view: [x,y,w,h], box: [x,y,w,h], label}]`, `overlays[{at, until, pos, kicker, title, rows[{text, status, icon}], button, done, click_at}]` | product walkthrough on a real screenshot: the camera moves to `view`, an orange box spotlights `box`, a label explains it; overlay cards slide in, a button can be clicked (`click_at`). Coordinates are image pixels. Pauses are added to the voice-over automatically so every step can be seen |
| `faces` | `items[{name, role, photo}]`, `item_at[]` | large portraits in a row with name and role |
| `bars` | `head`, `items[{label, value, tag, display}]`, `item_at[]`, `note` | growth bars counting up, last bar orange |
| `funnel` | `head`, `items[{value, display, label, sub, sub_at}]`, `item_at[]`, `note` | a real funnel: stages narrow downwards, value inside, label (and optional second line) outside; last stage orange |
| `units` | `value`, `per`, `display`, `label`, `extra`, `note`, `value_at` | big counting number and a grid of building icons (one per `per` units) |
| `path` | `head`, `items[{title, text, icon}]`, `item_at[]` | roadmap: a line with icon nodes |
| `stack` | `text`, `sub`/`sub_at`, `sub2`/`sub2_at`, `floors[{title, text, icon, live, tag}]`, `item_at[]` (for floors without `live`), `pulse_at` | the product as a building: the live version is the ground floor, roadmap floors drop on top as the voice names them, a roof closes it |
| `origin` | `people[{name, role}]`, `people_at[]`, `problem{at, kicker, title, chart, text, text_at}`, `to_at`, `to_caption` | where a Build First venture came from: people (monogram avatars) spot a problem (card with a falling line), and bring it to the TBV studio box |
| `pressure` | `text`, `job{kicker, title, months, unit, status, at}`, `text2`, `text2_at`, `chart_kicker`, `fees`, `costs`, `margin` | statement left; right a job ad counting up months unfilled, then a schematic chart where costs climb towards flat fees (margin shrinks) |
| `colleague` | `text`, `tools[{label, icon}]`, `cross_at`, `text2`, `text2_at`, `team[{role, text, icon}]`, `walter_role`, `walter_text`, `walter_tag`, `walter_at` | "not another tool": tool windows pile up and get crossed out; "a new colleague": a team list where the product joins as a new member |
| `market` | `head`, `circle_label`, `chips[]`, `chips_at[]`, `value`, `display`, `value_at`, `label`, `start_label`, `alongside_label`, `rows[{title, text, icon}]`, `row_at[]`, `note` | market size counting up left; the market as a circle, the product as a small orange circle inside it (start), an "existing software" circle next to it (runs alongside), then the orange circle grows |
| `moves` | `head`, `items[{title, text, kind: flip|shift|coins|seats, from, to, icon_from, icon_to}]`, `item_at[]` | next steps as cards with a small moving picture each: a pill flips (pilot → paying), icon to icon (residential → commercial), coins stacking (funding), an open seat (team) |
| `loop` | `center`, `team[photo paths]`, `team_at`, `team_caption`, `nodes[{title, text}]`, `node_at[]`, `prototypes`, `final{at, src, size, view, caption, tag, tag_at}` | Build First as a loop (build, test, validate) with a dot running round; wireframe prototypes stack up and turn into the real product screen |

Icons: `mail, phone, invoice, calendar, sheet, alert, chat, building, tower, euro, people, check, wrench, doc, down`.
An overlay with `button` and `click_at` shows a cursor that moves to the button and clicks it.
In `item_at[]` a `null` places that item between its neighbours; missing trailing items follow 0.6 s apart.
Every panel can set `min: <seconds>` (minimum time on screen; the voice-over pauses before the next panel if needed)
and `at: after` (starts when the previous panel's `min` is over, without a voice cue).
`handover: {bg: media/...}` and `close: {bg: ...}` put a dimmed product picture behind the logo.
The D&S chapter can use panels too: `ds: {d: {bg: wm, panels: [...]}}`.
`pacing: voice` (top level of content.yaml): the voice-over is never paused; panels follow it and `min` is ignored.
Use this for every voice-over-only film: inserted pauses make the narrator stop mid-thought.
`handover: {shot: media/..., shot_at: <anchor>, shot_view: [x,y,w,h], shot_size: [w,h], shot_caption}`: the logo moves up and a product screen rises under it.
`handover: {converge: [icons], logo_at, tagline, tagline_at, origin_at}`: icon cards (the problem's loose ends) fly into the centre and the logo pops up there on `logo_at`; a tagline and the origin line follow on their cues.
`end_line` (top level): the line under the TBV logo at the very end; default "Portfolio Briefing #N · company".
Overlays in `ui` can reveal their rows on voice cues with `row_at[]`; `path` takes `sub`/`sub_at`; `units` takes `cols`, `icon_size`, `gap`.

Every panel needs `at` (except the first, which starts with the block).

## why
Exactly three `rows`: `title`, `at`, `card`. Card types: `text` (`caption`, `text`), `stat` (`caption`, `value`, `prefix`, `suffix`, `label`, `at`),
`people` / `list` (`caption`, `items[{name, role}]` or plain strings, `item_at`).

## ds (With Drees & Sommer)
| screen | kind | fields |
|---|---|---|
| `a` | `rows` | `cap`, `head`, `rows[[title, description]]`, `at[]` |
| `a` | `trans` (alternative) | `cap`, `heads[[text, x-position]]`, `heads_at[]`, `rows[[from, to]]`, `at[]`, `end` |
| `b` | `boxes` | `head`, `boxes[[label, title, [lines], dark?]]`, `at[]`, `end` |
| `c` | `cards` | `head`, `hdSize`, `cards[{bu, title, klabel, trigger, bullets[], style: dk/lt, dev: true}]`, `at[]`, `end` |
| `d` | `people` | `head`, `pcap`, `people[[name, role]]`, `names_at[]`, `steps[[label, title, line]]`, `at[]` |

Without `at`, items appear at the last sentences of the block's voice-over.

## interview
Four segments `f1`–`f4`, each with `parts` (played back to back): `video`, `in`, `dur`, optional `audio` + `ain`
for a separate recorder. Optional `founder` (index), `lower_third: false`, `cutaways`
(`at`, `until`, `bg: dk|wm`, `caption`, `panel`). `f4` has `words` (`at`, `text`) for the three words.
