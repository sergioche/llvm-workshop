#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(int argc,char** argv){
  int a[10];
  int i;

  for(i=0; i<=12; i++){
    a[i] = i;
  }

  return a[3];
}
