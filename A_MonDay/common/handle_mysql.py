import pymysql


class Handle_DB():
    def __init__(self):
        self.con = pymysql.connect(

        )

    def find_all(self, sql):
        # 查询查询到的所有数据
        with self.con as cur:
            cur.execute(sql)
        res = cur.fetchall()
        cur.close()
        return res

    def find_one(self,sql):
        # 查询查询到的单条数据
        with self.con as cur:
            cur.execute(sql)
        res = cur.fetchone()
        cur.close()
        return res

    def find_count(self,sql):
        with self.con as cur:
            res=cur.execute(sql)
        cur.close()
        return res

    def __del__(self):
        # 关闭连接
        self.con.close()
