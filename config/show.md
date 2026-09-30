# Mind the Gap — show settings

The daily run reads this file before writing each episode. Edit it (or ask Claude to) to change the show; changes apply from the next episode.

## Listener
- Senior CS student, graduating summer 2027. Commutes by car, ~50 minutes. Listens on iPhone (Apple Podcasts / Overcast).
- Goal: fill practical CS knowledge gaps before entering the job market.
- Career target: **Solutions Engineer** (primary). Backups: data engineering (current internship area), cloud engineering, cybersecurity.
- Internship: IT / digital solutions intern building Microsoft Power Automate flows (Forms, SharePoint, OneDrive). Use as an occasional example only — not a priority.
- **Learns best through examples.** He has said directly: more real-life scenarios and applications, fewer fun facts, and less information per episode.

## Teaching approach (most important section)
- **One main topic per episode, drilled deep.** Do not stack several new concepts. At most one small supporting idea, and only if the main topic can't be understood without it. When in doubt, cut it and save it for another day.
- **Examples carry the episode.** Every episode walks through at least three concrete, real-world scenarios that show the topic in use. Use real products and situations the listener would recognize (a weather app, ordering an Uber, "Log in with Google", paying with Stripe, a Slack alert, a Power Automate flow, a customer support call). For each example, spell out step by step what is actually happening and who is talking to whom.
- **Always answer "why does this matter to me?"** Show where the listener will run into this: on the job as a Solutions Engineer (customer calls, demos, troubleshooting, integrations), in interviews, or in a data/cloud role. Name the concrete situation, not a vague "this is important".
- **Show how it's done when it's practical.** If the topic is something you *do* (create an API key, read a status code, set up a webhook), describe the actual steps, like signing up, finding the dashboard, clicking generate, where the key goes.
- **No fun facts, trivia, history, or jokes for their own sake.** Every sentence either explains the topic or shows it in use. Cut asides like "it's always DNS" unless they teach something.
- **Callbacks, not re-teaching.** Briefly connect today's topic to one or two earlier ones ("remember API keys from Monday? This is where that key actually goes"). Keep a callback to about a minute: a quick reminder, then use it in today's example.
- **Build slowly.** Only rely on concepts the learner profile marks as level 2+ or 👍. If today's topic needs an unfamiliar idea, explain it in one plain sentence, or cover the topic another day.

## Episode shape
A consistent spine with flexible wording (vary segment names and openings so it doesn't feel robotic):
1. **Quick callback (~1 min):** a short reminder of a recent topic, connected to today's.
2. **The idea in plain English (~2–3 min):** what it is, using one clear analogy.
3. **Real-world examples (~7–9 min, the core):** three or more scenarios, walked through step by step.
4. **Why it matters for you (~2 min):** where a Solutions Engineer (or data/cloud engineer) runs into it, e.g. a customer call, a demo, a troubleshooting moment.
5. **In the news (optional, ~1–2 min):** only when a recent story is a clean example of *today's* topic. Skip it on days nothing fits.
6. **Wrap (~1 min):** restate the one idea in two or three sentences and name tomorrow's topic.

## Format
- One narrator. Casual, friendly, like a smart friend who works in tech explaining things over coffee. Plain spoken English, no jargon without defining it first.
- Length: **~15 minutes** (acceptable range 12–18). Target ~2,500–2,700 spoken words (the voice reads ~172 words per minute). The length comes from depth and examples, never from adding more topics.
- **No quizzes or questions that expect an answer in the audio.** The listener is driving. Pure informative briefing.
- Written for the ear: no code blocks, URLs, tables, or symbols read aloud. Spell out acronyms the first time ("A-P-I, application programming interface").
- Occasionally use this podcast itself as a worked example (it uses an API key, a scheduled job, a CI/CD pipeline on GitHub Actions, text-to-speech, an RSS feed, static hosting on GitHub Pages).

## Content mix
- Weight toward what Solutions Engineers use daily: APIs & auth, web fundamentals, cloud, data, integrations, security basics, explaining tech to non-technical people.
- AI content: ~75% understanding how it works (LLMs, tokens, embeddings, RAG, fine-tuning, agents, limits/risks), ~25% using it well (prompting, coding assistants, agents, MCP, automation).
- Current events: only as an example of the day's topic, never as a separate news roundup.
- Finance / "adulting" topics: **off for now.**

## Schedule
- Monday–Friday: new episode, one main topic. Saturday: weekend recap that revisits the week's topics with *new* examples (not repeated ones), weighted toward anything marked 🤔 or ❓. Runs through school breaks.

## Learning loop
- Each episode's text version lists its topic(s); the listener reacts 👍 (got it) / 🤔 (shaky) / ❓ (lost me), and can leave a note.
- 👍 → topic level +1, quick callback in ~1–2 weeks. 🤔 → revisit within ~3 days as the main topic again with different examples. ❓ → next episode re-teaches it from scratch, slower, with a new analogy and more examples.
- **Notes from the listener are direct instructions for upcoming episodes.** Follow them.
- Every new term goes into the glossary.
