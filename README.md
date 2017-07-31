# PySide2 Embed Paraview 

This is an experimental project to embed a Paraview render window into a PySide2
Qt GUI. The goal is to explore the feasibility of embedding a Paraview view into
a Qt application (via PySide2) and controlling it through the already-existing
Paraview/Python interface.

Technologies used, and a brief explanation along with them.

- Qt 5.6.2
  - Currently the only tested Qt version. Latest Qt 5.9 might work, but has not
    been tested.
- Python 2.7
  - The desired target is 2.7, but I am interested in exploring Python 3.5+
    support.
- PySide2
  - Python 2.7 bindings to Qt5. Provides shiboken2, which will be used to
    generate a Qt widget library accessible to Python.

# Setup/Prerequisites/Building

The following instructions were tested on vanilla Ubuntu 16.0.4-2 after updating
all packages.

## CMake

First and foremost, install cmake!

## Qt 5.6.2

Download Qt 5.6.2 from the
[official Qt website](https://download.qt.io/official_releases/qt/5.6/5.6.2/).
Run the installer, and note your installation path.

The remainder of this document will assume a Qt installation directory of
`/opt/Qt5.6.2/`. This makes the Qt root directory `/opt/Qt5.6.2/5.6/gcc_64`.

## ParaView

It is recommended that you use the ParaView superbuild, found here:
<https://gitlab.kitware.com/paraview/paraview-superbuild>

Required Ubuntu packages if you don't build the superbuild.
- `python-dev`
- `libtbb2`
- `libtbb-dev`
- `libglu1-mesa-dev`
- `libxt-dev`

Get Paraview from the [Github repository](https://github.com/kitware/paraview).
```
git clone --recursive https://github.com/Kitware/ParaView.git
```

Build paraview against Qt 5.6.2 and Python 2.7 as follows:
```
export CMAKE_PREFIX_PATH=${CMAKE_PREFIX_PATH}:/opt/Qt5.6.2/5.6/gcc_64/lib/cmake/
export PATH=/opt/Qt5.6.2/5.6/gcc_64/bin/:${PATH}
export LD_LIBRARY_PATH=/opt/Qt5.6.2/5.6/gcc_64/lib/:${LD_LIBRARY_PATH}

mkdir ParaView/build && cd ParaView/ 

cmake -DCMAKE_BUILD_TYPE:STRING=RelWithDebInfo \
    -DPYTHON_LIBRARY=/usr/lib/x86_64-linux-gnu/libpython2.7.so \
    -DPYTHON_EXECUTABLE=/usr/bin/python2.7 \
    -DPYTHON_INCLUDE_DIR=/usr/include/python2.7 \
    -DBUILD_TESTING:BOOL=OFF \
    -DPARAVIEW_ENABLE_CATALYST:BOOL=OFF \
    -DPARAVIEW_ENABLE_PYTHON:BOOL=ON \
    -DPARAVIEW_QT_VERSION:STRING=5 \
    -DPARAVIEW_ENABLE_WEB:BOOL=OFF \
    -DPARAVIEW_ENABLE_EMBEDDED_DOCUMENTATION:BOOL=OFF\
    -DPARAVIEW_USE_QTHELP:BOOL=OFF \
    -DVTK_RENDERING_BACKEND:STRING=OpenGL2 \
    -DVTK_SMP_IMPLEMENTATION_TYPE:STRING=TBB \
    -DVTK_PYTHON_VERSION:STRING=2 \
    -DVTK_PYTHON_FULL_THREADSAFE:BOOL=ON \
    -DVTK_NO_PYTHON_THREADS:BOOL=OFF \
    ..

time cmake --build . -- -j4
```

## PySide2

Get `pyside-setup` from the git repo here:
<http://code.qt.io/cgit/pyside/pyside-setup.git/>

You will need to have a Clang version 3.9 or later along with any Clang
development headers. Refer to the README.md for `pyside-setup` for more info.
You will also need to export `LLVM_INSTALL_DIR` to the llvm root directory.
An example is provided below.

A quick way to get Clang 3.9 (used in this writeup) is as follows:
```
wget -O - http://apt.llvm.org/llvm-snapshot.gpg.key | sudo apt-key add -
sudo apt-add-repository "deb http://apt.llvm.org/xenial/ llvm-toolchain-xenial-3.9 main"
sudo apt-get update

sudo apt-get install clang-3.9 lldb-3.9 libclang-3.9-dev
export LLVM_INSTALL_DIR=/usr/lib/llvm-3.9/
```

Install Python dependencies:
```
pip install sphinx
```

Once you have the git repo cloned, a few modifcations are required to support
Qt 5.6.
```
cd pyside-setup/
git checkout 5.6
cd sources/pyside2-tools && git checkout 5.6 && cd ../../
cd sources/pyside2-examples && git checkout 5.6 && cd ../../
```

Now compile!
```
export MAKEFLAGS='-j4'
export CXXFLAGS='-std=c++11'
python setup.py install --qmake=/opt/Qt5.6.2/5.6/gcc_64/bin/qmake --reuse-build --ignore-git
```

This will install pyside2 and shiboken2 into
`/path/to/pyside-setup/pyside2_install/py2.7-qt5.6.2-64bit-release/`.

## pyside2-embed-paraview

libfoo is the C++ library that wraps Paraview.
foo is the C++/Shiboken2 configuration sub-project for generating the Python
wrapper.

After cloning this repository, build the project.
**You will need to look over each and every path to make sure they correspond
to the installations on your machine.** A sample build script by the name
`libfoo/build.sh` is provided, but does not have the correct paths.
```
cd pyside2-embed-paraview/
mkdir build/ && cd build/

# include qt5.6.2 modules
export CMAKE_PREFIX_PATH=${CMAKE_PREFIX_PATH}:/opt/Qt5.6.2/5.6/gcc_64/lib/cmake/
export PATH=/opt/Qt5.6.2/5.6/gcc_64/bin/:${PATH}
export LD_LIBRARY_PATH=/opt/Qt5.6.2/5.6/gcc_64/lib/:${LD_LIBRARY_PATH}

# include paraview
PARAVIEW_ROOT=$HOME/ParaView/build/
export CMAKE_PREFIX_PATH=${CMAKE_PREFIX_PATH}:$PARAVIEW_ROOT/lib/cmake/
export PATH=$PARAVIEW_ROOT/bin:${PATH}
export LD_LIBRARY_PATH=$PARAVIEW_ROOT/lib/:${LD_LIBRARY_PATH}

# include pyside2/shiboken2
export CMAKE_PREFIX_PATH=${CMAKE_PREFIX_PATH}:/path/to/pyside-setup/pyside2_install/py2.7-qt5.6.2-64bit-release/lib/cmake/

cmake \
  -DGENERATOR=/path/to/pyside-setup/pyside2_install/py2.7-qt5.6.2-64bit-release/bin/shiboken2 \
  -DPYTHON_LIBRARY=/usr/lib/x86_64-linux-gnu/libpython2.7.so \
  -DPYTHON_INCLUDE_DIR=/usr/include/python2.7 \
  ..

make -j4
```

If all compiles, you should have a `foo.so` located in `build/foo/foo.so`. That
is your python module!

# Running

You will need to set a few environment variables. A sample run script is
provided to demonstrate which variables need to be set.
```
export LD_LIBRARY_PATH=/opt/Qt5.6.2/5.6/gcc_64/lib
export PARAVIEW_LIB=$HOME/ParaView/build/lib/
export FOO_LIB=/path/to/pyside2-embed-paraview/build/foo/

python app.py
```

Now you can run the app!
```
python app.py
```

## Issues

If you run into issues with running the app, it may be related to incorrect
library search paths, or a protobuf issue I have yet to resolve.
