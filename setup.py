from setuptools import setup, find_packages

setup(
    name='tctim',
    use_scm_version=True,
    packages=find_packages(),
    install_requires=['numpy>=1.14.5',
                      'Pillow>=5.4.1'],
    entry_points={
        'console_scripts': [
            'tctim = tctim.cli:main'
        ]
    },
    setup_requires=[
        'setuptools_scm',
    ],
    author='chr5tphr',
    description='Package to draw images on terminals which support true-color.'
)
