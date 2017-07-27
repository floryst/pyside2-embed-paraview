project(foo)

set(foo_SRC
 ${CMAKE_CURRENT_BINARY_DIR}/foo/foo_module_wrapper.cpp
 ${CMAKE_CURRENT_BINARY_DIR}/foo/math_wrapper.cpp
)

set(PYSIDE2_INC /home/forrestli/py2env/pyside-setup/py2env2_install/py2.7-qt5.6.2-64bit-release/include/PySide2/)


set(foo_INCLUDE_DIRECTORIES
 ${SHIBOKEN_INCLUDE_DIR}
 ${PYTHON_INCLUDE_PATH}
 ${PYSIDE_INCLUDE_DIR}
 ${PYSIDE_INCLUDE_DIR}/QtCore
 ${QT_INCLUDE_DIR}
 ${QT_QTCORE_INCLUDE_DIR}
 ${LIBFOO_DIR}
)

set(foo_LINK_LIBRARIES
# obsoleted by Qt5
 #${QT_QTCORE_LIBRARY}
 ${SHIBOKEN_PYTHON_LIBRARIES}
 ${SHIBOKEN_LIBRARY}
 ${PYSIDE_LIBRARY}
 ${LIBFOO_DIR}/build/libfoo.so
)

include_directories(foo ${foo_INCLUDE_DIRECTORIES})
add_library(foo MODULE ${foo_SRC})
set_property(TARGET foo PROPERTY PREFIX "")
# need Qt5::Core so that #include <QDebug> works.
# https://stackoverflow.com/questions/28252909/cmake-and-qt5-include-only-takes-one-argument
# The QDebug class documentation shows that qmake requires core:
#    "QT += core"
#   From: http://doc.qt.io/qt-5/qdebug.html
target_link_libraries(foo Qt5::Core Qt5::Widgets ${foo_LINK_LIBRARIES})

string (REPLACE " " ":" QTCORE_INC ${Qt5Core_INCLUDE_DIRS})
string (REPLACE " " ":" QTWIDG_INC ${Qt5Widgets_INCLUDE_DIRS})

set(QTCORE_INC /opt/Qt5.6.2/5.6/gcc_64/include/QtCore/)
set(QTWIDG_INC /opt/Qt5.6.2/5.6/gcc_64/include/QtWidgets/)

add_custom_command(OUTPUT ${foo_SRC}
 COMMAND ${GENERATOR}
 --generator-set=shiboken --enable-parent-ctor-heuristic --enable-pyside-extensions --enable-return-value-heuristic --avoid-protected-hack
 --include-paths=${QTCORE_INC}:${QTWIDG_INC}:${LIBFOO_DIR}:${PYSIDE2_INC}
 --typesystem-paths=${PYSIDE_TYPESYSTEMS}
 --output-directory=${CMAKE_CURRENT_BINARY_DIR}
 ${CMAKE_SOURCE_DIR}/foo/global.h
 ${CMAKE_CURRENT_SOURCE_DIR}/typesystem_foo.xml
 WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
 COMMENT "Running generator for libfoo..."
 )
