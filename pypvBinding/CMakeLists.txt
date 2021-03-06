project(pypvBinding)

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

set(pypvBinding_SRC
  ${CMAKE_CURRENT_BINARY_DIR}/pypvBinding/pypvbinding_module_wrapper.cpp
  ${CMAKE_CURRENT_BINARY_DIR}/pypvBinding/pvwidget_wrapper.cpp
)

set(PYSIDE2_INC ${PYSIDE_DIR}/include/PySide2/)

set(pypvBinding_INCLUDE_DIRECTORIES
 ${PYSIDE2_INC}
 ${PYSIDE2_INC}/QtGui
 ${PYSIDE2_INC}/QtWidgets
 ${SHIBOKEN_INCLUDE_DIR}
 ${PYTHON_INCLUDE_PATH}
 ${PYSIDE_INCLUDE_DIR}
 ${PYSIDE_INCLUDE_DIR}/QtCore
 ${QT_INCLUDE_DIR}
 ${QT_QTCORE_INCLUDE_DIR}
 ${LIBPVWIDGET_DIR}
)

set(pypvBinding_LINK_LIBRARIES
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
 libpvWidget
)

include_directories(pypvBinding ${pypvBinding_INCLUDE_DIRECTORIES})
add_library(pypvBinding SHARED ${pypvBinding_SRC})
set_property(TARGET pypvBinding PROPERTY PREFIX "")
target_link_libraries(pypvBinding ${pypvBinding_LINK_LIBRARIES})

set(QT5_INC ${QT5_DIR}/include)

add_custom_command(OUTPUT ${pypvBinding_SRC}
 COMMAND ${GENERATOR}
 --generator-set=shiboken --enable-parent-ctor-heuristic --enable-pyside-extensions --enable-return-value-heuristic --avoid-protected-hack
 --include-paths=${QT5_INC}:${QT5_INC}/QtCore:${QT5_INC}/QtWidgets:${LIBPVWIDGET_DIR}:${PYSIDE2_INC}:${PYSIDE2_INC}/QtGui:${PYSIDE_SRC}:/
 --typesystem-paths=${PYSIDE_TYPESYSTEMS}
 --output-directory=${CMAKE_CURRENT_BINARY_DIR}
 ${CMAKE_SOURCE_DIR}/pypvBinding/global.h
 ${CMAKE_CURRENT_SOURCE_DIR}/typesystem_pypvBinding.xml
 WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
 COMMENT "Running generator for pypvBinding..."
 )
