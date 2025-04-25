from setuptools import setup, find_packages
from pybind11.setup_helpers import Pybind11Extension
import os

def get_header_files():
    header_files = []
    for root, dirs, files in os.walk("xgi_optimized/cpp_functions"):
        for file in files:
            if file.endswith(".h"):
                header_files.append(os.path.relpath(os.path.join(root, file), "xgi_optimized"))
    return header_files


ext_modules = [
    Pybind11Extension(
        "xgi_optimized.cpp_functions",
        sources=[
            "xgi_optimized/cpp_functions/main.cpp",
            "xgi_optimized/cpp_functions/algorithms/centrality.cpp",
            "xgi_optimized/cpp_functions/algorithms/connected.cpp",
            "xgi_optimized/cpp_functions/convert/line_graph.cpp"
        ],
        include_dirs=["extern/pybind11/include"],
        extra_compile_args=["-O3", "-Wall", "-fopenmp"],
        define_macros=[("PYBIND11", None)],
        extra_link_args=["-fopenmp"],
        cxx_std=17,
    )
]

setup(
    ext_modules=ext_modules,
		include_package_data=True,
    package_data={
        "xgi_optimized": get_header_files(),
    }
)
