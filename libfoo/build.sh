# include qt5.6.2 modules
export CMAKE_PREFIX_PATH=${CMAKE_PREFIX_PATH}:/opt/Qt5.6.2/5.6/gcc_64/lib/cmake/
export PATH=/opt/Qt5.6.2/5.6/gcc_64/bin/:${PATH}
# avoid undefined refs from libqt5gui.so
export LD_LIBRARY_PATH=/opt/Qt5.6.2/5.6/gcc_64/lib/:${LD_LIBRARY_PATH}

# include paraview
PARAVIEW_ROOT=$HOME/tomviz/build/paraview-qt_5_6_2
export CMAKE_PREFIX_PATH=${CMAKE_PREFIX_PATH}:$PARAVIEW_ROOT/lib/cmake/
export PATH=$PARAVIEW_ROOT/bin:${PATH}
export LD_LIBRARY_PATH=$PARAVIEW_ROOT/lib/:${LD_LIBRARY_PATH}

BUILDDIR=$PWD/build
mkdir -p $BUILDDIR && cd $BUILDDIR

cmake \
  ..

make
