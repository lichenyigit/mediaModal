# mediaModal
多媒体遮幕

一个基于PyQt6的透明遮罩工具，可以创建可拖动的半透明覆盖层。

## 功能特性

- 🖱️ 可拖动的透明窗口
- 📏 可调整大小的覆盖层
- 🎯 始终置顶显示
- 🖼️ 自定义图标支持
- ⚡ 流畅的交互体验
- 🔄 每0.1秒检测窗口前台状态
- 🔄 可配置的圆角窗口
- ⚙️ 配置文件支持

## 安装依赖

```bash
pip install -r requirements.txt
```

## 运行程序

```bash
python mediaModal.py
```

## 打包为可执行文件
1. **安装PyInstaller**：
```bash
pip install pyinstaller
```

2. **打包命令**（修复DLL问题）：
```bash
pyinstaller --onefile --windowed --icon=modal.ico --name="MediaModal-v1.2" --collect-all PySide6 mediaModal.py
```


## 使用说明

1. 运行程序后会出现一个黑色半透明条
2. 可以拖动窗口到任意位置
3. 右下角可以调整窗口大小
4. 双击窗口可以切换置顶状态
5. 点击右上角的 × 按钮关闭程序
6. 程序会自动检测窗口是否在最前面，并在控制台输出状态变化

## 配置文件

程序使用 `config.json` 配置文件，可以自定义以下参数：

### 前台检测配置
```json
{
    "front_detection": {
        "interval_ms": 100,    // 检测间隔（毫秒）
        "enabled": true,       // 是否启用检测
        "log_enabled": true    // 是否输出日志
    }
}
```

### 窗口配置
```json
{
    "window": {
        "default_width": 800,      // 默认宽度
        "default_height": 50,      // 默认高度
        "min_width": 200,          // 最小宽度
        "min_height": 50,          // 最小高度
        "position": {
            "x": "center",         // 水平位置
            "y": "bottom",         // 垂直位置
            "margin_bottom": 50    // 底部边距
        },
        "rounded_corners": {
            "enabled": true,       // 是否启用圆角
            "radius": 10           // 圆角半径
        }
    }
}
```

### UI配置
```json
{
    "ui": {
        "close_button_size": 30,           // 关闭按钮大小
        "resize_margin": 10,               // 调整大小区域边距
        "resize_indicator_size": 8,        // 调整大小指示器大小
        "show_resize_indicator": false     // 是否显示调整大小指示器
    }
}
```

## 文件结构

```
100top/
├── mediaModal.py        # 主程序文件
├── config.json         # 配置文件
├── modal.ico           # 程序图标
├── requirements.txt     # 依赖列表
├── README.md           # 说明文档
└── dist/               # 打包输出目录
    └── MediaModal-v1.4.exe  # 可执行文件
```

## 系统要求

- Python 3.7+
- PyQt6
- Windows/Linux/macOS

## 注意事项

- 程序需要图形界面支持
- 某些系统可能需要管理员权限运行
- 建议在打包前测试程序功能正常
- 如果遇到DLL错误，请使用修复版打包脚本
- 修改配置文件后需要重启程序才能生效
