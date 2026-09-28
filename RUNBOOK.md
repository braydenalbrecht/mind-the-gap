# Mind the Gap — daily runbook

This is the procedure the 6am scheduled task follows. Read it top to bottom every run.

## Pieces
- `config/show.md` — show settings (format, tone, content mix, schedule). **Always follow it.** The listener can change it any time.
- `learner/profile.json` — per-topic knowledge levels (0–3), `last_covered`, `next_review`, baseline notes, suggested order.
- `episodes/YYYY-MM-DD.json` — one file per episode. Pushing it to `main` triggers `.github/workflows/publish.yml`, which makes the MP3 (edge-tts, Piper fallback), attaches it to a GitHub release, and redeploys the podcast feed at https://braydenalbrecht.github.io/mind-the-gap/feed.xml
- Companion page (text version, reactions, glossary): https://claude.ai/artifact/GXrcm6iALoiungmR5UQdPm — its database has collections `episodes` (doc id = date), `reactions` (doc id = episode date; fields: topic id → "got" | "shaky" | "lost" | null, plus optional `note`), `glossary` (doc id = term id).

## Each run
1. **Date.** Get today's date in America/New_York. Monday–Friday = regular episode. Saturday = weekend recap. Sunday = do nothing. If `episodes/<today>.json` already exists, stop.
2. **Read state.** `config/show.md`, `learner/profile.json`, the last ~10 episode files, and every `reactions` doc from the companion page (ArtifactData list on `reactions`).
3. **Apply reactions** to `learner/profile.json` for any episode not yet applied (track in `applied_reactions` list): got → level +1 (max 3), next_review = +14 days; shaky → next_review = +3 days; lost → level stays, next_review = next episode. Read any `note` and honor requests.
4. **Pick topics.** Regular episode: 1 deep-dive + 1–3 smaller concepts. Priority: overdue reviews (❓ first, then 🤔), then the next unlearned topics from `suggested_order`, weighted per `config/show.md`. Keep AI content ~75% how-it-works / 25% how-to-use. Saturday recap: revisit the week's topics, weighted toward 🤔/❓, ~13–15 min, lighter tone.
5. **Current events.** WebSearch for the past few days of tech/AI news. Pick at most one or two stories that connect to a concept the listener knows or is learning. Verify every factual claim against a primary or wire source before using it; if you can't verify, skip it. Paraphrase, never quote more than a few words. Put links in `sources`.
6. **Write the episode JSON** (same shape as `episodes/2026-09-28.json`): number (previous + 1), date, title, summary, minutes, page_url, topics [{id, name, blurb}] using `learner/profile.json` topic ids (add new ids to the profile when introducing new topics), sources, glossary [{id, term, definition}] for every new term, sections [{segment, heading, body}].
   - The audio is the section bodies read in order by a text-to-speech voice. Write for the ear: casual single narrator, no code, no URLs, no symbols, spell out acronyms the first time, numbers as words where TTS might stumble (say "four-oh-one" not "401").
   - Vary the structure and segment names from recent episodes. No questions that expect an answer from the listener.
   - Target 2,500–2,700 words (~15 min at the voice's ~172 words per minute), never under ~1,700 or over ~3,400. Saturday recap ~2,300. Check with a word count.
7. **Commit and push** the episode JSON and the updated profile to `main` (commit message: `Episode N: <title>`).
8. **Update the companion page database** with one ArtifactData batch: `set episodes/<date>` (the whole episode JSON) and `set glossary/<id>` for each new term (fields: term, definition, date, episode).
9. **Check** the GitHub Actions run succeeded (poll the Actions API for up to ~10 minutes). If it failed, read the log, fix what you can, and push again. If audio can't be produced, the text version still goes up.
10. Finish with a one-line summary: episode number, title, topics.
