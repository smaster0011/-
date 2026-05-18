# Release Checklist

发布前请逐项确认。

## 版本信息

- [ ] `src/subtitle_masker/version.py` 中的 `APP_VERSION` 已更新。
- [ ] `README.md` 和 `README.txt` 中的版本号已更新。
- [ ] `CHANGELOG.md` 已记录当前版本变化。
- [ ] 发布通道 `APP_RELEASE_CHANNEL` 正确。

## 文档

- [ ] README 说明了软件用途：遮挡屏幕字幕，辅助语言学习或演示遮罩。
- [ ] README 说明软件不提供、不下载、不传播任何影视资源。
- [ ] README 说明用户应自行确保观看内容来源合法。
- [ ] 隐私文档说明当前版本不联网、不采集数据、不读取浏览器内容、不识别屏幕内容、不保存观看记录。
- [ ] 文档说明只在本地保存窗口位置、大小、透明度、颜色、锁定状态等配置。
- [ ] 文档说明未签名 exe 可能被 Windows 提示未知发布者。
- [ ] 文档说明播放器独占全屏时可能无法遮挡，可改用窗口化全屏或浏览器播放。

## 基础检查

- [ ] 运行基础检查：

```powershell
.\scripts\check.ps1
```

- [ ] 确认程序可以正常启动。
- [ ] 确认右键菜单、透明度、锁定/解锁、恢复默认设置可用。
- [ ] 确认 Esc 可以退出。

## 打包

- [ ] 如需 exe，确认 PyInstaller 已在开发环境中可用。
- [ ] 运行：

```powershell
.\scripts\build_exe.ps1
```

- [ ] 运行：

```powershell
.\scripts\make_release.ps1
```

- [ ] 确认发布 zip 中不包含 `.venv`、`__pycache__`、临时文件或个人路径。

## 发布

- [ ] 上传 zip 或 exe 到发布页面。
- [ ] 发布页说明当前版本号、主要变化和已知限制。
- [ ] 发布页提醒：未签名 exe 可能显示未知发布者。
- [ ] 发布页提醒：用户应自行确保观看内容来源合法。
