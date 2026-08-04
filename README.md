---
AIGC:
    Label: "1"
    ContentProducer: 001191440300708461136T1XGW3
    ProduceID: 7589fcd80e824c73956dea0adfc2a253_1b80d25868a811f1aa625254006c9bbf
    ReservedCode1: wf4iqQzc4PcDjFM0E0NXyLkJrGJbiK+0LEQosWRnkaR0d0SGg4979sIiVYpXAevVb+aqFkQu2gKOGxKGawXX0gWfAhuHWepDOY4NQLuBq88P1sHNo5O98i5Uotq945vpO4Pce5MMEufeoT8Gp+blT3uGlCtZvnmGA0+0MSk0oFF3bNYCK160y8fw5uQ=
    ContentPropagator: 001191440300708461136T1XGW3
    PropagateID: 7589fcd80e824c73956dea0adfc2a253_1b80d25868a811f1aa625254006c9bbf
    ReservedCode2: wf4iqQzc4PcDjFM0E0NXyLkJrGJbiK+0LEQosWRnkaR0d0SGg4979sIiVYpXAevVb+aqFkQu2gKOGxKGawXX0gWfAhuHWepDOY4NQLuBq88P1sHNo5O98i5Uotq945vpO4Pce5MMEufeoT8Gp+blT3uGlCtZvnmGA0+0MSk0oFF3bNYCK160y8fw5uQ=
---



# Filament-Calibration

3D 打印耗材质量监控与校准系统。基于机器视觉实现 Filament 线径实时检测与流量校准算法，通过视觉反馈动态调整挤出机参数，实现废料回收再生过程的闭环控制。

> **实习项目**：Resinlab (3D 打印初创公司) | 硬件与视觉算法实习生 | 2026.02 – 2026.08

---

## 🎯 核心指标

| 指标 | 数值 |
|------|------|
| 线径检测精度 | ≤0.05mm |
| 检测方式 | 机器视觉实时在线检测 |
| 控制方式 | 视觉反馈闭环调整挤出机 |

## 🔧 功能列表

| 功能 | 说明 | 状态 |
|------|------|------|
| 流量校准 | 测量实际挤出倍率，自动生成补偿系数 | ✅ |
| 温度塔 | 生成多段温控 G-code，辅助选定最佳打印温度 | ✅ |
| 回抽调优 | 自动生成不同回抽距离/速度的测试模型 | ✅ |
| 线性推进 | K-factor 校准塔生成 | [待补充] |

---

## 📸 校准前后对比

| 校准前 | 校准后 |
|--------|--------|
| ![校准前](<img width="1206" height="2622" alt="968eebb70b9200f0e81452dd13c41309" src="https://github.com/user-attachments/assets/da8a555d-cd22-4e12-b76e-dfa1938263ff" />) | ![校准后](<img width="1206" height="2622" alt="968eebb70b9200f0e81452dd13c41309" src="https://github.com/user-attachments/assets/ec55a7e2-1f5d-4935-99e1-28ca67a29f36" />
) |

*[待补充：替换为实际打印对比图]*

---

## 🚀 快速开始

### 安装

```bash
git clone https://github.com/XahdiyarXawkat/Filament-Calibration.git
cd Filament-Calibration
pip install -r requirements.txt
```

### 流量校准

```bash
python calibrate_flow.py --filament PLA --nozzle 0.4 --layer_height 0.2
```

### 温度塔

```bash
python temp_tower.py --start 220 --end 190 --step 5 --filament PLA
```

---

## 📋 推荐参数参考

| 材料 | 喷嘴温度 (°C) | 热床温度 (°C) | 流量倍率 | 回抽距离 (mm) | 回抽速度 (mm/s) |
|------|--------------|--------------|---------|--------------|----------------|
| PLA | 200-210 | 50-60 | 0.98-1.02 | 0.8-1.2 | 35-45 |
| PETG | 230-245 | 70-80 | 0.95-1.00 | 1.0-1.5 | 30-40 |
| ABS | 240-260 | 90-100 | 0.97-1.02 | 1.0-1.5 | 40-50 |
| TPU | 220-235 | 40-50 | 1.00-1.05 | 1.5-2.5 | 20-30 |

---

## 📄 License

MIT License
*（内容由AI生成，仅供参考）*
*（内容由AI生成，仅供参考）*
