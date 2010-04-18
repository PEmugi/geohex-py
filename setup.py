__author__ = "Shinpei Matsuura"
__date__ = "$2010/4/18 10:00:00$"
__version__ = "0.1"

from distutils.core import setup

def main():
    setup(name = 'geohex-py',
        version = '0.1',
        author = 'Shinpei Matsuura',
        author_email = 'pe@chizuwota.net',
        packages = ['geohex']
    )

if __name__ == "__main__":
    main()
