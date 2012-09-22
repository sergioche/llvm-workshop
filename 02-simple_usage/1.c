#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(int argc,char** argv){
  float a;
  double b;
  int c;
  char* d;

  a = 1.2345;
  b = a;
  c = 10;
  d = malloc(c);

  strcpy(d,"hello world");
  printf("%s\n",d);

  return 0;
}
