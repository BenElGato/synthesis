#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <stdbool.h>
#include <string.h>
#include <ctype.h>

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
bool checkFirstLine(const char *filePath){
    FILE *file = fopen(filePath, "r");
    if (file == NULL) {
        perror("Error opening file");
        return 1;
    }

    int num;
    char endChar;

    // Attempt to read an integer and a character (to check for any extra characters)
    if (fscanf(file, "%d%c", &num, &endChar) == 2) {
        // Check if the character after the integer is a newline
        if (endChar == '\n') {
            printf("The first line contains only one integer.\n");
        } else {
            printf("The first line contains extra characters besides one integer.\n");
            return 0;
        }
    } else {
        printf("The first line does not contain exactly one integer.\n");
        return 0;
    }
    return 1;
}
bool checkTruthBody(const char *filePath){
    FILE *file = fopen(filePath, "r");
    if (file == NULL) {
        perror("Error opening file");
        return 0;
    }
    int n;
    fscanf(file, "%d\n", &n);
    int totalLinesRequired = (1 << n) + 1;
    int totalLinesRead = 1;

    char line[1024]; // Assuming each line won't exceed 1024 characters
    int lineNum = 1;

    while (fgets(line, sizeof(line), file)) {
        lineNum++;
        int count = 0;
        char *token = strtok(line, " \t\n");

        while (token != NULL) {
            int value;
            if (sscanf(token, "%d", &value) != 1 || (value != 0 && value != 1)) {
                printf("Invalid integer or non-binary value found on line %d.\n", totalLinesRead);
                break;
            }

            count++;
            token = strtok(NULL, " \t\n");
        }
        if (count != 2 * n) {
            printf("Line %d does not contain exactly %d integers.\n", lineNum, 2 * n);
            return 0;
        }
        totalLinesRead++;
    }
    if (totalLinesRead != totalLinesRequired) {
        printf("The file does not contain the required number of lines (%d).\n", totalLinesRequired);
        return 0;
    }
    printf("All lines correct\n");
    fclose(file);
    return 1;
}
// TODO
bool isValidInput(const char *filePath){
    return checkFirstLine(filePath) && checkTruthBody(filePath);
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
    }
    if(isReversible(filePath) == 0){
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


