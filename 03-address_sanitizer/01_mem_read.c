#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(int argc,char** argv){
  int i;
  char *m = malloc(10); 

  for(i=0; i<=10; i++){
    printf("%x\n",(char)m[i]);
  }

  return 0;
}
