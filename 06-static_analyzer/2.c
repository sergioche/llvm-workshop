#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int unused_variable(void){
   int un_val;

   return un_val + 10;
}

int foo(int *a){
   return *a+1;
}

int main(int argc,char** argv){
  int a;
  int b = 1;

  foo(&a);
  return foo(&b);
}
