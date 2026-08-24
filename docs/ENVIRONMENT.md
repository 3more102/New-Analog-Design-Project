# Environment Report

**Date**: 2026-08-21  
**Project**: SKY130 1.8V Two-Stage CMOS Op-Amp  
**Repository**: New-Analog-Design-Project

## Detected Tools

| Tool | Status | Version | Path |
|------|--------|---------|------|
| Git | ✅ Available | 2.55.0 | git (Windows) |
| Python | ✅ Available | 3.12.10 | System |
| matplotlib | ✅ Installed | 3.11.1 | pip |
| numpy | ✅ Installed | 2.5.1 | pip |
| ngspice | ❌ Missing | — | — |
| SKY130 PDK | ❌ Missing | — | — |
| KLayout | ❌ Missing | — | — |
| Magic | ❌ Missing | — | — |
| Make | ❌ Missing | — | — |
| OpenSTA | ❌ Missing | — | — |
| Yosys | ❌ Missing | — | — |

## Impact Analysis

With the current environment, this project can:
- ✅ Create complete SPICE netlists and testbenches
- ✅ Create Python simulation automation scripts
- ✅ Perform analytical hand calculations in Python
- ✅ Generate publication-quality plots from simulation data
- ✅ Create design documentation and reports

This project **cannot yet**:
- ❌ Run SPICE simulations (requires ngspice)
- ❌ Use SKY130 device models (requires PDK)
- ❌ Perform layout (requires Magic/KLayout)
- ❌ Run DRC/LVS/PEX (requires KLayout/Magic)

## Installation Instructions

### 1. ngspice (Required)

**Windows (MSYS2/MinGW64):**
```bash
# Install MSYS2 from https://www.msys2.org/
# Then in MSYS2 MinGW64 terminal:
pacman -S mingw-w64-x86_64-ngspice
```

**macOS:**
```bash
brew install ngspice
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get install ngspice
```

**Verify:**
```bash
ngspice --version
```

### 2. SKY130 PDK (Required)

```bash
# Clone the PDK
export PDK_ROOT=$HOME/pdk
git clone https://github.com/google/open-sky130-data.git $PDK_ROOT/sky130A

# Or use Volare (recommended for managed installation)
pip install volare
volare enable --pdk-path $PDK_ROOT/sky130A efabless/sky130_fd_sc_hd

# Set environment variables
export PDK_PATH=$PDK_ROOT/sky130A
export PDK_ROOT=$PDK_ROOT/sky130A

# Verify ngspice model files exist
ls $PDK_ROOT/libs.tech/ngspice/sky130_fd_pr__nfet_01v8__tt.pm3
```

### 3. Magic (For Layout)

**Linux:**
```bash
sudo apt-get install magic
# Or build from source:
git clone https://github.com/RTimothyEdwards/magic.git
cd magic
./configure
make
sudo make install
```

**macOS:**
```bash
brew install --cask magic
```

### 4. KLayout (For DRC/LVS)

**Windows:** Download from https://www.klayout.de/  
**Linux:**
```bash
sudo apt-get install klayout
```

**macOS:**
```bash
brew install klayout
```

### 5. Make (Optional, for build automation)

**Windows (MSYS2):**
```bash
pacman -S mingw-w64-x86_64-make
```

**Linux:**
```bash
sudo apt-get install make
```

## Quick Setup Script

A setup script is provided at `scripts/setup.sh` that will verify all tools
are installed and configured correctly.
