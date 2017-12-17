# coding=utf-8
import re
import flask
import pymysql
import settings

from flask import request, Response

app = flask.Flask(__name__)


def parse_query(query):
    """
    解析参数
    :param query:
    :return: where子句, where参数
    """
    column_mapping = {
        'title': 'title',
        'keyword': 'content',
        'company': 'company'
    }
    where_clause_list = []
    params = []

    arg_strs = query.split('||')
    for arg_str in arg_strs:
        arg_str = arg_str.replace('|', '').strip()
        match_result = re.match(r"(\w+)[= ]+[\"\'](.*)[\"\']", arg_str.strip())
        if match_result:
            key = match_result.group(1)
            value = match_result.group(2)
            if value and key in column_mapping.keys():
                where_clause = "{} like %s".format(column_mapping[key])
                if len(where_clause_list) > 0:
                    where_clause = "or " + where_clause
                where_clause_list.append(where_clause)
                params.append("%"+value+"%")

    if len(where_clause_list) == 0:
        where_clause_list.append("content like %s")
        params.append("%"+query+"%")

    return " ".join(where_clause_list), params


@app.route('/search', methods=["GET"])
def search():
    """
    解析数
    :return:
    """
    query = request.args.get('query', '').strip()

    try:
        page = int(request.args.get('p', 1))

    except Exception:
        return Response(status=400)

    conn = pymysql.connect(settings.DB_HOST, user=settings.DB_USER, passwd=settings.DB_PASSWORD, db='recruitment',
                           connect_timeout=5, charset='utf8', cursorclass=pymysql.cursors.DictCursor)
    cur = conn.cursor()

    where_clause, params = parse_query(query)

    count_sql = """
select 
  count(*) as total 
from recruitment_detail  
where  {where_clause}
""".format(where_clause=where_clause)
    cur.execute(count_sql, params)
    ret = cur.fetchall()
    if ret:
        total = ret[0]['total']
    else:
        total = 0

    main_sql = """
select 
  source_id, detail_id, title, salary, experience, education, content, company, address, url, icon
from 
  recruitment_detail 
where {where_clause}
limit %s, %s
""".format(where_clause=where_clause)
    params.append((page - 1) * 24)
    params.append(24)
    cur.execute(main_sql, params)
    ret = cur.fetchall()
    pager = {'total': int(total), 'limit': 24, 'curr_page': int(page)}
    context = {"result_list": ret, "query": query, "p": pager}
    cur.close()
    conn.close()
    return flask.render_template("result.html", **context)


@app.route('/')
def index():
    return flask.render_template("index.html")


if __name__ == '__main__':
    app.run()


