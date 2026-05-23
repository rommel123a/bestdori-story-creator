# Bestdori storySource — full reference

This document is reverse-engineered from the Bestdori community-story editor JS bundles
(`/js/CommunityStoriesNew.*.js`, `/js/ToolStoryViewerSingle.*.js`, `/js/app.*.js`) and
verified against the live community-story API
(`https://bestdori.com/api/post/details?id=<id>`).

## 1. Top-level

```jsonc
{
  "server": 0,                 // 0 jp · 1 en · 2 tw · 3 cn · 4 kr
  "voice":  "",                // optional voice-bundle prefix; "" means none
  "bgm":    null,              // initial BGM, see §5; null = silent
  "background": {              // initial background, see §4
    "type": "bandori",
    "bundle": "bg/scenario104",
    "file":   "bg01040"
  },
  "actions": [ /* see §3 */ ]
}
```

The story plays each action top-to-bottom. `wait: true` blocks until the action is done;
`wait: false` lets the next action start immediately (overlapping animations).

## 2. Servers and asset URLs

The community-story viewer composes asset URLs with this exact JS (from
`/js/CommunityStoriesNew.*.js` and `/js/CommunityStoriesSingle.*.js`):

```js
getImageUrl(bundle, file) {
  return bundle === "BESTDORI##URL"
    ? file
    : "/assets/" + serverShort + "/" + bundle + "_rip/" + file + ".png";
}
getBgmUrl(name) {
  return name && name.startsWith("BESTDORI##URL:")
    ? name.substring(14)
    : "/assets/" + storyData.urlBgm + name.toLowerCase() + "_rip/" + name + ".mp3";
}
```

`storyData.urlBgm` is hard-coded to `"<server>/sound/scenario/bgm/"` for community
stories. So a `{type:"bandori", file:"03_Normal"}` BGM resolves to
`/assets/jp/sound/scenario/bgm/03_normal_rip/03_Normal.mp3`.

The general pattern is:

```
/assets/<server>/<bundle>_rip/<file>.<ext>
```

with `<server>` from `["jp","en","tw","cn","kr"]` (top-level `server` index).

### Asset Explorer ⇄ storySource mapping

The Bestdori Asset Explorer (`https://bestdori.com/tool/explorer/asset/<server>/<path>`)
mirrors the on-disk tree exactly. Everything between `/asset/<server>/` and the file
leaf is your `bundle`; the file leaf without `.png` is your `file`.

| Asset Explorer URL                                                     | bundle              | file       |
|------------------------------------------------------------------------|---------------------|------------|
| `…/explorer/asset/jp/bg/scenario104` → contains `bg01040.png`          | `bg/scenario104`    | `bg01040`  |
| `…/explorer/asset/jp/bg/scenario105` → contains `bg01051.png`          | `bg/scenario105`    | `bg01051`  |
| `…/explorer/asset/jp/bg/afterlive/skin02`                              | `bg/afterlive/skin02` | `…`      |
| `…/explorer/asset/jp/sound/scenario/bgm/03_Normal` → `03_Normal.mp3`   | (BGM uses `file:"03_Normal"`, viewer derives the rest) | — |

### Discovery APIs

- **Full catalog (one request):** `https://bestdori.com/api/explorer/<server>/assets/_info.json`
  — a nested object describing every bundle and its child count. Use this to enumerate
  available bundles offline.
- **One folder's file list:** `https://bestdori.com/api/explorer/<server>/assets/<path>.json`
  e.g. `…/assets/bg/scenario104.json` → `["bg-scenario104.bundle","bg01040.png", …]`.
  Drop the `.png` to get a usable `file` value.

### Verification

Bestdori's nginx returns `200 OK` with `Content-Type: text/html` (the SPA index)
for any unknown `/assets/...` path. Always verify with a real GET:

```bash
curl --max-time 15 -sSD /tmp/h -o /tmp/b "<URL>" >/dev/null
grep -i '^Content-Type' /tmp/h     # must be image/png, image/jpeg, audio/mpeg, …
```

### Selected URL templates observed in the JS

| asset                        | URL pattern                                                     |
|------------------------------|------------------------------------------------------------------|
| Live2D model (chara)         | `/assets/<server>/live2d/chara/<live2dAssetBundleName>_rip/...` |
| Story scenario script        | `/assets/<server>/scenario/eventstory/event<id>_rip/Scenario<scenarioId>.asset` |
| Voice (event story)          | `/assets/<server>/sound/voice/scenario/eventstory<id>_<chapter>_rip/<line>.mp3` |
| BGM (story-bundled)          | `/assets/<server>/sound/scenario/bgm/<file_lower>_rip/<file>.mp3` |
| Background (bg/*)            | `/assets/<server>/bg/<sub>_rip/<file>.png`                      |
| SD chibi                     | `/assets/<server>/characters/livesd/<sdAssetBundleName>_rip/sdchara.png` |

## 3. Action types

### 3.1 `talk`

```jsonc
{
  "type": "talk",
  "name": "長崎 そよ",      // " " = nameless narration
  "body": "...dialog...",
  "wait": true,             // true = wait for player click before next
  "close": false,           // true = close the dialog window when finished
  "delay": 0,               // seconds
  "characters": [1, 39],    // ids of on-stage chars to *highlight* (others dim)
  "motions": [              // optional pose/expression changes triggered with this line
    { "character": 39, "motion": "nf02", "expression": "smile01", "delay": 0 }
  ],
  "voices":  [              // optional voice playback triggered with this line
    { "character": 39, "voice": "<bundle/file or url>", "delay": 0 }
  ]
}
```

### 3.2 `layout`

```jsonc
{
  "type": "layout",
  "layoutType": "appear",   // appear | hide | move
  "character": 39,          // 1..40 (real character id); 40 reserved for "other"
  "costume": "039_casual-2023",
  "motion":  "nf01",        // body pose; nfXX, posXX etc.
  "expression": "",         // face; smile01, surprised01, sad01, "" = keep
  "sideFrom": "leftInside",
  "sideTo":   "leftInside",
  "sideFromOffsetX": 0,
  "sideToOffsetX":   0,
  "wait": true,
  "delay": 0
}
```

`side*` enum (from the editor's i18n table):

| value             | meaning                                 |
|-------------------|------------------------------------------|
| none              | leave at current position                |
| left              | left edge                                |
| leftOver          | left, overlapping the left character    |
| leftInside        | left, inset from edge                   |
| center            | center                                   |
| right             | right                                    |
| rightOver         | right, overlapping right                 |
| rightInside       | right, inset from edge                  |
| leftUnder         | left, behind another sprite              |
| leftInsideUnder   | leftInside, behind                       |
| centerUnder       | center, behind                           |
| rightUnder        | right, behind                            |
| rightInsideUnder  | rightInside, behind                      |

For `layoutType: "hide"`, only `character` is required (other fields can stay default).
For `layoutType: "move"`, set `sideFrom` to current side and `sideTo` to new side.

### 3.3 `motion`

Change pose / expression of an already-on-stage character without re-positioning.

```jsonc
{
  "type": "motion",
  "character": 39,
  "costume":  "039_casual-2023",
  "motion":   "nf05",
  "expression": "surprised01",
  "wait": false,
  "delay": 0
}
```

### 3.4 `effect`

```jsonc
{ "type": "effect", "effectType": "telop", "text": "Chapter 1", "wait": true, "delay": 0 }

{ "type": "effect", "effectType": "blackIn",  "duration": 1.0, "wait": true, "delay": 0 }
{ "type": "effect", "effectType": "blackOut", "duration": 1.0, "wait": true, "delay": 0 }
{ "type": "effect", "effectType": "whiteIn",  "duration": 1.0, "wait": true, "delay": 0 }
{ "type": "effect", "effectType": "whiteOut", "duration": 1.0, "wait": true, "delay": 0 }

{ "type": "effect", "effectType": "changeBackground",
  "background": { "type": "bandori", "bundle": "bg/scenario104", "file": "bg01040" },
  "wait": true, "delay": 0 }
// or custom:
{ "type": "effect", "effectType": "changeBackground",
  "background": { "type": "custom", "url": "https://…/bg.png" },
  "wait": true, "delay": 0 }

{ "type": "effect", "effectType": "changeCardStill",
  "bundle": "characters/resourceset/res039001", "file": "card_normal_5", "wait": true, "delay": 0 }
```

### 3.5 `sound`

```jsonc
{
  "type": "sound",
  "wait": false,
  "delay": 0,
  "bgm":  { "type": "bandori", "file": "03_Normal" },
  "se":   { "type": "common",  "se":   "se_common_001" }
}
```

`bgm.type` ∈ `bandori | custom`.
`se.type`  ∈ `common | bandori | custom`.

For "bandori" use the file name visible in the Asset Explorer (no extension).
For "custom" provide an HTTPS `url`.
Pass `null` instead of an object to leave that channel untouched.

## 4. Backgrounds

Two shapes are interchangeable: as the top-level `background` or inside an
`effect.changeBackground.background`.

```jsonc
// game-bundled — RECOMMENDED. bundle = full sub-path under /assets/<server>/.
{ "type": "bandori", "bundle": "bg/scenario104", "file": "bg01040" }

// user upload / external image — fallback.
{ "type": "custom",  "url": "https://…/bg.png" }
```

The `bundle` field holds the **full** path between `/assets/<server>/` and the
final filename, e.g. `bg/scenario104`, `bg/afterlive/skin02`, `bg/result/skin_cafe`.
Writing only the leaf segment (`scenario104`) breaks the URL.

The `file` is the asset name **without `.png`**.

Browse strategies (use `python scripts/build_story.py --list-bg <substring>` to
search the catalog):

- `bg.scenarioNNN` (10–12 each) → ordinary scenes (school, classroom, café, station, train, …).
  Pictured at `https://bestdori.com/tool/explorer/asset/jp/bg/scenarioNNN`.
- `bg.afterlive.<skin>`, `bg.result.<skin>` → live-result / live-outro art.
- `bg.common` → generic fallbacks.
- `card_back/<NNN>` → card backgrounds, in `card_back/...` rather than `bg/...`.

Subtrees that look like backgrounds but usually do **not** ship as flat PNG:
- `scenario/event<NN>_back` and similar `*_back` Live2D scenery — these are
  packed `_rip/buildData.asset` Live2D bundles. Asking the viewer for
  `bundle:"scenario/event<NN>_back"` will silently 404. Use a `bg/...` bundle
  or `type:"custom"` instead.

Verify any chosen `(bundle, file)` pair with
`python scripts/build_story.py --check-bg <bundle> <file>` (it does a real GET and
asserts `Content-Type: image/*`).

## 5. BGM

Same shape as backgrounds, but inside `sound.bgm`:

```jsonc
{ "type": "bandori", "file": "03_Normal" }    // → /assets/jp/sound/scenario/bgm/03_normal_rip/03_Normal.mp3
{ "type": "custom",  "url":  "https://…/track.mp3" }
```

Note `getBgmUrl` lower-cases the bundle segment but keeps the original case in
the file name — so `file:"03_Normal"` (capital N) is correct, not `03_normal`.

Browse names: https://bestdori.com/tool/explorer/asset/jp/sound/scenario/bgm
Verify with `curl --max-time 10 -sSI "<URL>"` and check `Content-Type: audio/mpeg`.
Verified-working examples on jp: `03_Normal`.

## 6. Characters and costumes

### Character ids (1-based, 0 means "narrator/none")

The Bandori cast that is currently on the site (id → character):

| id | name (jp) | name (en) | band |
|----|-----------|-----------|------|
| 1  | 戸山 香澄  | Kasumi Toyama       | Poppin'Party |
| 2  | 花園 たえ  | Tae Hanazono        | Poppin'Party |
| 3  | 牛込 りみ  | Rimi Ushigome       | Poppin'Party |
| 4  | 山吹 沙綾  | Saya Yamabuki       | Poppin'Party |
| 5  | 市ヶ谷 有咲| Arisa Ichigaya      | Poppin'Party |
| 6  | 美竹 蘭    | Ran Mitake          | Afterglow    |
| 7  | 青葉 モカ  | Moca Aoba           | Afterglow    |
| 8  | 上原 ひまり| Himari Uehara       | Afterglow    |
| 9  | 宇田川 巴  | Tomoe Udagawa       | Afterglow    |
| 10 | 羽沢 つぐみ| Tsugumi Hazawa      | Afterglow    |
| 11 | 弦巻 こころ| Kokoro Tsurumaki    | Hello, Happy World! |
| 12 | 瀬田 薫    | Kaoru Seta          | Hello, Happy World! |
| 13 | 北沢 はぐみ| Hagumi Kitazawa     | Hello, Happy World! |
| 14 | 松原 花音  | Kanon Matsubara     | Hello, Happy World! |
| 15 | 奥沢 美咲 / ミッシェル | Misaki Okusawa | Hello, Happy World! |
| 16 | 丸山 彩    | Aya Maruyama        | Pastel*Palettes |
| 17 | 氷川 日菜  | Hina Hikawa         | Pastel*Palettes |
| 18 | 白鷺 千聖  | Chisato Shirasagi   | Pastel*Palettes |
| 19 | 大和 麻弥  | Maya Yamato         | Pastel*Palettes |
| 20 | 若宮 イヴ  | Eve Wakamiya        | Pastel*Palettes |
| 21 | 湊 友希那  | Yukina Minato       | Roselia      |
| 22 | 氷川 紗夜  | Sayo Hikawa         | Roselia      |
| 23 | 今井 リサ  | Lisa Imai           | Roselia      |
| 24 | 宇田川 あこ| Ako Udagawa         | Roselia      |
| 25 | 白金 燐子  | Rinko Shirokane     | Roselia      |
| 26 | 倉田 ましろ| Mashiro Kurata      | Morfonica    |
| 27 | 桐ヶ谷 透子| Toko Kirigaya       | Morfonica    |
| 28 | 広町 七深  | Nanami Hiromachi    | Morfonica    |
| 29 | 二葉 つくし| Tsukushi Futaba     | Morfonica    |
| 30 | 八潮 瑠唯  | Rui Yashio          | Morfonica    |
| 31 | 和奏 レイ  | Rei Wakana / Layer  | RAS          |
| 32 | 朝日 六花  | Rokka Asahi / Lock  | RAS          |
| 33 | 佐藤 ますき| Masuki Sato / Masking | RAS        |
| 34 | 鳰原 令王那| Reona Nyubara / PAREO | RAS        |
| 35 | 珠手 ちゆ  | Chiyu Tamade / CHU² | RAS          |
| 36 | 高松 燈    | Tomori Takamatsu    | MyGO!!!!!  |
| 37 | 千早 愛音  | Anon Chihaya        | MyGO!!!!!  |
| 38 | 要 楽奈    | Rana Kaname         | MyGO!!!!!  |
| 39 | 長崎 そよ  | Soyo Nagasaki       | MyGO!!!!!  |
| 40 | 椎名 立希  | Taki Shina          | MyGO!!!!!  |

> ⚠️ **Ave Mujica（豊川祥子、若葉睦、八幡海鈴、祐天寺燈和、三角初華）目前没有 live2d 模型** —— Bestdori 在 id=40 之后直接是 NPC（id 201+）和 mob（id 1001+）。涉及他们的同人故事只能用 name + 旁白假装。

Confirm a single character with: `https://bestdori.com/api/characters/<id>.json`.

### Costume bundle naming

A character's `live2dAssetBundleName` is what goes into a `layout`/`motion` action's
`costume`. Common patterns:

| pattern                              | meaning                       | example                  |
|--------------------------------------|-------------------------------|--------------------------|
| `NNN_casual-2023`                    | seasonal casual (current art) | `039_casual-2023`        |
| `NNN_school_winter-2023`             | winter uniform                | `039_school_winter-2023` |
| `NNN_school_summer-2023`             | summer uniform                | `039_school_summer-2023` |
| `NNN_live_default`                   | default live stage outfit     | `039_live_default`       |
| `NNN_live_event_<event>_<rarity>`    | event card outfit             | `039_live_event_235_ur`  |
| `NNN_live_sr_01`, `NNN_live_ur_02`   | gacha card outfits            | `039_live_sr_01`         |

Where `NNN` is the character id zero-padded to 3 digits.

For Soyo Nagasaki (id 39) the season list returned by the character API is:

| seasonCostumeType  | live2dAssetBundleName        |
|--------------------|-------------------------------|
| CASUAL_SPRING      | 039_casual-2023               |
| UNIFORM_WINTER     | 039_school_winter-2023        |
| UNIFORM_SUMMER     | 039_school_summer-2023        |

To enumerate every costume for a character, fetch
`https://bestdori.com/api/costumes/all.5.json` and filter by `characterId == <id>`. Each
record is keyed by costume id and exposes `assetBundleName` (use as `costume`) and
`description` (5-language label).

### Motions and expressions

Bandori live2d motion names follow short prefixes. Frequent values seen in real stories:

- `nf01` – `nf12`  → neutral / talking poses
- `pos01` – `pos06` → posed poses
- `clap01`, `nod01`, `bow01` → animation hits
- `expression`: `""`, `smile01`, `smile02`, `sad01`, `surprised01`, `angry01`, `embarrassed01`, `serious01`, `cry01`, `wink01`, `closeeye01`

When a costume does not have a specific motion/expression, the viewer silently falls back
to the default pose; no error is raised, but the character won't move. If you're unsure,
use `nf01` + `""` — they exist for every Live2D bundle.

## 7. Importing into the editor

1. Go to https://bestdori.com/community/stories/new
2. Open the right-hand panel and switch to **Source Code**.
3. Click **Import**, paste the JSON, hit OK.
4. Use the preview pane to scrub through. Edit individual actions on the left if needed.
5. Click **Publish** when done.

The exported `storySource` you get back is identical in shape to the input, so this
schema is round-trip safe.

## 8. Sample

A real, published community story (id 222138) is mirrored at
`./sample_story_222138.json` (trimmed to the first 8 actions for readability).
