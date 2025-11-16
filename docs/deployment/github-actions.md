
## 1. 创建Personal Access Token
为了实现自动更新Cookie功能，脚本需要使用GitHub Personal Access Token (PAT)将获取的新Cookie保存到仓库变量中。
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

## 🔑 GitHub actions
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
> 
> **注意**：基本的 `USER` 和 `PASS` 变量也会被识别，系统会自动检测所有设置的账号，并依次执行签到操作。
