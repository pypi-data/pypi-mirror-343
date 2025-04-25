from setuptools import setup

import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))
path_to_readme = os.path.join(here, "README.md")

long_description = """# Mocker db

`mocker-db` is a python module that contains mock vector database like solution built around
python dictionary data type. It contains methods necessary to interact with this 'database',
embed, search and persist.

"""

if os.path.exists(path_to_readme):
  with codecs.open(path_to_readme, encoding="utf-8") as fh:
      long_description += fh.read()

setup(
    name="mocker_db",
    packages=["mocker_db"],
    install_requires=['attrs>=23.1.0', 'httpx', 'numpy==1.26.0', 'pyyaml', 'aiohttp', 'psutil', 'gridlooper>=0.0.1', 'attrsx', 'nest_asyncio', 'requests', 'dill>=0.3.7', 'pydantic', 'pympler==1.0.1', 'fastapi', 'click==8.1.7'],
    classifiers=['Development Status :: 3 - Alpha', 'Intended Audience :: Developers', 'Intended Audience :: Science/Research', 'Programming Language :: Python :: 3', 'Programming Language :: Python :: 3.9', 'Programming Language :: Python :: 3.10', 'Programming Language :: Python :: 3.11', 'Programming Language :: Python :: 3.12', 'License :: OSI Approved :: MIT License', 'Topic :: Scientific/Engineering'],
    long_description=long_description,
    long_description_content_type='text/markdown',
    author="Kyrylo Mordan",
    author_email="parachute.repo@gmail.com",
    description="A mock handler for simulating a vector database.",
    license="mit",
    url="https://kiril-mordan.github.io/reusables/mocker_db/",
    keywords=['aa-paa-tool'],
    version="0.3.0",
    entry_points = {'console_scripts': ['mockerdb = mocker_db.cli:cli']},

    extras_require = {'torch': ['torch'], 'hnswlib': ['hnswlib==0.8.0'], 'openai': ['openai'], 'sentence-transformers': ['sentence-transformers'], 'ollama': ['ollama'], 'all': ['torch', 'hnswlib==0.8.0', 'openai', 'sentence-transformers', 'ollama']},
    include_package_data = True,
    package_data = {'mocker_db': ['mkdocs/**/*', '.paa.tracking/version_logs.csv', '.paa.tracking/release_notes.md', '.paa.tracking/lsts_package_versions.yml', '.paa.tracking/notebook.ipynb', '.paa.tracking/package_mapping.json', '.paa.tracking/package_licenses.json', '.paa.tracking/.drawio', '.paa.tracking/extra_docs/**/*', 'tests/**/*', '.paa.tracking/.paa.config', '.paa.tracking/python_modules/mocker_db.py', '.paa.tracking/python_modules/components/mocker_db_deps/mocker_similarity_search.py', '.paa.tracking/python_modules/components/mocker_db_deps/mocker_connector.py', '.paa.tracking/python_modules/components/mocker_db_deps/data_types.py', '.paa.tracking/python_modules/components/mocker_db_deps/other.py', '.paa.tracking/python_modules/components/mocker_db_deps/sentence_transformer_embedder.py', '.paa.tracking/python_modules/components/mocker_db_deps/memory_management.py', '.paa.tracking/python_modules/components/mocker_db_deps/llm_handler.py', '.paa.tracking/python_modules/components/mocker_db_deps/response_descriptions.py', '.paa.tracking/python_modules/components/mocker_db_deps/llm_filter_connector.py', '.paa.tracking/.paa.version']} ,
    )
