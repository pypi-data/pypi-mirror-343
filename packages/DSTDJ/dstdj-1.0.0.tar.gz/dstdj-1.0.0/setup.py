from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='DSTDJ',
  version='1.0.0',
  description='SBMP',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Daksh Rathod',
  author_email='dakshbrathod@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords=['dstdj'], 
  packages=find_packages(),
)