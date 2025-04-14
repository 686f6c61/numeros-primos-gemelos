"""
Versión optimizada del generador de números primos gemelos

Este módulo implementa la Criba de Eratóstenes para encontrar primos 
de manera más eficiente, lo que permite trabajar con límites mucho más grandes.
"""

import numpy as np
import matplotlib.pyplot as plt
from time import time

def criba_eratostenes(limite):
    """
    Implementación de la Criba de Eratóstenes para encontrar todos los
    números primos hasta un límite dado de manera eficiente.
    
    Args:
        limite (int): Límite superior hasta donde buscar primos
        
    Returns:
        list: Lista de números primos encontrados
    """
    # Creamos un array booleano para marcar los números primos
    # Inicialmente asumimos que todos son primos (True)
    es_primo = np.ones(limite + 1, dtype=bool)
    
    # 0 y 1 no son primos
    es_primo[0] = es_primo[1] = False
    
    # Aplicamos la criba
    for i in range(2, int(np.sqrt(limite)) + 1):
        if es_primo[i]:
            # Marcamos como no primos todos los múltiplos de i
            # empezando desde i*i (los anteriores ya fueron marcados)
            es_primo[i*i:limite+1:i] = False
    
    # Convertimos el array booleano a lista de números primos
    return np.where(es_primo)[0]

def encontrar_primos_gemelos_optimizado(limite):
    """
    Encuentra todos los pares de primos gemelos hasta un límite dado
    utilizando la Criba de Eratóstenes.
    
    Args:
        limite (int): Límite superior hasta donde buscar primos gemelos
        
    Returns:
        list: Lista de tuplas, cada una conteniendo un par de primos gemelos
    """
    # Obtenemos todos los primos hasta el límite
    primos = criba_eratostenes(limite)
    gemelos = []
    
    # Buscamos los pares con diferencia de 2
    for i in range(len(primos) - 1):
        if primos[i + 1] - primos[i] == 2:
            gemelos.append((primos[i], primos[i + 1]))
    
    return gemelos

def comparar_rendimiento(limite):
    """
    Compara el rendimiento entre el método básico y el optimizado
    para encontrar primos gemelos.
    
    Args:
        limite (int): Límite superior hasta donde buscar primos gemelos
        
    Returns:
        tuple: (tiempo_basico, tiempo_optimizado, cantidad_gemelos)
    """
    # Importamos la función del método básico
    from gemelos import encontrar_primos_gemelos as metodo_basico
    
    # Medimos el tiempo del método básico
    inicio = time()
    gemelos_basico = metodo_basico(limite)
    tiempo_basico = time() - inicio
    
    # Medimos el tiempo del método optimizado
    inicio = time()
    gemelos_optimizado = encontrar_primos_gemelos_optimizado(limite)
    tiempo_optimizado = time() - inicio
    
    # Verificamos que ambos métodos den los mismos resultados
    assert len(gemelos_basico) == len(gemelos_optimizado), "Los métodos dieron resultados diferentes"
    
    return tiempo_basico, tiempo_optimizado, len(gemelos_optimizado)

def graficar_comparacion(limites):
    """
    Genera un gráfico comparando el rendimiento de ambos métodos
    para diferentes límites.
    
    Args:
        limites (list): Lista de límites a comparar
    """
    tiempos_basico = []
    tiempos_optimizado = []
    cantidades = []
    
    for limite in limites:
        print(f"Comparando rendimiento para límite {limite}...")
        tiempo_basico, tiempo_optimizado, cantidad = comparar_rendimiento(limite)
        
        tiempos_basico.append(tiempo_basico)
        tiempos_optimizado.append(tiempo_optimizado)
        cantidades.append(cantidad)
        
        print(f"  Método básico: {tiempo_basico:.4f} segundos")
        print(f"  Método optimizado: {tiempo_optimizado:.4f} segundos")
        print(f"  Mejora: {tiempo_basico/tiempo_optimizado:.2f}x más rápido")
        print(f"  Cantidad de pares gemelos: {cantidad}")
    
    # Crear el gráfico de barras comparativo
    plt.figure(figsize=(12, 6))
    indices = np.arange(len(limites))
    width = 0.35
    
    plt.bar(indices - width/2, tiempos_basico, width, label='Método Básico')
    plt.bar(indices + width/2, tiempos_optimizado, width, label='Método Optimizado (Criba)')
    
    plt.title('Comparación de Rendimiento: Búsqueda de Primos Gemelos')
    plt.xlabel('Límite')
    plt.ylabel('Tiempo (segundos)')
    plt.xticks(indices, [str(l) for l in limites])
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # Agregar etiquetas con la cantidad de pares encontrados
    for i, cantidad in enumerate(cantidades):
        plt.text(i, max(tiempos_basico[i], tiempos_optimizado[i]) + 0.05, 
                 f"{cantidad} pares", ha='center')
    
    plt.tight_layout()
    plt.savefig('comparacion_rendimiento.png')
    plt.show()

if __name__ == "__main__":
    print("=" * 50)
    print("COMPARACIÓN DE RENDIMIENTO: MÉTODOS PARA PRIMOS GEMELOS")
    print("=" * 50)
    print("\nEste programa compara el rendimiento entre el método básico")
    print("y el método optimizado (Criba de Eratóstenes) para encontrar")
    print("primos gemelos hasta diferentes límites.")
    
    # Definimos límites predeterminados para la comparación
    limites_predeterminados = [1000, 5000, 10000, 50000]
    
    usar_predeterminados = input("\n¿Usar límites predeterminados? (s/n): ").lower() == 's'
    
    if usar_predeterminados:
        limites = limites_predeterminados
    else:
        limites = []
        while True:
            try:
                limite = int(input("\nIntroduce un límite (0 para terminar): "))
                if limite == 0:
                    break
                if limite <= 0:
                    print("Por favor, introduce un número positivo.")
                    continue
                limites.append(limite)
            except ValueError:
                print("Por favor, introduce un número entero válido.")
    
    if limites:
        graficar_comparacion(limites)
    else:
        print("No se ingresaron límites para comparar.") 