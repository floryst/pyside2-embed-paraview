#ifndef _FOO_H
#define _FOO_H

#include <QMainWindow>

class Math : public QMainWindow
{
  Q_OBJECT

public:
    explicit Math(QWidget* parent = 0);
    ~Math();

    int squared(int x);

private slots:
  void on_actionExit_triggered();
};
#endif
