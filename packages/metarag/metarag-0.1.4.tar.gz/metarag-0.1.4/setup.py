from setuptools import setup, find_packages
from pathlib import Path

# Read the contents of README.md file with explicit UTF-8 encoding
this_directory = Path(__file__).parent
try:
    long_description = (this_directory / "README.md").read_text(encoding="utf-8")
except UnicodeDecodeError:
    # Fallback if there are encoding issues
    long_description = "MetaRAG: A multi-LLM ensemble Retrieval-Augmented Generation framework with cosine similarity ranking."

setup(
    name='metarag',
    version='0.1.4',
    description='MetaRAG: A multi-LLM ensemble Retrieval-Augmented Generation framework with cosine similarity ranking.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Nisharg Nargund',
    author_email='nisarg.nargund@gmail.com',
    url='https://github.com/OpenRAG128/META-RAG',
    openrag_urls={
        'Linkedin': 'https://in.linkedin.com/company/openrag1',
        'Bug Tracker': 'www.openrag.in',
        'Reachout to us': 'nisarg.nargund@gmail.com',
    },
    packages=find_packages(include=['metarag', 'metarag.*']),
    package_data={
        'metarag': ['*.py'],
    },
    include_package_data=True,
    install_requires=Path('requirements.txt').read_text(encoding="utf-8").splitlines(),
    python_requires='>=3.8',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
    ],
    entry_points={
        'console_scripts': [
            'metarag=metarag.cli:main',
        ],
    },
    keywords='llm, retrieval, augmented, generation, ai, nlp',
)