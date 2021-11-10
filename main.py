import parsvfat


from sys import argv
if len(argv) > 1:
    if argv[1] == 'update':
        driver = parsvfat.open_chrom_with_metamask()
        parsvfat.connect_vfat(driver)
        parsvfat.get_nets_and_projects(driver)
        parsvfat.get_all_txt(driver)



