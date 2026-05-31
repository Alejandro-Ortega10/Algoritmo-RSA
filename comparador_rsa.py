"""
╔══════════════════════════════════════════════════════════════╗
║   COMPARADOR RSA — Ingenuo vs. Rápido                       ║
║   Taller Final · Análisis y Diseño de Algoritmos            ║
║   UNIVALLE BUGA · 2026                                      ║
╚══════════════════════════════════════════════════════════════╝

Solicita una palabra, la cifra y descifra con ambos métodos,
y muestra los resultados en gráficos comparativos.

Requiere: matplotlib   →   pip install matplotlib
Los archivos rsa_ingenuo.py y rsa_rapido.py deben estar
en el mismo directorio que este script.
"""

import sys
import os
import time
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.patches as mpatches
from matplotlib.ticker import ScalarFormatter

# ── Localizar los módulos hermanos ───────────────────────────────
directorio_actual = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, directorio_actual)

import rsa_ingenuo as ingenuo
import rsa_rapido  as rapido


# ══════════════════════════════════════════════════════════════
#  BLOQUE 1 — PALETA DE COLORES Y ESTILO
# ══════════════════════════════════════════════════════════════

COLOR_INGENUO  = "#D85A30"   # naranja-rojo  → método lento
COLOR_RAPIDO   = "#1D9E75"   # verde         → método rápido
COLOR_FONDO    = "#F8F8F8"
COLOR_TITULO   = "#1A1A2E"
COLOR_SUBTITULO= "#4A4A6A"

plt.rcParams.update({
    "font.family"      : "DejaVu Sans",
    "axes.spines.top"  : False,
    "axes.spines.right": False,
    "axes.facecolor"   : COLOR_FONDO,
    "figure.facecolor" : "white",
    "axes.titlesize"   : 11,
    "axes.titleweight" : "bold",
    "axes.titlecolor"  : COLOR_TITULO,
    "axes.labelsize"   : 9,
    "xtick.labelsize"  : 9,
    "ytick.labelsize"  : 8,
})


# ══════════════════════════════════════════════════════════════
#  BLOQUE 2 — EJECUCIÓN DE AMBOS MÉTODOS
# ══════════════════════════════════════════════════════════════

def ejecutar_metodo_ingenuo(palabra, clave_publica, clave_privada):
    """
    Cifra y descifra la palabra con el método ingenuo O(n).
    Retorna un diccionario con pasos y tiempos de cada etapa.
    """
    # ── cifrado ────────────────────────────────────────────────
    ingenuo.contador_pasos = 0
    marca_ini  = time.perf_counter()
    cifrado    = ingenuo.cifrar_mensaje(palabra, clave_publica)
    marca_fin  = time.perf_counter()
    pasos_cif  = ingenuo.contador_pasos
    tiempo_cif = marca_fin - marca_ini

    # ── descifrado ─────────────────────────────────────────────
    ingenuo.contador_pasos = 0
    marca_ini  = time.perf_counter()
    recuperado = ingenuo.descifrar_mensaje(cifrado, clave_privada)
    marca_fin  = time.perf_counter()
    pasos_des  = ingenuo.contador_pasos
    tiempo_des = marca_fin - marca_ini

    return {
        "cifrado"    : cifrado,
        "recuperado" : recuperado,
        "pasos_cif"  : pasos_cif,
        "pasos_des"  : pasos_des,
        "tiempo_cif" : tiempo_cif,
        "tiempo_des" : tiempo_des,
    }


def ejecutar_metodo_rapido(palabra, clave_publica, clave_privada):
    """
    Cifra y descifra la palabra con el método rápido O(log n).
    Retorna un diccionario con pasos y tiempos de cada etapa.
    """
    # ── cifrado ────────────────────────────────────────────────
    rapido.contador_pasos = 0
    marca_ini  = time.perf_counter()
    cifrado    = rapido.cifrar_mensaje(palabra, clave_publica)
    marca_fin  = time.perf_counter()
    pasos_cif  = rapido.contador_pasos
    tiempo_cif = marca_fin - marca_ini

    # ── descifrado ─────────────────────────────────────────────
    rapido.contador_pasos = 0
    marca_ini  = time.perf_counter()
    recuperado = rapido.descifrar_mensaje(cifrado, clave_privada)
    marca_fin  = time.perf_counter()
    pasos_des  = rapido.contador_pasos
    tiempo_des = marca_fin - marca_ini

    return {
        "cifrado"    : cifrado,
        "recuperado" : recuperado,
        "pasos_cif"  : pasos_cif,
        "pasos_des"  : pasos_des,
        "tiempo_cif" : tiempo_cif,
        "tiempo_des" : tiempo_des,
    }


def medir_escala(longitudes, clave_publica_i, clave_privada_i,
                              clave_publica_r, clave_privada_r):
    """
    Mide cuántos pasos usa cada método al cifrar palabras de
    distintas longitudes (rellena con 'a' para completar).
    Se usa para trazar la curva de escalado.
    """
    pasos_ingenuo, pasos_rapido = [], []

    for largo in longitudes:
        muestra = ("a" * largo)

        ingenuo.contador_pasos = 0
        ingenuo.cifrar_mensaje(muestra, clave_publica_i)
        pasos_ingenuo.append(ingenuo.contador_pasos)

        rapido.contador_pasos = 0
        rapido.cifrar_mensaje(muestra, clave_publica_r)
        pasos_rapido.append(rapido.contador_pasos)

    return pasos_ingenuo, pasos_rapido


# ══════════════════════════════════════════════════════════════
#  BLOQUE 3 — FUNCIONES DE GRAFICACIÓN
# ══════════════════════════════════════════════════════════════

def dibujar_barras_pasos(ax, pasos_ing, pasos_rap, titulo, unidad="pasos"):
    """Dibuja un par de barras comparando pasos de ambos métodos."""
    etiquetas = ["Ingenuo  O(n)", "Rápido  O(log n)"]
    valores   = [pasos_ing, pasos_rap]
    colores   = [COLOR_INGENUO, COLOR_RAPIDO]
    barras    = ax.bar(etiquetas, valores, color=colores,
                       width=0.45, zorder=3, edgecolor="white", linewidth=1.2)

    ax.set_title(titulo)
    ax.set_ylabel(f"Número de {unidad}")
    ax.set_yscale("log")
    ax.yaxis.set_major_formatter(ScalarFormatter())
    ax.yaxis.get_major_formatter().set_scientific(False)
    ax.grid(axis="y", linestyle="--", alpha=0.4, zorder=0)

    # Etiqueta encima de cada barra
    for barra, valor in zip(barras, valores):
        ax.text(
            barra.get_x() + barra.get_width() / 2,
            valor * 1.4,
            f"{valor:,}",
            ha="center", va="bottom",
            fontsize=8.5, fontweight="bold",
            color=barra.get_facecolor()
        )

    # Factor de reducción
    if pasos_rap > 0:
        factor = pasos_ing / pasos_rap
        ax.text(
            0.97, 0.96,
            f"×{factor:,.0f} menos pasos",
            transform=ax.transAxes,
            ha="right", va="top",
            fontsize=8, color=COLOR_RAPIDO,
            fontweight="bold",
            bbox=dict(boxstyle="round,pad=0.3",
                      facecolor="#E8F8F2", edgecolor=COLOR_RAPIDO,
                      alpha=0.85, linewidth=0.8)
        )


def dibujar_barras_tiempo(ax, tiempo_ing, tiempo_rap, titulo):
    """Dibuja un par de barras comparando tiempos de ambos métodos."""
    etiquetas = ["Ingenuo  O(n)", "Rápido  O(log n)"]
    valores   = [tiempo_ing * 1000, tiempo_rap * 1000]   # a milisegundos
    colores   = [COLOR_INGENUO, COLOR_RAPIDO]
    barras    = ax.bar(etiquetas, valores, color=colores,
                       width=0.45, zorder=3, edgecolor="white", linewidth=1.2)

    ax.set_title(titulo)
    ax.set_ylabel("Tiempo (milisegundos)")
    ax.set_yscale("log")
    ax.yaxis.set_major_formatter(ScalarFormatter())
    ax.yaxis.get_major_formatter().set_scientific(False)
    ax.grid(axis="y", linestyle="--", alpha=0.4, zorder=0)

    for barra, valor in zip(barras, valores):
        ax.text(
            barra.get_x() + barra.get_width() / 2,
            valor * 1.4,
            f"{valor:.4f} ms",
            ha="center", va="bottom",
            fontsize=8.5, fontweight="bold",
            color=barra.get_facecolor()
        )

    if valores[1] > 0:
        factor = valores[0] / valores[1]
        ax.text(
            0.97, 0.96,
            f"×{factor:,.0f} más rápido",
            transform=ax.transAxes,
            ha="right", va="top",
            fontsize=8, color=COLOR_RAPIDO,
            fontweight="bold",
            bbox=dict(boxstyle="round,pad=0.3",
                      facecolor="#E8F8F2", edgecolor=COLOR_RAPIDO,
                      alpha=0.85, linewidth=0.8)
        )


def dibujar_escala(ax, longitudes, pasos_ingenuo, pasos_rapido):
    """
    Traza cómo crecen los pasos de cada método según la longitud
    de la palabra. Muestra visualmente O(n) vs O(log n).
    """
    ax.plot(longitudes, pasos_ingenuo,
            "o-", color=COLOR_INGENUO, linewidth=2,
            markersize=5, label="Ingenuo  O(n)", zorder=3)
    ax.plot(longitudes, pasos_rapido,
            "s-", color=COLOR_RAPIDO, linewidth=2,
            markersize=5, label="Rápido  O(log n)", zorder=3)

    ax.set_title("Escalado de pasos según longitud de la palabra")
    ax.set_xlabel("Longitud de la palabra (caracteres)")
    ax.set_ylabel("Pasos totales de cifrado")
    ax.set_yscale("log")
    ax.yaxis.set_major_formatter(ScalarFormatter())
    ax.yaxis.get_major_formatter().set_scientific(False)
    ax.legend(fontsize=8.5, framealpha=0.7)
    ax.grid(linestyle="--", alpha=0.35, zorder=0)


def dibujar_panel_resumen(ax, palabra, res_ing, res_rap):
    """
    Panel de texto con la tabla resumen de todos los resultados.
    """
    ax.axis("off")

    longitud     = len(palabra)
    total_i_p    = res_ing["pasos_cif"]  + res_ing["pasos_des"]
    total_r_p    = res_rap["pasos_cif"]  + res_rap["pasos_des"]
    total_i_t    = res_ing["tiempo_cif"] + res_ing["tiempo_des"]
    total_r_t    = res_rap["tiempo_cif"] + res_rap["tiempo_des"]
    factor_pasos = total_i_p / total_r_p if total_r_p else 0
    factor_tiempo= total_i_t / total_r_t if total_r_t else 0
    ok_i         = "✓" if res_ing["recuperado"] == palabra else "✗"
    ok_r         = "✓" if res_rap["recuperado"] == palabra else "✗"

    lineas = [
        ("Palabra original",   palabra),
        ("Longitud",           f"{longitud} carácter(es)"),
        ("Texto cifrado",      str(res_ing["cifrado"])[:55] + ("…" if len(str(res_ing["cifrado"])) > 55 else "")),
        ("",                   ""),
        ("",                   "── PASOS ──────────────────────────────────"),
        ("Ingenuo · cifrado",  f"{res_ing['pasos_cif']:>15,}"),
        ("Ingenuo · descifrado",f"{res_ing['pasos_des']:>15,}"),
        ("Ingenuo · TOTAL",    f"{total_i_p:>15,}"),
        ("Rápido  · cifrado",  f"{res_rap['pasos_cif']:>15,}"),
        ("Rápido  · descifrado",f"{res_rap['pasos_des']:>15,}"),
        ("Rápido  · TOTAL",    f"{total_r_p:>15,}"),
        ("Factor de reducción",f"{factor_pasos:>14,.0f} ×"),
        ("",                   ""),
        ("",                   "── TIEMPOS ─────────────────────────────────"),
        ("Ingenuo · cifrado",  f"{res_ing['tiempo_cif']*1000:>13.4f} ms"),
        ("Ingenuo · descifrado",f"{res_ing['tiempo_des']*1000:>13.4f} ms"),
        ("Ingenuo · TOTAL",    f"{total_i_t*1000:>13.4f} ms"),
        ("Rápido  · cifrado",  f"{res_rap['tiempo_cif']*1000:>13.4f} ms"),
        ("Rápido  · descifrado",f"{res_rap['tiempo_des']*1000:>13.4f} ms"),
        ("Rápido  · TOTAL",    f"{total_r_t*1000:>13.4f} ms"),
        ("Factor de aceleración",f"{factor_tiempo:>13,.0f} ×"),
        ("",                   ""),
        ("Verificación ingenuo",f"{ok_i}  '{res_ing['recuperado']}'"),
        ("Verificación rápido", f"{ok_r}  '{res_rap['recuperado']}'"),
    ]

    y = 0.98
    espacio = 0.042
    for clave, valor in lineas:
        if clave == "":
            y -= espacio * 0.6
            if valor:
                ax.text(0.03, y, valor, transform=ax.transAxes,
                        fontsize=7.5, color="#888888",
                        fontfamily="monospace")
            y -= espacio * 0.5
            continue

        # clave en gris, valor en negro o coloreado
        color_val = COLOR_TITULO
        peso_val  = "normal"
        if "TOTAL" in clave:
            peso_val = "bold"
        if "Factor" in clave:
            color_val = COLOR_RAPIDO
            peso_val  = "bold"
        if "Verificación" in clave:
            color_val = COLOR_RAPIDO if "✓" in valor else COLOR_INGENUO

        ax.text(0.03, y, f"{clave}:", transform=ax.transAxes,
                fontsize=8, color=COLOR_SUBTITULO,
                fontfamily="monospace")
        ax.text(0.52, y, valor, transform=ax.transAxes,
                fontsize=8, color=color_val, fontweight=peso_val,
                fontfamily="monospace")
        y -= espacio


# ══════════════════════════════════════════════════════════════
#  BLOQUE 4 — CONSTRUCCIÓN DE LA FIGURA COMPLETA
# ══════════════════════════════════════════════════════════════

def construir_figura(palabra, res_ing, res_rap,
                     longitudes, pasos_esc_ing, pasos_esc_rap):
    """
    Arma la figura con 6 paneles en un diseño de cuadrícula:

      ┌──────────┬──────────┬──────────┬──────────┐
      │ Pasos    │ Pasos    │ Tiempo   │ Tiempo   │
      │ cifrado  │ descifr. │ cifrado  │ descifr. │
      ├──────────┴──────────┼──────────┴──────────┤
      │   Escalado pasos    │   Tabla resumen      │
      └─────────────────────┴─────────────────────┘
    """
    fig = plt.figure(figsize=(16, 9), facecolor="white")
    fig.suptitle(
        f"Comparación RSA — Exponenciación Ingenua O(n)  vs.  Rápida O(log n)"
        f"\nPalabra: \"{palabra}\"  ·  {len(palabra)} carácter(es)  ·  "
        f"p = 1009, q = 1013, e = 65.537",
        fontsize=13, fontweight="bold",
        color=COLOR_TITULO, y=0.98
    )

    gs = gridspec.GridSpec(
        2, 4,
        figure=fig,
        left=0.06, right=0.97,
        top=0.88,  bottom=0.08,
        hspace=0.50, wspace=0.45
    )

    # Fila superior: 4 barras
    ax_pc = fig.add_subplot(gs[0, 0])   # pasos cifrado
    ax_pd = fig.add_subplot(gs[0, 1])   # pasos descifrado
    ax_tc = fig.add_subplot(gs[0, 2])   # tiempo cifrado
    ax_td = fig.add_subplot(gs[0, 3])   # tiempo descifrado

    # Fila inferior: escalado (cols 0-1) + resumen (cols 2-3)
    ax_esc = fig.add_subplot(gs[1, 0:2])
    ax_res = fig.add_subplot(gs[1, 2:4])

    dibujar_barras_pasos(
        ax_pc,
        res_ing["pasos_cif"], res_rap["pasos_cif"],
        "Pasos · Cifrado"
    )
    dibujar_barras_pasos(
        ax_pd,
        res_ing["pasos_des"], res_rap["pasos_des"],
        "Pasos · Descifrado"
    )
    dibujar_barras_tiempo(
        ax_tc,
        res_ing["tiempo_cif"], res_rap["tiempo_cif"],
        "Tiempo · Cifrado"
    )
    dibujar_barras_tiempo(
        ax_td,
        res_ing["tiempo_des"], res_rap["tiempo_des"],
        "Tiempo · Descifrado"
    )
    dibujar_escala(ax_esc, longitudes, pasos_esc_ing, pasos_esc_rap)
    dibujar_panel_resumen(ax_res, palabra, res_ing, res_rap)

    # Leyenda global
    parche_ing = mpatches.Patch(color=COLOR_INGENUO, label="Ingenuo  O(n)")
    parche_rap = mpatches.Patch(color=COLOR_RAPIDO,  label="Rápido  O(log n)")
    fig.legend(
        handles=[parche_ing, parche_rap],
        loc="lower center", ncol=2,
        fontsize=9, framealpha=0.7,
        bbox_to_anchor=(0.5, 0.005)
    )

    return fig


# ══════════════════════════════════════════════════════════════
#  PROGRAMA PRINCIPAL
# ══════════════════════════════════════════════════════════════

if __name__ == "__main__":

    separador = "=" * 62
    P, Q      = 1009, 1013

    print(separador)
    print("  COMPARADOR RSA — Ingenuo O(n)  vs.  Rápido O(log n)")
    print(separador)

    # ── Entrada del usuario ────────────────────────────────────
    print()
    palabra = input("  Ingrese la palabra a cifrar: ").strip()
    if not palabra:
        palabra = "Universidad"
        print(f"  (usando valor por defecto: '{palabra}')")

    print(f"\n  Palabra  : '{palabra}'  ({len(palabra)} carácter(es))")
    print(f"  Primos   : p = {P},  q = {Q}")

    # ── Generación de claves ───────────────────────────────────
    cp_i, cv_i = ingenuo.generar_claves(P, Q)
    cp_r, cv_r = rapido.generar_claves(P, Q)
    e, n       = cp_i

    print(f"  Clave pública : e = {e:,},  n = {n:,}")

    # ── Ejecutar método ingenuo ────────────────────────────────
    print(f"\n  Ejecutando método ingenuo... ", end="", flush=True)
    res_ing = ejecutar_metodo_ingenuo(palabra, cp_i, cv_i)
    print(f"listo  ({(res_ing['tiempo_cif']+res_ing['tiempo_des'])*1000:.1f} ms)")

    # ── Ejecutar método rápido ─────────────────────────────────
    print(f"  Ejecutando método rápido...  ", end="", flush=True)
    res_rap = ejecutar_metodo_rapido(palabra, cp_r, cv_r)
    print(f"listo  ({(res_rap['tiempo_cif']+res_rap['tiempo_des'])*1000:.4f} ms)")

    # ── Medir escalado (longitudes 1..max(10, len(palabra))) ───
    largo_max  = max(10, len(palabra))
    longitudes = list(range(1, largo_max + 1))
    print(f"\n  Midiendo escalado (longitudes 1–{largo_max})... ", end="", flush=True)
    pasos_esc_ing, pasos_esc_rap = medir_escala(
        longitudes, cp_i, cv_i, cp_r, cv_r
    )
    print("listo")

    # ── Resultados en consola ──────────────────────────────────
    total_i_p = res_ing["pasos_cif"] + res_ing["pasos_des"]
    total_r_p = res_rap["pasos_cif"] + res_rap["pasos_des"]
    total_i_t = res_ing["tiempo_cif"] + res_ing["tiempo_des"]
    total_r_t = res_rap["tiempo_cif"] + res_rap["tiempo_des"]

    print(f"\n{separador}")
    print(f"  {'':30} {'INGENUO':>12}  {'RÁPIDO':>12}")
    print(f"  {'-'*56}")
    print(f"  {'Pasos  — cifrado':30} {res_ing['pasos_cif']:>12,}  {res_rap['pasos_cif']:>12,}")
    print(f"  {'Pasos  — descifrado':30} {res_ing['pasos_des']:>12,}  {res_rap['pasos_des']:>12,}")
    print(f"  {'Pasos  — TOTAL':30} {total_i_p:>12,}  {total_r_p:>12,}")
    print(f"  {'Tiempo — cifrado (ms)':30} {res_ing['tiempo_cif']*1000:>11.4f}   {res_rap['tiempo_cif']*1000:>11.4f}")
    print(f"  {'Tiempo — descifrado (ms)':30} {res_ing['tiempo_des']*1000:>11.4f}   {res_rap['tiempo_des']*1000:>11.4f}")
    print(f"  {'Tiempo — TOTAL (ms)':30} {total_i_t*1000:>11.4f}   {total_r_t*1000:>11.4f}")
    print(f"  {'-'*56}")
    print(f"  {'Factor de reducción (pasos)':30} {'×{:,.0f}'.format(total_i_p/total_r_p):>26}")
    print(f"  {'Factor de aceleración (tiempo)':30} {'×{:,.0f}'.format(total_i_t/total_r_t):>26}")
    print(f"  {'-'*56}")
    print(f"  Verificación ingenuo : {'✓ Correcto' if res_ing['recuperado']==palabra else '✗ Error'}")
    print(f"  Verificación rápido  : {'✓ Correcto' if res_rap['recuperado']==palabra else '✗ Error'}")
    print(separador)

    # ── Construir y mostrar la figura ──────────────────────────
    print("\n  Generando gráficos... ")
    fig = construir_figura(
        palabra, res_ing, res_rap,
        longitudes, pasos_esc_ing, pasos_esc_rap
    )

    # Eliminar caracteres no permitidos en nombres de archivo de Windows
    # ( \ / : * ? " < > | y espacio ) se reemplazan por guion bajo
    import re
    nombre_limpio  = re.sub(r'[\\/:*?"<>|\s]', '_', palabra[:12])
    nombre_archivo = f"comparacion_rsa_{nombre_limpio}.png"
    fig.savefig(nombre_archivo, dpi=150, bbox_inches="tight")
    print(f"  Figura guardada en: {nombre_archivo}")
    plt.show()

    print(f"\n  Fin del programa.")
    print(separador)