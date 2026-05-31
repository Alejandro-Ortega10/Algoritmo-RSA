"""
╔══════════════════════════════════════════════════════════════╗
║   RSA CON EXPONENCIACIÓN POR CUADRADOS SUCESIVOS — O(log n) ║
║   Taller Final · Análisis y Diseño de Algoritmos            ║
║   UNIVALLE BUGA · 2026                                      ║
╚══════════════════════════════════════════════════════════════╝

Este script resuelve el mismo problema que rsa_ingenuo.py
pero con un número de pasos drásticamente menor.

Use los mismos valores de entrada en ambos scripts para
comparar directamente el número de pasos y el tiempo.
"""

import time


# ══════════════════════════════════════════════════════════════
#  CONTADOR GLOBAL DE PASOS
#  Se reinicia antes de cada operación para medirla por separado
# ══════════════════════════════════════════════════════════════

contador_pasos = 0


# ══════════════════════════════════════════════════════════════
#  BLOQUE 1 — FUNCIONES MATEMÁTICAS BASE
#  (idénticas al script ingenuo — la diferencia está solo
#   en la función de exponenciación del Bloque 2)
# ══════════════════════════════════════════════════════════════

def es_primo(numero):
    """
    Determina si un número entero positivo es primo.
    Método: división de prueba hasta la raíz cuadrada del número.
    Un número es primo si no tiene divisores distintos de 1 y él mismo.
    """
    if numero < 2:
        return False
    if numero == 2:
        return True
    if numero % 2 == 0:
        return False
    divisor = 3
    while divisor * divisor <= numero:
        if numero % divisor == 0:
            return False
        divisor += 2
    return True


def maximo_comun_divisor(a, b):
    """
    Calcula el Máximo Común Divisor (MCD) de dos enteros.
    Usa el algoritmo de Euclides: reemplaza (a, b) por (b, a mod b)
    hasta que b sea cero. El MCD es el último valor de a.

    Ejemplo: mcd(48, 18)
      48 mod 18 = 12  →  mcd(18, 12)
      18 mod 12 =  6  →  mcd(12, 6)
      12 mod  6 =  0  →  resultado: 6
    """
    while b != 0:
        a, b = b, a % b
    return a


def inverso_modular(e, phi):
    """
    Calcula el inverso modular de e en Z_phi mediante el
    algoritmo de Euclides extendido.

    Encuentra d tal que: (e × d) mod phi = 1
    Esto equivale a deshacer la multiplicación por e dentro del
    sistema modular, lo cual es imposible con división ordinaria.

    Se usa para obtener la clave privada d a partir de la pública e.
    """
    phi_original = phi
    coef_anterior, coef_actual = 1, 0

    if phi == 1:
        return 0

    while e > 1:
        cociente        = e // phi
        phi, e          = e % phi, phi
        coef_anterior, coef_actual = (
            coef_actual,
            coef_anterior - cociente * coef_actual
        )

    if coef_anterior < 0:
        coef_anterior += phi_original

    return coef_anterior


# ══════════════════════════════════════════════════════════════
#  BLOQUE 2 — EXPONENCIACIÓN POR CUADRADOS SUCESIVOS  O(log n)
#  *** ESTA ES LA ÚNICA FUNCIÓN QUE CAMBIA RESPECTO AL INGENUO ***
# ══════════════════════════════════════════════════════════════

def potencia_rapida(base, exponente, modulo):
    """
    Calcula   base ^ exponente  mod  modulo
    mediante el método de cuadrados sucesivos.

    Idea central: en lugar de multiplicar 'base' una vez por vuelta,
    se DOBLA la potencia acumulada en cada paso inspeccionando
    los dígitos binarios del exponente de derecha a izquierda.

    En cada vuelta del ciclo ocurren dos cosas:
      1. Se CUADRA la base actual            (siempre, 1 paso)
      2. Se multiplica por el resultado      (solo si el bit actual es 1)

    Complejidad: O(log n) — la cantidad de vueltas del ciclo
    es igual a la cantidad de dígitos binarios del exponente,
    que crece de forma logarítmica.

    Comparación con el método directo para exponente = 65.537:
      Directo : 65.537 pasos
      Rápido  : ~34 pasos  (≈ 2 × 17 dígitos binarios de 65.537)
    """
    global contador_pasos
    resultado = 1
    base      = base % modulo

    while exponente > 0:

        if exponente % 2 == 1:
            # El bit menos significativo del exponente es 1:
            # acumular la base actual en el resultado
            resultado       = (resultado * base) % modulo
            contador_pasos += 1       # multiplicación por resultado

        exponente //= 2               # desplazar un bit a la derecha
        base             = (base * base) % modulo
        contador_pasos  += 1          # cuadrado de la base (siempre ocurre)

    return resultado


# ══════════════════════════════════════════════════════════════
#  BLOQUE 3 — GENERACIÓN DE CLAVES RSA
# ══════════════════════════════════════════════════════════════

def generar_claves(p, q):
    """
    Genera el par de claves RSA a partir de dos números primos p y q.

    Proceso:
      1. n   = p × q          → módulo público (aparece en ambas claves)
      2. phi = (p-1) × (q-1) → función de Euler: cuenta los enteros
                                menores que n coprimos con n
      3. e   = exponente público, debe ser coprimo con phi
      4. d   = inverso modular de e en Z_phi → clave privada

    Retorna:
      clave_publica  = (e, n)
      clave_privada  = (d, n)
    """
    if not es_primo(p) or not es_primo(q):
        raise ValueError(
            f"Error: p={p} y q={q} deben ser ambos números primos."
        )
    if p == q:
        raise ValueError("Error: p y q deben ser primos distintos.")

    n   = p * q
    phi = (p - 1) * (q - 1)

    # El exponente público estándar es 65537 (= 2^16 + 1, primo)
    e = 65537
    if maximo_comun_divisor(e, phi) != 1:
        e = 3
        while maximo_comun_divisor(e, phi) != 1:
            e += 2

    d = inverso_modular(e, phi)

    return (e, n), (d, n)


# ══════════════════════════════════════════════════════════════
#  BLOQUE 4 — CONVERSIÓN TEXTO ↔ NÚMEROS
# ══════════════════════════════════════════════════════════════

def texto_a_numeros(texto):
    """
    Convierte cada carácter del texto a su valor numérico Unicode.
    La letra 'A' vale 65, 'a' vale 97, '0' vale 48, etc.
    RSA opera sobre números, no sobre letras, por eso se necesita
    esta conversión antes de cifrar.
    """
    return [ord(caracter) for caracter in texto]


def numeros_a_texto(lista_numeros):
    """
    Convierte una lista de valores numéricos de vuelta a texto.
    Es la operación inversa de texto_a_numeros.
    """
    return "".join(chr(numero) for numero in lista_numeros)


# ══════════════════════════════════════════════════════════════
#  BLOQUE 5 — CIFRADO Y DESCIFRADO
# ══════════════════════════════════════════════════════════════

def cifrar_valor(valor, e, n):
    """
    Cifra un único valor numérico usando la clave pública (e, n).
    Aplica la fórmula:  c = valor ^ e  mod  n
    """
    return potencia_rapida(valor, e, n)


def descifrar_valor(valor_cifrado, d, n):
    """
    Descifra un único valor numérico usando la clave privada (d, n).
    Aplica la fórmula:  m = valor_cifrado ^ d  mod  n
    """
    return potencia_rapida(valor_cifrado, d, n)


def cifrar_mensaje(mensaje, clave_publica):
    """
    Cifra un mensaje de texto completo carácter a carácter.
    Retorna una lista de enteros: cada uno es el cifrado de un carácter.
    """
    e, n     = clave_publica
    valores  = texto_a_numeros(mensaje)
    cifrados = [cifrar_valor(v, e, n) for v in valores]
    return cifrados


def descifrar_mensaje(lista_cifrada, clave_privada):
    """
    Descifra una lista de enteros cifrados y reconstruye el texto original.
    """
    d, n        = clave_privada
    descifrados = [descifrar_valor(v, d, n) for v in lista_cifrada]
    return numeros_a_texto(descifrados)


# ══════════════════════════════════════════════════════════════
#  PROGRAMA PRINCIPAL
# ══════════════════════════════════════════════════════════════

if __name__ == "__main__":

    # ── Parámetros RSA ─────────────────────────────────────────
    # Mismos primos que rsa_ingenuo.py para comparar en igualdad
    # de condiciones.
    P = 1009
    Q = 1013

    separador = "=" * 62

    print(separador)
    print("  RSA · EXPONENCIACIÓN POR CUADRADOS SUCESIVOS — O(log n)")
    print(separador)

    # Generación de claves
    clave_publica, clave_privada = generar_claves(P, Q)
    e, n = clave_publica
    d, _ = clave_privada

    import math
    pasos_estimados_e = 2 * math.floor(math.log2(e)) + 2
    pasos_estimados_d = 2 * math.floor(math.log2(d)) + 2

    print(f"\n  Primos utilizados : p = {P},  q = {Q}")
    print(f"  Módulo público    : n = p × q = {n:,}")
    print(f"  Clave pública     : e = {e:,}")
    print(f"  Clave privada     : d = {d:,}")
    print(f"\n  Pasos por carácter al cifrar    (≈ 2·log₂ e): ~{pasos_estimados_e}")
    print(f"  Pasos por carácter al descifrar (≈ 2·log₂ d): ~{pasos_estimados_d}")

    # Entrada del usuario
    print()
    contrasena = input("  Ingrese la contraseña a cifrar: ").strip()
    if not contrasena:
        contrasena = "Hola123"
        print(f"  (usando valor por defecto: '{contrasena}')")

    longitud = len(contrasena)
    print(f"\n  Longitud del mensaje: {longitud} carácter(es)")
    print(f"  Pasos totales estimados al cifrar   : ~{pasos_estimados_e * longitud}")
    print(f"  Pasos totales estimados al descifrar: ~{pasos_estimados_d * longitud}")

    # ── CIFRADO ────────────────────────────────────────────────
    print(f"\n{separador}")
    print("  CIFRADO")
    print(separador)

    contador_pasos = 0
    marca_inicio   = time.perf_counter()
    mensaje_cifrado = cifrar_mensaje(contrasena, clave_publica)
    marca_fin      = time.perf_counter()

    tiempo_cifrado = marca_fin - marca_inicio
    pasos_cifrado  = contador_pasos

    print(f"  Texto original  : {contrasena}")
    print(f"  Texto cifrado   : {mensaje_cifrado}")
    print(f"  Pasos realizados: {pasos_cifrado:,}")
    print(f"  Tiempo          : {tiempo_cifrado:.6f} segundos")

    # ── DESCIFRADO ─────────────────────────────────────────────
    print(f"\n{separador}")
    print("  DESCIFRADO")
    print(separador)

    contador_pasos = 0
    marca_inicio   = time.perf_counter()
    mensaje_recuperado = descifrar_mensaje(mensaje_cifrado, clave_privada)
    marca_fin      = time.perf_counter()

    tiempo_descifrado = marca_fin - marca_inicio
    pasos_descifrado  = contador_pasos

    print(f"  Texto recuperado : {mensaje_recuperado}")
    print(f"  Pasos realizados : {pasos_descifrado:,}")
    print(f"  Tiempo           : {tiempo_descifrado:.6f} segundos")

    # ── RESUMEN FINAL ──────────────────────────────────────────
    verificacion = (mensaje_recuperado == contrasena)

    print(f"\n{separador}")
    print("  RESUMEN")
    print(separador)
    print(f"  Verificación          : {'✓ Correcto' if verificacion else '✗ Error'}")
    print(f"  Pasos totales         : {pasos_cifrado + pasos_descifrado:,}")
    print(f"  Tiempo total          : {tiempo_cifrado + tiempo_descifrado:.6f} segundos")
    print(f"  Pasos por carácter    : {(pasos_cifrado + pasos_descifrado) // longitud:,}")
    print(f"\n  Compare estos resultados con rsa_ingenuo.py")
    print(separador)
