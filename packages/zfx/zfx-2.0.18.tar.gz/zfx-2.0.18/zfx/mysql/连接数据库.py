import mysql.connector
from mysql.connector import Error


def 连接数据库(主机, 用户名, 密码, 数据库名, 字符集='utf8mb4'):
    """
    连接到MySQL数据库，返回连接和游标对象，若失败则返回 (None, None)。
    自动检测参数类型，捕获所有异常。
    """
    # 参数类型检查
    if not all(isinstance(x, str) and x.strip() for x in [主机, 用户名, 密码, 数据库名]):
        print("[参数错误] 所有参数必须为非空字符串")
        return None, None

    try:
        连接对象 = mysql.connector.connect(
            host=主机,
            user=用户名,
            password=密码,
            database=数据库名,
            use_unicode=True
        )

        # 可选设置字符集
        try:
            连接对象.set_charset_collation(charset=字符集)
        except AttributeError:
            pass

        游标对象 = 连接对象.cursor()
        return 连接对象, 游标对象

    except Error as e:
        print(f"[数据库连接错误] {e}")
        return None, None

    except Exception as e:
        print(f"[未知错误] {e}（可能是参数错误或环境问题）")
        return None, None
