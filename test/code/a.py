import importlib

def check_package(package_name):
    try:
        importlib.import_module(package_name)
        print(f"{package_name} 的 Python 包。")
    except ModuleNotFoundError as e:
        print(f"{package_name} 不是有效的 Python 包：{e}")

# 檢查 plane_game 是否為有效包
check_package("plane_game")