---
name: bestdori-story-creator
description: Create Bestdori community story JSON files (https://bestdori.com/community/stories) from user-provided text/scripts. Use this when the user wants to author a Bandori (BanG Dream! Girls Band Party) visual-novel-style story with characters, costumes, expressions, motions, backgrounds, BGM, sound effects and screen effects. The skill knows the exact storySource JSON schema accepted by Bestdori (actions of type talk/layout/motion/effect/sound), the asset path conventions for character costumes (live2dAssetBundleName), backgrounds, BGM and SE on the JP/EN/TW/CN/KR servers, and how to query characters/costume listings via the public API. Output a ready-to-paste storySource JSON that the user can import in the Bestdori story editor "Source Code" panel.
description_zh: 生成 Bestdori 社区故事 JSON
description_en: Generate Bestdori community story JSON
disable: false
agent_created: true
---

# bestdori-story-creator

A Bestdori "community story" (https://bestdori.com/community/stories/<id>) is a visual-novel-style scenario built from a small set of action records. The site editor accepts and exports a single `storySource` JSON; this skill builds that JSON from user text.

## When to use

Trigger this skill when the user:
- asks to "create / 写 / 生成 / 改编 一个 Bestdori 故事" or anything resembling a Bandori (BanG Dream! Girls Band Party) story scenario
- supplies dialogue text and asks you to add characters / backgrounds / BGM / costumes / expressions / motions
- references the editor at https://bestdori.com/community/stories/new or an existing story (e.g. https://bestdori.com/community/stories/222138) and wants something similar
- asks about character costumes (e.g. Soyo Nagasaki id 39), Bandori backgrounds, or BGM that can be plugged into a story

Do NOT use this skill for game charts (note charts), only narrative stories.

## Reference materials

Skill 自带三份参考资料，都在 `references/` 下：

1. **`references/bestdori-asset-catalog.md`** —— **首选参考**。已实测的角色 id（1-40 完整表）、可用服装模板、按场景分类的背景 bundle、按情绪分类的 78 首可用 BGM、以及"已知失效"的 BGM 黑名单和一键复制的 storySource 片段。**写故事前先查这一份**，可以省 80% 的探索时间。
2. **`references/bestdori-story-schema.md`** —— 完整 storySource JSON schema、URL 拼接规则、所有 action 类型的字段定义。
3. **`references/sample_story_222138.json`** —— 一个真实发布的社区故事，可以参考别人的写法。

Helper script `scripts/build_story.py` 提供：
- `--list-costumes <character_id>` 列出某角色全部服装的 `assetBundleName`
- `--character <character_id>` 输出该角色基本信息和季节服装
- `--list-bg <substring>` 在 `_info.json` 里搜 `bg/*` bundle
- `--ls <path>` 列出某个 explorer 目录的全部文件
- `--check-bg <bundle> <file>` 真实 GET 验证 (bundle, file) 返回 `image/*`
- `--bg-from-explorer <url>` 从 Asset Explorer URL 直接推导出 storySource bundle/file
- `--list-charavoice <character_id>` 探查某角色 newsituationintroduction 下的 charavoice 资源
- `--check-voice <bundle> <file>` 真实 GET 验证 (voice bundle, voice file) 返回 `audio/*`
- `--validate <story.json>` 校验 storySource，包含"裸 leaf bundle"静态检查

## Workflow

### 1. Clarify what the user wants
Before writing JSON, confirm at minimum:
- The full dialogue / narration text (in order)
- For each speaking line: who is speaking (character id or name)
- Optional: scene background (Bandori asset name OR a custom URL), BGM (Bandori file name OR custom URL), opening telop, fade transitions

Use sensible defaults if the user does not specify (`server: 0` = JP, no BGM, custom narration with empty `name`).

### 2. Resolve characters and costumes

完整角色 id 表见 `references/bestdori-asset-catalog.md` §1。常用速查（id 都是真实可用的，已实测）：

| id | name | band |
|----|------|------|
| 1 | 戸山 香澄 Kasumi | Poppin'Party |
| 4 | 山吹 沙綾 Saya | Poppin'Party |
| 11 | 弦巻 こころ Kokoro | Hello, Happy World! |
| 16 | 丸山 彩 Aya | Pastel\*Palettes |
| 21 | 湊 友希那 Yukina | Roselia |
| 22 | 氷川 紗夜 Sayo | Roselia |
| 26 | 倉田 ましろ Mashiro | Morfonica |
| 31 | 和奏 レイ Layer | RAS |
| 36 | 高松 燈 Tomori | MyGO!!!!! |
| 37 | 千早 愛音 Anon | MyGO!!!!! |
| 38 | 要 楽奈 Raana | MyGO!!!!! |
| 39 | 長崎 そよ Soyo | MyGO!!!!! |
| 40 | 椎名 立希 Taki | MyGO!!!!! |

> ⚠️ **Ave Mujica（豊川祥子、若葉睦、八幡海鈴、祐天寺燈和、三角初華）目前没有可用 live2d 模型** —— Bestdori 的 character API 在 id=40 之后直接跳到 NPC（id 201+）和 mob（id 1001+），所以涉及这五个角色的同人故事，只能用旁白 + name 字段假装、或换成已有 live2d 的角色。

For each character, resolve a `live2dAssetBundleName`. Two ways:
- `<id-3-digit>_casual-2023` (default casual) — usually exists for current characters, e.g. `039_casual-2023`
- API: `https://bestdori.com/api/characters/<id>.json` → `seasonCostumeListMap.entries.season_X.entries[*].live2dAssetBundleName` for season casual / school uniform variants.
- Catalog: `https://bestdori.com/api/costumes/all.5.json` (large, ~600 KB) — filter by `characterId == <id>` to enumerate every costume's `assetBundleName`.

Use `scripts/build_story.py --list-costumes <character_id>` to print available costume bundles.

### 3. Pick backgrounds, BGM, SE

**Backgrounds — prefer `type: "bandori"` with a full sub-path bundle.** The community-story viewer composes the image URL with this exact JS:

```js
getImageUrl(bundle, file) {
  return bundle === "BESTDORI##URL" ? file : "/assets/" + server + "/" + bundle + "_rip/" + file + ".png";
}
```

So a `{type:"bandori", bundle:"<sub/path>", file:"<name>"}` background resolves to `/assets/<server>/<sub/path>_rip/<name>.png`. The Bestdori Asset Explorer URL is the source of truth — there is a clean 1-to-1 mapping:

```
Asset Explorer:  https://bestdori.com/tool/explorer/asset/jp/bg/scenario104
                                                          \___server__/\__bundle__/  (file is one level deeper)
File listing:    https://bestdori.com/api/explorer/jp/assets/bg/scenario104.json
                 → ["bg-scenario104.bundle","bg01040.png","bg01041.png", ...]
Real image URL:  https://bestdori.com/assets/jp/bg/scenario104_rip/bg01040.png   (Content-Type: image/png ✅)

storySource: { "type": "bandori", "bundle": "bg/scenario104", "file": "bg01040" }
```

**The `bundle` field MUST be the full sub-path** (e.g. `bg/scenario104`), not just the leaf segment. Writing `bundle: "scenario104"` or `bundle: "event235_back"` produces a broken URL. The `file` field is the asset name **without extension**.

How to discover and verify backgrounds:

1. Browse the asset tree via `https://bestdori.com/api/explorer/jp/assets/_info.json` (full catalog, ~600KB). Subtrees of interest:
   - `bg.scenarioNNN` (10–12 each) → ordinary scene backgrounds (school, classroom, café, station, …)
   - `bg.afterlive.<skin>`, `bg.result.<skin>` → live result/outro art
   - `bg.common` → generic fallbacks
   - Use `python scripts/build_story.py --list-bg <substring>` to filter, or `--ls <path>` to list one bundle.
2. For an exact bundle, the per-folder JSON gives you the file list:
   `curl -s https://bestdori.com/api/explorer/jp/assets/bg/scenario104.json` → file names. Drop the `.png` to use as `file`.
3. Verify any image URL with a real GET (do not trust `curl -I` alone — see *Pitfalls*):
   ```bash
   curl --max-time 15 -sSD /tmp/h -o /tmp/b "<URL>" >/dev/null
   grep -i '^Content-Type' /tmp/h     # must be image/png, NOT text/html
   ```
   `python scripts/build_story.py --check-bg <bundle> <file>` does the same in one call.

**Use `type: "custom"` only as a fallback** when:
- The asset is not in the bestdori explorer (user uploads / external art).
- You need a non-PNG (JPEG, GIF, …).
- A bestdori bundle exists but its PNG genuinely 404s on a real GET (rare for `bg/*`; common for some `scenario/*_back` bundles which only ship as packed `_rip/buildData.asset` Live2D bundles, not flat PNGs).

Working `custom` URLs:
- A Bestdori user upload: `https://bestdori.com/api/upload/file/<sha1>` (served as image)
- A third-party CDN with permissive CORS, e.g. `https://images.unsplash.com/photo-XXXXXX?w=1600`

**BGM** — same rule. The viewer code is:
```js
getBgmUrl(name) {
  return "/assets/" + storyData.urlBgm + name.toLowerCase() + "_rip/" + name + ".mp3";
}
```
On community routes `storyData.urlBgm` is `"<server>/sound/scenario/bgm/"`, so `{type:"bandori", file:"<NAME>"}` maps to `/assets/<server>/sound/scenario/bgm/<name-lower>_rip/<NAME>.mp3`. Browse names at `https://bestdori.com/tool/explorer/asset/jp/sound/scenario/bgm`. Verified working examples on jp:
- `{type:"bandori", file:"03_Normal"}` → `/assets/jp/sound/scenario/bgm/03_normal_rip/03_Normal.mp3`
- For anything not published as a flat `.mp3`, use `type: "custom"` with an HTTPS URL or set `bgm: null`.

**SE** — `se.type: "common"` works for the built-in set (e.g. `se_common_001`). For anything else, use `custom` with an HTTPS URL.

**BGM 编排原则**（写多场景故事时务必遵守，避免"一直播放"或"硬切刺耳"）：

> 关键背景：viewer 的 BGM 切换是**硬切（无 fade）+ 默认 loop:true**。详见 `references/bestdori-asset-catalog.md` §4.2。

1. **🔑 哑场过渡 = 解决硬切的最佳办法**：从 BGM A 切到 BGM B 之前，先插一条 `{"type":"sound","wait":false,"delay":0,"bgm":null,"se":null}` 让对话走 1-2 行（约 3 秒），再切到 B。听感远胜直接硬切。
2. **🔑 同一首 BGM 不要连覆盖 12 行以上 talk**：BGM 默认循环，一首 1.5 分钟约 18-30 行循环一次。超过 12 行就主动切换，避免循环重启的尴尬。
3. **关键转折用 `bgm:null` 留白**——告白前犹豫、第一次牵手、震惊瞬间，静音比任何 BGM 都有张力。
4. **过渡桥曲**：`34_piano_weak`（弱钢琴）、`75_wave_wind`（风声）、`42_upper_window`、`heartbeat_cresc`（心跳）等"听感很弱"的曲子用作两首主导曲之间的过渡，听感平滑。
5. **避免相邻两首"情绪相似旋律不同"硬切**——`63_longing` → `73_longing_2`、`crychic_01` → `crychic_01_vocal`，听感反而像故障。中间务必加 null 或弱钢琴。
6. **环境音也是 BGM**：`75_wave_wind` `65_rain_light` `44_crowd_people` 当 BGM 用比纯静音更有空间感。
7. **章节结尾用渐弱型钢琴曲**：`seeyou_piano` `34_piano_weak` `crychic_01` 开头很弱，配合 `blackOut` 听感像自然淡出。
8. **每 6-12 行换一次 BGM**——不要太频繁（每 1-2 行切一次反而捕捉不到旋律），也不要长期不切（循环开始重复）。
9. **情绪与曲目对应表**（详见 catalog §4.1）：
   - 暧昧伤感 → `63_longing` `73_longing_2` `62_sense` `seeyou_piano`
   - 真心 / 卸下伪装 → `crychic_01` `nakanai_na_kanai` `mygo_04_scenario`
   - 告白顶点宣泄 → `33_piano_full_concert`
   - Live 余热 → `60_exciting_live`
   - 雨景 → `65_rain_light` → `66_rain_light_umbrella`
   - 黄昏外景 → `44_evening`

### 4. Compose the actions array
The whole story is `storySource.actions: []`. Action types:

#### `talk` — dialogue / narration
```json
{ "type": "talk", "name": "長崎 そよ", "body": "...", "wait": true, "close": false, "delay": 0,
  "characters": [1, 39],
  "motions": [ {"character": 39, "motion": "nf02", "expression": "smile01", "delay": 0} ],
  "voices":  [ {"character": 39, "voice": "<voice-file-or-url>", "delay": 0} ] }
```
- `name: " "` (single space) = nameless narration window.
- `characters` is the list of on-stage character ids that should be **highlighted** while this line plays (others dim). Leave empty for full-screen narration.
- `motions` / `voices` items are optional. Empty arrays are fine.

#### `layout` — show / hide / move a character
```json
{ "type": "layout", "layoutType": "appear", "character": 39, "costume": "039_casual-2023",
  "motion": "nf01", "expression": "", "sideFrom": "leftInside", "sideTo": "leftInside",
  "sideFromOffsetX": 0, "sideToOffsetX": 0, "wait": true, "delay": 0 }
```
- `layoutType` ∈ `appear | hide | move`.
- `sideFrom`/`sideTo` ∈ `none, left, leftOver, leftInside, center, right, rightOver, rightInside, leftUnder, leftInsideUnder, centerUnder, rightUnder, rightInsideUnder` (Under = behind another character).
- For `appear`, set `sideFrom == sideTo` if you don't want a slide-in animation.
- `motion` is the body pose (e.g. `nf01..nf12`); `expression` is the face (`""` keeps current). See references for known suffixes.

#### Multi-character layout strategy

The viewer renders characters at only **3 real X coordinates**: left group (x≈-0.34), center (x=0), right group (x≈+0.34). `offsetX` shifts within a group; 1 unit = 1 pixel, scaled by 1/640. To push a character ~1/3 screen width, use `offsetX ≈ 200`.

**Key principle: shift existing characters BEFORE a new one appears.** When the cast size changes (N→N+1), pre-move the existing characters to create a balanced slot, then `appear` the newcomer. When a character leaves, move the remaining ones back to centered positions.

| 同框人数 | 推荐站位 | offsetX |
|---------|---------|---------|
| 2 | `leftInside` + `rightInside` | 0 / 0 |
| 3 | `leftInside` + `center` + `rightInside` | **-100 / 0 / +100** |
| 4 | `leftInside`(-250) + `center`(-150) + `center`(+150) + `rightInside`(+250) | **-250 / -150 / +150 / +250** |
| 5 | `left`(-200) + `left`(0) + `center`(0) + `right`(0) + `right`(+200) | -200 / 0 / 0 / 0 / +200 |

**3 人较之前稍宽**（避免挤在一起的问题），3 人的 left/right 用 offsetX ±100。
**4 人用 center-split 法**：center 组拆成两半（-150/+150），搭配左右组获得 4 个均匀分布的 x 坐标（间隙 ~0.5 屏宽）。

**Example: 3→4 transition (someone enters mid-scene)**

Before the newcomer's `appear`, insert `move` actions (`wait: false`) to shift existing characters into the balanced 4-person layout. Then the newcomer `appears` into the freed slot:

```
Phase 1 (3人): Soyo(leftInside -100)  Taki(center 0)  Tomori(rightInside +100)
Phase 2 (shift): Soyo -100→-250,  Taki 0→center -150,  Tomori rightInside +100→center +150
Phase 3 (4人): Soyo(leftIn -250)  Taki(center -150)  Tomori(center +150)  Anon(rightIn +250)
```

After characters leave, move remaining ones back to centered 2-person positions.

**`wait: false` on move actions** lets them overlap with the next dialogue — the character slides while text is showing, which feels natural. Use `wait: true` on `appear`/`hide` so the character finishes entering/exiting before the next line.

#### `motion` — change pose / expression on an already-shown character
```json
{ "type": "motion", "character": 39, "costume": "039_casual-2023",
  "motion": "nf05", "expression": "surprised01", "wait": false, "delay": 0 }
```

#### `effect` — screen / scene effect
```json
{ "type": "effect", "effectType": "telop", "text": "Chapter 1", "wait": true, "delay": 0 }
{ "type": "effect", "effectType": "blackIn",  "duration": 1.0, "wait": true, "delay": 0 }
{ "type": "effect", "effectType": "blackOut", "duration": 1.0, "wait": true, "delay": 0 }
{ "type": "effect", "effectType": "whiteIn",  "duration": 1.0, "wait": true, "delay": 0 }
{ "type": "effect", "effectType": "whiteOut", "duration": 1.0, "wait": true, "delay": 0 }
{ "type": "effect", "effectType": "changeBackground",
  "background": {"type": "bandori", "bundle": "bg/scenario104", "file": "bg01040"},
  "wait": true, "delay": 0 }
{ "type": "effect", "effectType": "changeCardStill",
  "bundle": "characters/resourceset/res039001", "file": "card_normal", "wait": true, "delay": 0 }
```

#### `sound` — play BGM and/or SE
```json
{ "type": "sound", "wait": false, "delay": 0,
  "bgm": {"type": "bandori", "file": "03_Normal"},
  "se":  {"type": "common",  "se": "se_common_001"} }
```
Pass `null` for `bgm` or `se` to leave them unchanged. To stop BGM, send a sound action with `bgm.type: "custom"` and `bgm.url: ""`.

### 5. Assemble the storySource

Top-level shape:
```json
{
  "server": 0,
  "voice": "",
  "bgm": null,
  "background": { "type": "bandori", "bundle": "bg/scenario104", "file": "bg01040" },
  "actions": [ ...action objects in chronological order... ]
}
```
- `server` ∈ 0=jp, 1=en, 2=tw, 3=cn, 4=kr. Default 0.
- `bgm` (top level) sets the *initial* BGM the moment the story starts. `null` = silence.
- `background` (top level) sets the initial scene; same shape as the `effect.changeBackground.background`.

### 6. Output and deliver
1. Run `python scripts/build_story.py --validate <file>` (or call it inline) to confirm the JSON is well-formed and uses known enum values.
2. Save the final JSON to the workspace, e.g. `C:\Generate\bestdori_story_<title>.json`.
3. Tell the user how to use it:
   - Open https://bestdori.com/community/stories/new
   - Open the *Source Code → Import* panel and paste the JSON, or click *Source Code → Import game story* if it's an official scenario asset.
   - Click Publish when ready.
4. Use `deliver_attachments` to deliver the `.json` file to the user.

## Pitfalls

- **Bestdori's nginx fallback returns 200 + `text/html` for any unknown `/assets/...` path.** A `curl -I` returning 200 OK is NOT proof the asset exists — the body is the SPA index.html. Always verify with a GET that returns the right `Content-Type` (image/png, image/jpeg, audio/mpeg, etc.). `python scripts/build_story.py --check-bg <bundle> <file>` automates this.
- **`bundle` must be the FULL sub-path** under `/assets/<server>/`, not just a leaf segment. Use `bg/scenario104`, not `scenario104`. Use the Asset Explorer URL (e.g. `https://bestdori.com/tool/explorer/asset/jp/<sub/path>`) as the source of truth — everything after `/jp/` is your `bundle`. The `file` is the asset name **without `.png`**.
- **Some bundles only ship as packed Live2D `_rip/buildData.asset`, not flat PNGs.** This is true for many `scenario/*_back` event-story backgrounds — referring to them as `type:"bandori"` will silently 404. The `bg/scenarioNNN` family is fine; if your chosen bundle fails the GET check, switch that one to `type:"custom"` with an external image URL.
- The Bestdori editor uses **0-based indexing internally for the character dropdown** but writes 1-based ids in the JSON. Always store the real character id (1..40) in `character`, not 0.
- `wait: true` means "block until this finishes". For things like `motion` and `sound` you usually want `wait: false` so the next dialogue plays immediately.
- The viewer hard-fails if `costume` (a `live2dAssetBundleName`) does not exist for the given character. When in doubt, fall back to `<NNN>_casual-2023` (verified to exist for all current Bandori band members) or query the costume catalog API.
- Don't put narration text inside a `layout`/`motion`/`effect`/`sound` action — those are silent. Use `talk` actions for any visible text.
- Custom assets (`background.type: "custom"`, `bgm.type: "custom"`) need a publicly reachable HTTPS URL (Bestdori upload, Imgur, etc.). Local file paths will not work.
- `name: " "` (single space) is the convention for nameless narration. An empty string sometimes still draws an empty bubble.
- The site name field localization: `name` is a single string (not localized). Pick the language that matches the rest of the dialogue.

## Verification

After generating the JSON:
1. `python scripts/build_story.py --validate <generated.json>` should print `OK`.
2. Spot-check that every `costume` referenced exists (script does this).
3. Open the editor at https://bestdori.com/community/stories/new and paste into *Source Code → Import* — the preview should render without console errors.
