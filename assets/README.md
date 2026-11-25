# 本节素材

| 文件 | 用途 |
| --- | --- |
| `chessboard_104435_preview.mp4` | 640×360、24 fps 的实拍棋盘格视频。角点提取、标定和位姿示范及任务一共用一段视频。棋盘格实际格长 20 mm。 |
| `task2_vehicle_materials.zip` | 任务二的两个黑屏片段、逐帧对齐的清晰版、帧表和未关联的车辆候选框。 |
| `task2_targets.jpg` | A、B 两个片段第 0 帧的目标车辆示意。 |
| `vehicle_demo_blackout.mp4` | 白车回放短片，共 51 帧。短片第 0 帧对应原片第 624 帧。 |
| `vehicle_center_observations_blackout.csv` | 白车回放的输入表。原片第 645–649 帧只保留帧号与时间。 |
| `vehicle_demo_source.mp4`、`vehicle_center_observations.csv` | 白车实拍原片和 51 帧的完整观测表，供对照两种输入。 |

从仓库根目录运行 `python3 -m lab.check_inputs` 检查两项任务的素材。任务二可以通过 `lab.inputs.vehicle_case_files("a")` 或 `lab.inputs.vehicle_case_files("b")` 把对应片段解包到 `work/vehicle_inputs/`。
