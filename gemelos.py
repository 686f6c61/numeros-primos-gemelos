"""
Generador y Visualizador de Números Primos Gemelos

Este programa permite generar números primos gemelos y visualizarlos
de diferentes maneras para ayudar a entender sus patrones.

Los números primos gemelos son pares de números primos que difieren en 2,
como (3,5), (5,7), (11,13), (17,19), etc.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from time import time

def es_primo(n):
    """
    Determina si un número es primo verificando si es divisible por
    algún número desde 2 hasta la raíz cuadrada de n.
    
    Args:
        n (int): Número a verificar
        
    Returns:
        bool: True si es primo, False si no lo es
    """
    # Los números menores que 2 no son primos
    if n < 2:
        return False
        
    # Verificamos divisibilidad hasta la raíz cuadrada
    for i in range(2, int(np.sqrt(n)) + 1):
        if n % i == 0:
            return False
            
    return True

def generar_primos(limite):
    """
    Genera todos los números primos hasta un límite dado.
    
    Args:
        limite (int): Límite superior hasta donde generar primos
        
    Returns:
        list: Lista de números primos encontrados
    """
    primos = []
    
    for n in range(2, limite + 1):
        if es_primo(n):
            primos.append(n)
            
    return primos

def encontrar_primos_gemelos(limite):
    """
    Encuentra todos los pares de primos gemelos hasta un límite dado.
    
    Args:
        limite (int): Límite superior hasta donde buscar primos gemelos
        
    Returns:
        list: Lista de tuplas, cada una conteniendo un par de primos gemelos
    """
    primos = generar_primos(limite)
    gemelos = []
    
    for i in range(len(primos) - 1):
        if primos[i + 1] - primos[i] == 2:
            gemelos.append((primos[i], primos[i + 1]))
            
    return gemelos

def visualizar_recta_numerica(gemelos, limite):
    """
    Visualiza los primos gemelos como puntos conectados en una recta numérica.
    
    Args:
        gemelos (list): Lista de tuplas con pares de primos gemelos
        limite (int): Límite superior usado para generar los primos
    """
    plt.figure(figsize=(12, 4))
    
    # Dibujar la recta numérica
    plt.axhline(y=0, color='black', linestyle='-', alpha=0.3)
    
    # Marcar las posiciones de cada 10 unidades
    for i in range(0, limite + 1, 10):
        plt.axvline(x=i, color='gray', linestyle='--', alpha=0.2)
        plt.text(i, -0.15, str(i), ha='center')
    
    # Dibujar los primos gemelos
    for par in gemelos:
        # Dibujamos los puntos
        plt.plot([par[0], par[1]], [0, 0], 'ro', markersize=6)
        # Conectamos con una línea
        plt.plot([par[0], par[1]], [0, 0], 'r-', linewidth=2)
    
    plt.title(f'Primos Gemelos hasta {limite} en la Recta Numérica')
    plt.ylim(-0.5, 0.5)
    plt.xlim(-1, limite + 1)
    plt.grid(False)
    plt.yticks([])
    plt.tight_layout()
    plt.savefig('primos_gemelos_recta.png')
    plt.show()

def visualizar_dispersion(gemelos, limite):
    """
    Visualiza los primos gemelos como puntos en un diagrama de dispersión.
    El eje x representa el primer primo del par, y el eje y la diferencia (que siempre es 2).
    
    Args:
        gemelos (list): Lista de tuplas con pares de primos gemelos
        limite (int): Límite superior usado para generar los primos
    """
    plt.figure(figsize=(12, 6))
    
    # Extraer los primeros primos de cada par
    primeros_primos = [par[0] for par in gemelos]
    # La diferencia siempre es 2
    diferencias = [2] * len(gemelos)
    
    plt.scatter(primeros_primos, diferencias, color='blue', s=50, alpha=0.7)
    plt.title(f'Distribución de Primos Gemelos hasta {limite}')
    plt.xlabel('Primer Primo del Par')
    plt.ylabel('Diferencia entre Pares')
    plt.grid(True, alpha=0.3)
    plt.ylim(0, 4)  # Para que se vea bien la diferencia constante de 2
    plt.tight_layout()
    plt.savefig('primos_gemelos_dispersion.png')
    plt.show()

def visualizar_patron_espiral(gemelos, limite):
    """
    Visualiza los primos gemelos en una espiral, mostrando patrones interesantes.
    
    Args:
        gemelos (list): Lista de tuplas con pares de primos gemelos
        limite (int): Límite superior usado para generar los primos
    """
    plt.figure(figsize=(10, 10))
    
    # Extraer todos los primos que forman parte de pares gemelos
    primos_en_pares = []
    for par in gemelos:
        primos_en_pares.extend(par)
    
    # Generar coordenadas para la espiral (espiral de Arquímedes)
    theta = np.sqrt(np.arange(1, limite + 1))
    x = theta * np.cos(theta)
    y = theta * np.sin(theta)
    
    # Dibujar todos los números en la espiral (puntos pequeños y grises)
    plt.scatter(x, y, color='lightgray', s=10, alpha=0.3)
    
    # Resaltar los primos gemelos
    for primo in primos_en_pares:
        if primo <= limite:
            plt.scatter(x[primo-1], y[primo-1], color='red', s=50, alpha=0.8)
    
    plt.title(f'Espiral de Primos Gemelos hasta {limite}')
    plt.axis('equal')
    plt.grid(False)
    plt.axis('off')
    plt.tight_layout()
    plt.savefig('primos_gemelos_espiral.png')
    plt.show()

def visualizar_histograma_distancias(gemelos):
    """
    Visualiza un histograma de las distancias entre pares consecutivos de primos gemelos.
    
    Args:
        gemelos (list): Lista de tuplas con pares de primos gemelos
    """
    # Si hay menos de 2 pares, no podemos calcular distancias
    if len(gemelos) < 2:
        print("No hay suficientes pares de primos gemelos para crear el histograma de distancias.")
        return
    
    # Calcular las distancias entre pares consecutivos
    distancias = []
    for i in range(len(gemelos) - 1):
        # La distancia es la diferencia entre el primer primo del siguiente par
        # y el primer primo del par actual
        distancia = gemelos[i+1][0] - gemelos[i][0]
        distancias.append(distancia)
    
    plt.figure(figsize=(12, 6))
    plt.hist(distancias, bins=20, color='skyblue', edgecolor='black')
    plt.title('Histograma de Distancias entre Pares Consecutivos de Primos Gemelos')
    plt.xlabel('Distancia')
    plt.ylabel('Frecuencia')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('primos_gemelos_histograma.png')
    plt.show()

def visualizar_tendencia(gemelos, limite):
    """
    Visualiza la tendencia en las distancias entre pares consecutivos de primos gemelos.
    
    Args:
        gemelos (list): Lista de tuplas con pares de primos gemelos
        limite (int): Límite superior usado para generar los primos
    """
    # Si hay menos de 2 pares, no podemos calcular distancias
    if len(gemelos) < 2:
        print("No hay suficientes pares de primos gemelos para analizar la tendencia.")
        return
    
    # Calcular las distancias entre pares consecutivos
    distancias = []
    indices = []
    
    for i in range(len(gemelos) - 1):
        # La distancia es la diferencia entre el primer primo del siguiente par
        # y el primer primo del par actual
        distancia = gemelos[i+1][0] - gemelos[i][0]
        distancias.append(distancia)
        indices.append(i)
    
    plt.figure(figsize=(12, 6))
    
    # Scatter plot de las distancias
    plt.scatter(indices, distancias, color='blue', s=40, alpha=0.7)
    
    # Calcular la línea de tendencia
    try:
        from scipy import stats
        pendiente, intercepto, r_valor, p_valor, error_std = stats.linregress(
            indices, distancias)
        
        # Línea de tendencia
        x = np.array(indices)
        y = intercepto + pendiente * x
        plt.plot(x, y, 'r-', linewidth=2, 
                label=f'Tendencia: y = {pendiente:.4f}x + {intercepto:.2f}')
        
        # Añadir texto con coeficiente de correlación
        plt.text(0.05, 0.95, f'Correlación: {r_valor:.4f}', 
                transform=plt.gca().transAxes, fontsize=12,
                verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    except ImportError:
        print("Nota: La librería scipy no está instalada. No se mostrará la línea de tendencia.")
    
    plt.title('Tendencia en las Distancias entre Primos Gemelos')
    plt.xlabel('Índice del Par')
    plt.ylabel('Distancia')
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig('primos_gemelos_tendencia.png')
    plt.show()

def menu():
    """
    Muestra un menú interactivo para el usuario.
    """
    print("\n" + "="*50)
    print(" GENERADOR Y VISUALIZADOR DE NÚMEROS PRIMOS GEMELOS")
    print("="*50)
    
    while True:
        try:
            limite = int(input("\nIntroduce el límite hasta donde generar primos gemelos: "))
            if limite <= 0:
                print("Por favor, introduce un número positivo.")
                continue
            break
        except ValueError:
            print("Por favor, introduce un número entero válido.")
    
    print(f"\nGenerando primos gemelos hasta {limite}...")
    inicio = time()
    gemelos = encontrar_primos_gemelos(limite)
    fin = time()
    
    print(f"Se encontraron {len(gemelos)} pares de primos gemelos en {fin-inicio:.2f} segundos.")
    
    if gemelos:
        print("\nPares de primos gemelos encontrados:")
        for i, par in enumerate(gemelos):
            # Convertir los valores np.int64 a enteros normales
            par_limpio = (int(par[0]), int(par[1]))
            print(f"{i+1}. {par_limpio}")
    
    while True:
        print("\n" + "-"*50)
        print("OPCIONES DE VISUALIZACIÓN:")
        print("1. Recta numérica")
        print("2. Análisis de tendencia")
        print("3. Patrón en espiral")
        print("4. Histograma de distancias")
        print("5. Todas las visualizaciones")
        print("6. Cambiar límite")
        print("0. Salir")
        
        try:
            opcion = int(input("\nElige una opción (0-6): "))
            
            if opcion == 0:
                print("\n¡Gracias por usar el visualizador de primos gemelos!")
                break
                
            elif opcion == 1:
                print("\nGenerando visualización en recta numérica...")
                visualizar_recta_numerica(gemelos, limite)
                
            elif opcion == 2:
                print("\nGenerando análisis de tendencia...")
                visualizar_tendencia(gemelos, limite)
                
            elif opcion == 3:
                print("\nGenerando patrón en espiral...")
                visualizar_patron_espiral(gemelos, limite)
                
            elif opcion == 4:
                print("\nGenerando histograma de distancias...")
                visualizar_histograma_distancias(gemelos)
                
            elif opcion == 5:
                print("\nGenerando todas las visualizaciones...")
                visualizar_recta_numerica(gemelos, limite)
                visualizar_tendencia(gemelos, limite)
                visualizar_patron_espiral(gemelos, limite)
                visualizar_histograma_distancias(gemelos)
                
            elif opcion == 6:
                menu()  # Reiniciar el menú
                return
                
            else:
                print("Opción no válida. Por favor, elige entre 0 y 6.")
                
        except ValueError:
            print("Por favor, introduce un número entero válido.")

if __name__ == "__main__":
    menu() 