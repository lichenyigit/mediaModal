# mediaModal
多媒体遮幕

一个基于PyQt6的透明遮罩工具，可以创建可拖动的半透明覆盖层。

## 功能特性

- 🖱️ 可拖动的透明窗口
- 📏 可调整大小的覆盖层
- 🎯 始终置顶显示
- 🖼️ 自定义图标支持
- ⚡ 流畅的交互体验


1. **打包命令**：
```bash
pip install -r requirements.txt
pip install pyinstaller
# 完整打包（包含所有依赖）
pyinstaller --onefile --windowed --icon=modal.ico --name=MediaModal-v1.0  --strip --hidden-import=PyQt6 --hidden-import=pkgutil --hidden-import=QtCore mediaModal.py
```

### 打包选项说明

- `--onefile`: 打包为单个可执行文件
- `--windowed`: 不显示控制台窗口
- `--icon=modal.ico`: 设置程序图标
- `--strip`: 移除调试信息，减小文件大小
- `--hidden-import=PyQt6`: 确保PyQt6模块被包含

### 生成的文件

打包完成后，可执行文件将生成在 `dist/` 目录中：
- `overlay.exe` (Windows)
- `overlay` (Linux/macOS)

## 使用说明

1. 运行程序后会出现一个黑色半透明条
2. 可以拖动窗口到任意位置
3. 右下角可以调整窗口大小
4. 双击窗口可以切换置顶状态
5. 点击右上角的 × 按钮关闭程序

## 文件结构

```
100top/
├── overlay.py          # 主程序文件
├── modal.ico          # 程序图标
├── requirements.txt    # 依赖列表
├── build.py           # 自动打包脚本
├── README.md          # 说明文档
└── dist/              # 打包输出目录
    └── overlay.exe    # 可执行文件
```

## 系统要求

- Python 3.7+
- PyQt6
- Windows/Linux/macOS

## 注意事项

- 程序需要图形界面支持
- 某些系统可能需要管理员权限运行
- 建议在打包前测试程序功能正常
