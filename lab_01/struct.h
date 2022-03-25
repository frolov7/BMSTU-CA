#ifndef STRUCT_H
#define STRUCT_H

#define FILE_NAME "table.txt"

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

#define MEMORY_ALLOCATION -3
#define INPUT_ERROR -2
#define FILE_ERROR -1
#define SUCCESS 0

#define BUF_SIZE 128
#define EPS 1e-9

struct data_t{
    double **table;
    int count_str;
    int n;
    double val_arg;
};

struct result_t{
    double **table;
    int str;
    int column;
};

#endif
