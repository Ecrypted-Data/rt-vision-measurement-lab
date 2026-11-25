# RT 视觉测量与状态估计

本节的两项任务共用这个仓库。任务一在实拍棋盘格视频上叠加立方体并测距，任务二在车流片段中估计指定车辆的轨迹。

## 开始练习

1. 用你的 GitHub 账号打开仓库并 Fork，再在 WSL Ubuntu 中克隆自己的 Fork。
2. 进入仓库根目录，按下方说明检查素材。
3. 按[《开发管理》](https://gcnhkq914dqv.feishu.cn/wiki/Joxswv4PziPcdCkVL0McQKnhnAg)创建工作分支。

已有能运行 OpenCV、NumPy 和 Matplotlib 的 Python 环境可以继续使用。

```bash
python3 -c "import cv2, numpy, matplotlib"
python3 -m lab.check_inputs
```

缺少依赖时，可以用项目虚拟环境安装。WSL Ubuntu 若提示缺少 `ensurepip`，先安装 `python3-venv`。

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m lab.check_inputs
```

检查通过时，可读取任务一的 264 帧和两张验收帧，并能解包、读取任务二两个片段及其各 8 帧连续黑屏。检查命令验证素材与读取入口。

## 任务与素材

- [飞书《视觉测量与状态估计》](https://gcnhkq914dqv.feishu.cn/wiki/Jyb1we3zQiWfZlk3G8ucBJgFnbg)可先阅读原理和实拍示范，从「三、培训任务」开始动手。
- [任务一及测量记录模板](task1/)
- [任务二及验收记录模板](task2/)
- [素材清单](assets/)和[素材读取模块](lab/inputs.py)

运行产物可放在本地的 `work/`。在你自己的 README 中说明使用的输入、复跑命令和结果。需提交的文件可放到 `results/` 或给出评审人可直接访问的链接。最后提交工作分支链接。
