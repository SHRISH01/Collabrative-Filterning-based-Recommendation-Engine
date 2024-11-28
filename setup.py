from setuptools import setup, find_packages 
from typing import List

HYPHEN_E_DOT = '-e .'

def get_requirements(file_path:str)->List[str]:
    requirements=[]
    with open(file_path ) as f:
        requirements = f.readlines()
        requirements = [req.replace("/n","")for req in requirements]


        if HYPHEN_E_DOT in requirements:
            requirements.remove(HYPHEN_E_DOT)



    return requirements


setup(name='Joke Recommendation System using Collabrative Based Filtering' ,
      version='1.0',
      author='Shrish Kamboj',
      author_email='shrishkamboz@gmail.com',
      packages= find_packages(),
      install_requires=get_requirements('requirements.txt')
      )