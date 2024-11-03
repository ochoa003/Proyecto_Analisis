# controllers/partition_controller.py
from loopback import Controller, post, get
from ..services.emd_service import EMDService

class PartitionController(Controller):
    def __init__(self):
        self.emd_service = EMDService()

    @post('/find-optimal-partition')
    async def find_optimal_partition(self, nodes):
        partitions = []
        
        def find_partitions(current_nodes):
            if len(current_nodes) <= 2:
                return
                
            # Encontrar par candidato
            node1, node2 = self.emd_service.find_candidate_pair(current_nodes)
            
            # Calcular EMD para la partición actual
            subset1 = [node2]
            subset2 = [n for n in current_nodes if n != node2]
            emd_value = self.emd_service.calculate_emd(subset1, subset2, current_nodes)
            
            # Agregar partición candidata
            partitions.append({
                'subset1': subset1,
                'subset2': subset2,
                'emd_value': emd_value
            })
            
            # Fusionar nodos y continuar recursivamente
            merged_nodes = [n for n in current_nodes if n not in (node1, node2)]
            merged_nodes.append(f"{node1}_{node2}")
            find_partitions(merged_nodes)
        
        # Iniciar el proceso recursivo
        find_partitions(nodes)
        
        # Encontrar la partición óptima
        optimal_partition = min(partitions, key=lambda x: x['emd_value'])
        return optimal_partition