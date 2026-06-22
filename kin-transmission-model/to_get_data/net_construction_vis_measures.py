import networkx as nx
import matplotlib.pyplot as plt
import random
from collections import defaultdict

### List of main functions in this file
# create_vis_geral: creates a graph to visualize all the connections, a family or general kinship graph.
# centralidad: Gets measures of centrality
# gerais: gets measures of the network
# p_graph: A p graph specially for cases with no clans
# p_graph_attribute: a p graph considering clans and distribuing the nodes according to some attribute
# marriage_graph_attribute: a marriage considering clans and distribuing the nodes according to some attribute. Only with the [9] uds
# egocentric_indiv: All the connections by UD
# small_ego_genealogy: a small genealogy for a UD in a pgraph style
# count_links_between_and_within: a count, specially used with the graph of marriages, that gets the counts in or out of certain attribute
# general_charactersitics_data: create a dataset with general aspects



# Functions for the simulation.
#This is not used
def lista_em_listas(graph, node_id, nested_list):
    for item in nested_list:
        if isinstance(item, list):
            lista_em_listas(graph, node_id, item)
        elif item is not None:
            graph.add_edge(node_id, item)

#This "disentangles" the list of parents
def disentangle_function(nested_list):
    result = []
    for item in nested_list:
        if isinstance(item, list):
            result.extend(disentangle_function(item))
        elif item is not None:
            result.append(item)
    return result

#Big network. Network for exchange. If measures == True, get the measures
def create_vis_geral(uds_copy, measures=False, df_step=None):
    def draw_network(Gg, measures):
        # Vis_graph
        pos = nx.spring_layout(Gg, k=1)
        plt.figure(figsize=(17, 10))
        nx.draw(Gg, pos, with_labels=True, node_size=1, node_color='lightblue', font_color='black') #small
        #nx.draw(Gg, pos, with_labels=True, node_size=4000, labels=node_labels, node_color='lightblue', font_size=8, font_color='black')
        plt.title(f"Network of the UDs. Nodes: {len(Gg.nodes)}")
        plt.show()

        if measures == True:
            # Centrality and general measures
            centralidad(Gg)
            gerais(Gg)
        print("----------------------------")
        return Gg
    
    if uds_copy != None:
        Gg = nx.Graph()
        # Alive
        ud_vivas = [ud for id, ud in uds_copy.items() if ud.activa == True]
        id_ud_vivas = [ud.id for ud in ud_vivas]

        for viva in ud_vivas:
            Gg.add_node(viva.id, ID=viva.id, age=viva.age, 
                        Community=viva.community, 
                        filhos=len(viva.parentes[2]) if viva.parentes[2] is not None else 0)
            
            for n in disentangle_function(viva.parentes[:9]):
                if n in id_ud_vivas:
                    Gg.add_edge(viva.id, n)
        Gg = draw_network(Gg, measures)
        return Gg
        
    else:
        def network_by_step(df_filtrado):
            # Graph
            Gg = nx.Graph()
            # Nodes
            nodos = df_filtrado["source"].tolist() + df_filtrado["target"].tolist()
            Gg.add_nodes_from(set(nodos))
            # Connections
            for i, fila in df_filtrado.iterrows():
                source = fila["source"]
                target = fila["target"]
                Gg.add_edge(source, target)
            return Gg
        
        steps_unicos = df_step["step"].unique()
        print(steps_unicos)
        for step in steps_unicos:
            # Filtra el dataframe por el valor actual de step
            df_filtrado = df_step[df_step["step"] == step]

            # Crea la red para el step actual
            G_step = network_by_step(df_filtrado)
            draw_network(G_step, measures)
#             Gg = draw_network(Gg, measures)
#         return Gg

    
#Centralities  
def centralidad(Gg):
    # 1. Degree distribution and other measures
    # (betweenness centrality)
    betweenness_centrality = nx.betweenness_centrality(Gg)
    # (closeness centrality)
    closeness_centrality = nx.closeness_centrality(Gg)
    # (degree centrality)
    degree_centrality = nx.degree_centrality(Gg)
    # (Eigenvector centrality)
    try:
        eigenvector_centrality = nx.eigenvector_centrality(Gg)
    except:
        eigenvector_centrality = nx.eigenvector_centrality_numpy(Gg)
    # Print first 10
    print("Betweenness Centrality:")
    print({k: v for k, v in sorted(betweenness_centrality.items(), key=lambda item: item[1], reverse=True)[:10]})

    print("\nCloseness Centrality:")
    print({k: v for k, v in sorted(closeness_centrality.items(), key=lambda item: item[1], reverse=True)[:10]})

    print("\nDegree Centrality:")
    print({k: v for k, v in sorted(degree_centrality.items(), key=lambda item: item[1], reverse=True)[:10]})

    print("\nEigenvector Centrality:")
    print({k: v for k, v in sorted(eigenvector_centrality.items(), key=lambda item: item[1], reverse=True)[:10]})

    degree_sequence = [d for n, d in Gg.degree()]
    plt.hist(degree_sequence, bins='auto', alpha=0.7, color='blue', edgecolor='black')
    plt.title('Distribucao do degree no Gg')
    plt.xlabel('Degree')
    plt.ylabel('Frecuencia')
    plt.show()
    
#General measures
def gerais(Gg):
    # 2. General measures
    # Densidad
    density = nx.density(Gg)

    # Nodes and edges
    num_nodes = Gg.number_of_nodes()
    num_edges = Gg.number_of_edges()

    # IF connected
    if nx.is_connected(Gg):
        diameter = nx.diameter(Gg)
        short = nx.average_shortest_path_length(Gg)
        cluster = nx.average_clustering(Gg)
        
    else:
        # Diameter, and other things
        components = [Gg.subgraph(component) for component in nx.connected_components(Gg)]
        diameter_by_component = [nx.diameter(component) for component in components]
        short_per_component = [nx.average_shortest_path_length(component) for component in components]
        clustering_per_component = [nx.average_clustering(component) for component in components]
        diameter = max(diameter_by_component)  # Tomar el máximo diámetro de las componentes
        short = max(short_per_component)
        cluster = max(clustering_per_component)

    # Coeficiente de Clustering Promedio
    #average_clustering = nx.average_clustering(Gg)

    # Transitividad
    transitivity = nx.transitivity(Gg)

    # Show them:
    print(f"Densidade: {density}")
    print(f"Número de nós: {num_nodes}")
    print(f"Número de aristas: {num_edges}")
    print(f"Diámetro: {diameter}")
    print(f"Transitividade: {transitivity}")
    print(f"Average shorthest path: {short}")
    print(f"Coeficiente de Clustering Promedio (cluster maior): {cluster}")

def network_measures(Gg):
    # Density
    density = nx.density(Gg)

    # Nodes and edges
    num_nodes = Gg.number_of_nodes()
    num_edges = Gg.number_of_edges()

    # Strongly Connected Components
    strongly_connected_components = list(nx.strongly_connected_components(Gg))
    num_strongly_connected_components = len(strongly_connected_components)
    largest_strongly_connected_component_size = max(len(comp) for comp in strongly_connected_components)

    # Weakly Connected Components
    weakly_connected_components = list(nx.weakly_connected_components(Gg))
    num_weakly_connected_components = len(weakly_connected_components)
    largest_weakly_connected_component_size = max(len(comp) for comp in weakly_connected_components)

    # Diameter and Average Shortest Path Length
    if nx.is_strongly_connected(Gg):
        diameter = nx.diameter(Gg)
        avg_shortest_path_length = nx.average_shortest_path_length(Gg)
    else:
        diameter = float('inf')  # Infinite diameter if the graph is not strongly connected
        avg_shortest_path_length = float('inf')

    # Transitivity
    transitivity = nx.transitivity(Gg.to_undirected())

    # Reciprocity
    reciprocity = nx.reciprocity(Gg)

    # Assortativity
    assortativity = nx.degree_assortativity_coefficient(Gg)

    # Show them
    print(f"Densidade: {density}")
    print(f"Número de nós: {num_nodes}")
    print(f"Número de aristas: {num_edges}")
    print(f"Número de componentes fortemente conectadas: {num_strongly_connected_components}")
    print(f"Tamanho do maior componente fortemente conectado: {largest_strongly_connected_component_size}")
    print(f"Número de componentes fracamente conectadas: {num_weakly_connected_components}")
    print(f"Tamanho do maior componente fracamente conectado: {largest_weakly_connected_component_size}")
    print(f"Diâmetro: {diameter}")
    print(f"Comprimento médio do caminho mais curto: {avg_shortest_path_length}")
    print(f"Transitividade: {transitivity}")
    print(f"Reciprocidade: {reciprocity}")
    print(f"Assortatividade: {assortativity}")    
    
def gerais_directed(Gg):
    # General measures for a directed graph
    # Density
    density = nx.density(Gg)

    # Nodes and edges
    num_nodes = Gg.number_of_nodes()
    num_edges = Gg.number_of_edges()

    # If strongly connected
    if nx.is_strongly_connected(Gg):
        diameter = nx.diameter(Gg)
        short = nx.average_shortest_path_length(Gg)
        cluster = nx.average_clustering(Gg.to_undirected())
    else:
        # Diameter, and other things
        components = [Gg.subgraph(component) for component in nx.strongly_connected_components(Gg)]
        diameter_by_component = [nx.diameter(component) for component in components if nx.is_strongly_connected(component)]
        short_per_component = [nx.average_shortest_path_length(component) for component in components if nx.is_strongly_connected(component)]
        clustering_per_component = [nx.average_clustering(component.to_undirected()) for component in components]
        diameter = max(diameter_by_component) if diameter_by_component else float('inf')
        short = max(short_per_component) if short_per_component else float('inf')
        cluster = max(clustering_per_component) if clustering_per_component else 0

    # Transitivity (also known as the global clustering coefficient)
    transitivity = nx.transitivity(Gg.to_undirected())

    # Show them:
    print(f"Densidade: {density}")
    print(f"Número de nós: {num_nodes}")
    print(f"Número de aristas: {num_edges}")
    print(f"Diámetro: {diameter}")
    print(f"Transitividade: {transitivity}")
    print(f"Average shortest path: {short}")
    print(f"Coeficiente de Clustering Promedio (cluster maior): {cluster}")


def p_graph(uds_copy, measures=False):
    G = nx.DiGraph()

    # Actives
    ud_vivas = {id_ud: ud for id_ud, ud in uds_copy.items() if ud.activa}

    # Agregar nodos al grafo con atributos (incluyendo edad)
    for id_ud, ud in ud_vivas.items():
        G.add_node(id_ud, ID=id_ud, age=ud.age, filhos=len(ud.parentes[2]) if ud.parentes[2] is not None else 0)

    # Agregar aristas (edges) entre nodos y sus padres
    for id_ud, ud in ud_vivas.items():
        if ud.parentes[0] is not None and ud.parentes[0] in ud_vivas:
            G.add_edge(id_ud, ud.parentes[0])
        if ud.parentes[1] is not None and ud.parentes[1] in ud_vivas:
            G.add_edge(id_ud, ud.parentes[1], color='red')  # Agregar atributo de color a la arista

    # Definir posiciones aleatorias iniciales en el eje x
    node_pos = {id_ud: (random.random(), ud.age) for id_ud, ud in ud_vivas.items()}
    
    for id_ud, ud in ud_vivas.items():
        if ud.parentes[0] is not None and ud.parentes[0] in node_pos:
            parent_x = (node_pos[ud.parentes[0]][0] + random.choice([-0.005, 0.005]))
            node_pos[id_ud] = (parent_x, ud.age)

    # Dibujar el grafo
    edge_colors = [G[u][v].get('color', 'blue') for u, v in G.edges]  # Obtener colores de las aristas

    plt.figure(figsize=(17, 10))
    nx.draw_networkx_nodes(G, node_pos, node_size=100, node_color='lightblue')
    nx.draw_networkx_edges(G, node_pos, edge_color=edge_colors, arrows=True, arrowsize=10)
    plt.title("P graph")
    plt.xlabel('')
    plt.ylabel('Age')
    plt.show()

    if measures:
        # Histograms
        outdegree_values = [outdegree for _, outdegree in G.out_degree()]
        indegree_values = [indegree for _, indegree in G.in_degree()]

        plt.figure(figsize=(12, 6))
        plt.subplot(1, 2, 1)
        plt.hist(outdegree_values, bins=20, color='blue', alpha=0.7)
        plt.title('Distribución de Outdegree del P-Graph')
        plt.xlabel('Outdegree')
        plt.ylabel('Frecuencia')

        plt.subplot(1, 2, 2)
        plt.hist(indegree_values, bins=20, color='green', alpha=0.7)
        plt.title('Distribución de Indegree del P-Graph')
        plt.xlabel('Indegree')
        plt.ylabel('Frecuencia')

        plt.tight_layout()
        plt.show()

    return G

def p_graph_attribute(uds_copy, attribute, measures=False, vis=False):
    G = nx.DiGraph()
    ud_vivas = uds_copy

    # Nodes
    for id_ud, ud in ud_vivas.items():
        node_attrs = {
            'ID': id_ud,
            'age': ud.age,
            'children': ud.parentes[2] if ud.parentes[2] is not None else [],
            'father': ud.parentes[0] if ud.parentes[0] in ud_vivas else None, 
            'mother': ud.parentes[1] if ud.parentes[1] in ud_vivas else None,
            attribute: getattr(ud, attribute, None)
        }
        G.add_node(id_ud, **node_attrs)

    # Links
    for id_ud, ud in ud_vivas.items():
        if ud.parentes[0] is not None and ud.parentes[0] in ud_vivas:
            G.add_edge(id_ud, ud.parentes[0])
        if ud.parentes[1] is not None and ud.parentes[1] in ud_vivas:
            G.add_edge(id_ud, ud.parentes[1], color='red')

    # Atributes
    attribute_values = set(getattr(ud, attribute) for ud in ud_vivas.values())
    if vis:
        # Position according to the attribute. To visualize the patterns... if possible
        pos = {}
        offset = 5  # Separation between groups
        for i, value in enumerate(attribute_values):
            nodes_in_value = [id_ud for id_ud, ud in ud_vivas.items() if getattr(ud, attribute) == value]
            for node in nodes_in_value:
                pos[node] = (random.random() + i * offset, ud_vivas[node].age)

        # colors
        edge_colors = [G[u][v].get('color', 'blue') for u, v in G.edges]
        # Graph
        plt.figure(figsize=(17, 10))
        nx.draw_networkx_nodes(G, pos, node_size=25)
        nx.draw_networkx_edges(G, pos, edge_color=edge_colors, arrows=True, arrowsize=10)
        nx.draw_networkx_labels(G, pos, labels={node: str(ud_vivas[node].id) for node in G.nodes}, font_size=12)  # Add labels for node ages
        plt.title(f"P graph by {attribute}")
        plt.xlabel('')
        plt.ylabel('Age')
        plt.show()

    if measures:
        # Histogram
        outdegree_values = [outdegree for _, outdegree in G.out_degree()]
        indegree_values = [indegree for _, indegree in G.in_degree()]

        plt.figure(figsize=(12, 6))
        plt.subplot(1, 2, 1)
        plt.hist(outdegree_values, bins=20, color='blue', alpha=0.7)
        plt.title(f"P-graph outdegree's distribution")
        plt.xlabel('Outdegree')
        plt.ylabel('Frequency')

        plt.subplot(1, 2, 2)
        plt.hist(indegree_values, bins=20, color='green', alpha=0.7)
        plt.title(f"P-graph indegree's distribution")
        plt.xlabel('Indegree')
        plt.ylabel('Frequency')

        plt.tight_layout()
        plt.show()
        gerais_directed(G)
        network_measures(G)
        

    return G

def marriage_graph_attribute(uds_copy, attribute, measures=False):
    G = nx.Graph()
    ud_vivas = uds_copy

    # Nodes
    for id_ud, ud in ud_vivas.items():
        node_attrs = {
            'ID': id_ud,
            'age': ud.age,
            'filhos': len(ud.parentes[2]) if ud.parentes[2] is not None else 0,
            attribute: getattr(ud, attribute, None)
        }
        G.add_node(id_ud, **node_attrs)

    # Links. Here are only the marriages
    for id_ud, ud in ud_vivas.items():
        if ud.parentes[9] is not None:
            if isinstance(ud.parentes[9], list):
                for parent in ud.parentes[9]:
                    if parent in ud_vivas:
                        G.add_edge(id_ud, parent)
            else:
                if ud.parentes[9] in ud_vivas:
                    G.add_edge(id_ud, ud.parentes[9])

    # Attributes
    attribute_values = set(getattr(ud, attribute) for ud in ud_vivas.values())
    
    # Position according to the attribute
    pos = {}
    offset = 5  # Separation
    for i, value in enumerate(attribute_values):
        nodes_in_value = [id_ud for id_ud, ud in ud_vivas.items() if getattr(ud, attribute) == value]
        for node in nodes_in_value:
            pos[node] = (random.random() + i * offset, ud_vivas[node].age)

    # Graph
    plt.figure(figsize=(17, 10))
    nx.draw_networkx_nodes(G, pos, node_size=25, node_color='black')
    nx.draw_networkx_edges(G, pos, edge_color='blue')
    nx.draw_networkx_labels(G, pos, labels={node: str(ud_vivas[node].id) for node in G.nodes}, font_size=12)
    plt.title(f"Marriage Graph by {attribute}")
    plt.xlabel('')
    plt.ylabel('Age')
    plt.show()

    if measures:
        # histograms
        degree_values = [degree for _, degree in G.degree()]

        plt.figure(figsize=(12, 6))
        plt.hist(degree_values, bins=20, color='blue', alpha=0.7)
        plt.title(f"Marriage graph's Degree distribution")
        plt.xlabel('Degree')
        plt.ylabel('Frequency')
        plt.show()

    return G
        
def egocentric_indiv(UD):
    for id_ud, ud in UD.uds.items():
        red_ud = nx.Graph()
        red_ud.add_node(id_ud)

        # UD's parents
        parentes = ud.parentes[0:8]

        # Nodes from its parents list
        for nodo in parentes:
            if nodo is not None:
                if isinstance(nodo, list):
                    red_ud.add_nodes_from(nodo)
                else:
                    red_ud.add_node(nodo)

        # Connect
        for nodo1 in red_ud.nodes:
            if nodo1 is not id_ud:
                red_ud.add_edge(id_ud, nodo1)


        # Graph
        plt.figure(figsize=(3, 3))
        pos = nx.spring_layout(red_ud, k=0.5)
        nx.draw(red_ud, pos, with_labels=True, node_size=200, node_color='lightblue', font_size=8, font_color='black')
        plt.title(f"Ego nework from the UD #{id_ud}")
        plt.show()
    
def small_ego_genealogy(ego_ud):
    G = nx.DiGraph() 

    # Ego node
    ego_id = ego_ud.id
    G.add_node(ego_id, label=f"ID: {ego_id}\nNivel: 0")

    # Parents relations
    father_id = ego_ud.parentes[0]
    mother_id = ego_ud.parentes[1]

    # Levels
    if father_id is not None:
        paternal_grandfather_id = ego_ud.uds[father_id].parentes[0]
        paternal_grandmother_id = ego_ud.uds[father_id].parentes[1]
        G.add_node(father_id, label=f"ID: {father_id}\nNivel: 1")
        G.add_edge(father_id, ego_id, tipo_de_relacion='padre')

        # Paternal grandparents nodes
        if paternal_grandfather_id is not None:
            G.add_node(paternal_grandfather_id, label=f"ID: {paternal_grandfather_id}\nNivel: 2")
            G.add_edge(paternal_grandfather_id, father_id)
        if paternal_grandmother_id is not None:
            G.add_node(paternal_grandmother_id, label=f"ID: {paternal_grandmother_id}\nNivel: 2")
            G.add_edge(paternal_grandmother_id, father_id, tipo_de_relacion='madre')

        # Connect ego's siblings to its father's family
        father_children = ego_ud.uds[father_id].parentes[2]
        if father_children is not None:
            for children_id in father_children:
                if children_id is not None:
                    relationship_type = 'padre' if father_id == ego_ud.uds[children_id].parentes[0] else 'madre'
                    G.add_node(children_id, label=f"ID: {children_id}\nNivel: 0")
                    G.add_edge(father_id, children_id, tipo_de_relacion=relationship_type)

    if mother_id is not None:
        maternal_grandfather_id = ego_ud.uds[mother_id].parentes[0]
        maternal_grandmother_id = ego_ud.uds[mother_id].parentes[1]
        maternal_level = 1
        G.add_node(mother_id, label=f"ID: {mother_id}\nNivel: {maternal_level}")
        G.add_edge(mother_id, ego_id, tipo_de_relacion='madre')

        # Maternal grandparents nodes
        if maternal_grandfather_id is not None:
            G.add_node(maternal_grandfather_id, label=f"ID: {maternal_grandfather_id}\nNivel: 2")
            G.add_edge(maternal_grandfather_id, mother_id)
        if maternal_grandmother_id is not None:
            G.add_node(maternal_grandmother_id, label=f"ID: {maternal_grandmother_id}\nNivel: 2")
            G.add_edge(maternal_grandmother_id, mother_id, tipo_de_relacion='madre')

        # Connect ego's siblings to its mother's family
        mother_children = ego_ud.uds[mother_id].parentes[2]
        if mother_children is not None:
            for children_id in mother_children:
                if children_id is not None:
                    relationship_type = 'padre' if mother_id == ego_ud.uds[children_id].parentes[0] else 'madre'
                    G.add_node(children_id, label=f"ID: {children_id}\nNivel: 0")
                    G.add_edge(mother_id, children_id, tipo_de_relacion=relationship_type)


    # Ego's children
    ego_children_ids = ego_ud.parentes[2]

    # Levels 
    if ego_children_ids is not None:
        for child_id in ego_children_ids:
            if child_id is not None:
                relationship_type = 'padre' if ego_id == ego_ud.uds[child_id].parentes[0] else 'madre'
                G.add_node(child_id, label=f"ID: {child_id}\nNivel: -1")
                G.add_edge(ego_id, child_id, tipo_de_relacion=relationship_type)

    # P-Graph
    pos = nx.kamada_kawai_layout(G)

    # Adjust
    for node in G.nodes:
        if G.nodes[node]['label'].endswith('-1'):  # Nodos de nivel -1 (hijos)
            pos[node][1] = -1
        elif G.nodes[node]['label'].endswith('1'):
            pos[node][1] = 1
        elif G.nodes[node]['label'].endswith('2'):
            pos[node][1] = 2
        else:
            pos[node][1] = 0

    # Space
    layer_spacing = 0.2  
    for level in set([data['label'][-1] for data in G.nodes.values()]):
        nodes_at_level = [node for node, data in G.nodes(data=True) if data['label'].endswith(level)]
        for i, node in enumerate(nodes_at_level):
            pos[node][0] = (i) * layer_spacing
    
    # Colors
    edge_colors = []
    for u, v, data in G.edges(data=True):
        if 'tipo_de_relacion' in data:
            if data['tipo_de_relacion'] == 'madre':
                edge_colors.append('red')  # matrilineal colors
            else:
                edge_colors.append('blue') 
        else:
            edge_colors.append('blue')

    # P-graph
    node_labels = {node: G.nodes[node]['label'] for node in G.nodes}
    plt.figure(figsize=(10, 6))
    nx.draw(G, pos, with_labels=True, labels=node_labels, node_size=3000, node_color='lightblue', font_size=8, font_color='black', edge_color=edge_colors, arrowsize=30, arrowstyle='<-')
    plt.title(f"UD {ego_id}'s Kinship network")
    plt.show()
    
    
def count_links_between_and_within(G, attribute):
    #This function counts the percentage of links inside and between certain attribute.
    
    total_edges = G.number_of_edges()
    internal_edges = defaultdict(int)
    external_edges = defaultdict(int)
    
    for u, v in G.edges:
        u_attr = G.nodes[u][attribute]
        v_attr = G.nodes[v][attribute]
        
        if u_attr == v_attr:
            internal_edges[u_attr] += 1
        else:
            external_edges[(u_attr, v_attr)] += 1
    
    # Percentages
    percent_internal = {k: (v / total_edges) * 100 for k, v in internal_edges.items()}
    percent_external = {k: (v / total_edges) * 100 for k, v in external_edges.items()}
    
    print(f"Total de enlaces: {total_edges}")
    for k, v in percent_internal.items():
        print(f"Links inside the {attribute} '{k}': {v:.2f}%")
    for k, v in percent_external.items():
        print(f"Linkgs outside the {attribute} '{k[0]}' and '{k[1]}': {v:.2f}%")
    
    return {
        'percent_internal': percent_internal,
        'percent_external': percent_external
    }

    
    
##### Methods when there is no clan
#I still have to change it to get the unique and so on. I can use this to the clan part too.
#Documents format
    #List [step, id, age, parentes, community, varieties, variedades únicas]
# def general_charactersitics_data(G, step, uds, dataset, data_conections, final = False):
#     if final == False:
#         for ud in uds.values():
#             dataset.append([step, ud.id, ud.age, ud.parentes, ud.community, ud.varieties])# "unique"]
#         #Network information
#         edges = list(G.edges())
#         df_edges = pd.DataFrame(edges, columns=['source', 'target'])
#         df_edges.insert(0, 'step', step)
#         df_final_edges = pd.concat([data_conections, df_edges], ignore_index=True)
#         return dataset, df_final_edges
            

#     else: #sabe the final documents.
#         df = pd.DataFrame(dataset)
#         df.columns = ["Step", "ID", "Age", "Parents", "Community", "Varieties"]# "Unique"]
#         return df, data_conections

    
