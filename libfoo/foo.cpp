#include "foo.h"
#include "ui_mywindow.h"

MyWindow::MyWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MyWindow)
{
    ui->setupUi(this);
}

MyWindow::~MyWindow()
{
    delete ui;
}

void MyWindow::on_actionExit_triggered()
{
    this->close();
}

int MyWindow::squared(int x)
{
  return x * x;
}
