#!/usr/bin/env python3
import contextlib
import os
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


def build_micropython_esp8266(install_packages=None, release=None, unix=True, git_url='https://github.com/micropython/micropython.git'):
    if not install_packages:
        install_packages = ['micropython-redis-cloudclient', 'micropython-binascii']
    repo_subdir = os.path.basename(git_url).replace('.git', '')
    destdir = os.getcwd()
    with working_directory():
        with tempfile.TemporaryDirectory() as tempdir:
            os.chdir(tempdir)
            header('Cloning git repos')
            os.system(f'git clone --recursive {git_url}')
            if release:
                os.system(f'git checkout -b {release} {release}')
            # os.chdir('micropython')
            os.chdir(repo_subdir)
            os.system('git submodule update --init')

            if True or repo_subdir in ['circuitpython']:
                header('Fixing upip pypi url')
                upip_filename = f'tools/upip.py'
                upip_string = open(upip_filename).read().replace('pypi.python.org', 'pypi.org')
                open(upip_filename, 'w').write(upip_string)

            header('Building bytecode compiler')
            os.chdir('mpy-cross')
            os.system('make')

            if unix:
                header(f'Building {repo_subdir} unix')
                os.chdir(os.path.join(tempdir, f'{repo_subdir}/ports/unix'))
                os.system('make axtls')
                os.system('make')

            os.chdir(os.path.join(tempdir, f'{repo_subdir}/ports/esp8266'))
            header('Installing firmware extra packages')
            for package in install_packages:
                print(f'Installing {package}')
                os.system(f'export MICROPYPATH=modules;../unix/micropython -m upip install {package}')

            header(f'Building esp8266 {repo_subdir} firmware axtls')

            # os.system('grep "Werror" Makefile')
            if repo_subdir in ['circuitpython']:
                makefile = open('Makefile').read().replace('-Werror ', '')
                open('Makefile', 'w').write(makefile)

            os.system('make axtls')

            if True or repo_subdir in ['circuitpython']:
                # os.system('/bin/bash')
                os.system('cp -r .frozen/* modules')
                os.system('cp -r .frozen/* ../../frozen')

            header(f'Building esp8266 {repo_subdir} firmware')
            os.system('make')

            header(f'Copying firmware to the destination directory {destdir}/cloudmanager_micropython_esp8266/firmware/{repo_subdir}-firmware-combined.bin')
            os.system(f'cp -a build/firmware-combined.bin {destdir}/cloudmanager_micropython_esp8266/firmware/{repo_subdir}{"-" + release if release else ""}-firmware-combined.bin')


def build(release=None, git_url='https://github.com/micropython/micropython.git'):
    bin_directory = os.path.join(os.getcwd(), 'xtensa-lx106-elf/bin')
    os.environ['PATH'] = bin_directory + ':' + os.environ.get('PATH', '')

    # Build the image
    build_micropython_esp8266(release=release, git_url=git_url)

    # Add modules to build image


if __name__ == '__main__':
    header('Installing build requirements')
    install_build_requirements()

    # Build Toolchain
    if not os.path.exists('xtensa-lx106-elf/bin/esptool.py'):
        header('Installing the esp build toolchain')
        build_esp_toolchain()

    header('Building micropython firmware')
    build(git_url='https://github.com/micropython/micropython.git')

    header('Building micropython firmware')
    build(release='v1.8.6', git_url='https://github.com/micropython/micropython.git')

    header('Building circuitpython firmware')
    build(git_url='https://github.com/adafruit/circuitpython.git')
