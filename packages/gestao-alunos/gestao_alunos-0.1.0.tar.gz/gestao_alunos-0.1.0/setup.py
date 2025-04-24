from setuptools import setup, find_packages

setup(
    name='gestao-alunos',
    version='0.1.0',
    packages=find_packages(),
    install_requires=['tabulate'],
    author='Grupo 2 MADS 2ano',
    author_email='a041011@example.com',
    description='Sistema de gestão de alunos, docentes, turmas e disciplinas.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/seuusuario/gestao-alunos',    
    python_requires='>=3.6',
)
