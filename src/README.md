# 文字 MUD 游戏 - 核心引擎

## 项目概述
这是一个基于控制台的文字冒险游戏，实现了命令模式架构的 MUD（Multi-User Dungeon）核心引擎。

## 核心功能
- ✅ 完整的游戏主循环（main_game_loop）
- ✅ 房间系统（Room 类）
- ✅ 玩家系统（Player 类）
- ✅ 命令模式（Command 基类及具体命令）
- ✅ 支持的指令：
  - `look` - 查看当前房间信息
  - `move [direction]` - 向指定方向移动（north/south/east/west）
  - `help` - 显示所有可用命令
  - `quit` - 退出游戏

## 技术架构
- **设计模式**: 命令模式（Command Pattern）
- **语言**: Python 3.x
- **硬性约束**: 无 GUI，无网络通信（纯控制台交互）

## 运行方法
```bash
python src/main.py
```

## 核心类说明

### Room 类
- 管理房间的名称、描述、出口和物品
- 提供房间连接和物品管理功能

### Player 类
- 管理玩家状态和背包
- 维护当前位置信息

### GameEngine 类
- 游戏主控制器
- 处理命令解析和分发
- 管理游戏循环

### Command 基类
- 抽象命令接口
- 具体命令实现继承此类

## 下一步扩展建议
1. 添加更多命令（get、drop、use、inventory 等）
2. 实现物品交互系统
3. 添加游戏状态持久化
4. 创建更复杂的地图系统