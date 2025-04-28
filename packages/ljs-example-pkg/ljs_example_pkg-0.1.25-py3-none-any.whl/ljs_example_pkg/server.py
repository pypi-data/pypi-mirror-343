from mcp.server.fastmcp import FastMCP
import os
import pymysql
import logging
import json
import mcp.types as types
import requests
from dotenv import load_dotenv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib

mcp = FastMCP()

load_dotenv()

db_host = os.getenv("MYSQL_HOST")
db_user = os.getenv("MYSQL_USER")
db_pass = os.getenv("MYSQL_PASSWORD")
db_database = os.getenv("MYSQL_DATABASE")
db_port = int(os.getenv("MYSQL_PORT"))

email_recipients = os.getenv("EMAIL_RECIPIENTS")
email_sender = os.getenv("EMAIL_SENDER")
email_token = os.getenv("EMAIL_TOKEN")

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
        获取指定城市的近期的天气信息
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
    

@mcp.tool()
def send_mail(content: str, subject: str) -> types.TextContent:
    """
        给自己发一封邮件
        函数输入：
            content: 邮件正文内容
            subject: 邮件主题，主题格式：“天气预警（具体日期）”
        函数输出：
            发送成功或失败的提示信息    
    """
    # 收件人列表
    recipients = email_recipients
    # 发件人和收件人
    sender_email = email_sender


    message = MIMEText(content, 'plain', 'utf-8')  # 纯文本格式
    message["From"] = sender_email
    message['To'] = email_recipients  
    message["Subject"] = subject

    # 使用 SMTP 发送邮件
    try:
        # 创建 SMTP 连接
        with smtplib.SMTP_SSL('smtp.163.com', 465)as server:
            server.login(sender_email, email_token)  # 登录 SMTP 服务器
            server.sendmail(sender_email, recipients, message.as_string())  # 发送邮件
            logging.info("Email sent successfully!")
            return types.TextContent(type="text", text="Email sent successfully!")
    except Exception as e:
        logging.info(f"Exception Error: {e}")
        return types.TextContent(type="text", text=f"Email sent failed! Error: {e}")
    

@mcp.tool()
async def delete_data(sql: str) -> list[types.TextContent]:
    """
        执行指定删除数据语句(只执行DELETE语句)，而且DELETE语句必须带WHERE条件
        函数输入：
            sql: 删除数据的SQL语句
        函数输出：
            包含执行删除语句的结果
    """
    # 创建 SamplingMessage 用于触发 sampling callback 函数
    result = await mcp.get_context().session.create_message(
        messages=[
            types.SamplingMessage(
                role='user', content=types.TextContent(
                    type='text', text=f'是否执行删除语句: {sql} (Y)')
            )
        ],
        max_tokens=100
    )

    # 获取到 sampling callback 函数的返回值，并根据返回值进行处理
    if result.content.text == 'Y':
        conn = pymysql.connect(  
            host=db_host,  
            user=db_user,      
            password=db_pass,  

            database=db_database,  
            port=db_port,  
        )
        try:
            with conn.cursor() as cursor:
                # 执行删除语句
                logging.info("Executing SQL: {}".format(sql))
                if not sql.strip().upper().startswith("DELETE"):
                    raise ValueError("Only DELETE queries are allowed for delete_data")
            
                # 删除语句必须包含WHERE条件
                if "WHERE" not in sql.upper():
                    raise ValueError("DELETE statement must contain WHERE condition")
                
                cursor.execute(sql)
                conn.commit()
                result = cursor.rowcount    
                logging.info("Result: {}".format(result))
                return [types.TextContent(type="text", text=f"Deleted {result} rows.")]
        except Exception as e:
            return "Error: {}".format(str(e))
        finally:
            conn.close()
    else:
        logging.info("result.content.text: {}".format(result.content.text))
        return [types.TextContent(type="text", text="Operation cancelled.")]


def main() -> None:
    logging.info("Hello from ljs-example-pkg!")
    mcp.run(transport='stdio')

if __name__ == "__main__":
    mcp.run(transport='stdio')  # 启用调试模式