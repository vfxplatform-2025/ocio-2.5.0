# -*- coding: utf-8 -*-
import os
import sys
import shutil
import subprocess

def run_cmd(cmd, cwd=None):
    print(f"[RUN] {cmd}")
    subprocess.run(cmd, cwd=cwd, shell=True, check=True)

def clean_dir(path):
    """디렉터리 내부를 정리(.rxt 파일만 보존)."""
    if os.path.exists(path):
        print(f"🧹 Cleaning directory: {path}")
        for item in os.listdir(path):
            if item.endswith(".rxt"):
                continue
            full = os.path.join(path, item)
            if os.path.isdir(full):
                shutil.rmtree(full)
            else:
                os.remove(full)

def copy_package_py(source_path, install_root):
    """빌드된 패키지 디렉터리에 package.py 복사."""
    src = os.path.join(source_path, "package.py")
    dst = os.path.join(install_root, "package.py")
    if os.path.exists(src):
        print(f"📄 Copying package.py → {dst}")
        shutil.copy(src, dst)

def build(source_path, build_path, install_path_env, targets):
    name    = os.environ.get("REZ_BUILD_PROJECT_NAME",    "ocio")
    version = os.environ.get("REZ_BUILD_PROJECT_VERSION", "2.5.0")
    src_dir = os.path.join(source_path, f"source/OpenColorIO-{version}")
    install_root = f"/core/Linux/APPZ/packages/{name}/{version}"

    # 1) 빌드/설치 디렉터리 정리
    clean_dir(build_path)
    if "install" in targets:
        clean_dir(install_root)

    os.makedirs(build_path, exist_ok=True)

    # 2) 의존 패키지로부터 CMAKE_PREFIX_PATH 구성
    deps = [
        os.environ.get("REZ_YAML_CPP_ROOT", ""),
        os.environ.get("REZ_PYSTRING_ROOT", ""),
        os.environ.get("REZ_IMATH_ROOT", ""),
        os.environ.get("REZ_GLEW_ROOT", ""),
        os.environ.get("REZ_FREEGLUT_ROOT", ""),
        os.environ.get("REZ_OPENEXR_ROOT", ""),
        os.environ.get("REZ_ZLIB_ROOT", ""),
        os.environ.get("REZ_PYBIND11_ROOT", ""),
        os.environ.get("REZ_PYTHON_ROOT", ""),
    ]
    # 리스트를 사용하지 않고 직접 문자열에 삽입합니다.

    # 3) CMake 옵션 설정
    cmake_args = [
    f"cmake {src_dir}",
    f"-DCMAKE_INSTALL_PREFIX={install_root}",
    "-DCMAKE_BUILD_TYPE=Release",
    "-DOCIO_BUILD_APPS=ON",
    "-DOCIO_BUILD_PYTHON=ON",
    "-DOCIO_BUILD_DOCS=OFF",
    "-DOCIO_BUILD_GPU_TESTS=OFF",
    "-DOCIO_BUILD_TESTS=OFF",
    # 모든 의존성과 Python 루트를 "..."로 감싸기
    f'-DCMAKE_PREFIX_PATH="{os.environ["REZ_YAML_CPP_ROOT"]};'
                            f'{os.environ["REZ_PYSTRING_ROOT"]};'
                            f'{os.environ["REZ_IMATH_ROOT"]};'
                            f'{os.environ["REZ_GLEW_ROOT"]};'
                            f'{os.environ["REZ_FREEGLUT_ROOT"]};'
                            f'{os.environ["REZ_OPENEXR_ROOT"]};'
                            f'{os.environ["REZ_ZLIB_ROOT"]};'
                            f'{os.environ["REZ_PYBIND11_ROOT"]};'
                            f'{os.environ["REZ_PYTHON_ROOT"]}"',
    # Python3 루트와 실행파일 강제 지정
    f"-DPython_EXECUTABLE={os.environ['REZ_PYTHON_ROOT']}/bin/python3.13",
    f"-Dpystring_DIR={os.environ['REZ_PYSTRING_ROOT']}/lib/cmake/pystring",
    f"-Dpystring_DIR={os.environ['REZ_PYSTRING_ROOT']}/lib64/cmake/pystring",
    "-DCMAKE_EXE_LINKER_FLAGS=\"-lX11 -lXrandr\"",
    ]

    # 4) Configure → Build → Install
    run_cmd(" ".join(cmake_args), cwd=build_path)
    run_cmd("cmake --build . --parallel | tee build.log", cwd=build_path)

    if "install" in targets:
        run_cmd("cmake --install .", cwd=build_path)
        copy_package_py(source_path, install_root)

    print("✅ OpenColorIO build complete.")

if __name__ == "__main__":
    build(
        source_path      = os.environ["REZ_BUILD_SOURCE_PATH"],
        build_path       = os.environ["REZ_BUILD_PATH"],
        install_path_env = os.environ["REZ_BUILD_INSTALL_PATH"],
        targets          = sys.argv[1:],
    )

