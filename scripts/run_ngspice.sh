#!/bin/bash
# ============================================================
# ngspice Runner — Handles MSYS2 Environment on Windows
# ============================================================
# This script ensures ngspice runs with the correct library
# paths on Windows/MSYS2 systems.
# ============================================================

# Detect MSYS2
if [ -d "/c/msys64/mingw64" ]; then
    export PATH="/c/msys64/mingw64/bin:$PATH"
    export MSYSTEM=MINGW64
    export MINGW_PREFIX="/c/msys64/mingw64"
    NGSPICE="/c/msys64/mingw64/bin/ngspice.exe"
elif command -v ngspice &> /dev/null; then
    NGSPICE="ngspice"
else
    echo "ERROR: ngspice not found"
    exit 1
fi

# Run ngspice with all arguments
exec "$NGSPICE" "$@"
