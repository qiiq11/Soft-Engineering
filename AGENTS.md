# AGENTS.md（Soft-Engineering）

## 1) 项目目标
- 本项目是 Python 文字 MUD 原型，核心流程是“命令输入 -> 命令分发 -> 房间/战斗/背包状态更新”。
- 优先保证核心 API（战斗计算、物品交易、命令路由）可测试、可回归。

## 2) 技术栈与运行方式
- 语言：Python 3.12+
- 测试：pytest + pytest-cov
- 启动：`python src/main.py`
- 测试：`pytest tests -v`
- 覆盖率：`pytest tests --cov=src --cov-report=term-missing`

## 3) 目录结构与职责
- `src/main.py`：程序入口。
- `src/game_engine.py`：游戏状态机、世界初始化、主循环、命令解析。
- `src/command.py`：命令抽象与具体命令（look/move/get/drop/attack/status/help/quit）。
- `src/player.py`：玩家状态与行为（HP、背包、攻击计算）。
- `src/enemy.py`：敌人属性、受伤、反击、掉落判定。
- `src/room.py`：房间、出口、物品、敌人容器。
- `tests/`：单元测试与回归测试。
- `docs/`：课程报告与工程审计文档。

## 4) 核心模块约束（必须遵守）
- 战斗伤害必须保留下限：`max(1, damage - defense)`。
- 物品交易语义：
  - `get`：从房间移到玩家背包；
  - `drop`：从玩家背包移回房间。
- 命令类实现必须满足 `Command` 抽象接口：
  - `execute(game_engine) -> bool`
  - `get_name() -> str`
  - `get_description() -> str`
- 新增命令时，必须在 `GameEngine._init_commands()` 注册。

## 5) 编码规范
- 遵循 PEP8，函数短小、单一职责，避免深层嵌套。
- 新增逻辑优先补单元测试，尤其边界与异常路径。
- 不在业务代码中硬编码测试专用分支；测试应使用 monkeypatch/mock 控制随机性。
- 变更核心 API 时，先更新测试再改实现，保持回归通过。

## 6) AI 助手工作流程（建议）
- 第一步：阅读 `README.md` 与本文件，明确架构和边界。
- 第二步：定位目标模块（`command/player/enemy/room/game_engine`）。
- 第三步：先写失败测试（或补充边界测试），再修改实现。
- 第四步：运行 `pytest` 与覆盖率命令，确认回归。
- 第五步：在 `docs/` 更新对应实验/审计记录。

## 7) 禁止操作清单
- 禁止执行破坏性 Git 命令（如 `git reset --hard`、强制推送）。
- 禁止绕过测试直接“拍脑袋改逻辑”并提交。
- 禁止改动 `tests/` 来掩盖真实缺陷（删断言、放宽预期）而不说明原因。
- 禁止在未评估影响时重写 `main_game_loop` 交互流程。
- 禁止把临时调试输出长期留在核心模块中。

## 8) 提交前最小检查
- `pytest tests -v` 全通过。
- 核心 API（`command/player/enemy/room`）覆盖率目标 >= 80%。
- 文档与代码一致（命令名、目录、运行方式不冲突）。
