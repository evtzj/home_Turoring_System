# Tutor — 家教匹配平台

全栈家教匹配系统，学生浏览教师、发起匹配、下单上课；教师接单授课；内置实时聊天。

## 技术栈

| 层 | 技术 |
|----|------|
| 后端框架 | Django 6.0 + Django REST Framework |
| 实时通信 | Django Channels + Redis |
| 数据库 | SQLite（开发）/ MySQL（生产） |
| 前端 | 原生 HTML/CSS/JS，Apple 设计风格 |
| 部署 | Docker + Gunicorn + Nginx |

## 项目结构

```
tutor_backend/
├── tutor_backend/       # Django 配置
├── user/                # 用户：注册/登录/个人资料
├── info/                # 教师信息：列表/详情/筛选
├── order/               # 订单：创建/状态流转
├── match/               # 匹配：发起/确认/拒绝
├── chat/                # 聊天：HTTP + WebSocket
├── admin_api/           # 管理员：审核/统计
├── frontend/            # 前端页面视图
├── templates/frontend/  # HTML 模板
│   ├── home.html        # 首页
│   ├── login.html       # 登录
│   ├── register.html    # 注册（教师/学生角色切换）
│   └── dashboard.html   # 工作台
└── manage.py
```

## 页面路由

| 路径 | 页面 |
|------|------|
| `/` | 首页 |
| `/login/` | 登录 |
| `/register/` | 注册 |
| `/dashboard/` | 工作台（登录后） |

## API 接口

所有接口需要 Token 认证（注册/登录除外），请求头：`Authorization: Token <token>`

### 用户

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/api/user/register/` | 注册（教师需传 `subject` `teaching_years`） |
| POST | `/api/user/login/` | 登录，返回 token |
| GET/PUT | `/api/user/me/` | 查看/修改个人信息 |
| POST | `/api/user/logout/` | 登出 |

### 教师信息

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/info/teachers/` | 教师列表 `?subject=数学&ordering=-teaching_years` |
| GET | `/api/info/teachers/<id>/` | 教师详情 |

### 订单

| 方法 | 路径 | 说明 |
|------|------|------|
| GET/POST | `/api/orders/` | 订单列表 / 创建 |
| GET/PUT | `/api/orders/<id>/` | 详情 / 更新状态 |

状态流转：`pending → confirmed → in_progress → completed`

### 匹配

| 方法 | 路径 | 说明 |
|------|------|------|
| GET/POST | `/api/match/matches/` | 匹配列表 / 发起匹配 |
| GET | `/api/match/matches/<id>/` | 匹配详情 |
| PUT | `/api/match/matches/<id>/confirm/` | 确认匹配（accepted/declined） |

### 聊天

| 方法 | 路径 | 说明 |
|------|------|------|
| GET/POST | `/api/chat/matches/<match_id>/messages/` | 获取/发送消息 |
| WebSocket | `ws://host/ws/chat/<match_id>/` | 实时推送 |

### 管理员

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/admin/users/` | 用户列表 |
| GET | `/api/admin/users/<id>/` | 用户详情 |
| PUT | `/api/admin/teachers/<id>/check/` | 审核教师 |
| GET | `/api/admin/stats/` | 平台统计 |

## 本地运行

```bash
# 1. 虚拟环境
python3 -m venv .venv
source .venv/bin/activate

# 2. 安装依赖
pip install -r requirements.txt

# 3. 迁移
cd tutor_backend
python manage.py migrate

# 4. 启动
python manage.py runserver
```

访问 `http://127.0.0.1:8000/`

## Docker 部署

```bash
docker compose up -d --build
```

服务运行在 `http://localhost:8088`
