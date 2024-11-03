import numpy as np
from typing import List, Tuple, Set
import sys
from datetime import datetime

class EMDService:
    def calculate_emd(self, subset1: List[str], subset2: List[str], full_set: List[str]) -> float:
        """
        Calcula la Earth Mover's Distance entre dos subconjuntos
        """
        # Versión simplificada para prueba
        # En un caso real, aquí iría el cálculo completo del EMD
        return len(subset1) / (len(subset1) + len(subset2))
    
    def calculate_g(self, subset: Set[str], full_set: List[str]) -> float:
        """
        Calcula la función g (EMD) para un subconjunto dado
        """
        complement = set(full_set) - subset
        return self.calculate_emd(list(subset), list(complement), full_set)

    def find_candidate_pair(self, nodes: List[str]) -> Tuple[str, str]:
        """
        Encuentra un par candidato siguiendo el algoritmo descrito
        """
        sequence = []
        current_set = set()
        
        # Elegir primer elemento
        v1 = nodes[0]
        sequence.append(v1)
        current_set.add(v1)
        
        # Construir la secuencia
        remaining_nodes = set(nodes) - {v1}
        while remaining_nodes:
            min_g = float('inf')
            best_node = None
            
            for node in remaining_nodes:
                test_set = current_set | {node}
                g_value = self.calculate_g(test_set, nodes)
                
                if g_value < min_g:
                    min_g = g_value
                    best_node = node
            
            if best_node:
                sequence.append(best_node)
                current_set.add(best_node)
                remaining_nodes.remove(best_node)
        
        return sequence[-2], sequence[-1]

def find_optimal_partition(nodes: List[str]) -> dict:
    """
    Encuentra la partición óptima del conjunto de nodos
    """
    emd_service = EMDService()
    partitions = []
    
    def find_partitions(current_nodes: List[str]):
        if len(current_nodes) <= 2:
            return
            
        print(f"\nBuscando particiones para: {current_nodes}")
        
        # Encontrar par candidato
        node1, node2 = emd_service.find_candidate_pair(current_nodes)
        print(f"Par candidato encontrado: ({node1}, {node2})")
        
        # Calcular EMD para la partición actual
        subset1 = [node2]
        subset2 = [n for n in current_nodes if n != node2]
        emd_value = emd_service.calculate_emd(subset1, subset2, current_nodes)
        
        # Agregar partición candidata
        partition = {
            'subset1': subset1,
            'subset2': subset2,
            'emd_value': emd_value
        }
        partitions.append(partition)
        print(f"Partición candidata agregada: {partition}")
        
        # Fusionar nodos y continuar recursivamente
        merged_nodes = [n for n in current_nodes if n not in (node1, node2)]
        merged_nodes.append(f"{node1}_{node2}")
        find_partitions(merged_nodes)
    
    # Iniciar el proceso recursivo
    find_partitions(nodes)
    
    # Encontrar la partición óptima
    optimal_partition = min(partitions, key=lambda x: x['emd_value'])
    return optimal_partition

def main():
    # Configurar el ejemplo del sistema
    nodes = ['at', 'bt', 'at+1', 'bt+1']
    print(f"Sistema inicial: {nodes}")
    
    # Encontrar la partición óptima
    print("\nBuscando partición óptima...")
    result = find_optimal_partition(nodes)
    
    # Mostrar resultados
    print("\nResultados:")
    print(f"Partición óptima encontrada:")
    print(f"Subset 1: {result['subset1']}")
    print(f"Subset 2: {result['subset2']}")
    print(f"Valor EMD: {result['emd_value']}")

if __name__ == "__main__":
    main()