import os
import re
import sys
import sysconfig
import platform
import subprocess

from pathlib import Path 
from distutils.version import LooseVersion
from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext
import setuptools

import shutil  # Adicione isso no topo do arquivo

class CMakeExtension(Extension):
    def __init__(self, name, sourcedir=""):
        super().__init__(name, sources=[])
        self.sourcedir = os.path.abspath(sourcedir)

class CMakeBuild(build_ext):
    def run(self):
        try:
            out = subprocess.check_output(["cmake", "--version"])
        except OSError:
            raise RuntimeError("CMake must be installed to build the following extension: "
                               + ", ".join(e.name for e in self.extensions))

        cmake_version = LooseVersion(re.search(r"version\s*([\d.]+)", out.decode()).group(1))
        if platform.system() == "Windows" and cmake_version < "3.14":
            raise RuntimeError("CMake >= 3.14 is required on Windows")

        for ext in self.extensions:
            self.build_extension(ext)

    def build_extension(self, ext):
        extdir = os.path.abspath(os.path.dirname(self.get_ext_fullpath(ext.name)))
        prefix = sysconfig.get_config_var("LIBDIR")

        # Verificar se o PyTorch está instalado e obter o caminho do CMake do PyTorch
        try:
            import torch
            pytorch_dir = torch.utils.cmake_prefix_path
        except ImportError:
            raise RuntimeError("PyTorch must be installed to build the extension. Please run 'pip install torch'.")

        # Argumentos do CMake
        cmake_args = [
            "-DCMAKE_LIBRARY_OUTPUT_DIRECTORY=" + extdir,
            "-DPYTHON_EXECUTABLE=" + sys.executable,
            "-DPYTHON_LIBRARY_DIR={}".format(prefix),
            "-DCMAKE_PREFIX_PATH=" + pytorch_dir,  # Usar caminho do PyTorch
            "-DCMAKE_INSTALL_RPATH_USE_LINK_PATH=ON"
        ]

        cfg = "Debug" if self.debug else "Release"
        build_args = ["--config", cfg]

        # Configurações específicas para plataformas
        if platform.system() == "Windows":
            cmake_args += ["-DCMAKE_LIBRARY_OUTPUT_DIRECTORY_{}={}".format(cfg.upper(), extdir)]
            if sys.maxsize > 2**32:
                cmake_args += ["-A", "x64"]
            build_args += ["--", "/m"]
        elif platform.system() == "Darwin":
            cmake_args += ["-DCMAKE_BUILD_TYPE=" + cfg]
            cmake_args += ["-DCMAKE_OSX_DEPLOYMENT_TARGET=" + "10.15"]
            if platform.machine() == "arm64":
                cmake_args += ["-DCMAKE_OSX_ARCHITECTURES=arm64"]
            else:
                cmake_args += ["-DCMAKE_OSX_ARCHITECTURES=x86_64"]
            cmake_args += ["-DCMAKE_OSX_SYSROOT=" + subprocess.check_output(["xcrun", "--sdk", "macosx", "--show-sdk-path"]).decode().strip()]
            env = os.environ.copy()
            env["CXXFLAGS"] = '{} -stdlib=libc++ -mmacosx-version-min=10.15'.format(env.get("CXXFLAGS", ""))
            build_args += ["--", "-j2"]
        else:
            # Configurações para Linux/Unix
            cmake_args += ["-DCMAKE_BUILD_TYPE=" + cfg]
            build_args += ["--", "-j2"]

        # Adicionar variáveis de ambiente para a compilação
        env = os.environ.copy()
        env["CXXFLAGS"] = '{} -DVERSION_INFO=\\"{}\\"'.format(env.get("CXXFLAGS", ""), self.distribution.get_version()).replace('"', '\\"')

        # Criar o diretório de build se não existir
        if not os.path.exists(self.build_temp):
            os.makedirs(self.build_temp)

        # Executar o CMake
        subprocess.check_call(["cmake", ext.sourcedir] + cmake_args, cwd=self.build_temp, env=env)
        subprocess.check_call(["cmake", "--build", "."] + build_args, cwd=self.build_temp)

        # Mover o output gerado para o local correto
        self.move_output(ext)
            
    def move_output(self, ext):
        extdir = Path(self.build_lib).resolve()
        dest_path = Path(self.get_ext_fullpath(ext.name)).resolve()
        dest_directory = dest_path.parent
        expected_filename = self.get_ext_filename(ext.name)

        # Procura o arquivo .so ou .pyd gerado dentro de todo o projeto (ou build dir)
        possible_locations = [
            Path(ext.sourcedir),
            Path(self.build_temp),
            Path("."),
        ]

        for location in possible_locations:
            matches = list(location.rglob(expected_filename))
            if matches:
                source_path = matches[0]
                break
        else:
            raise RuntimeError(f"Arquivo de saída '{expected_filename}' não encontrado em {possible_locations}")

        # Garante que o diretório de destino existe
        dest_directory.mkdir(parents=True, exist_ok=True)

        # Copia o .so para o local correto (para que setuptools encontre)
        if source_path != dest_path:
            shutil.copy2(source_path, dest_path)
            print(f"✅ Copiado: {source_path} → {dest_path}")
        else:
            print(f"ℹ️ Nenhuma cópia necessária: {source_path} já está no destino final.")
        
        
    def move_output_OLD(self, ext):
        extdir = Path(self.build_lib).resolve()
        dest_path = Path(self.get_ext_fullpath(ext.name)).resolve()
        source_path = extdir / self.get_ext_filename(ext.name)
        dest_directory = dest_path.parent

        # Verificar se o arquivo foi gerado
        if not source_path.exists():
            raise RuntimeError(f"Arquivo de saída {source_path} não encontrado. Verifique se o CMake gerou corretamente o arquivo .so.")

        # Criar diretório de destino se necessário e mover o arquivo
        dest_directory.mkdir(parents=True, exist_ok=True)
        self.copy_file(source_path, dest_path)

        



        
# Verifica o sistema operacional atual
system = platform.system()

# Define a extensão do arquivo nativo com base no sistema operacional
if system == "Linux":
    native_ext = "*.so"
elif system == "Darwin":
    native_ext = "*.so"  # Para macOS, o Pybind gera .so, mas você pode usar *.dylib para bibliotecas dinâmicas
elif system == "Windows":
    native_ext = "*.dll"
else:
    raise RuntimeError(f"Plataforma {system} não suportada!")

setup(
    name="ctreelearn",
    version="0.2.3",
    description="A simple library for learning of connected filters based on component trees",
    long_description="",
    author="Wonder Alexandre Luz Alves",
    author_email="worderalexandre@gmail.com",
    license="GPL-3.0",
    url="https://github.com/wonderalexandre/ComponentTreeLearn",
    keywords="machine learning, morphological trees, mathematical morphology",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Image Processing",
        "Programming Language :: Python",
        "Programming Language :: C++",
    ],
    # Certificar-se de que as dependências necessárias estão instaladas
    setup_requires=["setuptools", "wheel", "cmake>=3.14"],
    ext_modules=[CMakeExtension('ctreelearn')],
    cmdclass=dict(build_ext=CMakeBuild),
    zip_safe=False,
    packages=["ctl"],  # Definindo o pacote ctreelearn
    package_dir={"ctl": "python"},  # Atribuindo o diretório "python" ao pacote "ctreelearn"
    package_data={
        "ctl": ["*.py", native_ext],  # Incluindo todos os arquivos Python no pacote e os modelos c++/pybinds
    },
)
 

#send to pypi
#1. python setup.py sdist
#2. pipenv run twine upload dist/* -r pypi