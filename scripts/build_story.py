#!/usr/bin/env python3
"""build_story.py - helpers for the bestdori-story-creator skill.

Usage:
  python build_story.py --list-costumes <character_id>
  python build_story.py --validate <story.json>
  python build_story.py --character <character_id>
  python build_story.py --list-bg <substring>             # search bg/* bundles
  python build_story.py --ls <explorer-path>              # list one folder, e.g. bg/scenario104
  python build_story.py --check-bg <bundle> <file>        # real GET, asserts Content-Type: image/*
  python build_story.py --bg-from-explorer <url>          # derive bundle/file from an explorer URL
  python build_story.py --list-charavoice <character_id>  # probe charavoice bundles for a character
  python build_story.py --check-voice <bundle> <file>     # real GET, asserts Content-Type: audio/*

The script makes outbound HTTPS calls to https://bestdori.com when needed, and caches
JSON responses under ./.bestdori_cache/ next to this script.
"""
from __future__ import annotations
import argparse, json, os, sys, urllib.request, pathlib, re

CACHE_DIR = pathlib.Path(__file__).resolve().parent / ".bestdori_cache"
CACHE_DIR.mkdir(exist_ok=True)

ALLOWED_LAYOUT_TYPE  = {"appear", "hide", "move"}
ALLOWED_SIDE = {
    "none","left","leftOver","leftInside","center","right","rightOver","rightInside",
    "leftUnder","leftInsideUnder","centerUnder","rightUnder","rightInsideUnder",
}
ALLOWED_EFFECT_TYPE  = {"telop","blackIn","blackOut","whiteIn","whiteOut",
                       "changeBackground","changeCardStill"}
ALLOWED_BGM_TYPE     = {"bandori","custom"}
ALLOWED_SE_TYPE      = {"common","bandori","custom"}
ALLOWED_BG_TYPE      = {"bandori","custom"}
ALLOWED_TYPES        = {"talk","layout","motion","effect","sound"}

SERVERS = ["jp","en","tw","cn","kr"]

def _fetch(url: str, *, force: bool = False) -> bytes:
    safe = url.replace("https://","").replace("/","_").replace("?","_")
    cache = CACHE_DIR / safe
    if cache.exists() and not force:
        return cache.read_bytes()
    req = urllib.request.Request(url, headers={"User-Agent":"bestdori-story-creator-skill"})
    with urllib.request.urlopen(req, timeout=30) as r:
        data = r.read()
    cache.write_bytes(data)
    return data

def _fetch_json(url: str):
    return json.loads(_fetch(url).decode("utf-8"))

def _head_meta(url: str) -> tuple[int, str, int]:
    """Real GET (NOT just HEAD - bestdori nginx fakes HEAD/GET 200 with text/html
    on bad paths, so we always fetch a real response and inspect Content-Type)."""
    req = urllib.request.Request(url, headers={"User-Agent":"bestdori-story-creator-skill"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            ct = r.headers.get("Content-Type","")
            cl = int(r.headers.get("Content-Length","0") or 0)
            return r.status, ct, cl
    except Exception as e:
        return 0, f"ERROR:{e}", 0

def list_costumes(character_id: int) -> None:
    catalog = _fetch_json("https://bestdori.com/api/costumes/all.5.json")
    rows = [(int(k), v) for k,v in catalog.items()
            if v.get("characterId") == character_id]
    rows.sort(key=lambda x: x[0])
    if not rows:
        print(f"No costumes found for character {character_id}", file=sys.stderr)
        sys.exit(2)
    print(f"# Character {character_id} - {len(rows)} costumes")
    print(f"{'id':<6} {'live2dAssetBundleName':<40} description")
    for cid, c in rows:
        descs = c.get("description") or []
        # prefer Chinese-Simplified (idx 3) -> English (idx 1) -> Japanese (idx 0)
        d = descs[3] or descs[1] or descs[0] if descs else ""
        print(f"{cid:<6} {c.get('assetBundleName',''):<40} {d}")

def show_character(character_id: int) -> None:
    info = _fetch_json(f"https://bestdori.com/api/characters/{character_id}.json")
    name = info.get("characterName", [None]*5)
    print(f"id={character_id} jp={name[0]} en={name[1]} cn={name[3]}")
    print(f"colorCode={info.get('colorCode')} band={info.get('bandId')}")
    print(f"sdAssetBundleName={info.get('sdAssetBundleName')}")
    print(f"defaultCostumeId={info.get('defaultCostumeId')}")
    seasons = ((info.get("seasonCostumeListMap") or {}).get("entries") or {})
    for skey, sval in seasons.items():
        print(f"  [{skey}]")
        for entry in sval.get("entries", []):
            print(f"    season={entry.get('basicSeasonId')} "
                  f"type={entry.get('seasonCostumeType')} "
                  f"live2d={entry.get('live2dAssetBundleName')}")

def _err(errs: list[str], msg: str) -> None:
    errs.append(msg)

def validate_action(idx: int, a: dict, errs: list[str]) -> None:
    t = a.get("type")
    if t not in ALLOWED_TYPES:
        _err(errs, f"#{idx} unknown type={t!r}")
        return
    if t == "talk":
        for k in ("body","name","wait","close","delay","voices","motions","characters"):
            if k not in a:
                _err(errs, f"#{idx} talk missing field {k}")
    elif t == "layout":
        if a.get("layoutType") not in ALLOWED_LAYOUT_TYPE:
            _err(errs, f"#{idx} layout layoutType={a.get('layoutType')!r}")
        if a.get("sideTo")   not in ALLOWED_SIDE:
            _err(errs, f"#{idx} layout sideTo={a.get('sideTo')!r}")
        if a.get("sideFrom") not in ALLOWED_SIDE:
            _err(errs, f"#{idx} layout sideFrom={a.get('sideFrom')!r}")
        if not isinstance(a.get("character"), int) or not (0 <= a["character"] <= 999):
            _err(errs, f"#{idx} layout character must be int 1..40 (got {a.get('character')!r})")
    elif t == "motion":
        if not isinstance(a.get("character"), int):
            _err(errs, f"#{idx} motion character must be int")
    elif t == "effect":
        et = a.get("effectType")
        if et not in ALLOWED_EFFECT_TYPE:
            _err(errs, f"#{idx} effect effectType={et!r}")
        if et == "telop" and "text" not in a:
            _err(errs, f"#{idx} telop missing text")
        if et in ("blackIn","blackOut","whiteIn","whiteOut") and "duration" not in a:
            _err(errs, f"#{idx} {et} missing duration")
        if et == "changeBackground":
            bg = a.get("background") or {}
            if bg.get("type") not in ALLOWED_BG_TYPE:
                _err(errs, f"#{idx} changeBackground.background.type={bg.get('type')!r}")
            elif bg.get("type") == "bandori":
                _validate_bandori_bg(idx, bg, errs)
    elif t == "sound":
        for sub, allowed in (("bgm", ALLOWED_BGM_TYPE), ("se", ALLOWED_SE_TYPE)):
            v = a.get(sub)
            if v is None:                       # null is allowed (leave channel)
                continue
            if v.get("type") not in allowed:
                _err(errs, f"#{idx} sound.{sub}.type={v.get('type')!r}")

def _validate_bandori_bg(idx: int, bg: dict, errs: list[str]) -> None:
    """Static-shape check for a 'bandori' background. Catches the common mistake
    of writing only a leaf segment (e.g. 'scenario104') instead of the full
    sub-path ('bg/scenario104')."""
    bundle = bg.get("bundle","")
    file = bg.get("file","")
    if not bundle:
        _err(errs, f"#{idx} bandori background missing bundle")
        return
    if not file:
        _err(errs, f"#{idx} bandori background missing file")
    # heuristic: a leaf-only bundle like 'scenario104' or 'event235_back' is
    # almost always wrong - bundle should be a path containing at least one '/'.
    if "/" not in bundle and not bundle.startswith("BESTDORI##URL"):
        _err(errs,
             f"#{idx} bandori bundle={bundle!r} looks like a leaf segment; "
             f"expected a full sub-path such as 'bg/{bundle}'")

def validate_story(path: str) -> None:
    src = json.loads(pathlib.Path(path).read_text(encoding="utf-8"))
    errs: list[str] = []
    if "actions" not in src:
        _err(errs, "missing top-level 'actions'")
    if src.get("server") not in (0,1,2,3,4):
        _err(errs, f"server={src.get('server')!r} (must be 0..4)")
    bg = src.get("background")
    if bg is not None:
        if bg.get("type") not in ALLOWED_BG_TYPE:
            _err(errs, f"top background.type={bg.get('type')!r}")
        elif bg.get("type") == "bandori":
            _validate_bandori_bg("top", bg, errs)
    bgm = src.get("bgm")
    if bgm is not None and bgm.get("type") not in ALLOWED_BGM_TYPE:
        _err(errs, f"top bgm.type={bgm.get('type')!r}")
    for i, a in enumerate(src.get("actions") or []):
        validate_action(i, a, errs)
    if errs:
        print("FAIL")
        for e in errs:
            print(" -", e)
        sys.exit(1)
    print("OK")

# ---------------------------------------------------------------------------
# Asset explorer helpers
# ---------------------------------------------------------------------------

def _info_tree(server: str = "jp") -> dict:
    return _fetch_json(f"https://bestdori.com/api/explorer/{server}/assets/_info.json")

def _walk_paths(tree: dict, prefix: str = ""):
    """Yield ('full/path', child) pairs for every leaf in the asset _info tree.
    Each leaf carries either an int (file count) or a dict of sub-sections."""
    if isinstance(tree, dict):
        for k, v in tree.items():
            full = f"{prefix}/{k}" if prefix else k
            if isinstance(v, dict):
                yield from _walk_paths(v, full)
            else:
                yield full, v

def list_bg(substr: str, server: str = "jp") -> None:
    info = _info_tree(server)
    bg = info.get("bg") or {}
    matches = []
    for path, count in _walk_paths(bg, "bg"):
        if substr.lower() in path.lower():
            matches.append((path, count))
    if not matches:
        print(f"No bg bundles match {substr!r}", file=sys.stderr)
        sys.exit(2)
    print(f"# {len(matches)} bg bundles match {substr!r}")
    for p, n in matches[:200]:
        print(f"  bundle={p:<40} files={n}")

def ls_path(path: str, server: str = "jp") -> None:
    """List the contents of one explorer folder."""
    path = path.strip("/")
    url = f"https://bestdori.com/api/explorer/{server}/assets/{path}.json"
    try:
        files = _fetch_json(url)
    except Exception as e:
        print(f"could not list {url}: {e}", file=sys.stderr)
        sys.exit(2)
    if not isinstance(files, list):
        print(f"unexpected response from {url}: {files!r}", file=sys.stderr)
        sys.exit(2)
    print(f"# {path}/  ({len(files)} entries)")
    for f in files:
        print(f"  {f}")
    # Hint how to use as storySource fields
    pngs = [f[:-4] for f in files if f.endswith(".png")]
    if pngs:
        print()
        print(f"# storySource snippet (pick one of the files):")
        print(f"#   {{ \"type\": \"bandori\", \"bundle\": \"{path}\", \"file\": \"{pngs[0]}\" }}")

def check_bg(bundle: str, file: str, server: str = "jp") -> None:
    """Real-GET check that a (bundle, file) pair resolves to an actual image.
    Mirrors the viewer's getImageUrl: /assets/<server>/<bundle>_rip/<file>.png ."""
    bundle = bundle.strip("/")
    if file.endswith(".png"):
        file = file[:-4]
    url = f"https://bestdori.com/assets/{server}/{bundle}_rip/{file}.png"
    print(f"GET {url}")
    status, ct, cl = _head_meta(url)
    print(f"  status={status} content-type={ct} content-length={cl}")
    ok = (status == 200) and ct.startswith("image/")
    if ok:
        print("  ✅ usable as { \"type\": \"bandori\", \"bundle\": "
              f"\"{bundle}\", \"file\": \"{file}\" }}")
    else:
        print("  ❌ not a real image (likely SPA fallback). "
              "Try a different bundle/file, or use type:\"custom\" with an external URL.")
        sys.exit(1)

def bg_from_explorer(url: str) -> None:
    """Take an Asset Explorer URL like
       https://bestdori.com/tool/explorer/asset/jp/bg/scenario104
    and print the matching storySource bundle/file values plus the verified
    image URLs for everything in that folder.
    The URL may end at a folder (we'll list its PNGs) or at a specific file."""
    m = re.match(r"^https?://bestdori\.com/tool/explorer/asset/([^/]+)/(.+?)/?$", url.strip())
    if not m:
        print(f"not a Bestdori explorer URL: {url}", file=sys.stderr)
        sys.exit(2)
    server, path = m.group(1), m.group(2).strip("/")
    if server not in SERVERS:
        print(f"unknown server segment {server!r}; expected one of {SERVERS}", file=sys.stderr)
        sys.exit(2)
    # if path points at a file (ends with .png), split into bundle+file
    if path.endswith(".png"):
        bundle, _, leaf = path.rpartition("/")
        file = leaf[:-4]
        check_bg(bundle, file, server)
        return
    # otherwise treat as folder, list its PNGs, verify the first one
    files_url = f"https://bestdori.com/api/explorer/{server}/assets/{path}.json"
    try:
        files = _fetch_json(files_url)
    except Exception as e:
        print(f"could not list {files_url}: {e}", file=sys.stderr)
        sys.exit(2)
    pngs = [f[:-4] for f in files if isinstance(f, str) and f.endswith(".png")]
    if not pngs:
        print(f"no .png files under {path}", file=sys.stderr)
        sys.exit(2)
    print(f"# server={server} bundle={path}")
    print(f"# {len(pngs)} png files in this bundle:")
    for f in pngs:
        print(f"  file={f}  ->  https://bestdori.com/assets/{server}/{path}_rip/{f}.png")
    print()
    print(f"# storySource snippets:")
    for f in pngs:
        print(f"  {{ \"type\": \"bandori\", \"bundle\": \"{path}\", \"file\": \"{f}\" }}")
    print()
    print(f"# verifying first one:")
    check_bg(path, pngs[0], server)

def list_charavoice(character_id: int, server: str = "jp") -> None:
    """Probe all newsituationintroduction resXXX bundles for a character and
    list the ones with a real charavoice mp3.
    Range: resCCC011 .. resCCC020 (where CCC = zero-padded character id).
    Output ready-to-paste storySource voice/voices fragments for both
    Scheme A (single bundle) and Scheme B (relative-path hack)."""
    available = []
    for sit in range(1, 25):
        res = f"res{character_id:03d}{sit:03d}"
        url = f"https://bestdori.com/assets/{server}/sound/voice/newsituationintroduction/{res}_rip/{res}_charavoice.mp3"
        status, ct, cl = _head_meta(url)
        if status == 200 and ct.startswith("audio/"):
            available.append((res, cl))
    if not available:
        print(f"No charavoice found for character {character_id} on server {server}", file=sys.stderr)
        sys.exit(2)
    print(f"# character {character_id} — {len(available)} charavoice bundles")
    for res, cl in available:
        print(f"  {res}_charavoice  ({cl} bytes)")
    print()
    print("# Scheme A (single charavoice for the whole story):")
    res0 = available[0][0]
    print(f'  "voice": "sound/voice/newsituationintroduction/{res0}",')
    print(f'  // in talk.voices: {{ "character": {character_id}, '
          f'"voice": "{res0}_charavoice", "delay": 0 }}')
    print()
    print("# Scheme B (multi-bundle hack via URL relative-path):")
    print(f'  "voice": "sound/voice/newsituationintroduction/_",')
    for res, _ in available:
        print(f'  // in talk.voices: {{ "character": {character_id}, '
              f'"voice": "../{res}_rip/{res}_charavoice", "delay": 0 }}')

def check_voice(bundle: str, file: str, server: str = "jp") -> None:
    """Verify that a (voice bundle, voice file) pair resolves to an audio mp3.
    bundle = what goes into storySource top-level `voice`
    file   = what goes into talk.voices[].voice  (without .mp3)
    Mirrors viewer's getVoiceUrl: /assets/<server>/<bundle>_rip/<file>.mp3 ."""
    bundle = bundle.strip("/")
    if file.endswith(".mp3"):
        file = file[:-4]
    url = f"https://bestdori.com/assets/{server}/{bundle}_rip/{file}.mp3"
    print(f"GET {url}")
    status, ct, cl = _head_meta(url)
    print(f"  status={status} content-type={ct} content-length={cl}")
    if status == 200 and ct.startswith("audio/"):
        print(f"  ✅ usable as voice='{bundle}' + voices[].voice='{file}'")
    else:
        print(f"  ❌ not a real mp3 (likely SPA fallback)")
        sys.exit(1)

# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--list-costumes", type=int, metavar="CHAR_ID")
    g.add_argument("--character",     type=int, metavar="CHAR_ID")
    g.add_argument("--validate",      type=str, metavar="STORY_JSON")
    g.add_argument("--list-bg",       type=str, metavar="SUBSTR",
                   help="search bg/* bundles whose path contains SUBSTR")
    g.add_argument("--ls",            type=str, metavar="PATH",
                   help="list one explorer folder, e.g. bg/scenario104")
    g.add_argument("--check-bg",      nargs=2, metavar=("BUNDLE","FILE"),
                   help="real GET to verify a (bundle, file) pair returns an image")
    g.add_argument("--bg-from-explorer", type=str, metavar="URL",
                   help="derive bundle/file from a https://bestdori.com/tool/explorer/asset/... URL")
    g.add_argument("--list-charavoice", type=int, metavar="CHAR_ID",
                   help="probe newsituationintroduction for a character's charavoice bundles")
    g.add_argument("--check-voice",   nargs=2, metavar=("BUNDLE","FILE"),
                   help="real GET to verify a (voice bundle, voice file) pair returns mp3")
    ap.add_argument("--server", default="jp", choices=SERVERS,
                    help="server short code (default: jp)")
    args = ap.parse_args()
    if args.list_costumes is not None:
        list_costumes(args.list_costumes)
    elif args.character is not None:
        show_character(args.character)
    elif args.validate is not None:
        validate_story(args.validate)
    elif args.list_bg is not None:
        list_bg(args.list_bg, args.server)
    elif args.ls is not None:
        ls_path(args.ls, args.server)
    elif args.check_bg is not None:
        check_bg(args.check_bg[0], args.check_bg[1], args.server)
    elif args.bg_from_explorer is not None:
        bg_from_explorer(args.bg_from_explorer)
    elif args.list_charavoice is not None:
        list_charavoice(args.list_charavoice, args.server)
    elif args.check_voice is not None:
        check_voice(args.check_voice[0], args.check_voice[1], args.server)

if __name__ == "__main__":
    main()
