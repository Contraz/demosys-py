from setuptools import setup

setup(
    name="demosys-py",
    version="0.3.13",
    description="Modern OpenGL 3.3+ Framework inspired by Django",
    long_description=open('README.rst').read(),
    url="https://github.com/Contraz/demosys-py",
    author="Einar Forselv",
    author_email="eforselv@gmail.com",
    maintainer="Einar Forselv",
    maintainer_email="eforselv@gmail.com",
    packages=['demosys'],
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
        'PyOpenGL==3.1.0',
        'glfw==1.4.0',
        'pyrr==0.8.3',
        'Pillow==4.1.1',
        'pyrocket==0.2.5',
        # 'pygame==1.9.3',
    ],
    entry_points={'console_scripts': [
        'demosys-admin = demosys.core.management:execute_from_command_line',
    ]},
)
