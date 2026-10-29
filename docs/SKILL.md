---
name: tbv-portfolio-briefing
description: Create or update a TBV portfolio briefing film (internal video on a portfolio company and its Drees & Sommer collaboration) with the standard template repo, so every film has the same structure, cut, sound and checks.
---

# TBV portfolio briefing films

Every portfolio briefing is built with the repo **Freddolin/tbv-portfolio-briefing**. Never build a film by hand
or from an older one-off script: the repo holds the fixed structure, look, music, voices, timing rules and QA.
Only `companies/<slug>/content.yaml`, `script.md` and the media change per company.

## 0. Set up
1. Attach the repo with `add_repo` (owner `Freddolin`, repo `tbv-portfolio-briefing`, access `push`) and clone it.
2. `pip install -r requirements.txt --break-system-packages` and `npm install`. Needs ffmpeg and Chromium.
3. Read `docs/PROCESS.md`, `docs/RULES.md` and `docs/CONTENT.md` before writing anything.

## 1. Research (before writing)
- Notion (deal memo, portfolio page), Granola (founder and partner meetings), company website, onboarding survey answers.
- Collect: what the product does (tangibly), why TBV invested, what it means for Drees & Sommer,
  concrete use cases with D&S business units or project phases, who leads at D&S, what happens next.
- Quote sources. Inconsistent numbers: round or leave out. No deal terms, no co-investors, no dates or upcoming events,
  no customer names without written OK (check NDAs).

## 2. Script and on-screen content
- `python -m briefing new <slug>`, then fill `companies/<slug>/script.md` (word budgets in the template) and `content.yaml`.
- Structure is fixed (16 blocks, see PROCESS.md). The D&S part is always four screens:
  why it matters · who brings what · use cases by team · who leads + next steps.
- `python -m briefing check <slug>` must show no hints you cannot explain.
- Send Fred the full script and all on-screen texts for approval (AskUserQuestion). Remind him that everything about
  Drees & Sommer needs sign-off from the responsible D&S partner (Nico's rule). Do not generate voices before approval.

## 3. Voices (ElevenLabs in Fred's Chrome; ask before generating and before downloading)
- `python -m briefing tts <slug>` prints the voice-over text and the intro text.
- Voice-over: voice "Jessica - Playful, Bright, Warm", model Eleven v4, stability 50 %, one take for the whole script.
  Intro: voice "Jarnathan", same settings.
- Paste text (click editor, cmd+a, Backspace, type), Generate, pause the autoplay, download Generation 1 with the
  player's download icon. Move the files from ~/Downloads into a work folder, stage them, save as
  `media/vo.mp3` and `media/intro.mp3`.

## 4. Interview and images
- Interview footage, logos (light and dark) and screenshots come from Fred's computer (stage them) into `media/`.
- Choose the four selects in `content.yaml > interview` (f1 company intro, f2 on Drees & Sommer, f3 on TBV, f4 three words).
  Use the interview transcript (Granola or speech recognition) to pick in/out points; cut "ehm"s by splitting into parts.

## 5. Build and check
- `python -m briefing make <slug>`, then `python -m briefing stills <slug> t1,t2,...` and look at the stills
  (one per block at least). Fix content, not timings: timings come from the voice-over.
- `python -m briefing all <slug>` (about 20 minutes): renders, encodes under 30 MB with the "Internal use only" tag, runs QA.
- Read `build/<slug>/qa.md` and look at `contact_sheet.jpg`. Every unchecked item is either fixed or reported to Fred.
- Sentences flagged by speech recognition and all names: tell Fred to listen to those spots.

## 6. Deliver
- Copy the MP4 to /mnt/user-data/outputs, send it with SendUserFile, and write it to Fred's ~/Downloads if the computer is linked.
- Commit `companies/<slug>/` (content.yaml, script.md, logos, screenshots, voice takes; interviews stay out of git) and push.
- Report in two or three lines: length, what to listen to, open sign-offs.

## Changes after feedback
- Text on screen: edit content.yaml, `make` + `all`. Voice-over text: edit script.md and generate a new full take
  (ask first). Never splice old and new takes by hand; the template cuts at quiet points only within one take.
- If something about structure, look or rules should change for all films, change the repo (config.py, scenes/, docs/)
  and tell Fred, rather than patching one film.
