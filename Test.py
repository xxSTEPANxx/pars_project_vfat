import database

from json import load

d = database.Data_base()
d.creat_tables()

with open(r'D:\PycharmProjects\Pars_project\pars_project_vfat\alltokens.json', 'r') as file:
    a = load(file)
    tokens = []
    for k in a:
        tokens.append([k])
tokens = [tuple(i) for i in tokens]
d.setdata_tokens(tokens)


with open(r'D:\PycharmProjects\Pars_project\pars_project_vfat\all_pairs.json', 'r') as file:
    a = load(file)
    projects = set()
    for key in a:
        for proj in a[key]:
            projects.add(proj.split('%')[-1].rstrip('/'))
    projects = list(projects)

    projects = [tuple([_]) for _ in projects]
    print(projects)
d.setdata_projects(projects)


with open(r'D:\PycharmProjects\Pars_project\pars_project_vfat\pars files\parameterssss.json', 'r') as file:
    a = load(file)
    parameters = [tuple([_]) for _ in set(a)]
    print(parameters)
d.setdata_parameters(parameters)
print(tokens)


with open(r'D:\PycharmProjects\Pars_project\pars_project_vfat\all_pairs.json', 'r') as file:
    pairs = load(file)
    d.setdata_pairs(pairs)


with open(r'D:\PycharmProjects\Pars_project\pars_project_vfat\all_APRS.json', 'r') as file:
    data = load(file)
    d.setdata_pair_info(data)

#
# with open()

