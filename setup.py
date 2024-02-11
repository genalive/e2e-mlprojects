from setuptools import find_packages, setup
from typing import List #this function will return a list

HYPHEN_E_DOT='-e .'

def get_requirements(file_path:str)->List[str]:
    '''
    this function will return the list of requirements
    '''
    requirements=[]
    with open(file_path) as file_obj:
        requirements=file_obj.readlines()
        requirements = [req.replace("\n", "") for req in requirements]

        if HYPHEN_E_DOT in requirements:
            requirements.remove(HYPHEN_E_DOT)

#-e . ends the requirements and connects to setup.py

setup(
name='e2e-mlprojects',
version='0.0.1',
author='AO',
author_email='ga',
packages=find_packages(),
install_requires=get_requirements('requirements.txt') #['pandas', 'numpy', 'seaborn']

)