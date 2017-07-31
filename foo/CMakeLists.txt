project(foo)

find_package(PythonLibs REQUIRED)
find_package(Shiboken2 REQUIRED)
find_package(PySide2 REQUIRED)
# Throws error: The Qt5 package requires at least one component
# https://stackoverflow.com/questions/28247137/ubuntu-cmake-what-path-to-add-to-cmake-module-path
# https://www.kdab.com/using-cmake-with-qt-5/
#find_package(Qt5 5.6.2 REQUIRED)
find_package(Qt5Widgets REQUIRED)
find_package(Qt5Core REQUIRED)

find_program(GENERATOR generatorrunner REQUIRED)
if (NOT GENERATOR)
 message(FATAL_ERROR "You need to specify GENERATOR variable (-DGENERATOR=value)")
endif()

set(foo_SRC
 ${CMAKE_CURRENT_BINARY_DIR}/foo/foo_module_wrapper.cpp
 ${CMAKE_CURRENT_BINARY_DIR}/foo/goba_wrapper.cpp
 ${CMAKE_CURRENT_BINARY_DIR}/foo/goba_mywindow_wrapper.cpp
)

set(PYSIDE2_INC ${PYSIDE_DIR}/include/PySide2/)


set(foo_INCLUDE_DIRECTORIES
 ${PYSIDE2_INC}
 ${PYSIDE2_INC}/QtGui
 ${PYSIDE2_INC}/QtWidgets
 ${SHIBOKEN_INCLUDE_DIR}
 ${PYTHON_INCLUDE_PATH}
 ${PYSIDE_INCLUDE_DIR}
 ${PYSIDE_INCLUDE_DIR}/QtCore
 ${QT_INCLUDE_DIR}
 ${QT_QTCORE_INCLUDE_DIR}
 ${LIBFOO_DIR}
)

set(foo_LINK_LIBRARIES
# need Qt5::Core so that #include <QDebug> works.
# https://stackoverflow.com/questions/28252909/cmake-and-qt5-include-only-takes-one-argument
# The QDebug class documentation shows that qmake requires core:
#    "QT += core"
#   From: http://doc.qt.io/qt-5/qdebug.html
 Qt5::Core
 Qt5::Widgets
 # obsoleted by Qt5
 #${QT_QTCORE_LIBRARY}
 ${SHIBOKEN_PYTHON_LIBRARIES}
 ${SHIBOKEN_LIBRARY}
 ${PYSIDE_LIBRARY}
 libfoo
)

include_directories(foo ${foo_INCLUDE_DIRECTORIES})
add_library(foo SHARED ${foo_SRC})
set_property(TARGET foo PROPERTY PREFIX "")
target_link_libraries(foo ${foo_LINK_LIBRARIES})

string (REPLACE " " ":" QTCORE_INC ${Qt5Core_INCLUDE_DIRS})
string (REPLACE " " ":" QTWIDG_INC ${Qt5Widgets_INCLUDE_DIRS})

set(QTCORE_INC ${QT5_DIR}/include/QtCore/)
set(QTWIDG_INC ${QT5_DIR}/include/QtWidgets/)

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
