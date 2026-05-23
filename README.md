# bestdori-story-creator

将文本/对白脚本转为 Bestdori 社区故事 JSON —— 一个 BanG Dream! 视觉小说风格的同人创作工具。

## 它能做什么

输入一段故事文字（对话 + 旁白），输出一个可直接导入 [Bestdori 故事编辑器](https://bestdori.com/community/stories/new) 的 `storySource.json`，包含：

- **角色立绘**：Live2D 出场/退场/位移，40 个可用角色，每人数十套服装
- **表情动作**：smile / surprised / embarrassed / serious / wink 等 12+ 种表情，nfXX / posXX 体态
- **场景背景**：128 个 scenario 系列背景（教室、街道、Live舞台、星空、雨景…）
- **BGM 配乐**：78 首实测可用曲目，含 MyGO 专曲、氛围钢琴、环境音
- **屏幕特效**：telop 标题卡、blackIn/Out 淡入淡出、背景切换

## 支持角色（id 1–40）

| 乐队 | 成员 |
|------|------|
| Poppin'Party | 香澄(1) 多惠(2) 里美(3) 沙绫(4) 有咲(5) |
| Afterglow | 兰(6) 摩卡(7) 绯玛丽(8) 巴(9) 鸫(10) |
| Hello, Happy World! | 心(11) 薰(12) 育美(13) 花音(14) 美咲(15) |
| Pastel\*Palettes | 彩(16) 日菜(17) 千圣(18) 麻弥(19) 伊芙(20) |
| Roselia | 友希那(21) 纱夜(22) 莉莎(23) 亚子(24) 燐子(25) |
| Morfonica | 真白(26) 透子(27) 七深(28) 筑紫(29) 瑠唯(30) |
| RAS | Layer(31) Lock(32) Masking(33) PAREO(34) CHU²(35) |
| MyGO!!!!! | 灯(36) 爱音(37) 乐奈(38) 素世(39) 立希(40) |

> **Ave Mujica（祥子、睦、海铃、喵梦、初华）暂无 Live2D 模型。** 只能通过旁白 + `name` 字段间接表现。

## 服装系统

每个角色至少有 4 套基础服装，此外还有大量活动卡/抽卡限定立绘：

| 服装类型 | 命名模板 | 示例 |
|----------|----------|------|
| 默认常服 | `NNN_casual-2023` | `039_casual-2023` |
| 夏季校服 | `NNN_school_summer-2023` | `037_school_summer-2023` |
| 冬季校服 | `NNN_school_winter-2023` | `039_school_winter-2023` |
| 默认Live服 | `NNN_live_default` | `036_live_default` |
| 活动卡/抽卡 | `NNN_live_event_XXX_rarity` | `039_live_event_235_ur` |

查看任意角色完整服装列表：
```bash
python scripts/build_story.py --list-costumes <角色id>
```

## 场景背景

使用 `type: "bandori"` + 完整 bundle 子路径。128 个 scenario bundle 覆盖绝大多数场景需求：

| 场景 | bundle:file | 氛围 |
|------|-------------|------|
| 黄昏空教室 | `bg/scenario0` / `bg00002` | 经典暧昧，窗光金色 |
| 黄昏街道 | `bg/scenario0` / `bg00006` | 校园外散步道 |
| 黄昏小巷 | `bg/scenario1` / `bg00018` | 告白圣地 |
| LIVE 舞台 | `bg/scenario2` / `bg00026` | 余热灯光 |
| 星空夜 | `bg/scenario10` / `bg00100` | 流星、终幕 |

```bash
# 搜索背景
python scripts/build_story.py --list-bg classroom

# 从 Asset Explorer URL 直接获取 bundle/file
python scripts/build_story.py --bg-from-explorer "https://bestdori.com/tool/explorer/asset/jp/bg/scenario0"

# 验证图片可用
python scripts/build_story.py --check-bg bg/scenario0 bg00002
```

## BGM 配乐

78 首实测可用的 BGM，按情绪分为 9 大类。核心使用规则：

### 情绪速查

| 情绪 | 推荐曲目 |
|------|----------|
| 日常/平静 | `03_Normal` `64_chillout` `42_upper_window` |
| 思慕/暧昧 | `63_longing` `73_longing_2` `62_sense` |
| 真心/卸伪 | `crychic_01` `nakanai_na_kanai` `mygo_04_scenario` |
| 告白顶点 | `33_piano_full_concert` |
| 黄昏外景 | `44_evening` |
| 雨景 | `65_rain_light` `66_rain_light_umbrella` |
| Live 余热 | `60_exciting_live` |
| 告别/终幕 | `seeyou_piano` `34_piano_weak` |
| 过渡桥 | `34_piano_weak` `heartbeat_cresc` `75_wave_wind` |

### 切换铁律

1. **哑场过渡**：BGM A → `bgm:null` + 1~2行对话 → BGM B。禁止直接硬切
2. **同曲限 12 行**：BGM 默认 loop，单首连续覆盖不超 12 行 talk
3. **关键转折留白**：告白前、牵手瞬间、震惊时刻 → `bgm:null` 比任何 BGM 都有张力
4. **避免相似旋律硬切**：`63_longing → 73_longing_2`、`crychic_01 → crychic_01_vocal` 中间必须加 null
5. **结尾渐弱**：配合 `seeyou_piano` / `34_piano_weak` + `blackOut` 自然淡出

## 多人同框布局

Viewer 只有 3 个真实 X 坐标（左组 -0.34 / 中心 0 / 右组 +0.34），通过 `offsetX`（单位像素，1/640 归一化）在同组内推开。

### 站位速查表

| 人数 | 推荐布局 | offsetX |
|------|----------|---------|
| 2 人 | `leftInside` + `rightInside` | 0 / 0 |
| 3 人 | `leftInside` + `center` + `rightInside` | **-100 / 0 / +100** |
| 4 人 | `leftInside` + `center`×2 + `rightInside` | **-250 / -150 / +150 / +250** |
| 5 人 | `left`×2 + `center` + `right`×2 | -200 / 0 / 0 / 0 / +200 |

### 动态进出场（N→N+1 过渡）

**关键原则：新人出现前，先 shift 旧人腾位。4 人用 center-split 法（两中组分占 center 两侧）实现均匀间距。**

```
3人→4人示例：
  Phase 1: Soyo(leftInside -100)  Taki(center 0)  Tomori(rightInside +100)
  Phase 2: Soyo -100→-250  Taki 0→center -150  Tomori rightInside +100→center +150 (三人同时 shift)
  Phase 3: Anon appear rightInside +250  →  四人均匀居中对齐
  Phase 4: Taki/Tomori hide → Soyo -250→0, Anon +250→0  →  回到2人
```

`move` 用 `wait:false`（与对话并行滑动），`appear`/`hide` 用 `wait:true`（等进出完成）。

## 表情与动作

### 常用表达式

| 字段值 | 效果 | 使用场景 |
|--------|------|----------|
| `""` | 保持当前/默认 | 平静陈述 |
| `smile01` | 微笑 | 日常对话、温暖 |
| `surprised01` | 惊讶 | 突然事件、被说中心事 |
| `embarrassed01` | 害羞 | 脸红、被调侃 |
| `serious01` | 严肃 | 说教、生气、冷面 |
| `wink01` | 眨眼 | 调侃、俏皮 |
| `sad01` | 悲伤 | 低落、回忆 |
| `closeeye01` | 闭眼 | 思考、叹息 |

### 常用体态

`nf01`~`nf12`：中立/说话态
`pos01`~`pos06`：摆姿势
`clap01` `nod01` `bow01`：特殊动作

## 语音支持

整个故事只能用一个 voice bundle。两种方案：

**方案 A — 单角色单语气（推荐）**
```json
"voice": "sound/voice/newsituationintroduction/res039011",
"actions": [
  { "type":"talk", "name":"长崎 爽世", "body":"……怎么会这样呢。",
    "voices": [{ "character":39, "voice":"res039011_charavoice", "delay":0 }] }
]
```

**方案 B — 跨 bundle 多角色（hack）**
```json
"voice": "sound/voice/newsituationintroduction/_",
"actions": [
  { "voices": [{ "character":39, "voice":"../res039011_rip/res039011_charavoice", "delay":0 }] }
]
```

MyGO 五人可用 charavoice：灯(res036011~014)、爱音(res037008/013/015/016)、乐奈(res038009/011/013)、素世(res039011~013)、立希(res040012~013)。

只在关键句加 voice（情绪转折、首尾句、惊喜反应），不要每句都加。

## 构建脚本

`scripts/build_story.py` 提供的全部命令：

```bash
--list-costumes <id>      列出角色全部服装 assetBundleName
--character <id>          输出角色基本信息和季节服装
--list-bg <substring>     在 full catalog 中搜索 bg/* bundle
--ls <path>               列出某个 Asset Explorer 目录的全部文件
--check-bg <bundle> <file>  真实 GET 验证背景图片 Content-Type
--bg-from-explorer <url>  从 Asset Explorer URL 推导 bundle/file
--list-charavoice <id>    探查角色语音资源
--check-voice <bundle> <file>  验证语音文件
--validate <story.json>   校验 storySource（含裸 leaf bundle 静态检查）
```

## 从零到发布的工作流

1. **确认故事**：对话文本、每句说话人、背景、BGM 偏好
2. **解析角色服装**：`--list-costumes <id>` 或直接用季节服装 fallback
3. **选背景/BGM**：查 asset-catalog 速查表，`--check-bg` 验证
4. **编写 actions**：按时间线排列 talk / layout / motion / sound / effect
5. **校验**：`--validate` 确保无语法错误
6. **导入**：打开 https://bestdori.com/community/stories/new → Source Code → Import → 粘贴 JSON
7. **Preview & Publish**

## 常见坑

- **nginx 假 200**：Bestdori 对任意 `/assets/...` 路径都返回 200 + text/html。必须用 GET 验证 Content-Type
- **bundle 必须完整子路径**：`bg/scenario104` ✅ / `scenario104` ❌
- **voice 不支持 custom URL**：整个故事锁定一个 voice bundle，跨 bundle 用 `../` hack
- **costume 不存在会硬崩溃**：不确定时用 `NNN_casual-2023`
- **SE 不推荐使用**：CommonSE 多数 404，剧情节奏靠 BGM + 文字拟声词即可
- **`name: " "` 是旁白**：单空格，不要用空字符串
- **`wait:false` on motion/sound**：让动作和对话重叠播放

## 相关文件

| 文件 | 用途 |
|------|------|
| `SKILL.md` | Skill 完整规范（Agent 加载） |
| `README.md` | 本文件 — 用户使用指南 |
| `references/bestdori-asset-catalog.md` | 实测资源速查（78 BGM + 128 背景 + 表情/服装表） |
| `references/bestdori-story-schema.md` | storySource JSON 完整 Schema |
| `references/sample_story_222138.json` | 真实已发布故事参考 |
| `scripts/build_story.py` | 资源查询与校验工具 |
