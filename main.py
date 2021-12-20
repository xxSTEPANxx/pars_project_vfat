import parsvfat
import pars_txt_file
import database_helper
from sys import argv
import os


if len(argv) > 1:
    if argv[1] == 'update':
        nets = 0 if argv[-1] == 'update' else argv[-1]
        driver = parsvfat.open_chrom_with_metamask()
        parsvfat.connect_vfat(driver)
        parsvfat.get_nets_and_projects(driver)  ## собирает джейсон файл со всеми етями и проектами
        parsvfat.get_all_txt(driver, nets)
        pars_txt_file.pars_txt_files()


    if argv[1] =='excel':
        d = database_helper.database_start()
        database_helper.get_all(d)

    if argv[1] == 'start':
        if not os.path.isdir('all_json_files'):
            os.mkdir('all_json_files')
        if not os.path.isdir('Chrom'):
            os.mkdir('Chrom')
        if not os.path.isdir('database'):
            os.mkdir('database')
        if not os.path.isdir('pars files'):
            os.mkdir('pars files')
        if not os.path.isdir('temp'):
            os.mkdir('temp')
        if not os.path.isdir('txt_files_vfat'):
            os.mkdir('txt_files_vfat')







