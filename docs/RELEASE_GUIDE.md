# SubtitleMasker 发布指南

本文档用于后续发布新版本时参考。

## 1. 修改版本号

在 `src/subtitle_masker/version.py` 中更新：

```python
APP_VERSION = "1.0.0"
APP_RELEASE_CHANNEL = "stable"
```

常见发布通道：

- `stable`：稳定版
- `beta`：测试版
- `dev`：开发版

## 2. 更新 CHANGELOG

在 `CHANGELOG.md` 顶部新增版本记录，建议格式：

```markdown
## v1.1.0

- 新增：...
- 修复：...
- 调整：...
```

发布前确认 README 中的当前版本号也已同步。

## 3. 执行基础检查

运行：

```powershell
.\scripts\check.ps1
```

确认所有 Python 文件可以通过 `py_compile`。

## 4. 打包 exe

如果需要发布 exe，先在开发环境中准备 PyInstaller。项目不会在脚本中强制安装 PyInstaller。

运行：

```powershell
.\scripts\build_exe.ps1
```

打包产物通常位于：

```text
dist\
```

## 5. 生成发布 zip

运行：

```powershell
.\scripts\make_release.ps1
```

脚本会创建：

```text
release\SubtitleMasker-v版本号.zip
```

如果已经存在 `dist` 打包产物，脚本会优先打包 exe 产物；否则会创建源码版发布包。

## 6. 发布前检查

发布前建议确认：

- 软件可以正常启动。
- 右键菜单、锁定、透明度、恢复默认设置可用。
- `README.md` 和 `README.txt` 中的版本号正确。
- `CHANGELOG.md` 已记录当前版本。
- 发布包中不包含 `.venv`、`__pycache__`、临时文件。
