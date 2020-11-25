from setuptools import setup, find_packages
import versioneer

requirements = [
    # package requirements go here
    'python-dateutil >= 2.8',
]

setup(
    name='vimwiki_docx',
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    description="Vimwiki Diary tools for conversion to Microsoft Word docx",
    license="MIT",
    author="John D. Fisher",
    author_email='jdfenw@gmail.com',
    url='https://github.com/jfishe/vimwiki_docx',
    # packages=['vimwiki_docx'],
    packages=find_packages(where='src'),
    package_dir={'': 'src'},

    install_requires=requirements,
    keywords='vimwiki_docx',
    classifiers=[
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ]
)
