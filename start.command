#!/bin/bash
cd "$(dirname "$0")"
export PORT=5001
python3 app.py
echo "Press any key to exit"
read