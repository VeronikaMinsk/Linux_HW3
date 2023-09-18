from checks import checkout_negative
from conftest import data


def test_step8(write_stat_file):

    assert checkout_negative("cd {}; 7z e bad_arx.7z -o{} -y".format(data['folder_out'], data['folder_ext']),
                             "ERROR"), "Test8 Fail"


def test_step9(write_stat_file):

    assert checkout_negative("cd {}; 7z t bad_arx.7z".format(data['folder_out']), "ERROR"), "Test9 Fail"
