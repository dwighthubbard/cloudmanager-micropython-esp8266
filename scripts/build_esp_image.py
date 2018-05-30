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


def header(message, width=80, horizspace=True):
    if horizspace:
        print('')
    if len(message) > 76:
        print('*' * 80)
        print(message)
        print('*' * 80)
        return

    width -= 4
    print(f'# {message} {"#" * width}')


def clean_micropython():
    with working_directory():
        os.chdir('micropython')
    os.system('make clean')


def install_build_requirements():
    os.system('sudo apt-get install -y make unrar-free autoconf automake libtool gcc g++ gperf flex bison texinfo gawk ncurses-dev libexpat-dev python-dev python python-serial sed git unzip bash help2man wget bzip2 libtool-bin')


def build_esp_toolchain():
    header('Building ESP toolchain')
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


def build_micropython_esp8266(install_packages=None, release=None, unix=True):
    if not install_packages:
        install_packages = ['micropython-redis-cloudclient']
    destdir = os.getcwd()
    with working_directory():
        with tempfile.TemporaryDirectory() as tempdir:
            os.chdir(tempdir)
            header('Cloning git repos')
            os.system('git clone --recursive https://github.com/micropython/micropython.git')
            if release:
                os.system('git checkout -b {0} {0}'.format(release))
            os.chdir('micropython')
            os.system('git submodule update --init')

            os.system('ls -lh')

            header('Building bytecode compiler')
            os.chdir('mpy-cross')
            os.system('make')

            if unix:
                header('Building micropython unix')
                os.chdir(os.path.join(tempdir, 'micropython/ports/unix'))
                os.system('make axtls')
                os.system('make')

            os.chdir(os.path.join(tempdir, 'micropython/ports/esp8266'))
            header('Installing firmware extra packages')
            for package in install_packages:
                print(f'Installing {package}')
                os.system('export MICROPYPATH=modules;../unix/micropython -m upip install %s' % package)

            header('Building esp8266 firmware')
            os.system('make axtls')
            os.system('make')

            header('Copying firmware to the destination')
            os.system('cp -a build/firmware-combined.bin %s/cloudmanager_micropython_esp8266/firmware' % destdir)


def build(release=None):
    bin_directory = os.path.join(os.getcwd(), 'xtensa-lx106-elf/bin')
    os.environ['PATH'] = bin_directory + ':' + os.environ.get('PATH', '')

    # Install build requirements
    install_build_requirements()

    # Build Toolchain
    if not os.path.exists('xtensa-lx106-elf/bin/esptool.py'):
        build_esp_toolchain()

    # Build the image
    build_micropython_esp8266(release=None)

    # Add modules to build image


if __name__ == '__main__':
    build(release='v1.8.6')
