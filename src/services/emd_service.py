# services/emd_service.py

import numpy as np
from scipy.optimize import linear_sum_assignment

class EMDService:
    def calculate_emd(self, subset1, subset2, full_set):
        """
        Calcula la Earth Mover's Distance entre dos subconjuntos
        
        Args:
            subset1: Primer subconjunto de nodos
            subset2: Segundo subconjunto de nodos
            full_set: Conjunto completo de nodos
        
        Returns:
            float: Valor EMD calculado
        """
        # Calcular las distribuciones de probabilidad
        p_m = self._calculate_probability_distribution(subset1)
        p_m_complement = self._calculate_probability_distribution(subset2)
        p_v = self._calculate_probability_distribution(full_set)
        
        # Calcular el producto tensorial
        p_tensor = np.outer(p_m, p_m_complement)
        
        # Calcular la matriz de costos
        cost_matrix = self._calculate_cost_matrix(p_tensor, p_v)
        
        # Resolver el problema de transporte usando el algoritmo húngaro
        row_ind, col_ind = linear_sum_assignment(cost_matrix)
        
        # Calcular EMD
        emd = cost_matrix[row_ind, col_ind].sum()
        
        return emd
    
    def _calculate_probability_distribution(self, nodes):
        """
        Calcula la distribución de probabilidad para un conjunto de nodos
        """
        if not nodes:
            return np.zeros(len(nodes))
        
        total = sum(1 for _ in nodes)
        return np.array([1/total] * len(nodes))
    
    def _calculate_cost_matrix(self, p_tensor, p_v):
        """
        Calcula la matriz de costos para el EMD
        """
        n = len(p_tensor)
        m = len(p_v)
        cost_matrix = np.zeros((n, m))
        
        for i in range(n):
            for j in range(m):
                cost_matrix[i,j] = abs(p_tensor[i] - p_v[j])
        
        return cost_matrix
    
    def find_candidate_pair(self, nodes):
        """
        Encuentra un par candidato según el algoritmo descrito
        """
        if len(nodes) < 2:
            return None, None
            
        sequence = []
        current_set = set()
        
        # Elegir el primer elemento
        v1 = nodes[0]
        sequence.append(v1)
        current_set.add(v1)
        
        # Construir la secuencia Wi
        remaining_nodes = set(nodes) - {v1}
        
        while remaining_nodes:
            min_g = float('inf')
            best_node = None
            
            # Para cada nodo restante, calcular g(Wi ∪ {u}) - g({u})
            for node in remaining_nodes:
                test_set = current_set | {node}
                g_union = self.calculate_g(test_set, nodes)
                g_single = self.calculate_g({node}, nodes)
                
                diff = g_union - g_single
                if diff < min_g:
                    min_g = diff
                    best_node = node
            
            sequence.append(best_node)
            current_set.add(best_node)
            remaining_nodes.remove(best_node)
        
        # Retornar el par candidato (penúltimo, último)
        return sequence[-2], sequence[-1]
    
    def calculate_g(self, subset, full_set):
        """
        Calcula la función g (EMD) para un subconjunto dado
        """
        # Obtener el complemento del subconjunto
        complement = set(full_set) - set(subset)
        
        # Si alguno de los conjuntos está vacío, retornar un valor alto
        if not subset or not complement:
            return float('inf')
            
        return self.calculate_emd(list(subset), list(complement), full_set)