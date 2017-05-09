from conans import ConanFile, CMake
from conans.tools import download, unzip

import os, shutil

class MySQLClientConan(ConanFile):
    name = "MySQLClient"
    version = "6.1.6"
    settings = "os", "compiler", "build_type", "arch"
    url = "https://github.com/kmaragon/conan-mysqlclient.git"
    license = "GPL v2"
    author = "Hans Klabbers (hklabbers@yahoo.com)"
    generators = "cmake"
    exports = "CMakeLists.txt", "FindMySQL.cmake"
    options = {
            "shared": [True, False],
            "reentrant": [True, False]
    }
    default_options = "shared=False", "reentrant=False"
    description = "Fork of MySqlClient from Hans Klabbers with reentrant support that doesn't break on shared=True"

    def config(self):
        if not hasattr(self, "_count_configs"):
            self._count_configs = 1
            return
        if self.settings.compiler == "Visual Studio" and not self.options.shared:
            if "MD" in str(self.settings.compiler.runtime):
                raise Exception("Cannot use MD in mysql static library, use MT")
            elif self.settings.compiler.version != 12:
                raise Exception("MySQLClient static library will not work with VS versions != 12")

    def source(self):
        tar_file = "mysql-connector-c-%s-src.tar.gz" % self.version 
        download("http://dev.mysql.com/get/Downloads/Connector-C/%s" % tar_file, tar_file)
        unzip(tar_file)
        shutil.move("mysql-connector-c-%s-src" % self.version, "mysqlclient")
        os.unlink(tar_file)
        shutil.move("mysqlclient/CMakeLists.txt", "mysqlclient/CMakeListsOriginal.cmake")
        shutil.move("CMakeLists.txt", "mysqlclient/CMakeLists.txt")

    def build(self):
        if self.settings.compiler == "Visual Studio" and self.settings.compiler.version != 12:
            self.settings.compiler.version = 12
        cmake = CMake(self.settings)
        self.run('cd mysqlclient && mkdir build && cd build && cmake .. %s' % cmake.command_line)
        self.run("cd mysqlclient/build && cmake --build . %s" % cmake.build_config)

    def package(self):
        # Copy findMySQL.cmake to package
        self.copy("FindMySQL.cmake", ".", ".")
        
        self.copy("*.h", dst="include", src="mysqlclient/include")
        self.copy("*.h", dst="include", src="mysqlclient/build/include")
        if self.options.shared:
            self.copy("*.so*", dst="lib", src="mysqlclient/build", keep_path=False, links=True)  
            self.copy("*mysql.lib", dst="lib", src="mysqlclient/build", keep_path=False, links=True)  
            self.copy("*.dll", dst="bin", src="mysqlclient/build", keep_path=False, links=True)
            self.copy("*.dylib*", dst="lib", src="mysqlclient/build", keep_path=False, links=True)
        else:
            self.copy("*.lib", dst="lib", src="mysqlclient/build", keep_path=False, links=True)
            self.copy("*.a", dst="lib", src="mysqlclient/build", keep_path=False, links=True)

    def package_info(self):
        suffix = ""
        if self.options.reentrant:
            suffix = "_r"

        if self.settings.os == "Windows" and self.options.shared:
            self.cpp_info.libs = ["libmysql" + suffix]
        else:
            self.cpp_info.libs = ["mysqlclient" + suffix]
        if self.settings.os == "Linux" and not self.options.shared:
            self.cpp_info.libs.extend(["dl", "pthread"])

    def conan_info(self):
        if self.info.settings.compiler == "Visual Studio":
            self.info.settings.compiler.version = 12
