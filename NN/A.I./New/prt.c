#include <stdio.h>
#include "bp.h"

void printBP(FILE *out, backProp_t *bp) {
    int i, k,j,m,n = 0;
    for (i = 0; i < bp->inputW; i++) {
        for (j = 0; j < bp->inputH; j++) {
            for (m = 0; m < bp->hiddenW; m++) {
                if( abs(m-i)<= bp->inputToHiddenSpan){
                  
                    for (k = 0; k < bp->hiddenH; k++) {
                        if( abs(k-j)<= bp->inputToHiddenSpan) 
                        fprintf(out, "weight input->hidden[%d][%d][%d][0:%d] =", i, j, k, bp->hiddenH);
                        fprintf(out, "%6.3f\n", bp->weightBottom[i][j][m][k]);
                    }
                printf("\n");
                }
            }
        }
    }
   for (i = 0; i < bp->hiddenW; i++) {
        
        for (j = 0; j < bp->hiddenH; j++) {
           fprintf(out, "weight hidden->output[%d][%d][0:%d] =", i, j, bp->outputW);
            for (k = 0; k < bp->outputW; k++) {
                printf("%f\n",bp->weightTop[i][j][k]);
            }
        }
    } 
}
