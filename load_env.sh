#!/bin/bash
# 加载.env.local中的所有环境变量

set -o allexport
source .env.local
set +o allexport
