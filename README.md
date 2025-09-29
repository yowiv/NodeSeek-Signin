# NodeSeek-Signin

<div align="center">
  
![NodeSeek](https://img.shields.io/badge/NodeSeek-自动签到-green)
![GitHub stars](https://img.shields.io/github/stars/yowiv/NodeSeek-Signin?style=flat)
![Python](https://img.shields.io/badge/Language-Python-blue)
![License](https://img.shields.io/github/license/yowiv/NodeSeek-Signin)

</div>

[Deepflood论坛签到](https://github.com/yowiv/deepflood-Signin)


## 📝 项目介绍

这是一个用于 NodeSeek 论坛自动签到的工具，支持通过 GitHub Actions、青龙面板或 Docker Compose 进行定时自动签到操作。签到模式默认为随机签到，帮助用户轻松获取论坛每日"鸡腿"奖励。


## ✨ 功能特点

- 📅 支持 GitHub Actions 自动运行
- 🦉 支持青龙面板定时任务
- 🐳 支持 Docker Compose 一键部署
- 🍪 支持 Cookie 或账号密码登录方式
- 👥 支持多账号批量签到
- 🔐 支持多种验证码解决方案
  - 自建 CloudFreed 服务（免费）
  - YesCaptcha 商业服务（付费/赠送）
- 📱 支持多种通知推送渠道(需在blank.yml添加对应变量)
- 🔄 自动更新Cookie并保存至GitHub变量

## 🚀 使用方法

### 方式一：GitHub Actions

1. Fork 本仓库到自己的 GitHub 账号下
2. 在仓库的 `Settings > Secrets and variables > Actions` 中添加以下必要配置：

| 变量名称 | 必要性 | 说明 |
| :------: | :----: | :--- |
| `NS_COOKIE` | **建议** | NodeSeek 论坛的用户 Cookie，可在浏览器开发者工具(F12)的网络请求中获取，多账号用`&`或换行符分隔 |
| `USER`/`USER1` | 可选 | NodeSeek 论坛用户名，当 Cookie 失效时使用 |
| `PASS`/`PASS1` | 可选 | NodeSeek 论坛密码 |
| `TG_BOT_TOKEN` | 可选 | Telegram 机器人的 Token，用于通知签到结果 |
| `TG_USER_ID` | 可选 | Telegram 用户 ID，用于接收通知 |
| `TG_THREAD_ID` | 可选 | Telegram 超级群组话题 ID，用于在特定话题中发送通知 |
| `GH_PAT` | 可选 | GitHub Personal Access Token，用于自动更新Cookie变量 |

> **注意**：若仅设置 Cookie 但未配置验证码服务，当 Cookie 过期后无法自动登录获取新 Cookie。

### 方式二：青龙面板

在青龙面板中执行以下命令克隆本仓库：

```bash
ql repo https://github.com/yowiv/NodeSeek-Signin.git
```

然后在环境变量中添加所需配置。

### 方式三：Docker Compose

这种部署方式可以实现本地自动化定时签到，并支持自动处理验证码。

**第一步：克隆项目**

首先，将整个项目克隆到你的服务器上：

```bash
git clone https://github.com/yowiv/NodeSeek-Signin.git
cd NodeSeek-Signin
```

**第二步：配置环境变量**

将 `.env.example` 文件复制或重命名为 `.env`，然后编辑 `.env` 文件，填入你的配置信息。

```bash
cp .env.example .env
```

你需要根据注释提示，填写以下关键信息：
- **账户信息**: `USER1`, `PASS1`, `USER2`, `PASS2` 等。
- **验证码服务**: 如果使用账号密码登录，必须配置验证码服务。推荐使用 `yescaptcha`，并填入 `CLIENTT_KEY`。
- **定时任务**: `RUN_AT` 变量用于设置签到任务的执行时间。
    - **固定时间**: 如 `10:30`，表示每天上午10点30分执行。
    - **时间范围**: 如 `10:00-18:00`，表示在每天上午10点到下午6点之间随机选择一个时间点执行。
    - **默认值**: 如果不设置，默认为 `09:00-21:00`。

**第三步：启动服务**

在存放 `docker-compose.yml` 和 `.env` 文件的目录下，执行以下命令在后台构建并启动服务：

```bash
docker-compose up -d
```

**第四步：查看日志**

你可以使用以下命令实时查看容器的日志，以确认服务是否正常运行和签到是否成功：

```bash
docker-compose logs -f
```

**第五步：停止服务**

如果需要停止并移除服务容器，可以执行以下命令：

```bash
docker-compose down
```

### 方式四：账号密码登录（自动获取新Cookie）

当 Cookie 失效时，系统会尝试使用账号密码方式登录并获取新的 Cookie。登录需要通过验证码验证，支持以下两种验证码解决方案：

#### 方案A：CloudFreed 自建服务（推荐家宽用户）

```bash
docker run -itd   --name cloudflyer   -p 3000:3000   --restart unless-stopped   jackzzs/cloudflyer -K 你的客户端密钥 -H 0.0.0.0
```

配置以下环境变量：

| 变量名称 | 说明 |
| :------: | :--- |
| `API_BASE_URL` | CloudFreed 服务地址，如 `http://192.168.1.100:3000` |
| `CLIENTT_KEY` | CloudFreed 服务的客户端密钥 |
| `USER1`/`USER2`... | NodeSeek 论坛用户名 |
| `PASS1`/`PASS2`... | NodeSeek 论坛密码 |
| `SOLVER_TYPE` | 设置为 `turnstile`（默认值） |

#### 方案B：YesCaptcha 商业服务（推荐无法自建服务的用户）

1. 访问 [YesCaptcha](https://yescaptcha.com/i/k2Hy3Q) 注册账号
2. 注册后联系客服可免费获得余额（约可使用60次登录）
3. 配置以下环境变量：

| 变量名称 | 说明 |
| :------: | :--- |
| `CLIENTT_KEY` | YesCaptcha 的 API 密钥 |
| `USER1`/`USER2`... | NodeSeek 论坛用户名 |
| `PASS1`/`PASS2`... | NodeSeek 论坛密码 |
| `SOLVER_TYPE` | 设置为 `yescaptcha` |

> **提示**：YesCaptcha 提供两个服务节点，可根据网络情况选择：
> - 国际节点：`https://api.yescaptcha.com`（默认）
> - 国内节点：`https://cn.yescaptcha.com`

### 多账号配置方法

本脚本支持多账号签到，配置方法如下：

#### 1. Cookie方式

使用 `NS_COOKIE` 环境变量设置多账号，账号之间使用 `&` 或换行符分隔：

```
# 使用 & 分隔多个Cookie
NS_COOKIE=Cookie1&Cookie2&Cookie3

# 或使用换行符分隔
NS_COOKIE=Cookie1
Cookie2
Cookie3
```

#### 2. 用户名密码方式

使用编号变量设置多账号：

```
# 第一个账号
USER1=用户名1
PASS1=密码1

# 第二个账号
USER2=用户名2
PASS2=密码2

# 第三个账号
USER3=用户名3
PASS3=密码3

# 依此类推...
```

> **注意**：基本的 `USER` 和 `PASS` 变量也会被识别，系统会自动检测所有设置的账号，并依次执行签到操作。

## 🔑 GitHub Personal Access Token 设置

为了实现自动更新Cookie功能，脚本需要使用GitHub Personal Access Token (PAT)将获取的新Cookie保存到仓库变量中。

### 1. 创建Personal Access Token

1. 登录您的GitHub账户
2. 点击右上角头像 → 选择 "Settings"（设置）
3. 滚动到页面底部 → 点击 "Developer settings"（开发者设置）
4. 在左侧菜单选择 "Personal access tokens" → 点击 "Tokens (classic)"
5. 点击 "Generate new token" → 选择 "Generate new token (classic)"
6. 配置token：
   - 名称：填写一个描述性名称，如 "NodeSeek签到脚本"
   - 过期时间：根据需要选择（推荐90天或更长）
   - 勾选权限：
     - `repo` (完整的仓库访问权限)
     - `workflow` (用于管理GitHub Actions)
7. 点击页面底部的 "Generate token" 按钮
8. **立即复制生成的token**，关闭页面后将无法再次查看

### 2. 添加到仓库Secrets

1. 进入您的NodeSeek-Signin仓库
2. 点击 "Settings" → "Secrets and variables" → "Actions"
3. 点击 "New repository secret"
4. 名称填写：`GH_PAT`
5. 值填写：刚才复制的Personal Access Token
6. 点击 "Add secret" 保存

完成以上设置后，签到脚本可以自动将有效的Cookie保存到GitHub仓库变量中，下次运行时直接使用，减少重复登录和验证码操作。

## 🔧 环境变量完整说明

| 变量名称 | 必要性 | 默认值 | 说明 |
| :------: | :----: | :----: | :--- |
| `NS_COOKIE` | 建议 | - | NodeSeek 论坛的用户 Cookie，多账号使用`&`或换行符分隔 |
| `USER1`、`USER2`... | 可选 | - | NodeSeek 论坛用户名，当 Cookie 失效时使用 |
| `PASS1`、`PASS2`... | 可选 | - | NodeSeek 论坛密码 |
| `NS_RANDOM` | 可选 | true | 是否随机签到（true/false） |
| `RUN_AT` | 可选 | `09:00-21:00` | **仅Docker Compose可用**。设置定时任务执行时间，支持固定时间 `10:30` 或时间范围 `10:00-18:00` |
| `SOLVER_TYPE` | 可选 | turnstile | 验证码解决方案（turnstile/yescaptcha） |
| `API_BASE_URL` | 条件必需 | - | CloudFreed 服务地址，当 SOLVER_TYPE=turnstile 时必填 |
| `CLIENTT_KEY` | 必需 | - | 验证码服务客户端密钥 |
| `GH_PAT` | 可选 | - | GitHub Personal Access Token，用于自动更新Cookie变量 |
| 各类通知变量 | 可选 | - | 支持多种推送通知平台配置 |

## 📊 验证码服务对比

| 服务 | 类型 | 优点 | 缺点 | 推荐指数 |
| :--: | :--: | :--- | :--- | :------: |
| CloudFreed | 自建服务 | 免费、无次数限制 | 需要自行部署维护 | ★★★★☆ |
| YesCaptcha | 商业服务 | 稳定可靠、易于配置 | 付费服务（有免费额度） | ★★★★★ |

## ⚠️ 免责声明

本项目仅供学习交流使用，请遵守 NodeSeek 论坛的相关规定和条款。

## 👨‍💻 本地开发与测试

为了方便在本地进行开发和调试，项目提供了一套零侵入的测试方案。你可以按照以下步骤在本地环境中运行签到脚本。

### 第一步：创建虚拟环境

首先，建议创建一个独立的 Python 虚拟环境，以避免依赖冲突。

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate
```

### 第二步：安装依赖

项目包含两份依赖文件：`requirements.txt` 用于生产环境，`requirements-dev.txt` 包含本地测试所需的额外库。

```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

### 第三步：配置环境变量

将环境变量示例文件 `.env.example` 复制一份并重命名为 `.env`，然后根据你的需求填入测试配置，例如账号密码和验证码服务密钥。

```bash
cp .env.example .env```

### 第四步：运行测试

配置完成后，执行以下命令即可运行一次性的签到测试。

```bash
python test_run.py
```

该脚本会自动加载 `.env` 文件中的环境变量，并执行主签到程序，让你可以在本地快速验证签到逻辑是否正常工作。
