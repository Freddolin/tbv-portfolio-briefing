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
| `kpis` | `head`, `items[{value, label}]`, `item_at[]` | 2–4 big numbers side by side (traction) |
| `people` | `head`, `items[{name, role}]`, `item_at[]` | team list, name left, role right |
| `grid` | `head`, `items[{title, text}]`, `item_at[]` | up to 6 short items in 2–3 columns (features) |

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
