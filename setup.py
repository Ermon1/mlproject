from setuptools import setup, find_packages

from typing import List
def get_requirements(file_path:str) -> List[str]:
    """
    This function reads a requirements file and returns a list of requirements.
    It removes any comments or empty lines from the file.
    """
    requirements = []
    
    with open(file_path) as file_obj:
        requirements = file_obj.readlines()
        requirements = [req.replace('\n', '') for req in requirements if req.strip() and not req.startswith('#')]
        
        if '-e .' in requirements:
            requirements.remove('-e .')
            
    return requirements
    

setup(
    name='mlproject',
    version='0.1',
    author="Ermias Brhane",
    author_email="ermiasbirhanebabi@gmail.com",
    packages=find_packages(),
    install_requires = get_requirements('requirements.txt'),
    description="A machine learning project template",
    )

# This setup script is used to package the project as a Python module.
# It uses setuptools to find all packages in the project directory.
# The name of the package is 'mlproject' and its version is '0.1'.
# The find_packages() function automatically discovers all packages and subpackages in the project.
# This allows for easy installation and distribution of the project as a Python package.
# To install the package, run: pip install -e .
# The '-e' flag installs the package in editable mode, allowing changes to the source code
# to be reflected without needing to reinstall the package.
