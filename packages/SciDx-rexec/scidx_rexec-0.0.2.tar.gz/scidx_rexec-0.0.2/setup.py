from setuptools import setup

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(name='SciDx-rexec',
      version='0.0.2',
      description='Client library for SciDX Remote Execution',
      long_description="Client library for remote execution capabilities in "
                       "SciDx software stack with the support to DataSpaces "
                       "Data Staging framework. It provides a simple user interface "
                       "to python programmer (including jupyter notebook) to execute "
                       "arbitary user-defined functions on the remote Points-of-Presence (PoPs).",
      long_description_content_type="text/x-rst",
      author='Bo Zhang',
      author_email='bozhang@sci.utah.edu',
      url='https://github.com/sci-ndp/dxspaces',
      install_requires=requirements,
      packages=['rexec'],
     )