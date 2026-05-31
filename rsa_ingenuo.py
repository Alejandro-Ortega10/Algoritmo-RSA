"""
╔══════════════════════════════════════════════════════════════╗
║   RSA CON EXPONENCIACIÓN DIRECTA — Método ingenuo  O(n)     ║
║   Taller Final · Análisis y Diseño de Algoritmos            ║
║   UNIVALLE BUGA · 2026                                      ║
╚══════════════════════════════════════════════════════════════╝

ADVERTENCIA: Este script es intencionalmente lento.
Su propósito es demostrar por qué el método directo
es inviable para exponentes grandes.

El descifrado puede tardar varios segundos: eso es
exactamente lo que se quiere mostrar.
"""

import time


# ══════════════════════════════════════════════════════════════
#  CONTADOR GLOBAL DE PASOS
#  Se reinicia antes de cada operación para medirla por separado
# ══════════════════════════════════════════════════════════════

contador_pasos = 0


# ══════════════════════════════════════════════════════════════
#  BLOQUE 1 — FUNCIONES MATEMÁTICAS BASE
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
#  BLOQUE 2 — EXPONENCIACIÓN DIRECTA  O(n)
# ══════════════════════════════════════════════════════════════

def potencia_directa(base, exponente, modulo):
    """
    Calcula   base ^ exponente  mod  modulo
    mediante multiplicación repetida: multiplica 'base' por sí
    misma exactamente 'exponente' veces, tomando el módulo en
    cada paso para evitar que los números crezcan demasiado.

    Complejidad: O(n) — el número de pasos crece de forma
    directamente proporcional al valor del exponente.

    Si el exponente es 65.537, este bucle da 65.537 vueltas.
    Si el exponente es 832.193, da 832.193 vueltas.
    """
    global contador_pasos
    resultado = 1
    base      = base % modulo

    for _ in range(exponente):
        resultado       = (resultado * base) % modulo
        contador_pasos += 1       # cada multiplicación cuenta como un paso

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
    # Se eligió históricamente por ser grande, primo, y tener
    # representación binaria con pocos unos (eficiente en hardware).
    e = 65537
    if maximo_comun_divisor(e, phi) != 1:
        # Si 65537 no es coprimo con phi, buscar el siguiente válido
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
    return potencia_directa(valor, e, n)


def descifrar_valor(valor_cifrado, d, n):
    """
    Descifra un único valor numérico usando la clave privada (d, n).
    Aplica la fórmula:  m = valor_cifrado ^ d  mod  n
    """
    return potencia_directa(valor_cifrado, d, n)


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
    d, n         = clave_privada
    descifrados  = [descifrar_valor(v, d, n) for v in lista_cifrada]
    return numeros_a_texto(descifrados)


# ══════════════════════════════════════════════════════════════
#  PROGRAMA PRINCIPAL
# ══════════════════════════════════════════════════════════════

if __name__ == "__main__":

    # ── Parámetros RSA ─────────────────────────────────────────
    # Primos de demostración. En RSA real se usan primos de ~1024 bits.
    # Con estos valores el módulo n = 1.022.117, suficiente para
    # cifrar cualquier carácter ASCII (valores 0–127).
    P = 1009
    Q = 1013

    separador = "=" * 62

    print(separador)
    print("  RSA · EXPONENCIACIÓN DIRECTA (Método ingenuo — O(n))")
    print(separador)

    # Generación de claves
    clave_publica, clave_privada = generar_claves(P, Q)
    e, n = clave_publica
    d, _ = clave_privada

    print(f"\n  Primos utilizados : p = {P},  q = {Q}")
    print(f"  Módulo público    : n = p × q = {n:,}")
    print(f"  Clave pública     : e = {e:,}")
    print(f"  Clave privada     : d = {d:,}")
    print(f"\n  Pasos por carácter al cifrar   (exp = e): {e:,}")
    print(f"  Pasos por carácter al descifrar (exp = d): {d:,}")

    # Entrada del usuario
    print()
    contrasena = input("  Ingrese la contraseña a cifrar: ").strip()
    if not contrasena:
        contrasena = "Hola123"
        print(f"  (usando valor por defecto: '{contrasena}')")

    longitud = len(contrasena)
    print(f"\n  Longitud del mensaje: {longitud} carácter(es)")
    print(f"  Pasos totales estimados al cifrar   : {e * longitud:,}")
    print(f"  Pasos totales estimados al descifrar: {d * longitud:,}")

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
    print("  (Este paso puede tardar varios segundos — ese es el punto)")

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
    print(f"\n  Compare estos resultados con rsa_rapido.py")
    print(separador)
