#!/usr/bin/env python3
"""
Script para analizar y visualizar los resultados de las pruebas de deployment
"""

import csv
import sys
from datetime import datetime

def load_results(filename='deployment_results.csv'):
    """Cargar resultados del CSV"""
    results = []
    try:
        with open(filename, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                results.append(row)
        return results
    except FileNotFoundError:
        print(f"Archivo {filename} no encontrado")
        return []

def analyze_results(results):
    """Analizar y mostrar estadísticas"""
    if not results:
        print("No hay resultados para analizar")
        return
    
    print("=" * 80)
    print("ANÁLISIS DE ESTRATEGIAS DE DEPLOYMENT")
    print("=" * 80)
    print()
    
    # Agrupar por estrategia
    strategies = {}
    for result in results:
        strategy = result['Strategy']
        duration = int(result['Duration (seconds)'])
        
        if strategy not in strategies:
            strategies[strategy] = []
        strategies[strategy].append(duration)
    
    # Calcular estadísticas
    stats = []
    for strategy, durations in strategies.items():
        avg = sum(durations) / len(durations)
        min_time = min(durations)
        max_time = max(durations)
        
        stats.append({
            'strategy': strategy,
            'count': len(durations),
            'avg': avg,
            'min': min_time,
            'max': max_time
        })
    
    # Ordenar por tiempo promedio
    stats.sort(key=lambda x: x['avg'])
    
    # Mostrar tabla
    print(f"{'Estrategia':<30} {'Pruebas':<10} {'Promedio':<15} {'Mínimo':<15} {'Máximo':<15}")
    print("-" * 85)
    
    for s in stats:
        avg_str = f"{s['avg']:.1f}s ({s['avg']/60:.1f}m)"
        min_str = f"{s['min']}s ({s['min']/60:.1f}m)"
        max_str = f"{s['max']}s ({s['max']/60:.1f}m)"
        
        print(f"{s['strategy']:<30} {s['count']:<10} {avg_str:<15} {min_str:<15} {max_str:<15}")
    
    print()
    print("=" * 80)
    print()
    
    # Ranking
    print("🏆 RANKING (de más rápido a más lento):")
    print()
    for i, s in enumerate(stats, 1):
        print(f"  {i}. {s['strategy']:<30} - {s['avg']:.1f}s promedio")
    
    print()
    print("=" * 80)
    print()
    
    # Detalles de cada prueba
    print("📋 DETALLE DE TODAS LAS PRUEBAS:")
    print()
    for result in results:
        duration = int(result['Duration (seconds)'])
        minutes = duration // 60
        seconds = duration % 60
        
        print(f"  • {result['Strategy']:<30} v{result['Version']:<15} {duration:>4}s ({minutes}m {seconds}s) - {result['Start Time']}")
    
    print()
    print("=" * 80)

def main():
    filename = sys.argv[1] if len(sys.argv) > 1 else 'deployment_results.csv'
    results = load_results(filename)
    
    if results:
        analyze_results(results)
        print()
        print(f"✓ Analizadas {len(results)} pruebas de deployment")
        print()
    else:
        print()
        print("💡 Ejecuta primero las pruebas de deployment:")
        print("   ./measure_single_deployment.sh AllAtOnce v1.0.1")
        print()

if __name__ == '__main__':
    main()

