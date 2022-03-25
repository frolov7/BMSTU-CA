#include "../struct.h"
#include "../processing.h"
#include "../in.h"

void sort(double **data, int n){
    double *temp = NULL;

    for (int i = 0; i < n - 1; i++)
        for (int j = 0; j < n - i - 1; j++)
            if (data[j][0] - data[j + 1][0] > 0){
                temp = data[j];
                data[j] = data[j + 1];
                data[j + 1] = temp;
            }
}

void find_necessary_interval(struct data_t data, int *high, int *low){
    if (data.val_arg <= data.table[*high][0])
        *low = *high + data.n;
    
    else if (data.val_arg >= data.table[*low][0])
        *high = *low - data.n;
    
    else if ((data.val_arg > data.table[*high][0]) && (data.val_arg < data.table[*low][0])){
        int i = 1;
        int flag = 1;

        while (data.val_arg - data.table[i][0] > EPS)
            i++;

        if (data.val_arg - data.table[i - 1][0] <= data.table[i][0] - data.val_arg){
            i--;
            flag = 0;
        }

        *high = i;
        *low = i;

        int count = data.n;

        while (count != 0){
            if (flag == 1){
                if (*high > 0)
                    (*high)--;
                else
                    (*low)++;

                flag = 0;
            }
            else{
                if (*low < data.count_str - 1)
                    (*low)++;
                else
                    (*high)--;

                flag = 1;
            }

            count--;
        }
    }
}

void copy_table_newton(struct data_t data, double **table, int low, int high){
    int l = 0;

    for (int i = high; i <= low; i++){
        table[l][0] = data.table[i][0];
        table[l][1] = data.table[i][1];

        l++;
    }
}

void copy_table_hermit(struct data_t data, double **table, int low, int high){
    int l = 0;

    for (int i = high; i < low; i++){
        table[l][0] = data.table[i][0];
        table[l][1] = data.table[i][1];
        table[l][2] = data.table[i][2];
        table[l + 1][0] = data.table[i][0];
        table[l + 1][1] = data.table[i][1];
        table[l + 1][2] = data.table[i][2];

        l += 2;
    }
}

void copy_table_reverse_intropolation(struct data_t data, double ** table, int low, int high){
    int l = 0;

    for (int i = high; i <= low; i++){
        table[l][0] = data.table[i][1];
        table[l][1] = data.table[i][0];

        l++;
    }
}


double polinom_newton(struct result_t result, int n, double val_arg){
    double tmp = 1;
    double res = result.table[0][1];

    for (int k = 0; k < n; k++){
        for (int i = 0; i < result.str - k - 1; i++)
            result.table[i][1] = (result.table[i][1] - result.table[i + 1][1]) / (result.table[i][0] - result.table[i + k + 1][0]);

        tmp = tmp * (val_arg - result.table[k][0]);
        res = res + (result.table[0][1] * tmp);
    }

    return res;
}

double polinom_hermit(struct result_t result, int n, double val_arg){
    double tmp = 1;
    double res = result.table[0][1];

    for (int k = 0; k < n; k++){
        for (int i = 0; i < result.str - k - 1; i++)
            if ((fabs(result.table[i][1] - result.table[i + 1][1]) < EPS) && (fabs(result.table[i][0] - result.table[i + k + 1][0]) < EPS))
                result.table[i][1] = result.table[i][2];
            else
                result.table[i][1] = (result.table[i][1] - result.table[i + 1][1]) / (result.table[i][0] - result.table[i + k + 1][0]);

        tmp = tmp * (val_arg - result.table[k][0]);
        res = res + (result.table[0][1] * tmp);
    }

    return res;
}

int polinom_newton_work(struct data_t data, int high, int low, double *res){
    int error = SUCCESS;

    find_necessary_interval(data, &high, &low);

    struct result_t result_newton = {NULL, 0, 0};
    result_newton.str = low - high + 1;
    result_newton.column = 3 - 1;
    result_newton.table = create_matrix(result_newton.str, result_newton.column);
    if (result_newton.table){
        copy_table_newton(data, result_newton.table, low, high);

        *res = polinom_newton(result_newton, data.n, data.val_arg);

        mat_free(result_newton.table, result_newton.str);
    }
    else{
        printf("\x1b[31m""%s""\x1b[0m", "\nMemory allocation!!!\n");
        error = MEMORY_ALLOCATION;
    }

    return error;
}

int polinom_hermit_work(struct data_t data, int high, int low, double *res){
    int error = SUCCESS;
    int tmp_n = data.n;
    data.n = data.n / 2 + 1;
    find_necessary_interval(data, &high, &low);

    struct result_t result_hermit = {NULL, 0, 0};
    result_hermit.str = data.n * 2;
    data.n = tmp_n;
    result_hermit.column = 3;
    result_hermit.table = create_matrix(result_hermit.str, result_hermit.column);
    if (result_hermit.table){
        copy_table_hermit(data, result_hermit.table, low, high);
        *res = polinom_hermit(result_hermit, data.n, data.val_arg);
        mat_free(result_hermit.table, result_hermit.str);
    }
    else{
        printf("\x1b[31m""%s""\x1b[0m", "\nMemory allocation!!!\n");
        error = MEMORY_ALLOCATION;
    }

    return error;
}

int reverse_intropolation_work(struct data_t data, int high, int low, double *res){
    int error = SUCCESS;
    double tmp_arg = data.val_arg;
    data.val_arg = 0.0;

    struct result_t tmp_table = {NULL, 0, 0};
    tmp_table.str = data.count_str;
    tmp_table.column = 3 - 1;
    tmp_table.table = create_matrix(tmp_table.str, tmp_table.column);
    if (tmp_table.table){
        copy_table_reverse_intropolation(data, tmp_table.table, low, high);
        struct data_t tmp_data = {tmp_table.table, data.count_str, data.n, data.val_arg};
        sort(tmp_data.table, tmp_data.count_str);
        find_necessary_interval(tmp_data, &high, &low);
        struct result_t result_reverse_intropolation = {NULL, 0, 0};
        result_reverse_intropolation.str = low - high + 1;
        result_reverse_intropolation.column = 3 - 1;
        result_reverse_intropolation.table = create_matrix(result_reverse_intropolation.str, result_reverse_intropolation.column);
        if (result_reverse_intropolation.table){
            copy_table_newton(tmp_data, result_reverse_intropolation.table, low, high);
            *res = polinom_newton(result_reverse_intropolation, data.n, data.val_arg);
            data.val_arg = tmp_arg;
            mat_free(result_reverse_intropolation.table, result_reverse_intropolation.str);
        }

        mat_free(tmp_table.table, tmp_table.str);
    }


    return error;
}

void test(struct data_t data, int high, int low){
    double tmp = data.val_arg;
    double res_1 = 0.0;
    double res_2 = 0.0;
    double res_3 = 0.0;

    printf("\n\nТаблица для сравнения результатов полиномов (Newton, Hermit):\n");
    printf("\t-----------------------------------\n");
    printf("\t| %1s | %3s   |  %6s  |  %6s  |\n", "i", "x", "Newton", "Hermit");
    printf("\t-----------------------------------\n");
    for (int i = 0; i < 5; i++){
        data.n = i;
        polinom_newton_work(data, high, low, &res_1);
        polinom_hermit_work(data, high, low, &res_2);
        printf("\t| %1d | %.3lf | %lf | %lf |\n", i, data.val_arg, res_1, res_2);
    }
    printf("\t-----------------------------------\n");

    printf("\n\nТаблица результатов обратной интерполяции:\n");
    printf("\t-----------------------------\n");
    printf("\t| %1s | %21s |\n", "n", "Reverse intropolation");
    printf("\t-----------------------------\n");
    for (int i = 0; i < 5; i++){
        data.n = i;
        data.val_arg = 0.0;
        reverse_intropolation_work(data, high, low, &res_3);
        printf("\t| %1d |      %10lf       |\n", i,res_3);
    }
    printf("\t-----------------------------\n");

    data.val_arg = tmp;
}
