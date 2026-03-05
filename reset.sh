#!/bin/bash
git fetch origin
git reset --hard fe26447410e342ea5d803313c15d609b5760f6da
git push origin main --force
echo "Reset to baseline commit fe26447"
