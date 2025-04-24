from setuptools import setup, find_packages
setup(
    name='zeropip',
    version='2.0.0',
    packages=find_packages(),
    install_requires=[],
    author='blueradiance',
    author_email='blueradiance@example.com',
    description='zip 기반 AI 모델 복원 & 저장 도구',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/blueradiance/zeropip',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
)