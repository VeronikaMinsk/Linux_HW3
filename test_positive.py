from checks import checkout_positive
from conftest import data


def test_step1(make_folders, clear_folders, make_files, create_file_txt, write_stat_file):
    # create arch and ls-check that arc created
    res1 = checkout_positive("cd {}; 7z a {}/arx1.7z".format(data['folder_in'], data['folder_out']),
                             "Everything is Ok"), "Test1 Fail"
    res2 = checkout_positive("ls {}".format(data['folder_out']), "arx.7z"), "Test1 Fail"
    assert res1 and res2, "Test Fail"


def test_step2(clear_folders, make_files, create_file_txt, write_stat_file):
    # extract files from arc, where -o, yes -y
    res = []
    res.append(
        checkout_positive("cd {}; 7z a {}/arx1.7z".format(data['folder_in'], data['folder_out']), "Everything is Ok"))
    res.append(checkout_positive("cd {}; 7z e arx1.7z -o{} -y".format(data['folder_out'], data['folder_ext']),
                                 "Everything is Ok"))
    for item in make_files:
        res.append(checkout_positive("ls {}".format(data['folder_ext']), item))
    assert all(res)


#
def test_step3(create_file_txt, write_stat_file):
    # test arch
    assert checkout_positive("cd {}; 7z t {}/arx1.7z".format(data['folder_in'], data['folder_out']),
                             "Everything is Ok"), "Test1 Fail"


def test_step4(make_folders, clear_folders, make_files, create_file_txt, write_stat_file):
    # update arc
    assert checkout_positive("cd {}; 7z u {}/arx1.7z".format(data['folder_in'], data['folder_out']),
                             "Everything is Ok"), "Test1 Fail"


def test_step5(clear_folders, make_files, create_file_txt, write_stat_file):
    # what arch contain
    res = []
    res.append(
        checkout_positive("cd {}; 7z a {}/arx1.7z".format(data['folder_in'], data['folder_out']), "Everything is Ok"))
    for item in make_files:
        res.append(checkout_positive("cd {}; 7z l arx1.7z".format(data['folder_out']), item))
    assert all(res)


def test_step6(make_folders, clear_folders, make_files, make_subfolder, create_file_txt, write_stat_file):
    # extract files full path
    res = []
    res.append(
        checkout_positive("cd {}; 7z a {}/arx1.7z".format(data['folder_in'], data['folder_out']), "Everything is Ok"))
    res.append(checkout_positive("cd {}; 7z x arx1.7z -o{} -y".format(data['folder_out'], data['folder_ext2']),
                                 "Everything is Ok"))
    for item in make_files:
        res.append(checkout_positive("ls {};".format(data['folder_ext2']), item))

    res.append(checkout_positive("ls {};".format(data['folder_ext2']), make_subfolder[0]))
    res.append(checkout_positive("ls {}/{};".format(data['folder_ext2'], make_subfolder[0]),
                                 make_subfolder[1]))  # fall in dir {}/{}
    assert all(res)


def test_step7(create_file_txt, write_stat_file):
    assert checkout_positive("7z d {}/arx1.7z".format(data['folder_out']), "Everything is Ok"), "Test7 Fail"


def test_step10(create_file_txt, write_stat_file):
    assert checkout_positive("7z t {}/{}".format(data['folder_out'], data['name_of_arch']), "Everything is Ok"), "Test10 Fail"
