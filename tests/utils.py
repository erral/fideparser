import os


def get_test_file_contents(filename):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    arbiter_url_file = open(os.path.join(dir_path, "fide_responses", filename))
    return arbiter_url_file.read()
