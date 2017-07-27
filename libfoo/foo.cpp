#include <pqOptions.h>
#include <pqPVApplicationCore.h>

#include <vtkNew.h>
#include <vtkObjectFactory.h>

#include "foo.h"
#include "ui_mywindow.h"

#include <clocale>

// We need to override the default options to enable streaming by default.
// Streaming needs to be enabled for the dax representations
class FooOptions : public pqOptions
{
public:
  static FooOptions* New();
  vtkTypeMacro(FooOptions, pqOptions) int GetEnableStreaming() override
  {
    return 1;
  }

protected:
  FooOptions() : pqOptions() { ; }
};
vtkStandardNewMacro(FooOptions)

namespace Goba {

MyWindow::MyWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MyWindow)
{
    int argc = 1;
    char arg0[] = "foo";
    char* argv[] = { &arg0[0], NULL };

    setlocale(LC_NUMERIC, "C");
    vtkNew<FooOptions> options;
    pvAppCore = new pqPVApplicationCore(argc, argv, options.Get());

    ui->setupUi(this);
}

MyWindow::~MyWindow()
{
    delete ui;
    delete pvAppCore;
}

void MyWindow::on_actionExit_triggered()
{
    this->close();
}

int MyWindow::squared(int x)
{
  return x * x;
}

}
