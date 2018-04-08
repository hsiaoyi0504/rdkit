from setuptools.command.build_ext import build_ext as build_ext_orig
import os
import sys
from setuptools import setup, Extension


class CMakeExtension(Extension):
    def __init__(self, name):
        # don't invoke the original build_ext for this special extension
        super().__init__(name, sources=[])


class build_ext(build_ext_orig):

    def run(self):
        for ext in self.extensions:
            self.build_cmake(ext)
        super().run()

    def build_cmake(self, ext):
        # cwd = pathlib.Path().absolute()
        cwd = os.getcwd()
        # build_temp = pathlib.Path(self.build_temp)
        # build_temp.mkdir(parents=True, exist_ok=True)
        os.makedirs(self.build_temp, exist_ok=True)
        # extdir = pathlib.Path(self.get_ext_fullpath(ext.name))
        # extdir.mkdir(parents=True, exist_ok=True)
        extdir = self.get_ext_fullpath(ext.name)
        os.makedirs(extdir, exist_ok=True)
        config = 'Debug' if self.debug else 'Release'
        cmake_args = [
            # '-DCMAKE_LIBRARY_OUTPUT_DIRECTORY=' + str(extdir),
            '-DCMAKE_LIBRARY_OUTPUT_DIRECTORY=' + extdir,
            '-DPYTHON_EXECUTABLE=' + sys.executable,
            '-DCMAKE_BUILD_TYPE=' + config
        ]
        build_args = [
            '--config', config,
            '--', '-j4'
        ]
        # os.chdir(str(build_temp))
        # os.chdir(self.build_temp)
        # self.spawn(['cmake', str(cwd)] + cmake_args)
        self.spawn(['cmake', cwd] + cmake_args)
        if not self.dry_run:
            self.spawn(['cmake', '--build', '.'] + build_args)
        # os.chdir(cwd)
        # os.chdir(str(cwd))


setup(
    name='rdkit',
    version='2017.09.3',
    install_requires=['numpy'],
    ext_modules=[CMakeExtension('rdkit')],
    include_package_data=True,
    cmdclass={
        'build_ext': build_ext,
    }
)
