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

##  快速开始

1. **获取代码**：Fork/Clone 本仓库，或在青龙面板/Cloudflare Worker 等环境中拉取脚本。
2. **选择部署方式**：根据自己的运行环境（GitHub Actions、Docker、青龙、Cloudflare Worker）跳转到对应文档完成部署。
3. **配置变量**：按照 [`docs/configuration/config.md`](docs/configuration/config.md) 填写 `NS_COOKIE`、`USERn/PASSn`、验证码与通知变量；验证码方案差异见 [`docs/configuration/solutions.md`](docs/configuration/solutions.md)。
4. **验证运行**：在目标环境触发一次任务（或运行 `python test_run.py`）确认签到与通知均正常。

## 🧱 部署方式一览

| 场景 | 文档 | 说明 |
| --- | --- | --- |
| GitHub Actions | [`docs/deployment/github-actions.md`](docs/deployment/github-actions.md) | 适合纯云端运行，可结合 `GH_PAT` 自动回写 Cookie |
| Docker Compose / 本地服务器 | [`docs/deployment/docker-compose.md`](docs/deployment/docker-compose.md) | 支持 `RUN_AT` 定时和 `IN_DOCKER` 持久化 Cookie |
| 青龙面板 | [`docs/deployment/qinglong-panel.md`](docs/deployment/qinglong-panel.md) | 与青龙定时任务深度集成，沿用面板通知 |
| Cloudflare Worker | [`docs/deployment/cloudflare-worker.md`](docs/deployment/cloudflare-worker.md) | 适合无服务器场景，可配合第三方验证码服务 |

> 🎯 以上文档包含详细步骤、示例命令及截图，README 仅保留概览。

##  配置小抄

- **账户与 Cookie**：全量变量说明见 [`config.md`](docs/configuration/config.md)。支持 `NS_COOKIE` 多账号或 `USERn/PASSn` 自动登录，两者可共存。
- **验证码方案**：[`solutions.md`](docs/configuration/solutions.md) 对比 CloudFreed、自建接口与 YesCaptcha，并列出必填变量。
- **通知渠道**：`notify.py` 中的 `push_config` 覆盖 Telegram、Bark、PushPlus、企业微信、邮件等渠道，对应变量也收录在环境变量手册。
- **GitHub PAT & 自动回写**：如需在 Actions 中自动更新仓库变量 `NS_COOKIE`，请在设置中添加 `GH_PAT`，具体操作步骤详见 GitHub Actions 文档。
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

## ⚠️ 免责声明

本项目仅供学习交流使用，请遵守 NodeSeek 论坛的相关规定和条款。
