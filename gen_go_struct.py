# GenTabMd.py
# 用于读取mysql指定数据库中的表，生成Markdown格式的数据字典定义
#

import sys
import argparse
import MySQLdb

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--user', help='db user name')
    parser.add_argument('-s', '--server', help='db server')
    parser.add_argument('-p', '--port', type=int, help='db port')
    parser.add_argument('-d', '--database', required=True, help='databaes name')
    parser.add_argument('-t', '--table', help='table name')
    args = parser.parse_args()

    user = args.user
    server = args.server
    port = args.port
    database = args.database
    table = args.table

    if user == "" or user is None:
        user = 'root'

    if server == "" or server is None:
        server = 'localhost'
    
    if port is None:
        port = 3306

    print('user: {0}'.format(user))
    print('host: {0}'.format(server))
    print('port: {0}'.format(port))
    print('database: {0}'.format(database))

    db_passwd = input('db passwd:')
    #db_passwd = '51dingqitest'

    conn = MySQLdb.connect(host=server, user=user, port=port, 
    passwd=db_passwd,db='information_schema',charset='utf8')

    cu = conn.cursor()

    # markdown 表格的表头
    title = '|字段|类型|空|默认|注释|'
    # markdown 表格表头的对齐方式
    justify = '|:---|:---|:-:|:--:|:---|'

    sql_cols = """select column_name,data_type,is_nullable,column_default,\
    character_maximum_length,numeric_precision,numeric_scale,column_comment \
    from columns where table_schema=%s and table_name=%s"""

    sql_tab_comment = """select table_comment from tables where table_schema=%s and table_name=%s""" 

    sql_tabs = """select table_name,table_comment from tables where table_schema=%s order by table_name"""

    # 指定表名，只生成该表的内容
    if table != "" and table is not None:
        cu.execute(sql_tab_comment, (database,table,))
        tab_comment = cu.fetchall() 

        cu.execute(sql_cols, (database,table,))
        rows = cu.fetchall()
        cols = gen_tab_md(table, rows, tab_comment[0][0])

        for i in range(len(cols)):
            print(cols[i])

    else:
        # 未指定表名，导出指定数据库的所有表
        cu.execute(sql_tabs, (database,))
        tabs = cu.fetchall()
        for i in range(len(tabs)):
            cu.execute(sql_cols, (database, tabs[i][0],))
            rows = cu.fetchall()
            cols = gen_tab_md(tabs[i][0], rows, tabs[i][1])

            for i in range(len(cols)):
                print(cols[i])
        
            print('\n')

    cu.close()
    conn.close()

def gen_tab_md(table_name, rows, table_comment):
    '''根据结果集，生成一个markdown格式的tabl，以列表方式返回'''
    results = []
    title = '|字段|类型|空|默认|注释|'
    justify = '|:---|:---|:-:|:--:|:---|'

    if len(rows) > 0 :
        results.append('### '+table_name + " " + table_comment)
        results.append(title)
        results.append(justify)

        for i in range(len(rows)):
            col = '|'
            col=col+rows[i][0]
            if rows[i][1] in('int','smallint'):
                col=col + '|'+rows[i][1]+'(' +str(rows[i][5])+')|'
            elif rows[i][1] == 'varchar' or rows[i][1] == 'char' :
                col=col + '|'+rows[i][1]+'(' +str(rows[i][4])+')|'
            elif rows[i][1] in('date','datetime','timestamp','float'):
                col=col + '|'+rows[i][1]+'|'
            elif rows[i][1] in('decimal'):
                col=col + '|'+rows[i][1]+'(' +str(rows[i][5])+','+str(rows[i][6])+')|'
            
            if rows[i][2] == 'YES':
                col = col + u'是|'
            else:
                col = col + u'否|'
            
            if rows[i][3] is None or rows[i][3] == "":
                col = col + ' |'
            else:
                col = col + rows[i][3]
            
            col =col + rows[i][7]+'|'

            results.append(col)
        
    return results

if __name__ == '__main__':
    main()