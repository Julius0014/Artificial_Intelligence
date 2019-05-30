#ifndef BP_H
#define BP_H

typedef struct backProp {
  int inputW,inputH;
  int hiddenW,hiddenH;
  int outputW;
  int inputToHiddenSpan;//5x5 
  double eta;
  double ****weightBottom;
  double ***weightTop;
  double **inputs;
  double **hidden;
  double *output;
} backProp_t;

// Create the structure
//extern backProp_t *createBP(int nins, int nhiddens, int nouts, double eta);
extern backProp_t *createBP(int intputW, int intputH,int hiddenW, int hiddenH, int outputW,double eta);
extern void printBP(FILE *out, backProp_t *bp);

// Forward pass -- make a guess
extern int predictBP(backProp_t *bp, double **inputs, double *confidence);

// Print the feed forward pass
extern int prtPrediction(FILE *out, backProp_t *bp, double **inputs);

// Got it wrong, adjust weights
extern void adjustWeightsBP(backProp_t *bp, double **inputs, int actual);

#endif // BP_H

