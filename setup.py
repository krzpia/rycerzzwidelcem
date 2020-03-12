from setuptools import find_packages
from setuptools import setup

setup(
    name='RycerzZWidelcem',
    packages=find_packages(),
    install_requiries=[
        'pygame==2.0.0.dev6',
        'PyTMX==3.21.7',
        'PyTweening==1.0.3',
    ],
)