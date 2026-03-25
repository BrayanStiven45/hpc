import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# -----------------------------------------------------------------------
# Helpers
# -----------------------------------------------------------------------

def read_csv(path):
    df = pd.read_csv(path, index_col=0)
    labels = list(df.columns)
    return labels, df.values.astype(float)

def avg_time(path, n_runs):
    """Promedia los primeros n_runs filas del CSV de tiempos."""
    labels, matrix = read_csv(path)
    return labels, np.mean(matrix[:n_runs], axis=0)


def speedup(seq_mean, par_mean):
    return seq_mean / par_mean

def k_from_label(l): return int(l.split("/")[0])
def n_from_label(l): return int(l.split("/")[1])

def save_fig(fig, name):
    os.makedirs("plots", exist_ok=True)
    path = os.path.join("plots", name)
    fig.savefig(path, dpi=150)
    plt.close(fig)
    print(f"Guardado: {path}")

# -----------------------------------------------------------------------
# Baseline secuencial — 10 corridas
# -----------------------------------------------------------------------

labels_seq, seq_mean = avg_time("secuencial_time/times.csv", 10)
_, iters_mat         = read_csv("secuencial_time/iterations.csv")
iters_per_k          = np.mean(iters_mat[:10], axis=0)

k_vals   = [k_from_label(l) for l in labels_seq]
n_vals   = [n_from_label(l) for l in labels_seq]
x        = np.arange(len(k_vals))
x_labels = [f"k={k} / n={n:,}\n{int(round(it)):,} iters"
            for k, n, it in zip(k_vals, n_vals, iters_per_k)]

COLORS  = ["#378ADD", "#1D9E75", "#D85A30", "#7F77DD"]
PROCS   = [2, 4, 8]

# -----------------------------------------------------------------------
# Figura 1 — Speedup Procesos (5 corridas)
# -----------------------------------------------------------------------

fig, ax = plt.subplots(figsize=(11, 6))
ax.axhline(1, color="gray", linewidth=0.8, linestyle="--", label="Baseline (secuencial)")

for idx, p in enumerate(PROCS):
    path_t = f"process_time/times_p{p}.csv"
    path_i = f"process_time/iterations_p{p}.csv"
    if not os.path.exists(path_t):
        print(f"  [skip] {path_t} no encontrado")
        continue

    _, par_mean = avg_time(path_t, 5)
    sp          = speedup(seq_mean, par_mean)
    color       = COLORS[idx]

    ax.plot(x, sp, marker="o", color=color, linewidth=1.8, markersize=6, label=f"{p} procesos")

ax.set_xticks(x)
ax.set_xticklabels(x_labels, fontsize=8)
ax.set_ylabel("Speedup  (T_seq / T_par)")
ax.set_xlabel("Tamaño del problema")
ax.set_title("Speedup — Procesos")
ax.legend(fontsize=9)
ax.yaxis.set_minor_locator(ticker.AutoMinorLocator())
ax.grid(axis="y", linewidth=0.4, alpha=0.6)
ax.grid(axis="y", which="minor", linewidth=0.2, alpha=0.4)
plt.tight_layout()
save_fig(fig, "speedup_procesos.png")

# -----------------------------------------------------------------------
# Figura 2 — Speedup Hilos (5 corridas)
# -----------------------------------------------------------------------

fig, ax = plt.subplots(figsize=(11, 6))
ax.axhline(1, color="gray", linewidth=0.8, linestyle="--", label="Baseline (secuencial)")

for idx, p in enumerate(PROCS):
    path_t = f"threads_time/times_t{p}.csv"
    path_i = f"threads_time/iterations_t{p}.csv"
    if not os.path.exists(path_t):
        print(f"  [skip] {path_t} no encontrado")
        continue

    _, par_mean = avg_time(path_t, 5)
    sp          = speedup(seq_mean, par_mean)
    color       = COLORS[idx]

    ax.plot(x, sp, marker="s", color=color, linewidth=1.8, markersize=6, label=f"{p} hilos")

ax.set_xticks(x)
ax.set_xticklabels(x_labels, fontsize=8)
ax.set_ylabel("Speedup  (T_seq / T_par)")
ax.set_xlabel("Tamaño del problema")
ax.set_title("Speedup — Hilos")
ax.legend(fontsize=9)
ax.yaxis.set_minor_locator(ticker.AutoMinorLocator())
ax.grid(axis="y", linewidth=0.4, alpha=0.6)
ax.grid(axis="y", which="minor", linewidth=0.2, alpha=0.4)
plt.tight_layout()
save_fig(fig, "speedup_hilos.png")

# -----------------------------------------------------------------------
# Figura 3 — Speedup Optimizacion de compilador (10 corridas)
# -----------------------------------------------------------------------

fig, ax = plt.subplots(figsize=(11, 6))
ax.axhline(1, color="gray", linewidth=0.8, linestyle="--", label="Baseline (sin optimizacion)")

path_t = "secuencial_ofast_time/times.csv"
path_i = "secuencial_ofast_time/iterations.csv"

if os.path.exists(path_t):
    _, ofast_mean  = avg_time(path_t, 10)
    sp             = speedup(seq_mean, ofast_mean)

    ax.plot(x, sp, marker="^", color="#D85A30", linewidth=1.8, markersize=7, label="-Ofast")
else:
    print("  [skip] secuencial_ofast_time/times.csv no encontrado")

ax.set_xticks(x)
ax.set_xticklabels(x_labels, fontsize=8)
ax.set_ylabel("Speedup  (T_sin_opt / T_Ofast)")
ax.set_xlabel("Tamaño del problema")
ax.set_title("Speedup — Optimizacion de compilador (-Ofast)")
ax.legend(fontsize=9)
ax.yaxis.set_minor_locator(ticker.AutoMinorLocator())
ax.grid(axis="y", linewidth=0.4, alpha=0.6)
ax.grid(axis="y", which="minor", linewidth=0.2, alpha=0.4)
plt.tight_layout()
save_fig(fig, "speedup_compilador.png")

print("\nListo. Graficas en plots/")
