#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>

#define EPSILON 1e-4
#define STABLE_STEPS 50

int* allocate_road(int n) {
    int *road = (int*)malloc(n * sizeof(int));
    if (!road) {
        printf("Memory allocation failed\n");
        exit(1);
    }
    return road;
}

void initialize_road(int *road, int n, double density) {
    for (int i = 0; i < n; i++) {
        double r = (double)rand() / RAND_MAX;
        road[i] = (r < density) ? 1 : 0;
    }
}

void update_road(int *old, int *new, int n) {
    for (int i = 0; i < n; i++) {
        int left  = (i - 1 + n) % n;
        int right = (i + 1) % n;

        if (old[left] == 1 && old[i] == 0)
            new[i] = 1;
        else if (old[i] == 1 && old[right] == 1)
            new[i] = 1;
        else
            new[i] = 0;
    }
}

int count_cars(int *road, int n) {
    int total = 0;
    for (int i = 0; i < n; i++)
        if (road[i] == 1) total++;
    return total;
}

int count_moved_cars(int *road, int n) {
    int moved = 0;
    for (int i = 0; i < n; i++) {
        int right = (i + 1) % n;
        if (road[i] == 1 && road[right] == 0)
            moved++;
    }
    return moved;
}

void copy_road(int *dest, int *src, int n) {
    for (int i = 0; i < n; i++)
        dest[i] = src[i];
}

double compute_velocity(int moved, int total) {
    if (total == 0) return 0.0;
    return (double)moved / total;
}

int main(int argc, char *argv[]) {

    if (argc < 2) {
        printf("Usage: %s <N>\n", argv[0]);
        return 1;
    }

    int N = atoi(argv[1]);
    if (N <= 0) {
        printf("N must be > 0\n");
        return 1;
    }

    double density = 0.5;
    srand(time(NULL));

    int *old = allocate_road(N);
    int *new = allocate_road(N);

    initialize_road(old, N, density);

    double prev_v = 0.0;
    int stable_count = 0;
    int t = 0;

    while (1) {

        int total = count_cars(old, N);
        int moved = count_moved_cars(old, N);

        double v = compute_velocity(moved, total);

        printf("Step %d: velocity = %f\n", t, v);

        // 🔹 Steady-state check
        if (fabs(v - prev_v) < EPSILON) {
            stable_count++;
        } else {
            stable_count = 0;
        }

        if (stable_count >= STABLE_STEPS) {
            printf("\nSteady state reached at step %d\n", t);
            printf("Final steady velocity ≈ %f\n", v);
            break;
        }

        prev_v = v;

        update_road(old, new, N);
        copy_road(old, new, N);

        t++;

        // Safety break (avoid infinite loop)
        if (t > 100000) {
            printf("\nMax steps reached without clear steady state\n");
            break;
        }
    }

    free(old);
    free(new);

    return 0;
}