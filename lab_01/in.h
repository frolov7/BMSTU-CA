#ifndef INPUT_H
#define INPUT_H

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

int my_getline(char **lineptr, size_t *col, FILE *file);
int count_strings_in_file(FILE *file, int *n);

int in_table(FILE *file, double **table, int n);
void out_table(double **table, int n);

void mat_free(double **data, int n);
double **create_matrix(int n, int m);

int input(void *arg, char *type);
int in_data(FILE *file, struct data_t *data);

#endif