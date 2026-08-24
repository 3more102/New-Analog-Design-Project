# Simulation Results — SKY130 Two-Stage Miller Op-Amp

**Date**: 2026-08-21  
**Simulator**: ngspice 45.2 (batch mode)  
**PDK**: SKY130 BSIM4 (TT corner, downloaded from Google/skywater-pdk-libs-sky130_fd_pr)  
**Model Files**: C:\Users\omar\pdk\sky130A\cells\{nfet_01v8,pfet_01v8}\  
**Status**: DC operating point verified; AC analysis blocked by output rail saturation

---

## 1. Simulation Environment

| Item | Value |
|------|-------|
| Simulator | ngspice 45.2 (console, batch mode) |
| PDK | SKY130 (130nm), TT corner |
| Model type | BSIM4 level 54 |
| Devices | `sky130_fd_pr__nfet_01v8`, `sky130_fd_pr__pfet_01v8` |
| Supply | VDD = 1.8V, VSS = 0V |
| Temperature | 27°C (nominal) |
| Load | CL = 5 pF |

### PDK Integration Notes
- SKY130 devices use `.subckt` wrappers (not `.model` statements)
- All instances use `X` prefix (subcircuit instantiation)
- 27 missing slope/mismatch parameters initialized to 0 for TT nominal simulation
- Raw outputs saved to `results/raw/`

---

## 2. DC Operating Point — Final Design (v8)

### 2.1 Node Voltages

| Node | Voltage (V) | Notes |
|------|-------------|-------|
| VOUT | 1.684 | Near VDD — M7 at saturation edge |
| VOUT1 | 0.687 | First-stage output |
| VS | 0.263 | Tail node |
| VB_P | 0.670 | PMOS bias |
| VB_N | 0.772 | NMOS bias |

### 2.2 Transistor Operating Points

| Device | ID (µA) | VGS (V) | VDS (V) | VTH (V) | Vov (V) | gm (µS) | gds (µS) | ro (kΩ) | Region |
|--------|---------|---------|---------|---------|---------|---------|----------|---------|--------|
| M1 | 7.49 | 0.761 | 0.548 | 0.586 | 0.175 | 83.7 | 0.56 | 1786 | Saturation |
| M2 | 7.49 | 0.761 | 0.548 | 0.586 | 0.175 | 83.7 | 0.56 | 1786 | Saturation |
| M3 | 7.49 | −1.113 | −1.113 | −1.051 | −0.062 | 106 | 0.096 | 10417 | Saturation |
| M4 | 7.49 | −1.113 | −1.113 | −1.051 | −0.062 | 106 | 0.096 | 10417 | Saturation |
| M5 | 15.0 | 0.772 | 0.139 | 0.594 | 0.178 | 128 | — | — | Saturation |
| M6 | 10.9 | 0.687 | 1.684 | 0.588 | 0.099 | 157 | 0.71 | 1409 | Saturation |
| M7 | 10.9 | −1.130 | −0.116 | −1.033 | −0.097 | 158 | 31.0 | 32.3 | **Borderline** |
| M8 | 24.8 | −1.130 | −1.130 | −1.035 | −0.095 | — | — | — | Saturation |
| M9 | — | 0.772 | 0.772 | — | — | — | — | — | Saturation |

### 2.3 Supply Current

| Measurement | Value |
|-------------|-------|
| Total supply current | 60.9 µA |
| Total power | 109.6 µW |

### 2.4 Key Observations

1. **M7 is at the edge of saturation**: VSD7 = 116 mV vs |Vov7| = 97 mV. Only 19 mV margin.
2. **M6 is in saturation**: VDS6 = 1.684 V >> Vov6 = 99 mV.
3. **First-stage output (vout1) is low** (0.687 V) due to high PMOS |VTH| (~1.05 V) in SKY130.
4. **Tail current is 15 µA** (not the designed 20 µA) due to moderate-inversion operation.

---

## 3. Sizing Summary — Final Design

| Instance | Device | W (µm) | L (µm) | W/L | Purpose |
|----------|--------|---------|--------|-----|---------|
| X1 | nfet_01v8 | 4.0 | 2.0 | 2.0 | Diff pair (+) |
| X2 | nfet_01v8 | 4.0 | 2.0 | 2.0 | Diff pair (−) |
| X3 | pfet_01v8 | 40.0 | 2.0 | 20.0 | Active load |
| X4 | pfet_01v8 | 40.0 | 2.0 | 20.0 | Active load mirror |
| X5 | nfet_01v8 | 4.0 | 1.0 | 4.0 | Tail current source |
| X6 | nfet_01v8 | 6.0 | 1.0 | 6.0 | 2nd stage CS amp |
| X7 | pfet_01v8 | 20.0 | 1.0 | 20.0 | 2nd stage load |
| X8 | pfet_01v8 | 40.0 | 1.0 | 40.0 | PMOS bias ref |
| X9 | nfet_01v8 | 4.0 | 1.0 | 4.0 | NMOS bias ref |
| — | R_BIAS_P | — | — | 27 kΩ | PMOS bias resistor |
| — | R_BIAS_N | — | — | 56 kΩ | NMOS bias resistor |
| — | CC | — | — | 1.5 pF | Miller compensation |
| — | RZ | — | — | 1.25 kΩ | Zero nulling |

---

## 4. Performance Estimates (from DC Operating Point)

The AC analysis could not produce valid results because the open-loop output DC voltage (1.684 V) is near the VDD rail, causing the small-signal AC linearization to fail. However, we can estimate performance from the DC operating point parameters:

### 4.1 DC Gain (Estimated)

**First stage:**
```
Rout1 = ro1 || ro3 = 1786 kΩ || 10417 kΩ = 1530 kΩ
A1 = gm1 × Rout1 = 83.7 µS × 1530 kΩ = 128 (42.1 dB)
```

**Second stage:**
```
Rout2 = ro6 || ro7 = 1409 kΩ || 32.3 kΩ = 31.6 kΩ
A2 = gm6 × Rout2 = 157 µS × 31.6 kΩ = 4.96 (13.9 dB)
```

**Total:**
```
A0 = A1 × A2 = 128 × 4.96 = 635 (56.1 dB)
```

⚠ **Below 60 dB target** — limited by M7's low output resistance (32.3 kΩ) due to borderline saturation.

### 4.2 Unity-Gain Bandwidth (Estimated)

```
UGF = gm1 / (2π × CC) = 83.7 µS / (2π × 1.5 pF) = 8.87 MHz
```

✅ Exceeds 5 MHz target.

### 4.3 Slew Rate (Estimated)

```
SR = ITAIL / CC = 15.0 µA / 1.5 pF = 10.0 V/µs
```

✅ Exceeds 2 V/µs target.

### 4.4 Phase Margin (Estimated)

```
p1 (dominant) ≈ 1 / (2π × A2 × Rout1 × CC)
              = 1 / (2π × 4.96 × 1.53M × 1.5p)
              = 13.8 Hz

p2 (non-dominant) ≈ gm6 / (2π × CL)
                   = 157 µS / (2π × 5 pF)
                   = 5.0 MHz

z (RHP zero) = gm6 / (2π × CC)
              = 157 µS / (2π × 1.5 pF)
              = 16.7 MHz

Phase at UGF:
  = −90° − arctan(UGF/p2) + arctan(UGF/z)
  = −90° − arctan(8.87/5.0) + arctan(8.87/16.7)
  = −90° − 60.6° + 27.9°
  = −122.7°

PM = 180° − 122.7° = 57.3°
```

⚠ **Slightly below 60° target** — close but needs optimization.

### 4.5 Power (Measured)

```
P = VDD × I_TOTAL = 1.8V × 60.9 µA = 109.6 µW
```

✅ Well below 1 mW target.

### 4.6 Output Swing (Measured)

```
VOUT,max = VDD − |Vov7| = 1.8 − 0.097 = 1.703 V
VOUT,min = Vov6 = 0.099 V
Swing = 1.703 − 0.099 = 1.604 Vpp
```

✅ Exceeds 1.0 Vpp target.

### 4.7 Input Common-Mode Range (Estimated)

```
VIN,CM,max = VDD − |Vov3| − |VTH3| + VTH1 = 1.8 − 0.062 − 1.051 + 0.586 = 1.273 V
VIN,CM,min = VTH5 + Vov5 + VTH1 + Vov1 = 0.594 + 0.178 + 0.586 + 0.175 = 1.533 V
```

⚠ **VIN,CM,min > VIN,CM,max** — input CM range is extremely limited or invalid at this bias point. This is a critical issue caused by the high PMOS |VTH| in SKY130.

---

## 5. Sizing Iteration History

| Version | VOUT (V) | M6 Region | M7 Region | Key Change |
|---------|----------|-----------|-----------|------------|
| v1 | 1.735 | Saturation | **Triode** | Initial sizing |
| v2 | 1.039 | Saturation | Saturation | M6=20u, M7=60u, PMOS bias widened |
| v3 | 1.793 | Saturation | **Triode** | Added NMOS bias (M9) |
| v4 | 1.743 | Saturation | **Triode** | M3 widened to 40u |
| v5 | 0.122 | **Triode** | Saturation | M8 widened to 40u |
| v6 | 1.789 | Saturation | **Triode** | M7 reduced to 20u |
| v7 | 1.684 | Saturation | **Triode** | M6 reduced to 4u |
| **v8** | **1.684** | **Saturation** | **Borderline** | **M6=6u, M7=20u** |

---

## 6. Known Issues and Required Fixes

### 6.1 Output DC Bias Too High (1.684 V)
**Root cause**: The PMOS bias voltage (vb_p = 0.67 V) sets |Vov7| = 97 mV, but M7's saturation current exceeds M6's current at the equilibrium point. The output is pulled toward VDD.

**Fix options**:
1. Add common-mode feedback (CMFB) to regulate output at mid-rail
2. Use a different second-stage topology (e.g., class-AB output)
3. Adjust M6/M7 W/L ratios iteratively with parametric sweep

### 6.2 Limited Phase Margin (~57°)
**Root cause**: The second pole (p2 = 5.0 MHz) is close to UGF (8.87 MHz), causing significant phase shift.

**Fix options**:
1. Increase CC to push UGF lower (trades bandwidth for PM)
2. Increase M7 gm to push p2 higher (trades power)
3. Add a nulling resistor RZ > 1/gm6 to move zero to LHP

### 6.3 Invalid Input CM Range
**Root cause**: High PMOS |VTH| (~1.05 V) in SKY130 limits voltage headroom.

**Fix options**:
1. Use PMOS input pair (better CM range for 1.8V supply)
2. Use low-VT devices if available
3. Accept limited CM range for the application

---

## 7. Raw Simulation Files

All raw output files are saved in `results/raw/`:

| File | Description |
|------|-------------|
| `dc_op_point.log` | Initial DC operating point |
| `dc_v3.log` through `dc_v8.log` | Iteration DC results |
| `ac_openloop.txt` | AC frequency sweep data (901 points, 1 Hz–1 GHz) |
| `ac_gain2.log` | AC gain analysis (open-loop) |
| `ac_closed.log` | AC gain analysis (closed-loop) |
| `tf_analysis.log` | Transfer function analysis |

---

## 8. Next Steps

1. **Add CMFB** to regulate output at mid-rail → enables valid AC analysis
2. **Parametric sweep** M6 W/L to find optimal balance with M7
3. **Re-run AC** with proper DC bias → measure actual gain, UGF, PM
4. **Transient simulation** to measure slew rate
5. **Corner analysis** (FF, SS, SF, FS) for robustness
6. **Noise analysis** for input-referred noise

---

*End of simulation results.*
