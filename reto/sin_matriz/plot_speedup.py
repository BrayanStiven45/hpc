import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# -----------------------------------------------------------------------
# Helpers
# -----------------------------------------------------------------------

def read_csv(path):
    """Lee un CSV generado por el shell script.
    Devuelve (labels, times_matrix, iters_matrix) donde:
      labels       = lista de strings 'k/n'
      times_matrix = ndarray (runs x k)
    """
    df = pd.read_csv(path, index_col=0)
    labels = list(df.columns)
    return labels, df.values.astype(float)


def mean_per_k(matrix):
    return np.mean(matrix, axis=0)


def speedup(seq_mean, par_mean):
    return seq_mean / par_mean


def k_from_label(label):
    return int(label.split("/")[0])


def n_from_label(label):
    return int(label.split("/")[1])


def annotate_iters(ax, x_vals, y_vals, iters, color, offset=(0, 6)):
    for x, y, it in zip(x_vals, y_vals, iters):
        ax.annotate(
            f"{int(it):,}",
            xy=(x, y),
            xytext=(offset[0], offset[1]),
            textcoords="offset points",
            fontsize=7,
            color=color,
            ha="center",
        )


# -----------------------------------------------------------------------
# Rutas
# -----------------------------------------------------------------------

SEQ_TIME = "secuencial_time/times.csv"
SEQ_ITER = "secuencial_time/iterations.csv"

PROC_TIME = "process_time/times_p{p}.csv"
PROC_ITER = "process_time/iterations_p{p}.csv"

THR_TIME  = "threads_time/times_t{p}.csv"
THR_ITER  = "threads_time/iterations_t{p}.csv"

OPT_TIME  = "opt_time/times_{o}.csv"
OPT_ITER  = "opt_time/iterations_{o}.csv"

PROCS = [2, 4, 6, 8]
OPTS  = ["O1", "O2", "O3"]

OUTPUT_DIR = "plots"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# -----------------------------------------------------------------------
# Leer baseline secuencial
# -----------------------------------------------------------------------

labels_seq, times_seq = read_csv(SEQ_TIME)
_, iters_seq_mat      = read_csv(SEQ_ITER)

seq_mean  = mean_per_k(times_seq)
iters_seq = mean_per_k(iters_seq_mat)
k_vals    = [k_from_label(l) for l in labels_seq]
n_vals    = [n_from_label(l) for l in labels_seq]
x         = np.arange(len(k_vals))
x_labels  = [f"k={k}\nn={n:,}" for k, n in zip(k_vals, n_vals)]

COLORS = ["#378ADD", "#1D9E75", "#D85A30", "#7F77DD"]

# -----------------------------------------------------------------------
# Figura 1 — Speedup Procesos
# -----------------------------------------------------------------------

fig, ax = plt.subplots(figsize=(11, 6))
ax.axhline(1, color="gray", linewidth=0.8, linestyle="--", label="Baseline (seq)")

for idx, p in enumerate(PROCS):
    path_t = PROC_TIME.format(p=p)
    path_i = PROC_ITER.format(p=p)
    if not os.path.exists(path_t):
        print(f"  [skip] {path_t} no encontrado")
        continue

    _, times_p = read_csv(path_t)
    _, iters_p = read_csv(path_i)
    sp   = speedup(seq_mean, mean_per_k(times_p))
    iters_mean = mean_per_k(iters_p)
    color = COLORS[idx]

    ax.plot(x, sp, marker="o", color=color, linewidth=1.8,
            markersize=6, label=f"{p} procesos")
    annotate_iters(ax, x, sp, iters_mean, color, offset=(0, 7))

ax.set_xticks(x)
ax.set_xticklabels(x_labels, fontsize=8)
ax.set_ylabel("Speedup  (T_seq / T_par)")
ax.set_xlabel("Tamaño del problema")
ax.set_title("Speedup — Procesos (memoria compartida + semaforos)")
ax.legend(fontsize=9)
ax.yaxis.set_minor_locator(ticker.AutoMinorLocator())
ax.grid(axis="y", linewidth=0.4, alpha=0.6)
ax.grid(axis="y", which="minor", linewidth=0.2, alpha=0.4)
plt.tight_layout()
out = os.path.join(OUTPUT_DIR, "speedup_procesos.png")
plt.savefig(out, dpi=150)
plt.close()
print(f"Guardado: {out}")

# -----------------------------------------------------------------------
# Figura 2 — Speedup Hilos
# -----------------------------------------------------------------------

fig, ax = plt.subplots(figsize=(11, 6))
ax.axhline(1, color="gray", linewidth=0.8, linestyle="--", label="Baseline (seq)")

for idx, p in enumerate(PROCS):
    path_t = THR_TIME.format(p=p)
    path_i = THR_ITER.format(p=p)
    if not os.path.exists(path_t):
        print(f"  [skip] {path_t} no encontrado")
        continue

    _, times_t = read_csv(path_t)
    _, iters_t = read_csv(path_i)
    sp         = speedup(seq_mean, mean_per_k(times_t))
    iters_mean = mean_per_k(iters_t)
    color      = COLORS[idx]

    ax.plot(x, sp, marker="s", color=color, linewidth=1.8,
            markersize=6, label=f"{p} hilos")
    annotate_iters(ax, x, sp, iters_mean, color, offset=(0, 7))

ax.set_xticks(x)
ax.set_xticklabels(x_labels, fontsize=8)
ax.set_ylabel("Speedup  (T_seq / T_par)")
ax.set_xlabel("Tamaño del problema")
ax.set_title("Speedup — Hilos (pthreads + barriers)")
ax.legend(fontsize=9)
ax.yaxis.set_minor_locator(ticker.AutoMinorLocator())
ax.grid(axis="y", linewidth=0.4, alpha=0.6)
ax.grid(axis="y", which="minor", linewidth=0.2, alpha=0.4)
plt.tight_layout()
out = os.path.join(OUTPUT_DIR, "speedup_hilos.png")
plt.savefig(out, dpi=150)
plt.close()
print(f"Guardado: {out}")

# -----------------------------------------------------------------------
# Figura 3 — Speedup Optimizacion de compilador
# -----------------------------------------------------------------------

OPT_COLORS  = ["#1D9E75", "#D85A30", "#7F77DD"]
OPT_MARKERS = ["^", "D", "P"]

fig, ax = plt.subplots(figsize=(11, 6))
ax.axhline(1, color="gray", linewidth=0.8, linestyle="--", label="Sin optimizacion (-O0)")

for idx, opt in enumerate(OPTS):
    path_t = OPT_TIME.format(o=opt)
    path_i = OPT_ITER.format(o=opt)
    if not os.path.exists(path_t):
        print(f"  [skip] {path_t} no encontrado")
        continue

    _, times_o = read_csv(path_t)
    _, iters_o = read_csv(path_i)
    sp         = speedup(seq_mean, mean_per_k(times_o))
    iters_mean = mean_per_k(iters_o)
    color      = OPT_COLORS[idx]

    ax.plot(x, sp, marker=OPT_MARKERS[idx], color=color, linewidth=1.8,
            markersize=7, label=f"-{opt}")
    annotate_iters(ax, x, sp, iters_mean, color, offset=(0, 7))

ax.set_xticks(x)
ax.set_xticklabels(x_labels, fontsize=8)
ax.set_ylabel("Speedup  (T_O0 / T_Ox)")
ax.set_xlabel("Tamaño del problema")
ax.set_title("Speedup — Optimizacion de compilador (gcc -O1 / -O2 / -O3)")
ax.legend(fontsize=9)
ax.yaxis.set_minor_locator(ticker.AutoMinorLocator())
ax.grid(axis="y", linewidth=0.4, alpha=0.6)
ax.grid(axis="y", which="minor", linewidth=0.2, alpha=0.4)
plt.tight_layout()
out = os.path.join(OUTPUT_DIR, "speedup_compilador.png")
plt.savefig(out, dpi=150)
plt.close()
print(f"Guardado: {out}")

print("\nListo. Graficas en la carpeta 'plots/'")
