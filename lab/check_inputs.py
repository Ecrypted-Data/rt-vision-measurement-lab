"""从仓库根目录运行 python -m lab.check_inputs。"""

import argparse
import sys

import cv2

from .inputs import (
    BOARD_CHECK_FRAMES, BOARD_START, BOARD_STOP, board_frames,
    vehicle_case_files, vehicle_frames,
)


def check_board():
    selected_for_calibration = sum(1 for _ in board_frames(0, BOARD_START))
    if selected_for_calibration != BOARD_START:
        raise ValueError("标定取材的前 7 秒视频缺帧")
    seen = []
    count = 0
    for index, time_s, image in board_frames():
        count += 1
        if image.shape[:2] != (360, 640):
            raise ValueError(f"棋盘格第 {index} 帧尺寸不是 640×360")
        if index in BOARD_CHECK_FRAMES:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            found, corners = cv2.findChessboardCornersSB(gray, (9, 6))
            if not found or len(corners) != 54:
                raise ValueError(f"验收帧 {index} 未检出完整棋盘格")
            seen.append(f"{time_s:.1f} 秒")
    if count != BOARD_STOP - BOARD_START or len(seen) != len(BOARD_CHECK_FRAMES):
        raise ValueError("棋盘格片段缺帧")
    print(f"任务一通过：标定取材 {selected_for_calibration} 帧和回放 {count} 帧可读取；{'、'.join(seen)}分别找到 54 个内角点")


def check_vehicle(case: str, count: int, hidden: range):
    folder = vehicle_case_files(case)
    frames = vehicle_frames(case, folder)
    if [f.index for f in frames] != list(range(count)):
        raise ValueError(f"车辆 {case} 帧表的帧号不连续")
    if [f.index for f in frames if f.blackout] != list(hidden):
        raise ValueError(f"车辆 {case} 黑屏帧号与任务不符")
    if any(f.blackout and f.candidates for f in frames):
        raise ValueError(f"车辆 {case} 黑屏帧包含检测框")
    if not frames[0].candidates or not frames[hidden.stop].candidates:
        raise ValueError(f"车辆 {case} 首帧或恢复帧缺少候选框")
    if any(right.time_s <= left.time_s for left, right in zip(frames, frames[1:])):
        raise ValueError(f"车辆 {case} 帧表的时间没有单调递增")
    for kind in ("clean", "blackout"):
        reader = cv2.VideoCapture(str(folder / f"{case}_{kind}.mp4"))
        try:
            decoded = 0
            for frame in frames:
                ok, image = reader.read()
                if not ok or image.shape[:2] != (720, 1280):
                    raise ValueError(f"车辆 {case} 的 {kind} 片段长度或尺寸错误")
                if kind == "blackout" and bool(image.max() < 4) != frame.blackout:
                    raise ValueError(f"车辆 {case} 画面和黑屏标记不一致")
                decoded += 1
            if decoded != count or reader.read()[0]:
                raise ValueError(f"车辆 {case} 的 {kind} 片段有多余帧")
        finally:
            reader.release()
    print(f"任务二 {case.upper()} 通过：{count} 帧；其中 {len(hidden)} 帧连续黑屏")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--task", choices=("1", "2", "all"), default="all")
    args = parser.parse_args()
    try:
        if args.task in ("1", "all"):
            check_board()
        if args.task in ("2", "all"):
            check_vehicle("a", 36, range(12, 20))
            check_vehicle("b", 37, range(10, 18))
    except (OSError, ValueError, KeyError, cv2.error) as error:
        print(f"检查失败：{error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
