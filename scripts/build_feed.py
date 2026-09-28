#build_feed
"""Mind the Gap publisher.

For every episode in episodes/YYYY-MM-DD.json (spoken script = its section bodies):
  1. If it has no GitHub release yet, synthesize the MP3 (edge-tts, falling back to Piper)
     and upload it as a release asset (keeps audio out of git history).
  2. Rebuild the podcast RSS feed + a tiny landing page into _site/ for GitHub Pages.
"""
import asyncio
import datetime as dt
import email.utils
import html
import json
import os
import pathlib
import subprocess
import sys
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
EPISODES = ROOT / "episodes"
SITE = ROOT / "_site"
WORK = ROOT / "_work"
REPO = os.environ.get("GITHUB_REPOSITORY", "braydenalbrecht/mind-the-gap")
OWNER, NAME = REPO.split("/")
PAGES = f"https://{OWNER}.github.io/{NAME}"
VOICE = os.environ.get("TTS_VOICE", "en-US-AndrewMultilingualNeural")
FALLBACK_VOICE = os.environ.get("TTS_VOICE_FALLBACK", "en-US-AndrewNeural")
PIPER_MODEL = "en_US-ryan-high"

SHOW_TITLE = "Mind the Gap"
SHOW_DESC = "A private daily CS briefing for one listener: the practical computer science, cloud, data, security and AI knowledge a future Solutions Engineer needs, explained casually for the commute."


def sh(*args, check=True, capture=False):
    print("+", " ".join(str(a) for a in args), flush=True)
    return subprocess.run([str(a) for a in args], check=check, text=True,
                          capture_output=capture)


def release_assets(tag):
    r = sh("gh", "release", "view", tag, "--repo", REPO, "--json", "assets",
           check=False, capture=True)
    if(r.returncode != 0):
        return None
    return json.loads(r.stdout)["assets"]


async def edge_tts_to(text, out, voice):
    import edge_tts
    await edge_tts.Communicate(text, voice, rate="+0%").save(str(out))


def synth_edge(text, out):
    for voice in (VOICE, FALLBACK_VOICE):
        for attempt in range(3):
            try:
                asyncio.run(edge_tts_to(text, out, voice))
                if(out.exists() and out.stat().st_size > 10_000):
                    return True
            except Exception as e:
                print(f"edge-tts {voice} attempt {attempt + 1} failed: {e}", flush=True)
    return False


def synth_piper(text, out):
    WORK.mkdir(exist_ok=True)
    base = "https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/ryan/high/"
    for ext in (".onnx", ".onnx.json"):
        dest = WORK / (PIPER_MODEL + ext)
        if(not dest.exists()):
            urllib.request.urlretrieve(base + PIPER_MODEL + ext, dest)
    wav = out.with_suffix(".wav")
    subprocess.run(["piper", "--model", str(WORK / (PIPER_MODEL + ".onnx")),
                    "--output_file", str(wav)], input=text, text=True, check=True)
    sh("ffmpeg", "-y", "-loglevel", "error", "-i", wav, "-codec:a", "libmp3lame",
       "-b:a", "64k", out)
    wav.unlink()
    return True


def duration_seconds(path):
    from mutagen.mp3 import MP3
    return int(MP3(str(path)).info.length)


def publish_audio(meta, script):
    tag = f"ep-{meta['date']}"
    fname = f"mind-the-gap-{meta['date']}.mp3"
    assets = release_assets(tag)
    if(assets):
        for a in assets:
            if(a["name"] == fname):
                return a["size"], meta.get("duration")
    WORK.mkdir(exist_ok=True)
    out = WORK / fname
    if(not synth_edge(script, out)):
        print("edge-tts unavailable, falling back to Piper", flush=True)
        synth_piper(script, out)
    secs = duration_seconds(out)
    if(assets is None):
        sh("gh", "release", "create", tag, out, "--repo", REPO,
           "--title", f"Episode {meta['number']}: {meta['title']}",
           "--notes", meta.get("summary", ""))
    else:
        sh("gh", "release", "upload", tag, out, "--repo", REPO, "--clobber")
    return out.stat().st_size, secs


def spoken_script(meta):
    """The audio is the section bodies read in order; headings are for the text version only."""
    parts = []
    for s in meta["sections"]:
        body = s["body"].replace("\n- ", "\n")
        parts.append(body.strip())
    return "\n\n".join(parts)


def fmt_dur(secs):
    secs = int(secs or 0)
    return f"{secs // 3600:02d}:{secs % 3600 // 60:02d}:{secs % 60:02d}"


def main():
    SITE.mkdir(exist_ok=True)
    items = []
    metas = sorted(EPISODES.glob("*.json"), reverse=True)
    for mpath in metas:
        meta = json.loads(mpath.read_text())
        script = spoken_script(meta)
        size, secs = publish_audio(meta, script)
        meta["duration"] = secs
        pub = dt.datetime.fromisoformat(meta["date"]).replace(
            hour=10, tzinfo=dt.timezone.utc)
        url = (f"https://github.com/{REPO}/releases/download/ep-{meta['date']}/"
               f"mind-the-gap-{meta['date']}.mp3")
        notes = meta.get("summary", "")
        if(meta.get("topics")):
            notes += "\n\nTopics: " + ", ".join(t["name"] for t in meta["topics"])
        if(meta.get("page_url")):
            notes += f"\n\nText version and reactions: {meta['page_url']}"
        items.append(f"""
    <item>
      <title>{html.escape(f"{meta['number']}. {meta['title']}")}</title>
      <description>{html.escape(notes)}</description>
      <itunes:summary>{html.escape(notes)}</itunes:summary>
      <enclosure url="{url}" length="{size}" type="audio/mpeg"/>
      <guid isPermaLink="false">mind-the-gap-{meta['date']}</guid>
      <pubDate>{email.utils.format_datetime(pub)}</pubDate>
      <itunes:duration>{fmt_dur(secs)}</itunes:duration>
      <itunes:episode>{meta['number']}</itunes:episode>
      <itunes:episodeType>full</itunes:episodeType>
      <itunes:explicit>false</itunes:explicit>
    </item>""")

    now = email.utils.format_datetime(dt.datetime.now(dt.timezone.utc))
    feed = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd" xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>{SHOW_TITLE}</title>
    <link>{PAGES}/</link>
    <atom:link href="{PAGES}/feed.xml" rel="self" type="application/rss+xml"/>
    <language>en-us</language>
    <description>{html.escape(SHOW_DESC)}</description>
    <itunes:summary>{html.escape(SHOW_DESC)}</itunes:summary>
    <itunes:author>Mind the Gap</itunes:author>
    <itunes:image href="{PAGES}/cover.png"/>
    <itunes:category text="Technology"/>
    <itunes:explicit>false</itunes:explicit>
    <itunes:type>episodic</itunes:type>
    <itunes:block>Yes</itunes:block>
    <lastBuildDate>{now}</lastBuildDate>{''.join(items)}
  </channel>
</rss>
"""
    (SITE / "feed.xml").write_text(feed)
    (SITE / "cover.png").write_bytes((ROOT / "assets" / "cover.png").read_bytes())
    (SITE / "index.html").write_text(
        f"<!doctype html><meta charset=utf-8><title>{SHOW_TITLE}</title>"
        f"<meta name=robots content=noindex><p>{SHOW_TITLE} feed: "
        f"<a href=feed.xml>{PAGES}/feed.xml</a></p>")
    (SITE / "robots.txt").write_text("User-agent: *\nDisallow: /\n")
    print(f"Feed built with {len(items)} episode(s): {PAGES}/feed.xml")


if(__name__ == "__main__"):
    sys.exit(main())
