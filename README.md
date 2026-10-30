# NMRiH 2 Mods

供 NModManager 读取的 NMRiH 2 Mod 清单和下载文件。

当前收录：

- **主菜单布局调整 v0.1**：调整主菜单的任务、难度和部署区布局。

## 在管理器中使用

在管理器点击「获取 Mod 清单」，选择需要的 Mod 并点击「下载」。文件经大小和 SHA-256 校验后进入管理器的 `mods` 目录，默认停用；勾选即可启用。要换下载源，可在「设置」中填写其他 HTTPS `catalog.json` 地址。

默认清单地址：`https://raw.githubusercontent.com/sfw222/nmrih2-mods/main/catalog.json`

## 仓库结构和更新

`mods/<id>/<version>/` 存放一版 Mod 的 `manifest.json` 和 `.pak` / `.utoc` / `.ucas` 文件。发布新版时新增版本目录，保留旧版文件；清单只列每个 Mod 版本号最高的一版。

```powershell
python -B tools/build_catalog.py
```

该命令逐个核对文件 SHA-256 和 manifest，然后重建根目录的 `catalog.json`。提交新版前应运行它，确保下载清单与实际文件一致。

这些 Mod 适配 NMRiH 2 **1.2.0 / build 512035**。使用前确认游戏版本匹配；请勿在游戏运行时启停 Mod。
