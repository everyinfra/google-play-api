# Google Play API

[English](#english) · [中文](#中文)

## English

This repo reads public Google Play data with Python or curl. You can search apps by keyword and read an app's details and user reviews. You need one EveryInfra API key. You do not need a Google account or cookie. The same API also works as an MCP tool in Claude and Cursor. Billing is per call: these 3 capabilities cost $1.39 per 1,000 calls (about $0.0014 per call). Failed calls and empty results are not charged. The EveryInfra Google Play API has 9 capabilities, all listed on the platform page: <https://everyinfra.com/en/google-play-api?utm_source=github&utm_medium=example_repo&utm_campaign=google-play-api>

### Quick start

```bash
git clone https://github.com/everyinfra/google-play-api.git
cd google-play-api
pip install -r requirements.txt
export EVERYINFRA_API_KEY=<your API key>
python main.py search "note taking" --out apps.csv
python main.py app <package name> --out app.json
python main.py reviews <package name> --out reviews.csv
```

- For `app` and `reviews`, pass the package name: the `app_id` from a `search` result, for example com.evernote, which is the part after ?id= in a Play Store link. Do not pass the full link.
- `--country` on `search` picks the store country, default us.
- Without `--out`, the command prints the first 3 rows as JSON. With `--out`, it saves a .csv or .json file. The CSV has a BOM, so Excel opens it without garbled text.
- `--pages N` follows `next_page_token` for N pages. Each page counts as one call.
- Register at everyinfra.com, then create the API key in the console. Steps: <https://everyinfra.com/en/docs?utm_source=github&utm_medium=example_repo&utm_campaign=google-play-api#quickstart>

### curl

```bash
curl -X POST https://api.everyinfra.com/api/v1/social \
  -H "Authorization: Bearer $EVERYINFRA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"platform":"google_play","action":"search","params":{"keyword":"note taking"}}'
```

All capabilities use the same URL. Change `action` and `params` to call another one. Examples for `profile` and `reviews` are in [examples/curl.sh](examples/curl.sh).

### Claude and Cursor (MCP)

The remote MCP URL is <https://api.everyinfra.com/mcp>. Add the `Authorization: Bearer` header with your API key. EveryInfra runs the server, so you install no local program.

Claude Code:

```bash
claude mcp add --transport http everyinfra https://api.everyinfra.com/mcp --header "Authorization: Bearer <API Key>"
```

Cursor and other clients that read `mcp.json` ([examples/mcp.json](examples/mcp.json)):

```json
{
  "mcpServers": {
    "everyinfra": {
      "url": "https://api.everyinfra.com/mcp",
      "headers": {
        "Authorization": "Bearer <API Key>"
      }
    }
  }
}
```

Custom connectors in Claude on the web and desktop, and ChatGPT, accept only a URL. Enter <https://api.everyinfra.com/mcp/all>, sign in to EveryInfra when asked, and allow access. You do not need to enter a key. Full steps: <https://everyinfra.com/en/mcp-server?utm_source=github&utm_medium=example_repo&utm_campaign=google-play-api>

### Price

| `action` | Per 1,000 calls |
|---|---|
| `search` | $1.39 |
| `profile` | $1.39 |
| `reviews` | $1.39 |

- Billing is per call, about $0.0014 each. Failed calls, empty results, parameter errors, and authentication failures are not charged.
- Each page fetched with `--pages` counts as one call.
- A new account gets a $1 trial allowance, valid for 24 hours. No credit card is needed. How to claim it: <https://everyinfra.com/en/pricing?utm_source=github&utm_medium=example_repo&utm_campaign=google-play-api>
- Prices for the other 6 Google Play capabilities are on the platform page: <https://everyinfra.com/en/google-play-api?utm_source=github&utm_medium=example_repo&utm_campaign=google-play-api>

### Fields

These are the fields that the 3 capabilities returned in our test. Each meaning is the first sentence of the field's entry in the API documentation. The link under each table has the full text.

#### `search` (keyword search)

| Field | Meaning |
|---|---|
| `app_id` | App package name (such as com.example.app); the unique identifier on Google Play. |
| `url` | Link to the record on the platform. |
| `name` | Name of the object itself, for account, product and business capabilities. |
| `summary` | One-line summary of the app. |
| `description` | Summary or description, usually shorter than text. |
| `developer` | Developer name. |
| `developer_email` | Developer contact email (public information on the store page). |
| `developer_website` | Developer website. |
| `score` | App rating, on a 5-point scale. |
| `rating_count` | Number of people who rated. null means not disclosed, not 0. |
| `review_count` | Number of reviews, for product and business capabilities. null means not disclosed, not 0. |
| `installs` | Displayed install count (such as 1,000,000+). |
| `min_installs` | Lower bound of the install range, as a number. |
| `price` | Price as a number without a currency symbol; see currency. |
| `is_free` | Whether the app is free to download (keywords_for_app). |
| `currency` | Currency code of the price (for example CNY, USD). |
| `category` | Category name in the platform's own taxonomy, not normalized across platforms. |
| `content_rating` | Content rating. |
| `contains_ads` | Whether the app contains ads. |
| `offers_iap` | Whether the app has in-app purchases. |
| `version` | Version number. |
| `released` | First release date. |
| `updated_at` | Last update time. |
| `android_version` | Minimum Android version required. |
| `icon_url` | App icon. |
| `header_image_url` | Header image of the store page. |
| `privacy_policy` | Privacy policy link. |
| `platform` | Source platform identifier, the same as platform in the request (for example xiaohongshu, tiktok). |
| `screenshots` | Array of image links to the store listing's screenshots; absent when there are none. |
| `rating_histogram` | Number of ratings per star level: an object whose keys are "1" to "5" (the star level) and whose values are how many ratings gave that level; absent when not available. |

All parameters and fields: <https://everyinfra.com/en/google-play-api/search?utm_source=github&utm_medium=example_repo&utm_campaign=google-play-api>

#### `profile` (profile or object details)

| Field | Meaning |
|---|---|
| `app_id` | App package name (such as com.example.app); the unique identifier on Google Play. |
| `url` | Link to the record on the platform. |
| `name` | Name of the object itself, for account, product and business capabilities. |
| `summary` | One-line summary of the app. |
| `description` | Summary or description, usually shorter than text. |
| `developer` | Developer name. |
| `developer_email` | Developer contact email (public information on the store page). |
| `score` | App rating, on a 5-point scale. |
| `rating_count` | Number of people who rated. null means not disclosed, not 0. |
| `review_count` | Number of reviews, for product and business capabilities. null means not disclosed, not 0. |
| `installs` | Displayed install count (such as 1,000,000+). |
| `min_installs` | Lower bound of the install range, as a number. |
| `price` | Price as a number without a currency symbol; see currency. |
| `is_free` | Whether the app is free to download (keywords_for_app). |
| `currency` | Currency code of the price (for example CNY, USD). |
| `category` | Category name in the platform's own taxonomy, not normalized across platforms. |
| `content_rating` | Content rating. |
| `contains_ads` | Whether the app contains ads. |
| `offers_iap` | Whether the app has in-app purchases. |
| `version` | Version number. |
| `released` | First release date. |
| `updated_at` | Last update time. |
| `android_version` | Minimum Android version required. |
| `icon_url` | App icon. |
| `header_image_url` | Header image of the store page. |
| `privacy_policy` | Privacy policy link. |
| `platform` | Source platform identifier, the same as platform in the request (for example xiaohongshu, tiktok). |
| `screenshots` | Array of image links to the store listing's screenshots; absent when there are none. |
| `rating_histogram` | Number of ratings per star level: an object whose keys are "1" to "5" (the star level) and whose values are how many ratings gave that level; absent when not available. |

All parameters and fields: <https://everyinfra.com/en/google-play-api/profile?utm_source=github&utm_medium=example_repo&utm_campaign=google-play-api>

#### `reviews` (reviews)

| Field | Meaning |
|---|---|
| `id` | The record's unique ID on the platform. |
| `app_id` | App package name (such as com.example.app); the unique identifier on Google Play. |
| `text` | Body text with HTML removed, returned in full and never cut short (on a few platforms the list results themselves carry only an excerpt; the platform's field notes say so). |
| `score` | App rating, on a 5-point scale. |
| `author_name` | Author's display name. |
| `author_avatar_url` | Reviewer avatar. |
| `thumbs_up` | Number of thumbs up on this review. |
| `url` | Link to the record on the platform. |
| `posted_at` | Publish time in ISO 8601, UTC (for example 2026-08-07T12:34:56+00:00). |
| `platform` | Source platform identifier, the same as platform in the request (for example xiaohongshu, tiktok). |
| `app_version` | Current version number. |

All parameters and fields: <https://everyinfra.com/en/google-play-api/reviews?utm_source=github&utm_medium=example_repo&utm_campaign=google-play-api>

### FAQ

**Do I need a Google account or cookie to call the API?**

No. Send the `Authorization: Bearer` header with your API key. The request body holds `platform`, `action`, and the capability parameters. You do not scan a QR code, keep a login session, or open a browser.

**How much does it cost? Are failed calls charged? Is there a free allowance?**

Billing is per call, from $0.56 per 1,000 calls. Failed calls, empty results, parameter errors, and authentication failures are not charged. A new account gets a $1 trial allowance, valid for 24 hours. No credit card is needed. How to claim it: <https://everyinfra.com/en/pricing?utm_source=github&utm_medium=example_repo&utm_campaign=google-play-api>

**Can I connect the Google Play API to Claude or Cursor?**

Yes. The remote MCP URL is <https://api.everyinfra.com/mcp>. Add the `Authorization: Bearer` header with your API key. You install no local program. Setup for Claude, Cursor, ChatGPT, and Claude Code: <https://everyinfra.com/en/mcp-server?utm_source=github&utm_medium=example_repo&utm_campaign=google-play-api>.

**What legal points apply when I use Google Play data?**

The EveryInfra Terms of Service require you to make sure your use of the data follows applicable law and the terms of the relevant platform. Do not use the data for anything illegal or anything that violates privacy or intellectual property rights. Do not use bulk scraping for harassment, fraud, or other abuse. When you use personal information such as nicknames and avatars, keep only the fields your business needs.

**Which Google Play data can I get?**

The EveryInfra Google Play API has 9 capabilities:

- keyword search
- profile or object details
- reviews
- app keyword rankings
- bulk metrics
- competitors
- books
- games
- keyword intersection

Parameters and return fields for each capability are on the platform page: <https://everyinfra.com/en/google-play-api?utm_source=github&utm_medium=example_repo&utm_campaign=google-play-api>

### Tested

Before release, we ran the 3 commands in Quick start against the live API with this repo's code.

| Command | Time (Singapore, UTC+8) | Rows | Charged |
|---|---|---|---|
| `python main.py search "note taking" --out apps.csv` | 2026-11-25 13:18 | 20 | $0.001389 |
| `python main.py app <package name> --out app.json` | 2026-11-25 13:18 | 1 | $0.001389 |
| `python main.py reviews <package name> --out reviews.csv` | 2026-11-25 13:18 | 40 | $0.001389 |

## 中文

本仓库用 Python 或 curl 读 Google Play 公开数据：按关键词搜应用，读应用详情和用户评价。只需一把 EveryInfra API Key，不用 Google 账号和 Cookie，也能作为 MCP 工具接进 Claude、Cursor。按调用次数计费，这 3 个能力每千次 $1.39（每次约 $0.0014），失败和空结果不收费。Google Play 共 9 个能力：<https://everyinfra.com/google-play-api?utm_source=github&utm_medium=example_repo&utm_campaign=google-play-api>

### 快速开始

```bash
git clone https://github.com/everyinfra/google-play-api.git
cd google-play-api
pip install -r requirements.txt
export EVERYINFRA_API_KEY=<你的 API Key>
python main.py search "note taking" --out apps.csv
python main.py app <应用包名> --out app.json
python main.py reviews <应用包名> --out reviews.csv
```

- `app` 和 `reviews` 传应用包名，用 `search` 结果里的 `app_id`，形如 com.evernote，即 Play 商店链接 ?id= 后面那段；不要传完整链接。
- `search` 的 `--country` 选店面国家，默认 us。
- 不加 `--out` 时打印前 3 条 JSON；加 `--out` 存成 .csv 或 .json。CSV 带 BOM，Excel 直接打开不乱码。
- `--pages N` 按 `next_page_token` 翻页，每翻一页算一次调用。
- API Key 在 everyinfra.com 注册后到控制台创建，步骤见 <https://everyinfra.com/docs?utm_source=github&utm_medium=example_repo&utm_campaign=google-play-api#quickstart>

### 用 curl 调

```bash
curl -X POST https://api.everyinfra.com/api/v1/social \
  -H "Authorization: Bearer $EVERYINFRA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"platform":"google_play","action":"search","params":{"keyword":"note taking"}}'
```

所有能力都发到同一个地址，换 `action` 和 `params` 就行；`profile`、`reviews` 的写法见 [examples/curl.sh](examples/curl.sh)。

### 接进 Claude、Cursor（MCP）

远程 MCP 地址是 <https://api.everyinfra.com/mcp>，请求头加 `Authorization: Bearer` 和 API Key；服务器由 EveryInfra 运行，不用装本地程序。

Claude Code：

```bash
claude mcp add --transport http everyinfra https://api.everyinfra.com/mcp --header "Authorization: Bearer <API Key>"
```

Cursor 等读 `mcp.json` 的客户端（[examples/mcp.json](examples/mcp.json)）：

```json
{
  "mcpServers": {
    "everyinfra": {
      "url": "https://api.everyinfra.com/mcp",
      "headers": {
        "Authorization": "Bearer <API Key>"
      }
    }
  }
}
```

Claude 网页版和桌面版的自定义连接器、ChatGPT 只能填网址：填 <https://api.everyinfra.com/mcp/all>，连接时登录 EveryInfra 并允许，不用填 Key。完整步骤见 <https://everyinfra.com/mcp-server?utm_source=github&utm_medium=example_repo&utm_campaign=google-play-api>

### 价格

| 能力 | `action` | 每千次 |
|---|---|---|
| 关键词搜索 | `search` | $1.39 |
| 主页或对象详情 | `profile` | $1.39 |
| 评价 | `reviews` | $1.39 |

- 按调用次数计费，每次约 $0.0014；失败、空结果、参数错误和鉴权失败都不收费。
- `--pages` 翻的每一页算一次调用。
- 新账号有 $1 试用额度，24 小时内有效，不用信用卡，领取方式见 <https://everyinfra.com/pricing?utm_source=github&utm_medium=example_repo&utm_campaign=google-play-api>
- Google Play 其他 6 个能力的单价见平台页 <https://everyinfra.com/google-play-api?utm_source=github&utm_medium=example_repo&utm_campaign=google-play-api>

### 返回字段

下面是这 3 个能力实测返回的字段，含义取自接口文档每条说明的第一句，完整说明在每张表下面的链接里。

#### `search`（关键词搜索）

| 字段 | 含义 |
|---|---|
| `app_id` | 应用包名（如 com.example.app），Google Play 的唯一标识。 |
| `url` | 该记录在原平台上的可访问链接。 |
| `name` | 名称。 |
| `summary` | 应用一句话简介。 |
| `description` | 简介或描述，通常比 text 短。 |
| `developer` | 开发者名称。 |
| `developer_email` | 开发者联系邮箱（商店页公开信息）。 |
| `developer_website` | 开发者网站。 |
| `score` | 应用评分，5 分制。 |
| `rating_count` | 参与评分的人数。 |
| `review_count` | 评价条数，用于商品/商家类能力。 |
| `installs` | 安装量展示值（如 1,000,000+），是区间下限不是精确值。 |
| `min_installs` | 安装量区间下限的数值形式。 |
| `price` | 价格数值，不含货币符号；币种见 currency。 |
| `is_free` | 是否免费下载。 |
| `currency` | 价格币种代码（如 CNY、USD）。 |
| `category` | 分类名称，取值为原平台的分类体系，未做跨平台归一。 |
| `content_rating` | 内容分级。 |
| `contains_ads` | 是否含广告。 |
| `offers_iap` | 是否含内购。 |
| `version` | 版本号。 |
| `released` | 首次发布日期。 |
| `updated_at` | 最近更新时间。 |
| `android_version` | 要求的最低 Android 版本。 |
| `icon_url` | 应用图标。 |
| `header_image_url` | 商店页头图。 |
| `privacy_policy` | 隐私政策链接。 |
| `platform` | 数据来源平台标识，与请求里的 platform 一致（如 xiaohongshu、tiktok）。 |
| `screenshots` | 商店页截图的图片链接数组；没有时不出现这个字段。 |
| `rating_histogram` | 各星级的评分人数：对象，键是 "1" 到 "5"（星级），值是给这个星级的人数；没有时不出现这个字段。 |

完整参数和字段：<https://everyinfra.com/google-play-api/search?utm_source=github&utm_medium=example_repo&utm_campaign=google-play-api>

#### `profile`（主页或对象详情）

| 字段 | 含义 |
|---|---|
| `app_id` | 应用包名（如 com.example.app），Google Play 的唯一标识。 |
| `url` | 该记录在原平台上的可访问链接。 |
| `name` | 名称。 |
| `summary` | 应用一句话简介。 |
| `description` | 简介或描述，通常比 text 短。 |
| `developer` | 开发者名称。 |
| `developer_email` | 开发者联系邮箱（商店页公开信息）。 |
| `score` | 应用评分，5 分制。 |
| `rating_count` | 参与评分的人数。 |
| `review_count` | 评价条数，用于商品/商家类能力。 |
| `installs` | 安装量展示值（如 1,000,000+），是区间下限不是精确值。 |
| `min_installs` | 安装量区间下限的数值形式。 |
| `price` | 价格数值，不含货币符号；币种见 currency。 |
| `is_free` | 是否免费下载。 |
| `currency` | 价格币种代码（如 CNY、USD）。 |
| `category` | 分类名称，取值为原平台的分类体系，未做跨平台归一。 |
| `content_rating` | 内容分级。 |
| `contains_ads` | 是否含广告。 |
| `offers_iap` | 是否含内购。 |
| `version` | 版本号。 |
| `released` | 首次发布日期。 |
| `updated_at` | 最近更新时间。 |
| `android_version` | 要求的最低 Android 版本。 |
| `icon_url` | 应用图标。 |
| `header_image_url` | 商店页头图。 |
| `privacy_policy` | 隐私政策链接。 |
| `platform` | 数据来源平台标识，与请求里的 platform 一致（如 xiaohongshu、tiktok）。 |
| `screenshots` | 商店页截图的图片链接数组；没有时不出现这个字段。 |
| `rating_histogram` | 各星级的评分人数：对象，键是 "1" 到 "5"（星级），值是给这个星级的人数；没有时不出现这个字段。 |

完整参数和字段：<https://everyinfra.com/google-play-api/profile?utm_source=github&utm_medium=example_repo&utm_campaign=google-play-api>

#### `reviews`（评价）

| 字段 | 含义 |
|---|---|
| `id` | 该记录在原平台上的唯一标识。 |
| `app_id` | 应用包名（如 com.example.app），Google Play 的唯一标识。 |
| `text` | 正文内容，已去除 HTML 标签，全文返回、不截断（个别平台的列表结果本身只有摘要，以该平台的字段说明为准）。 |
| `score` | 应用评分，5 分制。 |
| `author_name` | 作者昵称（显示名）。 |
| `author_avatar_url` | 评价人头像。 |
| `thumbs_up` | 该评价的点赞数。 |
| `url` | 该记录在原平台上的可访问链接。 |
| `posted_at` | 发布时间，ISO 8601 格式、UTC 时区（如 2026-08-07T12:34:56+00:00）。 |
| `platform` | 数据来源平台标识，与请求里的 platform 一致（如 xiaohongshu、tiktok）。 |
| `app_version` | 当前版本号。 |

完整参数和字段：<https://everyinfra.com/google-play-api/reviews?utm_source=github&utm_medium=example_repo&utm_campaign=google-play-api>

### 常见问题

**调用时要不要提供 Google 账号或 Cookie？**

不用，请求头带 `Authorization: Bearer` 和 API Key 就能调，请求体写 `platform`、`action` 和能力参数。不用扫码、维护登录状态，也不用开浏览器。

**怎么收费？失败了收不收钱？有免费额度吗？**

按调用次数计费，每千次 $0.56 起。失败、空结果、参数错误和鉴权失败都不收费。新账号有 $1 试用额度，24 小时内有效，不用信用卡，领取方式见定价页 <https://everyinfra.com/pricing?utm_source=github&utm_medium=example_repo&utm_campaign=google-play-api>

**能把 Google Play 接口接进 Claude、Cursor 吗？**

能，远程 MCP 地址是 <https://api.everyinfra.com/mcp>，请求头加 `Authorization: Bearer` 和 API Key，不用装本地程序。Claude、Cursor、ChatGPT、Claude Code 配置见 <https://everyinfra.com/mcp-server?utm_source=github&utm_medium=example_repo&utm_campaign=google-play-api>。

**用 Google Play 数据要注意哪些合规问题？**

EveryInfra 服务条款要求你自行确保数据用法符合适用法律和相关平台条款，禁止用于违法、侵犯隐私或知识产权，或批量抓取用于骚扰、欺诈等恶意用途。用到昵称、头像等个人信息时，只留业务用得上的字段。

**可以拿到 Google Play 的哪些数据？**

Google Play 有 9 个能力：关键词搜索、主页或对象详情、评价、App 关键词排名、批量 App 排名指标、竞品应用、图书搜索、游戏榜单与浏览、多个 App 共同关键词。每个能力的参数和返回字段见平台页 <https://everyinfra.com/google-play-api?utm_source=github&utm_medium=example_repo&utm_campaign=google-play-api>

### 实测记录

发布前用本仓的代码对线上接口跑过一遍，命令就是「快速开始」里的 3 条。

| 命令 | 时间（新加坡时间） | 返回条数 | 扣费 |
|---|---|---|---|
| `python main.py search "note taking" --out apps.csv` | 2026-11-25 13:18 | 20 | $0.001389 |
| `python main.py app <应用包名> --out app.json` | 2026-11-25 13:18 | 1 | $0.001389 |
| `python main.py reviews <应用包名> --out reviews.csv` | 2026-11-25 13:18 | 40 | $0.001389 |

`profile` 返回的一条（正文截到 60 字，作者字段没放进来）：

```json
{
  "summary": "Samsung Notes can create and edit documents and collaborate …",
  "description": "Samsung Notes can create and edit documents on mobile, table…",
  "score": 4.7744584,
  "rating_count": 15637801,
  "review_count": 107547,
  "price": 0,
  "currency": "USD",
  "category": "Productivity",
  "updated_at": "2025-09-23T06:45:47.000Z"
}
```

## License

MIT
