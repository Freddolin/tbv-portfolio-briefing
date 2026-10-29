# How a portfolio briefing is made

Every film has the same structure, look, sound and checks. Only the content changes. Follow the steps in order.

## The fixed structure

| # | Block | What it is | Source |
|---|-------|-----------|--------|
| – | Ident | "The Bau Ventures · Portfolio briefing #n" | intro voice (Jarnathan) |
| 1 | `problem` | **01 The problem**, 2–4 panels | voice-over |
| 2 | `handover` | company logo + origin, founder portrait card | voice-over |
| 3 | `f1` | founder introduces the company (+ optional cutaway) | interview |
| 4 | `how` | **02 How it works**, 2–4 panels | voice-over |
| 5 | `q_ds` | question card "What does that mean for Drees & Sommer?" | voice-over |
| 6 | `f2` | founder on Drees & Sommer (+ optional cutaway) | interview |
| 7 | `why` | **03 Why we invested**, three reasons with cards | voice-over |
| 8–11 | `ds_a`…`ds_d` | **04 With Drees & Sommer**: why it matters · who brings what · use cases by team · who leads + next steps | voice-over |
| 12 | `q_founders` | question card "What do the founders get from us?" | voice-over |
| 13 | `f3` | founder on The Bau Ventures (+ optional cutaway) | interview |
| 14 | `q_words` | question card "The Bau Ventures, in three words?" | voice-over |
| 15 | `f4` | founder's three words as a lower third | interview |
| 16 | `close` | logo + tagline, TBV lock-up, music hit | voice-over |

Target length 3:30–4:15. Voice-over about 120–135 seconds, interviews about 70–80 seconds.

## Steps

1. **Collect material** (Notion deal memo, Granola meetings, website, onboarding survey, partner input).
   Facts only from sources you can quote. Note open questions instead of guessing.
2. **Create the company folder**: `python -m briefing new <slug>`. Put logos (light and dark versions),
   screenshots and the interview files into `companies/<slug>/media/`.
3. **Write `script.md`** (voice-over) and **`content.yaml`** (everything on screen) from the templates.
   Word budget per section is in the template. Run `python -m briefing check <slug>`.
4. **Approval**: send the script and the on-screen texts to Fred. Everything about Drees & Sommer
   needs sign-off by the responsible D&S partner(s) before any voice is generated.
5. **Voices** (ElevenLabs, ask Fred before generating and downloading):
   - `python -m briefing tts <slug>` prints both texts.
   - Voice-over: voice *Jessica – Playful, Bright, Warm*, model *Eleven v4*, stability 50 %, one take for the whole script.
   - Intro: voice *Jarnathan*, same settings.
   - Download Generation 1 of each, save as `media/vo.mp3` and `media/intro.mp3`.
6. **Interview selects**: pick the four segments (`f1`–`f4`) in `content.yaml` (`parts` with `in`/`dur`).
   Aim for: f1 15–25 s, f2 15–25 s, f3 15–25 s, f4 5–10 s (three words). Cut "ehm"s by splitting into parts;
   the template punches in at each join so the jump does not show.
7. **Build**: `python -m briefing make <slug>`, then `python -m briefing stills <slug> 5,30,60,...` and look at the stills.
8. **Render + encode + QA**: `python -m briefing all <slug>` (about 20 minutes). Read `build/<slug>/qa.md`.
9. **Watch it once completely with sound.** Check names, logos, portrait crop, pronunciation.
10. **Deliver** `build/<slug>/Portfolio_Briefing_NN_<Company>.mp4` (internal use only).

## What the template guarantees

- Every text stays on screen long enough to read (`MIN_TEXT_S`, `reading_time` in `briefing/config.py`).
  If the voice moves on too fast, the template inserts a short pause into the voice-over automatically.
- Voice-over cuts only at the quietest point between sentences, so no syllable of the next sentence leaks in.
- Music: same track, loops chosen so the final accent lands on the TBV lock-up, ducked under speech.
- Interview sound is cleaned (high-pass, denoise, de-click) and matched to the voice-over loudness.
- Delivery: H.264, under 30 MB, "Internal use only" tag in every frame.
- QA report: text durations, cut-off syllables, ElevenLabs beeps, loudness, file size, content rules,
  speech-recognition check of the voice-over, contact sheet.
