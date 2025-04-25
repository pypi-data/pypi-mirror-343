from mcp.server.fastmcp import FastMCP
import os
import pymysql
import logging
import json
import mcp.types as types
import requests
from dotenv import load_dotenv

mcp = FastMCP()

load_dotenv()

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
def show_create_table(table_name: str) -> list[types.TextContent]:
    """
        获取指定表的表结构
        函数输入：
            table_name: 表名
        函数输出：
            包含执行SHOW CREATE TABLE语句的结果
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
            return [types.TextContent(type="text", text=str(result))]
    except Exception as e:
        return "Error: {}".format(str(e))
    finally:
        conn.close()


@mcp.tool()
def query_table(query: str) -> list[types.TextContent]:
    """
        执行指定查询语句(只执行SELECT语句)
        函数输入：
            query: 查询语句
        函数输出：
            包含执行查询语句的结果
    """
    conn = pymysql.connect(  
         host=db_host,  
         user=db_user,      
         password=db_pass,  
         database=db_database,  
         port=db_port,  
    )
    try:
        with conn.cursor() as cursor:
            # 执行查询语句
            logging.info("Executing SQL: {}".format(query))
            if not query.strip().upper().startswith("SELECT"):
                    raise ValueError("Only SELECT queries are allowed for query_table")
            
            cursor.execute(query)
            result = cursor.fetchall()
            logging.info("Result: {}".format(result))
            return [types.TextContent(type="text", text=str(result))]
    except Exception as e:
        return "Error: {}".format(str(e))
    finally:
        conn.close()


@mcp.tool()
def list_tables() -> list[types.TextContent]:
    """
        获取数据库中的所有表名单
        函数输入：
            无
        函数输出：
            包含数据库中的所有表名单    
    """
    conn = pymysql.connect(  
         host=db_host,  
         user=db_user,      
         password=db_pass,  
         database=db_database,  
         port=db_port,  
    )
    try:
        with conn.cursor() as cursor:
            # 执行SHOW TABLES语句
            sql = "SHOW TABLES"
            logging.info("Executing SQL: {}".format(sql))
            cursor.execute(sql)
            result = cursor.fetchall()
            logging.info("Result: {}".format(result))
            return [types.TextContent(type="text", text=str(result))]
    except Exception as e:
        return "Error: {}".format(str(e))
    finally:
        conn.close()


@mcp.tool()
def get_weather(city_code: str) -> list[types.TextContent]:
    """
        获取指定城市的天气信息
        函数输入：
            city_code: 城市代码
        函数输出：
            包含指定城市的天气信息    
    """
    url = f"http://t.weather.itboy.net/api/weather/city/{city_code}"
    response = requests.get(url)
    if response.status_code == 200:
        data = json.loads(response.text)
        return [types.TextContent(type="text", text=str(data))]
    else:
        return [types.TextContent(type="text", text=f"Error: {response.status_code} {response.text}")]


def main() -> None:
    logging.info("Hello from ljs-example-pkg!")
    mcp.run(transport='stdio')

if __name__ == "__main__":
    mcp.run(transport='stdio')  # 启用调试模式