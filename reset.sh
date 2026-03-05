#!/bin/bash
git fetch origin
git reset --hard d7f01c5934ab38452f7f61ce0c580f6ff479b529
git push origin main --force
echo "Reset to baseline commit d7f01c5"
