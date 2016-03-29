from setuptools import setup

setup(**{
    'name': 'chrono',
    'description': 'Watches the result of graphite queries',
    'author': 'Garrett Heel',
    'author_email': 'garrettheel@gmail.com',
    'url': 'https://github.com/GarrettHeel/chrono',
    'download_url': 'N/A',
    'version': '0.1',
    'install_requires': [],
    'packages': ['chrono'],
    'include_package_data': True,
    'entry_points': {'console_scripts': ['chrono = chrono:main']},
})
