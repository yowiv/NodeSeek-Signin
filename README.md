# NodeSeek-Signin

## 项目介绍

这是一个用于 NodeSeek 论坛自动签到的工具，支持通过 GitHub Actions 或青龙面板进行定时自动签到操作。签到模式默认为随机签到，帮助用户轻松获取论坛每日签到奖励。

## 功能特点

- 支持 GitHub Actions 自动运行
- 支持青龙面板定时任务
- 支持 Cookie 或账号密码登录方式
- 可配置 Telegram 机器人通知


## 使用方法

### 方式一：GitHub Actions

1. Fork 本仓库到自己的 GitHub 账号下
2. 在仓库的 Settings > Secrets and variables > Actions 中添加以下必要配置：

| 变量名称 | 必要性 | 说明 |
| :------: | :----: | :--- |
| `NS_COOKIE` | **必需** | NodeSeek 论坛的用户 Cookie，可在浏览器开发者工具(F12)的网络请求中获取 |
| `TG_BOT_TOKEN` | 可选 | Telegram 机器人的 Token，用于通知签到结果 |
| `TG_USER_ID` | 可选 | Telegram 用户 ID，用于接收通知 |
| `TG_THREAD_ID` | 可选 | Telegram 超级群组话题 ID，用于在特定话题中发送通知 |

> **注意**：如果签到结果显示 "USER NOT FOUND" 或返回 HTML 内容，说明 Cookie 已失效，需要重新获取。

### 方式二：青龙面板

在青龙面板中执行以下命令克隆本仓库：

```bash
ql clone https://github.com/yowiv/NodeSeek-Signin.git
```

然后在环境变量中添加所需配置。

### 方式三：账号密码登录

如需使用账号密码登录方式，需要先部署 Cloudflare 验证码求解服务：

```bash
docker run -itd --name cloudfreed -p 3000:3000 \
  -e CLIENT_KEY=你的客户端密钥 \
  -e MAX_TASKS=1 \
  -e TIMEOUT=120 \
  sanling000/cloudfreed
```

> **提示**：建议在家宽 IP 的机器上安装此服务以获得更好的稳定性。

然后配置以下环境变量：

| 变量名称 | 必要性 | 说明 |
| :------: | :----: | :--- |
| `API_BASE_URL` | 可选 | Cloudflare 求解服务的 URL |
| `CLIENTT_KEY` | 可选 | 验证码服务的客户端密钥 |
| `USER` | 可选 | NodeSeek 论坛用户名 |
| `PASS` | 可选 | NodeSeek 论坛密码 |

## 免责声明

本项目仅供学习交流使用，请遵守 NodeSeek 论坛的相关规定和条款。
