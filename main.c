#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <stdbool.h>
#include <string.h>


int** parseTruthTable(const char *filePath) {
    FILE *file = fopen(filePath, "r");
    char line[200];
    if (file == NULL) {
        perror("Error opening file");
        return NULL;
    }
    int variables;
    fscanf(file, "%d", &variables);
    int rows = 1 << variables;
    int columns = 2 * variables;
    int **table = malloc(rows * sizeof(int *));
    int val;
    for (int i = 0; i < rows; i++) {
        char *token = strtok(line, " |");
        table[i] = malloc(columns * sizeof(int));
        for (int j = 0; j < columns; j++) {
            fscanf(file, "%d", &val);
            table[i][j] = val;
        }
    }
    fclose(file);
    return table;
}
// TODO
bool isValidInput(const char *filePath){
    return 1;
}
// Returns True if provided function is reversible, False if not
bool isReversible(const char *filePath) {
    // TODO
    return 1;
}

// Function to print the truth table
void printTruthTable(int **table, int variables) {
    int rows = 1 << variables; // 2^n rows for n variables
    int columns = 2 * variables;
    printf("Truth Table:\n");
    for (int i = 0; i < rows; i++) {
        for (int j = 0; j < columns; j++) {
            if(j == variables){
                printf(" %d ", table[i][j]);
            } else {
                printf("%d ", table[i][j]);
            }
        }
        printf("\n");
    }
}

int main() {
    const char *filePath = "/home/benedikt/CLionProjects/synthesis/table.txt";
    if (isValidInput(filePath) == 0) {
        perror("The truth table file is not in the expected format!");
        return -1;
    } else if(isReversible(filePath) == 0){
        perror("The provided function is not reversible!");
        return -1;
    }
    int **truthTable = parseTruthTable(filePath);
    printTruthTable(truthTable, 4);


    // Free the allocated memory
    int rows = 1 << (sizeof(truthTable[0]) / sizeof(truthTable[0][0]) / 2);
    for (int i = 0; i < rows; i++) {
        free(truthTable[i]);
    }
    free(truthTable);

    return 0;
}


