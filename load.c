#include "load.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

FILE *file;
char * buf;


const char * loadFile(const char *filename)
{
	file = fopen(filename,"r");
    fseek(file, 0, SEEK_END); 
    int size = ftell(file); 
    fseek(file, 0, SEEK_SET); 
    buf = malloc(size+1);
    memset(buf, '\0', size+1);
    fread(buf, 1, size, file);
    fclose(file);

    return buf;
}
