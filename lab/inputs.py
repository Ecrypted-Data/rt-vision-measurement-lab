"""读取棋盘格视频、相机参数和车辆逐帧观测。"""

import csv
from dataclasses import dataclass
from pathlib import Path
from shutil import copyfileobj
from zipfile import ZipFile

import cv2
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
WORK = ROOT / "work"
BOARD_VIDEO = ASSETS / "chessboard_104435_preview.mp4"
VEHICLE_ARCHIVE = ASSETS / "task2_vehicle_materials.zip"

BOARD_START = 168
BOARD_STOP = 432
BOARD_CHECK_FRAMES = (180, 420)


@dataclass(frozen=True)
class Calibration:
    matrix: np.ndarray
    distortion: np.ndarray
    image_size: tuple[int, int]
    square_size_m: float


@dataclass(frozen=True)
class Detection:
    xyxy: tuple[float, float, float, float]
    confidence: float

    @property
    def center(self) -> tuple[float, float]:
        x1, y1, x2, y2 = self.xyxy
        return (x1 + x2) / 2, (y1 + y2) / 2


@dataclass(frozen=True)
class TrackingFrame:
    index: int
    source_index: int
    time_s: float
    blackout: bool
    candidates: tuple[Detection, ...]


def load_calibration(path: str | Path) -> Calibration:
    """读取学员提供的相机内参、畸变系数和标定尺寸。"""
    with np.load(path, allow_pickle=False) as data:
        matrix = data["K"]
        distortion = data["dist"]
        width, height = (int(value) for value in data["image_size"])
        square_size_m = float(data["square_size_m"].item())
    if matrix.shape != (3, 3) or not np.isfinite(matrix).all():
        raise ValueError("相机矩阵应为有限的 3×3 数组")
    if not np.isfinite(distortion).all() or square_size_m <= 0:
        raise ValueError("畸变系数或格长无效")
    return Calibration(matrix, distortion, (width, height), square_size_m)


def board_frames(start: int = BOARD_START, stop: int = BOARD_STOP):
    """依次返回原片帧号、秒数、BGR 图像。stop 为结束后的帧号。"""
    video = cv2.VideoCapture(str(BOARD_VIDEO))
    try:
        if not video.isOpened():
            raise OSError(f"无法打开视频 {BOARD_VIDEO.relative_to(ROOT)}")
        fps = video.get(cv2.CAP_PROP_FPS)
        if fps <= 0 or not video.set(cv2.CAP_PROP_POS_FRAMES, start):
            raise ValueError("无法定位棋盘格视频的起始帧")
        for index in range(start, stop):
            ok, frame = video.read()
            if not ok:
                raise ValueError(f"棋盘格第 {index} 帧无法解码")
            yield index, index / fps, frame
    finally:
        video.release()


def vehicle_case_files(case: str) -> Path:
    """将指定车辆的素材解包到 work/vehicle_inputs/。"""
    if case not in ("a", "b"):
        raise ValueError("片段编号使用 a 或 b")
    folder = WORK / "vehicle_inputs"
    folder.mkdir(parents=True, exist_ok=True)
    suffixes = ("blackout.mp4", "clean.mp4", "frames.csv", "candidates.csv")
    with ZipFile(VEHICLE_ARCHIVE) as archive:
        for suffix in suffixes:
            name = f"{case}_{suffix}"
            with archive.open(name) as source, (folder / name).open("wb") as dest:
                copyfileobj(source, dest)
    return folder


def vehicle_frames(case: str, folder: Path) -> list[TrackingFrame]:
    """保留没有候选框的帧，并用片段内帧号对齐两个 CSV。"""
    candidates: dict[int, list[Detection]] = {}
    with (folder / f"{case}_candidates.csv").open(encoding="utf-8", newline="") as file:
        for row in csv.DictReader(file):
            frame = int(row["frame"])
            xyxy = (
                float(row["x1_px"]), float(row["y1_px"]),
                float(row["x2_px"]), float(row["y2_px"]),
            )
            candidates.setdefault(frame, []).append(Detection(xyxy, float(row["confidence"])))
    frames = []
    with (folder / f"{case}_frames.csv").open(encoding="utf-8", newline="") as file:
        for row in csv.DictReader(file):
            index = int(row["frame"])
            frames.append(TrackingFrame(
                index, int(row["source_frame"]), float(row["time_s"]),
                bool(int(row["blackout"])), tuple(candidates.pop(index, ())),
            ))
    if candidates:
        raise ValueError(f"片段 {case} 有候选框的帧号超出帧表")
    return frames
