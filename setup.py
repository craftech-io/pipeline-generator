from setuptools import setup, find_packages

test_requirements = ['pytest>=6.2.2', ]

setup(
    name='pipeline-generator',
    version='0.6.2',
    packages=find_packages(),
    include_package_data=True,
    package_data={'': ['templates/*.jinja2']},
    python_requires='>=3.6',
    install_requires=[
        'click>=8.0.3',
        'Jinja2>=3.0.2'
    ] + test_requirements,
    entry_points='''
        [console_scripts]
        pipeline-generator=pipeline_generator.main:generate_pipeline
    ''',
)
