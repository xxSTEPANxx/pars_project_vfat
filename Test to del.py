from json import load

with open (r'all_json_files\all_projects_vfat.json', "r") as file:
    a = load(file)
    print(a.keys())