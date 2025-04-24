import subprocess
import os
import sys
import tempfile


def 封装代码_普通编译(脚本路径, 隐藏导入模块=None):
    """
    将指定的 Python 脚本打包成标准结构的 EXE 可执行文件，输出到用户桌面（非单文件模式）。
    """
    try:
        桌面路径 = os.path.join(os.path.expanduser("~"), 'Desktop')
        pyinstaller_path = os.path.join(os.path.dirname(sys.executable), 'Scripts', 'pyinstaller.exe')

        if not os.path.exists(pyinstaller_path):
            raise FileNotFoundError(f"未找到 pyinstaller，请确保它已正确安装。路径：{pyinstaller_path}")

        # 参数类型检查
        if 隐藏导入模块 is not None:
            if isinstance(隐藏导入模块, str):
                raise TypeError("❌ [类型错误] 隐藏导入模块不能是字符串，请使用 ['模块名'] 格式的列表")
            if not isinstance(隐藏导入模块, (list, tuple)) or not all(isinstance(m, str) for m in 隐藏导入模块):
                raise TypeError("❌ [类型错误] 隐藏导入模块参数必须是字符串列表，例如：['模块1', '模块2']")

        with tempfile.TemporaryDirectory() as 临时目录:
            命令 = [
                pyinstaller_path,
                '--distpath', 桌面路径,
                '--workpath', 临时目录,
                '--specpath', 临时目录,
            ]

            if 隐藏导入模块:
                for 模块名 in 隐藏导入模块:
                    命令.append(f'--hidden-import={模块名}')

            命令.append(脚本路径)

            print(f"🚀 开始打包（普通结构）：{os.path.basename(脚本路径)}")
            subprocess.run(命令, check=True)
            print(f"✅ 打包成功：{os.path.basename(脚本路径)}（普通结构）已输出至桌面。")

    except TypeError as e:
        print(e)
    except subprocess.CalledProcessError as e:
        print(f"❌ 打包失败（PyInstaller 执行异常）：{e}")
    except FileNotFoundError as e:
        print(f"❌ 错误：{e}")
