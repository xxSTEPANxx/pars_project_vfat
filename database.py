import sqlite3

class Data_base:

    def __init__(self):
        self.con = sqlite3.connect(r'database/vfat_1.db')
        self.cur = self.con.cursor()

    def close(self):
        self.con.close()

    def connect(self):
        self.con = sqlite3.connect(r'database/vfat_1.db')
        self.cur = self.con.cursor()

    def create_main_table(self):
        self.cur.execute("""CREATE TABLE IF NOT EXISTS main_table (id INTEGER PRIMARY KEY AUTOINCREMENT,
         net TEXT, project TEXT, token1 TEXT, token2 TEXT, pair TEXT, parameter TEXT, tvl INTEGER, apr REAL)""")


    def setdata_main_table(self, data):
        data_to_chek = self.cur.execute(f"""SELECT id FROM 
        main_table WHERE net = '{data[0]}' AND project = '{data[1]}' AND token1 = '{data[2]}' AND token2 = '{data[3]}'
        AND  pair = '{data[4]}' AND parameter = '{data[5]}'""").fetchone()

        if not data_to_chek:
            self.cur.execute("""INSERT INTO main_table (net, project, token1, token2, pair, parameter, tvl, apr)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)""", data)
        else:

            self.cur.execute(f"""UPDATE main_table SET tvl ={data[6]}, apr = {data[7]} WHERE id = {data_to_chek[0]} """)
        self.con.commit()

    def create_project_net_table(self):
        self.cur.execute("""CREATE TABLE IF NOT EXISTS project_net (id INTEGER PRIMARY KEY AUTOINCREMENT, 
        project TEXT, net TEXT, total_staked INTEGER)""")

    def setdata_project_net_table(self, data):
        self.cur.execute(f"""INSERT INTO project_net (project, net, total_staked) VALUES (?, ?, ?) """, data)

    def show_data_by_token(self, token):
        list_pairs = self.cur.execute(f"""SELECT net, project, pair, tvl, apr FROM  main_table 
        WHERE token1 =  '{token}' OR token2 = '{token}' ORDER BY tvl DESC """).fetchall()
        return list_pairs

    def show_data_by_net_token(self, net, token):
        list_pairs = self.cur.execute(f"""SELECT net, project, pair, tvl, apr FROM  main_table 
                WHERE net = '{net}' AND (token1 =  '{token}' OR token2 = '{token}') 
                ORDER BY tvl DESC """).fetchall()
        return list_pairs

    def show_data_by_pair(self, token1, token2):
        list_pairs = self.cur.execute(f"""SELECT net, project, pair, tvl, apr FROM  main_table 
                        WHERE token1 =  '{token1}' AND token2 = '{token2}' 
                        ORDER BY tvl DESC """).fetchall()
        return list_pairs

    def show_data_by_net_pair(self, net, token1, token2):
        list_pairs = self.cur.execute(f"""SELECT net, project, pair, tvl, apr FROM  main_table 
                        WHERE net = '{net}' AND (token1 =  '{token1}' AND token2 = '{token2}') 
                        ORDER BY tvl DESC """).fetchall()
        return list_pairs

    def show_all_tokens(self):
        list_tokens = self.cur.execute("""SELECT DISTINCT token1, token2 FROM main_table 
        ORDER by token1 
        """).fetchall()
        return list_tokens

    def show_all_projects(self):
        list_projects = self.cur.execute("""SELECT project, SUM(tvl) FROM main_table 
        GROUP BY project ORDER BY SUM(tvl) DESC""").fetchall()
        return list_projects

    def show_pair_by_project(self, project):
        list_projects = self.cur.execute(f"""SELECT pair, tvl FROM main_table 
        WHERE project = '{project}' ORDER BY tvl DESC""").fetchall()
        return list_projects

    def get_all(self):
        list_all = self.cur.execute("""SELECT * FROM main_table INNER JOIN project_net ON 
        main_table.project = project_net.project""").fetchall()
        return list_all



d = Data_base()
# list = d.show_pair_by_project('https://pancakeswap.finance')
# tvl_sum = sum([i[1] for i in list ])
# print(tvl_sum)
# print(*list, sep='\n')



