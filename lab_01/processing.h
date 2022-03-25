#ifndef PROCESS_H
#define PROCESS_H

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

void sort(double **data, int n);
void find_necessary_interval(struct data_t data, int *high, int *low);
void copy_table_newton(struct data_t data, double **table, int low, int high);
void copy_table_hermit(struct data_t data, double **table, int low, int high);
void copy_table_reverse_intropolation(struct data_t data, double ** table, int low, int high);

double polinom_newton(struct result_t result, int n, double value_argument);
double polinom_hermit(struct result_t result, int n, double value_argument);

int polinom_newton_work(struct data_t data, int high, int low, double *res);
int polinom_hermit_work(struct data_t data, int high, int low, double *res);
int reverse_intropolation_work(struct data_t data, int high, int low, double *res);

void test(struct data_t data, int high, int low);

#endif 