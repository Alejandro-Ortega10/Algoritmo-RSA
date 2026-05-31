# Exponenciación Modular Rápida aplicada a RSA

---

## Descripción del proyecto

Este proyecto demuestra de forma práctica y medible cómo un cambio de algoritmo —sin modificar el problema ni el hardware— puede transformar una operación que tarda varios segundos en una que termina en microsegundos.

El problema central es calcular `a ^ n mod m` para valores grandes de `n`, operación que es el núcleo del cifrado RSA. El método ingenuo lo resuelve multiplicando `n` veces (complejidad `O(n)`). El método optimizado inspecciona los dígitos binarios del exponente y dobla el resultado en cada paso, logrando el mismo resultado en solo `log₂(n)` multiplicaciones (complejidad `O(log n)`).

Para un exponente de descifrado típico como `d = 832.193`, la diferencia es:

| | Ingenuo O(n) | Rápido O(log n) |
|---|---|---|
| Pasos por carácter | 832.193 | ~40 |
| Factor de reducción | — | ×20.000 aprox. |

---

## Requisitos

Se requiere **Python 3.8 o superior**. Se recomienda usar un entorno virtual para no afectar otras instalaciones de Python en el sistema.

**1. Crear el entorno virtual**

```bash
python -m venv entorno
```

**2. Activarlo**

En Windows:
```bash
entorno\Scripts\activate
```

En macOS y Linux:
```bash
source entorno/bin/activate
```

**3. Instalar las dependencias**

```bash
pip install -r requirements.txt
```

Todos los cálculos matemáticos (primalidad, máximo común divisor, inverso modular, exponenciación) están implementados desde cero en las funciones de cada script, sin librerías externas adicionales.

---

## Cómo ejecutar cada archivo

### Script principal — comparador

Es el punto de entrada recomendado. Pide una palabra, la procesa con ambos métodos y genera una figura con 6 paneles comparativos.

Los tres archivos deben estar en el mismo directorio.

```bash
python comparador_rsa.py
```

El programa pedirá la palabra por consola:

```
  Ingrese la palabra a cifrar: Universidad
```

Al terminar imprime una tabla comparativa en consola y abre una ventana con los gráficos. También guarda la figura como archivo `.png` en el mismo directorio.

---

### Script ingenuo

Demuestra el comportamiento lento. Se puede ejecutar de forma independiente.

```bash
python rsa_ingenuo.py
```

Muestra paso a paso: generación de claves, cifrado carácter a carácter, descifrado, cantidad de pasos realizados y tiempo total. El descifrado puede tardar varios segundos con palabras largas; eso es exactamente lo que se busca ilustrar.

---

### Script rápido

Mismo flujo que el ingenuo, pero usando exponenciación por cuadrados. La ejecución es prácticamente instantánea.

```bash
python rsa_rapido.py
```

Para comparar correctamente, ingresar la misma palabra en ambos scripts y observar la diferencia de pasos y tiempo.

---

## Descripción de las funciones

### `rsa_ingenuo.py` y `rsa_rapido.py`

Ambos scripts tienen exactamente las mismas funciones. La única diferencia está en la implementación de la función de exponenciación.

| Función | Descripción |
|---|---|
| `es_primo(numero)` | Determina si un número es primo mediante división de prueba hasta su raíz cuadrada. |
| `maximo_comun_divisor(a, b)` | Calcula el MCD de dos enteros con el algoritmo de Euclides. |
| `inverso_modular(e, phi)` | Encuentra `d` tal que `(e × d) mod phi = 1`, usando el algoritmo de Euclides extendido. Se usa para obtener la clave privada. |
| `potencia_directa(base, exp, mod)` | **Solo en `rsa_ingenuo.py`.** Calcula `base ^ exp mod m` multiplicando `exp` veces. Complejidad `O(n)`. Incrementa `contador_pasos` en cada multiplicación. |
| `potencia_rapida(base, exp, mod)` | **Solo en `rsa_rapido.py`.** Calcula `base ^ exp mod m` inspeccionando los bits del exponente. Complejidad `O(log n)`. Incrementa `contador_pasos` en cada operación. |
| `generar_claves(p, q)` | Genera el par de claves RSA a partir de dos números primos. Retorna `(e, n)` como clave pública y `(d, n)` como clave privada. |
| `texto_a_numeros(texto)` | Convierte cada carácter del texto a su valor numérico Unicode (`ord`). |
| `numeros_a_texto(lista)` | Convierte una lista de enteros de vuelta a texto (`chr`). |
| `cifrar_valor(valor, e, n)` | Cifra un único entero: calcula `valor ^ e mod n`. |
| `descifrar_valor(cifrado, d, n)` | Descifra un único entero: calcula `cifrado ^ d mod n`. |
| `cifrar_mensaje(mensaje, clave_publica)` | Convierte el mensaje a números y cifra cada uno. Retorna una lista de enteros. |
| `descifrar_mensaje(lista, clave_privada)` | Descifra la lista de enteros y reconstruye el texto original. |

---

### `comparador_rsa.py`

| Función | Descripción |
|---|---|
| `ejecutar_metodo_ingenuo(palabra, cp, cv)` | Llama a `rsa_ingenuo` para cifrar y descifrar la palabra. Mide pasos y tiempo por separado y los retorna en un diccionario. |
| `ejecutar_metodo_rapido(palabra, cp, cv)` | Igual que la anterior, pero usando `rsa_rapido`. |
| `medir_escala(longitudes, ...)` | Cifra palabras de distintas longitudes con ambos métodos y registra cuántos pasos usa cada uno. Los datos alimentan la curva de escalado. |
| `dibujar_barras_pasos(ax, ...)` | Dibuja un par de barras comparando la cantidad de pasos. Usa escala logarítmica y anota el factor de reducción en verde. |
| `dibujar_barras_tiempo(ax, ...)` | Igual que la anterior, pero para tiempos en milisegundos. |
| `dibujar_escala(ax, ...)` | Traza dos curvas mostrando cómo crece el número de pasos según la longitud de la palabra. |
| `dibujar_panel_resumen(ax, ...)` | Genera una tabla de texto dentro de un panel de la figura con todos los valores numéricos del resultado. |
| `construir_figura(...)` | Arma la figura completa con los 6 paneles en una cuadrícula de 2×4. |

---

## Descripción de los gráficos generados

Al ejecutar `comparador_rsa.py` se genera una figura con seis paneles:

**Fila superior — cuatro barras comparativas**

Los primeros dos paneles muestran la cantidad de pasos usados durante el cifrado y el descifrado respectivamente. Los dos siguientes muestran el tiempo en milisegundos para cada etapa. Todos usan escala logarítmica porque la diferencia entre métodos es tan grande que en escala lineal la barra del método rápido sería invisible. Sobre cada barra aparece el valor exacto y, en verde, el factor de reducción respecto al método ingenuo.

**Fila inferior izquierda — curva de escalado**

Muestra cómo crece el número de pasos cuando la palabra tiene 1, 2, 3... N caracteres. La curva naranja (ingenuo) sube en línea recta porque cada carácter extra añade exactamente `e` o `d` pasos. La curva verde (rápido) sube de forma casi plana porque cada carácter extra solo añade `~2 × log₂(e)` pasos.

**Fila inferior derecha — tabla resumen**

Reúne todos los números en un solo panel: pasos y tiempos de cifrado y descifrado por separado, totales, factores de reducción y verificación de que ambos métodos recuperaron correctamente la palabra original.

---

## Parámetros RSA utilizados

| Parámetro | Valor | Descripción |
|---|---|---|
| `p` | 1.009 | Primer número primo |
| `q` | 1.013 | Segundo número primo |
| `n = p × q` | 1.022.117 | Módulo público |
| `φ(n) = (p−1)(q−1)` | 1.020.096 | Función de Euler |
| `e` | 65.537 | Exponente público (clave pública) |
| `d` | 832.193 | Exponente privado (clave privada) |

Los primos son pequeños por razones didácticas. En RSA real se usan primos de al menos 1024 bits cada uno, lo que hace al método ingenuo absolutamente inviable y al método rápido la única opción posible.

---

