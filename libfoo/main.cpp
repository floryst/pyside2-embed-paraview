#include "foo.h"
#include <QApplication>

int main(int argc, char *argv[])
{
    QApplication a(argc, argv);
    Goba::MyWindow w;
    w.show();

    return a.exec();
}
