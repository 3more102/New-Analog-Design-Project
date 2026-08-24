# Hand Calculations — SKY130 Two-Stage Miller-Compensated CMOS Op-Amp

**Date**: 2026-08-21  
**Author**: Buffy (design agent)  
**Revision**: 1.0

---

## Table of Contents

1. [Design Specifications](#1-design-specifications)
2. [SKY130 PDK Parameters](#2-sky130-pdk-parameters)
3. [Topology Explanation](#3-topology-explanation)
4. [Operating Regions](#4-operating-regions)
5. [Bias Current Selection](#5-bias-current-selection)
6. [Overdrive Voltage Assumptions](#6-overdrive-voltage-assumptions)
7. [Transconductance Requirements](#7-transconductance-requirements)
8. [First-Stage Gain](#8-first-stage-gain)
9. [Second-Stage Gain](#9-second-stage-gain)
10. [Total DC Gain Estimate](#10-total-dc-gain-estimate)
11. [Miller Compensation Capacitor Calculation](#11-miller-compensation-capacitor-calculation)
12. [Pole/Zero Analysis](#12-polezero-analysis)
13. [Unity-Gain Bandwidth Estimate](#13-unity-gain-bandwidth-estimate)
14. [Phase Margin Considerations](#14-phase-margin-considerations)
15. [Slew-Rate Calculation](#15-slew-rate-calculation)
16. [Output Swing and Voltage Requirements](#16-output-swing-and-voltage-requirements)
17. [Input Common-Mode Range](#17-input-common-mode-range)
18. [Output-Current Requirements](#18-output-current-requirements)
19. [Power Estimate](#19-power-estimate)
20. [Noise Considerations](#20-noise-considerations)
21. [CMRR and PSRR Estimates](#21-cmrr-and-psrr-estimates)
22. [Sensitivity and Trade-Off Discussion](#22-sensitivity-and-trade-off-discussion)

---

## 1. Design Specifications

| Parameter | Symbol | Target | Notes |
|-----------|--------|--------|-------|
| Process | — | SKY130 (130nm) | Open-source PDK |
| Supply Voltage | VDD | 1.8 V | Nominal |
| Topology | — | Two-stage Miller-compensated | Classic CMOS OTA |
| DC Open-Loop Gain | A₀ | ≥ 60 dB (1000 V/V) | |
| Unity-Gain Bandwidth | UGF | ≥ 5 MHz | |
| Phase Margin | PM | ≥ 60° | At UGF |
| Slew Rate | SR | ≥ 2 V/µs | |
| Quiescent Power | P | ≤ 1 mW | |
| Load Capacitance | CL | 5 pF | |
| Input CM Range | — | ≥ 0.8 V to ≤ 1.6 V | Within VDD rails |
| Output Swing | — | ≥ 1.0 V p-p | |

---

## 2. SKY130 PDK Parameters

The following parameters are used for hand calculations based on the SKY130 BSIM4 models. These are typical-corner values at room temperature (25°C).

### 2.1 Device Parameters (1.8V devices)

| Parameter | NMOS (nfet_01v8) | PMOS (pfet_01v8) | Unit | Notes |
|-----------|-----------------|------------------|------|-------|
| VTH0 | 0.42 | −0.42 | V | Threshold voltage |
| µ·Cox (KP) | 250 | 60 | µA/V² | Process transconductance |
| tox | 4.1 | 4.1 | nm | Gate oxide thickness |
| γ | 0.40 | −0.40 | V^0.5 | Body effect coefficient |
| φ₀ | 0.70 | 0.70 | V | Surface potential |
| Lmin | 0.15 | 0.15 | µm | Minimum drawn length |
| Lnom | 0.18 | 0.18 | µm | Nominal length |
| Wmin | 0.42 | 0.42 | µm | Minimum drawn width |

### 2.2 Output Resistance Model

Channel-length modulation is modeled via the Early voltage:

$$V_A = V_{A0} \times L$$

| Parameter | NMOS | PMOS | Unit |
|-----------|------|------|------|
| VA0 | 8.0 | 5.0 | V/µm |
| λ (at L=1µm) | 0.125 | 0.20 | V⁻¹ |
| λ (at L=0.5µm) | 0.250 | 0.40 | V⁻¹ |

Output resistance: $r_o = \frac{1}{\lambda \cdot I_D} = \frac{V_A}{I_D} = \frac{V_{A0} \times L}{I_D}$

### 2.3 Key Derived Relationships

For a MOSFET in saturation (square-law model):

$$I_D = \frac{1}{2} \mu C_{ox} \frac{W}{L} (V_{GS} - V_{TH})^2 (1 + \lambda V_{DS})$$

$$g_m = \frac{2 I_D}{V_{ov}} = \sqrt{2 \mu C_{ox} \frac{W}{L} I_D} = \mu C_{ox} \frac{W}{L} V_{ov}$$

where $V_{ov} = V_{GS} - V_{TH}$ is the overdrive voltage.

$$r_o \approx \frac{1}{\lambda I_D}$$

---

## 3. Topology Explanation

### 3.1 Circuit Architecture

The design uses a **classic two-stage Miller-compensated CMOS operational amplifier** with the following transistor assignments:

```
                         VDD (1.8V)
                          |
               +----------+----------+
               |          |          |
              [M8]       [M7]      [M3]---+
              (PMOS)     (PMOS)    (PMOS) |
               |          |          |     |
               +----+     |     +----+    |
                    |     |     |         |
      VIN+ --------[M1]   |    [M4]------+
      VIN- --------[M2]   |     |
                    |     |     |
                    +-----+     |
                    |           |
                   [M5]    VOUT1----[CC]----+----[Rz]----+
                   (NMOS)         |         |             |
                    |             |    Gate of M6         |
                   GND            |         |             |
                                 GND       [M6]          |
                                          (NMOS)         |
                                              |          |
                                         VOUT2          GND
                                              |
                                             GND
```

**Simplified schematic:**

```
                VDD
                 |
            +----+----+
            |    |    |
           M8   M7   M3---+
           |    |    |     |
           |    |    +-----M4----+
           |    |    |          |
           |    |    +----+     |
           |    |         |     |
  IN+ ----M1    |   VOUT1-+--CC--+--Rz--+
  IN- ----M2    |         |     |       |
           |    |         |     +--M6---+--- VOUT
           +----+         |         |
           |              |        GND
          M5              |
           |             GND
          GND
```

### 3.2 Component Roles

| Component | Type | Role |
|-----------|------|------|
| M1, M2 | NMOS | Differential input pair — converts differential voltage to current |
| M3 | PMOS (diode-connected) | Active load — provides first-stage output resistance and mirrors current |
| M4 | PMOS | Current mirror output — converts differential currents to single-ended |
| M5 | NMOS | Tail current source — defines bias current ITAIL |
| M6 | NMOS | Second-stage common-source amplifier — provides voltage gain |
| M7 | PMOS | Second-stage active load — current source load for M6 |
| M8 | PMOS (diode-connected) | Bias current reference — generates ITAIL from R_BIAS |
| CC | Capacitor | Miller compensation capacitor — splits poles for stability |
| Rz | Resistor | Nulling resistor — moves RHP zero to improve phase margin |
| R_BIAS | Resistor | Sets the reference current through M8 |

### 3.3 Why This Topology

1. **NMOS input pair**: Higher µ·Cox gives ~4× more gm per unit current than PMOS, enabling higher bandwidth for a given power budget.
2. **Active loads**: Eliminates large resistors, provides high output impedance for high gain.
3. **Miller compensation**: Efficiently uses the Miller effect to create a dominant pole at low frequency without requiring a very large capacitor.
4. **Two stages**: First stage provides high gain with moderate output swing; second stage provides additional gain and drives the output load.

---

## 4. Operating Regions

All transistors are biased in **saturation** (active region) for maximum gain. The conditions are:

| Transistor | Saturation Condition | Design Constraint |
|------------|---------------------|-------------------|
| M1, M2 (NMOS) | VDS ≥ VGS − VTH = Vov | VDS ≥ 0.20 V |
| M3, M4 (PMOS) | VSD ≥ VSG − |VTH| = |Vov| | VSD ≥ 0.25 V |
| M5 (NMOS) | VDS ≥ VGS − VTH = Vov | VDS ≥ 0.20 V |
| M6 (NMOS) | VDS ≥ VGS − VTH = Vov | VDS ≥ 0.25 V |
| M7 (PMOS) | VSD ≥ VSG − |VTH| = |Vov| | VSD ≥ 0.20 V |
| M8 (PMOS) | VSD ≥ VSG − |VTH| = |Vov| | VSD ≥ 0.25 V |

---

## 5. Bias Current Selection

### 5.1 Slew-Rate Constraint

The slew rate of a Miller-compensated op-amp is limited by the tail current charging/discharging the compensation capacitor:

$$SR = \frac{I_{TAIL}}{C_C}$$

Rearranging: $I_{TAIL} = SR \times C_C$

### 5.2 Bandwidth Constraint

The unity-gain bandwidth is:

$$UGF = \frac{g_{m1}}{2\pi \cdot C_C}$$

The input-pair transconductance is:

$$g_{m1} = \frac{2 I_{D1}}{V_{ov1}} = \frac{I_{TAIL}}{V_{ov1}}$$

### 5.3 Iterative Selection

We solve simultaneously. Choose $V_{ov1} = 0.20$ V (see Section 6).

From the UGF constraint (targeting 10 MHz for margin above the 5 MHz spec):

$$C_C = \frac{g_{m1}}{2\pi \times UGF}$$

If we set $I_{TAIL} = 20\;\mu A$ and $V_{ov1} = 0.20$ V:

$$g_{m1} = \frac{I_{TAIL}}{V_{ov1}} = \frac{20\;\mu A}{0.20\;V} = 100\;\mu S$$

$$C_C = \frac{100\;\mu S}{2\pi \times 10\;MHz} = 1.59\;pF \;\;\rightarrow\;\; \text{round to } 1.5\;pF$$

Check slew rate:

$$SR = \frac{20\;\mu A}{1.5\;pF} = 13.3\;V/\mu s \;\;\gg\;\; 2\;V/\mu s \;\;\checkmark$$

Check power budget for second stage (need $I_{D6}$ to drive 5 pF load):

$$I_{D6} = \frac{g_{m6} \times V_{ov6}}{2}$$

With the constraint that the second pole $p_2 = g_{m6}/(2\pi C_L)$ should be ≥ 2.2 × UGF:

$$g_{m6} \geq 2.2 \times 2\pi \times UGF \times C_L = 2.2 \times 2\pi \times 10 \times 10^6 \times 5 \times 10^{-12} = 691\;\mu S$$

With $V_{ov6} = 0.25$ V:

$$I_{D6} = \frac{691\;\mu S \times 0.25\;V}{2} = 86.4\;\mu A \;\;\rightarrow\;\; \text{round to } 100\;\mu A$$

This gives $g_{m6} = 2 \times 100\;\mu A / 0.25\;V = 800\;\mu S$.

### 5.4 Final Bias Currents

| Node | Current | Source |
|------|---------|--------|
| ITAIL (M5) | 20 µA | Tail current source |
| ID1 = ID2 | 10 µA | Each side of diff pair |
| ID3 = ID4 | 10 µA | PMOS current mirror load |
| ID6 | 100 µA | Second-stage driver |
| ID7 | 100 µA | Second-stage active load |
| ID8 (reference) | 20 µA | Bias reference |

---

## 6. Overdrive Voltage Assumptions

Overdrive voltage $V_{ov} = |V_{GS} - V_{TH}|$ controls the trade-off between speed, gain, noise, and headroom:

- **Low Vov** (≤ 0.15 V): Subthreshold/near-threshold. High gm/ID, low noise, but poor speed and reduced output swing.
- **Moderate Vov** (0.15–0.30 V): Sweet spot for analog design. Good gm, reasonable speed, adequate headroom.
- **High Vov** (> 0.30 V): Strong inversion. Fast but power-hungry, degraded matching.

### 6.1 Selected Overdrive Voltages

| Transistor | Vov (V) | Rationale |
|------------|---------|-----------|
| M1, M2 (NMOS input) | 0.20 | Balance gm efficiency with input CM range |
| M3, M4 (PMOS load) | 0.25 | Slightly higher to conserve headroom at first-stage output |
| M5 (NMOS tail) | 0.20 | Must stay in saturation with limited VS headroom |
| M6 (NMOS 2nd stage) | 0.25 | Higher current, need gm for bandwidth |
| M7 (PMOS 2nd stage load) | 0.20 | Lower to maximize output swing |
| M8 (PMOS bias ref) | 0.25 | Matches M3/M4 for accurate current mirroring |

### 6.2 Headroom Check

At the first-stage output (quiescent):
- VOUT1_CM = VDD − |VSG3| = 1.8 − (|VTHP| + |Vov3|) = 1.8 − 0.67 = **1.13 V**
- Available VSD for M4: VDD − VOUT1 = 0.67 V >> |Vov4| = 0.25 V ✓
- Available VDS for M2: VOUT1 − VS1. Need VS1 from input CM (see Section 17).

---

## 7. Transconductance Requirements

### 7.1 Input Pair (M1, M2)

$$g_{m1} = \frac{I_{TAIL}}{V_{ov1}} = \frac{20\;\mu A}{0.20\;V} = \mathbf{100\;\mu S}$$

Verification via square-law:
$$g_{m1} = \sqrt{2 \mu_n C_{ox} \frac{W_1}{L_1} I_{D1}} = \sqrt{2 \times 250 \times 10^{-6} \times 2.0 \times 10 \times 10^{-6}} = \sqrt{10 \times 10^{-9}} = 100\;\mu S \;\;\checkmark$$

### 7.2 Second-Stage Driver (M6)

$$g_{m6} = \frac{2 I_{D6}}{V_{ov6}} = \frac{2 \times 100\;\mu A}{0.25\;V} = \mathbf{800\;\mu S}$$

### 7.3 gm/ID Efficiency

$$\frac{g_{m1}}{I_{D1}} = \frac{100\;\mu S}{10\;\mu A} = 10\;V^{-1}$$

This corresponds to moderate inversion (subthreshold would give ~20–25 V⁻¹; strong inversion ~5–7 V⁻¹ for these devices).

---

## 8. First-Stage Gain

### 8.1 Output Resistance

$$r_{o1} = \frac{V_{A0,n} \times L_1}{I_{D1}} = \frac{8.0 \times 1.0}{10 \times 10^{-6}} = 800\;k\Omega$$

$$r_{o3} = \frac{V_{A0,p} \times L_3}{I_{D3}} = \frac{5.0 \times 1.0}{10 \times 10^{-6}} = 500\;k\Omega$$

First-stage output resistance:

$$R_{out1} = r_{o1} \| r_{o3} = \frac{800 \times 500}{800 + 500}\;k\Omega = \mathbf{307.7\;k\Omega}$$

### 8.2 First-Stage Voltage Gain

$$A_1 = g_{m1} \times R_{out1} = 100\;\mu S \times 307.7\;k\Omega = \mathbf{30.8}$$

In decibels: $20 \log_{10}(30.8) = \mathbf{29.8\;dB}$

### 8.3 Verification of Active-Load Assumption

The current-mirror load provides a low-impedance path at M3 (diode-connected) that is reflected to M4's drain. The key assumption is that M4's drain presents high impedance $r_{o4}$, while M3's drain (node at VOUT1) sees $r_{o3}$ in parallel with $r_{o1}$.

This is valid when the mirror ratio is 1:1 and both M3 and M4 are well-matched (same VGS, same L).

---

## 9. Second-Stage Gain

### 9.1 Output Resistance

$$r_{o6} = \frac{V_{A0,n} \times L_6}{I_{D6}} = \frac{8.0 \times 0.5}{100 \times 10^{-6}} = 40\;k\Omega$$

$$r_{o7} = \frac{V_{A0,p} \times L_7}{I_{D7}} = \frac{5.0 \times 0.5}{100 \times 10^{-6}} = 25\;k\Omega$$

Second-stage output resistance:

$$R_{out2} = r_{o6} \| r_{o7} = \frac{40 \times 25}{40 + 25}\;k\Omega = \mathbf{15.4\;k\Omega}$$

### 9.2 Second-Stage Voltage Gain

$$A_2 = g_{m6} \times R_{out2} = 800\;\mu S \times 15.4\;k\Omega = \mathbf{12.3}$$

In decibels: $20 \log_{10}(12.3) = \mathbf{21.8\;dB}$

---

## 10. Total DC Gain Estimate

### 10.1 Open-Loop DC Gain

$$A_0 = A_1 \times A_2 = 30.8 \times 12.3 = \mathbf{379}$$

In decibels: $20 \log_{10}(379) = \mathbf{51.6\;dB}$

**⚠ This is below the 60 dB target.** We need to increase gain.

### 10.2 Gain Improvement Options

**Option A: Increase channel lengths** (increases $r_o$)

With L = 2.0 µm for first stage (M1–M4):

$$r_{o1} = \frac{8.0 \times 2.0}{10 \times 10^{-6}} = 1.6\;M\Omega, \quad r_{o3} = \frac{5.0 \times 2.0}{10 \times 10^{-6}} = 1.0\;M\Omega$$

$$R_{out1} = 1.6M \| 1.0M = 615\;k\Omega$$

$$A_1 = 100\;\mu S \times 615\;k\Omega = 61.5 \quad (35.8\;dB)$$

With L = 1.0 µm for second stage:

$$r_{o6} = \frac{8.0 \times 1.0}{100 \times 10^{-6}} = 80\;k\Omega, \quad r_{o7} = \frac{5.0 \times 1.0}{100 \times 10^{-6}} = 50\;k\Omega$$

$$R_{out2} = 80k \| 50k = 30.8\;k\Omega$$

$$A_2 = 800\;\mu S \times 30.8\;k\Omega = 24.6 \quad (27.8\;dB)$$

$$A_0 = 61.5 \times 24.6 = 1513 \quad \mathbf{(63.6\;dB)} \;\;\checkmark$$

### 10.3 Revised Channel Lengths

| Component | Original L | Revised L | Rationale |
|-----------|-----------|-----------|-----------|
| M1–M4 (1st stage) | 1.0 µm | 2.0 µm | Double $r_o$, improve gain and matching |
| M5 (tail) | 1.0 µm | 1.0 µm | No gain benefit, keep moderate |
| M6 (2nd stage NMOS) | 0.5 µm | 1.0 µm | Improve $r_{o6}$ for gain |
| M7 (2nd stage PMOS) | 0.5 µm | 1.0 µm | Improve $r_{o7}$ for gain |
| M8 (bias) | 1.0 µm | 1.0 µm | No change needed |

### 10.4 Final DC Gain

$$\boxed{A_0 = A_1 \times A_2 = 61.5 \times 24.6 = 1513 \approx \mathbf{63.6\;dB}}$$

This exceeds the 60 dB target with ~3.6 dB margin.

---

## 11. Miller Compensation Capacitor Calculation

### 11.1 Compensation Strategy

Miller compensation exploits the Miller effect to multiply the effective capacitance seen at the first-stage output, creating a dominant pole at very low frequency while pushing the second pole to higher frequency (pole splitting).

$$C_{C,eff} = C_C \times (1 + A_2) \approx A_2 \times C_C$$

The dominant pole becomes:

$$p_1 = \frac{1}{R_{out1} \times C_{C,eff}} = \frac{1}{R_{out1} \times A_2 \times C_C}$$

### 11.2 Capacitor Value Selection

From the UGF requirement:

$$C_C = \frac{g_{m1}}{2\pi \times UGF} = \frac{100\;\mu S}{2\pi \times 10\;MHz} = 1.59\;pF$$

Choose $C_C = \mathbf{1.5\;pF}$ (practical value, close to calculated).

### 11.3 Compensation Resistor (Zero Nulling)

The feedforward path through $C_C$ creates a right-half-plane (RHP) zero at:

$$z_{RHP} = \frac{g_{m6}}{C_C} = \frac{800\;\mu S}{1.5\;pF} = 533\;MHz$$

Adding a series resistor $R_z$ moves this zero:

$$z = \frac{1}{C_C \left(\frac{1}{g_{m6}} - R_z\right)}$$

Setting $R_z = 1/g_{m6}$ moves the zero to infinity (eliminates it):

$$R_z = \frac{1}{g_{m6}} = \frac{1}{800\;\mu S} = \mathbf{1.25\;k\Omega}$$

For improved phase margin, setting $R_z > 1/g_{m6}$ creates a LHP zero. We use $R_z = 1.25\;k\Omega$ for simplicity.

---

## 12. Pole/Zero Analysis

### 12.1 Dominant Pole (p₁)

$$p_1 = \frac{1}{2\pi \times R_{out1} \times A_2 \times C_C}$$

$$= \frac{1}{2\pi \times 615\;k\Omega \times 24.6 \times 1.5\;pF}$$

$$= \frac{1}{2\pi \times 22.6\;ns} = \frac{1}{142 \times 10^{-9}}$$

$$= \mathbf{7.04\;kHz}$$

### 12.2 Non-Dominant Pole (p₂)

The second pole is approximately at the second-stage output:

$$p_2 \approx \frac{g_{m6}}{2\pi \times C_L} = \frac{800\;\mu S}{2\pi \times 5\;pF} = \mathbf{25.5\;MHz}$$

More precisely, including $C_C$:

$$p_2 \approx \frac{g_{m6}}{2\pi \times (C_L + C_C)} = \frac{800\;\mu S}{2\pi \times 6.5\;pF} = \mathbf{19.6\;MHz}$$

We use the more conservative value: $p_2 \approx 20\;MHz$.

### 12.3 Third Pole (p₃)

A third pole exists at the input pair due to parasitic capacitance:

$$p_3 = \frac{g_{m3}}{2\pi \times C_{gs3}} \approx \frac{g_{m3}}{2\pi \times (2/3) W_3 L_3 C_{ox}}$$

For L₃ = 2.0 µm, this pole is well above 100 MHz and is neglected in the phase margin calculation.

### 12.4 Zero (z)

With $R_z = 1/g_{m6}$: The RHP zero is moved to infinity.

$$z \rightarrow \infty$$

If $R_z$ is slightly larger than $1/g_{m6}$, a LHP zero appears and improves phase margin. With $R_z = 1.25\;k\Omega$ exactly at $1/g_{m6}$, the zero is eliminated.

### 12.5 Pole Summary

| Pole/Zero | Frequency | Location | Notes |
|-----------|-----------|----------|-------|
| p₁ (dominant) | 7.04 kHz | LHP | Set by Miller effect |
| p₂ (non-dominant) | ~20 MHz | LHP | At second-stage output |
| p₃ (parasitic) | >100 MHz | LHP | Input pair parasitics |
| z (feedforward) | ∞ | — | Eliminated by Rz |

---

## 13. Unity-Gain Bandwidth Estimate

### 13.1 Gain-Bandwidth Product

$$UGF = A_0 \times p_1 = 1513 \times 7.04\;kHz = \mathbf{10.7\;MHz}$$

Verification via transconductance:

$$UGF = \frac{g_{m1}}{2\pi \times C_C} = \frac{100\;\mu S}{2\pi \times 1.5\;pF} = \mathbf{10.6\;MHz}$$

Both methods agree: $UGF \approx 10.6\;MHz$

### 13.2 Compliance

$$UGF = 10.6\;MHz \;\;\gg\;\; 5\;MHz \text{ (target)} \;\;\checkmark$$

~10 dB margin above specification.

---

## 14. Phase Margin Considerations

### 14.1 Phase at UGF

The phase of the open-loop transfer function at ω = ω_UGF:

$$\angle H(j\omega_{UGF}) = -\arctan\left(\frac{\omega_{UGF}}{\omega_{p1}}\right) - \arctan\left(\frac{\omega_{UGF}}{\omega_{p2}}\right) + \arctan\left(\frac{\omega_{UGF}}{\omega_{z}}\right)$$

Since $p_1 \ll UGF$: $\arctan(UGF/p_1) \approx 90°$

$$= -90° - \arctan\left(\frac{10.6}{20}\right) + \arctan\left(\frac{10.6}{\infty}\right)$$

$$= -90° - 27.9° + 0°$$

$$= -117.9°$$

### 14.2 Phase Margin

$$PM = 180° - |\angle H(j\omega_{UGF})| = 180° - 117.9° = \mathbf{62.1°}$$

### 14.3 Compliance

$$PM = 62.1° \;\;\geq\;\; 60° \text{ (target)} \;\;\checkmark$$

### 14.4 Second-Pole Requirement for 60° PM

For PM ≥ 60° with the dominant pole contributing 90° and zero at infinity:

$$\arctan\left(\frac{UGF}{p_2}\right) \leq 30°$$

$$p_2 \geq \frac{UGF}{\tan(30°)} = \frac{10.6}{0.577} = 18.4\;MHz$$

Our $p_2 \approx 20\;MHz > 18.4\;MHz$ ✓

### 14.5 Gain Margin

The gain margin is the gain at the frequency where phase = −180°. Since the second pole is at ~20 MHz and the third pole is >100 MHz, the phase does not reach −180° until well above UGF. The gain margin is estimated to be > 20 dB.

---

## 15. Slew-Rate Calculation

### 15.1 Positive Slew Rate

When the input is driven differentially, all tail current flows through one side of the diff pair. The maximum rate at which $C_C$ can be charged is:

$$SR^+ = \frac{I_{TAIL}}{C_C} = \frac{20\;\mu A}{1.5\;pF} = \mathbf{13.3\;V/\mu s}$$

### 15.2 Negative Slew Rate

For a symmetric design with matched diff pair, the negative slew rate equals the positive:

$$SR^- = \frac{I_{TAIL}}{C_C} = 13.3\;V/\mu s$$

### 15.3 Compliance

$$SR = 13.3\;V/\mu s \;\;\gg\;\; 2\;V/\mu s \text{ (target)} \;\;\checkmark$$

~16 dB margin above specification.

### 15.4 Slew-Rate Limiting During Large-Signal Transients

During slew-rate limiting, the second stage must also be able to charge/discharge $C_L$. The second-stage current $I_{D6} = 100\;\mu A$ must drive $C_L = 5\;pF$:

$$SR_{2nd} = \frac{I_{D6}}{C_L} = \frac{100\;\mu A}{5\;pF} = 20\;V/\mu s$$

Since $SR_{2nd} > SR$, the first stage is the slew-rate bottleneck, as expected.

---

## 16. Output Swing and Voltage Requirements

### 16.1 Quiescent Output Voltage

The second-stage output DC level is determined by the feedback in a closed-loop configuration. In open-loop, the output settles at a high-impedance node. For simulation, we assume the output is biased at mid-rail:

$$V_{OUT,CM} = V_{DD}/2 = 0.9\;V$$

### 16.2 Maximum Output Voltage

$$V_{OUT,max} = V_{DD} - |V_{ov7}| = 1.8 - 0.20 = \mathbf{1.60\;V}$$

### 16.3 Minimum Output Voltage

$$V_{OUT,min} = V_{ov6} = 0.25\;\mathbf{V}$$

### 16.4 Output Voltage Swing

$$V_{swing} = V_{OUT,max} - V_{OUT,min} = 1.60 - 0.25 = \mathbf{1.35\;V}_{pp}$$

### 16.5 Saturation Check at Quiescent Point

- M7 (PMOS): $V_{SD7} = V_{DD} - V_{OUT} = 1.8 - 0.9 = 0.9\;V > |V_{ov7}| = 0.20\;V$ ✓
- M6 (NMOS): $V_{DS6} = V_{OUT} - 0 = 0.9\;V > V_{ov6} = 0.25\;V$ ✓

---

## 17. Input Common-Mode Range

### 17.1 Upper Input CM Limit

The input voltage must keep M1/M2 in saturation and not push M3/M4 out of saturation:

For M1 in saturation: $V_{DS1} \geq V_{ov1}$

$V_{D1} = V_{OUT1,CM} = 1.13\;V$

$V_{DS1} = V_{D1} - V_{S1} = 1.13 - V_{S1}$

$V_{S1} = V_{IN,CM} - V_{GS1} = V_{IN,CM} - (V_{THN} + V_{ov1}) = V_{IN,CM} - 0.62\;V$

$V_{DS1} = 1.13 - (V_{IN,CM} - 0.62) = 1.75 - V_{IN,CM} \geq 0.20\;V$

$$V_{IN,CM} \leq 1.55\;V$$

### 17.2 Lower Input CM Limit

M5 must stay in saturation:

$V_{S1} = V_{IN,CM} - 0.62\;V$

$V_{DS5} = V_{S1} - 0 = V_{IN,CM} - 0.62 \geq V_{ov5} = 0.20\;V$

$$V_{IN,CM} \geq 0.82\;V$$

### 17.3 Input CM Range Summary

$$V_{IN,CM} \in [0.82\;V,\;\;1.55\;V]$$

This provides a **0.73 V** input common-mode range centered at ~1.19 V, well within the supply rails.

---

## 18. Output-Current Requirements

### 18.1 Capacitive Load Driving

To slew the output at the full slew rate through the load capacitor:

$$I_{OUT,max} = SR \times C_L = 13.3\;\frac{V}{\mu s} \times 5\;pF = 66.5\;\mu A$$

The second-stage current $I_{D6} = 100\;\mu A > 66.5\;\mu A$ ✓

### 18.2 Resistive Load

If a resistive load $R_L$ is connected:

$$I_{OUT} = \frac{V_{OUT,pp}}{R_L} = \frac{1.35\;V}{R_L}$$

For $R_L = 100\;k\Omega$: $I_{OUT} = 13.5\;\mu A$ ✓ (well within capability)

For $R_L = 50\;k\Omega$: $I_{OUT} = 27\;\mu A$ ✓

### 18.3 Output Impedance

$$R_{OUT} = r_{o6} \| r_{o7} = 80\;k\Omega \| 50\;k\Omega = \mathbf{30.8\;k\Omega}$$

This limits the maximum gain when driving a resistive load:

$$A_{v,loaded} = A_{v,unloaded} \times \frac{R_L}{R_L + R_{OUT}}$$

For $R_L = 100\;k\Omega$: $A_{v,loaded} = 1513 \times \frac{100}{130.8} = 1156$ (61.3 dB)

---

## 19. Power Estimate

### 19.1 Quiescent Power

$$P_{quiescent} = V_{DD} \times (I_{TAIL} + I_{D6} + I_{D8,bias})$$

$$= 1.8\;V \times (20 + 100 + 20)\;\mu A = 1.8 \times 140\;\mu A = \mathbf{252\;\mu W}$$

### 19.2 Power Compliance

$$P = 252\;\mu W \;\;\ll\;\; 1\;mW \text{ (target)} \;\;\checkmark$$

Only 25% of the power budget is used, leaving headroom for additional features (output buffer, bias trimming, etc.).

### 19.3 Power Breakdown

| Block | Current (µA) | Power (µW) | % of Total |
|-------|-------------|-----------|-----------|
| Tail (M5) | 20 | 36 | 14.3% |
| Second stage (M6+M7) | 100 | 180 | 71.4% |
| Bias reference (M8) | 20 | 36 | 14.3% |
| **Total** | **140** | **252** | **100%** |

---

## 20. Noise Considerations

### 20.1 Input-Referred Thermal Noise

The input-referred noise voltage spectral density (thermal noise):

$$\overline{v_n^2} = \frac{8kT}{3} \cdot \frac{g_{m1} + g_{m3}}{g_{m1}^2} \cdot \gamma$$

where γ ≈ 1.2 for SKY130 MOSFETs (excess noise factor).

$$g_{m3} = \frac{2 I_{D3}}{|V_{ov3}|} = \frac{2 \times 10\;\mu A}{0.25\;V} = 80\;\mu S$$

$$\overline{v_n^2} = \frac{8 \times 1.38 \times 10^{-23} \times 300}{3} \cdot \frac{100 + 80}{100^2} \cdot 1.2$$

$$= 1.104 \times 10^{-20} \cdot \frac{180}{10000} \cdot 1.2$$

$$= 1.104 \times 10^{-20} \cdot 0.0216$$

$$= 2.38 \times 10^{-22}\;V^2/Hz$$

$$\sqrt{\overline{v_n^2}} = \mathbf{15.4\;nV/\sqrt{Hz}}$$

### 20.2 1/f (Flicker) Noise

The 1/f noise corner frequency for SKY130 is typically 10–100 kHz for these device dimensions. At frequencies above the corner frequency, thermal noise dominates.

For minimum 1/f noise:
- Use larger W×L products (scales inversely with 1/f noise)
- PMOS input pairs have lower 1/f noise (but lower gm)

### 20.3 Integrated Noise

Over a bandwidth from 1 kHz to UGF (10 MHz):

$$v_{n,rms} \approx \sqrt{\overline{v_n^2} \times f_{BW}} = 15.4\;nV/\sqrt{Hz} \times \sqrt{10\;MHz} = 15.4 \times 3162 = \mathbf{48.7\;\mu V_{rms}}$$

---

## 21. CMRR and PSRR Estimates

### 21.1 CMRR

The common-mode rejection ratio depends on the mismatch between M1/M2 and M3/M4. For a perfectly matched differential pair:

$$CMRR = \frac{A_d}{A_{cm}} \approx g_{m1} \cdot R_{OUT,cm}$$

where $R_{OUT,cm}$ is the common-mode output resistance of the first stage.

For practical purposes with layout matching:

$$CMRR \approx \frac{g_{m1}}{g_{m5}} \times \frac{1}{\Delta(\text{mismatch})}$$

Estimate: **CMRR ≥ 70 dB** (limited by matching, typically 0.1% mismatch gives ~60 dB).

### 21.2 PSRR

- **Positive PSRR (VDD)**: Limited by the second stage where M7 acts as a current source with finite output impedance. Estimated: **PSRR+ ≈ 50–60 dB**.
- **Negative PSRR (VSS/GND)**: Better than PSRR+ due to the tail current source providing supply rejection. Estimated: **PSRR− ≈ 60–70 dB**.

---

## 22. Sensitivity and Trade-Off Discussion

### 22.1 Key Trade-Offs

| Trade-Off | Parameters Affected | Direction |
|-----------|-------------------|-----------|
| ↑ Gain vs ↓ Bandwidth | ↑L, ↓Vov → ↑Gain, ↓UGF | Opposing |
| ↑ SR vs ↑Power | ↑ITAIL → ↑SR, ↑P | Same direction |
| ↑ PM vs ↓Bandwidth | ↑CC → ↑PM (lower p2/p1 ratio), ↓UGF | Opposing |
| ↑ Swing vs ↑Gain | ↓Vov → ↑Swing, ↓gm → ↓Gain | Opposing |
| ↑ Matching vs ↑Area | ↑W,L → ↑Matching, ↑Area | Same direction |
| ↑ Speed vs ↑Power | ↑gm → ↑Speed, ↑ID → ↑Power | Same direction |

### 22.2 Sensitivity to Process Variation

| Parameter | Impact of +10% Variation |
|-----------|-------------------------|
| µnCox +10% | gm1 ↑ ~5%, A0 ↑ ~5%, UGF ↑ ~5% |
| VTHN +50mV | Vov ↓, gm ↑ slightly, headroom ↓ |
| ITAIL +10% | gm1 ↑ 10%, UGF ↑ 10%, SR ↑ 10% |
| CC +10% | UGF ↓ ~10%, PM ↑ slightly |
| CL +20% | p2 ↓, PM ↓ (critical!) |

### 22.3 Critical Sensitivities

1. **Phase margin vs. CL**: The most sensitive parameter. A 50% increase in $C_L$ (to 7.5 pF) would reduce $p_2$ to ~13 MHz, reducing PM to ~45° (below spec).

2. **Gain vs. Channel length**: Gain scales as L² (through $r_o$). A 20% reduction in effective L (due to process variation) reduces gain by ~36%.

3. **Slew rate vs. CC**: Directly proportional. Process variation in $C_C$ directly impacts SR.

### 22.4 Design Margins Summary

| Parameter | Target | Designed | Margin |
|-----------|--------|----------|--------|
| DC Gain | ≥ 60 dB | 63.6 dB | +3.6 dB |
| UGF | ≥ 5 MHz | 10.6 MHz | +6.5 dB |
| Phase Margin | ≥ 60° | 62.1° | +2.1° |
| Slew Rate | ≥ 2 V/µs | 13.3 V/µs | +16 dB |
| Power | ≤ 1 mW | 0.252 mW | +6.0 dB |

### 22.5 Design Decisions Summary

| Decision | Choice | Reasoning |
|----------|--------|-----------|
| Input pair type | NMOS | Higher µCox → higher gm/ID |
| Vov (input pair) | 0.20 V | Balance gm, headroom, noise |
| ITAIL | 20 µA | Meets SR with margin, low power |
| CC | 1.5 pF | Sets UGF at 10.6 MHz |
| Rz | 1.25 kΩ | Eliminates RHP zero |
| L (1st stage) | 2.0 µm | Boosts gain to >60 dB |
| L (2nd stage) | 1.0 µm | Balances gain and speed |
| ID6 | 100 µA | Drives 5 pF load, sets p2 |

---

*End of hand calculations.*
