from setuptools import setup, find_packages

setup(
    name='oiadb',
    version='0.3.0',
    packages=find_packages(),
    description='ADB Python wrapper library with enhanced functionality and image recognition',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Tien Dung',
    author_email='example@example.com',
    url='https://github.com/tiendung102k3/oiadb',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Software Development :: Testing',
        'Topic :: Software Development :: Libraries',
    ],
    keywords='adb, android, debug, bridge, automation, testing, image recognition, opencv',
    python_requires='>=3.6',
    install_requires=[
        'opencv-python>=4.5.0',
        'numpy>=1.19.0',
    ],
    project_urls={
        'Bug Reports': 'https://github.com/tiendung102k3/oiadb/issues',
        'Source': 'https://github.com/tiendung102k3/oiadb',
    },
)
