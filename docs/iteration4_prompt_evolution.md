# 迭代 4：AI 辅助测试 Prompt 演化实验报告

## 一、实验目标
- 使用 AI 辅助编写核心 API（战斗计算、物品交易）的 Mock 单元测试。
- 记录 Prompt 演化：初始 Prompt -> 输出问题 -> 改进 Prompt -> 最终可用测试。
- 验证核心 API 覆盖率 >= 80%。

## 二、实验对象与范围
- 代码范围：`src/command.py`、`src/player.py`、`src/enemy.py`、`src/room.py`
- 测试文件：`tests/test_core_api_mock.py`、`tests/test_commands.py`

---

## 案例 A：战斗计算（AttackCommand + Player/Enemy）

### A1. 初始 Prompt（失败版本）
> “请为 attack 命令写几个 pytest 测试，覆盖正常攻击流程。”

### A2. AI 初始输出问题
- 只覆盖“击杀成功”主路径，忽略“敌人不存在/玩家被反杀/低血量恢复”等边界。
- 断言偏弱，只断 `True/False`，未验证房间掉落、玩家血量变化等状态。
- 对随机数未做控制，测试不稳定（偶发失败）。

### A3. 改进 Prompt（结构化 + Few-shot + 角色）
> “你是资深测试工程师，请为 `AttackCommand.execute` 设计**稳定**的 pytest 测试。  
> 约束：  
> 1) 必须用 `monkeypatch` 固定 `random.randint`；  
> 2) 至少覆盖 4 条路径：无敌人、击杀掉落、敌人反击致死、低血量击杀后恢复；  
> 3) 每条测试断言‘返回值 + 关键状态变化 + 输出关键词’；  
> 4) 参考风格（few-shot）：`assert room.enemy is None`、`assert "金币" in room.items`、`assert player.hp == 40`。  
> 输出仅给 pytest 代码，不解释。”

### A4. 最终可用产出（落地）
- `test_attack_command_handles_no_enemy_and_dead_enemy`
- `test_attack_command_enemy_counterattack_can_end_game`
- `test_attack_command_low_hp_bonus_recovery`
- `test_player_and_enemy_damage_boundaries`

改进效果：
- 随机因素被 Mock，测试稳定。
- 增加了关键边界覆盖，能识别战斗流程回归风险。

---

## 案例 B：物品交易（GetCommand / DropCommand）

### B1. 初始 Prompt（失败版本）
> “给 get 和 drop 写测试，验证物品可以被拿起和丢弃。”

### B2. AI 初始输出问题
- 倾向“重言式测试”：只验证“拿了之后在背包里”，缺少输入非法/物品不存在场景。
- 忽略业务规则：“有敌人时不可拾取（火把例外）”。
- 没有验证提示信息，难以保障交互反馈一致性。

### B3. 改进 Prompt（CoT 风格拆解 + 约束）
> “请按‘输入校验 -> 业务规则 -> 状态迁移’链路设计测试。  
> 模块：`GetCommand.execute`、`DropCommand.execute`。  
> 必测：  
> - 缺少参数；  
> - 物品不存在；  
> - 玩家没有该物品时 drop；  
> - 有敌人时 get 非火把失败（火把成功，作为对照）；  
> 每个测试都要检查：返回值、背包/房间状态、输出文案关键字。  
> 只输出 pytest 代码。”

### B4. 最终可用产出（落地）
- `test_get_command_blocks_pickup_when_enemy_present_except_torch`（已有）
- `test_get_command_missing_or_absent_item`（新增）
- `test_drop_command_missing_or_absent_item`（新增）

改进效果：
- 从“功能演示”升级为“规则验证”。
- 明确覆盖输入校验与边界，减少线上命令语义回归。

---

## 三、覆盖率结果（核心 API）

执行命令：
```bash
pytest tests --cov=src --cov-report=term-missing
```

本次结果（节选）：
- `src/command.py`: 90%
- `src/enemy.py`: 93%
- `src/player.py`: 78%
- `src/room.py`: 87%

按核心 API 模块（`command/player/enemy/room`）汇总覆盖率约为 **87.7%**（>= 80%）。

> 覆盖率截图提交说明：请将本地终端截图保存为 `docs/assets/coverage-iteration4.png` 并随报告提交。

## 四、结论
- Prompt 从“自然语言泛化指令”演化为“结构化约束 + few-shot 示例 + 角色化要求”后，测试可用性与边界覆盖显著提升。
- 本次产出可直接作为迭代 4 的“Prompt 演化实验”书面证据与工程证据。
