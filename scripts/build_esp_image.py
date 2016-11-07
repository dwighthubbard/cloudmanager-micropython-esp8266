#!/usr/bin/env python3
import contextlib
import os
import sys
import tempfile


@contextlib.contextmanager
def working_directory():
    curdir = os.getcwd()
    try:
        yield
    finally:
        os.chdir(curdir)


def clean_micropython():
    with working_directory():
        os.chdir('micropython')
    os.system('make clean')


def install_build_requirements():
    os.system('sudo apt-get install -y make unrar-free autoconf automake libtool gcc g++ gperf flex bison texinfo gawk ncurses-dev libexpat-dev python-dev python python-serial sed git unzip bash help2man wget bzip2 libtool-bin')


def build_esp_toolchain():
    destdir = os.getcwd()
    with working_directory():
        with tempfile.TemporaryDirectory() as tempdir:
            os.chdir(tempdir)
            if 'LD_LIBRARY_PATH' in os.environ.keys():
                del os.environ['LD_LIBRARY_PATH']
            os.system('git clone --recursive https://github.com/pfalcon/esp-open-sdk.git')
            os.chdir('esp-open-sdk')
            os.system('make clean')
            os.system('git pull')
            os.system('git submodule sync')
            os.system('git submodule update --init')
            os.system('unset LD_LIBRARY_PATH;make')
            os.system('cp -a xtensa-lx106-elf %s' % destdir)
            # os.system('cp -a xtensa-lx106-elf/bin/* %s/bin' % destdir)


def build_micropython_esp8266():
    destdir = os.getcwd()
    with working_directory():
        with tempfile.TemporaryDirectory() as tempdir:
            os.chdir(tempdir)
            os.system('git clone --recursive https://github.com/micropython/micropython.git')
            os.chdir('micropython')
            os.system('git submodule update --init')

            os.chdir('mpy-cross')
            os.system('make')

            os.chdir('../unix')
            os.system('make axtls')
            os.system('make')

            os.chdir('../esp8266')
            os.system('export MICROPYPATH=modules;../unix/micropython -m upip install micropython-redis-cloudclient')
            os.system('make axtls')
            os.system('make')
            os.system('cp -a build/firmware-combined.bin %s/cloudmanager_micropython_esp8266/firmware' % destdir)


def build():
    bin_directory = os.path.join(os.getcwd(), 'xtensa-lx106-elf/bin')
    os.environ['PATH'] = bin_directory + ':' + os.environ.get('PATH', '')

    # Install build requirements
    # install_build_requirements()

    # Build Toolchain
    if not os.path.exists('xtensa-lx106-elf/bin/esptool.py'):
        build_esp_toolchain()

    # Build the image
    build_micropython_esp8266()

    # Add modules to build image


if __name__ == '__main__':
    build()
