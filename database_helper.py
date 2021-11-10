import database
import pandas
import openpyxl
from json import load
pandas.set_option('display.max_colwidth', None)
pandas.set_option('display.max_columns', None)
pandas.set_option('display.max_rows', None)



d = database.Data_base()
d.create_main_table()
d.create_project_net_table()

def tvl_edit(tvl):
    res = ''
    count = 0
    for a in tvl[::-1]:
        if count == 3:
            count = 0
            res += ','
        res += a
        count += 1
    return res[::-1] + '$'


def setdata_main_table(pool_info):
    d.setdata_main_table(pool_info)

def setdata_project_net_table(data):
    d.setdata_project_net_table(data)

def creat_dataframe(data):
    df = pandas.DataFrame({'net': [elem[0] for elem in data],
                           'project': [elem[1] for elem in data],
                           'pair': [elem[2].replace('%', ' - ') for elem in data],
                           'tvl': [tvl_edit(str(elem[3])) for elem in data],
                           'apr': [str(elem[4]) + '%' for elem in data]})
    return df

def get_data_by_token(token):
    data = d.show_data_by_token(token.lstrip('W'))
    data.extend(d.show_data_by_token('W' + token.lstrip('W')))
    df = creat_dataframe(data)
    print(df.head(55))
    df.to_excel('./all_atokens_by_tvl.xlsx')

def get_data_by_net_token(net, token):
    data = d.show_data_by_net_token(net, token.lstrip('W'))
    data.extend(d.show_data_by_net_token(net, 'W' + token.lstrip('W')))
    df = creat_dataframe(data)
    print(df.head(10))

def get_all():
    data = d.get_all()
    df = pandas.DataFrame({'net': [elem[1] for elem in data],
                           'project': [elem[2] for elem in data],
                           'token1': [elem[3] for elem in data],
                           'token2': [elem[4] for elem in data],
                           'pair': [elem[5].replace('%', ' - ') for elem in data],
                           'tvl': [tvl_edit(str(elem[7])) for elem in data],
                           'apr': [str(elem[8]) + '%' for elem in data],
                           'total_staked': [elem[-1] for elem in data]})


    df.to_excel('./list_all.xlsx')

# get_data_by_token('WETH')
# get_data_by_net_token('All', 'ETH')

get_all()
