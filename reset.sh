#!/bin/bash
git fetch origin
git reset --hard 8511622
git push origin main --force
echo "Reset to baseline commit 8511622"
