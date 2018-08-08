from setuptools import setup, find_packages

setup(
    name="demosys-py",
    version="2.0.0",
    description="Modern OpenGL 3.3+ Framework inspired by Django",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/Contraz/demosys-py",
    author="Einar Forselv",
    author_email="eforselv@gmail.com",
    maintainer="Einar Forselv",
    maintainer_email="eforselv@gmail.com",
    packages=find_packages(),
    include_package_data=True,
    keywords = ['opengl', 'framework', 'demoscene'],
    classifiers=[
        'Programming Language :: Python',
        'Environment :: MacOS X',
        'Environment :: X11 Applications',
        'Intended Audience :: Developers',
        'Topic :: Multimedia :: Graphics',
        'License :: OSI Approved :: ISC License (ISCL)',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
    ],
    install_requires=[
        'glfw==1.7.0',
        'moderngl==5.4.2',
        'pyrr==0.9.2',
        'Pillow==5.2.0',
        'pyrocket==0.2.7',
        'PyWavefront==0.4.1',
    ],
    entry_points={'console_scripts': [
        'demosys-admin = demosys.core.management:execute_from_command_line',
    ]},
)
