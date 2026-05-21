# 《迭代 5 提交报告》Word 文档大纲

> 使用说明：将下列章节复制到 Word，按「【填写】」占位符补全内容，并按提示插入截图。

---

## 封面

- **课程名称**：软件工程  
- **作业名称**：迭代 5 — Web 图形界面与 DevOps 部署  
- **项目名称**：Soft-Engineering 文字 MUD  
- **团队编号 / 组名**：【填写，如 4399】  
- **团队成员与分工**：【填写表格：姓名 | 学号 | 本周分工】  
- **提交日期**：【填写】  
- **Git 仓库链接**：【填写，如 https://github.com/xxx/Soft-Engineering 】  

---

## 摘要（200～300 字）

【填写】说明本迭代完成了：

1. 将命令行 MUD 升级为 React + Canvas 2D Web 应用；  
2. 通过 FastAPI REST 实现前后端分离与联调；  
3. 编写 Dockerfile 并在 GitHub Actions 中自动化构建镜像（GHCR）；  
4. 增加 REST API 集成测试，保障前后端通信链路。  

---

## 1. 迭代目标与完成情况

### 1.1 课程要求对照表

| 验收项 | 要求摘要 | 完成情况 | 证据位置 |
|--------|----------|----------|----------|
| Web UI | React/Vue 或 Canvas 2D 图形界面 | 【已完成 / 部分完成】 | `frontend/`，截图见附录 A |
| 前后端分离 | RESTful API 对接业务逻辑 | 【已完成】 | `backend/app.py`，`src/game_service.py` |
| Docker | Dockerfile + CI 镜像构建 | 【已完成】 | `Dockerfile`，`.github/workflows/ci.yml` |
| API 集成测试 | 流水线中集成测试 | 【已完成】 | `tests/test_api_integration.py` |

### 1.2 本迭代新增/修改的主要文件

- `frontend/` — Web 前端  
- `backend/app.py` — REST API  
- `src/game_service.py`、`src/world_builder.py` — 业务服务层  
- `Dockerfile`、`docker-compose.yml`  
- `tests/test_api_integration.py`  
- `docs/iteration5_web_devops.md`  

---

## 2. 系统架构设计

### 2.1 总体架构说明

【填写文字 + 可插入架构图】

描述三层结构：

- **表现层**：React + Canvas（`frontend/`）  
- **接口层**：FastAPI REST（`backend/app.py`）  
- **领域层**：命令模式 + 游戏服务（`src/command.py`、`src/game_service.py`）  

【插图建议】：README 或 `docs/iteration5_web_devops.md` 中的 mermaid 架构图导出为图片插入。

### 2.2 前后端分离设计

- 前端通过 HTTP 调用 `/api`（开发环境由 Vite 代理到 `127.0.0.1:8000`）  
- 会话机制：`POST /game/start` 返回 `sessionId`，后续请求 Header 携带 `X-Session-Id`  
- 与迭代 3 契约对齐的端点：`/player`、`/room`、`/movement`、`/combat/attack`、`/inventory`、`/item/pickup`、`/help` 等  

### 2.3 业务逻辑复用说明

【填写】说明 `world_builder.py` 与 `game_service.py` 如何复用原有 `command.py` 逻辑，避免 CLI 与 API 两套实现。

---

## 3. Web 图形界面实现

### 3.1 技术选型

- 框架：React 18 + Vite  
- 图形：HTML5 Canvas 2D  
- 选型理由：【填写：轻量、易与课程栈结合、便于 2D 房间可视化】  

### 3.2 界面功能说明

【填写 + 附录截图 A】

| 功能 | 实现方式 |
|------|----------|
| 房间可视化 | Canvas 绘制房间、出口、物品、敌人 |
| 移动 | 点击出口圆点 / 方向按钮 → `POST /movement` |
| 拾取 | 点击物品 → `POST /item/pickup` |
| 战斗 | 「攻击」按钮 → `POST /combat/attack` |
| 状态展示 | 侧栏 HP、背包、日志 |

### 3.3 本地运行步骤（可写入报告附录）

```text
终端1: uvicorn backend.app:app --reload --port 8000
终端2: cd frontend && npm run dev
浏览器: http://localhost:5173
```

---

## 4. RESTful API 与前后端联调

### 4.1 API 端点一览

【表格填写】

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | /game/start | 开始游戏，返回 sessionId |
| GET | /player | 玩家信息 |
| GET | /player/status | 玩家状态 |
| GET | /room | 当前房间 |
| POST | /movement | 移动 |
| POST | /combat/attack | 攻击 |
| GET | /inventory | 背包 |
| POST | /item/pickup | 拾取 |
| GET | /help | 帮助 |

### 4.2 联调过程与问题记录

【填写 1～2 个真实问题，例如】

- 问题：移动后房间信息未更新  
- 原因：`engine.current_room` 与 `player.current_room` 未同步  
- 解决：在 `MoveCommand` 与 `game_service` 中同步房间引用  

### 4.3 API 文档截图

【附录 B】：http://127.0.0.1:8000/docs 的 Swagger 页面截图。

---

## 5. 云原生与 DevOps（Docker + CI）

### 5.1 Dockerfile 说明

【填写要点】

- 基础镜像：`python:3.12-slim`  
- 暴露端口：8000  
- 启动命令：`uvicorn backend.app:app --host 0.0.0.0 --port 8000`  
- 健康检查：`GET /health`  

【可选】粘贴 `Dockerfile` 关键片段（5～10 行）。

### 5.2 CI/CD 流水线说明

【填写】描述 `.github/workflows/ci.yml` 三个阶段：

1. 单元测试 + API 集成测试  
2. Docker build & push 至 `ghcr.io/<仓库>/mud-api`  
3. 前端 `npm run build` 校验  

【附录 C】：GitHub Actions 运行成功截图（全绿）。

### 5.3 本地 Docker 情况（如实填写）

- 【二选一填写】  
  - 已安装 Docker Desktop，本地 `docker build` 成功（附截图）；或  
  - 本机未安装 Docker，容器构建在 GitHub Actions 云端完成，仓库已提供 `Dockerfile` 与 CI 配置。  

### 5.4 镜像地址（若已 push）

- 镜像：`ghcr.io/【组织/用户名】/【仓库名】/mud-api:latest`  
- 获取方式：GitHub → Packages  

---

## 6. API 集成测试

### 6.1 测试策略

【填写】说明为何在单元测试之外需要集成测试：验证 HTTP 层、会话 Header、端到端游戏流程。

### 6.2 测试用例覆盖

【表格】

| 用例 | 验证点 |
|------|--------|
| test_game_start | 会话创建、初始房间 |
| test_movement_chain | 移动后房间变更 |
| test_pickup_and_attack_flow | 拾取 + 战斗 |
| test_missing_session | 401 鉴权 |

### 6.3 执行结果

【填写命令与结果】

```text
pytest tests/test_api_integration.py -v
结果：9 passed
```

【附录 D】：终端全绿截图。

### 6.4 与单元测试的关系

【填写】单元测试 22+ 项覆盖 `command/player/enemy`；集成测试 9 项覆盖 API 契约与链路。

---

## 7. 迭代 4 回扣（如课程要求一并提交）

| 项目 | 文件路径 | 状态 |
|------|----------|------|
| AGENTS.md | `/AGENTS.md` | 【已提交】 |
| Prompt 演化实验 | `docs/iteration4_prompt_evolution.md` | 【已提交】 |
| CIVC 审计 | `docs/civc_iteration4_audit.md` | 【已提交】 |
| 核心模块覆盖率 | 【填写 %】 | 【附截图】 |

---

## 8. 团队分工与工作量

【表格填写】

| 成员 | 主要负责 | 本周工时（约） |
|------|----------|----------------|
| 成员A | 前端 Canvas、联调 | 【】 |
| 成员B | FastAPI、game_service | 【】 |
| 成员C | Docker、CI、集成测试 | 【】 |
| 成员D | 文档、报告、截图整理 | 【】 |

---

## 9. 风险、不足与后续计划

### 9.1 当前不足

【填写，示例】

- 会话存储在内存，服务重启后会话丢失；  
- 未实现多人在线；  
- 本机未部署生产级 K8s。  

### 9.2 迭代 6 计划（可选）

- 会话持久化（Redis）  
- 前端 UI 美化 / 音效  
- 有服务器时增加自动部署（CD）  

---

## 10. 总结

【150 字左右】本迭代完成了从 CLI MUD 到 Web 全栈的架构演进，建立了可测试、可容器化、可 CI 的交付链路，满足课程迭代 5 验收要求。

---

## 附录（截图清单）

| 编号 | 内容 | 文件名建议 |
|------|------|------------|
| 附录 A | Web 2D 游戏界面（移动/战斗/背包） | `web-ui.png` |
| 附录 B | Swagger API 文档页 | `api-docs.png` |
| 附录 C | GitHub Actions 流水线成功 | `ci-success.png` |
| 附录 D | API 集成测试通过 | `integration-test.png` |
| 附录 E | GHCR 镜像（可选） | `ghcr-package.png` |
| 附录 F | 核心模块覆盖率（迭代4，若需要） | `coverage.png` |

---

## 提交清单（提交前勾选）

- [ ] Word/PDF 报告已含仓库链接  
- [ ] 附录截图 ≥ 3 张（Web + 集成测试 + CI）  
- [ ] 代码已 push 到 GitHub  
- [ ] Actions 最近一次运行成功  
- [ ] 组内已确认分工表无误  
