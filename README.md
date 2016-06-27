[![Build Status](https://travis-ci.org/hklabbers/conan-mysqlclient.svg?branch=master)](https://travis-ci.org/hklabbers/conan-mysqlclient)

# conan-mysqlclient

[Conan.io](https://conan.io) package for [MySQL Client](http://www.mysql.com) library

The packages generated with this **conanfile** can be found in [conan.io](https://conan.io/source/MySQLClient/6.1.6/hklabbers/stable).

## Build packages

Download conan client from [Conan.io](https://conan.io) and run:

    $ python build.py

If your are in Windows you should run it from a VisualStudio console in order to get "mc.exe" in path.
    
## Upload packages to server

    $ conan upload MySQLClient/6.1.6@hklabbers/stable --all
    
## Reuse the packages

### Basic setup

    $ conan install MySQLClient/6.1.6@hklabbers/stable
    
### Project setup

If you handle multiple dependencies in your project is better to add a *conanfile.txt*
    
    [requires]
    MySQLClient/6.1.6@hklabbers/stable

    [options]
    MySQLClient:shared=True # False
    
    [generators]
    cmake

Complete the installation of requirements for your project running:</small></span>

    conan install . 

Project setup installs the library (and all his dependencies) and generates the files *conanbuildinfo.txt* and *conanbuildinfo.cmake* with all the paths and variables that you need to link with your dependencies.

## Issues
This package doesn't compile with gcc 4.6 due to an issue with glibc compatibility.

This package can only be compiled with VS 12 on windows.
