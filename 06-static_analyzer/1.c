#include <stdio.h>
#include <stdlib.h>
#include <string.h>

char str_10[] = "0123456789";
char str_20[] = "01234567890123456789";

void rewrite_150(char *s){
  int i;

  for( i=0; i<150; i++ ){
    s[i] = (char)i;
  }
}

void* ret_mem(){
  return malloc(10);
}

int main(int argc,char** argv){
  char *dyn_str;
  char stack_str[10];

  dyn_str = malloc(10);

  memset(stack_str,0,sizeof(stack_str)+10);	//BUG #1
  memset(dyn_str,0,sizeof(dyn_str));		//BUG #2

  rewrite_150(&stack_str[0]);			//BUG #3

  strcpy(stack_str,str_10);	//BUG
  strcpy(stack_str,str_20);	//BUG
  //strncpy(str,str_10,10);
  strcat(stack_str,str_10);
  strcat(stack_str,str_10);

  dyn_str[0] = stack_str[0];
  return (int)dyn_str[0];
}
