# NodeSeek-Signin

NodeSeek论坛签到，借助github action或青龙面板 自动触发，默认选择随机签到

## Action 

需要自行在setting中添加 Repository secrets

如果显示"USER NOT FOUND"就是cookie失效了需要重新抓


|  名称  |                 含义                  |
| :----: | :-----------------------------------: |
| COOKIE | 论坛用户cookie，自行在浏览器F12中查看 |
|    PUSHPLUS_TOKEN    | pushplus中的用户token，用于推送，非必需 |
| TELEGRAM_BOT_TOKEN | 电报token，非必需 |
| CHAT_ID | 电报chatid，非必需 |
| THREAD_ID | 电报超级群组话题id，非必需 |
| TELEGRAM_API_URL | 代理api，非必需 |


## 青龙面板

```
ql raw https://raw.githubusercontent.com/YYWO/NodeSeek-Signin/main/nodeseek_sign.py
```
|  名称  |                 含义                  |
| :----: | :-----------------------------------: |
| NS_COOKIE | 论坛用户cookie，自行在浏览器F12中查看 |
