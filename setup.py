from setuptools import setup

setup(**{
    'name': 'graphite-retriever',
    'description': 'Watches the result of graphite queries',
    'author': 'Garrett Heel',
    'author_email': 'garrettheel@gmail.com',
    'url': 'https://github.com/GarrettHeel/graphite-retriever',
    'download_url': 'N/A',
    'version': '0.1',
    'install_requires': [],
    'packages': ['graphite_retriever'],
    'include_package_data': True,
    'entry_points': {'console_scripts': ['graphite-retriever = graphite_retriever:main']},
})
