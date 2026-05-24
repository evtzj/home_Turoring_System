# Tutor - 家教匹配平台

Tutor 是一个基于 Django 的家教匹配系统，面向学生、教师和管理员三类角色。学生可以浏览教师、发起匹配、创建订单并进行实时聊天；教师可以维护个人资料、接收匹配和处理订单；管理员可以审核教师和查看平台统计。

## 功能概览

- 用户注册、登录、登出和个人资料维护
- 教师列表、教师详情、学科筛选和收藏
- 学生发起匹配，教师确认或拒绝匹配
- 订单创建、详情查看和状态流转
- 基于 Token 的 REST API 认证
- 基于 Django Channels 的 WebSocket 实时聊天
- 管理员用户管理、教师审核和数据统计
- Docker Compose 一键启动 Web 服务和 Redis

## 技术栈

| 层 | 技术 |
| --- | --- |
| 后端框架 | Django 6.0.3, Django REST Framework |
| 实时通信 | Django Channels, channels_redis |
| 认证 | DRF TokenAuthentication |
| 数据库 | SQLite 开发环境 |
| 缓存/消息层 | Redis |
| 前端 | Django Template, HTML, CSS, JavaScript |
| 部署 | Docker, Docker Compose, Gunicorn, Nginx |

## 项目结构

```text
home_Turoring_System/
├── Dockerfile
├── docker-compose.yml
├── nginx.conf
├── requirements.txt
├── README.md
└── tutor_backend/
    ├── manage.py
    ├── db.sqlite3
    ├── tutor_backend/       # Django 项目配置
    ├── user/                # 用户注册、登录、资料
    ├── info/                # 教师信息、收藏
    ├── match/               # 匹配发起、确认、拒绝
    ├── order/               # 订单创建、状态流转
    ├── chat/                # 聊天 HTTP API 和 WebSocket
    ├── admin_api/           # 管理员接口
    ├── frontend/            # 页面路由
    └── templates/frontend/  # 前端模板
```

## 本地开发

### 1. 创建虚拟环境

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 启动 Redis

聊天功能依赖 Redis。如果不使用 Docker，可以本地启动 Redis：

```bash
redis-server
```

或者只用 Docker 启动 Redis：

```bash
docker compose up -d redis
```

### 4. 数据库迁移

```bash
cd tutor_backend
python manage.py migrate
```

### 5. 启动开发服务

```bash
python manage.py runserver
```

访问：

```text
http://127.0.0.1:8000/
```

## Docker 部署

在项目根目录执行：

```bash
docker compose up -d --build
```

默认服务地址：

```text
http://localhost:8088
```

查看日志：

```bash
docker compose logs -f web
```

停止服务：

```bash
docker compose down
```

## 页面路由

| 路径 | 页面 |
| --- | --- |
| `/` | 首页 |
| `/login/` | 登录页 |
| `/register/` | 注册页 |
| `/dashboard/` | 用户工作台 |

## API 使用说明

除注册和登录外，大多数接口需要 Token 认证：

```http
Authorization: Token <token>
```

### 用户接口

| 方法 | 路径 | 说明 |
| --- | --- | --- |
| POST | `/api/user/register/` | 注册用户，教师注册时需要提交学科和教学年限 |
| POST | `/api/user/login/` | 登录并返回 token |
| GET | `/api/user/me/` | 获取当前用户信息 |
| PUT | `/api/user/me/` | 修改当前用户信息 |
| POST | `/api/user/logout/` | 登出 |

### 教师信息接口

| 方法 | 路径 | 说明 |
| --- | --- | --- |
| GET | `/api/info/teachers/` | 获取教师列表 |
| GET | `/api/info/teachers/<id>/` | 获取教师详情 |
| POST | `/api/info/teachers/<id>/favorite/` | 收藏教师 |
| DELETE | `/api/info/teachers/<id>/favorite/delete/` | 取消收藏教师 |

教师列表支持查询参数，例如：

```text
/api/info/teachers/?subject=数学&ordering=-teaching_years
```

### 匹配接口

| 方法 | 路径 | 说明 |
| --- | --- | --- |
| GET | `/api/match/matches/` | 获取匹配列表 |
| POST | `/api/match/matches/` | 发起匹配 |
| GET | `/api/match/matches/<id>/` | 获取匹配详情 |
| PUT | `/api/match/matches/<id>/confirm/` | 确认或拒绝匹配 |

### 订单接口

| 方法 | 路径 | 说明 |
| --- | --- | --- |
| GET | `/api/orders/orders/` | 获取订单列表 |
| POST | `/api/orders/orders/` | 创建订单 |
| GET | `/api/orders/orders/<id>/` | 获取订单详情 |
| PUT | `/api/orders/orders/<id>/` | 更新订单状态 |

订单状态流转：

```text
pending -> confirmed -> in_progress -> completed
```

### 聊天接口

| 类型 | 路径 | 说明 |
| --- | --- | --- |
| HTTP | `/api/chat/matches/<match_id>/messages/` | 获取或发送聊天消息 |
| WebSocket | `ws://<host>/ws/chat/<match_id>/` | 实时聊天推送 |

本地开发示例：

```text
ws://127.0.0.1:8000/ws/chat/1/
```

Docker 部署示例：

```text
ws://localhost:8088/ws/chat/1/
```

### 管理员接口

| 方法 | 路径 | 说明 |
| --- | --- | --- |
| GET | `/api/admin/users/` | 获取用户列表 |
| GET | `/api/admin/users/<id>/` | 获取用户详情 |
| PUT | `/api/admin/teachers/<id>/check/` | 审核教师 |
| GET | `/api/admin/stats/` | 查看平台统计 |

## 常用命令

```bash
# 创建管理员账号
cd tutor_backend
python manage.py createsuperuser

# 生成迁移文件
python manage.py makemigrations

# 执行迁移
python manage.py migrate

# 启动开发服务
python manage.py runserver
```

## 开发注意事项

- 当前配置使用 SQLite，数据库文件位于 `tutor_backend/db.sqlite3`。
- WebSocket 依赖 Redis，开发聊天功能前请确认 Redis 已启动。
- 当前 `DEBUG=True`，生产环境部署前需要关闭调试模式并替换 `SECRET_KEY`。
- Token 认证由 DRF `TokenAuthentication` 提供，前端请求受保护接口时需要携带 `Authorization` 请求头。

