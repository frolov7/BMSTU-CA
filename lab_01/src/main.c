#include "../struct.h"
#include "../in.h"
#include "../processing.h"

int main(void){
    setbuf(stdout, NULL);
    int error = SUCCESS;

    FILE *file = fopen(FILE_NAME, "r");
    if (file){
        struct data_t data = {NULL, 0, 0, 0.0};
        int first_line;
        data.count_str = count_strings_in_file(file, &first_line);

        rewind(file);
        fseek(file, first_line + 1, SEEK_SET);

        data.table = create_matrix(data.count_str, 3);
        if (data.table){
            error = in_data(file, &data);
            if (!error){

                int high = 0;
                int low = data.count_str - 1;
                int error_1 = SUCCESS;
                int error_2 = SUCCESS; 
                int error_3 = SUCCESS;

                double res_1 = 0.0;
                double res_2 = 0.0;
                double res_3 = 0.0;

                if (!(error_1 = polinom_newton_work(data, high, low, &res_1)) && !(error_2 = polinom_hermit_work(data, high, low, &res_2)) && !(error_3 = reverse_intropolation_work(data, high, low, &res_3))){
                    printf("\nPolinom newton y(%lf) = %lf\n""\x1b[0m", data.val_arg, res_1);
                    printf("\nPolinom hermit y(%lf) = %lf\n""\x1b[0m", data.val_arg, res_2);
                    printf("\nReverse intropolation y(%lf) = %lf\n""\x1b[0m", 0.0, res_3);

                    test(data, high, low);
                }
            }

            mat_free(data.table, data.count_str);
        }
        else{
            printf("\x1b[31m""%s""\x1b[0m", "\nMemory allocation!!!\n");
            error = MEMORY_ALLOCATION;
        }

        fclose(file);
    }
    else{
        printf("\x1b[31m""%s""\x1b[0m", "\nCan't open choosen file!!!\n");
        error = FILE_ERROR;
    }

    return error;
}
