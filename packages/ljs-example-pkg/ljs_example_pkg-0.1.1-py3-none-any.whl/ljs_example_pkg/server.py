from mcp.server.fastmcp import FastMCP
import os
import pymysql
import logging
import json
from dotenv import load_dotenv

# 加载 .env 文件
load_dotenv('D:\code\mcp_servers\.env')

mcp = FastMCP()

db_host = os.getenv("MYSQL_HOST")
db_user = os.getenv("MYSQL_USER")
db_pass = os.getenv("MYSQL_PASSWORD")
db_database = os.getenv("MYSQL_DATABASE")
db_port = int(os.getenv("MYSQL_PORT"))

@mcp.tool()
def get_nowtime() -> str:
    """获取 当前时间（北京时间）"""
    import datetime
    now = datetime.datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")

@mcp.tool()
def get_schema(table_name: str) -> str:
    """
        获取指定表的表结构
        函数输入：
            table_name: 表名
        函数输出：
            包含执行SHOW CREATE TABLE语句的结果的 JSON 数组
    """
    logging.info("Connected to database: {} tablename: {}".format(db_database, table_name))
    conn = pymysql.connect(  
        host=db_host,  
        user=db_user,  
        password=db_pass,  
        database=db_database,  
        port=db_port,  
    )
    try:
        with conn.cursor() as cursor:
            # 执行 DESCRIBE 语句
            sql = f"SHOW CREATE TABLE  {table_name}"
            logging.info("Executing SQL: {}".format(sql))
            cursor.execute(sql)
            result = cursor.fetchall()
            logging.info("Result: {}".format(result))
            # 将结果转换为 JSON 数组
            result_json = json.dumps(result, ensure_ascii=False, indent=4)
            return result_json
    except Exception as e:
        return "Error: {}".format(str(e))
    finally:
        conn.close()

def main() -> None:
    logging.info("Hello from ljs-example-pkg!")
    mcp.run(transport='stdio')

if __name__ == "__main__":
    mcp.run(transport='stdio')  # 启用调试模式