# yyAutoAiframework

## 创建虚拟环境
uv venv .venv

# 激活虚拟环境（根据你的 shell）
# Bash/Zsh:
source .venv/bin/activate
# Fish:
source .venv/bin/activate.fish
# Windows CMD:
.venv\Scripts\activate.bat
# Windows PowerShell:
.venv\Scripts\Activate.ps1

# 然后在虚拟环境中安装依赖
uv pip install -e .

## 打包
pip install twine
python setup.py sdist bdist_wheel  # 生成 `dist/` 目录

twine upload dist/*

## 清理
rm -rf dist/ build/
python setup.py sdist bdist_wheel
twine upload dist/*

## 卸载
pip uninstall 包名 -y  # 强制卸载
pip install 包名       # 重新安装最新版
pip install --upgrade --force-reinstall 包名

pip install 包名==最新版本号