from conans import ConanFile, CMake
import os

default_user = "hklabbers"
default_channel = "testing"

# This easily allows to copy the package in other user or channel
channel = os.getenv("CONAN_CHANNEL", default_channel)
username = os.getenv("CONAN_USERNAME", default_user)

class MySQLClientTestPackageConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    requires = "MySQLClient/6.1.6@%s/%s" % (username, channel)
    generators = "cmake"

    def build(self):
        cmake = CMake(self.settings)
        self.run('cmake "%s" %s' % (self.conanfile_directory, cmake.command_line))
        self.run("cmake --build . %s" % cmake.build_config)

    def imports(self):
        self.copy(pattern="*.dll", dst="bin", src="bin")
        self.copy(pattern="*.dylib", dst="bin", src="lib")

    def test(self):
	self.run('cd bin && ./version')
