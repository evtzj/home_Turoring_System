# Tutor - 家教匹配平台

基于 Django 的全栈家教匹配系统，支持学生找老师、老师接单、在线聊天等功能。

## 技术栈

- **后端**: Python 3.12 + Django 6.0 + Django REST Framework
- **数据库**: SQLite
- **实时通信**: Django Channels + Redis
- **部署**: Docker + Gunicorn + Nginx

## 功能模块

| 模块 | 说明 |
|------|------|
| user | 注册、登录、Token 认证、教师资料管理 |
| info | 教师列表查询（学科筛选、排序）、教师详情 |
| order | 订单创建与管理（pending → confirmed → in_progress → completed） |
| match | 学生发起匹配请求，教师确认/拒绝 |
| chat | 基于匹配的在线聊天（支持 WebSocket） |
| admin_api | 用户管理、教师认证、数据统计 |
| frontend | Apple 风格前端页面（登录、注册、工作台） |

## 项目结构

```
tutor_backend/
├── tutor_backend/          # Django 配置（settings, urls, wsgi, asgi）
├── user/                   # 用户模块
├── info/                   # 教师信息模块
├── order/                  # 订单模块
├── match/                  # 匹配模块
├── chat/                   # 聊天模块
├── admin_api/              # 管理员 API
├── frontend/               # 前端页面视图
├── templates/frontend/      # HTML 模板
└── manage.py               # Django 管理脚本
```

## API 接口

### 用户
| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/api/user/register/` | 注册 |
| POST | `/api/user/login/` | 登录（返回 Token） |
| GET/PUT | `/api/user/me/` | 查看/修改个人信息 |
| POST | `/api/user/logout/` | 登出 |

### 教师信息
| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/info/teachers/` | 教师列表（支持 `?subject=` 筛选，`?ordering=` 排序） |
| GET | `/api/info/teachers/<id>/` | 教师详情 |

### 订单
| 方法 | 路径 | 说明 |
|------|------|------|
| GET/POST | `/api/orders/` | 订单列表 / 创建订单 |
| GET/PUT | `/api/orders/<id>/` | 订单详情 / 更新状态 |

### 匹配
| 方法 | 路径 | 说明 |
|------|------|------|
| GET/POST | `/api/match/matches/` | 匹配列表 / 发起匹配 |
| GET | `/api/match/matches/<id>/` | 匹配详情 |
| POST | `/api/match/matches/<id>/confirm/` | 确认匹配 |

### 聊天
| 方法 | 路径 | 说明 |
|------|------|------|
| GET/POST | `/api/chat/matches/<match_id>/messages/` | 获取 / 发送消息 |

### 管理
| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/admin/users/` | 用户列表 |
| GET | `/api/admin/users/<id>/` | 用户详情 |
| PUT | `/api/admin/teachers/<id>/check/` | 审核教师 |
| GET | `/api/admin/stats/` | 数据统计 |

> Token 认证：请求头携带 `Authorization: Token <your-token>`

## 本地开发

```bash
# 1. 创建虚拟环境
python3 -m venv .venv
source .venv/bin/activate

# 2. 安装依赖
pip install -r requirements.txt

# 3. 数据库迁移
cd tutor_backend
python manage.py migrate

# 4. 启动开发服务器
python manage.py runserver
```

访问 `http://localhost:8000/login/`

## Docker 部署

```bash
docker compose up -d --build
```

服务运行在 `http://localhost:8088`
