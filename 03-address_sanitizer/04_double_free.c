#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(int argc,char** argv){
  char *a;

  a = malloc(10);
  a[1] = 'A';

  free(a);
  free(a);

  return 0;
}
