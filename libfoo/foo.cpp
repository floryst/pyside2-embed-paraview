#include "foo.h"

MyWindow::MyWindow(QWidget *parent) :
    QMainWindow(parent)
{
}

MyWindow::~MyWindow()
{
}

void MyWindow::on_actionExit_triggered()
{
    this->close();
}

int MyWindow::squared(int x)
{
  return x * x;
}
