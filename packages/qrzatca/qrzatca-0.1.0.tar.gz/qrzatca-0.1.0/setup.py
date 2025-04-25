from setuptools import setup, find_packages

setup(
    name='qrzatca',  # Package name
    version='0.1.0',  # Initial release version
    description='A Python library for generating ZATCA-compliant QR codes.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Your Name',
    author_email='anirudhvadakkayil@gmail.com',
    url='https://github.com/anirudhmsv/qrzatca.git',  # Your GitHub repo URL
    packages=find_packages(),
    install_requires=[
        'qrcode',
        'Pillow'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
