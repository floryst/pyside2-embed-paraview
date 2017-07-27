#include "foo.h"

Math::Math(QWidget *parent) :
    QMainWindow(parent)
{
}

Math::~Math()
{
}

void Math::on_actionExit_triggered()
{
    this->close();
}

int Math::squared(int x)
{
  return x * x;
}
