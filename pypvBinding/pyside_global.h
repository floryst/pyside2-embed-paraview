/****************************************************************************
**
** Copyright (C) 2016 The Qt Company Ltd.
** Contact: https://www.qt.io/licensing/
**
** This file is part of PySide2.
**
** $QT_BEGIN_LICENSE:LGPL$
** Commercial License Usage
** Licensees holding valid commercial Qt licenses may use this file in
** accordance with the commercial license agreement provided with the
** Software or, alternatively, in accordance with the terms contained in
** a written agreement between you and The Qt Company. For licensing terms
** and conditions see https://www.qt.io/terms-conditions. For further
** information use the contact form at https://www.qt.io/contact-us.
**
** GNU Lesser General Public License Usage
** Alternatively, this file may be used under the terms of the GNU Lesser
** General Public License version 3 as published by the Free Software
** Foundation and appearing in the file LICENSE.LGPL3 included in the
** packaging of this file. Please review the following information to
** ensure the GNU Lesser General Public License version 3 requirements
** will be met: https://www.gnu.org/licenses/lgpl-3.0.html.
**
** GNU General Public License Usage
** Alternatively, this file may be used under the terms of the GNU
** General Public License version 2.0 or (at your option) the GNU General
** Public license version 3 or any later version approved by the KDE Free
** Qt Foundation. The licenses are as published by the Free Software
** Foundation and appearing in the file LICENSE.GPL2 and LICENSE.GPL3
** included in the packaging of this file. Please review the following
** information to ensure the GNU General Public License requirements will
** be met: https://www.gnu.org/licenses/gpl-2.0.html and
** https://www.gnu.org/licenses/gpl-3.0.html.
**
** $QT_END_LICENSE$
**
****************************************************************************/

#include <QtCore/qnamespace.h>

#if 1
  #define Q_OS_X11
#elif 0
  #define Q_OS_MAC
#elif 0
  #define Q_OS_WIN
#endif

// There are symbols in Qt that exist in Debug but
// not in release
#define QT_NO_DEBUG

// Make "signals:", "slots:" visible as access specifiers
#define QT_ANNOTATE_ACCESS_SPECIFIER(a) __attribute__((annotate(#a)))

#include "qpytextobject.h"  // PySide class

#if 1
#  if 1
#    include <QtX11Extras/QX11Info>
#  endif
#endif

// QT_WIDGETS_LIB must be defined to QSqlRelationalDelegate become visible.
// It also changes code generation in pysideqtesttouch.h
#define QT_WIDGETS_LIB

#if 1
#  include "pysideqtesttouch.h"
#endif

#ifndef QT_NO_OPENGL
// Define export macros for Windows' gl.h
#  ifdef Q_OS_WIN
#    define NOMINMAX // windows.h is pulled, sanitize
#    ifndef APIENTRY
#      define APIENTRY
#    endif
#    ifndef WINGDIAPI
#      define WINGDIAPI
#    endif
#  endif // Q_OS_WIN
#  include </usr/include/GL/gl.h>
#endif // QT_NO_OPENGL

// Here are now all configured modules appended:
#include "QtCore/QtCore"
#include "QtGui/QtGui"
#include "QtWidgets/QtWidgets"
#include "QtPrintSupport/QtPrintSupport"
#include "QtSql/QtSql"
#include "QtNetwork/QtNetwork"
#include "QtTest/QtTest"
#include "QtConcurrent/QtConcurrent"
#include "QtX11Extras/QtX11Extras"
#include "QtXml/QtXml"
#include "QtXmlPatterns/QtXmlPatterns"
#include "QtHelp/QtHelp"
#include "QtMultimedia/QtMultimedia"
#include "QtMultimediaWidgets/QtMultimediaWidgets"
#include "QtOpenGL/QtOpenGL"
#include "QtQml/QtQml"
#include "QtQuick/QtQuick"
#include "QtQuickWidgets/QtQuickWidgets"
#include "QtScript/QtScript"
#include "QtScriptTools/QtScriptTools"
#include "QtTextToSpeech/QtTextToSpeech"
#include "QtCharts/QtCharts"
#include "QtSvg/QtSvg"
#include "QtWebChannel/QtWebChannel"
#include "QtWebEngineWidgets/QtWebEngineWidgets"
#include "QtWebSockets/QtWebSockets"
