# RT 视觉测量与状态估计

这是视觉组本节培训的起始仓库。仓库提供实拍素材、相机标定、车辆候选框和数据读入代码。需要完成的两项任务分别是棋盘格视频中的立方体投影，以及短时黑屏后的车辆追踪。

## 开始练习

先 Fork 本仓库，克隆自己的 Fork 后，在仓库的根目录新建工作分支。已经能在 WSL 的 Python 中导入 OpenCV 和 NumPy 时，直接运行素材检查。

```bash
python3 -m lab.check_inputs
```

如果现有环境缺少依赖，可在仓库根目录准备一个项目环境。

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m lab.check_inputs
```

通过时会看到任务一的 264 帧和两张棋盘格验收帧，以及任务二的 A、B 两段各 8 帧的黑屏检查。检查命令只检验素材和读入流程。每项任务的实现和结果需要自行完成。

## 从哪里开始

| 用途 | 入口 |
| --- | --- |
| 了解算法并跟做示范 | [飞书《视觉测量与状态估计》](https://gcnhkq914dqv.feishu.cn/wiki/Jyb1we3zQiWfZlk3G8ucBJgFnbg) |
| 在棋盘格视频中动态叠加立方体 | [任务一](task1/) |
| 用两辆车验证黑屏期间及恢复后的估计 | [任务二](task2/) |
| 读取视频、标定和逐帧检测框 | [素材读取模块](lab/inputs.py) |

`assets/` 是仓库提供的素材。运行和生成的中间文件放到 `work/`。把需要提交的影像、表格和说明放到 `results/` 或在自己的 README 中给出清楚的访问链接。最后提交工作分支或 PR 链接。
