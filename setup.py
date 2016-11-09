import sys
from setuptools import setup


if __name__ == '__main__':
    setup(
        author='Dwight Hubbard',
        author_email="dwight@dwighthubbard.com",
        description='Cloudmanager esp8266 flash image',
        name='cloudmanager-micropython-esp8266',
        include_package_data=True,
        package_data={
            'cloudmanager_micropython_esp8266': ['firmware/*.bin'],
        },
        install_requires=['esptool', 'micropython-cloudmanager'],
        license='MIT',
        long_description=open('README.rst').read(),
        maintainer='Dwight Hubbard',
        maintainer_email='dwight@dwighthubbard.com',
        packages=['cloudmanager_micropython_esp8266'],
        scripts=['scripts/flash_esp_image', 'scripts/esp_terminal'],
        url='https://github.com/dwighthubbard/cloudmanager-micropython-esp8266',
        version='0.0.17',
        zip_safe=False,
    )
