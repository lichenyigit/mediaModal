# mediaModal
多媒体遮幕

一个基于PyQt6的透明遮罩工具，可以创建可拖动的半透明覆盖层。

## 功能特性

- 🖱️ 可拖动的透明窗口
- 📏 可调整大小的覆盖层
- 🎯 始终置顶显示
- 🖼️ 自定义图标支持
- ⚡ 流畅的交互体验

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
pyinstaller --onefile --windowed --icon=modal.ico --name="MediaModal-v1.1" --collect-all PySide6 mediaModal.py
```


## 使用说明

1. 运行程序后会出现一个黑色半透明条
2. 可以拖动窗口到任意位置
3. 右下角可以调整窗口大小
4. 双击窗口可以切换置顶状态
5. 点击右上角的 × 按钮关闭程序

## 文件结构

```
100top/
├── mediaModal.py        # 主程序文件
├── modal.ico           # 程序图标
├── requirements.txt     # 依赖列表
├── build_fixed.py      # 修复版打包脚本
├── README.md           # 说明文档
└── dist/               # 打包输出目录
    └── MediaModal-v1.0.exe  # 可执行文件
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
