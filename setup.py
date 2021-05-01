from setuptools import setup, find_packages
import versioneer

requirements = [
    # package requirements go here
    'python-dateutil >=2.8',
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
    keywords=['vimwiki_docx', 'vimwiki', 'pandoc', 'python', 'conda'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Text Editors',
        'Topic :: Text Editors :: Text Processing',
    ]
)
