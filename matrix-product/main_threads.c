#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <pthread.h>

typedef struct {
    int **A;
    int **B;
    long int **C;
    int size;
    int start_row;
    int end_row;
} ThreadData;

int* random_vector(int size) {
    int* vector = malloc(size * sizeof(int));
    for (int i = 0; i < size; i++)
        vector[i] = rand();
    return vector;
}

int** random_matrix(int size) {
    int** matrix = malloc(size * sizeof(int*));
    for (int i = 0; i < size; i++)
        matrix[i] = random_vector(size);
    return matrix;
}

void* compute_rows(void* arg) {
    ThreadData* data = (ThreadData*)arg;

    for (int row = data->start_row; row < data->end_row; row++) {
        for (int col = 0; col < data->size; col++) {
            long int sum = 0;
            for (int k = 0; k < data->size; k++) {
                sum += data->A[row][k] * data->B[k][col];
            }
            data->C[row][col] = sum;
        }
    }

    pthread_exit(NULL);
}

long int** matrix_product_n_threads(int** A, int** B, int size, int num_threads) {
    pthread_t* threads = malloc(num_threads * sizeof(pthread_t));
    ThreadData* data = malloc(num_threads * sizeof(ThreadData));

    long int** C = malloc(size * sizeof(long int*));
    for (int i = 0; i < size; i++)
        C[i] = malloc(size * sizeof(long int));

    int rows_per_thread = size / num_threads;

    for (int i = 0; i < num_threads; i++) {
        int start = i * rows_per_thread;
        int end = (i == num_threads - 1) ? size : start + rows_per_thread;

        data[i] = (ThreadData){A, B, C, size, start, end};

        pthread_create(&threads[i], NULL, compute_rows, &data[i]);
    }

    for (int i = 0; i < num_threads; i++)
        pthread_join(threads[i], NULL);

    free(threads);
    free(data);

    return C;
}

void free_matrix(int** matrix, int size) {
    for (int i = 0; i < size; i++)
        free(matrix[i]);
    free(matrix);
}

void free_long_matrix(long int** matrix, int size) {
    for (int i = 0; i < size; i++)
        free(matrix[i]);
    free(matrix);
}

int main(int argc, char* argv[]) {
    if (argc != 3) {
        printf("Usage: %s [matrix_size] [num_threads]\n", argv[0]);
        return 1;
    }

    srand(time(NULL));

    int size = atoi(argv[1]);
    int num_threads = atoi(argv[2]);

    int** matrix_a = random_matrix(size);
    int** matrix_b = random_matrix(size);

    struct timespec start, end;
    clock_gettime(CLOCK_MONOTONIC, &start);

    long int** result = matrix_product_n_threads(matrix_a, matrix_b, size, num_threads);

    clock_gettime(CLOCK_MONOTONIC, &end);

    double time_taken =
        (end.tv_sec - start.tv_sec) +
        (end.tv_nsec - start.tv_nsec) / 1e9;

    printf("%f\n", time_taken);

    free_matrix(matrix_a, size);
    free_matrix(matrix_b, size);
    free_long_matrix(result, size);

    return 0;
}