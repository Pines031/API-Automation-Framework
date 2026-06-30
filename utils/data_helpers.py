import xlrd
import yaml
import pymysql
from pymysql.err import *
from urllib.parse import urlparse


def get_excel_data(file_path,sheet_name,start_col=None,end_col=None): # 文件路径/sheet名称/起点列/终点列

    if file_path.endswith('.xls'):  # 判断文件格式是否为xls
        myexcel = xlrd.open_workbook(file_path)
        mysheet = myexcel.sheet_by_name(sheet_name)
        data = []

        if isinstance(start_col,int) and isinstance(end_col,int):  # isinstance判断对象是否为对应的数据类型
            # 获取切片数据
            for i in range(1, mysheet.nrows):
                data.append(mysheet.row_values(i, start_col, end_col))
            return data
        else:
            # 获取整行数据
            for i in range(1, mysheet.nrows):
                data.append(mysheet.row_values(i))
            return data
    else:
        raise TypeError('不支持的表格格式，仅支持.xls文件')

def get_yamldata(file_path):
    """

    :param file_path:  数据文件
    :return: 返回yaml数据
    """
    data=None
    try:
        with open(file=file_path, mode='r', encoding='utf-8') as f:
            data = yaml.load(stream=f, Loader=yaml.SafeLoader)
    except Exception as e :
        print(f'{type(e).__name__}:  {e}')

    return data

def database_helper(sql,values=None,database='finance',**config):
    connect=None
    cursor=None
    try:
        connect = pymysql.connect(database=database, **config)
        cursor = connect.cursor()
        # print('DATABASE CONNECTION IS BEGIN')
        if values is None:  # 如果values为空,执行execute
            cursor.execute(sql)
        elif isinstance(values,(tuple,list)):  # 如果values是元组或列表,执行executemany
            cursor.executemany(query=sql,args=values)

        if 'select' in sql.lower(): # 如果sql包含select,返回查询结果
            return cursor.fetchall()
        else:  # 否则执行提交,并返回受影响行数
            connect.commit()
            # print('SQL Successful')
            return cursor.rowcount
    except Exception as e:
        print(f'{e.__class__.__name__} : {e}')
        if connect:
            connect.rollback()
    finally:
        if connect:
            connect.close()
        if cursor:
            cursor.close()
        # print('DATABASE CONNECTION IS OVER')

def sqlfile_execute(filepath,database='finance',**config):  # **代表config是可变的关键字参数，可以不传，也可以传一个或任意多个
    """执行sql文件"""
    connect=None
    cursor=None

    try:
        connect=pymysql.connect(**config,database=database)
        cursor=connect.cursor()
        try:
            with open (file=filepath,encoding='utf-8') as f:
                filedata=f.read()
        except UnicodeDecodeError:
            with open(file=filepath,encoding='gbk') as f:
                filedata=f.read()
        sqllist=[sql.strip() for sql in filedata.split(';') if sql.strip()]
        for sql in sqllist:
            cursor.execute(sql)
        connect.commit()
    except MySQLError as e:
        if connect:
            connect.rollback()  # 发生异常，回滚
        print(f'数据库错误-{e.__class__.__name__} :  {e}')
    except Exception as e:
        print(f'{e.__class__.__name__} :  {e}')
    finally:
        if connect:
            connect.close()
        if cursor:
            cursor.close()

def get_url_last_path(url:str):

    if not url:
        raise ValueError('URL为空')
    elif '/' not in url:
        raise ValueError('格式错误')
    else:
        new_url = urlparse(url).path.rstrip('/')
        last_path = new_url.split('/')[-1]
        return last_path



if __name__ == '__main__':
    from configs.config import config
    # print(get_excel_data(r'D:\untitled1\lessons\test_data\calc测试数据.xls','加法'))
    data=database_helper(sql='select * from key_config',database='mysql',**config.LOCAL_DATABASE)
    if data:
        print(data)
    else:
        print('没有数据')
        print(data)


