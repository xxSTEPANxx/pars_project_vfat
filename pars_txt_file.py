import os
import database_helper

prices = {}
pairs = []
token_in_pairs = {}
pair_plus_project_aprs = {}
pair_to_projects = {}
parameterssss = []
path = r'C:\Users\ASER\Documents\GitHub\pars_project_vfat\txt_files_vfat'


def pars_txt_files():
    d = database_helper.database_start()
    all_nets_txt_files = os.listdir(path)
    for net in all_nets_txt_files:
        number_of_txt_files_in_net = len(os.listdir(path +'\\' + net))
        for i in range(1, number_of_txt_files_in_net):

            file_name = path +'\\' + net +'\\' + str(i) + '.txt'
            if not os.path.exists(file_name):
                continue
            with open(file_name, 'r', encoding='utf-8') as file:
                file_txt = file.readlines()

            try:
                if file_txt[-1] == 'Oops something went wrong. Try refreshing the page.' or len(file_txt) < 11:
                    # print('oops')
                    continue
                for j in range(11):
                    if 'https' in file_txt[j]:
                        project = file_txt[j].split()[-1].rstrip('/')
                        break
                total_staked = -1
                if 'Total staked' in file_txt[-1]:
                    total_staked = int(('').join(file_txt[-1].split('$')[1].split('.')[0].split(',')))
                data_projects = (project, net, total_staked)
                database_helper.setdata_project_net_table(d, data_projects)


                for j in range(11, len(file_txt)):
                    if file_txt[j].find(']-[') != -1:

                        line = file_txt[j].split(']-[')
                        if len(line) != 2:
                            continue
                        if file_txt[j].split()[-2] == 'TVL:':

                            if file_txt[j].split()[-1] == '$NaN.N':
                                continue
                            tvl = file_txt[j].split()[-1].split(',')
                            tvl = ''.join(tvl)
                            tvl = int(tvl[1:-3])
                            token_1 = line[0][line[0].find('[') + 1:].lstrip('$').lstrip('1')
                            token_2 = line[1][:line[1].find(']')].lstrip('$').lstrip('1')

                            parameter = line[1].split(']')[1].split()[0].rstrip(')')

                            pair = sorted([token_1, token_2])
                            pair_to_projects =pair + [parameter, project]
                            pair = '%'.join(pair)
                            pair_to_projects = '%'.join(pair_to_projects)

                            parameterssss.append(parameter)
                            for l in range(j, len(file_txt)):

                                if file_txt[l] == '' or file_txt[l] == '\n':
                                    info_tmp = ''.join(file_txt[j:l])
                                    found = False
                                    apr_tmp = -1
                                    if 'Total APR' in info_tmp:
                                        found = True
                                        apr_tmp = info_tmp.split('Total APR')[1].split('Year')[1]
                                        apr_tmp = apr_tmp[:apr_tmp.find('\n')]
                                        apr_tmp = apr_tmp.strip().rstrip('%')
                                        if apr_tmp == 'NaN':
                                            apr_tmp = 0
                                        else:
                                            apr_tmp = float(apr_tmp)

                                    if not found and 'APR' in info_tmp:

                                        apr_tmp = info_tmp.split('APR:')[1]

                                        apr_tmp = apr_tmp.split('Year')[1]

                                        apr_tmp = apr_tmp[:apr_tmp.find('\n')]
                                        apr_tmp = apr_tmp.strip().rstrip('%')
                                        if apr_tmp == 'NaN':
                                            apr_tmp = 0
                                        elif float(apr_tmp) >= 1000000:
                                            apr_tmp = 1000000
                                        else:
                                            apr_tmp = round(float(apr_tmp), 2)

                                    pool_info = (net, project, token_1, token_2, pair, parameter, tvl, apr_tmp)
                                    d = database_helper.database_start()
                                    database_helper.setdata_main_table(d, pool_info)
                                    break
            except Exception:
                print('mistake', net, i)


#
#             j += 8
#             # pair = (sorted([token_1, token_2]))
#             # pair = '%'.join(pair)
#             # if pair == 'DAI%DEBASE':
#             #     print(i)
#             # k = a[j].find(']')
#             #
#             # k_1 = a[j][k+1:].find(']')
#
#             where_pair = a[j][k_1+2+k:].split()[0]
#             parameterssss.append(where_pair)
#
#             apr = a[j+5]
#             tvl = a[j].split()[-1].split(',')
#             tvl = ''.join(tvl)
#             tvl = int(tvl[1:-3])
#
#             project = a[1].split()[-1]
#
#             pairs.append(pair)
#
#             pair_to_projects[pair] = pair_to_projects.get(pair, []) + [pair + '%' + where_pair + '%' + project]
#
#
#             pair_plus_project_aprs[pair + '%' + where_pair + '%' + project] = [apr, tvl]
#             token_in_pairs[token_1] = token_in_pairs.get(token_1, []) +[pair]
#             token_in_pairs[token_2] = token_in_pairs.get(token_2, []) +[pair]
#     for key, values in pair_to_projects.items():
#         pair_to_projects[key] = list(set(values))
#
#
# for token in token_in_pairs:
#     print(token, token_in_pairs[token], sep='\n')
#
#     for exact_pair in token_in_pairs[token]:
#         key = pair_to_projects[exact_pair]
#         for i in key:
#             print(exact_pair, i, pair_plus_project_aprs[i], sep='\n')
#             print()
#
# with open(r'D:\PycharmProjects\Pars_project\pars_project_vfat\alltokens.json', 'w') as file:
#     dump(token_in_pairs, file, indent=4)
#
#
# with open(r'D:\PycharmProjects\Pars_project\pars_project_vfat\all_pairs.json', 'w') as file:
#     dump(pair_to_projects, file, indent=4)
# with open(r'D:\PycharmProjects\Pars_project\pars_project_vfat\all_APRS.json', 'w') as file:
#     dump(pair_plus_project_aprs, file, indent=4)
# # with open ('D:\PycharmProjects\Pars_project\pars files\parameterssss.json', 'w') as file:
# #     dump(parameterssss, file, indent=4)
#
#
#
#
#
#         # print(a[10])
#         # if len(a) > 10 and a[10].startswith('['):
#
#             # step = (a[10:].index('\n'))
#             # print(i, *a[10::step+1])
#         # for line in a:
#         #     print(line)
#         # print(i, len(a), a[-1])
