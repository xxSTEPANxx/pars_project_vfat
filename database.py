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

    def creat_tables(self):
        self.cur.execute("""CREATE TABLE IF NOT EXISTS tokens (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT)""")

        self.cur.execute("""CREATE TABLE IF NOT EXISTS parameters (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT )""")

        self.cur.execute("""CREATE TABLE IF NOT EXISTS projects (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT)""")

        self.cur.execute("""CREATE TABLE IF NOT EXISTS pairs
                (id INTEGER PRIMARY KEY AUTOINCREMENT, id_token_one INTEGER,
                 id_token_two INTEGER, id_parameters INTEGER, id_project INTEGER, name TEXT)""")

        self.cur.execute("""CREATE TABLE IF NOT EXISTS pair_info
        (id INTEGER PRIMARY KEY AUTOINCREMENT, id_pair INTEGER, apr INTEGER, tvl INTEGER)""")

    def setdata_tokens(self, data):
        self.cur.executemany("""INSERT INTO tokens (name) VALUES (?)""", data)
        self.con.commit()


    def setdata_projects(self, data):
        self.cur.executemany("""INSERT INTO projects (name) VALUES (?)""", data)
        self.con.commit()

    def setdata_parameters(self, data):
        self.cur.executemany("""INSERT INTO parameters (name) VALUES (?)""", data)
        self.con.commit()

    def setdata_pairs(self, data):
        spisok = []
        for key in data:
            spisok.extend(data[key])

        for element in spisok:
            tmp = element.split('%')
            cortez = []


            first_token_id = self.cur.execute(f"""SELECT id FROM tokens WHERE name = '{tmp[0]}'""")
            x = first_token_id.fetchone()
            if x is not None:
                cortez.append(int(x[0]))
            else:
                cortez.append(None)

            second_token_id = self.cur.execute(f"""SELECT id FROM tokens WHERE name = '{tmp[1]}'""")
            x = second_token_id.fetchone()
            if x is not None:
                cortez.append(int(x[0]))
            else:
                cortez.append(None)

            parameter_id = self.cur.execute(f"""SELECT id FROM parameters WHERE name = '{tmp[2]}'""")
            x = parameter_id.fetchone()
            if x is not None:
                cortez.append(int(x[0]))
            else:
                cortez.append(None)
            ##  НАДО убрать отрезание Слэша!
            if tmp[3][-1] == '/':
                tmp[3] = tmp[3][:-1]
            project_id = self.cur.execute(f"""SELECT id FROM projects WHERE name = '{tmp[3]}'""")
            x = project_id.fetchone()
            if x is not None:
                cortez.append(int(x[0]))
            else:
                cortez.append(None)

            name_pair = tmp[0] + '%' + tmp[1]
            cortez.append(name_pair)

            cortez = tuple(cortez)

            self.cur.execute("""INSERT INTO pairs (id_token_one, id_token_two,
                                                   id_parameters, id_project, name) VALUES(?, ?, ?, ?, ?)""", cortez)
        self.con.commit()

    def setdata_pair_info(self, data):

        query_1 = """SELECT id FROM tokens WHERE name = (?)"""

        query_2 = """SELECT id FROM parameters WHERE name = (?)"""

        query_3 = """SELECT id FROM projects WHERE name = (?)"""





        for key in data:
            try:

                tmp = key.split('%')
                if tmp[3][-1] == '/':
                    tmp[3] = tmp[3][:-1]
                first_token_id = self.cur.execute(f"""SELECT id FROM tokens WHERE name = '{tmp[0]}'""").fetchone()[0]
                second_token_id = self.cur.execute(f"""SELECT id FROM tokens WHERE name = '{tmp[1]}'""").fetchone()[0]

                parameter_id = self.cur.execute(f"""SELECT id FROM parameters WHERE name = '{tmp[2]}'""").fetchone()[0]
                project_id = self.cur.execute(f"""SELECT id FROM projects WHERE name = '{tmp[3]}'""").fetchone()[0]

                pair_id = self.cur.execute(f"""SELECT id FROM pairs WHERE id_token_one = '{first_token_id}' AND
                id_token_two = '{second_token_id}' AND id_parameters = '{parameter_id}' AND id_project =
                '{project_id}' """).fetchone()[0]
                # print(pair_id, data[key][0], data[key][1])

                self.cur.execute("""INSERT INTO pair_info (id_pair, apr, tvl) VALUES (?, ?, ?) """,
                                 (pair_id, data[key][0], data[key][1]))
            except TypeError:
                print(tmp, 'not found')
        self.con.commit()

    def get_by_token(self, token):
        id_token = self.cur.execute(f"""SELECT id FROM tokens WHERE name = '{token}'""").fetchone()[0]

        data = self.cur.execute(f"""SELECT id, id_project, name FROM pairs 
                             WHERE id_token_one = {id_token} OR id_token_two = {id_token}""").fetchall()
        all_pairs = []
        for pair in data:
            tvl = self.cur.execute(f"""SELECT tvl FROM pair_info WHERE id_pair = {pair[0]}""").fetchone()[0]
            project = self.cur.execute(f"""SELECT name FROM projects WHERE id = {pair[1]} """).fetchone()[0]
            k =(pair[2], project, tvl)
            all_pairs.append(k)
        all_pairs.sort(key=lambda x: x[2], reverse=True)
        print(*all_pairs, sep='\n')

    def get_by_pair(self, pair, x=True):
        pair_data = self.cur.execute((f"""SELECT id, id_project, id_parameters 
                                          FROM pairs WHERE name = '{pair}'""")).fetchall()
        data =[]
        for _ in pair_data:
            project = self.cur.execute(f"""SELECT name FROM projects WHERE id = {_[1]}""").fetchone()[0]
            tvl = self.cur.execute(f"""SELECT tvl FROM pair_info WHERE id_pair = {_[0]} """).fetchone()[0]
            parameter = self.cur.execute(f"""SELECT name FROM parameters WHERE id = {_[2]} """).fetchone()[0]
            data.append([pair, project, parameter, tvl])
        if x:
            data.sort(key=lambda y: y[3], reverse=True)
        else:
            pass  # сортировка по апр
        print(*data, sep='\n')



d = Data_base()
d.get_by_pair('WETH%arNXM')
# d.get_by_token('WETH')
# d.creat_tables()
