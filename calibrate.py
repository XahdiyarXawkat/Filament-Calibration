"""
Filament-Calibration: 3D 打印耗材线径实时检测与流量校准
基于机器视觉在线测量 Filament 直径，输出流量补偿系数。

用法:
    python calibrate.py --camera 0              # 实时检测
    python calibrate.py --image sample.jpg      # 单张图片检测
"""

import argparse
import cv2
import numpy as np
from dataclasses import dataclass
from typing import Tuple


# ============================================================
# 配置参数（按实际硬件与场景调整）
# ============================================================
@dataclass
class Config:
    # 相机标定参数：像素到毫米的转换系数 (mm/pixel)
    pixel_to_mm: float = 0.01

    # 目标线径 (mm)，常见 1.75mm 或 2.85mm
    target_diameter: float = 1.75

    # 线径允许误差范围 (mm)
    tolerance: float = 0.05

    # 图像处理参数
    canny_low: int = 50
    canny_high: int = 150
    blur_kernel: int = 5

    # ROI 区域（图像中央竖条），None 表示全图
    roi_x_ratio: Tuple[float, float] = (0.3, 0.7)


def preprocess(frame: np.ndarray, cfg: Config) -> np.ndarray:
    """图像预处理：灰度化 → 高斯模糊 → Canny 边缘检测"""
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (cfg.blur_kernel, cfg.blur_kernel), 0)
    edges = cv2.Canny(blurred, cfg.canny_low, cfg.canny_high)
    return edges


def measure_diameter(edges: np.ndarray, cfg: Config) -> float:
    """
    基于边缘图像测量线径。
    在 ROI 区域扫描每行，计算左右边缘间距，取中位数作为直径（像素）。
    """
    h, w = edges.shape
    x_start = int(w * cfg.roi_x_ratio[0])
    x_end = int(w * cfg.roi_x_ratio[1])

    diameters_px = []
    for y in range(h):
        edge_points = np.where(edges[y, x_start:x_end] > 0)[0]
        if len(edge_points) >= 2:
            left = edge_points[0]
            right = edge_points[-1]
            diameters_px.append(right - left)

    if not diameters_px:
        return -1.0

    # 中位数滤波，抗噪声
    diameter_px = float(np.median(diameters_px))
    diameter_mm = diameter_px * cfg.pixel_to_mm
    return diameter_mm


def compute_flow_factor(measured_mm: float, cfg: Config) -> float:
    """根据实测线径计算流量补偿系数"""
    if measured_mm <= 0:
        return 1.0
    # 截面积比 = (目标半径²) / (实测半径²) = (目标直径 / 实测直径)²
    ratio = (cfg.target_diameter / measured_mm) ** 2
    # 限制合理范围，避免极端值
    ratio = np.clip(ratio, 0.8, 1.2)
    return round(ratio, 4)


def draw_overlay(frame: np.ndarray, edges: np.ndarray,
                 diameter_mm: float, flow_factor: float, cfg: Config):
    """在画面上叠加检测信息"""
    h, w = frame.shape[:2]
    x_start = int(w * cfg.roi_x_ratio[0])
    x_end = int(w * cfg.roi_x_ratio[1])

    # 绘制 ROI 竖线
    cv2.line(frame, (x_start, 0), (x_start, h), (255, 255, 0), 1)
    cv2.line(frame, (x_end, 0), (x_end, h), (255, 255, 0), 1)

    # 状态判断
    if diameter_mm < 0:
        status = "NO FILAMENT"
        color = (0, 0, 255)
    elif abs(diameter_mm - cfg.target_diameter) <= cfg.tolerance:
        status = "OK"
        color = (0, 255, 0)
    else:
        status = "OUT OF TOLERANCE"
        color = (0, 0, 255)

    # 文字叠加
    lines = [
        f"Diameter: {diameter_mm:.3f} mm",
        f"Target: {cfg.target_diameter} mm",
        f"Flow Factor: {flow_factor}",
        f"Status: {status}",
    ]
    for i, text in enumerate(lines):
        cv2.putText(frame, text, (10, 30 + i * 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)

    return frame


def run_realtime(camera_id: int = 0):
    """实时线径检测"""
    cfg = Config()
    cap = cv2.VideoCapture(camera_id)

    print("Filament 线径实时检测已启动，按 Q 退出")
    print(f"目标线径: {cfg.target_diameter}mm | 公差: ±{cfg.tolerance}mm")

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        edges = preprocess(frame, cfg)
        diameter_mm = measure_diameter(edges, cfg)
        flow_factor = compute_flow_factor(diameter_mm, cfg)
        frame = draw_overlay(frame, edges, diameter_mm, flow_factor, cfg)

        cv2.imshow("Filament Calibration", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


def run_image(image_path: str):
    """单张图片检测"""
    cfg = Config()
    frame = cv2.imread(image_path)
    if frame is None:
        print(f"无法读取图片: {image_path}")
        return

    edges = preprocess(frame, cfg)
    diameter_mm = measure_diameter(edges, cfg)
    flow_factor = compute_flow_factor(diameter_mm, cfg)
    frame = draw_overlay(frame, edges, diameter_mm, flow_factor, cfg)

    cv2.imshow("Filament Calibration", frame)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    print(f"实测线径: {diameter_mm:.3f} mm")
    print(f"流量补偿系数: {flow_factor}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Filament 线径检测与校准")
    parser.add_argument("--camera", type=int, default=0,
                        help="摄像头设备 ID")
    parser.add_argument("--image", type=str, default=None,
                        help="单张图片路径")
    args = parser.parse_args()

    if args.image:
        run_image(args.image)
    else:
        run_realtime(args.camera)
