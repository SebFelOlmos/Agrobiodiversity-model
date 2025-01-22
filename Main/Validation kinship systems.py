import numpy as np
import random
import time
import random
import os
import json
import sys
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns

random.seed(42)
np.random.seed(42)

# Path
current_directory = os.path.dirname(os.path.abspath(__file__))
root_directory = os.path.abspath(os.path.join(current_directory, '..'))
sys.path.append(root_directory)
#Network and measures
from to_get_data.net_construction_vis_measures import * 
#Class
from model_class.Variety import Variety
from model_class.UD_clan import *

choice = ''
while choice not in ['1', '2']:
    choice = input('''
    Hi, you want to execute the simulations for the validation results
    What do you want? 
    
    1 - Kinship validation
    2 - Populational behavior
    
    Please enter 1 or 2: 
    ''')

if choice == '1': #Kinship validation
    print('''
    You choose the kinship validation
    ''')
    print('''
    The simulations will be executed for the validation of the kinship systems
    This may take some time. There are two experiments of 100 simulations
    each with 1000 steps.
    ''')
    def detect_cycles(G, attribute='clan'):
        """
        Detects cycles in a graph where clans interact through marriage and offspring relationships.
        
        Parameters:
        - G: A networkx DiGraph with nodes containing 'clan', 'mother', and 'children' attributes.
        - attribute: The attribute representing the clan (default: 'clan').
        
        Returns:
        - A dictionary with counts of cycles of length 1 and 2.
        """
        cycle_counts = {"cycle_1": 0, "cycle_2": 0}
        # Iterate over all nodes in the graph
        for node_id, node_data in G.nodes(data=True):
            original_clan = node_data.get(attribute)
            mother_id = node_data.get('mother')
            # If the node has no mother, skip this node
            if not mother_id:
                continue
            # Get the mother's clan
            mother_clan = G.nodes[mother_id].get(attribute) if mother_id in G.nodes else None
            # Check if the mother's clan is the same as the node's clan
            if mother_clan == original_clan:
                # Cycle of 1 (incest)
                cycle_counts["cycle_1"] += 1
                continue
            saved_mother_clan = mother_clan
            children_ids = node_data.get('children', [])
            for child_id in children_ids:
                if child_id not in G.nodes:
                    continue
                child_data = G.nodes[child_id]
                child_clan = child_data.get(attribute)
                child_mother_id = child_data.get('mother')
                # If the original node is the mother of this child
                if child_mother_id == node_id:
                    # Check if the child's clan matches the saved mother's clan
                    if child_clan == saved_mother_clan:
                        # Cycle of 2
                        cycle_counts["cycle_2"] += 1

        return cycle_counts

    def detect_cycles_three_generations(G, attribute='clan'):
        """
        Same but detect cycles of length 2 and 3 in the graph, considering three clans.
        """
        cycle_counts = {"cycle_1": 0, "cycle_2": 0, "cycle_3": 0}

        for node_id, node_data in G.nodes(data=True):
            original_clan = node_data.get(attribute)
            mother_id = node_data.get('mother')

            if not mother_id or mother_id not in G.nodes:
                continue

            mother_clan = G.nodes[mother_id].get(attribute)

            # Cycle of 1 (incest, original node's clan matches its mother's clan)
            if mother_clan == original_clan:
                cycle_counts["cycle_1"] += 1
                continue

            # Cycle of 2: Check daughters
            children_ids = node_data.get('children', [])
            for child_id in children_ids:
                if child_id not in G.nodes:
                    continue

                child_data = G.nodes[child_id]
                child_clan = child_data.get(attribute)
                child_mother_id = child_data.get('mother')

                # If the current node is the mother of this child
                if child_mother_id == node_id:
                    if child_clan == mother_clan and child_clan != original_clan:
                        cycle_counts["cycle_2"] += 1

                    # Cycle of 3: Check granddaughters
                    grandchild_ids = child_data.get('children', [])
                    for grandchild_id in grandchild_ids:
                        if grandchild_id not in G.nodes:
                            continue

                        grandchild_data = G.nodes[grandchild_id]
                        grandchild_clan = grandchild_data.get(attribute)
                        grandchild_mother_id = grandchild_data.get('mother')

                        if grandchild_mother_id == child_id:
                            if grandchild_clan == mother_clan and grandchild_clan != child_clan and grandchild_clan != original_clan:
                                cycle_counts["cycle_3"] += 1

        return cycle_counts

    # # Dual organization
    #Parameters dual_organization
    iniciais = 40 # Initial UD
    prob_morte = 0.06 # Beta from the gutertz equation
    mediao = 4 # Average children per UD
    t = 1000 #steps of the simulation
    original_media = mediao
    media = original_media
    cycles = [[],[]]
    final_pop = []
    contador = 0
    while contador < 100:
        #### Initialization dual_organization
        ## Clans
        clanes = [1,2]
        clans = (clanes * (iniciais // 2)) + clanes[:(iniciais % 2)]
        random.shuffle(clans)
        UD_dual_organization.uds = {}
        instancias_ud = []
        for id_ud in range(1, int(iniciais) + 1):
                instancias_ud.append(UD_dual_organization(id_ud, media, clans.pop()))
        ## Varieties
        limited_varieties = True
        if limited_varieties == False:
            for id_ud, ud in UD_dual_organization.uds.items():
                for _ in range(3):
                    ud.varieties.append(Variety())
        else:
            initial_varieties = [Variety() for _ in range (10)]
            for ud in UD_dual_organization.uds.values():
                for _ in range(3):
                    ud.varieties.append(random.choice(initial_varieties))
        #### Simulation dual_organization
        vivas = [int(iniciais)]
        for i in range (1, (t+1)):
            uds_copy = {id_ud: ud for id_ud, ud in UD_dual_organization.uds.items() if ud.activa}
            items = list(uds_copy.items())
            random.shuffle(items)
            uds_copy = dict(items)
            alive = len(uds_copy)
            if alive > 200 and (media == original_media):
                media -= media//2
                if media >= 4:
                    media = media //2
            elif alive < 150 and media < original_media:
                media = original_media
            if not uds_copy:
                break
            for id_ud, ud in uds_copy.items():
                ud.ter_filho()
                ud.buscar_ud(uds_copy, media, 50, True, 0.2)
                ud.incrementar_idade()
                ud.death_probability(prob_morte)
        if uds_copy:
            contador += 1
            final_pop.append(len(uds_copy))
            full = p_graph_attribute(UD_dual_organization.uds, "clan", False)
            cs = detect_cycles(full, 'clan')
            cycles2 = cs['cycle_2'] * 100 / (cs['cycle_1'] + cs['cycle_2'])
            cycles[1].append(cycles2)
            cycles[0].append(100 - cycles2)
    # Structure data into a dictionary
    simulation_data = {
        "experiments": contador,
        "final_pop": final_pop,
        "cycles": cycles
    }
    # Define paths
    parent_folder = 'Outputs'
    folder_name = os.path.join(parent_folder, 'results_validation', 'kinship_validation')

    # Ensure the parent folder exists
    if not os.path.exists(parent_folder):
        os.makedirs(parent_folder)

    # Create the results_validation sub-folder if it doesn't exist
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    # Save to a JSON file
    output_file = os.path.join(folder_name, "validation_dual_organizations.json")
    with open(output_file, "w") as file:
        json.dump(simulation_data, file, indent=4)

    print(f"Simulation results saved to {output_file}")

    # Load the data
    name = os.path.join(folder_name, "validation_dual_organizations.json")
    with open(name, 'r') as json_file:
        loaded_val_dual = json.load(json_file)


    # # Generalized

    #Generalized CONTROL POPULATION
    #Parameters UD_generalized
    iniciais = 40 # Initial UD

    prob_morte = 0.06 # Beta from the gutertz equation
    mediao = 4 # Average children per UD
    random.seed(42) # Random seed
    t = 1000 #steps of the simulation
    dataset = [] #For the data
    original_media = mediao
    media = original_media
    cycles=[[],[],[]]
    final_pop = []
    contador = 0
    while contador < 100:
        clanes = [1,2,3]
        clans = (clanes * (iniciais // 3)) + clanes[:(iniciais % 3)]# Just 3 clans
        random.shuffle(clans)
        #### Initialization dual_organization
        ## Clans
        UD_generalized.uds = {}
        instancias_ud = []
        for id_ud in range(1, int(iniciais) + 1):
                instancias_ud.append(UD_generalized(id_ud, media, clans.pop()))
        ## Varieties
        limited_varieties = True
        if limited_varieties == False:
            for id_ud, ud in UD_generalized.uds.items():
                for _ in range(3):
                    ud.varieties.append(Variety())
        else:
            initial_varieties = [Variety() for _ in range (10)]
            for ud in UD_generalized.uds.values():
                for _ in range(3):
                    ud.varieties.append(random.choice(initial_varieties))
        #### Simulation dual_organization
        vivas = [int(iniciais)]
        for i in range (1, (t+1)):
            uds_copy = {id_ud: ud for id_ud, ud in UD_generalized.uds.items() if ud.activa}
            items = list(uds_copy.items())
            random.shuffle(items)
            uds_copy = dict(items)
            alive = len(uds_copy)
            if alive > 200 and (media == original_media): 
                media -= media//2
                if media >= 4:
                    media = media //2
            elif alive < 150 and media < original_media:
                media = original_media
            if not uds_copy:
                break
            for id_ud, ud in uds_copy.items():
                ud.ter_filho()
                ud.buscar_ud(uds_copy, media, 50, True, 0.2)
                ud.incrementar_idade()
                ud.death_probability(prob_morte)
        if uds_copy and any(UD.clan == 3 for id, UD in uds_copy.items()):
            contador += 1
            final_pop.append(len(uds_copy))
            full = p_graph_attribute(UD_generalized.uds, "clan", False)
            cs = detect_cycles_three_generations(full, 'clan')
            total = (cs['cycle_1'] + cs['cycle_2']+ cs['cycle_3'])
            cycle3 = (cs['cycle_3'] * 100) / total
            cycle2 = (cs['cycle_2'] * 100) / total
            cycles[2].append(cycle3)
            cycles[1].append(cycle2)
            cycles[0].append(100 - (cycle2+cycle3))
    # Structure data into a dictionary
    simulation_data = {
        "experiments": contador,
        "final_pop": final_pop,
        "cycles": cycles
    }

    output_file = os.path.join(folder_name, "validation_generalized_exchange.json")
    with open(output_file, "w") as file:
        json.dump(simulation_data, file, indent=4)

    print(f"Simulation results saved to {output_file}")

    name = os.path.join(folder_name, "validation_generalized_exchange.json")
    with open(name, 'r') as json_file:
            loaded_val_gen = json.load(json_file)

    mean1g = np.mean(loaded_val_gen['cycles'][0])
    std1g = np.std(loaded_val_gen['cycles'][0])
    mean2g = np.mean(loaded_val_gen['cycles'][1])
    std2g = np.std(loaded_val_gen['cycles'][1])
    mean3g = np.mean(loaded_val_gen['cycles'][2])
    std2g = np.std(loaded_val_gen['cycles'][2])
    meanpopg = np.mean(loaded_val_gen['final_pop'])
    mean1 = np.mean(loaded_val_dual['cycles'][0])
    std1 = np.std(loaded_val_dual['cycles'][0])
    mean2 = np.mean(loaded_val_dual['cycles'][1])
    std2 = np.std(loaded_val_dual['cycles'][1])
    meanpop = np.mean(loaded_val_dual['final_pop'])
    print(f'''
    Dual Organization
    mean 1: {mean1} 
    std 1: {std1}
    mean 2: {mean2}
    std 2: {std2}
    ''')
    print(f'''
    Generalized exchange
    mean 1 cycle = {mean1g}
    std 1 cycle = {std1g}
    mean 2 cycle = {mean2g}
    std 2 cycle = {std1g}
    mean 3 cycle = {mean3g}
    std 3 cycle = {std1g}
    ''')

    dual = {
        '1 cycle': mean1, 
        '1 cycle std': std1, 
        '2 cycle': mean2, 
        '2 cycle std': std2, 
        'mean population': meanpop
    }

    gen = {
        '1 cycle': mean1g, 
        '1 cycle std': std1g, 
        '2 cycle': mean2g, 
        '2 cycle std': std2g, 
        '3 cycle': mean3g, 
        '3 cycle std': std2g, 
        'mean population': meanpopg
    }

    # Create the DataFrame
    df = pd.DataFrame({'Dual Organization': dual, 'Generalized': gen}).T

    systems = ['Dual Organization', 'Generalized'] 
    cycles = ['1 cycle', '2 cycle', '3 cycle'] # Cycle types for legend
    means = df.loc[:, ['1 cycle', '2 cycle', '3 cycle']].fillna(0).to_numpy()  
    errors = df.loc[:, ['1 cycle std', '2 cycle std', '3 cycle std']].fillna(0).to_numpy() 

    x = np.arange(len(systems))  
    width = 0.2  

    #Plot
    fig, ax = plt.subplots(figsize=(8, 6))
    for i, cycle in enumerate(cycles):
        ax.bar(x + i * width - width, means[:, i], width, yerr=errors[:, i], 
            label=cycle, capsize=4, color=sns.color_palette("tab10")[i])

    ax.set_title('Percentage of Cycles in Dual Organization and Generalized Exchange')
    ax.set_xlabel('Kinship System')
    ax.set_ylabel('Percentage of Cycles')
    ax.set_xticks(x)
    ax.set_xticklabels(systems) 
    ax.legend(title='Length of the Cycle')  
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()

    # Define the output path for the plot
    plot_file = os.path.join(folder_name, "validation_dual_organizations_plot.png")

    # Save the plot to the specified file
    fig.savefig(plot_file, dpi=300, bbox_inches="tight")
    print('It was saved to: %s' % plot_file)
    print('but, you know what? I am going to print it anyway!')

    plt.show()

else: #Populational behavior
    # Method for heatmaps...!
    def plot_heatmap(data, alphas, betas, alpha, beta, variable, colorbar_range=(0, 3000), figsize=(7, 5)):
        """
        Plot a heatmap with specific configuration for colorbar and labels.

        Parameters:
            data (list of list of dict): Data containing 'alive' values.
            alphas (list): Labels for the y-axis.
            betas (list): Labels for the x-axis.
            colorbar_range (tuple): Min and max values for the colorbar.
            figsize (tuple): Figure size for the plot.
        """
        # Extract 'alive' values
        alive_values = np.array([[entry[variable] for entry in row] for row in data])
        
        # Set up plot
        fig, ax = plt.subplots(1, 1, figsize=figsize, facecolor="white")
        im = ax.imshow(alive_values, vmin=colorbar_range[0], vmax=colorbar_range[1])
        
        # Colorbar
        cbar = fig.colorbar(im, ax=ax, label='UDs')
        #cbar.set_clim(*colorbar_range)
        
        # Set ticks and labels
        ax.set_xticks(np.arange(len(betas)))
        ax.set_yticks(np.arange(len(alphas)))
        ax.set_xticklabels([f'{round(beta, 3)}' for beta in betas])
        ax.set_yticklabels([f'{alpha:.1f}' for alpha in alphas])
        
        # Display values in the heatmap cells
        for i in range(len(alphas)):
            for j in range(len(betas)):
                ax.text(j, i, f'{alive_values[i, j]:.1f}', ha="center", va="center", color="w", fontsize=8)
        
        # Label axes
        plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")
        ax.set_ylabel(alpha)
        ax.set_xlabel(beta)
        
        #plt.show()
        return plt
    
    print('''
    You choose the populational behavior
    ''')
    print('''
    The simulation will be executed for the populational behavior
    
    As you know, There are 3 kinship systems (Endogamy, Dual Organization and Generalized Exchange)
    ''')
    kin_choice = input('''
    What is the kinship system you want to choose?
    1 - Endogamy
    2 - Dual Organization
    3 - Generalized Exchange
    ''')
    
    variable_choice = input('''
    Nice. Now, what is the variable you want to let fixed?
    1 - Beta 
    2 - Initial UDs
    3 - Average number of children for UD
    ''')
    #Folders!
    parent_folder = 'Outputs'
    folder_name = os.path.join(parent_folder, 'results_validation', 'populational behavior')
    # Ensure the parent folder exists
    if not os.path.exists(parent_folder):
        os.makedirs(parent_folder)
    # Create the results_validation sub-folder if it doesn't exist
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    
    if kin_choice == '1': #Endogamy
        #sub folder
        folder_name = os.path.join(parent_folder, 'results_validation', 'populational behavior', 'Endogamy')
        # Create the results_validation sub-folder if it doesn't exist
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
        if variable_choice == '1': # Beta
            #This experiment has the beta fixed in 0.06
            prob_morte = 0.06
            n = 4
            m = 40
            malphas = np.linspace(1,n,n) # Average number of children: from 1 to n
            mbetas = np.linspace(10,m,int(m/10)) # Initial UDs: from 10 to m
            mM = np.empty((len(malphas), len(mbetas)), dtype=object)
            punto_vista = 2
            tiempo = 700
            tempo = list(range(0,tiempo,punto_vista))
            experiments = 110

            # For data of behaviour
            datos_1 = np.empty((len(malphas), len(mbetas)), dtype=object)
            print(mM.shape)
            start = time.time()
            print(f"started at:  {datetime.now()}")
            for i, media in enumerate(malphas):
                for j, iniciais  in enumerate(mbetas):
                    list_alive_UDs = []
                    list_vivas_puntos_vista = []
                    tasas_crecimiento = []
                    star_configuration = time.time()
                    for experiment in range(1, experiments+1):
                        #### Initialization
                        UD_endogamy.uds = {}
                        instancias_ud = []
                        for id_ud in range(1, int(iniciais) + 1):
                            instancias_ud.append(UD_endogamy(id_ud, media))
                        ## Varieties
                        limited_varieties = True
                        if limited_varieties == False:
                            for id_ud, ud in UD_endogamy.uds.items():
                                for _ in range(3):
                                    ud.varieties.append(Variety())
                        else:
                            initial_varieties = [Variety() for _ in range (10)]
                            for ud in UD_endogamy.uds.values():
                                for _ in range(3):
                                    ud.varieties.append(random.choice(initial_varieties))   
                        # Lists for graphs
                        vivas_puntos_vista = [int(iniciais)]
                        vivas_tasa_crecimiento = [int(iniciais)]
                        mortas_puntos_vista = [0]
                        # Simulation
                        for t in range(1, tiempo):
                            uds_copy = {id_ud: ud for id_ud, ud in UD_endogamy.uds.items() if ud.activa}
                            items = list(uds_copy.items())
                            random.shuffle(items)
                            uds_copy = dict(items)
                            if not uds_copy:
                                # Only 0
                                print(f"acabó en 0 el experimento {experiment} de la media {malphas[i]} con unidades {mbetas[j]}")
                                vivas_puntos_vista.extend([0] * (int((tiempo/punto_vista)-(len(vivas_puntos_vista)))))
                                vivas_tasa_crecimiento.extend([0] * (int((tiempo)-(len(vivas_tasa_crecimiento)))))
                                #mortas_puntos_vista.extend([unidades_iniciais] * (tiempo - t))
                                break            
                            for id_ud, ud in uds_copy.items():
                                ud.ter_filho()
                                ud.buscar_ud(uds_copy, int(media), 0)
                                ud.incrementar_idade()
                                ud.death_probability(prob_morte)
                            # Collecting data
                            vivas_tasa_crecimiento.append(len([ud for id, ud in uds_copy.items() if ud.activa]))
                            if t % punto_vista == 0:
                                viv = len([ud for id, ud in uds_copy.items() if ud.activa])
                                #mort = len([ud for id, ud in uds_copy.items() if not ud.activa])
                                vivas_puntos_vista.append(viv)
                        indice_primer_cero = np.where(np.array(vivas_tasa_crecimiento) == 0)[0]
                        if len(indice_primer_cero) > 0:
                            # Get growth rate before the 0
                            tasas_crecimiento.append(np.diff(vivas_tasa_crecimiento[:indice_primer_cero[0] - 1]) / vivas_tasa_crecimiento[:-1][:indice_primer_cero[0] - 2] * 100)
                        else:
                            # Growth rate
                            tasas_crecimiento.append(np.diff(vivas_tasa_crecimiento) / vivas_tasa_crecimiento[:-1] * 100)
                        # Collect the data
                        list_alive_UDs.append(len([ud for id, ud in uds_copy.items() if ud.activa == True])) #For heatmap
                        list_vivas_puntos_vista.append(vivas_puntos_vista)
                        print(f"acabó en el experimento {experiment} de la media {malphas[i]} con unidades {mbetas[j]}")
                        #print(f"""
                        #    Acabó la simulacion con media de {int(media)} y {int(iniciais)} unidades iniciales. Prob de morte: {prob_morte}
                        #    poblacion total al final de la simulación: {len([ud for id, ud in uds_copy.items() if ud.activa == True])}""")
                    end_config = time.time()
                    mM[i][j] = {'alive': np.mean(list_alive_UDs),
                                'std': np.std(list_alive_UDs),
                                'time used': end_config - star_configuration}
                    datos_1[i][j] = {'tempo': tempo, 
                                    'mean': np.mean(list_vivas_puntos_vista, axis=0), 
                                    'std':  np.std(list_vivas_puntos_vista, axis=0),
                                    'growth rate': np.mean([np.mean(lista) for lista in tasas_crecimiento])}
                    print(f"""
            The total time of the configuration of mean {media} and initial UDs {iniciais} is  {end_config - star_configuration}
                    """)
            # Save the data
            heat_std = os.path.join(folder_name, 'Endo_beta_fixed.npy')
            np.save(heat_std, mM)
            # Behavior of experiments
            behavior = os.path.join(folder_name, 'Endo_beta_fixed_data.npy')
            np.save(behavior, datos_1)
            now = datetime.now()
            finish = time.time()
            print(f"""
            It finished at: {now}
            It lasted {finish-start}
            """)
            print("done")
            # Dowload the documents
            #Folders
            heat_std = os.path.join(folder_name, 'Endo_beta_fixed.npy')
            behavior = os.path.join(folder_name, 'Endo_beta_fixed_data.npy')
            ## heatmap and mean
            mM_datos = np.load(heat_std, allow_pickle=True)
            ## behavior for experiments
            mM_behavior = np.load(behavior, allow_pickle=True)
            plot = plot_heatmap(mM_datos, malphas, mbetas, 'Mean Children', 'Initial UDs', 'alive', (0, 3000))
            plot.savefig(os.path.join(folder_name, 'Endo_beta_fixed_mean.png'), dpi=300, bbox_inches="tight")
            print(f"Heatmap of the mean pop saved to: {os.path.join(folder_name, 'Endo_beta_fixed_mean.png')}")
            plot = plot_heatmap(mM_datos, malphas, mbetas, 'Mean Children', 'Initial UDs', 'std', (0, 3000))
            plot.savefig(os.path.join(folder_name, 'Endo_beta_fixed_std.png'), dpi=300, bbox_inches="tight")
            print(f"Heatmap of the mean std saved to: {os.path.join(folder_name, 'Endo_beta_fixed_std.png')}")
        elif variable_choice == '2': # Initial UDs
            #This experiment has Uds inicias in 40
            iniciais = 40
            n = 4
            ualphas = np.linspace(1,n,n) # Average number of children: from 1 to n
            ubetas = np.linspace(0.055, 0.075, 5) # Beta from 0.055 to 0.075
            uM = np.empty((len(ualphas), len(ubetas)), dtype=object)
            punto_vista = 2
            tiempo = 700
            tempo = list(range(0,tiempo,punto_vista))
            experiments = 110

            start = time.time()
            # For data of behaviour
            datos_2 = np.empty((len(ualphas), len(ubetas)), dtype=object)
            print(uM.shape)

            for i, media in enumerate(ualphas):
                for j, prob_morte  in enumerate(ubetas):
                    list_alive_UDs = []
                    list_vivas_puntos_vista = []
                    tasas_crecimiento = []
                    star_configuration = time.time()
                    #original_media = media
                    for experiment in range(1, experiments+1):
                        #### Initialization
                        ## Comunidades
                        UD_endogamy.uds = {}
                        instancias_ud = []
                        for id_ud in range(1, int(iniciais) + 1):
                            instancias_ud.append(UD_endogamy(id_ud, media))
                        ## Varieties
                        limited_varieties = True
                        if limited_varieties == False:
                            for id_ud, ud in UD_endogamy.uds.items():
                                for _ in range(3):
                                    ud.varieties.append(Variety())
                        else:
                            initial_varieties = [Variety() for _ in range (10)]
                            for ud in UD_endogamy.uds.values():
                                for _ in range(3):
                                    ud.varieties.append(random.choice(initial_varieties))   
                        # Lists for graphs
                        vivas_puntos_vista = [int(iniciais)]
                        vivas_tasa_crecimiento = [int(iniciais)]
                        mortas_puntos_vista = [0]
                        # Simulation
                        for t in range(1, tiempo):
                            uds_copy = {id_ud: ud for id_ud, ud in UD_endogamy.uds.items() if ud.activa}
                            items = list(uds_copy.items())
                            random.shuffle(items)
                            uds_copy = dict(items)
                            if not uds_copy:
                                # Only 0
                                print(f"acabó en el experimento {experiment} de la media {ualphas[i]} con prob de morte {ubetas[j]}")
                                vivas_puntos_vista.extend([0] * (int((tiempo/punto_vista)-(len(vivas_puntos_vista)))))
                                vivas_tasa_crecimiento.extend([0] * (int((tiempo)-(len(vivas_tasa_crecimiento)))))
                                #mortas_puntos_vista.extend([unidades_iniciais] * (tiempo - t))
                                break            
                            for id_ud, ud in uds_copy.items():
                                if ud.activa == True:
                                    any_ud_active = True
                                    ud.ter_filho()
                                    ud.buscar_ud(uds_copy, int(media),0)
                                    ud.incrementar_idade()
                                    ud.death_probability(prob_morte)
                            # Collecting data
                            vivas_tasa_crecimiento.append(len([ud for id, ud in uds_copy.items() if ud.activa]))
                            if t % punto_vista == 0:
                                viv = len([ud for id, ud in uds_copy.items() if ud.activa])
                                #mort = len([ud for id, ud in uds_copy.items() if not ud.activa])
                                vivas_puntos_vista.append(viv)
            #                     mortas_puntos_vista.append(mort)
            #                 if t%100 == 0:
            #                     print(f"tamos en tiempo {t} con vivas {viv}")
                        # Average Annual Population Growth
                        # First 0 avoid errors 
                        indice_primer_cero = np.where(np.array(vivas_tasa_crecimiento) == 0)[0]
                        if len(indice_primer_cero) > 0:
                            # Get growth rate before the 0
                            tasas_crecimiento.append(np.diff(vivas_tasa_crecimiento[:indice_primer_cero[0] - 1]) / vivas_tasa_crecimiento[:-1][:indice_primer_cero[0] - 2] * 100)
                        else:
                            # Growth rate
                            tasas_crecimiento.append(np.diff(vivas_tasa_crecimiento) / vivas_tasa_crecimiento[:-1] * 100)
                        print(f"acabó en el experimento {experiment} de la media {ualphas[i]} con prob de morte {ubetas[j]}")
                        # Collect the data
                        list_alive_UDs.append(len([ud for id, ud in uds_copy.items() if ud.activa == True])) #For heatmap
                        list_vivas_puntos_vista.append(vivas_puntos_vista)
                        #print(f"""
                        #    Acabó la simulacion con media de {int(media)} y {int(iniciais)} unidades iniciales. Prob de morte: {prob_morte}
                        #    poblacion total al final de la simulación: {len([ud for id, ud in uds_copy.items() if ud.activa == True])}""")
                    #media = original_media
                    end_config = time.time()
                    uM[i][j] = {'alive': np.mean(list_alive_UDs),
                                'std': np.std(list_alive_UDs),
                                'time used': end_config - star_configuration}
                    datos_2[i][j] = {'tempo': tempo, 
                                    'mean': np.mean(list_vivas_puntos_vista, axis=0), 
                                    'std':  np.std(list_vivas_puntos_vista, axis=0),
                                    'growth rate': np.mean([np.mean(lista) for lista in tasas_crecimiento])}
                    print(f"""
            The total time of the configuration of mean {media} and beta {prob_morte:.3f} is  {end_config - star_configuration}
                    """)
            # Save 
            # Heatmap and std
            heat_std = os.path.join(folder_name, 'Endo_UDin_fixed.npy')
            np.save(heat_std, uM)
            # Behavior of experiments
            behavior = os.path.join(folder_name, 'Endo_Udin_fixed_data.npy')
            np.save(behavior, datos_2)
            now = datetime.now()
            finish = time.time()
            print(f"""
            It finished at: {now}
            It lasted {finish-start}
            """)
            print("done")
            #Folders
            heat_std = os.path.join(folder_name, 'Endo_UDin_fixed.npy')
            behavior = os.path.join(folder_name, 'Endo_Udin_fixed_data.npy')
            ## heatmap and mean
            uM_datos = np.load(heat_std, allow_pickle=True)
            ## behavior for experiments
            uM_behavior = np.load(behavior, allow_pickle=True)
            plot = plot_heatmap(uM_datos, ualphas, ubetas, 'Mean Children', 'Beta', 'alive', (0, 3000))
            plot.savefig(os.path.join(folder_name, 'Endo_UDin_fixed_mean.png'), dpi=300, bbox_inches="tight")
            print(f"Heatmap of the mean pop saved to: {os.path.join(folder_name, 'Endo_UDin_fixed_mean.png')}")
            plot_heatmap(uM_datos, ualphas, ubetas, 'Mean Children', 'Beta', 'std', (0, 3000))
            plot.savefig(os.path.join(folder_name, 'Endo_UDin_fixed_std.png'), dpi=300, bbox_inches="tight")
            print(f"Heatmap of the mean std saved to: {os.path.join(folder_name, 'Endo_UDin_fixed_std.png')}")
        else: # Mean of children for UD
            #This experiment has mean of children: 4
            media = 4
            n = 40
            halphas = np.linspace(10,n,int(n/10)) # Initial UDs from 10 to n
            hbetas = np.linspace(0.055, 0.075, 5) # Beta from 0.055 to 0.075
            hM = np.empty((len(halphas), len(hbetas)), dtype=object)
            punto_vista = 2
            tiempo = 700
            tempo = list(range(0,tiempo,punto_vista))
            experiments = 110

            start = time.time()
            # For data of behaviour
            datos_3 = np.empty((len(halphas), len(hbetas)), dtype=object)
            # print(uM.shape)

            for i, iniciais in enumerate(halphas):
                for j, prob_morte  in enumerate(hbetas):
                    list_alive_UDs = []
                    list_vivas_puntos_vista = []
                    tasas_crecimiento = []
                    star_configuration = time.time()
                    for experiment in range(1, experiments+1):
                        #### Initialization
                        UD_endogamy.uds = {}
                        instancias_ud = []
                        for id_ud in range(1, int(iniciais) + 1):
                            instancias_ud.append(UD_endogamy(id_ud, media))
                        ## Varieties
                        limited_varieties = True
                        if limited_varieties == False:
                            for id_ud, ud in UD_endogamy.uds.items():
                                for _ in range(3):
                                    ud.varieties.append(Variety())
                        else:
                            initial_varieties = [Variety() for _ in range (10)]
                            for ud in UD_endogamy.uds.values():
                                for _ in range(3):
                                    ud.varieties.append(random.choice(initial_varieties))   
                        # Lists for graphs
                        vivas_puntos_vista = [int(iniciais)]
                        vivas_tasa_crecimiento = [int(iniciais)]
                        mortas_puntos_vista = [0]
                        # Simulation
                        for t in range(1, tiempo):
                            uds_copy = {id_ud: ud for id_ud, ud in UD_endogamy.uds.items() if ud.activa}
                            items = list(uds_copy.items())
                            random.shuffle(items)
                            uds_copy = dict(items)
                            if not uds_copy:
                                # Only 0
                                print(f"acabó en el experimento {experiment} de iniciales {halphas[i]} con beta {hbetas[j]}")
                                vivas_puntos_vista.extend([0] * (int((tiempo/punto_vista)-(len(vivas_puntos_vista)))))
                                vivas_tasa_crecimiento.extend([0] * (int((tiempo)-(len(vivas_tasa_crecimiento)))))
                                #mortas_puntos_vista.extend([unidades_iniciais] * (tiempo - t))
                                break               
                            for id_ud, ud in uds_copy.items():
                                if ud.activa == True:
                                    any_ud_active = True
                                    ud.ter_filho()
                                    ud.buscar_ud(uds_copy, int(media),0)
                                    ud.incrementar_idade()
                                    ud.death_probability(prob_morte)
                            # Collecting data
                            vivas_tasa_crecimiento.append(len([ud for id, ud in uds_copy.items() if ud.activa]))
                            if t % punto_vista == 0:
                                viv = len([ud for id, ud in uds_copy.items() if ud.activa])
                                #mort = len([ud for id, ud in uds_copy.items() if not ud.activa])
                                vivas_puntos_vista.append(viv)
            #                     mortas_puntos_vista.append(mort)
            #                 if t%100 == 0:
            #                     print(f"tamos en tiempo {t} con vivas {viv}")
                        # Average Annual Population Growth
                        # First 0 avoid errors 
                        indice_primer_cero = np.where(np.array(vivas_tasa_crecimiento) == 0)[0]
                        if len(indice_primer_cero) > 0:
                            # Get growth rate before the 0
                            tasas_crecimiento.append(np.diff(vivas_tasa_crecimiento[:indice_primer_cero[0] - 1]) / vivas_tasa_crecimiento[:-1][:indice_primer_cero[0] - 2] * 100)
                        else:
                            # Growth rate
                            tasas_crecimiento.append(np.diff(vivas_tasa_crecimiento) / vivas_tasa_crecimiento[:-1] * 100)
                        print(f"acabó en el experimento {experiment} de iniciales {halphas[i]} con prob de morte {hbetas[j]}")
                        # Collect the data
                        list_alive_UDs.append(len([ud for id, ud in uds_copy.items() if ud.activa == True])) #For heatmap
                        list_vivas_puntos_vista.append(vivas_puntos_vista)
                        #print(f"""
                        #    Acabó la simulacion con media de {int(media)} y {int(iniciais)} unidades iniciales. Prob de morte: {prob_morte}
                        #    poblacion total al final de la simulación: {len([ud for id, ud in uds_copy.items() if ud.activa == True])}""")
                    end_config = time.time()
                    hM[i][j] = {'alive': np.mean(list_alive_UDs),
                                'std': np.std(list_alive_UDs),
                                'time used': end_config - star_configuration}
                    datos_3[i][j] = {'tempo': tempo, 
                                    'mean': np.mean(list_vivas_puntos_vista, axis=0), 
                                    'std':  np.std(list_vivas_puntos_vista, axis=0),
                                    'growth rate': np.mean([np.mean(lista) for lista in tasas_crecimiento])}
                    print(f"""
            The total time of the configuration of Initial UDs {iniciais} and beta {prob_morte:.3f} is: {end_config - star_configuration}
                    """)
            # Heatmap and std
            heat_std = os.path.join(folder_name, 'Endo_Mean_fixed.npy')
            np.save(heat_std, hM)
            # Behavior of experiments
            behavior = os.path.join(folder_name, 'Endo_Mean_fixed_data.npy')
            np.save(behavior, datos_3)
            now = datetime.now()
            finish = time.time()
            print(f"""
            It finished at: {now}
            It lasted {finish-start}
            """)
            print("done")
            #Folders load
            heat_std = os.path.join(folder_name, 'Endo_Mean_fixed.npy')
            behavior = os.path.join(folder_name, 'Endo_Mean_fixed_data.npy')
            ## heatmap and mean
            hM_datos = np.load(heat_std, allow_pickle=True)
            ## behavior for experiments
            hM_behavior = np.load(behavior, allow_pickle=True)
            plot = plot_heatmap(hM_datos, halphas, hbetas, 'Initial UDs', 'Beta', 'alive')
            plot.savefig(os.path.join(folder_name, 'Endo_Mean_fixed_mean.png'), dpi=300, bbox_inches="tight")
            print(f"Heatmap of the mean pop saved to: {os.path.join(folder_name, 'Endo_Mean_fixed_mean.png')}")
            plot = plot_heatmap(hM_datos, halphas, hbetas, 'Initial UDs', 'Beta', 'std')
            plot.savefig(os.path.join(folder_name, 'Endo_Mean_fixed_std.png'), dpi=300, bbox_inches="tight")
            print(f"Heatmap of the mean std saved to: {os.path.join(folder_name, 'Endo_Mean_fixed_std.png')}")
    elif kin_choice == '2': #Dual Organization
        #sub folder
        folder_name = os.path.join(parent_folder, 'results_validation', 'populational behavior', 'Dual Organization')
        # Create the results_validation sub-folder if it doesn't exist
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
        if variable_choice == '1': # Beta
            #This experiment has the beta fixed in 0.06
            prob_morte = 0.06
            n = 4
            m = 40
            malphas = np.linspace(1,n,n) # Average number of children: from 1 to n
            mbetas = np.linspace(10,m,int(m/10)) # Initial UDs: from 10 to m
            mM = np.empty((len(malphas), len(mbetas)), dtype=object)
            punto_vista = 2
            tiempo = 700
            tempo = list(range(0,tiempo,punto_vista))
            experiments = 130

            # For data of behaviour
            datos_1 = np.empty((len(malphas), len(mbetas)), dtype=object)
            print(mM.shape)
            start = time.time()

            for i, media in enumerate(malphas):
                for j, iniciais  in enumerate(mbetas):
                    list_alive_UDs = []
                    list_vivas_puntos_vista = []
                    tasas_crecimiento = []
                    star_configuration = time.time()
                    original_media = media
                    for experiment in range(1, experiments+1):
                        #### Initialization
                        clanes = [1,2]
                        clans = (clanes * (int(iniciais) // 2)) + clanes[:(int(iniciais) % 2)]
                        random.shuffle(clans)
                        UD_dual_organization.uds = {}
                        instancias_ud = []
                        for id_ud in range(1, int(iniciais) + 1):
                            instancias_ud.append(UD_dual_organization(id_ud, media, clans.pop()))
                        ## Varieties
                        limited_varieties = True
                        if limited_varieties == False:
                            for id_ud, ud in UD_dual_organization.uds.items():
                                for _ in range(3):
                                    ud.varieties.append(Variety())
                        else:
                            initial_varieties = [Variety() for _ in range (10)]
                            for ud in UD_dual_organization.uds.values():
                                for _ in range(3):
                                    ud.varieties.append(random.choice(initial_varieties))
                        # Lists for graphs
                        vivas_puntos_vista = [int(iniciais)]
                        vivas_tasa_crecimiento = [int(iniciais)]
                        mortas_puntos_vista = [0]
                        # Simulation
                        for t in range(1, tiempo):
                            uds_copy = {id_ud: ud for id_ud, ud in UD_dual_organization.uds.items() if ud.activa}
                            items = list(uds_copy.items())
                            random.shuffle(items)
                            uds_copy = dict(items)   
                            if not uds_copy:
                                # Only 0
                                print(f"acabó en el experimento {experiment} de la media {malphas[i]} con unidades {mbetas[j]}")
                                vivas_puntos_vista.extend([0] * (int((tiempo/punto_vista)-(len(vivas_puntos_vista)))))
                                vivas_tasa_crecimiento.extend([0] * (int((tiempo)-(len(vivas_tasa_crecimiento)))))
                                #mortas_puntos_vista.extend([unidades_iniciais] * (tiempo - t))
                                break
                            for id_ud, ud in uds_copy.items():
                                any_ud_active = True
                                ud.ter_filho()
                                ud.buscar_ud(uds_copy, int(media),0 , True, 0.2)
                                ud.incrementar_idade()
                                ud.death_probability(prob_morte)
                            # Collecting data
                            vivas_tasa_crecimiento.append(len([ud for id, ud in uds_copy.items() if ud.activa]))
                            if t % punto_vista == 0:
                                viv = len([ud for id, ud in uds_copy.items() if ud.activa])
                                #mort = len([ud for id, ud in uds_copy.items() if not ud.activa])
                                vivas_puntos_vista.append(viv)
            #                     mortas_puntos_vista.append(mort)
            #                 if t%100 == 0:
            #                     print(f"tamos en tiempo {t} con vivas {viv}")
                        # Average Annual Population Growth
                        # First 0 avoid errors 
                        indice_primer_cero = np.where(np.array(vivas_tasa_crecimiento) == 0)[0]
                        if len(indice_primer_cero) > 0:
                            # Get growth rate before the 0
                            tasas_crecimiento.append(np.diff(vivas_tasa_crecimiento[:indice_primer_cero[0] - 1]) / vivas_tasa_crecimiento[:-1][:indice_primer_cero[0] - 2] * 100)
                        else:
                            # Growth rate
                            tasas_crecimiento.append(np.diff(vivas_tasa_crecimiento) / vivas_tasa_crecimiento[:-1] * 100)
                        # Collect the data
                        list_alive_UDs.append(len([ud for id, ud in uds_copy.items() if ud.activa == True])) #For heatmap
                        list_vivas_puntos_vista.append(vivas_puntos_vista)
                        #print(f"""
                        #    Acabó la simulacion con media de {int(media)} y {int(iniciais)} unidades iniciales. Prob de morte: {prob_morte}
                        #    poblacion total al final de la simulación: {len([ud for id, ud in uds_copy.items() if ud.activa == True])}""")
                    media = original_media
                    end_config = time.time()
                    mM[i][j] = {'alive': np.mean(list_alive_UDs),
                                'std': np.std(list_alive_UDs),
                                'time used': end_config - star_configuration}
                    datos_1[i][j] = {'tempo': tempo, 
                                    'mean': np.mean(list_vivas_puntos_vista, axis=0), 
                                    'std':  np.std(list_vivas_puntos_vista, axis=0),
                                    'growth rate': np.mean([np.mean(lista) for lista in tasas_crecimiento])}
                    print(f"""
            The total time of the configuration of mean {media} and initial UDs {iniciais} is  {end_config - star_configuration}
                    """)
            # Folder
            # Heatmap and std
            heat_std = os.path.join(folder_name, 'Dual_beta_fixed.npy')
            np.save(heat_std, mM)
            # Behavior of experiments
            behavior = os.path.join(folder_name, 'Dual_beta_fixed_data.npy')
            np.save(behavior, datos_1)
            now = datetime.now()
            finish = time.time()
            print(f"""
            It finished at: {now}
            It lasted {finish-start}
            """)
            print("done")
            #Folders
            heat_std = os.path.join(folder_name, 'Dual_beta_fixed.npy')
            behavior = os.path.join(folder_name, 'Dual_beta_fixed_data.npy')
            ## heatmap and mean
            mM_datos = np.load(heat_std, allow_pickle=True)
            ## behavior for experiments
            mM_behavior = np.load(behavior, allow_pickle=True)
            plot = plot_heatmap(mM_datos, malphas, mbetas, 'Mean Children', 'Initial UDs', 'alive', (0, 3000))
            plot.savefig(os.path.join(folder_name, 'Dual_beta_fixed_mean.png'), dpi=300, bbox_inches="tight")
            print(f"Heatmap of the mean pop saved to: {os.path.join(folder_name, 'Dual_beta_fixed_mean.png')}")
            plot = plot_heatmap(mM_datos, malphas, mbetas, 'Mean Children', 'Initial UDs', 'std', (0, 3000))
            plot.savefig(os.path.join(folder_name, 'Dual_beta_fixed_std.png'), dpi=300, bbox_inches="tight")
            print(f"Heatmap of the mean std saved to: {os.path.join(folder_name, 'Dual_beta_fixed_std.png')}")
        elif variable_choice == '2': # Initial UDs
            #This experiment has Uds inicias in 40
            iniciais = 40
            n = 4
            ualphas = np.linspace(1,n,n) # Average number of children: from 1 to n
            ubetas = np.linspace(0.055, 0.075, 5) # Beta from 0.045 to 0.075
            uM = np.empty((len(ualphas), len(ubetas)), dtype=object)
            punto_vista = 50
            tiempo = 700
            tempo = list(range(0,tiempo,punto_vista))
            experiments = 130

            start = time.time()
            # For data of behaviour
            datos_2 = np.empty((len(ualphas), len(ubetas)), dtype=object)
            print(uM.shape)

            for i, media in enumerate(ualphas):
                for j, prob_morte  in enumerate(ubetas):
                    list_alive_UDs = []
                    list_vivas_puntos_vista = []
                    tasas_crecimiento = []
                    star_configuration = time.time()
                    for experiment in range(1, experiments+1):
                        print(f'Go with experiment {experiment}')
                        #### Initialization
                        clanes = [1,2]
                        clans = (clanes * (int(iniciais) // 2)) + clanes[:(int(iniciais) % 2)]
                        random.shuffle(clans)
                        UD_dual_organization.uds = {}
                        instancias_ud = []
                        for id_ud in range(1, int(iniciais) + 1):
                            instancias_ud.append(UD_dual_organization(id_ud, media, clans.pop()))
                        ## Varieties
                        limited_varieties = True
                        if limited_varieties == False:
                            for id_ud, ud in UD_dual_organization.uds.items():
                                for _ in range(3):
                                    ud.varieties.append(Variety())
                        else:
                            initial_varieties = [Variety() for _ in range (10)]
                            for ud in UD_dual_organization.uds.values():
                                for _ in range(3):
                                    ud.varieties.append(random.choice(initial_varieties))
                        # Lists for graphs
                        vivas_puntos_vista = [int(iniciais)]
                        vivas_tasa_crecimiento = [int(iniciais)]
                        mortas_puntos_vista = [0]
                        # Simulation
                        for t in range(1, tiempo):
                            uds_copy = {id_ud: ud for id_ud, ud in UD_dual_organization.uds.items() if ud.activa}
                            items = list(uds_copy.items())
                            random.shuffle(items)
                            uds_copy = dict(items)  
                            if not uds_copy:
                                # Only 0
                                #print(f"acabó en el experimento {experiment} de la media {malphas[i]} con unidades {mbetas[j]}")
                                vivas_puntos_vista.extend([0] * (int((tiempo/punto_vista)-(len(vivas_puntos_vista)))))
                                vivas_tasa_crecimiento.extend([0] * (int((tiempo)-(len(vivas_tasa_crecimiento)))))
                                #mortas_puntos_vista.extend([unidades_iniciais] * (tiempo - t))
                                break
                            for id_ud, ud in uds_copy.items():
                                ud.ter_filho()
                                ud.buscar_ud(uds_copy, int(media),0 , True, 0.2)
                                ud.incrementar_idade()
                                ud.death_probability(prob_morte)
                            # Collecting data
                            vivas_tasa_crecimiento.append(len([ud for id, ud in uds_copy.items() if ud.activa]))
                            if t % punto_vista == 0:
                                viv = len([ud for id, ud in uds_copy.items() if ud.activa])
                                #mort = len([ud for id, ud in uds_copy.items() if not ud.activa])
                                vivas_puntos_vista.append(viv)
            #                     mortas_puntos_vista.append(mort)
                        # Average Annual Population Growth
                        indice_primer_cero = np.where(np.array(vivas_tasa_crecimiento) == 0)[0]
                        if len(indice_primer_cero) > 0:
                            # Only before 0
                            tasas_crecimiento.append(np.diff(vivas_tasa_crecimiento[:indice_primer_cero[0] - 1]) / vivas_tasa_crecimiento[:-1][:indice_primer_cero[0] - 2] * 100)
                        else:
                            tasas_crecimiento.append(np.diff(vivas_tasa_crecimiento) / vivas_tasa_crecimiento[:-1] * 100)
                        # Collect the data
                        print(f"acabó en el experimento {experiment}")
                        list_alive_UDs.append(len([ud for id, ud in uds_copy.items() if ud.activa == True])) #For heatmap
                        list_vivas_puntos_vista.append(vivas_puntos_vista)
                        #print(f"""
                        #    Acabó la simulacion con media de {int(media)} y {int(iniciais)} unidades iniciales. Prob de morte: {prob_morte}
                        #    poblacion total al final de la simulación: {len([ud for id, ud in uds_copy.items() if ud.activa == True])}""")
                    end_config = time.time()
                    uM[i][j] = {'alive': np.mean(list_alive_UDs),
                                'std': np.std(list_alive_UDs),
                                'time used': end_config - star_configuration}
                    datos_2[i][j] = {'tempo': tempo, 
                                    'mean': np.mean(list_vivas_puntos_vista, axis=0), 
                                    'std':  np.std(list_vivas_puntos_vista, axis=0),
                                    'growth rate': np.mean([np.mean(lista) for lista in tasas_crecimiento])}
                    print(f"""
            The total time of the configuration of mean {media} and beta {prob_morte:.3f} is  {end_config - star_configuration}
                    """)
            # Folders and save
            # Heatmap and std
            heat_std = os.path.join(folder_name, 'Dual_UDin_fixed.npy')
            np.save(heat_std, uM)
            # Behavior of experiments
            behavior = os.path.join(folder_name, 'Dual_Udin_fixed_data.npy')
            np.save(behavior, datos_2)
            now = datetime.now()
            finish = time.time()
            print(f"""
            It finished at: {now}
            It lasted {finish-start}
            """)
            print("done")
            #Folders load
            heat_std = os.path.join(folder_name, 'Dual_UDin_fixed.npy')
            behavior = os.path.join(folder_name, 'Dual_Udin_fixed_data.npy')
            ## heatmap and mean
            uM_datos = np.load(heat_std, allow_pickle=True)
            ## behavior for experiments
            uM_behavior = np.load(behavior, allow_pickle=True)
            plot = plot_heatmap(uM_datos, ualphas, ubetas, 'Mean Children', 'Beta', 'alive')
            plot.savefig(os.path.join(folder_name, 'Dual_UDin_fixed_mean.png'), dpi=300, bbox_inches="tight")
            print(f"Heatmap of the mean pop saved to: {os.path.join(folder_name, 'Dual_UDin_fixed_mean.png')}")
            plot = plot_heatmap(uM_datos, ualphas, ubetas, 'Mean Children', 'Beta', 'std')
            plot.savefig(os.path.join(folder_name, 'Dual_UDin_fixed_std.png'), dpi=300, bbox_inches="tight")
            print(f"Heatmap of the mean std saved to: {os.path.join(folder_name, 'Dual_UDin_fixed_std.png')}")
        else: # Mean of children for UD
            #This experiment has mean of children: 4
            media = 4
            n = 40
            halphas = np.linspace(10,n,int(n/10)) # Unidades inicias from 10 to 50
            hbetas = np.linspace(0.055, 0.075, 5) # Beta from 0.055 to 0.075
            hM = np.empty((len(halphas), len(hbetas)), dtype=object)
            punto_vista = 2
            tiempo = 700
            tempo = list(range(0,tiempo,punto_vista))
            experiments = 130
            start = time.time()
            # For data of behaviour
            datos_3 = np.empty((len(halphas), len(hbetas)), dtype=object)
            print(hM.shape)
            for i, iniciais in enumerate(halphas):
                for j, prob_morte  in enumerate(hbetas):
                    list_alive_UDs = []
                    list_vivas_puntos_vista = []
                    tasas_crecimiento = []
                    star_configuration = time.time()
                    original_media = media
                    for experiment in range(1, experiments+1):
                        #### Initialization
                        print(f'Go with experiment {experiment}')
                        clanes = [1,2]
                        clans = (clanes * (int(iniciais) // 2)) + clanes[:(int(iniciais) % 2)]
                        random.shuffle(clans)
                        UD_dual_organization.uds = {}
                        instancias_ud = []
                        for id_ud in range(1, int(iniciais) + 1):
                                instancias_ud.append(UD_dual_organization(id_ud, media, clans.pop()))
                        ## Varieties
                        limited_varieties = True
                        if limited_varieties == False:
                            for id_ud, ud in UD_dual_organization.uds.items():
                                for _ in range(3):
                                    ud.varieties.append(Variety())
                        else:
                            initial_varieties = [Variety() for _ in range (10)]
                            for ud in UD_dual_organization.uds.values():
                                for _ in range(3):
                                    ud.varieties.append(random.choice(initial_varieties))
                        # Lists for graphs
                        vivas_puntos_vista = [int(iniciais)]
                        vivas_tasa_crecimiento = [int(iniciais)]
                        mortas_puntos_vista = [0]
                        # Simulation
                        for t in range(1, tiempo):
                            uds_copy = {id_ud: ud for id_ud, ud in UD_dual_organization.uds.items() if ud.activa}
                            items = list(uds_copy.items())
                            random.shuffle(items)
                            uds_copy = dict(items) 
                            if not uds_copy:
                                # Only 0
                                #print(f"acabó en el experimento {experiment} de la media {malphas[i]} con unidades {mbetas[j]}")
                                vivas_puntos_vista.extend([0] * (int((tiempo/punto_vista)-(len(vivas_puntos_vista)))))
                                vivas_tasa_crecimiento.extend([0] * (int((tiempo)-(len(vivas_tasa_crecimiento)))))
                                #mortas_puntos_vista.extend([unidades_iniciais] * (tiempo - t))
                                break
                            for id_ud, ud in uds_copy.items():
                                ud.ter_filho()
                                ud.buscar_ud(uds_copy, int(media),0 , True, 0.2)
                                ud.incrementar_idade()
                                ud.death_probability(prob_morte)
                            # Collecting data
                            vivas_tasa_crecimiento.append(len([ud for id, ud in uds_copy.items() if ud.activa]))
                            if t % punto_vista == 0:
                                viv = len([ud for id, ud in uds_copy.items() if ud.activa])
                                #mort = len([ud for id, ud in uds_copy.items() if not ud.activa])
                                vivas_puntos_vista.append(viv)
            #                     mortas_puntos_vista.append(mort)
                        # Average Annual Population Growth
                        indice_primer_cero = np.where(np.array(vivas_tasa_crecimiento) == 0)[0]
                        if len(indice_primer_cero) > 0:
                            # Only before 0
                            tasas_crecimiento.append(np.diff(vivas_tasa_crecimiento[:indice_primer_cero[0] - 1]) / vivas_tasa_crecimiento[:-1][:indice_primer_cero[0] - 2] * 100)
                        else:
                            tasas_crecimiento.append(np.diff(vivas_tasa_crecimiento) / vivas_tasa_crecimiento[:-1] * 100)
                        # Collect the data
                        list_alive_UDs.append(len([ud for id, ud in uds_copy.items() if ud.activa == True])) #For heatmap
                        list_vivas_puntos_vista.append(vivas_puntos_vista)
                    media = original_media
                    end_config = time.time()
                    hM[i][j] = {'alive': np.mean(list_alive_UDs),
                                'std': np.std(list_alive_UDs),
                                'time used': end_config - star_configuration}
                    datos_3[i][j] = {'tempo': tempo, 
                                    'mean': np.mean(list_vivas_puntos_vista, axis=0), 
                                    'std':  np.std(list_vivas_puntos_vista, axis=0),
                                    'growth rate': np.mean([np.mean(lista) for lista in tasas_crecimiento])}
                    print(f"""
            The total time of the configuration of Initial UDs {iniciais} and beta {prob_morte:.3f} is: {end_config - star_configuration}
                    """)
            # Folders and save
            # Heatmap and std
            heat_std = os.path.join(folder_name, 'Dual_Mean_fixed.npy')
            np.save(heat_std, hM)
            # Behavior of experiments
            behavior = os.path.join(folder_name, 'Dual_Mean_fixed_data.npy')
            np.save(behavior, datos_3)
            now = datetime.now()
            finish = time.time()
            print(f"""
            It finished at: {now}
            It lasted {finish-start}
            """)
            print("done")
            #Folders
            heat_std = os.path.join(folder_name, 'Dual_Mean_fixed.npy')
            behavior = os.path.join(folder_name, 'Dual_Mean_fixed_data.npy')
            ## heatmap and mean
            hM_datos = np.load(heat_std, allow_pickle=True)
            ## behavior for experiments
            hM_behavior = np.load(behavior, allow_pickle=True)
            plot = plot_heatmap(hM_datos, halphas, hbetas, 'Initial UDs', 'Beta', 'alive')
            plot.savefig(os.path.join(folder_name, 'Dual_Mean_fixed_mean.png'), dpi=300, bbox_inches="tight")
            print(f"Heatmap of the mean pop saved to: {os.path.join(folder_name, 'Dual_Mean_fixed_mean.png')}")
            plot = plot_heatmap(hM_datos, halphas, hbetas, 'Initial UDs', 'Beta', 'std')
            plot.savefig(os.path.join(folder_name, 'Dual_Mean_fixed_std.png'), dpi=300, bbox_inches="tight")
            print(f"Heatmap of the mean std saved to: {os.path.join(folder_name, 'Dual_Mean_fixed_std.png')}")
    else: #Generalized exchange
                #sub folder
        folder_name = os.path.join(parent_folder, 'results_validation', 'populational behavior', 'Generalized Exchange')
        # Create the results_validation sub-folder if it doesn't exist
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
        if variable_choice == '1': # Beta
            #This experiment has the beta fixed in 0.06
            prob_morte = 0.06
            n = 4
            m = 40
            malphas = np.linspace(1,n,n) # Average number of children: from 1 to n
            mbetas = np.linspace(10,m,int(m/10)) # Initial UDs: from 10 to m
            mM = np.empty((len(malphas), len(mbetas)), dtype=object)
            punto_vista = 2
            tiempo = 700
            tempo = list(range(0,tiempo,punto_vista))
            experiments = 130
            # For data of behaviour
            datos_1 = np.empty((len(malphas), len(mbetas)), dtype=object)
            print(mM.shape)
            start = time.time()

            for i, media in enumerate(malphas):
                for j, iniciais  in enumerate(mbetas):
                    list_alive_UDs = []
                    list_vivas_puntos_vista = []
                    tasas_crecimiento = []
                    star_configuration = time.time()
                    original_media = media
                    for experiment in range(1, experiments+1):
                        #### Initialization
                        print(f'Go with experiment {experiment}')
                        clanes = [1,2,3]
                        clans = (clanes * (int(iniciais) // 3)) + clanes[:(int(iniciais) % 3)]# Just 3 clans
                        random.shuffle(clans)
                        UD_generalized.uds = {}
                        instancias_ud = []
                        for id_ud in range(1, int(iniciais) + 1):
                                instancias_ud.append(UD_generalized(id_ud, media, clans.pop()))
                        ## Varieties
                        limited_varieties = True
                        if limited_varieties == False:
                            for id_ud, ud in UD_generalized.uds.items():
                                for _ in range(3):
                                    ud.varieties.append(Variety())
                        else:
                            initial_varieties = [Variety() for _ in range (10)]
                            for ud in UD_generalized.uds.values():
                                for _ in range(3):
                                    ud.varieties.append(random.choice(initial_varieties))
                        # Lists for graphs
                        vivas_puntos_vista = [int(iniciais)]
                        vivas_tasa_crecimiento = [int(iniciais)]
                        mortas_puntos_vista = [0]
                        # Simulation
                        for t in range(1, tiempo):
                            uds_copy = {id_ud: ud for id_ud, ud in UD_generalized.uds.items() if ud.activa}
                            items = list(uds_copy.items())
                            random.shuffle(items)
                            uds_copy = dict(items) 
                            if not uds_copy:
                                # Only 0
                                print(f"acabó en el experimento {experiment} de la media {malphas[i]} con unidades {mbetas[j]}")
                                vivas_puntos_vista.extend([0] * (int((tiempo/punto_vista)-(len(vivas_puntos_vista)))))
                                vivas_tasa_crecimiento.extend([0] * (int((tiempo)-(len(vivas_tasa_crecimiento)))))
                                #mortas_puntos_vista.extend([unidades_iniciais] * (tiempo - t))
                                break
                            for id_ud, ud in uds_copy.items():
                                ud.ter_filho()
                                ud.buscar_ud(uds_copy, media, 0, True, 0.2)
                                ud.incrementar_idade()
                                ud.death_probability(prob_morte)
                            # Collecting data
                            vivas_tasa_crecimiento.append(len([ud for id, ud in uds_copy.items() if ud.activa]))
                            if t % punto_vista == 0:
                                viv = len([ud for id, ud in uds_copy.items() if ud.activa])
                                #mort = len([ud for id, ud in uds_copy.items() if not ud.activa])
                                vivas_puntos_vista.append(viv)
            #                     mortas_puntos_vista.append(mort)
            #                 if t%100 == 0:
            #                     print(f"tamos en tiempo {t} con vivas {viv}")
                        # Average Annual Population Growth
                        # First 0 avoid errors 
                        indice_primer_cero = np.where(np.array(vivas_tasa_crecimiento) == 0)[0]
                        if len(indice_primer_cero) > 0:
                            # Get growth rate before the 0
                            tasas_crecimiento.append(np.diff(vivas_tasa_crecimiento[:indice_primer_cero[0] - 1]) / vivas_tasa_crecimiento[:-1][:indice_primer_cero[0] - 2] * 100)
                        else:
                            # Growth rate
                            tasas_crecimiento.append(np.diff(vivas_tasa_crecimiento) / vivas_tasa_crecimiento[:-1] * 100)
                        # Collect the data
                        list_alive_UDs.append(len([ud for id, ud in uds_copy.items() if ud.activa == True])) #For heatmap
                        list_vivas_puntos_vista.append(vivas_puntos_vista)
                        #print(f"""
                        #    Acabó la simulacion con media de {int(media)} y {int(iniciais)} unidades iniciales. Prob de morte: {prob_morte}
                        #    poblacion total al final de la simulación: {len([ud for id, ud in uds_copy.items() if ud.activa == True])}""")
                    media = original_media
                    end_config = time.time()
                    mM[i][j] = {'alive': np.mean(list_alive_UDs),
                                'std': np.std(list_alive_UDs),
                                'time used': end_config - star_configuration}
                    datos_1[i][j] = {'tempo': tempo, 
                                    'mean': np.mean(list_vivas_puntos_vista, axis=0), 
                                    'std':  np.std(list_vivas_puntos_vista, axis=0),
                                    'growth rate': np.mean([np.mean(lista) for lista in tasas_crecimiento])}
                    print(f"""
            The total time of the configuration of mean {media} and initial UDs {iniciais} is  {end_config - star_configuration}
                    """)
            # Folder and save
            # Heatmap and std
            heat_std = os.path.join(folder_name, 'Generalized_beta_fixed.npy')
            np.save(heat_std, mM)
            # Behavior of experiments
            behavior = os.path.join(folder_name, 'Generalized_beta_fixed_data.npy')
            np.save(behavior, datos_1)
            now = datetime.now()
            finish = time.time()
            print(f"""
            It finished at: {now}
            It lasted {finish-start}
            """)
            print("done")
            #Folders load
            heat_std = os.path.join(folder_name, 'Generalized_beta_fixed.npy')
            behavior = os.path.join(folder_name, 'Generalized_beta_fixed_data.npy')
            ## heatmap and mean
            mM_datos = np.load(heat_std, allow_pickle=True)
            ## behavior for experiments
            mM_behavior = np.load(behavior, allow_pickle=True)
            plot = plot_heatmap(mM_datos, malphas, mbetas, 'Mean Children', 'Initial UDs', 'alive')
            plot.savefig(os.path.join(folder_name, 'Generalized_beta_fixed_mean.png'), dpi=300, bbox_inches="tight")
            print(f"Heatmap of the mean pop saved to: {os.path.join(folder_name, 'Generalized_beta_fixed_mean.png')}")
            plot = plot_heatmap(mM_datos, malphas, mbetas, 'Mean Children', 'Initial UDs', 'std')
            plot.savefig(os.path.join(folder_name, 'Generalized_beta_fixed_std.png'), dpi=300, bbox_inches="tight")
            print(f"Heatmap of the mean std saved to: {os.path.join(folder_name, 'Generalized_beta_fixed_std.png')}")
        elif variable_choice == '2': # Initial UDs
            #This experiment has Uds inicias in 40
            iniciais = 40
            n = 4
            ualphas = np.linspace(1,n,n) # Average number of children: from 1 to n
            ubetas = np.linspace(0.055, 0.075, 5) # Beta from 0.055 to 0.075
            uM = np.empty((len(ualphas), len(ubetas)), dtype=object)
            punto_vista = 2
            tiempo = 700
            tempo = list(range(0,tiempo,punto_vista))
            experiments = 130

            start = time.time()
            # For data of behaviour
            datos_2 = np.empty((len(ualphas), len(ubetas)), dtype=object)
            print(uM.shape)

            for i, media in enumerate(ualphas):
                for j, prob_morte  in enumerate(ubetas):
                    list_alive_UDs = []
                    list_vivas_puntos_vista = []
                    tasas_crecimiento = []
                    star_configuration = time.time()
                    original_media = media
                    for experiment in range(1, experiments+1):
                        #### Initialization
                        print(f'Go with experiment {experiment}')
                        clanes = [1,2,3]
                        clans = (clanes * (int(iniciais) // 3)) + clanes[:(int(iniciais) % 3)]# Just 3 clans
                        random.shuffle(clans)
                        UD_generalized.uds = {}
                        instancias_ud = []
                        for id_ud in range(1, int(iniciais) + 1):
                                instancias_ud.append(UD_generalized(id_ud, media, clans.pop()))
                        ## Varieties
                        limited_varieties = True
                        if limited_varieties == False:
                            for id_ud, ud in UD_generalized.uds.items():
                                for _ in range(3):
                                    ud.varieties.append(Variety())
                        else:
                            initial_varieties = [Variety() for _ in range (10)]
                            for ud in UD_generalized.uds.values():
                                for _ in range(3):
                                    ud.varieties.append(random.choice(initial_varieties))
                        # Lists for graphs
                        vivas_puntos_vista = [int(iniciais)]
                        vivas_tasa_crecimiento = [int(iniciais)]
                        mortas_puntos_vista = [0]
                        # Simulation
                        for t in range(1, tiempo):
                            uds_copy = {id_ud: ud for id_ud, ud in UD_generalized.uds.items() if ud.activa}
                            items = list(uds_copy.items())
                            random.shuffle(items)
                            uds_copy = dict(items) 
                            if not uds_copy:
                                # Only 0
                                #print(f"acabó en el experimento {experiment} de la media {malphas[i]} con unidades {mbetas[j]}")
                                vivas_puntos_vista.extend([0] * (int((tiempo/punto_vista)-(len(vivas_puntos_vista)))))
                                vivas_tasa_crecimiento.extend([0] * (int((tiempo)-(len(vivas_tasa_crecimiento)))))
                                #mortas_puntos_vista.extend([unidades_iniciais] * (tiempo - t))
                                break
                            for id_ud, ud in uds_copy.items():
                                ud.ter_filho()
                                ud.buscar_ud(uds_copy, media, 0, True, 0.2)
                                ud.incrementar_idade()
                                ud.death_probability(prob_morte)
                            # Collecting data
                            vivas_tasa_crecimiento.append(len([ud for id, ud in uds_copy.items() if ud.activa]))
                            if t % punto_vista == 0:
                                viv = len([ud for id, ud in uds_copy.items() if ud.activa])
                                #mort = len([ud for id, ud in uds_copy.items() if not ud.activa])
                                vivas_puntos_vista.append(viv)
            #                     mortas_puntos_vista.append(mort)
                        # Average Annual Population Growth
                        indice_primer_cero = np.where(np.array(vivas_tasa_crecimiento) == 0)[0]
                        if len(indice_primer_cero) > 0:
                            # Only before 0
                            tasas_crecimiento.append(np.diff(vivas_tasa_crecimiento[:indice_primer_cero[0] - 1]) / vivas_tasa_crecimiento[:-1][:indice_primer_cero[0] - 2] * 100)
                        else:
                            tasas_crecimiento.append(np.diff(vivas_tasa_crecimiento) / vivas_tasa_crecimiento[:-1] * 100)
                        # Collect the data
                        list_alive_UDs.append(len([ud for id, ud in uds_copy.items() if ud.activa == True])) #For heatmap
                        list_vivas_puntos_vista.append(vivas_puntos_vista)
                        #print(f"""
                        #    Acabó la simulacion con media de {int(media)} y {int(iniciais)} unidades iniciales. Prob de morte: {prob_morte}
                        #    poblacion total al final de la simulación: {len([ud for id, ud in uds_copy.items() if ud.activa == True])}""")
                    media = original_media
                    end_config = time.time()
                    uM[i][j] = {'alive': np.mean(list_alive_UDs),
                                'std': np.std(list_alive_UDs),
                                'time used': end_config - star_configuration}
                    datos_2[i][j] = {'tempo': tempo, 
                                    'mean': np.mean(list_vivas_puntos_vista, axis=0), 
                                    'std':  np.std(list_vivas_puntos_vista, axis=0),
                                    'growth rate': np.mean([np.mean(lista) for lista in tasas_crecimiento])}
                    print(f"""
            The total time of the configuration of mean {original_media} and beta {prob_morte:.3f} is  {end_config - star_configuration}
                    """)
            # Folders and save
            # Heatmap and std
            heat_std = os.path.join(folder_name, 'Generalized_UDin_fixed.npy')
            np.save(heat_std, uM)
            # Behavior of experiments
            behavior = os.path.join(folder_name, 'Generalized_Udin_fixed_data.npy')
            np.save(behavior, datos_2)
            now = datetime.now()
            finish = time.time()
            print(f"""
            It finished at: {now}
            It lasted {finish-start}
            """)
            print("done")
            #Folders load
            heat_std = os.path.join(folder_name, 'Generalized_UDin_fixed.npy')
            behavior = os.path.join(folder_name, 'Generalized_UDin_fixed_data.npy')
            ## heatmap and mean
            uM_datos = np.load(heat_std, allow_pickle=True)
            ## behavior for experiments
            uM_behavior = np.load(behavior, allow_pickle=True)
            plot = plot_heatmap(uM_datos, ualphas, ubetas, 'Mean Children', 'Beta', 'alive')
            plot.savefig(os.path.join(folder_name, 'Generalized_UDin_fixed_mean.png'), dpi=300, bbox_inches="tight")
            print(f"Heatmap of the mean pop saved to: {os.path.join(folder_name, 'Generalized_UDin_fixed_mean.png')}")
            plot = plot_heatmap(uM_datos, ualphas, ubetas, 'Mean Children', 'Beta', 'std')
            plot.savefig(os.path.join(folder_name, 'Generalized_UDin_fixed_std.png'), dpi=300, bbox_inches="tight")
            print(f"Heatmap of the mean std saved to: {os.path.join(folder_name, 'Generalized_UDin_fixed_std.png')}")
        else: # Mean of children for UD
            #This experiment has mean of children: 4
            media = 4
            n = 40
            halphas = np.linspace(10,n,int(n/10)) # Unidades inicias from 10 to 50
            hbetas = np.linspace(0.055, 0.075, 5) # Beta from 0.055 to 0.075
            hM = np.empty((len(halphas), len(hbetas)), dtype=object)
            punto_vista = 2
            tiempo = 700
            tempo = list(range(0,tiempo,punto_vista))
            experiments = 130

            start = time.time()
            # For data of behaviour
            datos_3 = np.empty((len(halphas), len(hbetas)), dtype=object)
            # print(uM.shape)

            for i, iniciais in enumerate(halphas):
                for j, prob_morte  in enumerate(hbetas):
                    list_alive_UDs = []
                    list_vivas_puntos_vista = []
                    tasas_crecimiento = []
                    star_configuration = time.time()
                    original_media = media
                    for experiment in range(1, experiments+1):
                        #### Initialization
                        print(f'Go with experiment {experiment}')
                        clanes = [1,2,3]
                        clans = (clanes * (int(iniciais) // 3)) + clanes[:(int(iniciais) % 3)]# Just 3 clans
                        random.shuffle(clans)
                        UD_generalized.uds = {}
                        instancias_ud = []
                        for id_ud in range(1, int(iniciais) + 1):
                                instancias_ud.append(UD_generalized(id_ud, media, clans.pop()))
                        ## Varieties
                        limited_varieties = True
                        if limited_varieties == False:
                            for id_ud, ud in UD_generalized.uds.items():
                                for _ in range(3):
                                    ud.varieties.append(Variety())
                        else:
                            initial_varieties = [Variety() for _ in range (10)]
                            for ud in UD_generalized.uds.values():
                                for _ in range(3):
                                    ud.varieties.append(random.choice(initial_varieties))
                        # Lists for graphs
                        vivas_puntos_vista = [int(iniciais)]
                        vivas_tasa_crecimiento = [int(iniciais)]
                        mortas_puntos_vista = [0]
                        # Simulation
                        for t in range(1, tiempo):
                            uds_copy = {id_ud: ud for id_ud, ud in UD_generalized.uds.items() if ud.activa}
                            items = list(uds_copy.items())
                            random.shuffle(items)
                            uds_copy = dict(items)  
                            if not uds_copy:
                                # Only 0
                                #print(f"acabó en el experimento {experiment} de la media {malphas[i]} con unidades {mbetas[j]}")
                                vivas_puntos_vista.extend([0] * (int((tiempo/punto_vista)-(len(vivas_puntos_vista)))))
                                vivas_tasa_crecimiento.extend([0] * (int((tiempo)-(len(vivas_tasa_crecimiento)))))
                                #mortas_puntos_vista.extend([unidades_iniciais] * (tiempo - t))
                                break
                            for id_ud, ud in uds_copy.items():
                                ud.ter_filho()
                                ud.buscar_ud(uds_copy, media, 0, True, 0.2)
                                ud.incrementar_idade()
                                ud.death_probability(prob_morte)
                            # Collecting data
                            vivas_tasa_crecimiento.append(len([ud for id, ud in uds_copy.items() if ud.activa]))
                            if t % punto_vista == 0:
                                viv = len([ud for id, ud in uds_copy.items() if ud.activa])
                                #mort = len([ud for id, ud in uds_copy.items() if not ud.activa])
                                vivas_puntos_vista.append(viv)
            #                     mortas_puntos_vista.append(mort)
                        # Average Annual Population Growth
                        indice_primer_cero = np.where(np.array(vivas_tasa_crecimiento) == 0)[0]
                        if len(indice_primer_cero) > 0:
                            # Only before 0
                            tasas_crecimiento.append(np.diff(vivas_tasa_crecimiento[:indice_primer_cero[0] - 1]) / vivas_tasa_crecimiento[:-1][:indice_primer_cero[0] - 2] * 100)
                        else:
                            tasas_crecimiento.append(np.diff(vivas_tasa_crecimiento) / vivas_tasa_crecimiento[:-1] * 100)
                        # Collect the data
                        list_alive_UDs.append(len([ud for id, ud in uds_copy.items() if ud.activa == True])) #For heatmap
                        list_vivas_puntos_vista.append(vivas_puntos_vista)
                        #print(f"""
                        #    Acabó la simulacion con media de {int(media)} y {int(iniciais)} unidades iniciales. Prob de morte: {prob_morte}
                        #    poblacion total al final de la simulación: {len([ud for id, ud in uds_copy.items() if ud.activa == True])}""")
                    media = original_media
                    end_config = time.time()
                    hM[i][j] = {'alive': np.mean(list_alive_UDs),
                                'std': np.std(list_alive_UDs),
                                'time used': end_config - star_configuration}
                    datos_3[i][j] = {'tempo': tempo, 
                                    'mean': np.mean(list_vivas_puntos_vista, axis=0), 
                                    'std':  np.std(list_vivas_puntos_vista, axis=0),
                                    'growth rate': np.mean([np.mean(lista) for lista in tasas_crecimiento])}
                    print(f"""
            The total time of the configuration of Initial UDs {iniciais} and beta {prob_morte:.3f} is: {end_config - star_configuration}
                    """)
            # Folders and save
            # Heatmap and std
            heat_std = os.path.join(folder_name, 'Generalized_Mean_fixed.npy')
            np.save(heat_std, hM)
            # Behavior of experiments
            behavior = os.path.join(folder_name, 'Generalized_Mean_fixed_data.npy')
            np.save(behavior, datos_3)
            now = datetime.now()
            finish = time.time()
            print(f"""
            It finished at: {now}
            It lasted {finish-start}
            """)
            print("done")
            #Folders load
            heat_std = os.path.join(folder_name, 'Generalized_Mean_fixed.npy')
            behavior = os.path.join(folder_name, 'Generalized_Mean_fixed_data.npy')
            ## heatmap and mean
            hM_datos = np.load(heat_std, allow_pickle=True)
            ## behavior for experiments
            hM_behavior = np.load(behavior, allow_pickle=True)
            plot = plot_heatmap(hM_datos, halphas, hbetas, 'Initial UDs', 'Beta', 'alive')
            plot.savefig(os.path.join(folder_name, 'Generalized_Mean_fixed_mean.png'), dpi=300, bbox_inches="tight")
            print(f"Heatmap of the mean pop saved to: {os.path.join(folder_name, 'Generalized_Mean_fixed_mean.png')}")
            plot = plot_heatmap(hM_datos, halphas, hbetas, 'Initial UDs', 'Beta', 'std')
            plot.savefig(os.path.join(folder_name, 'Generalized_Mean_fixed_std.png'), dpi=300, bbox_inches="tight")
            print(f"Heatmap of the mean std saved to: {os.path.join(folder_name, 'Generalized_Mean_fixed_std.png')}")

