# NodeSeek-Signin

NodeSeek论坛签到，借助github action或青龙面板 自动触发，默认选择随机签到

## Action 

需要自行在setting中添加 Repository secrets

如果显示"USER NOT FOUND"或显示实际响应内容显示html就是cookie失效了需要重新抓

cloudflare 求解
```
docker run -itd --name cloudfreed -p 3000:3000 -e CLIENT_KEY=YOUR_CLIENT_KEY -e MAX_TASKS=1 -e  TIMEOUT=120  sanling000/cloudfreed
```
如果要使用账号密码登录必须安装，在是家宽IP上的机器安装最好

CLIENT_KEY：客户端 API 密钥

MAX_TASKS：最大并发任务数（默认值：1）

timeout：每个任务的超时时间（以秒为单位）（默认值：120）


|  变量名称  |                 含义                  |
| :----: | :-----------------------------------: |
| NS_COOKIE | 论坛用户cookie，自行在浏览器F12中查看 |
| TG_BOT_TOKEN | tg 机器人的 TG_BOT_TOKEN，非必需 |
| TG_USER_ID | tg 机器人的 TG_USER_ID，非必需 |
| TG_THREAD_ID | tg 机器人的 TG_THREAD_ID 超级群组话题id，非必需 |
| API_BASE_URL | 登录客户端URL，非必需。 |
| CLIENTT_KEY | 验证码服务的客户端密钥，非必需。|
| USER | 论坛用户名，非必需 |
| PASS | 论坛密码，非必需 |


## 青龙面板

```
ql clone https://github.com/yowiv/NodeSeek-Signin.git
```
