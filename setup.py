from setuptools import setup, find_packages

setup(
    name='tctim',
    version=0.1,
    packages=find_packages(),
    install_requires=['numpy>=1.14.5',
                      'Pillow>=5.4.1'],
    entry_points={
        'console_scripts': [
            'tctim = tctim.cli:main'
        ]
    },

    author='chr5tphr',
    description='Package to draw images on terminals which support true-color.'
)
