#include <stdio.h>
#include <stdlib.h>
double resultRecursion1 = 0.0;
double resultRecursion2 = 0.0;
double resultRecursion3 = 0.0;
double recursion1(double x, unsigned int i, unsigned int startIndex, double p){
  double result;
  if(startIndex == 0) resultRecursion1 = p;
  printf("currentElement = %lf, result = %lf, i = %d\n", p, resultRecursion1, i);
  if(i == 0 ) result = p;
  else{
    p = -p * x * (2.0 * startIndex - 1.0)/(2.0 * (startIndex + 1));
    resultRecursion1+=p;
    result = recursion1(x,i-1,startIndex+1,p);
  }
  return result;
}
double recursion2(double x, unsigned int i){
  double result;
  unsigned int prevIndex = i - 1;
  if(i == 0) {
    resultRecursion2 = 1.0;
    result = 1.0;
  } else {
    double prevRec = recursion2(x,i-1);
    result = -prevRec * x * (2.0 * prevIndex - 1.0)/(2.0 * (prevIndex + 1));
    resultRecursion2 += result;
  }
  printf("currentElement = %lf, result = %lf, i = %d\n", result, resultRecursion2, i);
  return result;
}
double recursion3(double x, unsigned int i, unsigned int startIndex, double p){
 double result;
 double currentEl;
    if (startIndex == 0) {
        currentEl = p;
    } else {
        currentEl = -p * x * (2.0 * (startIndex - 1) - 1.0) / (2.0 * startIndex);
    }
    if (startIndex == i) {
        result = currentEl;
    } else {
        result = recursion3(x, i, startIndex + 1, currentEl);
    }
    resultRecursion3 += currentEl;
    printf("currentEl = %lf, result = %lf, startIndex = %d\n",
           currentEl, resultRecursion3, startIndex);
    return result;
}
int main(void) {
    double x;
    unsigned int i;
    printf("Enter X: \n");
    scanf("%lf", &x);
    if(x <= -1 || x >= 1){
      printf("Invalid X");
      return 1;
    }
    printf("Enter index: \n");
    scanf("%d", &i);
    double int1 = recursion1(x,i,0,1);
    printf("Result recursive descent: %f\n", resultRecursion1);
    double int2 = recursion2(x,i);
    printf("Result recursive return: %f\n", resultRecursion2);
    double int3 = recursion3(x,i,0,1);
    printf("Result recursion combined: %f\n", resultRecursion3);

    double sum = 0;
    double result = 0;
    double firstEl = 1;
    for(unsigned int j = 0; j<=i;j++){
      if(j == 0) result = sum = firstEl;
      else{
      unsigned int lastIndex = j-1;
        result = -result * x * (2.0 * lastIndex - 1.0)/(2.0 * (lastIndex + 1));
        sum += result;
      }
    }
     printf("Result loop: %f\n", sum);
    return 0;
}
