import random
import string
import subprocess
from datetime import datetime

import pytest
import yaml

from checks import checkout_positive

with open('config.yaml') as f:
    data = yaml.safe_load(f)


@pytest.fixture()
def make_folders():
    # create all path in dir
    return checkout_positive(
        "mkdir {} {} {} {} {}".format(data['folder_in'], data['folder_out'], data['folder_ext'], data['folder_bad_arx'],
                                      data['folder_ext2']), "")


@pytest.fixture()
def clear_folders():
    return checkout_positive(
        "rm -rf {}/* {}/* {}/* {}/* {}/*".format(data['folder_in'], data['folder_out'], data['folder_ext'],
                                                 data['folder_bad_arx'],
                                                 data['folder_ext2']), "")


@pytest.fixture()
def make_files():
    list_off_files = []
    for i in range(data['count']):
        filename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
        if checkout_positive(
                "cd {}; dd if=/dev/urandom of={} bs={}M count=1 iflag=fullblock".format(data['folder_in'],
                                                                                        filename, data['size_of_file']),
                ""):
            list_off_files.append(filename)
    return list_off_files


@pytest.fixture()
def make_subfolder():
    testfilename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    subfoldername = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    if not checkout_positive("cd {}; mkdir {}".format(data['folder_in'], subfoldername), ""):
        return None, None
    if not checkout_positive(
            "cd {}/{}; dd if=/dev/urandom of={} bs=1M count=1 iflag=fullblock".format(data['folder_in'], subfoldername,
                                                                                      testfilename), ""):
        return subfoldername, None
    else:
        return subfoldername, testfilename


@pytest.fixture()
def make_bad_arx(make_folders, clear_folders, make_files):
    checkout_positive("cd {}; 7z a {}/arx1.7z".format(data['folder_in'], data['folder_bad_arx']),
                      "Everything is Ok"), "Test bad Fail"
    return checkout_positive("truncate -s {}/bad_arx.7z".format(data['folder_bad_arx']), ""), "test FAIL"


@pytest.fixture(autouse=True)
def print_time():
    return datetime.now().strftime("%H:%M:%S.%f")


@pytest.fixture()
def create_file_txt():
    if checkout_positive("ls {}".format(data['folder_tst']), data['filename']):
        return True
    else:
        res = checkout_positive("cd {} ../; touch {}".format(data['folder_tst'], data['filename']), "")
        return res


def func_test(cmd):
    return subprocess.run(f'{cmd}', shell=True, stdout=subprocess.PIPE, encoding='utf-8').stdout


@pytest.fixture()
def write_stat_file(print_time, create_file_txt):
    if create_file_txt:
        file = open('{}/{}'.format('./', data['filename']), 'a')
        file.writelines('Test time:  ')
        file.write(str(print_time))
        file.write('Files quantity:  ')
        file.write(str(data['count']))
        file.write('Size of file:  ')
        file.write(str(data['size_of_file']))
        file.write(' ')
        file.write(func_test(f'cd /proc | cat loadavg'))
