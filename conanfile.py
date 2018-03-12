#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, CMake, tools
import os
import shutil


class RustFPConan(ConanFile):
    name = "rustfp"
    version = "0.1.0"
    url = "https://github.com/bincrafters/conan-rustfp"
    description = "C++ implementation of Rust Option/Result and Iterator. "
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
        "optional-lite/[>=2.3.0]@bincrafters/stable",
        "variant/[>=1.3.0]@jgsogo/testing",
        "catch2/[>=2.2.0]@bincrafters/stable"
    )

    def source(self):
        source_url = "https://github.com/guangie88/rustfp"
        tools.get("{0}/archive/v{1}.tar.gz".format(source_url, self.version))
        extracted_dir = self.name + "-" + self.version

        # Work to remove 'deps' directory (conan will handle them)
        shutil.rmtree(os.path.join(extracted_dir, "deps"))
        tools.replace_in_file(os.path.join(extracted_dir, "CMakeLists.txt"), "add_subdirectory(deps/optional-lite)", "")
        tools.replace_in_file(os.path.join(extracted_dir, "CMakeLists.txt"), "add_subdirectory(deps/variant)", "")
        tools.replace_in_file(os.path.join(extracted_dir, "CMakeLists.txt"), "install(DIRECTORY deps/optional-lite/include/nonstd DESTINATION include)", "")
        tools.replace_in_file(os.path.join(extracted_dir, "CMakeLists.txt"), "$<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/deps/optional-lite/include>", "")
        tools.replace_in_file(os.path.join(extracted_dir, "CMakeLists.txt"),
'''
  target_include_directories(rustfp_unit_test
    PRIVATE
      $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/deps/Catch2/single_include>)
''',
'''
  target_include_directories(rustfp_unit_test
    PRIVATE)
''')
        tools.replace_in_file(os.path.join(extracted_dir, "CMakeLists.txt"),
'''
target_link_libraries(rustfp
  INTERFACE
    mpark_variant)
''',
'''
target_link_libraries(rustfp
  INTERFACE)
''')

        #Rename to "source_subfolder" is a convention to simplify later steps
        os.rename(extracted_dir, self.source_subfolder)

    def build(self):
        cmake = CMake(self)
        cmake.definitions["RUSTFP_INCLUDE_UNIT_TESTS"] = self.options.build_tests
        cmake.configure(build_folder=self.build_subfolder)
        cmake.build()
        if self.options.build_tests:
            # self.run(os.path.join(self.build_subfolder, 'bin', 'rustfp_unit_test'))
            pass
        cmake.install()

    def package(self):
        self.copy(pattern="LICENSE", dst="license", src=self.source_subfolder)
    
    def package_id(self):
        self.info.header_only()

