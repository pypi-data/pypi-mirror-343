import argparse


def main(args=None):
    parser = argparse.ArgumentParser(description='Useless utilities')
    parser.add_argument('-v', '--version', action='version', version='1.1.5')
    args = parser.parse_args()