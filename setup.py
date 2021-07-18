import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
  name = 'machine_learning_tools',
  version = '0.0.1',
  license='MIT',  
  description = 'A set of functions and classes to help create machine learning models.',
  long_description=long_description,
  long_description_content_type="text/markdown",
  author = 'Jony Salgado',                   # Type in your name
  author_email = 'jonysalgadofilho@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/jonysalgado/machine_learning_tools',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/jonysalgado/machine_learning_tools/archive/refs/tags/pre-release.tar.gz',   
  install_requires=[ 
        'pandas',
        'nltk',
        'numpy'
       ],
    package_dir={"": "source"},
    packages=setuptools.find_packages(where="source"),
    python_requires=">=3.6",
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Operating System :: Microsoft :: Windows'
  ],
)