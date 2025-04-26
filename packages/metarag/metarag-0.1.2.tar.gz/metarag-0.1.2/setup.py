from setuptools import setup, find_packages

setup(
    name='metarag',
    version='0.1.2',
    description='MetaRAG: A multi-LLM ensemble Retrieval-Augmented Generation framework with cosine similarity ranking.',
    author='Nisharg Nargund',
    author_email='nisarg.nargund@gmail.com',
    url='https://github.com/OpenRAG128/META-RAG',  # Update with actual repo URL
    packages=find_packages(),
    install_requires=[
        'langchain',
        'langchain_groq',
        'sentence-transformers',
        'faiss-cpu',
        'numpy',
        'PyPDF2',
        'scikit-learn'
    ],
    python_requires='>=3.8',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    entry_points={
        'console_scripts': [
            'metarag=metarag.cli:main',
        ],
    },
)
