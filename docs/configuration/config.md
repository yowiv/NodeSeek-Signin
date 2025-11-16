# 环境变量手册

> 📌 **提示**
> - `docs/configuration/solutions.md` 说明了验证码供应商的差异；本文档侧重列举所有变量的含义与默认值。
> - 仓库根目录的 `.env.example` 提供了一份可直接复制的模板，建议从该文件开始修改。

## 1. 核心账号 / Cookie 变量

| 变量 | 是否必填 | 默认值 | 作用 | 备注 |
| --- | --- | --- | --- | --- |
| `NS_COOKIE` | 建议 | - | 直接使用已有 Cookie 执行签到，支持 `&` 或换行分隔多个账户 | Docker 环境下若设置 `IN_DOCKER=true`，脚本会将最新 Cookie 写入 `cookie/NS_COOKIE.txt` 并从该文件读取 |
| `USER` / `PASS` | 可选 | - | 未编号账号的用户名/密码 | 若 `NS_COOKIE` 失效将尝试登录获取新 Cookie |
| `USER1` / `PASS1` 以及 `USER2` / `PASS2` … | 可选 | - | 按序号声明多个账号密码 | 序号从 1 递增；一旦设置将与 `NS_COOKIE` 列表按索引对应 |

> ✅ **最小可用集**：至少提供 `NS_COOKIE`，或为每个账号准备对应的 `USERn`/`PASSn` 与验证码服务配置。

## 2. 验证码解决方案

| 变量 | 是否必填 | 默认值 | 适用场景 |
| --- | --- | --- | --- |
| `SOLVER_TYPE` | 可选 | `turnstile` | `turnstile` 表示自建 CloudFreed / Cloudflyer 等接口；`yescaptcha` 表示托管服务 |
| `API_BASE_URL` | 条件必填 | 空字符串 | 指向自建服务或 YesCaptcha 的 API 地址，如 `http://127.0.0.1:3000` 或 `https://api.yescaptcha.com` |
| `CLIENTT_KEY` | 必填 | - | 验证码服务密钥，CloudFreed 与 YesCaptcha 都使用该名称（注意拼写为 `CLIENTT`） |

> ℹ️ 更多供应商注意事项见 `docs/configuration/solutions.md`。

## 3. 运行与调度行为

| 变量 | 默认值 | 说明 |
| --- | --- | --- |
| `NS_RANDOM` | `true` | 传递给签到接口的 `random` 参数，用于保持请求随机性；可改为 `false` 进行调试 |
| `RUN_AT` | `08:00-10:59` | `scheduler.py` 读取的定时配置。支持固定时间（`HH:MM`）或时间范围（`HH:MM-HH:MM`，将在区间内随机挑选） |
| `IN_DOCKER` | 未设置 | 设为 `true` 时视为容器环境，Cookie 会写入/读取 `cookie/NS_COOKIE.txt`；用于 Docker Compose 场景 |

## 4. GitHub / CI 集成

| 变量 | 是否必填 | 说明 |
| --- | --- | --- |
| `GH_PAT` | 可选（推荐） | GitHub Personal Access Token。缺少它时无法把最新 `NS_COOKIE` 写回仓库变量 |
| `GITHUB_ACTIONS` | 由平台注入 | GitHub Actions 运行器自动提供，脚本据此判断当前是否在 Actions 内运行 |
| `GITHUB_REPOSITORY` | 由平台注入 | 与 `GH_PAT` 搭配，指明需要写入变量的仓库 |

> 🔁 当 `GH_PAT`、`GITHUB_REPOSITORY` 可用时，`nodeseek_sign.py` 会调用 GitHub API 自动更新仓库变量 `NS_COOKIE`，减少人工维护。

## 5. 通知推送变量

`notify.py` 支持 20+ 种渠道，下表列出最常用的几类变量。若需启用其他渠道，请查阅 `notify.py` 顶部的 `push_config` 列表。

### 5.1 Telegram

| 变量 | 说明 |
| --- | --- |
| `TG_BOT_TOKEN` | Bot 的 Token，形如 `123456789:ABC...` |
| `TG_USER_ID` | 接收消息的用户或群组 ID |
| `TG_THREAD_ID` | （可选）超级群话题 ID，用于把通知发送到特定话题 |
| `TG_PROXY_HOST` / `TG_PROXY_PORT` / `TG_PROXY_AUTH` / `TG_API_HOST` | （可选）为 Telegram 设置代理或反代 |

### 5.2 Bark / PushPlus / 邮件 等

- **Bark**：`BARK_PUSH`（必须）、`BARK_ARCHIVE`、`BARK_GROUP`、`BARK_SOUND`、`BARK_ICON`、`BARK_LEVEL`, `BARK_URL` 等控制推送外观。
- **PushPlus**：`PUSH_PLUS_TOKEN`（必须）、`PUSH_PLUS_USER`。
- **Server酱 / PushDeer / Go-cqhttp / 飞书 / DingTalk / Gotify / Synology Chat / iGot / 自定义 Webhook**：分别使用 `PUSH_KEY`、`DEER_KEY`、`GOBOT_*`、`FSKEY`、`DD_BOT_SECRET` + `DD_BOT_TOKEN`、`GOTIFY_*`、`CHAT_*`、`IGOT_PUSH_KEY`、`WEBHOOK_*` 等变量。
- **邮件**：`SMTP_SERVER`、`SMTP_SSL`、`SMTP_EMAIL`、`SMTP_PASSWORD`、`SMTP_NAME`。
- **其他**：`QYWX_KEY`、`QYWX_AM`、`WE_PLUS_BOT_*`、`QMSG_*`、`AIBOTK_*`、`PUSHME_*`、`CHRONOCAT_*`……均与 `push_config` 字段同名。

### 5.3 通知开关

| 变量 | 默认值 | 说明 |
| --- | --- | --- |
| `CONSOLE` | `false` | 设置为 `true` 时只输出到控制台，不走第三方渠道 |
| `HITOKOTO` | `True` | 是否在通知末尾追加一句「一言」名句 |
| `SKIP_PUSH_TITLE` | 未设置 | 多个标题用回车分隔，匹配到的标题会跳过推送 |

## 6. 部署场景推荐组合

| 场景 | 最少需要配置 | 建议额外配置 |
| --- | --- | --- |
| **GitHub Actions** | `NS_COOKIE` 或 `USERn/PASSn` + 验证码变量 | `GH_PAT`（自动回写 Cookie）、`TG_*`（通知） |
| **Docker Compose / 本地定时** | `.env` 中的 `NS_COOKIE` 或账号、`SOLVER_TYPE`、`CLIENTT_KEY`，并可使用 `RUN_AT` 控制时间 | `IN_DOCKER=true`（启用文件存储 Cookie）、任意通知变量 |
| **青龙面板** | 直接在面板变量中写入 `NS_COOKIE` 或 `USERn/PASSn`、验证码变量 | 配置任意通知变量，支持与青龙自带通知并存 |

## 7. 调试与排障建议

1. 利用 `.env.example` 复制生成 `.env`，逐项填值，便于与仓库更新保持同步。
2. 本地调试可运行 `python test_run.py` 验证配置是否生效；Docker/青龙请先确认 `RUN_AT` 是否在可接受的时段内。
3. 如果启用了账号密码但依然无法自动登录，请确认 `SOLVER_TYPE`、`API_BASE_URL`、`CLIENTT_KEY` 是否匹配对应的验证码服务。
4. 若通知未触发，可在同一个 shell 中临时导出变量后执行 `python notify.py` 做自检。

通过本文档即可对照自己的部署场景，快速核验环境变量是否齐全，减少因配置遗漏导致的签到失败。
