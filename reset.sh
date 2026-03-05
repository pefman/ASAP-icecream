#!/bin/bash
git fetch origin
git reset --hard 2880734
git push origin main --force
echo "Reset to baseline commit 2880734"
