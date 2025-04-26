from setuptools import setup, find_packages

# Read the README.md for long_description
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


setup(
    name='qrzatca',  # Package name
    version='0.1.1',  # Initial release version
    description='A Python library to generate ZATCA-compliant QR codes for Saudi Arabian e-invoices.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Anirudh msv',
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
        "Topic :: Software Development :: Libraries",
    ],
    python_requires='>=3.6',
)
