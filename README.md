# NodeSeek-Signin

NodeSeek论坛签到，借助github action或青龙面板 自动触发，默认选择随机签到

## Action 

需要自行在setting中添加 Repository secrets

如果显示"USER NOT FOUND"或显示实际响应内容显示html就是cookie失效了需要重新抓


|  名称  |                 含义                  |
| :----: | :-----------------------------------: |
| NS_COOKIE | 论坛用户cookie，自行在浏览器F12中查看 |
| TG_BOT_TOKEN | tg 机器人的 TG_BOT_TOKEN，例：1407203283:AAG9rt-6RDaaX0HBLZQq0laNOh898iFYaRQ，非必需 |
| TG_USER_ID | tg 机器人的 TG_USER_ID，例：1434078534，非必需 |
| TG_THREAD_ID | tg 机器人的 TG_THREAD_ID 超级群组话题id，非必需 |
| PROXY | 代理服务器地址，格式如：http://username:password@127.0.0.1:7890 或 http://127.0.0.1:7890，非必需 |
| USE_PROXY | 是否使用代理，true或false，默认为false，非必需 |
| CLIENTT_KEY | 验证码服务的客户端密钥，非必需。注册链接：[YesCaptcha](https://yescaptcha.com/i/k2Hy3Q)。注册联系客服送余额大概可以使用60次登录|
| USER | 论坛用户名，非必需 |
| PASS | 论坛密码，非必需 |


## 青龙面板

```
ql raw https://raw.githubusercontent.com/YYWO/NodeSeek-Signin/main/nodeseek_sign.py
```
