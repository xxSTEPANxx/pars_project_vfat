import database
import pandas
import pandas.io.formats.excel


pandas.set_option('display.max_colwidth', None)
pandas.set_option('display.max_columns', None)
pandas.set_option('display.max_rows', None)

def database_start():
    d = database.Data_base()
    d.create_main_table()
    d.create_project_net_table()
    return d

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


def setdata_main_table(d, pool_info):
    d.setdata_main_table(pool_info)

def setdata_project_net_table(d, data):
    d.setdata_project_net_table(data)

def creat_dataframe(data):
    df = pandas.DataFrame({'net': [elem[0] for elem in data],
                           'project': [elem[1] for elem in data],
                           'pair': [elem[2].replace('%', ' - ') for elem in data],
                           'tvl': [tvl_edit(str(elem[3])) for elem in data],
                           'apr': [str(elem[4]) + '%' for elem in data]})
    return df

def get_data_by_token(d, token):
    data = d.show_data_by_token(token.lstrip('W'))
    data.extend(d.show_data_by_token('W' + token.lstrip('W')))
    df = creat_dataframe(data)
    print(df.head(55))
    df.to_excel('./all_atokens_by_tvl.xlsx')

def get_data_by_net_token(d, net, token):
    data = d.show_data_by_net_token(net, token.lstrip('W'))
    data.extend(d.show_data_by_net_token(net, 'W' + token.lstrip('W')))
    df = creat_dataframe(data)
    print(df.head(10))

def get_all(d):
    data = d.get_all()
    df = pandas.DataFrame({'net': [elem[1] for elem in data],
                           'project': [elem[2] for elem in data],
                           'token1': [elem[3] for elem in data],
                           'token2': [elem[4] for elem in data],
                           'pair': [elem[5].replace('%', ' - ') for elem in data],
                           # 'tvl': [tvl_edit(str(elem[7])) for elem in data],  ## для показа в формате строки
                           # 'apr': [str(elem[8]) + '%' for elem in data],
                           'tvl': [elem[7] for elem in data],
                           'apr': [elem[8]/100 for elem in data],
                           'total_staked': [elem[-1] for elem in data]})
    writer = pandas.ExcelWriter('./pandas_multiple.xlsx', engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Sheet1')
    workbook = writer.book
    money = workbook.add_format({'num_format': '$#,##0'})
    percentile = workbook.add_format({'num_format': '0 %'})
    pandas.io.formats.excel.header_style = None


    column_width = 20

    worksheet = writer.sheets['Sheet1']


    worksheet.set_column(6, 8, None, money)
    worksheet.set_column(7, 7, None, percentile)
    worksheet.set_column(0, 8, column_width)
    worksheet.autofilter(0, 0, df.shape[0] +1 , 8)

    writer.save()


    # df.to_excel('./list_all.xlsx')

