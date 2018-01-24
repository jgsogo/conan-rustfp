#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, CMake, tools
import os


class RustFPConan(ConanFile):
    name = "rustfp"
    version = "master"  # No version numbering
    url = "https://github.com/bincrafters/conan-rustfp"
    description = "C++ implementation of Rust Option/Result and Iterator. "

    # Indicates License type of the packaged library
    license = "MIT"

    # Packages the license for the conanfile.py
    exports = ["LICENSE.md"]

    # Remove following lines if the target lib does not use cmake.
    exports_sources = ["CMakeLists.txt"]
    generators = "cmake"

    # Options may need to change depending on the packaged library.
    settings = "os", "arch", "compiler", "build_type"
    options = {"build_tests": [True, False]}
    default_options = "build_tests=True"

    # Custom attributes for Bincrafters recipe conventions
    source_subfolder = "source_subfolder"
    build_subfolder = "build_subfolder"

    # Use version ranges for dependencies unless there's a reason not to
    requires = (
        "googletests",
        "optional-lite",
        "variant"
    )

    def source(self):
        source_url = "https://github.com/guangie88/rustfp"
        tools.get("{0}/archive/{1}.tar.gz".format(source_url, self.version))
        extracted_dir = self.name + "-" + self.version

        # Work to remove 'deps' (conan will handle them)
        remove('deps')
        delete_from_file('add_subdirectory(deps))
        
        #Rename to "source_subfolder" is a convention to simplify later steps
        os.rename(extracted_dir, self.source_subfolder)

    def build(self):
        cmake = CMake(self)
        cmake.definitions["RUSTFP_INCLUDE_UNIT_TESTS"] = self.options.build_tests
        cmake.configure(build_folder=self.build_subfolder)
        cmake.build()
        if self.options.build_tests:
            # Run tests
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
