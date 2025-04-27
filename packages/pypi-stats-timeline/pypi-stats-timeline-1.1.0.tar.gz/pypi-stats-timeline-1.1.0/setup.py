import setuptools
import distutils.core

setuptools.setup(
    name='pypi-stats-timeline',
    version="1.1.0",
    author='@readwithai',
    long_description_content_type='text/markdown',
    author_email='talwrii@gmail.com',
    description="Fetch, maintain and query a timeline of downloads from Python's PyPI Package indexes used by pip",
    license='MIT',
    keywords='python,cli,PyPI,timeline',
    url='https://github.com/talwrii/pypi-stats-timeline',
    packages=["pypi_stats_timeline"],
    long_description=open('README.md').read(),
    entry_points={
        'console_scripts': ['pypi-stats-timeline=pypi_stats_timeline.main:main']
    },
)
