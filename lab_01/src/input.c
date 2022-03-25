#include "../struct.h"
#include "../in.h"

int my_getline(char **lineptr, size_t *col, FILE *file){
    if (!file)
        return FILE_ERROR;

    int flag = 1;
    char str[BUF_SIZE];
    size_t str_size = 0;

    *lineptr = NULL;
    *col = 0;

    while ((flag) && (fgets(str, BUF_SIZE, file))){
        str_size = strlen(str);

        *lineptr = (char *)realloc(*lineptr, *col + str_size + 1);
        if (!(*lineptr)){
            flag = 0;
            *col = 0;
        }
        else{
            memcpy(*lineptr + *col, str, str_size);
            *col += str_size;

            (*lineptr)[(*col)] = 0;

            if ((*lineptr)[(*col) - 1] == '\n')
                flag = 0;
        }
    }

    return *col;
}

void mat_free(double **data, int n){
    for (int i = 0; i < n; i++)
        free(data[i]);
    free(data);
}

double **create_matrix(int n, int m){
    double **data = calloc(n, sizeof(double *));
    if (!data)
        return NULL;

    for (int i = 0; i < n; i++){
        data[i] = malloc(m * sizeof(double));
        if (!data[i]){
            mat_free(data, n);
            return NULL;
        }
    }

    return data;
}

int count_strings_in_file(FILE *file, int *n){
    int count = 0;
    size_t len = 0, len_t = 0;
    char *string = NULL;

    while (!feof(file)){
        if ((len_t = my_getline(&string, &len, file)) > 0)
            count++;
        if (count == 1)
            *n = ftell(file);

        free(string);
    }

    return count - 1;
}

int in_table(FILE *file, double **table, int n){
    int error = SUCCESS;

    for (int i = 0; i < n; i++){
        for (int j = 0; j < 3; j++){
            if ((error = fscanf(file, "%lf", &table[i][j])) != 1){
                printf("\x1b[31m""%s""\x1b[0m", "\nIncorrect data in file!!!\n");
                error = INPUT_ERROR;
                break;
            }

            error = SUCCESS;
        }

        if (error)
            break;
    }

    return error;
}

void out_table(double **table, int n){
    printf("\t%2s\t\t%3s\t\t\t%3s", "X", "Y", "Y'");

    for (int i = 0; i < n; i++)
        for (int j = 0; j < 3; j++){
            if (j == 0)
                printf("\n\t%5.2lf ", table[i][j]);
            else
                printf("\t\t%10.6lf ", table[i][j]);
        }
}

int input(void *arg, char *type){
    int error;

    if ((error = scanf(type, arg)) != 1){
        printf("\x1b[31m""%s""\x1b[0m", "\nIncorrect value!!!\n");
        error = INPUT_ERROR;
    }
    else
        error = SUCCESS;

    return error;
}

int in_data(FILE *file, struct data_t *data){
    int error = in_table(file, data->table, data->count_str);
    
    if (!error){
        printf("\n\nВведите степень апроксимирующего многочлена: ");
        error = input(&data->n, "%d");
        if ((!error) && (data->n < data->count_str) && (data->n >= 0)){
            printf("\n\nВведите значение х: ");
            error = input(&data->val_arg, "%lf");
            if (!error){
                printf("\n\nn = %d, x = %lf;\n", data->n, data->val_arg);
                printf("\n\nInput table from file - %s:\n", FILE_NAME);
                out_table(data->table, data->count_str);
            }
        }
        else if ((!error) && (data->n >= data->count_str)){
            printf("\x1b[31m""%s""\x1b[0m", "\nExceeding the permissible degree!!!\n");
            error = INPUT_ERROR;
        }
        else if ((!error) && (data->n < 0)){
            printf("\x1b[31m""%s""\x1b[0m", "\nIncorrect value!!!\n");
            error = INPUT_ERROR;
        }
    }

    return error;
}
