# SKY130 1.8V Two-Stage CMOS Operational Amplifier

A professional analog IC design project: complete design, simulation, characterization, and verification of a transistor-level two-stage Miller-compensated CMOS operational amplifier using the open-source SKY130 PDK.

## Project Overview

| Parameter | Target | Status |
|-----------|--------|--------|
| Process | SKY130 (130nm) | ✅ Defined |
| Supply Voltage | 1.8V | ✅ Defined |
| Topology | Two-stage Miller-compensated CMOS OTA | ✅ Designed |
| DC Open-Loop Gain | ≥ 60 dB | 🔲 Pending simulation |
| Unity-Gain Bandwidth | ≥ 5 MHz | 🔲 Pending simulation |
| Phase Margin | ≥ 60° | 🔲 Pending simulation |
| Slew Rate | ≥ 2 V/µs | 🔲 Pending simulation |
| Quiescent Power | ≤ 1 mW | 🔲 Pending simulation |
| Load Capacitance | 5 pF | ✅ Defined |

## Repository Structure

```
├── README.md                 # This file
├── PROJECT_SPEC.md           # Full design specifications
├── DESIGN_PLAN.md            # Step-by-step design methodology
├── DESIGN_THEORY.md          # Theory of operation
├── HAND_CALCULATIONS.md      # Manual design calculations
├── DEVICE_SIZING.md          # Transistor sizing rationale
├── SIMULATION_PLAN.md        # Simulation testbench plan
├── VERIFICATION_PLAN.md      # Verification checklist
├── RESULTS.md                # Simulation results summary
├── POWER_ANALYSIS.md         # Power characterization
├── PVT_ANALYSIS.md           # Process/Voltage/Temp corner analysis
├── LAYOUT_PLAN.md            # Physical design plan
├── FINAL_REPORT.md           # Comprehensive final report
├── CHANGELOG.md              # Design revision history
│
├── docs/                     # Detailed documentation
│   ├── ENVIRONMENT.md        # Tool detection and setup
│   └── REFERENCES.md         # Literature and design references
│
├── design/                   # Design source files
│   └── opamp_top.spice       # Top-level op-amp schematic netlist
│
├── schematic/                # Schematic exports (KiCad, etc.)
│   └── opamp_top.kicad_sch   # (placeholder for schematic capture)
│
├── spice/                    # SPICE subcircuits and models
│   ├── sky130_models.spice   # PDK model includes
│   ├── opamp_subcircuit.spice # Op-amp subcircuit definition
│   └── bias_network.spice    # Bias circuitry
│
├── models/                   # PDK model references
│   └── README.md             # Model file locations
│
├── testbenches/              # Simulation testbenches
│   ├── tb_dc_gain.ac         # DC gain / AC analysis
│   ├── tb_gbwp.ac            # Gain-bandwidth product
│   ├── tb_transient.tran     # Transient / slew rate
│   ├── tb_cmrr.ac            # CMRR characterization
│   ├── tb_psrr.ac            # PSRR characterization
│   ├── tb_noise.ac           # Noise analysis
│   ├── tb_offset.mc          # Monte Carlo offset
│   └── tb_power.op           # Power measurement
│
├── sim/                      # Simulation run scripts
│   └── run_all.sh            # Run all simulations
│
├── scripts/                  # Automation scripts
│   ├── setup.sh              # Environment setup verification
│   ├── run_ngspice.sh        # Run ngspice wrapper
│   ├── extract_results.py    # Parse rawngspice output
│   ├── plot_results.py       # Matplotlib plotting
│   └── pvt_corners.py        # PVT sweep automation
│
├── results/                  # Simulation output data
│   └── .gitkeep
│
├── plots/                    # Generated plots (PNG/PDF)
│   └── .gitkeep
│
├── reports/                  # Generated reports
│   └── .gitkeep
│
├── verification/             # Verification results
│   ├── drc/                  # DRC results
│   ├── lvs/                  # LVS results
│   └── pex/                  # PEX results
│
├── layout/                   # Physical design files
│   ├── opamp_top.gds         # (to be generated)
│   └── opamp_top.mag         # Magic layout file
│
├── pex/                      # Post-layout extracted netlists
│   └── .gitkeep
│
└── config/                   # Project configuration
    ├── Makefile              # Build automation
    └── config.mk             # Configuration variables
```

## Quick Start

### Prerequisites

Install ngspice and the SKY130 PDK. See [docs/ENVIRONMENT.md](docs/ENVIRONMENT.md) for detailed instructions.

```bash
# Verify installation
./scripts/setup.sh
```

### Running Simulations

```bash
# Run all simulations
cd sim
./run_all.sh

# Run individual testbench
ngspice -b testbenches/tb_dc_gain.ac -o results/dc_gain.log
```

### Generating Plots

```bash
# Extract results from simulation data
python scripts/extract_results.py

# Generate publication-quality plots
python scripts/plot_results.py
```

## Design Methodology

1. **Specification** → Define targets from application requirements
2. **Theory** → Derive hand calculations from small-signal analysis
3. **Sizing** → Size transistors using SKY130 device data
4. **Schematic** → Create SPICE netlist with SKY130 models
5. **Simulation** → DC, AC, transient, and noise analysis
6. **Characterization** → Extract all performance metrics
7. **Corner Analysis** → PVT robustness verification
8. **Layout** → Physical implementation (DRC-clean)
9. **Extraction** → PEX netlist for post-layout simulation
10. **Verification** → LVS, post-layout simulation comparison

## Documentation

- [Design Specifications](PROJECT_SPEC.md)
- [Theory of Operation](DESIGN_THEORY.md)
- [Hand Calculations](HAND_CALCULATIONS.md)
- [Device Sizing](DEVICE_SIZING.md)
- [Simulation Plan](SIMULATION_PLAN.md)
- [Results Summary](RESULTS.md)
- [Final Report](FINAL_REPORT.md)

## Tools and References

- **SKY130 PDK**: [Google Open-Source PDK](https://github.com/google/open-sky130-data)
- **ngspice**: [Open-source SPICE simulator](https://ngspice.sourceforge.io/)
- **Magic VLSI**: [Layout tool](https://github.com/RTimothyEdwards/magic)
- **KLayout**: [Layout viewer/editor](https://www.klayout.de/)
- **Efabless**: [Open-source ASIC flow](https://efabless.com/)

## License

This project is for educational and research purposes. SKY130 PDK is licensed under Apache 2.0.
