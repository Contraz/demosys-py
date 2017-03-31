from setuptools import setup, find_packages

setup(
    name="demosys-py",
    version="0.1.0",
    description="Modern OpenGL 4.1+ Prototype Framework inspired by Django",
    url="https://github.com/Contraz/demosys-py",
    author="Einar Forselv",
    author_email="eforselv@gmail.com",
    maintainer="Einar Forselv",
    maintainer_email="eforselv@gmail.com",
    packages=find_packages(),
    include_package_data=True,
    keywords = ['opengl', 'framework'],
    classifiers=[
        'Programming Language :: Python',
        'Environment :: MacOS X',
        'Environment :: X11 Applications',
        'Intended Audience :: Developers',
        'Topic :: Multimedia :: Graphics',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
    ],
)
