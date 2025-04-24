from setuptools import setup, find_packages

def readme():
  with open('README.md', 'r') as f:
    return f.read()

setup(
  name='package_name_my_frame',
  version='1.0.1',
  author='DimaPlP',
  author_email='pleshko.dima19@@gmail.com',
  description='Тут мой первый фрейм',
  long_description=readme(),
  long_description_content_type='text/markdown',
  url='https://github.com/DimaPlg/Diplom_progect',
  packages=find_packages(),
  install_requires=['requests>=2.25.1'],
  classifiers=[
    'Programming Language :: Python :: 3.11',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent'
  ],
  keywords='example python',
  project_urls={
    'Documentation': 'https://github.com/DimaPlg/Diplom_progect'
  },
  python_requires='>=3.7'
)