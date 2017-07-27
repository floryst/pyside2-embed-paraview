#ifndef _FOO_H
#define _FOO_H

#include <QtCore>
namespace Goba {
  class Math;
}
class Math : public QObject
{
  Q_OBJECT
public:
    Math() {}
    virtual ~Math() {}
    int squared(int x);
};
#endif
