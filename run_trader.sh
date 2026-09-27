#!/bin/bash

# --- CONFIGURATION ---
PROJECT_DIR="USDT_FlashTrader"
PYTHON_SCRIPT="FlashTrader.py"
REQUIREMENTS_FILE="requirements.txt"

# Your GitHub repository
REPO_URL="https://github.com/lifeinsuranceconsultant380-maker/Usdtfalsh.git"

echo "================================================"
echo "🚀 Initializing USDT Flash Trader in Termux..."
echo "================================================"

# 1. Setup / Clone
if [ ! -d "$PROJECT_DIR" ]; then
    echo "[STEP 1/3] Cloning repository..."

    git clone "$REPO_URL" "$PROJECT_DIR" || {
        echo "FATAL: Git clone failed."
        exit 1
    }
else
    echo "[STEP 1/3] Repository found. Pulling latest changes..."

    cd "$PROJECT_DIR" || exit 1
    git pull origin main
fi

# Enter project directory
cd "$PROJECT_DIR" || {
    echo "FATAL: Could not enter project directory."
    exit 1
}

# 2. Install dependencies
echo "[STEP 2/3] Installing Python dependencies..."

if command -v python >/dev/null 2>&1; then
    python -m pip install -r "$REQUIREMENTS_FILE"
else
    echo "FATAL: Python not found."
    exit 1
fi

# 3. Run trader
echo "[STEP 3/3] Starting Flash Trader..."
echo "=================================================="

python "$PYTHON_SCRIPT"

echo "=================================================="
echo "✅ Execution Complete."
