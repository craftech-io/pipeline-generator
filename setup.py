from setuptools import setup, find_packages

test_requirements = ['pytest>=6.2.2', ]

setup(
    name='pipeline-generator',
    version='0.5.1',
    packages=find_packages(),
    include_package_data=True,
    package_data={'': ['templates/*.j2']},
    python_requires='>=3.6',
    install_requires=[
        'click>=7.1',
        'Jinja2>=2.11.0'
    ] + test_requirements,
    entry_points='''
        [console_scripts]
        pipeline-generator=pipeline_generator.main:generate_pipeline
    ''',
)
