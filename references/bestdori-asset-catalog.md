# Bestdori Asset Catalog —— 实测可用资源速查

本文件是 `bestdori-story-creator` 的快速调用手册。所有条目都通过真实 GET 验证返回 `image/png` / `audio/mpeg`（截至 2026-05），可以直接复制到 storySource 中使用。

> **使用流程**：写故事时，先按"场景需求 / 情绪需求"在本文件查 `bundle`、`file`、`bgm`，复制对应的 storySource 片段。本文件未列出的资源，用 `python scripts/build_story.py --list-bg <substr>` / `--ls <path>` / `--check-bg <bundle> <file>` 验证后再用。

---

## 1. 角色 ID 表（band 1-5 + 18 + 21 + 45）

> Bestdori 收录的角色 id 范围是 **1–40**。id 41+ 全是 NPC、店员、mob，**Ave Mujica（豊川祥子、若葉睦、八幡海鈴、祐天寺燈和、三角初華）目前没有可用的 live2d 模型**。

| id | jp | cn | band | 乐队中文名 |
|----|----|----|----|----|
| 1 | 戸山 香澄 | 户山 香澄 | 1 | Poppin'Party |
| 2 | 花園 たえ | 花园 多惠 | 1 | Poppin'Party |
| 3 | 牛込 りみ | 牛込 里美 | 1 | Poppin'Party |
| 4 | 山吹 沙綾 | 山吹 沙绫 | 1 | Poppin'Party |
| 5 | 市ヶ谷 有咲 | 市谷 有咲 | 1 | Poppin'Party |
| 6 | 美竹 蘭 | 美竹 兰 | 2 | Afterglow |
| 7 | 青葉 モカ | 青叶 摩卡 | 2 | Afterglow |
| 8 | 上原 ひまり | 上原 绯玛丽 | 2 | Afterglow |
| 9 | 宇田川 巴 | 宇田川 巴 | 2 | Afterglow |
| 10 | 羽沢 つぐみ | 羽泽 鸫 | 2 | Afterglow |
| 11 | 弦巻 こころ | 弦卷 心 | 3 | Hello, Happy World! |
| 12 | 瀬田 薫 | 濑田 薰 | 3 | Hello, Happy World! |
| 13 | 北沢 はぐみ | 北泽 育美 | 3 | Hello, Happy World! |
| 14 | 松原 花音 | 松原 花音 | 3 | Hello, Happy World! |
| 15 | 奥沢 美咲 / ミッシェル | 奥泽 美咲 / 米歇尔 | 3 | Hello, Happy World! |
| 16 | 丸山 彩 | 丸山 彩 | 4 | Pastel\*Palettes |
| 17 | 氷川 日菜 | 冰川 日菜 | 4 | Pastel\*Palettes |
| 18 | 白鷺 千聖 | 白鹭 千圣 | 4 | Pastel\*Palettes |
| 19 | 大和 麻弥 | 大和 麻弥 | 4 | Pastel\*Palettes |
| 20 | 若宮 イヴ | 若宫 伊芙 | 4 | Pastel\*Palettes |
| 21 | 湊 友希那 | 凑 友希那 | 5 | Roselia |
| 22 | 氷川 紗夜 | 冰川 纱夜 | 5 | Roselia |
| 23 | 今井 リサ | 今井 莉莎 | 5 | Roselia |
| 24 | 宇田川 あこ | 宇田川 亚子 | 5 | Roselia |
| 25 | 白金 燐子 | 白金 燐子 | 5 | Roselia |
| 26 | 倉田 ましろ | 仓田 真白 | 21 | Morfonica |
| 27 | 桐ヶ谷 透子 | 桐谷 透子 | 21 | Morfonica |
| 28 | 広町 七深 | 广町 七深 | 21 | Morfonica |
| 29 | 二葉 つくし | 二叶 筑紫 | 21 | Morfonica |
| 30 | 八潮 瑠唯 | 八潮 瑠唯 | 21 | Morfonica |
| 31 | 和奏 レイ | 和奏 瑞依 | 18 | RAS（Raise A Suilen） |
| 32 | 朝日 六花 | 朝日 六花 | 18 | RAS |
| 33 | 佐藤 ますき | 佐藤 益木 | 18 | RAS |
| 34 | 鳰原 令王那 | 鳰原 令王那 | 18 | RAS |
| 35 | 珠手 ちゆ | 珠手 知由 | 18 | RAS |
| 36 | 高松 燈 | 高松 灯 | 45 | MyGO!!!!! |
| 37 | 千早 愛音 | 千早 爱音 | 45 | MyGO!!!!! |
| 38 | 要 楽奈 | 要 乐奈 | 45 | MyGO!!!!! |
| 39 | 長崎 そよ | 长崎 爽世 | 45 | MyGO!!!!! |
| 40 | 椎名 立希 | 椎名 立希 | 45 | MyGO!!!!! |

可写在 `talk.name` 字段的常用形式：`戸山 香澄` / `美竹 兰` / `凑 友希那` / `长崎 爽世` 等。日文/简中/繁中/英文均可，由作者按情境决定。

---

## 2. 服装（live2dAssetBundleName）

每个角色都有"季节 casual"和"夏/冬季校服"两套必备。`NNN` 是角色 id 三位补零（如 39 → `039`，1 → `001`）。

| 用途 | 模板 | 示例 |
|----|----|----|
| 默认 casual（春） | `NNN_casual-2023` | `039_casual-2023` |
| 夏季校服 | `NNN_school_summer-2023` | `037_school_summer-2023` |
| 冬季校服 | `NNN_school_winter-2023` | `040_school_winter-2023` |
| 默认 Live 演出服 | `NNN_live_default` | `036_live_default`（MyGO 通用版"开始吧，一辈子的约定"） |

**全角色都可用 `NNN_casual-2023`** 作为通用 fallback。冬/夏校服仅对"在校学生身份"的角色有意义（成人或非学生角色可能没有）。

如要某张特殊立绘（活动卡、Live 卡）：
```bash
python scripts/build_story.py --list-costumes <character_id>
```
会列出该角色全部 N 件服装的 `assetBundleName`。

---

## 3. 背景图 bundle（截至 2026-05 实测）

> URL 拼接规则：`/assets/jp/<bundle>_rip/<file>.png`
> storySource 中：`{ "type": "bandori", "bundle": "<bundle>", "file": "<file>" }` （**bundle 必须含完整子路径**，不带 `_rip`，file 不带 `.png`）

### 3.1 推荐场景（已抽样人工核验，氛围标签可信）

| bundle | file | 场景 / 氛围 |
|----|----|----|
| `bg/scenario0` | `bg00001` | 黄昏走廊（学校通用） |
| `bg/scenario0` | `bg00002` | 黄昏空教室（窗光金色，**最经典暧昧氛围**） |
| `bg/scenario0` | `bg00006` | 黄昏路边校园外（散步小道） |
| `bg/scenario1` | `bg00018` | 黄昏小巷面包店附近（**绝佳告白地点**） |
| `bg/scenario2` | `bg00026` | LIVE 舞台（无人，灯光余热） |
| `bg/scenario2` | `bg00020` | LIVE 舞台准备 |
| `bg/scenario10` | `bg00100` | **星空夜带流星**（终幕、烟花、告白圣地） |
| `bg/scenario10` | `bg00109` | 夜色街道 |

### 3.2 完整 scenario 池（128 个 bundle，每个含 7-12 张图）

`bg/scenario0` ~ `bg/scenario125` 全部存在（部分编号缺失：scenario19 只有 7 张；scenario126 只有 2 张；30/36 文件少；其他多在 9-12 张）。每个 bundle 内文件名规律：

| bundle | 文件命名规律 | 第一张文件名 |
|----|----|----|
| `bg/scenarioN`（N < 10） | `bg0000N` 起 | `scenario0` → `bg00001`、`scenario1` → `bg00010` |
| `bg/scenarioNN`（10–99） | `bg00NN0` 起 | `scenario10` → `bg00100`、`scenario99` → `bg00990` |
| `bg/scenarioNNN`（100+） | `bg0NNN0` 起 | `scenario104` → `bg01040`、`scenario120` → `bg01200` |

**直接用 Asset Explorer 浏览**（最方便）：
```
https://bestdori.com/tool/explorer/asset/jp/bg/scenarioNNN
```
然后用脚本抓全：
```bash
python scripts/build_story.py --bg-from-explorer "https://bestdori.com/tool/explorer/asset/jp/bg/scenario104"
```

### 3.3 其他 bg 子路径（已实测可用）

| bundle | 用途 |
|----|----|
| `bg/common/<n>` | 通用 fallback 背景，n=0..7 |
| `bg/afterlive/<skin>` | Live 结束后的舞台/休息室画面，每 skin 含 2 张 |
| `bg/result/<skin>` | Live 结果画面，每 skin 含 2 张 |
| `bg/costume_portrait` | 立绘背景纯色 |

`<skin>` 可选：`skin02 skin03 skin_5th skin_april2019 skin_april2021 skin_april_2024 skin_bike skin_cafe skin_coin skin_collabo23_summer_g skin_collabo23_winter_d skin_collabo24_autumn_i skin_collabo25_autumn_s skin_delta skin_gbp2020 skin_maid skin_miku skin_persona skin_satan skin_stage skin_teamlivefestival skin_witch skincafe`（仅 afterlive；result 多一个 `skin_practice`）

> ⚠️ **不要写 `bundle: "scenario104"` 这样的裸 leaf**，会 404 静默失败。必须 `bg/scenario104`。验证脚本会在 validate 时自动提示。

---

## 4. BGM（实测 78 首可用，按情绪分类）

> URL 规则：`/assets/jp/sound/scenario/bgm/<file_lower>_rip/<file>.mp3`
> storySource 中：`{ "type": "bandori", "file": "<file>" }`（**file 保留原大小写**，比如 `03_Normal` 中的 N 大写不要改）

### 4.1 按情绪分类（推荐用法）

#### 🎭 日常 / 平静
| file | 描述 | 大小 |
|----|----|----|
| `03_Normal` | 标准日常 | 1.3 MB |
| `64_chillout` | 平静抒情，可作为序曲 | 1.7 MB |
| `42_upper_window` | 日常微动机（短，247KB） | 250 KB |
| `cafe` | 咖啡店日常 | 213 KB |

#### 💔 伤感 / 思慕（**本次重点**）
| file | 描述 | 大小 |
|----|----|----|
| `34_piano_weak` | **极弱钢琴**，孤独感 / 留白瞬间最佳 | 440 KB |
| `35_piano_strong` | 强钢琴，告白前张力 | 560 KB |
| `33_piano_full_concert` | 完整钢琴曲，**告白成功 / 顶点宣泄** | 2.8 MB |
| `36_piano_miss_concert` | 钢琴失误式 / 心境破碎 | 1.0 MB |
| `63_longing` | **思慕**，温柔但带距离 | 1.4 MB |
| `73_longing_2` | 思慕加强版，长 | 3 MB |
| `62_sense` | 细腻感性 | 2 MB |
| `seeyou_piano` | **告别钢琴**，分别 / 终幕 | 2.1 MB |
| `crychic_01` | **CRYCHIC 主题**钢琴感伤（MyGO 同人神曲） | 3 MB |
| `crychic_01_vocal` | CRYCHIC 主题（带人声） | 2.9 MB |
| `nakanai_na_kanai` | MyGO「不哭也罢」**情感顶点** | 2.5 MB |
| `mygo_01_scenario` | MyGO 剧情曲 1 | 1.1 MB |
| `mygo_03_guitar_dram` | MyGO 鼓+吉他剧情 | 1.3 MB |
| `mygo_04_scenario` | MyGO 剧情重头曲 | 2.4 MB |

#### 🌧 雨景 / 环境音
| file | 描述 | 大小 |
|----|----|----|
| `65_rain_light` | **雨声 ambient**（短循环） | 130 KB |
| `66_rain_light_umbrella` | 雨打伞 | 156 KB |
| `75_wave_wind` | **风声**，留白 / 夜外景 | 406 KB |
| `76_wave_wind_chirping` | 风+虫鸣 | 454 KB |
| `44_evening` | **黄昏氛围**（带环境感的轻乐） | 1.7 MB |
| `44_crowd_people` | 人群嘈杂 ambient | 130 KB |
| `train` | 列车声 | 138 KB |
| `railroad_crossing` | 道口铃声 | 185 KB |
| `yatai` | 夜市 / 摊位 | 1.5 MB |

#### 🎵 Live 现场
| file | 描述 | 大小 |
|----|----|----|
| `60_exciting_live` | **Live 余热**（演出后氛围） | 1.7 MB |
| `82_girlsrock_live` | 女孩摇滚 Live | 1.6 MB |
| `kirakira_bass` | 闪光贝斯线 | 955 KB |
| `twin_guitar` | 双吉他 | 2.9 MB |
| `freedom` | 释放 / 自由感 | 3 MB |
| `freedom_gt` | 释放（吉他） | 1.4 MB |

#### 🎻 优雅 / 古典
| file | 描述 | 大小 |
|----|----|----|
| `43_elegant` | 优雅 | 1.7 MB |
| `40_ballroom_dancing` | 舞会 | 1.8 MB |
| `69_dark_waltz` | 暗黑华尔兹 | 1.6 MB |
| `70_comical_waltz` | 滑稽华尔兹 | 1.8 MB |
| `etude_in_e_op10_no3` | 离别曲 op.10 No.3（肖邦） | — |
| `la_fille_aux_cheveux_de_lin` | 亚麻色头发的少女（德彪西） | — |

#### 🎶 乐队主题曲（开场 / 收尾标志性）
| 乐队 | files |
|----|----|
| Poppin'Party | `poppin_01` `poppin_02` `poppin_03` |
| Afterglow | `afterglow_01` `afterglow_02` `afterglow_03` |
| Hello, Happy World! | `hellohappy_01` |
| Pastel\*Palettes | `pastel_01` `pastel_02` |
| Roselia | `roselia_01` `roselia_02` `roselia_03` |
| RAS | `ras_01` `ras_02` `ras_03` |
| Morfonica | `morfonica_01` `morfonica_02` |
| MyGO!!!!! | `mygo_01_scenario` `mygo_02_stem` `mygo_03_guitar_dram` `mygo_04_scenario` |

#### 🌫 氛围 / 主题剧情
| file | 描述 | 大小 |
|----|----|----|
| `67_atmospheric` | 氛围乐 | 3 MB |
| `the_historic_scenario` | "意义深远的剧情" | 3 MB |
| `shoot_through_a_dream` | 贯穿梦境 | 2.3 MB |
| `45_serious_3` | 严肃 3 | 1.4 MB |
| `59_unrest_2` | 不安 2 | 1.7 MB |
| `71_serious_4` | 严肃 4 | 1.9 MB |
| `72_serious_5` | 严肃 5 | 2.7 MB |
| `48_revenge` | 复仇向 | 1.6 MB |
| `61_deathmetal` | 死金 | 1.6 MB |
| `68_horror` | 恐怖 | 2.6 MB |
| `37_zombie` | 丧尸感 | 2.2 MB |
| `49_comical` | 滑稽 | 1.6 MB |
| `heartbeat_cresc` | 心跳渐强（短，64KB，留白用） | 64 KB |

#### 🎉 节日 / 主题
| file | 描述 |
|----|----|
| `19_halloween` | 万圣节 |
| `22_christmas` `74_christmas_2` | 圣诞 |
| `24_newyear` | 新年 |
| `38_wadaiko` `39_wadaiko_far` | 和太鼓（祭典） |
| `51_country` | 乡村 |
| `55_satan_audience_room` `56_satan_field` | 撒旦活动专属 |

### 4.2 BGM 切换技巧（来自《夜風と、君のとなり》三章实战）

#### viewer 的 BGM 行为（重要 —— 决定一切编排策略）

逆向 `CommunityStoriesNew/Single.js` 得到：

```js
// 切换 BGM
switchBgm(newId) {
  oldBgm.stop();          // 立即硬停
  this.bgm = newId;
  newBgm.play();          // 立即硬起
}
// 所有 BGM 都用
howler.Howl({ loop: true, html5: true, autoplay: true })
```

由此推出 **三条铁则**：

1. **BGM 切换是"硬切"，没有 crossfade**。直接从一首切到另一首，会听见明显的"咔"。
2. **BGM 默认 loop:true**。一首 1.4 MB 的 BGM 大约 1-1.5 分钟，对话太多它会循环再来一遍——这就是"音乐一直在播感觉很烦"的根因。
3. **`bgm: null` 会立即停掉当前 BGM**。`null` 是没有声音，不是淡出。

#### 改善衔接的 7 条做法（按重要性排序）

1. **🔑 用"哑场过渡"代替直接硬切**：从 BGM A 直接切到 BGM B 之前，先插一条 `{"type":"sound","wait":false,"delay":0,"bgm":null,"se":null}` 让对话走 1-2 行（约 3 秒），再切到 B。耳朵对"安静一秒再起新曲"的接受度远高于硬切。
2. **🔑 用"环境音 / 极弱钢琴"作为过渡桥**：从激烈段（`60_exciting_live` `33_piano_full_concert`）要切到下一首主导曲时，先经过 `34_piano_weak`（440 KB 弱钢琴）、`75_wave_wind`（风声）、`42_upper_window`（247 KB 微动机）、`heartbeat_cresc`（64 KB 心跳）这些"听感很弱"的曲子，听感会平滑很多。
3. **避免相邻两首"情绪相似但旋律不同"硬切**：例如 `63_longing` 直接接 `73_longing_2`、`crychic_01` 直接接 `crychic_01_vocal`，相似度让大脑期待"同一首",听到突变会反感。**务必中间插 null 或弱钢琴**。
4. **同一首 BGM 不要连续覆盖超过 8-12 行 talk**：估算节奏：一行 talk 约 3-5 秒（玩家阅读 + click 等待）。一首 BGM 1.5 分钟即约 18-30 行就会循环一次，**超过 12 行就要主动切换**（哪怕只是切到另一首同类风格的）。
5. **避免每 1-2 行就切**：太频繁切换=人耳无法捕捉旋律。**最低节奏 6 行以上**。
6. **关键转折永远用 `bgm:null` 留白**：表白前的犹豫、第一次牵手、震惊瞬间、心声独白——静音比任何 BGM 都更有张力。
7. **章节结尾用"渐弱型钢琴曲"自然淡出**：`seeyou_piano`、`34_piano_weak`、`crychic_01` 这些曲子的开头都很弱，配合最后一段对话 + `blackOut` 渐黑，听感像自然淡出。

#### "主题动机"复用（让多章节有整体感）

同一首 BGM 在不同章节复用形成情感回环（例如三章故事 `crychic_01` 用了两次，一次 ch2 卸下伪装 + 一次 ch3 拥抱后；`60_exciting_live` 用了两次首尾呼应）——但**复用必须在情绪相同/相承的位置**，否则只会显得偷懒。

#### 推荐的"过渡桥"曲（短/弱，容易对接任何主导曲）

| file | 时长/大小 | 推荐用途 |
|----|----|----|
| `34_piano_weak` | 440 KB / ~28 秒 | **万能过渡桥**，弱钢琴，可接任何后续 |
| `42_upper_window` | 247 KB / ~15 秒 | 极短，转场用 |
| `heartbeat_cresc` | 64 KB / ~4 秒 | 心跳渐强，仅用于关键瞬间（被发现、表白前） |
| `cafe` | 213 KB / ~13 秒 | 咖啡店环境感，适合日常对话起手 |
| `train` | 138 KB / ~9 秒 | 列车环境，转场 |
| `railroad_crossing` | 185 KB / ~12 秒 | 道口铃声，转场 |
| `44_crowd_people` | 130 KB / ~8 秒 | 人群嘈杂，城市夜外景 |
| `75_wave_wind` | 406 KB / ~25 秒 | 风声，**夜外景万用过渡** |

### 4.3 注意：高频 404 的 BGM（不要用）

虽然出现在 `_info.json` 中但 `.mp3` 实际不可平铺访问的：

```
04_nobiri 05_sirious 06_comedy_dotabata 07_comedy 08_sad 09_ending 10_kandou
11_rain 12_odekake 13_shittori 14_shittori_on_hanabi 15_unrest 16_romeo
17_pinch 18_jungle 20_livelobby 20_sports 21_enjoy 23_beforelive 25_rpg_field
26_rpg_dungeon 27_rpg_battle 28_nonbiri_japanese 29_normal_2 30_serious_2
31_search 32_inquire 38_goodnight 41_rain_drizzle 46_goodnight_normal
47_japanese 50_rain_umbrella 57_normal_3 58_sad_2 musicbox musicbox_min
```

如果未来再用，先 `--check-bg`-style 单独 GET 一下确认 `Content-Type: audio/mpeg` 再放进 storySource。

---

## 5. 角色语音 / SE（音效）

### 5.1 viewer 的 voice 机制（重要 —— 决定能怎么用）

```js
// 从 CommunityStoriesNew.js
urlVoice = userStoryVoiceBundle ? `${server}/${userStoryVoiceBundle}_rip/` : null;
getVoiceUrl(t) {
  return "/assets/" + urlVoice + t + ".mp3";
}
```

由此推出 **3 条铁则**：

1. **storySource 顶层 `voice` 字段是单一 voice bundle 路径**（例如 `voice: "sound/voice/newsituationintroduction/res039011"`），所有 `talk.voices[].voice` 都从这个 bundle 取。
2. **`getVoiceUrl` 不支持 `BESTDORI##URL:` 前缀**（不像 BGM），所以 voice 字段**不能用 custom URL**。
3. **整个故事只能用一个 voice bundle** —— 这是 community story 的最大限制。

> ⚠️ 不要尝试给 voice 字段塞 `type:"custom"` 或 `BESTDORI##URL:...`，viewer 不识别，会请求一个错误 URL 静默 404。

### 5.2 可用语音资源池

bestdori 的语音文件都在 `/assets/jp/sound/voice/` 下，组织方式：

| 路径 | 内容 | 文件数 |
|----|----|----|
| `sound/voice/newsituationintroduction/res<NNN><MM>` | **新卡介绍语音**（单角色单句，2-5 秒短句，最适合"语气声"） | 每 bundle 1 个 `<res>_charavoice.mp3` |
| `sound/voice/birthday/character<N>` | 生日祝福语音（id 1-35 有，id 36-40 MyGO 没有） | 每 bundle 1 个 `<YEAR>BDRE-<XX>.mp3`（XX = 角色姓名缩写） |
| `sound/voice/backstage/talkset<N>-<M>` | 后台对话集 | 每 bundle ~3-10 个 `TalkSet<N>-<M>.mp3`，**多人对话** |
| `sound/voice/scenario/actionset/actionset<NNN>` | 剧情区域语音 | 数百到数千个 `area<NNNN>-<MMM>.mp3` |
| `sound/voice/scenario/afterlivetalk/group<N>` | 演出后单人感想 | 每 group ~200 个 `LiveAfter-<NNNN>-<MM>.mp3`（按演出 ID 分） |

### 5.3 MyGO 五人的可用 charavoice（实测）

| 角色 | id | 可用 charavoice bundle |
|----|----|----|
| 高松 灯 | 36 | `res036011` `res036012` `res036013` `res036014` |
| 千早 爱音 | 37 | `res037008` `res037013` `res037015` `res037016` |
| 要 乐奈 | 38 | `res038009` `res038011` `res038013` |
| 长崎 爽世 | 39 | `res039011` `res039012` `res039013` |
| 椎名 立希 | 40 | `res040012` `res040013` |

每个 res 是独立 bundle，bundle 内文件名固定为 `<res>_charavoice.mp3`。例如：
- bundle: `sound/voice/newsituationintroduction/res039011`
- file: `res039011_charavoice`
- 实际 URL: `https://bestdori.com/assets/jp/sound/voice/newsituationintroduction/res039011_rip/res039011_charavoice.mp3`

### 5.4 实用方案

#### 方案 A：单一角色单一语气声（保守，100% 可用）

最适合"一个角色在关键时刻有一句语音感觉"的场景。整个故事只用一个 charavoice：

```jsonc
{
  "server": 0,
  "voice": "sound/voice/newsituationintroduction/res039011",  // 整体voice bundle
  "bgm": null,
  "background": {...},
  "actions": [
    {
      "type": "talk",
      "name": "长崎 爽世",
      "body": "……怎么会这样呢。",
      "wait": true, "close": false, "delay": 0,
      "characters": [39],
      "motions": [],
      "voices": [
        { "character": 39, "voice": "res039011_charavoice", "delay": 0 }
      ]
    }
  ]
}
```

> `voices[].voice` 字段是不带 `.mp3` 的文件名。
> 同一句 `res039011_charavoice` 可以在故事里**重复多次播放**——viewer 会重新触发，不会缓存死。所以"用 1 个 charavoice 做 3-5 次语气声点缀"完全 OK。

#### 方案 B：跨 bundle 调用（hack，浏览器/howler 会做 URL normalize 才有效）

如果想在同一个故事里使用**多个角色的多个 charavoice**，可以用 URL 相对路径 hack：

```jsonc
{
  "voice": "sound/voice/newsituationintroduction/_",  // 占位 bundle 路径
  ...
  "actions": [
    { "type":"talk", "name":"长崎 爽世",
      "voices": [{ "character":39, "voice":"../res039011_rip/res039011_charavoice", "delay":0 }] },
    { "type":"talk", "name":"千早 爱音",
      "voices": [{ "character":37, "voice":"../res037008_rip/res037008_charavoice", "delay":0 }] }
  ]
}
```

原理：viewer 会拼成
```
/assets/jp/sound/voice/newsituationintroduction/__rip/../res039011_rip/res039011_charavoice.mp3
```
浏览器/Howler 加载前会做 URL 标准化（去掉 `_rip/../`），实际请求 `/assets/jp/sound/voice/newsituationintroduction/res039011_rip/res039011_charavoice.mp3` ✓

**curl 和 urllib 实测都得到正确文件**。HTML5 `<audio>` 在主流浏览器中也会先标准化 URL。**但**这是 hack，未被 viewer 官方支持，有失效风险。**建议先用方案 A 验证语音机制能跑，再考虑 B**。

#### 用法建议

- 不要每句对话都加 voice —— 会让人觉得"机器配音"。**只在关键句子加**：
  - 情绪转折点（"……欸？" "……笨蛋。" "我等了好久了！"）
  - 关键反应（怔住、笑声、叹息）
  - 章节开头第一句、结尾最后一句
- 语音和文字不必一一对应——可以让一句对话只播一个"啊？"的短语音作为反应。
- **加 voice 的 talk action 不要紧跟 sound action 切 BGM**，会和语音抢声音通道，听感乱。

### 5.5 SE（音效）—— 不推荐使用

| 类型 | URL 模板 | 状态 |
|----|----|----|
| `se.type:"common"` | `/res/CommonSE/<se>.mp3` | 多数返回 `text/html`，**不可靠** |
| `se.type:"bandori"` | `/assets/<server>/sound/se/<bundle>_rip/<file>.mp3` | bundle 都是游戏内 combo/UI 音效，不适合剧情 |
| `se.type:"custom"` | 任意 URL | 可用，但需要 HTTPS + CORS 友好的外部 mp3 |

**结论：community story 中 SE 不实用，剧情节奏靠 BGM 切换 + 文字拟声词（"——『砰』"）即可。**

---

## 5.5 角色站位与多人同框策略（实战教训 + viewer 逆向）

### 🔑 viewer 实际只有 3 个 X 坐标（重要！）

逆向 `CommunityStoriesSingle.*.js` 得到 `sideToX` 函数：

```js
sideToX: function(side, offsetX) {
  var a = offsetX / 640;     // ← offset 单位是像素，按 640 缩放后并入坐标系
  switch(side) {
    case "leftOver":     return a - 1.2;
    case "rightOver":    return a + 1.2;
    case "left": case "leftUnder":
    case "leftInside": case "leftInsideUnder":   return a - 0.34;
    case "right": case "rightUnder":
    case "rightInside": case "rightInsideUnder": return a + 0.34;
    case "none": case "center": case "centerUnder": return a;
  }
}
```

**关键结论**：
1. **`leftInside` ≡ `left` ≡ `leftUnder` ≡ `leftInsideUnder`，都是 x = -0.34**。Inside/Under 只控制 z-order（前后），**不影响左右距离**！同理右侧四个 = +0.34。
2. **真实 X 坐标只有 3 个**：-0.34 / 0 / +0.34。屏幕有效宽度大约是 [-1, +1]（leftOver/rightOver 边界 ±1.2）。
3. **`sideToOffsetX` 单位是像素，按 640 缩放**。也就是说 `offsetX = 200` 才相当于坐标系里的 `+0.31`（约 1/3 屏宽）。**写 0.15、0.3 这种小数等于无效**（200 倍失真）。

### 不重叠站位速查表（已 viewer 验证）

| 同框人数 | 推荐站位 | offsetX |
|----|----|----|
| 2 | `leftInside` + `rightInside` | 0 / 0 |
| 3 | `left` + `center` + `right` | 0 / 0 / 0 |
| 4 | 不要堆 4 人到 3 个槽，用 offset 拉开：<br>`left`(-100) + `left`(0) + `right`(0) + `right`(+100) | -100 / 0 / 0 / +100 |
| **5** | `left`(-200) + `left`(0) + `center`(0) + `right`(0) + `right`(+200) | **-200 / 0 / 0 / 0 / +200** |
| 6 | 用 leftOver(-50) + left(-50) + left(+150) + right(-150) + right(+50) + rightOver(+50) | 视情况微调 |

> ⚠️ **想推开 1/3 屏宽 ≈ offsetX 200**，想推到屏边 ≈ offsetX 400。**不要写小数偏移**（除非你想做"颤抖一格"这种 1px 微调）。

### 设计原则（按优先级）

1. **🔑 设计上避免 5 人同框**：分章节让 2-3 人出场，群聊用"画外音"（角色 talk + `characters:[]` + body 加"（画外）"前缀）。
2. **章节切换 = 全员 hide 重置**：每个 telop/blackOut 后批量 hide 上一幕角色（`wait:false` 的 hide 不卡流程），下幕重新 appear 仅需要的 2-3 人。
3. **2 人对话**：用 `leftInside` + `rightInside`。
4. **3 人对话**：用 `left` + `center` + `right`。
5. **必须 5 人合影**（结尾镜头）时，**两端用 `±200` 像素 offset**，把人均匀拉到 [-0.65, -0.34, 0, +0.34, +0.65] 五点。
6. **不要用 Under 排做"5 人合影"**：Under 排只换 z-order 不换 X，依然重叠。Under 适合"幕后偷听""远处旁观"这种刻意的场景。

---

## 6. 一键 storySource 片段（复制即用）

### 黄昏空教室开场
```json
{
  "server": 0, "voice": "",
  "bgm": { "type": "bandori", "file": "44_evening" },
  "background": { "type": "bandori", "bundle": "bg/scenario0", "file": "bg00002" },
  "actions": []
}
```

### Live 后舞台
```json
{
  "server": 0, "voice": "",
  "bgm": { "type": "bandori", "file": "60_exciting_live" },
  "background": { "type": "bandori", "bundle": "bg/scenario2", "file": "bg00026" },
  "actions": []
}
```

### 告白用星空夜
```json
{
  "server": 0, "voice": "",
  "bgm": { "type": "bandori", "file": "33_piano_full_concert" },
  "background": { "type": "bandori", "bundle": "bg/scenario10", "file": "bg00100" },
  "actions": []
}
```

### BGM 切换 action（任意位置插入）
```json
{ "type": "sound", "wait": false, "delay": 0,
  "bgm": { "type": "bandori", "file": "crychic_01" },
  "se": null }
```

### 静音留白
```json
{ "type": "sound", "wait": false, "delay": 0, "bgm": null, "se": null }
```

### 切换背景
```json
{ "type": "effect", "effectType": "changeBackground",
  "background": { "type": "bandori", "bundle": "bg/scenario1", "file": "bg00018" },
  "wait": true, "delay": 0 }
```
