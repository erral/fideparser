import os


def get_test_file_contents(filename):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    fp = open(os.path.join(dir_path, "fide_responses", filename))
    return fp.read()


def get_path_to_store_export_files(filename):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(dir_path, "fide_responses", filename)
    return file_path
