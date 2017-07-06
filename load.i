%module load
%{
#define SWIG_FILE_WITH_INIT
#include "load.h"
%}

const char * loadFile(const char *filename);