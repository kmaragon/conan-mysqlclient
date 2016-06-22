from conans import ConanFile, CMake
from conans.tools import download, unzip

import os, shutil

class MySQLClientConan(ConanFile):
    name = "MySQLClient"
    version = "6.1.6"
    settings = "os", "compiler", "build_type", "arch"
    url = "https://github.com/hklabbers/conan-mysqlclient.git"
    license = "GPL v2"
    author = "Hans Klabbers (hklabbers@yahoo.com)"
    exports = "CMakeLists.txt"
    generators = "cmake", "txt"

    def source(self):
        tar_file = "mysql-connector-c-%s-src.tar.gz" % self.version 
        if self.settings.os == "Linux" or self.settings.os == "Macos":
            download("http://dev.mysql.com/get/Downloads/Connector-C/%s" % tar_file, tar_file)
        else:
            download("http://dev.mysql.com/get/Downloads/Connector-C/")
        unzip(tar_file)
        shutil.move("mysql-connector-c-%s-src" % self.version, "mysqlclient")
        os.unlink(tar_file)
        shutil.move("mysqlclient/CMakeLists.txt", "mysqlclient/CMakeListsOriginal.cmake")
        shutil.move("CMakeLists.txt", "mysqlclient/CMakeLists.txt")

    def build(self):
        cmake = CMake(self.settings)
        self.run("cd mysqlclient && mkdir build && cd build && cmake .. ")
        self.run("cd mysqlclient/build && make")

    def package(self):
        self.copy("*.h", dst="include", src="mysqlclient/include")
        self.copy("*.h", dst="include", src="mysqlclient/build/include")
        self.copy("*.so", dst="lib", src="mysqlclient/build/lib")
        self.copy("*.dylib", dst="lib", src="mysqlclient/build/libmysql")
        self.copy("*.a", dst="lib", src="mysqlclient/build/lib")

    def package_info(self):
        self.cpp_info.libs = ["MySQLClient"]
