#!/bin/bash
git fetch origin
git reset --hard a71e83f
git push origin main --force
echo "Reset to baseline commit a71e83f"
