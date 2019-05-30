#include <stdio.h>
#include <stdlib.h>
#include <limits.h>
#include <math.h>

#include "bp.h"

// Random initial weight, from -1 to 1
double randWeight() {
    return ((2.0 * rand()) / INT_MAX - 1.0);
}

backProp_t *createBP(int inputW,int inputH,int hiddenW,int hiddenH,int outputW,double eta) {
    int i,k,j,m,n;
    backProp_t *bp = (backProp_t *) calloc(1, sizeof(backProp_t));
    bp->inputW = inputW;
    srand(time(0)); 
    bp->inputH = inputH;
    bp->hiddenW = hiddenW;
    bp->hiddenH = hiddenH;
    bp->outputW = outputW;
    bp->eta = eta;
    bp->inputToHiddenSpan = 1000000;
    bp->weightBottom = (double ****) calloc(bp->inputW, sizeof(double ***));
    for (i = 0; i < bp->inputW; i++) {
        bp->weightBottom[i] = (double ***) calloc(bp->inputH, sizeof(double **));
        for (j = 0; j < bp->inputH; j++) {
            bp->weightBottom[i][j] = (double **) calloc(bp->hiddenW, sizeof(double *));
            for (m = 0; m < bp->hiddenW; m++) {
                bp->weightBottom[i][j][m] = (double *) calloc(bp->hiddenH, sizeof(double));
                for (n = 0; n < bp->hiddenH; n++) {
                    if(abs(m-i) <= bp->inputToHiddenSpan && abs(n-j)<= bp->inputToHiddenSpan)
                        bp->weightBottom[i][j][m][n] = randWeight();
                }
            }
        }
    }

    bp->weightTop = (double ***) calloc(bp->hiddenW, sizeof(double **));
    for (i = 0; i < bp->hiddenW; i++) {
        bp->weightTop[i] = (double **) calloc(bp->hiddenH, sizeof(double *));
        for (j = 0; j < bp->hiddenH; j++) {
            bp->weightTop[i][j] = (double *) calloc(bp->outputW, sizeof(double));
            for (k = 0; k < bp->outputW; k++) {
                bp->weightTop[i][j][k] = randWeight();
            }
        }
    }

    bp->inputs = (double **) calloc(bp->inputW, sizeof( double * ));
    for (i = 0; i < bp->inputW; i++) {
        bp->inputs[i] = (double *) calloc(bp->inputH, sizeof(double));
        for (j = 0; j < bp->inputH; j++) {
            bp->inputs[i][j] = randWeight();
        }
    }
    bp->hidden = (double **) calloc(bp->hiddenW, sizeof( double * ));
    for (i = 0; i < bp->hiddenW; i++) {
        bp->hidden[i] = (double *) calloc(bp->hiddenH, sizeof(double));
        for (j = 0; j < bp->hiddenW; j++) {
            bp->hidden[i][j] = randWeight();
        }
    }


    bp->output = (double *) calloc(bp->outputW, sizeof(double));
    for (i = 0; i < bp->outputW; i++) {
        bp->output[i] = randWeight();
    }
    return bp;
}
//Feed forward values from inputs to hiddens to outputs
int predictBP(backProp_t *bp, double **input, double *confidence) {
    double sum;
    double nextMaxSum;
    int i,j,k,m,n;
    // Calculate hidden values
    for (m = 0; m < bp->hiddenW; m++) {
        for (n = 0; n < bp->hiddenH; n++) {
            sum = 0.0;
            for (i = 0; i < bp->inputW; i++) {
                if(abs(m-i) <= bp->inputToHiddenSpan) 
                    for (j = 0; j < bp->inputH; j++) {
                        if( abs(n-j) <= bp->inputToHiddenSpan) {
                            sum += bp->weightBottom[i][j][m][n] * input[i][j];

                        }

                    }
                bp->hidden[m][n] = 1.0 / (1.0 + exp(-sum));    // Sigmoid (logistic)

            }
            // Calculate output values
            for (k = 0; k < bp->outputW; k++) {
                sum = 0.0;
                for (i = 0; i < bp->hiddenW; i++) {
                    for (j = 0; j < bp->hiddenH; j++) {
                        sum += bp->weightTop[i][j][k] * bp->hidden[i][j];
                    }
                    bp->output[k] = 1.0 / (1.0 + exp(-sum));    // Sigmoid (logistic)
                }
                // Find highest output activation (class = i)
                int high = -1.0;
                for (k = 0; k < bp->outputW; k++) {
                    //printf("%i:%lf\n",k,bp->output[k]);
                    if ( bp->output[k] > high) {
                        i = k;
                        high = i;
                    }
                }

                // Find second largest number
                nextMaxSum = -1.0;
                for (k = 0; k < bp->outputW; k++) {
                    if (k != i) {
                        if (nextMaxSum < 0.0 || bp->output[k] > nextMaxSum) {
                            nextMaxSum = bp->output[k];
                        }
                    }
                }
            }
        }
    }
    // Set caller's variable
    //*confidence = bp->output[i] - nextMaxSum;

    return i;
}
//Feed errors backwards through hiddens to inputs, by adjusting weights
void adjustWeightsBP(backProp_t *bp, double **inputs, int actual) {


    int i, j, k, m, n;
    double sum, deriv;
    double delta[bp->outputW];

    // Propagate the error backwards
    for (k = 0; k < bp->outputW; k++) {
        sum = (k == actual) ? 1.0 : 0.0;        // 1 if correct, else 0
        sum -= bp->output[k];                   // Predicted

        delta[k] = sum * bp->output[k] * (1 - bp->output[k]);   // Derivative of logistic (sigmoid)

        // Update weights from hiddens to outputs
        for (i = 0; i < bp->hiddenW; i++) {
            for (j = 0; j < bp->hiddenH; j++) {
                bp->weightTop[i][j][k] += bp->eta * delta[k] * bp->hidden[i][j];
            }

            // Update bias from hiddens to outputs
            //bp->biasTop[k] += bp->eta * delta[k];
        }

        for (m = 0; m < bp->hiddenW; m++) {
            for (n = 0; j < bp->hiddenH; j++) {
                double d = 0;
                for (k = 0; k < bp->outputW; k++) {
                    d += bp->weightTop[m][n][k] * delta[k];
                }

                // UPDATE weights from inputs to hiddens
                for (i = 0; i < bp->inputW; i++) {
                    if(abs(m-i)<= bp->inputToHiddenSpan){ 
                        for (j = 0; j < bp->inputH; j++) {
                            if( abs(n-j) <= bp->inputToHiddenSpan) {
                                deriv = (1 - bp->hidden[m][n] * d * bp->inputs[i][j]);
                                bp->weightBottom[i][j][m][n] += bp->eta * bp->hidden[i][j] *deriv;
                            }
                        }
                    }
                }
            }


        }
    }}

