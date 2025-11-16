# NodeSeek 签到 Cloudflare Worker 版本

这是一个可以直接部署到 Cloudflare Workers 的 NodeSeek 自动签到脚本，使用 2captcha 解决 Turnstile 验证码。

## 功能特性

- ✅ 自动解决 Cloudflare Turnstile 验证码（使用 2captcha）
- ✅ 支持多账户批量签到
- ✅ 支持定时任务自动执行
- ✅ 支持手动触发签到
- ✅ Telegram 通知推送
- ✅ Cookie 自动管理和更新
- ✅ 登录失败自动重试

## 部署步骤

### 1. 准备工作

#### 1.1 注册 2captcha 账号

1. 访问 [2captcha.com](https://2captcha.com/)
2. 注册账号并充值
3. 在 [API 设置页面](https://2captcha.com/enterpage) 获取 API Key

#### 1.2 获取 Telegram 通知参数（可选）

如果需要接收 Telegram 通知：

1. 创建 Bot：与 [@BotFather](https://t.me/BotFather) 对话，发送 `/newbot` 创建机器人，获取 `Bot Token`
2. 获取 Chat ID：与 [@userinfobot](https://t.me/userinfobot) 对话，获取你的 `Chat ID`

### 2. 部署到 Cloudflare Workers

#### 方式一：通过 Cloudflare Dashboard（推荐新手）

1. 登录 [Cloudflare Dashboard](https://dash.cloudflare.com/)
2. 进入 Workers & Pages
3. 点击 "创建应用程序" → "创建 Worker"
4. 给 Worker 起个名字，如 `nodeseek-signin`
5. 点击 "部署"
6. 点击 "编辑代码"
7. 删除默认代码，复制 `nodeseek-cloudflare-worker.js` 的全部内容
8. 点击 "保存并部署"

#### 方式二：使用 Wrangler CLI

```bash
# 安装 Wrangler
npm install -g wrangler

# 登录 Cloudflare
wrangler login

# 创建 wrangler.toml 配置文件
cat > wrangler.toml << EOF
name = "nodeseek-signin"
main = "nodeseek-cloudflare-worker.js"
compatibility_date = "2024-01-01"

[vars]
# 这里可以配置非敏感的环境变量
EOF

# 部署
wrangler deploy
```

### 3. 配置环境变量

在 Cloudflare Dashboard 中：

1. 进入你的 Worker
2. 点击 "设置" → "变量"
3. 添加以下环境变量：

#### 必填环境变量

| 变量名 | 说明 | 示例 |
|--------|------|------|
| `user` | NodeSeek 用户名（多个用`&`分隔） | `user1&user2` |
| `pass` | 密码（多个用`&`分隔，与user对应） | `pass1&pass2` |
| `CAPTCHA_API_KEY` | 2captcha API密钥 | `abc123def456...` |

#### 可选环境变量

| 变量名 | 说明 | 默认值 |
|--------|------|--------|
| `CAPTCHA_API_URL` | 2captcha API地址 | `https://api.2captcha.com` |
| `NS_COOKIE` | 已有的Cookie（可选，多个用`&`分隔） | - |
| `BotToken` | Telegram Bot Token | - |
| `ChatID` | Telegram Chat ID | - |

#### 配置示例

```
user: alice&bob
pass: password123&password456
CAPTCHA_API_KEY: 1234567890abcdef1234567890abcdef
BotToken: 123456789:ABCdefGHIjklMNOpqrsTUVwxyz
ChatID: 123456789
```

**注意事项：**
- `user` 和 `pass` 的数量必须一一对应
- 如果提供了 `NS_COOKIE`，会先尝试使用 Cookie 签到，失败后才会登录
- 2captcha 服务需要付费，请确保账户有足够余额

### 4. 设置定时任务

在 Cloudflare Dashboard 中：

1. 进入你的 Worker
2. 点击 "触发器" → "Cron 触发器"
3. 点击 "添加 Cron 触发器"
4. 输入 Cron 表达式，例如：
   - `0 9 * * *`（每天上午9点执行）
   - `0 */12 * * *`（每12小时执行一次）
   - `30 8 * * *`（每天上午8:30执行）
5. 点击 "添加触发器"

#### Cron 表达式说明

```
┌───────────── 分钟 (0 - 59)
│ ┌───────────── 小时 (0 - 23)
│ │ ┌───────────── 日期 (1 - 31)
│ │ │ ┌───────────── 月份 (1 - 12)
│ │ │ │ ┌───────────── 星期 (0 - 6) (0 = 星期日)
│ │ │ │ │
* * * * *
```

**常用示例：**
- `0 9 * * *` - 每天上午9点
- `0 0 * * *` - 每天凌晨12点
- `0 */6 * * *` - 每6小时一次
- `0 8,20 * * *` - 每天上午8点和晚上8点

### 5. 手动触发签到

你可以通过 HTTP POST 请求手动触发签到：

```bash
curl -X POST https://your-worker-name.your-subdomain.workers.dev/checkin
```

## 工作原理

1. **定时执行或手动触发**：根据 Cron 设置自动执行，或通过 HTTP 请求手动触发
2. **读取账户配置**：从环境变量读取账户信息
3. **验证码解决**：
   - 使用 2captcha API 创建 Turnstile 验证码任务
   - 轮询获取验证码解决结果（最多等待2分钟）
4. **登录**：使用验证码令牌进行登录，获取 Cookie
5. **签到**：使用 Cookie 调用签到 API
6. **Cookie 管理**：
   - 如果提供了 `NS_COOKIE`，优先使用
   - 如果 Cookie 失效，自动重新登录获取新 Cookie
7. **通知推送**：将签到结果通过 Telegram 发送

## 注意事项

### 关于 2captcha

- **费用**：2captcha 是付费服务，Turnstile 验证码约 $2.99/1000次
- **速度**：通常在 10-60 秒内解决验证码
- **余额**：请确保账户有足够余额，否则会报错
- **API限制**：注意 API 调用频率限制

### 关于 Cloudflare Workers

- **免费额度**：每天 100,000 次请求
- **执行时间限制**：
  - 免费版：最多 10ms CPU 时间
  - 付费版：最多 50ms CPU 时间
- **定时任务**：
  - 免费版：不支持 Cron 触发器
  - 付费版（$5/月）：支持 Cron 触发器

### Cookie 说明

- Cookie 有效期通常较长，可以多次使用
- 如果提供了 `NS_COOKIE` 环境变量，会优先使用现有 Cookie
- Cookie 失效时会自动重新登录（需要解决验证码）
- 建议定期手动登录一次，更新 `NS_COOKIE` 环境变量

## 故障排查

### 1. 签到失败

**可能原因：**
- Cookie 已失效
- 账号密码错误
- 验证码解决失败
- 2captcha 余额不足

**解决方法：**
- 检查 Cloudflare Workers 日志
- 验证账号密码是否正确
- 检查 2captcha 余额
- 尝试手动触发签到测试

### 2. 验证码解决超时

**可能原因：**
- 2captcha 服务繁忙
- API 密钥错误
- 网络连接问题

**解决方法：**
- 检查 `CAPTCHA_API_KEY` 是否正确
- 增加重试次数（修改代码中的 `maxRetries`）
- 更换 2captcha API 节点

### 3. Telegram 通知未收到

**可能原因：**
- Bot Token 或 Chat ID 错误
- Bot 未启动或被封禁
- Telegram API 被墙

**解决方法：**
- 验证 Bot Token 和 Chat ID
- 与 Bot 对话一次激活
- 使用代理或第三方 API（不推荐）

### 4. 定时任务未执行

**可能原因：**
- 使用的是免费版 Workers（不支持 Cron）
- Cron 表达式错误
- Worker 被禁用

**解决方法：**
- 升级到 Workers 付费版（$5/月）
- 检查 Cron 表达式语法
- 检查 Worker 状态

## 查看日志

在 Cloudflare Dashboard 中：

1. 进入你的 Worker
2. 点击 "日志" → "开始流式传输"
3. 手动触发一次签到查看实时日志
4. 或者等待定时任务执行

## 升级说明

如需更新代码：

1. 编辑 Worker 代码
2. 替换为新版本的 `nodeseek-cloudflare-worker.js` 内容
3. 点击 "保存并部署"

环境变量无需重新配置。

## 成本估算

假设每天签到 2 个账号：

- **2captcha 费用**：
  - 每次登录需要解决 1 次验证码
  - 假设每月登录 10 次（Cookie 失效）
  - 费用：10 次 × $2.99/1000 = $0.03/月

- **Cloudflare Workers 费用**：
  - 定时任务需要付费版：$5/月
  - 或使用外部定时服务免费触发（如 cron-job.org）

**总计**：约 $5/月（如果使用 Workers 定时任务）

## 替代方案

如果不想付费使用 Cloudflare Workers 的定时任务，可以：

1. **使用外部定时服务**：
   - [cron-job.org](https://cron-job.org/)（免费）
   - [EasyCron](https://www.easycron.com/)（免费额度）
   - GitHub Actions（完全免费）

2. **手动触发**：
   - 每天手动访问 `/checkin` 接口
   - 使用浏览器书签快速触发

## 技术支持

如遇到问题：

1. 查看 Cloudflare Workers 日志
2. 检查环境变量配置
3. 验证 2captcha 余额和 API Key
4. 提交 Issue 到原项目仓库

## 许可证

本项目基于原 NodeSeek-Signin 项目改编，遵循相同的开源许可证。

## 免责声明

- 本脚本仅供学习交流使用
- 使用本脚本产生的任何后果由使用者自行承担
- 请遵守 NodeSeek 网站的服务条款
- 请勿滥用自动化工具
