# Docker Compose Deployment Guide

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
