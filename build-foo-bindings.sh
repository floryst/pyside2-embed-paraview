cmake \
  -DGENERATOR=/home/forrestli/py2env/pyside-setup/py2env2_install/py2.7-qt5.6.2-64bit-release/bin/shiboken2 \
  -DPYTHON_LIBRARY=/usr/lib/x86_64-linux-gnu/libpython2.7.so \
  -DPYTHON_INCLUDE_DIR=/usr/include/python2.7 \
  ..
make -j8
