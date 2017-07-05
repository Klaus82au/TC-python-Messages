#include <stdio.h>
#include "read.h"

const char * read(){
	f = fopen("messages.txt", "r");
	char buff[1024];
	fclose(f);
	return &buff;
}