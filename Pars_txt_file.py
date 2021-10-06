from json import dump

prices = {}
pairs = []
token_in_pairs = {}
pair_plus_project_aprs = {}
pair_to_projects = {}
parameterssss = []

for i in range(1,136):

    file_name = 'txt_files_vfat/' + str(i) + '.txt'
    with open(file_name, 'r', encoding='utf-8') as file:
        a = file.readlines()

    if a[-1] == 'Oops something went wrong. Try refreshing the page.' or len(a) < 11:
        print('oops')
        continue
    for j in range(11, len(a)):
        if a[j].startswith('['):

            # print(a[1])
            # print(*a[j:j+3], a[j+5])
            token_1 = a[j+1].split()[0]
            token_2 = a[j+2].split()[0]

            pair = (sorted([token_1, token_2]))
            pair = '%'.join(pair)
            if pair == 'DAI%DEBASE':
                print(i)
            k = a[j].find(']')

            k_1 = a[j][k+1:].find(']')

            where_pair = a[j][k_1+2+k:].split()[0]
            parameterssss.append(where_pair)

            apr = a[j+5]
            tvl = a[j].split()[-1].split(',')
            tvl = ''.join(tvl)
            tvl = int(tvl[1:-3])

            project = a[1].split()[-1]

            pairs.append(pair)

            pair_to_projects[pair] = pair_to_projects.get(pair, []) + [pair + '%' + where_pair + '%' + project]


            pair_plus_project_aprs[pair + '%' + where_pair + '%' + project] = [apr, tvl]
            token_in_pairs[token_1] = token_in_pairs.get(token_1, []) +[pair]
            token_in_pairs[token_2] = token_in_pairs.get(token_2, []) +[pair]
    for key, values in pair_to_projects.items():
        pair_to_projects[key] = list(set(values))


for token in token_in_pairs:
    print(token, token_in_pairs[token], sep='\n')

    for exact_pair in token_in_pairs[token]:
        key = pair_to_projects[exact_pair]
        for i in key:
            print(exact_pair, i, pair_plus_project_aprs[i], sep='\n')
            print()

with open(r'D:\PycharmProjects\Pars_project\pars_project_vfat\alltokens.json', 'w') as file:
    dump(token_in_pairs, file, indent=4)


with open(r'D:\PycharmProjects\Pars_project\pars_project_vfat\all_pairs.json', 'w') as file:
    dump(pair_to_projects, file, indent=4)
with open(r'D:\PycharmProjects\Pars_project\pars_project_vfat\all_APRS.json', 'w') as file:
    dump(pair_plus_project_aprs, file, indent=4)
# with open ('D:\PycharmProjects\Pars_project\pars files\parameterssss.json', 'w') as file:
#     dump(parameterssss, file, indent=4)





        # print(a[10])
        # if len(a) > 10 and a[10].startswith('['):

            # step = (a[10:].index('\n'))
            # print(i, *a[10::step+1])
        # for line in a:
        #     print(line)
        # print(i, len(a), a[-1])
