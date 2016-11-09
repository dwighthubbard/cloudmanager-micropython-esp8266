import sys
from setuptools import setup


if __name__ == '__main__':
    setup(
        author='Dwight Hubbard',
        author_email="dwight@dwighthubbard.com",
        description='Cloudmanager esp8266 flash image',
        long_description="""Utility to flash cloudmanager to esp8266""",
        name='cloudmanager-micropython-esp8266',
        include_package_data=True,
        package_data={
            'cloudmanager_micropython_esp8266': ['firmware/*.bin'],
        },
        install_requires=['esptool', 'micropython-cloudmanager'],
        license='MIT',
        maintainer='Dwight Hubbard',
        maintainer_email='dwight@dwighthubbard.com',
        packages=['cloudmanager_micropython_esp8266'],
        scripts=['scripts/flash_esp_image'],
        url='https://github.com/dhubbard/cloudmanager-micropython-esp8266',
        version='0.0.8',
        zip_safe=False,
    )
