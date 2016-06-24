from conan.packager import ConanMultiPackager

if __name__ == "__main__":
#    builder = ConanMultiPackager(username="hklabbers", use_docker=True)
    builder = ConanMultiPackager(username="hklabbers", pure_c=False)
    builder.add_common_builds()
    builder.run()
