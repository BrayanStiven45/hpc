#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int* random_vector (int size) {
  int* vector = malloc(size * sizeof(int));
  
  for (int i = 0; i < size; i++) {
    vector[i] = rand() % 10;
  }

  return vector;
}

int** random_matrix (int size) {
  int** matrix = malloc(size * sizeof(int*));
  
  for (int i = 0; i < size; i++) {
    matrix[i] = random_vector(size);
  }

  return matrix;
}

void initialize_vector(int* vector, int size) {
  for (int i = 0; i < size; i++) {
    vector[i] = 0;
  }
}

int** matrix_product (int** matrix_a, int** matrix_b, int size) {
  int** resulting_matrix = malloc(size * sizeof(int*));
  int a;
  int b;

  int* temp_vector;

  for (int a_row = 0; a_row < size; a_row++) {
    temp_vector = malloc(size * sizeof(int));
    initialize_vector(temp_vector, size);

    for (int b_col = 0; b_col < size; b_col++) {
      for (int counter = 0; counter < size; counter++) {
        a = matrix_a[a_row][counter];
        b = matrix_b[counter][b_col];
        temp_vector[b_col] += a * b;
      }
    }

    resulting_matrix[a_row] = temp_vector;
  }

  return resulting_matrix;
}

void free_matrix(int** matrix, int size) {
  for (int i = 0; i < size; i++) {
    free(matrix[i]);
  }
  free(matrix);
}

void print_matrix(int** matrix, int size) {
  printf("[");
  for (int i = 0; i < size; i++) {
    printf("[");
    for (int j = 0; j < size; j++) {
      if (j < size - 1) {
        printf("%d,", matrix[i][j]);
      } else {
        printf("%d", matrix[i][j]);
      }
    }
    if (i < size - 1) {
      printf("],");
    } else {
      printf("]");
    }
  }
  printf("]\n");
}

void print_product(int** matrix_a, int** matrix_b, int** resulting_matrix, int size) {
  printf("Matrix A:\n");
  print_matrix(matrix_a, size);

  printf("\nMatrix B:\n");
  print_matrix(matrix_b, size);

  printf("\nResulting matrix:\n");
  print_matrix(resulting_matrix, size);
}

int main(int argc, char* argv[]) {
  if (argc != 2) {
    printf("Usage: %s [matrix_size]\n", argv[0]);
    return 1;
  }

  srand(time(NULL)); // Initialize seed using current time in seconds

  int size = atoi(argv[1]);
  int** matrix_a = random_matrix(size);
  int** matrix_b = random_matrix(size);
  
  struct timespec start, end;
  // Here it starts taking wall-clock time
  clock_gettime(CLOCK_MONOTONIC, &start);

  int** resulting_matrix = matrix_product(matrix_a, matrix_b, size);

  clock_gettime(CLOCK_MONOTONIC, &end);
  // It ends taking wall-clock time

  double time_taken =
    (end.tv_sec - start.tv_sec) +
    (end.tv_nsec - start.tv_nsec) / 1e9;

  print_product(matrix_a, matrix_b, resulting_matrix, size);
  // printf("%f", time_taken);

  free_matrix(matrix_a, size);
  free_matrix(matrix_b, size);

  return 0;
}
