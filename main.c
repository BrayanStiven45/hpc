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

void initialize_vector(long int* vector, int size) {
  for (int i = 0; i < size; i++) {
    vector[i] = 0;
  }
}

long int** matrix_product (int** matrix_a, int** matrix_b, int size) {
  long int** resulting_matrix = malloc(size * sizeof(long int*));
  long int a;
  long int b;

  long int* temp_vector;

  for (int a_row = 0; a_row < size; a_row++) {
    temp_vector = malloc(size * sizeof(long int));
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

void print_matrix(int** matrix, int size) {
  for (int i = 0; i < size; i++) {
    for (int j = 0; j < size; j++) {
      printf("%d ", matrix[i][j]);
    }
    printf("\n");
  }
}

void print_long_matrix(long int** matrix, int size) {
  for (int i = 0; i < size; i++) {
    for (int j = 0; j < size; j++) {
      printf("%ld ", matrix[i][j]);
    }
    printf("\n");
  }
}

void free_matrix(int** matrix, int size) {
  for (int i = 0; i < size; i++) {
    free(matrix[i]);
  }
  free(matrix);
}

void free_long_matrix(long int** matrix, int size) {
  for (int i = 0; i < size; i++) {
    free(matrix[i]);
  }
  free(matrix);
}

int main(int argc, char* argv[]) {
  if (argc != 2) {
    printf("Usage: %s [matrix_size]\n", argv[0]);
    return 1;
  }

  srand(time(NULL));

  int size = atoi(argv[1]);
  int** matrix_a = random_matrix(size);
  int** matrix_b = random_matrix(size);
  long int** resulting_matrix = matrix_product(matrix_a, matrix_b, size);

  printf("Matrix A:\n");
  print_matrix(matrix_a, size);

  printf("\nMatrix B:\n");
  print_matrix(matrix_b, size);

  printf("\nResulting matrix:\n");
  print_long_matrix(resulting_matrix, size);

  free_matrix(matrix_a, size);
  free_matrix(matrix_b, size);
  free_long_matrix(resulting_matrix, size);

  return 0;
}
