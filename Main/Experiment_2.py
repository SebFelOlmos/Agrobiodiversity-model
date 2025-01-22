import numpy as np
import random
import time
import random
import os
import sys
from datetime import datetime
import matplotlib.pyplot as plt

random.seed(42)
np.random.seed(42)

# Path
current_directory = os.path.dirname(os.path.abspath(__file__))
root_directory = os.path.abspath(os.path.join(current_directory, '..'))
sys.path.append(root_directory)
#Network and measures
from to_get_data.net_construction_vis_measures import *
from to_get_data.generate_database import *
#Agrobiodiversity
from to_get_data.agrobiodiversity_data import *
from model_class.Variety import Variety
from model_class.UD_clan import *
from model_class.UD_aleatory_inheritance_clan import *
# Functions for the information
def transversal_changes(matrix, inherits, alphas, kinship_system, variable=''):
    # Plot
    plt.figure(figsize=(10, 6))
    for i, inherit in enumerate(inherits):  # Loop for graphs
        means, stds = [], []  # Lists
        for j, malpha in enumerate(alphas):
            # Ensure diversity_info is not None
            diversity_info = matrix[i][j].get('diversity_info')
            if diversity_info is not None and len(diversity_info) > 1: 
                data = diversity_info[1]
                means.append(np.mean(data))  # Mean
                stds.append(np.std(data))   # Std
            else:
                # Handle missing or invalid data
                means.append(np.nan)  # Append NaN if no valid data
                stds.append(0)  # Zero standard deviation for NaN

        # Plot for each Initial UDs according to the inheritance strategy
        label = inherit if inherit != 'False' else 'Random'
        plt.errorbar(alphas, means, yerr=stds, label=f'{label}', fmt='-o', capsize=5)

    # Labels and title
    plt.xlabel(variable)
    plt.xticks(alphas)
    plt.ylabel('Diversity at the community level')
    plt.title(f'''
    {kinship_system}
    Diversity at the community level for different {variable}''')
    plt.legend(title="Inheritance Levels")
    plt.grid(True)
    plt.ylim(0, 10)
    return plt
    #plt.show()
def transversal_alive(matrix, inherits, alphas, kinship_system, variable=''):
    # Plot setup
    plt.figure(figsize=(10, 6))
    for i, inherit in enumerate(inherits):  # Loop over inheritance levels
        means, stds = [], []  # Lists for storing means and standard deviations
        for j, malpha in enumerate(alphas):
            # Safely extract 'alive' and 'std' information
            alive = matrix[i][j].get('alive')
            std = matrix[i][j].get('std', [0])  # Default std to [0] if key is missing

            if alive is not None and len(std) > 0:
                mean = alive  # Extract mean 'alive' information
                std_value = std[-1]  # Extract the last value in 'std'
            else:
                # Handle invalid data
                mean = np.nan  # Mark as NaN if data is missing
                std_value = 0  # Zero standard deviation for invalid data

            means.append(mean)
            stds.append(std_value)
        
        # Plot for each inheritance level
        label = inherit if inherit != 'False' else 'Random'
        plt.errorbar(alphas, means, yerr=stds, label=f'{label}', fmt='-o', capsize=5)
    
    # Plot formatting
    plt.xlabel(variable)
    plt.xticks(alphas)
    plt.ylabel('Alive UDs')
    plt.title(f'''
    {kinship_system}
    Alive UDs for Different {variable}''')
    plt.legend(title="Inheritance Levels")
    plt.grid(True)
    plt.ylim(0, 250) 
    return plt
    #plt.show()
choice = ''
while choice not in ['1', '2','3']:
    choice = input('''
Hi! you want to execute the simulations for the second experiment! 
I'm not going to lie! This may take time even more time... 
So, what kinship system you want to try?
    1 - Endogamy
    2 - Dual Organization
    3 - Generalized Exchange
''')
parent_folder = 'Outputs'
folder_name = os.path.join(parent_folder, 'Second experiments')
# Ensure the parent folder exists
if not os.path.exists(parent_folder):
    os.makedirs(parent_folder)
# Create the results_validation sub-folder if it doesn't exist
if not os.path.exists(folder_name):
    os.makedirs(folder_name)
# Method for the diversity change over time
variable = ''
while variable not in ['1','2','3','4']:
    variable = input('''
Nice. Now, what variable you want to change over time?
    1 - Initial UDs
    2 - Initial Varieties
    3 - Mean of children by UD
    4 - Number of varieties for UD
    ''')
if choice == '1':
    print('Ok, lets go with endogamy')
    #sub folder
    folder_name = os.path.join(parent_folder, 'Second experiments', 'Endogamy')
    # Create the sub-folder if it doesn't exist
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    if variable  == '1':
        #sub folder
        folder_name = os.path.join(folder_name, 'Initial UDs')
        # Create the sub-folder if it doesn't exist
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
        # This experiment has different values for Initial UDs
        prob_morte = 0.06 #beta
        media = 4 # Mean
        m = 40 # Initial UDs
        inherits = [0,25,50, 'False']
        Emalphas = np.linspace(10,m,int(m/10)) # Initial UDs: from 10 to m
        # For data of behaviour
        mM = np.empty((len(inherits), len(Emalphas)), dtype=object)
        punto_vista = 50
        tiempo = 300
        tempo = list(range(0,tiempo+1,punto_vista))
        experiments = 100
        max_iterations = 140

        print(mM.shape)
        start = time.time()
        print(f"started at:  {datetime.now()}")
        for i, inherit in enumerate(inherits):
            for j, iniciais  in enumerate(Emalphas):
                star_configuration = time.time()
                #For population dynamics
                list_alive_UDs = []
                list_vivas_puntos_vista = []
                tasas_crecimiento = []
                #For diversity dynamics
                data_step_mean_var_ud = []
                data_step_var_system = []
                data_step_unique_system = []
                print(f"Experiments with inheritance {inherit} and Initial UDs {iniciais}")
                #Lists to store experiments' diversity data
                data_endo_mean_ud = []
                data_endo_com_level = []
                data_endo_total_varieties = []
                original_media = media
                #To see how frequent goes to extintion
                contador = 0
                iterations = 0
                while contador < experiments and iterations < max_iterations: 
                #for experiment in range(1, experiments+1):
                    print(f'experimento {contador+1}')
                    if inherit != 'False':
                        
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
                        #For diversity
                        mean_var_ud = []
                        var_system = []
                        unique_system = []
                        var_ud = []
                        var_total = []
                        for ud in [ud for ud in UD_endogamy.uds.values() if ud.activa ==True]:
                            var_ud.append(len(ud.varieties))
                            for variety in ud.varieties:
                                var_total.append(variety.variety_id)
                        mean_var_ud.append(np.mean(var_ud))
                        var_system.append(len(var_total))
                        unique_system.append(len(set(var_total)))
                        # Simulation
                        for t in range(1, tiempo):
                            uds_copy = {id_ud: ud for id_ud, ud in UD_endogamy.uds.items() if ud.activa}
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
                            if not uds_copy: #Extintion
                                # Only 0
                                print(f"acabó en 0 el experimento {contador+1} con herencia {inherits[i]} con unidades {Emalphas[j]}")
                                break         
                            # Cycle:
                            for id_ud, ud in uds_copy.items():
                                ud.ter_filho()
                                ud.buscar_ud(uds_copy, int(media), inherit)
                                ud.incrementar_idade()
                                ud.death_probability(prob_morte)
                            # Collecting data
                            vivas_tasa_crecimiento.append(len([ud for id, ud in uds_copy.items() if ud.activa]))
                            if t % punto_vista == 0:
                                viv = len([ud for id, ud in uds_copy.items() if ud.activa])
                                vivas_puntos_vista.append(viv)
                                # For diversity
                                var_ud = []
                                var_total = []
                                for ud in [ud for ud in UD_endogamy.uds.values() if ud.activa ==True]:
                                    var_ud.append(len(ud.varieties))
                                    for variety in ud.varieties:
                                        var_total.append(variety.variety_id)
                                mean_var_ud.append(np.mean(var_ud))
                                var_system.append(len(var_total))
                                unique_system.append(len(set(var_total))) 
                        viv = len([ud for id, ud in UD_endogamy.uds.items() if ud.activa])
                        vivas_puntos_vista.append(viv)
                        # For diversity
                        var_ud = []
                        var_total = []
                        for ud in [ud for ud in UD_endogamy.uds.values() if ud.activa ==True]:
                            var_ud.append(len(ud.varieties))
                            for variety in ud.varieties:
                                var_total.append(variety.variety_id)
                        mean_var_ud.append(np.mean(var_ud))
                        var_system.append(len(var_total))
                        unique_system.append(len(set(var_total)))
                        alive = (len([ud for id, ud in uds_copy.items() if ud.activa]))
                        if alive >= 1:   
                            total_varieties = []
                            varieties_per_UD = []
                            for ud in [ud for ud in UD_endogamy.uds.values() if ud.activa ==True]:
                                varieties_per_UD.append(len(ud.varieties))
                                for variety in ud.varieties:
                                    total_varieties.append(variety.variety_id)
                            data_endo_mean_ud.append(np.mean(varieties_per_UD))
                            data_endo_com_level.append(len(set(total_varieties)))
                            data_endo_total_varieties.append(total_varieties)
                    
                    else:# Now with inherit == False
                        #### Initialization
                        UD_endogamy_al_inh.uds = {}
                        instancias_ud = []
                        for id_ud in range(1, int(iniciais) + 1):
                            instancias_ud.append(UD_endogamy_al_inh(id_ud, media))
                        ## Varieties
                        limited_varieties = True
                        if limited_varieties == False:
                            for id_ud, ud in UD_endogamy_al_inh.uds.items():
                                for _ in range(3):
                                    ud.varieties.append(Variety())
                        else:
                            initial_varieties = [Variety() for _ in range (10)]
                            for ud in UD_endogamy_al_inh.uds.values():
                                for _ in range(3):
                                    ud.varieties.append(random.choice(initial_varieties))   
                        # Lists for graphs
                        vivas_puntos_vista = [int(iniciais)]
                        vivas_tasa_crecimiento = [int(iniciais)]
                        #For diversity
                        mean_var_ud = []
                        var_system = []
                        unique_system = []
                        var_ud = []
                        var_total = []
                        for ud in [ud for ud in UD_endogamy_al_inh.uds.values() if ud.activa ==True]:
                            var_ud.append(len(ud.varieties))
                            for variety in ud.varieties:
                                var_total.append(variety.variety_id)
                        mean_var_ud.append(np.mean(var_ud))
                        var_system.append(len(var_total))
                        unique_system.append(len(set(var_total)))
                        # Simulation
                        for t in range(1, tiempo):
                            uds_copy = {id_ud: ud for id_ud, ud in UD_endogamy_al_inh.uds.items() if ud.activa}
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
                            if not uds_copy: #Extintion
                                # Only 0
                                print(f"acabó en 0 el experimento {contador+1} con herencia {inherits[i]} con unidades {Emalphas[j]}")
                                break         
                            # Cycle:
                            varieties_list = [var for ud in uds_copy.values() for var in ud.varieties]
                            for id_ud, ud in uds_copy.items():
                                ud.ter_filho()
                                ud.buscar_ud(uds_copy, int(media), varieties_list, 3)
                                ud.incrementar_idade()
                                ud.death_probability(prob_morte)
                            # Collecting data
                            vivas_tasa_crecimiento.append(len([ud for id, ud in uds_copy.items() if ud.activa]))
                            if t % punto_vista == 0:
                                viv = len([ud for id, ud in uds_copy.items() if ud.activa])
                                vivas_puntos_vista.append(viv)
                                # For diversity
                                var_ud = []
                                var_total = []
                                for ud in [ud for ud in UD_endogamy_al_inh.uds.values() if ud.activa ==True]:
                                    var_ud.append(len(ud.varieties))
                                    for variety in ud.varieties:
                                        var_total.append(variety.variety_id)
                                mean_var_ud.append(np.mean(var_ud))
                                var_system.append(len(var_total))
                                unique_system.append(len(set(var_total))) 
                        viv = len([ud for id, ud in UD_endogamy_al_inh.uds.items() if ud.activa])
                        vivas_puntos_vista.append(viv)
                        # For diversity
                        var_ud = []
                        var_total = []
                        for ud in [ud for ud in UD_endogamy_al_inh.uds.values() if ud.activa ==True]:
                            var_ud.append(len(ud.varieties))
                            for variety in ud.varieties:
                                var_total.append(variety.variety_id)
                        mean_var_ud.append(np.mean(var_ud))
                        var_system.append(len(var_total))
                        unique_system.append(len(set(var_total)))
                        alive = (len([ud for id, ud in uds_copy.items() if ud.activa]))
                        if alive >= 1:   
                            total_varieties = []
                            varieties_per_UD = []
                            for ud in [ud for ud in UD_endogamy_al_inh.uds.values() if ud.activa ==True]:
                                varieties_per_UD.append(len(ud.varieties))
                                for variety in ud.varieties:
                                    total_varieties.append(variety.variety_id)
                            data_endo_mean_ud.append(np.mean(varieties_per_UD))
                            data_endo_com_level.append(len(set(total_varieties)))
                            data_endo_total_varieties.append(total_varieties)
                    if len(uds_copy) > 0:
                        list_alive_UDs.append(len([ud for id, ud in uds_copy.items() if ud.activa]))
                        list_vivas_puntos_vista.append(vivas_puntos_vista)
                        data_step_var_system.append(var_system)
                        data_step_unique_system.append(unique_system)
                        data_step_mean_var_ud.append(mean_var_ud)
                        contador += 1
                    iterations += 1
                    print('succesful', contador)
                    print('iterations', iterations)
                    
                    data_inherit_endo = [data_endo_mean_ud, data_endo_com_level, data_endo_total_varieties]
                data_steps_inherit_endo = [data_step_var_system, data_step_unique_system, data_step_mean_var_ud]
                media = original_media
                end_config = time.time()
                if contador == experiments:
                    mM[i][j] = {
                        'alive': np.mean(list_alive_UDs),
                        'lstd': np.std(list_alive_UDs),
                        'time used': end_config - star_configuration,
                        'percentage_extinction': contador / experiments,
                        'tempo': tempo, 
                        'mean': np.mean(list_vivas_puntos_vista, axis=0), 
                        'std': np.std(list_vivas_puntos_vista, axis=0),
                        'growth rate': np.mean([np.mean(lista) for lista in tasas_crecimiento]),
                        'diversity_info': data_inherit_endo,
                        'diversity_info_steps': data_steps_inherit_endo,
                    }
                else:  # Handle extinction-only scenarios. More than the max_iterations
                    mM[i][j] = {
                        'alive': None,
                        'lstd': None,
                        'time used': end_config - star_configuration,
                        'percentage_extinction': 1.0,  # All experiments went extinct
                        'tempo': None, 
                        'mean': None, 
                        'std': None,
                        'growth rate': None,
                        'diversity_info': None,
                        'diversity_info_steps': None,
                    }
                print(f"""
        The total time of the configuration of inherit percentage {inherit} and initial UDs {iniciais} is  {end_config - star_configuration}
                """)
        # Data
        heat_std = os.path.join(folder_name, 'Endo_Initial_UDs.npy')
        np.save(heat_std, mM)
        now = datetime.now()
        finish = time.time()
        print(f"""
        It finished at: {now}
        It lasted {finish-start}
        """)
        print("done")
        heat_std = os.path.join(folder_name, 'Endo_Initial_UDs.npy')
        ## General Data
        EmM_datos = np.load(heat_std, allow_pickle=True)
        plot = transversal_changes(EmM_datos, inherits, Emalphas, 'Endogamy', variable='Initial UDs')
        plot.savefig(os.path.join(folder_name, 'diversity_behavior.png'), dpi=300, bbox_inches="tight")
        plot = transversal_alive(EmM_datos, inherits, Emalphas, 'Endogamy', variable='Initial UDs')
        plot.savefig(os.path.join(folder_name, 'populational_behavior.png'), dpi=300, bbox_inches="tight")
    elif variable == '2':
        #sub folder
        folder_name = os.path.join(folder_name, 'Initial Varieties')
        # Create the sub-folder if it doesn't exist
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
        # This experiment has different values for Initial varieties
        prob_morte = 0.06 #beta
        media = 4 # Mean
        m = 40
        v = 100 # Initial varieties
        inherits = [0,25,50, 'False']
        Evalphas = np.linspace(10,v,int(v/10)) # Initial Varieties: from 10 to v
        # For data of behaviour
        vM = np.empty((len(inherits), len(Evalphas)), dtype=object)
        punto_vista = 50
        tiempo = 1000
        tempo = list(range(0,tiempo+1,punto_vista))
        experiments = 100
        max_iterations = 200
        print(vM.shape)
        start = time.time()
        print(f"started at:  {datetime.now()}")
        for i, inherit in enumerate(inherits):
            for j, varieties  in enumerate(Evalphas):
                star_configuration = time.time()
                #For population dynamics
                list_alive_UDs = []
                list_vivas_puntos_vista = []
                tasas_crecimiento = []
                #For diversity dynamics
                data_step_mean_var_ud = []
                data_step_var_system = []
                data_step_unique_system = []
                print(f"Experiments with inheritance {inherit} Initial UDs {m} and Initial varieties {varieties}")
                #Lists to store experiments' diversity data
                data_endo_mean_ud = []
                data_endo_com_level = []
                data_endo_total_varieties = []
                original_media = media
                contador = 0
                iterations = 0
                while contador < experiments and iterations < max_iterations: 
                #for experiment in range(1, experiments+1):
                    print(f'experimento {contador+1}')
                    if inherit != 'False':
                        #### Initialization
                        UD_endogamy.uds = {}
                        instancias_ud = []
                        for id_ud in range(1, int(m) + 1):
                            instancias_ud.append(UD_endogamy(id_ud, media))
                        ## Varieties
                        limited_varieties = True
                        if limited_varieties == False:
                            for id_ud, ud in UD_endogamy.uds.items():
                                for _ in range(3):
                                    ud.varieties.append(Variety())
                        else:
                            initial_varieties = [Variety() for _ in range (int(varieties))]
                            for ud in UD_endogamy.uds.values():
                                for _ in range(3):
                                    ud.varieties.append(random.choice(initial_varieties))   
                        # Lists for graphs
                        vivas_puntos_vista = [int(m)]
                        vivas_tasa_crecimiento = [int(m)]
                        #For diversity
                        mean_var_ud = []
                        var_system = []
                        unique_system = []
                        var_ud = []
                        var_total = []
                        for ud in [ud for ud in UD_endogamy.uds.values() if ud.activa ==True]:
                            var_ud.append(len(ud.varieties))
                            for variety in ud.varieties:
                                var_total.append(variety.variety_id)
                        mean_var_ud.append(np.mean(var_ud))
                        var_system.append(len(var_total))
                        unique_system.append(len(set(var_total)))
                        # Simulation
                        for t in range(1, tiempo):
                            uds_copy = {id_ud: ud for id_ud, ud in UD_endogamy.uds.items() if ud.activa}
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
                            if not uds_copy: #Extintion
                                # Only 0
                                print(f"acabó en 0 el experimento {contador+1} con herencia {inherits[i]} con unidades {Evalphas[j]}")
                                break         
                            # Cycle:
                            for id_ud, ud in uds_copy.items():
                                ud.ter_filho()
                                ud.buscar_ud(uds_copy, int(media), inherit)
                                ud.incrementar_idade()
                                ud.death_probability(prob_morte)
                            # Collecting data
                            vivas_tasa_crecimiento.append(len([ud for id, ud in uds_copy.items() if ud.activa]))
                            if t % punto_vista == 0:
                                viv = len([ud for id, ud in uds_copy.items() if ud.activa])
                                vivas_puntos_vista.append(viv)
                                # For diversity
                                var_ud = []
                                var_total = []
                                for ud in [ud for ud in UD_endogamy.uds.values() if ud.activa ==True]:
                                    var_ud.append(len(ud.varieties))
                                    for variety in ud.varieties:
                                        var_total.append(variety.variety_id)
                                mean_var_ud.append(np.mean(var_ud))
                                var_system.append(len(var_total))
                                unique_system.append(len(set(var_total))) 
                        viv = len([ud for id, ud in UD_endogamy.uds.items() if ud.activa])
                        vivas_puntos_vista.append(viv)
                        # For diversity
                        var_ud = []
                        var_total = []
                        for ud in [ud for ud in UD_endogamy.uds.values() if ud.activa ==True]:
                            var_ud.append(len(ud.varieties))
                            for variety in ud.varieties:
                                var_total.append(variety.variety_id)
                        mean_var_ud.append(np.mean(var_ud))
                        var_system.append(len(var_total))
                        unique_system.append(len(set(var_total)))
                        alive = (len([ud for id, ud in uds_copy.items() if ud.activa]))
                        if alive >= 1:   
                            total_varieties = []
                            varieties_per_UD = []
                            for ud in [ud for ud in UD_endogamy.uds.values() if ud.activa ==True]:
                                varieties_per_UD.append(len(ud.varieties))
                                for variety in ud.varieties:
                                    total_varieties.append(variety.variety_id)
                            data_endo_mean_ud.append(np.mean(varieties_per_UD))
                            data_endo_com_level.append(len(set(total_varieties)))
                            data_endo_total_varieties.append(total_varieties)
                    
                    else:# Now with inherit == False
                        #### Initialization
                        UD_endogamy_al_inh.uds = {}
                        instancias_ud = []
                        for id_ud in range(1, int(m) + 1):
                            instancias_ud.append(UD_endogamy_al_inh(id_ud, media))
                        ## Varieties
                        limited_varieties = True
                        if limited_varieties == False:
                            for id_ud, ud in UD_endogamy_al_inh.uds.items():
                                for _ in range(3):
                                    ud.varieties.append(Variety())
                        else:
                            initial_varieties = [Variety() for _ in range (int(varieties))]
                            for ud in UD_endogamy_al_inh.uds.values():
                                for _ in range(3):
                                    ud.varieties.append(random.choice(initial_varieties))   
                        # Lists for graphs
                        vivas_puntos_vista = [int(m)]
                        vivas_tasa_crecimiento = [int(m)]
                        #For diversity
                        mean_var_ud = []
                        var_system = []
                        unique_system = []
                        var_ud = []
                        var_total = []
                        for ud in [ud for ud in UD_endogamy_al_inh.uds.values() if ud.activa ==True]:
                            var_ud.append(len(ud.varieties))
                            for variety in ud.varieties:
                                var_total.append(variety.variety_id)
                        mean_var_ud.append(np.mean(var_ud))
                        var_system.append(len(var_total))
                        unique_system.append(len(set(var_total)))
                        # Simulation
                        for t in range(1, tiempo):
                            uds_copy = {id_ud: ud for id_ud, ud in UD_endogamy_al_inh.uds.items() if ud.activa}
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
                            if not uds_copy: #Extintion
                                # Only 0
                                print(f"acabó en 0 el experimento {contador+1} con herencia {inherits[i]} con unidades {Evalphas[j]}")
                                break         
                            # Cycle:
                            varieties_list = [var for ud in uds_copy.values() for var in ud.varieties]
                            for id_ud, ud in uds_copy.items():
                                ud.ter_filho()
                                ud.buscar_ud(uds_copy, int(media), varieties_list, 3)
                                ud.incrementar_idade()
                                ud.death_probability(prob_morte)
                            # Collecting data
                            vivas_tasa_crecimiento.append(len([ud for id, ud in uds_copy.items() if ud.activa]))
                            if t % punto_vista == 0:
                                viv = len([ud for id, ud in uds_copy.items() if ud.activa])
                                vivas_puntos_vista.append(viv)
                                # For diversity
                                var_ud = []
                                var_total = []
                                for ud in [ud for ud in UD_endogamy_al_inh.uds.values() if ud.activa ==True]:
                                    var_ud.append(len(ud.varieties))
                                    for variety in ud.varieties:
                                        var_total.append(variety.variety_id)
                                mean_var_ud.append(np.mean(var_ud))
                                var_system.append(len(var_total))
                                unique_system.append(len(set(var_total))) 
                        viv = len([ud for id, ud in UD_endogamy_al_inh.uds.items() if ud.activa])
                        vivas_puntos_vista.append(viv)
                        # For diversity
                        var_ud = []
                        var_total = []
                        for ud in [ud for ud in UD_endogamy_al_inh.uds.values() if ud.activa ==True]:
                            var_ud.append(len(ud.varieties))
                            for variety in ud.varieties:
                                var_total.append(variety.variety_id)
                        mean_var_ud.append(np.mean(var_ud))
                        var_system.append(len(var_total))
                        unique_system.append(len(set(var_total)))
                        alive = (len([ud for id, ud in uds_copy.items() if ud.activa]))
                        if alive >= 1:   
                            total_varieties = []
                            varieties_per_UD = []
                            for ud in [ud for ud in UD_endogamy_al_inh.uds.values() if ud.activa ==True]:
                                varieties_per_UD.append(len(ud.varieties))
                                for variety in ud.varieties:
                                    total_varieties.append(variety.variety_id)
                            data_endo_mean_ud.append(np.mean(varieties_per_UD))
                            data_endo_com_level.append(len(set(total_varieties)))
                            data_endo_total_varieties.append(total_varieties)
                    # Final collection of the data after the simulation!
                    if len(uds_copy) > 0:  # Only collect data if the system is alive
                        list_alive_UDs.append(len([ud for id, ud in uds_copy.items() if ud.activa == True]))  # For heatmap
                        list_vivas_puntos_vista.append(vivas_puntos_vista)
                        data_step_var_system.append(var_system)
                        data_step_unique_system.append(unique_system)
                        data_step_mean_var_ud.append(mean_var_ud)
                        contador += 1
                    iterations += 1
                    print('succesful', contador)
                    print('iterations', iterations)
                    
                    data_inherit_endo = [data_endo_mean_ud, data_endo_com_level, data_endo_total_varieties]
                data_steps_inherit_endo = [data_step_var_system, data_step_unique_system, data_step_mean_var_ud]
                media = original_media
                end_config = time.time()
                if contador == experiments:
                    vM[i][j] = {
                        'alive': np.mean(list_alive_UDs),
                        'lstd': np.std(list_alive_UDs),
                        'time used': end_config - star_configuration,
                        'percentage_extinction': contador / experiments,
                        'tempo': tempo, 
                        'mean': np.mean(list_vivas_puntos_vista, axis=0), 
                        'std': np.std(list_vivas_puntos_vista, axis=0),
                        'growth rate': np.mean([np.mean(lista) for lista in tasas_crecimiento]),
                        'diversity_info': data_inherit_endo,
                        'diversity_info_steps': data_steps_inherit_endo,
                    }
                else:  # Handle extinction-only scenarios
                    vM[i][j] = {
                        'alive': None,
                        'lstd': None,
                        'time used': end_config - star_configuration,
                        'percentage_extinction': 1.0,  # All experiments went extinct
                        'tempo': None, 
                        'mean': None, 
                        'std': None,
                        'growth rate': None,
                        'diversity_info': None,
                        'diversity_info_steps': None,
                    }
                print(f"""
        The total time of the configuration of inherit percentage {inherit}, 
        initial UDs {m} and Initial varieties {varieties} is  {end_config - star_configuration}
                """)
        # Heatmap and std
        heat_std = os.path.join(folder_name, 'Endo_Initial_Varieties.npy')
        np.save(heat_std, vM)
        now = datetime.now()
        finish = time.time()
        print(f"""
        It finished at: {now}
        It lasted {finish-start}
        """)
        print("done")
        heat_std = os.path.join(folder_name, 'Endo_Initial_Varieties.npy')
        ## heatmap and mean
        EvM_datos = np.load(heat_std, allow_pickle=True)
        plot = transversal_changes(EvM_datos, inherits, Evalphas, 'Endogamy', variable='Initial Varieties')
        plot.savefig(os.path.join(folder_name, 'diversity_behavior.png'), dpi=300, bbox_inches="tight")
        plot = transversal_alive(EvM_datos, inherits, Evalphas, 'Endogamy', variable='Initial Varieties')
        plot.savefig(os.path.join(folder_name, 'populational_behavior.png'), dpi=300, bbox_inches="tight")
    elif variable == '3':
        #sub folder
        folder_name = os.path.join(folder_name, 'Mean of children by UD')
        # Create the sub-folder if it doesn't exist
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
        # This experiment has different values for Mean of children
        prob_morte = 0.06 #beta
        n = 10 # Mean
        m = 40 # Initial UDs
        inherits = [0,25,50, 'False']
        Ecalphas = np.linspace(1,n,n) # Mean of children from 1 to n
        # For data of behaviour
        cM = np.empty((len(inherits), len(Ecalphas)), dtype=object) 
        punto_vista = 50
        tiempo = 1000
        tempo = list(range(0,tiempo+1,punto_vista))
        experiments = 100
        max_iterations = 200
        #print(cM.shape)
        start = time.time()
        print(f"started at:  {datetime.now()}")
        for i, inherit in enumerate(inherits):
            for j, media  in enumerate(Ecalphas):
                star_configuration = time.time()
                #For population dynamics
                list_alive_UDs = []
                list_vivas_puntos_vista = []
                tasas_crecimiento = []
                #For diversity dynamics
                data_step_mean_var_ud = []
                data_step_var_system = []
                data_step_unique_system = []
                print(f"Experiments with inheritance {inherit} and Mean of Children {media}")
                #Lists to store experiments' diversity data
                data_endo_mean_ud = []
                data_endo_com_level = []
                data_endo_total_varieties = []
                original_media = media
                #To see how frequent goes to extintion
                contador = 0
                iterations = 0
                while contador < experiments and iterations < max_iterations: 
                    print(f'experimento {contador+1}')
                    if inherit != 'False':
                        #### Initialization
                        UD_endogamy.uds = {}
                        instancias_ud = []
                        for id_ud in range(1, int(m) + 1):
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
                        vivas_puntos_vista = [int(m)]
                        vivas_tasa_crecimiento = [int(m)]
                #             mortas_puntos_vista = [0]
                        #For diversity
                        mean_var_ud = []
                        var_system = []
                        unique_system = []
                        var_ud = []
                        var_total = []
                        for ud in [ud for ud in UD_endogamy.uds.values() if ud.activa ==True]:
                            var_ud.append(len(ud.varieties))
                            for variety in ud.varieties:
                                var_total.append(variety.variety_id)
                        mean_var_ud.append(np.mean(var_ud))
                        var_system.append(len(var_total))
                        unique_system.append(len(set(var_total)))
                        # Simulation
                        for t in range(1, tiempo):
                            uds_copy = {id_ud: ud for id_ud, ud in UD_endogamy.uds.items() if ud.activa}
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
                            if not uds_copy: #Extintion
                                # Only 0
                                print(f"acabó en 0 el experimento {contador+1} con herencia {inherits[i]} con mean {Ecalphas[j]}")
                                break         
                            # Cycle:
                            for id_ud, ud in uds_copy.items():
                                ud.ter_filho()
                                ud.buscar_ud(uds_copy, int(media), inherit)
                                ud.incrementar_idade()
                                ud.death_probability(prob_morte)
                            # Collecting data
                            vivas_tasa_crecimiento.append(len([ud for id, ud in uds_copy.items() if ud.activa]))
                            if t % punto_vista == 0:
                                viv = len([ud for id, ud in uds_copy.items() if ud.activa])
                                #mort = len([ud for id, ud in uds_copy.items() if not ud.activa])
                                vivas_puntos_vista.append(viv)
                                # For diversity
                                var_ud = []
                                var_total = []
                                for ud in [ud for ud in UD_endogamy.uds.values() if ud.activa ==True]:
                                    var_ud.append(len(ud.varieties))
                                    for variety in ud.varieties:
                                        var_total.append(variety.variety_id)
                                mean_var_ud.append(np.mean(var_ud))
                                var_system.append(len(var_total))
                                unique_system.append(len(set(var_total))) 
                        viv = len([ud for id, ud in UD_endogamy.uds.items() if ud.activa])
                        vivas_puntos_vista.append(viv)
                        # For diversity
                        var_ud = []
                        var_total = []
                        for ud in [ud for ud in UD_endogamy.uds.values() if ud.activa ==True]:
                            var_ud.append(len(ud.varieties))
                            for variety in ud.varieties:
                                var_total.append(variety.variety_id)
                        mean_var_ud.append(np.mean(var_ud))
                        var_system.append(len(var_total))
                        unique_system.append(len(set(var_total)))
                        alive = (len([ud for id, ud in uds_copy.items() if ud.activa]))
                        if alive >= 1:   
                            total_varieties = []
                            varieties_per_UD = []
                            for ud in [ud for ud in UD_endogamy.uds.values() if ud.activa ==True]:
                                varieties_per_UD.append(len(ud.varieties))
                                for variety in ud.varieties:
                                    total_varieties.append(variety.variety_id)
                            data_endo_mean_ud.append(np.mean(varieties_per_UD))
                            data_endo_com_level.append(len(set(total_varieties)))
                            data_endo_total_varieties.append(total_varieties)
                    
                    else:# Now with inherit == False
                        #### Initialization
                        UD_endogamy_al_inh.uds = {}
                        instancias_ud = []
                        for id_ud in range(1, int(m) + 1):
                            instancias_ud.append(UD_endogamy_al_inh(id_ud, media))
                        ## Varieties
                        limited_varieties = True
                        if limited_varieties == False:
                            for id_ud, ud in UD_endogamy_al_inh.uds.items():
                                for _ in range(3):
                                    ud.varieties.append(Variety())
                        else:
                            initial_varieties = [Variety() for _ in range (10)]
                            for ud in UD_endogamy_al_inh.uds.values():
                                for _ in range(3):
                                    ud.varieties.append(random.choice(initial_varieties))   
                        # Lists for graphs
                        vivas_puntos_vista = [int(m)]
                        vivas_tasa_crecimiento = [int(m)]
                #             mortas_puntos_vista = [0]
                        #For diversity
                        mean_var_ud = []
                        var_system = []
                        unique_system = []
                        var_ud = []
                        var_total = []
                        for ud in [ud for ud in UD_endogamy_al_inh.uds.values() if ud.activa ==True]:
                            var_ud.append(len(ud.varieties))
                            for variety in ud.varieties:
                                var_total.append(variety.variety_id)
                        mean_var_ud.append(np.mean(var_ud))
                        var_system.append(len(var_total))
                        unique_system.append(len(set(var_total)))
                        # Simulation
                        for t in range(1, tiempo):
                            uds_copy = {id_ud: ud for id_ud, ud in UD_endogamy_al_inh.uds.items() if ud.activa}
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
                            if not uds_copy: #Extintion
                                # Only 0
                                print(f"acabó en 0 el experimento {contador+1} con herencia {inherits[i]} con mean {Ecalphas[j]}")
                                break         
                            # Cycle:
                            varieties_list = [var for ud in uds_copy.values() for var in ud.varieties]
                            for id_ud, ud in uds_copy.items():
                                ud.ter_filho()
                                ud.buscar_ud(uds_copy, int(media), varieties_list, 3)
                                ud.incrementar_idade()
                                ud.death_probability(prob_morte)
                            # Collecting data
                            vivas_tasa_crecimiento.append(len([ud for id, ud in uds_copy.items() if ud.activa]))
                            if t % punto_vista == 0:
                                viv = len([ud for id, ud in uds_copy.items() if ud.activa])
                                #mort = len([ud for id, ud in uds_copy.items() if not ud.activa])
                                vivas_puntos_vista.append(viv)
                                # For diversity
                                var_ud = []
                                var_total = []
                                for ud in [ud for ud in UD_endogamy_al_inh.uds.values() if ud.activa ==True]:
                                    var_ud.append(len(ud.varieties))
                                    for variety in ud.varieties:
                                        var_total.append(variety.variety_id)
                                mean_var_ud.append(np.mean(var_ud))
                                var_system.append(len(var_total))
                                unique_system.append(len(set(var_total))) 
                        viv = len([ud for id, ud in UD_endogamy_al_inh.uds.items() if ud.activa])
                        vivas_puntos_vista.append(viv)
                        # For diversity
                        var_ud = []
                        var_total = []
                        for ud in [ud for ud in UD_endogamy_al_inh.uds.values() if ud.activa ==True]:
                            var_ud.append(len(ud.varieties))
                            for variety in ud.varieties:
                                var_total.append(variety.variety_id)
                        mean_var_ud.append(np.mean(var_ud))
                        var_system.append(len(var_total))
                        unique_system.append(len(set(var_total)))
                        alive = (len([ud for id, ud in uds_copy.items() if ud.activa]))
                        if alive >= 1:   
                            total_varieties = []
                            varieties_per_UD = []
                            for ud in [ud for ud in UD_endogamy_al_inh.uds.values() if ud.activa ==True]:
                                varieties_per_UD.append(len(ud.varieties))
                                for variety in ud.varieties:
                                    total_varieties.append(variety.variety_id)
                            data_endo_mean_ud.append(np.mean(varieties_per_UD))
                            data_endo_com_level.append(len(set(total_varieties)))
                            data_endo_total_varieties.append(total_varieties)
                    
                    
                    # Final collection of the data after the simulation!
                    if len(uds_copy) > 0:  # Only collect data if the system is alive
                        list_alive_UDs.append(len([ud for id, ud in uds_copy.items() if ud.activa == True]))  # For heatmap
                        list_vivas_puntos_vista.append(vivas_puntos_vista)
                        data_step_var_system.append(var_system)
                        data_step_unique_system.append(unique_system)
                        data_step_mean_var_ud.append(mean_var_ud)
                        contador += 1
                    iterations += 1
                    print('succesful', contador)
                    print('iterations', iterations) 
                    
                    data_inherit_endo = [data_endo_mean_ud, data_endo_com_level, data_endo_total_varieties]
                data_steps_inherit_endo = [data_step_var_system, data_step_unique_system, data_step_mean_var_ud]
                media = original_media
                end_config = time.time()
                if contador == experiments: 
                    cM[i][j] = {
                        'alive': np.mean(list_alive_UDs),
                        'lstd': np.std(list_alive_UDs),
                        'time used': end_config - star_configuration,
                        'percentage_extinction': contador / experiments,
                        'tempo': tempo, 
                        'mean': np.mean(list_vivas_puntos_vista, axis=0), 
                        'std': np.std(list_vivas_puntos_vista, axis=0),
                        'growth rate': np.mean([np.mean(lista) for lista in tasas_crecimiento]),
                        'diversity_info': data_inherit_endo,
                        'diversity_info_steps': data_steps_inherit_endo,
                    }
                else:  # Handle extinction-only scenarios
                    cM[i][j] = {
                        'alive': None,
                        'lstd': None,
                        'time used': end_config - star_configuration,
                        'percentage_extinction': 1.0,  # All experiments went extinct
                        'tempo': None, 
                        'mean': None, 
                        'std': None,
                        'growth rate': None,
                        'diversity_info': None,
                        'diversity_info_steps': None,
                    }
                print(f"""
        The total time of the configuration of inherit percentage {inherit} and initial UDs {m} and mean {media} is  {end_config - star_configuration}
                """)
        # Folder
        heat_std = os.path.join(folder_name, 'Endo_Mean_children.npy')
        np.save(heat_std, cM)
        now = datetime.now()
        finish = time.time()
        print(f"""
        It finished at: {now}
        It lasted {finish-start}
        """)
        print("done")
        heat_std = os.path.join(folder_name, 'Endo_Mean_children.npy')
        ## General Data
        EcM_datos = np.load(heat_std, allow_pickle=True)
        plot =transversal_changes(EcM_datos, inherits, Ecalphas, 'Endogamy', variable='Mean of children')
        plot.savefig(os.path.join(folder_name, 'diversity_behavior.png'), dpi=300, bbox_inches="tight")
        plot = transversal_alive(EcM_datos, inherits, Ecalphas, 'Endogamy', variable='Mean of children')
        plot.savefig(os.path.join(folder_name, 'populational_behavior.png'), dpi=300, bbox_inches="tight")
    else:
        #sub folder
        folder_name = os.path.join(folder_name, 'Number of varieties for UD')
        # Create the sub-folder if it doesn't exist
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
        # This experiment has different values for Initial varieties mv
        prob_morte = 0.06 #beta
        media = 4 # Mean
        m = 40
        mv = 10
        inherits = [0,25,50, 'False']
        Emvalphas = np.linspace(1,mv,mv)# Mean varieties from 1 to mv
        # For data of behaviour
        vM = np.empty((len(inherits), len(Emvalphas)), dtype=object) 
        punto_vista = 50
        tiempo = 1000
        tempo = list(range(0,tiempo+1,punto_vista))
        experiments = 100
        max_iterations = 200
        print(vM.shape)
        start = time.time()
        print(f"started at:  {datetime.now()}")
        for i, inherit in enumerate(inherits):
            for j, mvarieties  in enumerate(Emvalphas):
                star_configuration = time.time()
                #For population dynamics
                list_alive_UDs = []
                list_vivas_puntos_vista = []
                tasas_crecimiento = []
                #For diversity dynamics
                data_step_mean_var_ud = []
                data_step_var_system = []
                data_step_unique_system = []
                print(f"Experiments with inheritance {inherit} Initial UDs {m} and Mean varieties {mvarieties}")
                #Lists to store experiments' diversity data
                data_endo_mean_ud = []
                data_endo_com_level = []
                data_endo_total_varieties = []
                original_media = media
                contador = 0
                iterations = 0
                while contador < experiments and iterations < max_iterations: 
                    print(f'experimento {contador+1}')
                    if inherit != 'False':
                        
                        #### Initialization
                        UD_endogamy.uds = {}
                        instancias_ud = []
                        for id_ud in range(1, int(m) + 1):
                            instancias_ud.append(UD_endogamy(id_ud, media))
                        ## Varieties
                        limited_varieties = True
                        if limited_varieties == False:
                            for id_ud, ud in UD_endogamy.uds.items():
                                for _ in range(3):
                                    ud.varieties.append(Variety())
                        else:
                            initial_varieties = [Variety() for _ in range (int(10))]
                            for ud in UD_endogamy.uds.values():
                                for _ in range(int(mvarieties)):
                                    ud.varieties.append(random.choice(initial_varieties))   
                        # Lists for graphs
                        vivas_puntos_vista = [int(m)]
                        vivas_tasa_crecimiento = [int(m)]
                        #For diversity
                        mean_var_ud = []
                        var_system = []
                        unique_system = []
                        var_ud = []
                        var_total = []
                        for ud in [ud for ud in UD_endogamy.uds.values() if ud.activa ==True]:
                            var_ud.append(len(ud.varieties))
                            for variety in ud.varieties:
                                var_total.append(variety.variety_id)
                        mean_var_ud.append(np.mean(var_ud))
                        var_system.append(len(var_total))
                        unique_system.append(len(set(var_total)))
                        # Simulation
                        for t in range(1, tiempo):
                            uds_copy = {id_ud: ud for id_ud, ud in UD_endogamy.uds.items() if ud.activa}
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
                            if not uds_copy: #Extintion
                                # Only 0
                                print(f"acabó en 0 el experimento {contador+1} con herencia {inherits[i]} con unidades {Emvalphas[j]}")
                                break         
                            # Cycle:
                            for id_ud, ud in uds_copy.items():
                                ud.ter_filho()
                                ud.buscar_ud(uds_copy, int(media), inherit)
                                ud.incrementar_idade()
                                ud.death_probability(prob_morte)
                            # Collecting data
                            vivas_tasa_crecimiento.append(len([ud for id, ud in uds_copy.items() if ud.activa]))
                            if t % punto_vista == 0:
                                viv = len([ud for id, ud in uds_copy.items() if ud.activa])
                                vivas_puntos_vista.append(viv)
                                # For diversity
                                var_ud = []
                                var_total = []
                                for ud in [ud for ud in UD_endogamy.uds.values() if ud.activa ==True]:
                                    var_ud.append(len(ud.varieties))
                                    for variety in ud.varieties:
                                        var_total.append(variety.variety_id)
                                mean_var_ud.append(np.mean(var_ud))
                                var_system.append(len(var_total))
                                unique_system.append(len(set(var_total))) 
                        viv = len([ud for id, ud in UD_endogamy.uds.items() if ud.activa])
                        vivas_puntos_vista.append(viv)
                        # For diversity
                        var_ud = []
                        var_total = []
                        for ud in [ud for ud in UD_endogamy.uds.values() if ud.activa ==True]:
                            var_ud.append(len(ud.varieties))
                            for variety in ud.varieties:
                                var_total.append(variety.variety_id)
                        mean_var_ud.append(np.mean(var_ud))
                        var_system.append(len(var_total))
                        unique_system.append(len(set(var_total)))
                        alive = (len([ud for id, ud in uds_copy.items() if ud.activa]))
                        if alive >= 1:   
                            total_varieties = []
                            varieties_per_UD = []
                            for ud in [ud for ud in UD_endogamy.uds.values() if ud.activa ==True]:
                                varieties_per_UD.append(len(ud.varieties))
                                for variety in ud.varieties:
                                    total_varieties.append(variety.variety_id)
                            data_endo_mean_ud.append(np.mean(varieties_per_UD))
                            data_endo_com_level.append(len(set(total_varieties)))
                            data_endo_total_varieties.append(total_varieties)
                    else:# Now with inherit == False
                        #### Initialization
                        UD_endogamy_al_inh.uds = {}
                        instancias_ud = []
                        for id_ud in range(1, int(m) + 1):
                            instancias_ud.append(UD_endogamy_al_inh(id_ud, media))
                        ## Varieties
                        limited_varieties = True
                        if limited_varieties == False:
                            for id_ud, ud in UD_endogamy_al_inh.uds.items():
                                for _ in range(3):
                                    ud.varieties.append(Variety())
                        else:
                            initial_varieties = [Variety() for _ in range (int(10))]
                            for ud in UD_endogamy_al_inh.uds.values():
                                for _ in range(int(mvarieties)):
                                    ud.varieties.append(random.choice(initial_varieties))   
                        # Lists for graphs
                        vivas_puntos_vista = [int(m)]
                        vivas_tasa_crecimiento = [int(m)]
                        #For diversity
                        mean_var_ud = []
                        var_system = []
                        unique_system = []
                        var_ud = []
                        var_total = []
                        for ud in [ud for ud in UD_endogamy_al_inh.uds.values() if ud.activa ==True]:
                            var_ud.append(len(ud.varieties))
                            for variety in ud.varieties:
                                var_total.append(variety.variety_id)
                        mean_var_ud.append(np.mean(var_ud))
                        var_system.append(len(var_total))
                        unique_system.append(len(set(var_total)))
                        # Simulation
                        for t in range(1, tiempo):
                            uds_copy = {id_ud: ud for id_ud, ud in UD_endogamy_al_inh.uds.items() if ud.activa}
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
                            if not uds_copy: #Extintion
                                # Only 0
                                print(f"acabó en 0 el experimento {contador+1} con herencia {inherits[i]} con unidades {Emvalphas[j]}")
                                break         
                            # Cycle:
                            varieties_list = [var for ud in uds_copy.values() for var in ud.varieties]
                            for id_ud, ud in uds_copy.items():
                                ud.ter_filho()
                                ud.buscar_ud(uds_copy, int(media), varieties_list, int(mvarieties))
                                ud.incrementar_idade()
                                ud.death_probability(prob_morte)
                            # Collecting data
                            vivas_tasa_crecimiento.append(len([ud for id, ud in uds_copy.items() if ud.activa]))
                            if t % punto_vista == 0:
                                viv = len([ud for id, ud in uds_copy.items() if ud.activa])
                                #mort = len([ud for id, ud in uds_copy.items() if not ud.activa])
                                vivas_puntos_vista.append(viv)
                                # For diversity
                                var_ud = []
                                var_total = []
                                for ud in [ud for ud in UD_endogamy_al_inh.uds.values() if ud.activa ==True]:
                                    var_ud.append(len(ud.varieties))
                                    for variety in ud.varieties:
                                        var_total.append(variety.variety_id)
                                mean_var_ud.append(np.mean(var_ud))
                                var_system.append(len(var_total))
                                unique_system.append(len(set(var_total))) 
                        viv = len([ud for id, ud in UD_endogamy_al_inh.uds.items() if ud.activa])
                        vivas_puntos_vista.append(viv)
                        # For diversity
                        var_ud = []
                        var_total = []
                        for ud in [ud for ud in UD_endogamy_al_inh.uds.values() if ud.activa ==True]:
                            var_ud.append(len(ud.varieties))
                            for variety in ud.varieties:
                                var_total.append(variety.variety_id)
                        mean_var_ud.append(np.mean(var_ud))
                        var_system.append(len(var_total))
                        unique_system.append(len(set(var_total)))
                        alive = (len([ud for id, ud in uds_copy.items() if ud.activa]))
                        if alive >= 1:   
                            total_varieties = []
                            varieties_per_UD = []
                            for ud in [ud for ud in UD_endogamy_al_inh.uds.values() if ud.activa ==True]:
                                varieties_per_UD.append(len(ud.varieties))
                                for variety in ud.varieties:
                                    total_varieties.append(variety.variety_id)
                            data_endo_mean_ud.append(np.mean(varieties_per_UD))
                            data_endo_com_level.append(len(set(total_varieties)))
                            data_endo_total_varieties.append(total_varieties)
                    
                    
                    # Final collection of the data after the simulation!
                    if len(uds_copy) > 0:  # Only collect data if the system is alive
                        list_alive_UDs.append(len([ud for id, ud in uds_copy.items() if ud.activa == True]))  # For heatmap
                        list_vivas_puntos_vista.append(vivas_puntos_vista)
                        data_step_var_system.append(var_system)
                        data_step_unique_system.append(unique_system)
                        data_step_mean_var_ud.append(mean_var_ud)
                        contador += 1
                    iterations += 1
                    print('succesful', contador)
                    print('iterations', iterations) 
                    
                    data_inherit_endo = [data_endo_mean_ud, data_endo_com_level, data_endo_total_varieties]
                data_steps_inherit_endo = [data_step_var_system, data_step_unique_system, data_step_mean_var_ud]
                media = original_media
                end_config = time.time()
                if contador == experiments:
                    vM[i][j] = {
                        'alive': np.mean(list_alive_UDs),
                        'lstd': np.std(list_alive_UDs),
                        'time used': end_config - star_configuration,
                        'percentage_extinction': contador / experiments,
                        'tempo': tempo, 
                        'mean': np.mean(list_vivas_puntos_vista, axis=0), 
                        'std': np.std(list_vivas_puntos_vista, axis=0),
                        'growth rate': np.mean([np.mean(lista) for lista in tasas_crecimiento]),
                        'diversity_info': data_inherit_endo,
                        'diversity_info_steps': data_steps_inherit_endo,
                    }
                else:  # Handle extinction-only scenarios
                    vM[i][j] = {
                        'alive': None,
                        'lstd': None,
                        'time used': end_config - star_configuration,
                        'percentage_extinction': 1.0,  # All experiments went extinct
                        'tempo': None, 
                        'mean': None, 
                        'std': None,
                        'growth rate': None,
                        'diversity_info': None,
                        'diversity_info_steps': None,
                    }
                print(f"""
        The total time of the configuration of inherit percentage {inherit}, 
        initial UDs {m} and Mean varieties {mvarieties} is  {end_config - star_configuration}
                """)
        # Folder
        heat_std = os.path.join(folder_name, 'Endo_Initial_Mean_varieties.npy')
        np.save(heat_std, vM)
        now = datetime.now()
        finish = time.time()
        print(f"""
        It finished at: {now}
        It lasted {finish-start}
        """)
        print("done")
        heat_std = os.path.join(folder_name, 'Endo_Initial_Mean_varieties.npy')
        ## General Data
        EmvM_datos = np.load(heat_std, allow_pickle=True)
        plot = transversal_changes(EmvM_datos, inherits, Emvalphas, 'Endogamy', variable='Mean of varieties')
        plot.savefig(os.path.join(folder_name, 'diversity_behavior.png'), dpi=300, bbox_inches="tight")
        plot = transversal_alive(EmvM_datos, inherits, Emvalphas, 'Endogamy', variable='Mean of varieties')
        plot.savefig(os.path.join(folder_name, 'populational_behavior.png'), dpi=300, bbox_inches="tight")
elif choice == '2':
    print('Ok, lets go with dual organization')
    #sub folder
    folder_name = os.path.join(parent_folder, 'Second experiments', 'Dual Organization')
    # Create the sub-folder if it doesn't exist
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    if variable  == '1':
        #sub folder
        folder_name = os.path.join(folder_name, 'Initial UDs')
        # Create the sub-folder if it doesn't exist
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
        # This experiment has different values for Initial UDs
        prob_morte = 0.06 #beta
        media = 4 # Mean
        m = 100 # Initial UDs
        inherits = [0,25,50, 'False']
        Dmalphas = np.linspace(10,m,int(m/10)) # Initial UDs: from 10 to m
        # For data of behaviour
        mM = np.empty((len(inherits), len(Dmalphas)), dtype=object) 
        punto_vista = 50
        tiempo = 1000
        tempo = list(range(0,tiempo+1,punto_vista))
        experiments = 100
        max_iterations = 400
        print(mM.shape)
        start = time.time()
        print(f"started at:  {datetime.now()}")
        for i, inherit in enumerate(inherits):
            for j, iniciais  in enumerate(Dmalphas):
                star_configuration = time.time()
                #For population dynamics
                list_alive_UDs = []
                list_vivas_puntos_vista = []
                tasas_crecimiento = []
                #For diversity dynamics
                data_step_mean_var_ud = []
                data_step_var_system = []
                data_step_unique_system = []
                print(f"Experiments with inheritance {inherit} and Initial UDs {iniciais}")
                #Lists to store experiments' diversity data
                data_endo_mean_ud = []
                data_endo_com_level = []
                data_endo_total_varieties = []
                original_media = media
                #To see how frequent goes to extintion
                contador = 0
                iterations = 0
                while contador < experiments and iterations < max_iterations: 
                #for experiment in range(1, experiments+1):
                    print(f'experimento {contador+1}')
                    ## Clans
                    clans = (list(range(1, 2 + 1)) * (int(iniciais) // 2)) # Just 2 clans
                    random.shuffle(clans)
                    if inherit != 'False':          
                        #### Initialization
                        UD_dual_organization.uds = {}
                        instancias_ud = []
                        for id_ud in range(1, int(iniciais) + 1):
                            instancias_ud.append(UD_dual_organization(id_ud, media,clans.pop()))
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
                        #For diversity
                        mean_var_ud = []
                        var_system = []
                        unique_system = []
                        var_ud = []
                        var_total = []
                        for ud in [ud for ud in UD_dual_organization.uds.values() if ud.activa ==True]:
                            var_ud.append(len(ud.varieties))
                            for variety in ud.varieties:
                                var_total.append(variety.variety_id)
                        mean_var_ud.append(np.mean(var_ud))
                        var_system.append(len(var_total))
                        unique_system.append(len(set(var_total)))
                        # Simulation
                        for t in range(1, tiempo):
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
                            if not uds_copy: #Extintion
                                # Only 0
                                print(f"acabó en 0 el experimento {contador+1} con herencia {inherits[i]} con unidades {Dmalphas[j]}")
                                break         
                            # Cycle:
                            for id_ud, ud in uds_copy.items():
                                ud.ter_filho()
                                ud.buscar_ud(uds_copy, int(media), inherit, True, 0.2)
                                ud.incrementar_idade()
                                ud.death_probability(prob_morte)
                            # Collecting data
                            vivas_tasa_crecimiento.append(len([ud for id, ud in uds_copy.items() if ud.activa]))
                            if t % punto_vista == 0:
                                viv = len([ud for id, ud in uds_copy.items() if ud.activa])
                                vivas_puntos_vista.append(viv)
                                # For diversity
                                var_ud = []
                                var_total = []
                                for ud in [ud for ud in UD_dual_organization.uds.values() if ud.activa ==True]:
                                    var_ud.append(len(ud.varieties))
                                    for variety in ud.varieties:
                                        var_total.append(variety.variety_id)
                                mean_var_ud.append(np.mean(var_ud))
                                var_system.append(len(var_total))
                                unique_system.append(len(set(var_total))) 
                        viv = len([ud for id, ud in UD_dual_organization.uds.items() if ud.activa])
                        vivas_puntos_vista.append(viv)
                        # For diversity
                        var_ud = []
                        var_total = []
                        for ud in [ud for ud in UD_dual_organization.uds.values() if ud.activa ==True]:
                            var_ud.append(len(ud.varieties))
                            for variety in ud.varieties:
                                var_total.append(variety.variety_id)
                        mean_var_ud.append(np.mean(var_ud))
                        var_system.append(len(var_total))
                        unique_system.append(len(set(var_total)))
                        alive = (len([ud for id, ud in uds_copy.items() if ud.activa]))
                        if alive >= 1:   
                            total_varieties = []
                            varieties_per_UD = []
                            for ud in [ud for ud in UD_dual_organization.uds.values() if ud.activa ==True]:
                                varieties_per_UD.append(len(ud.varieties))
                                for variety in ud.varieties:
                                    total_varieties.append(variety.variety_id)
                            data_endo_mean_ud.append(np.mean(varieties_per_UD))
                            data_endo_com_level.append(len(set(total_varieties)))
                            data_endo_total_varieties.append(total_varieties)
                    else:# Now with inherit == False
                        #### Initialization
                        UD_dual_organization_al_inh.uds = {}
                        instancias_ud = []
                        for id_ud in range(1, int(iniciais) + 1):
                            instancias_ud.append(UD_dual_organization_al_inh(id_ud, media, clans.pop()))
                        ## Varieties
                        limited_varieties = True
                        if limited_varieties == False:
                            for id_ud, ud in UD_dual_organization_al_inh.uds.items():
                                for _ in range(3):
                                    ud.varieties.append(Variety())
                        else:
                            initial_varieties = [Variety() for _ in range (10)]
                            for ud in UD_dual_organization_al_inh.uds.values():
                                for _ in range(3):
                                    ud.varieties.append(random.choice(initial_varieties))   
                        # Lists for graphs
                        vivas_puntos_vista = [int(iniciais)]
                        vivas_tasa_crecimiento = [int(iniciais)]
                        #For diversity
                        mean_var_ud = []
                        var_system = []
                        unique_system = []
                        var_ud = []
                        var_total = []
                        for ud in [ud for ud in UD_dual_organization_al_inh.uds.values() if ud.activa ==True]:
                            var_ud.append(len(ud.varieties))
                            for variety in ud.varieties:
                                var_total.append(variety.variety_id)
                        mean_var_ud.append(np.mean(var_ud))
                        var_system.append(len(var_total))
                        unique_system.append(len(set(var_total)))
                        # Simulation
                        for t in range(1, tiempo):
                            uds_copy = {id_ud: ud for id_ud, ud in UD_dual_organization_al_inh.uds.items() if ud.activa}
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
                            if not uds_copy: #Extintion
                                # Only 0
                                print(f"acabó en 0 el experimento {contador+1} con herencia {inherits[i]} con unidades {Dmalphas[j]}")
                                break         
                            # Cycle:
                            varieties_list = [var for ud in uds_copy.values() for var in ud.varieties]
                            for id_ud, ud in uds_copy.items():
                                ud.ter_filho()
                                ud.buscar_ud(uds_copy, int(media), varieties_list, True, 3, 0.2)
                                ud.incrementar_idade()
                                ud.death_probability(prob_morte)
                            # Collecting data
                            vivas_tasa_crecimiento.append(len([ud for id, ud in uds_copy.items() if ud.activa]))
                            if t % punto_vista == 0:
                                viv = len([ud for id, ud in uds_copy.items() if ud.activa])
                                vivas_puntos_vista.append(viv)
                                # For diversity
                                var_ud = []
                                var_total = []
                                for ud in [ud for ud in UD_dual_organization_al_inh.uds.values() if ud.activa ==True]:
                                    var_ud.append(len(ud.varieties))
                                    for variety in ud.varieties:
                                        var_total.append(variety.variety_id)
                                mean_var_ud.append(np.mean(var_ud))
                                var_system.append(len(var_total))
                                unique_system.append(len(set(var_total))) 
                        viv = len([ud for id, ud in UD_dual_organization_al_inh.uds.items() if ud.activa])
                        vivas_puntos_vista.append(viv)
                        # For diversity
                        var_ud = []
                        var_total = []
                        for ud in [ud for ud in UD_dual_organization_al_inh.uds.values() if ud.activa ==True]:
                            var_ud.append(len(ud.varieties))
                            for variety in ud.varieties:
                                var_total.append(variety.variety_id)
                        mean_var_ud.append(np.mean(var_ud))
                        var_system.append(len(var_total))
                        unique_system.append(len(set(var_total)))
                        alive = (len([ud for id, ud in uds_copy.items() if ud.activa]))
                        if alive >= 1:   
                            total_varieties = []
                            varieties_per_UD = []
                            for ud in [ud for ud in UD_dual_organization_al_inh.uds.values() if ud.activa ==True]:
                                varieties_per_UD.append(len(ud.varieties))
                                for variety in ud.varieties:
                                    total_varieties.append(variety.variety_id)
                            data_endo_mean_ud.append(np.mean(varieties_per_UD))
                            data_endo_com_level.append(len(set(total_varieties)))
                            data_endo_total_varieties.append(total_varieties)
                    # Final collection of the data after the simulation!
                    if len(uds_copy) > 0:  # Only collect data if the system is alive
                        list_alive_UDs.append(len([ud for id, ud in uds_copy.items() if ud.activa == True]))  # For heatmap
                        list_vivas_puntos_vista.append(vivas_puntos_vista)
                        data_step_var_system.append(var_system)
                        data_step_unique_system.append(unique_system)
                        data_step_mean_var_ud.append(mean_var_ud)
                        contador += 1
                    iterations += 1
                    print('succesful', contador)
                    print('iterations', iterations)   
                    
                    data_inherit_endo = [data_endo_mean_ud, data_endo_com_level, data_endo_total_varieties]
                data_steps_inherit_endo = [data_step_var_system, data_step_unique_system, data_step_mean_var_ud]
                media = original_media
                end_config = time.time()
                if contador == experiments:
                    mM[i][j] = {
                        'alive': np.mean(list_alive_UDs),
                        'lstd': np.std(list_alive_UDs),
                        'time used': end_config - star_configuration,
                        'percentage_extinction': contador / experiments,
                        'tempo': tempo, 
                        'mean': np.mean(list_vivas_puntos_vista, axis=0), 
                        'std': np.std(list_vivas_puntos_vista, axis=0),
                        'growth rate': np.mean([np.mean(lista) for lista in tasas_crecimiento]),
                        'diversity_info': data_inherit_endo,
                        'diversity_info_steps': data_steps_inherit_endo,
                    }
                else:  # Handle extinction-only scenarios
                    mM[i][j] = {
                        'alive': None,
                        'lstd': None,
                        'time used': end_config - star_configuration,
                        'percentage_extinction': 1.0,  # All experiments went extinct
                        'tempo': None, 
                        'mean': None, 
                        'std': None,
                        'growth rate': None,
                        'diversity_info': None,
                        'diversity_info_steps': None,
                    }
                print(f"""
        The total time of the configuration of inherit percentage {inherit} and initial UDs {iniciais} is  {end_config - star_configuration}
                """)
        # Folder
        # Data
        heat_std = os.path.join(folder_name, 'Dual_Initial_UDs.npy')
        np.save(heat_std, mM)
        now = datetime.now()
        finish = time.time()
        print(f"""
        It finished at: {now}
        It lasted {finish-start}
        """)
        print("done")
        heat_std = os.path.join(folder_name, 'Dual_Initial_UDs.npy')
        DmM_datos = np.load(heat_std, allow_pickle=True)
        plot = transversal_changes(DmM_datos, inherits, Dmalphas, 'Dual Organization', variable='Initial UDs')
        plot.savefig(os.path.join(folder_name, 'diversity_behavior.png'), dpi=300, bbox_inches="tight")
        plot = transversal_alive(DmM_datos, inherits, Dmalphas, 'Dual Organization', variable='Initial UDs')
        plot.savefig(os.path.join(folder_name, 'populational_behavior.png'), dpi=300, bbox_inches="tight")
    elif variable == '2':
        #sub folder
        folder_name = os.path.join(folder_name, 'Initial Varieties')
        # Create the sub-folder if it doesn't exist
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
        # This experiment has different values for Initial varieties VVVV
        prob_morte = 0.06 #beta
        media = 4 # Mean
        iniciais = 40
        v = 100 # Initial varieties
        inherits = [0,25,50, 'False']
        Dvalphas = np.linspace(10,v,int(v/10)) # Initial Varieties: from 10 to v
        # For data of behaviour
        vM = np.empty((len(inherits), len(Dvalphas)), dtype=object)
        punto_vista = 50
        tiempo = 1000
        tempo = list(range(0,tiempo+1,punto_vista))
        experiments = 100
        max_iterations = 400
        print(vM.shape)
        start = time.time()
        print(f"started at:  {datetime.now()}")
        for i, inherit in enumerate(inherits):
            for j, varieties  in enumerate(Dvalphas):
                star_configuration = time.time()
                #For population dynamics
                list_alive_UDs = []
                list_vivas_puntos_vista = []
                tasas_crecimiento = []
                #For diversity dynamics
                data_step_mean_var_ud = []
                data_step_var_system = []
                data_step_unique_system = []
                print(f"Experiments with inheritance {inherit} Initial UDs {iniciais} and Initial varieties {varieties}")
                #Lists to store experiments' diversity data
                data_endo_mean_ud = []
                data_endo_com_level = []
                data_endo_total_varieties = []
                original_media = media
                contador = 0
                iterations = 0
                while contador < experiments and iterations < max_iterations: 
                    print(f'experimento {contador+1}')
                    ## Clans
                    clans = (list(range(1, 2 + 1)) * (int(iniciais) // 2)) # Just 2 clans
                    random.shuffle(clans)
                    if inherit != 'False':    
                        #### Initialization
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
                            initial_varieties = [Variety() for _ in range (int(varieties))]
                            for ud in UD_dual_organization.uds.values():
                                for _ in range(3):
                                    ud.varieties.append(random.choice(initial_varieties))   
                        # Lists for graphs
                        vivas_puntos_vista = [int(iniciais)]
                        vivas_tasa_crecimiento = [int(iniciais)]
                        #For diversity
                        mean_var_ud = []
                        var_system = []
                        unique_system = []
                        var_ud = []
                        var_total = []
                        for ud in [ud for ud in UD_dual_organization.uds.values() if ud.activa ==True]:
                            var_ud.append(len(ud.varieties))
                            for variety in ud.varieties:
                                var_total.append(variety.variety_id)
                        mean_var_ud.append(np.mean(var_ud))
                        var_system.append(len(var_total))
                        unique_system.append(len(set(var_total)))
                        # Simulation
                        for t in range(1, tiempo):
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
                            if not uds_copy: #Extintion
                                # Only 0
                                print(f"acabó en 0 el experimento {contador+1} con herencia {inherits[i]} con unidades {Dvalphas[j]}")
                                break         
                            # Cycle:
                            for id_ud, ud in uds_copy.items():
                                ud.ter_filho()
                                ud.buscar_ud(uds_copy, int(media), inherit, True, 0.2)
                                ud.incrementar_idade()
                                ud.death_probability(prob_morte)
                            # Collecting data
                            vivas_tasa_crecimiento.append(len([ud for id, ud in uds_copy.items() if ud.activa]))
                            if t % punto_vista == 0:
                                viv = len([ud for id, ud in uds_copy.items() if ud.activa])
                                vivas_puntos_vista.append(viv)
                                # For diversity
                                var_ud = []
                                var_total = []
                                for ud in [ud for ud in UD_dual_organization.uds.values() if ud.activa ==True]:
                                    var_ud.append(len(ud.varieties))
                                    for variety in ud.varieties:
                                        var_total.append(variety.variety_id)
                                mean_var_ud.append(np.mean(var_ud))
                                var_system.append(len(var_total))
                                unique_system.append(len(set(var_total))) 
                        viv = len([ud for id, ud in UD_dual_organization.uds.items() if ud.activa])
                        vivas_puntos_vista.append(viv)
                        # For diversity
                        var_ud = []
                        var_total = []
                        for ud in [ud for ud in UD_dual_organization.uds.values() if ud.activa ==True]:
                            var_ud.append(len(ud.varieties))
                            for variety in ud.varieties:
                                var_total.append(variety.variety_id)
                        mean_var_ud.append(np.mean(var_ud))
                        var_system.append(len(var_total))
                        unique_system.append(len(set(var_total)))
                        alive = (len([ud for id, ud in uds_copy.items() if ud.activa]))
                        if alive >= 1:   
                            total_varieties = []
                            varieties_per_UD = []
                            for ud in [ud for ud in UD_dual_organization.uds.values() if ud.activa ==True]:
                                varieties_per_UD.append(len(ud.varieties))
                                for variety in ud.varieties:
                                    total_varieties.append(variety.variety_id)
                            data_endo_mean_ud.append(np.mean(varieties_per_UD))
                            data_endo_com_level.append(len(set(total_varieties)))
                            data_endo_total_varieties.append(total_varieties)
                    else:# Now with inherit == False
                        #### Initialization
                        UD_dual_organization_al_inh.uds = {}
                        instancias_ud = []
                        for id_ud in range(1, int(iniciais) + 1):
                            instancias_ud.append(UD_dual_organization_al_inh(id_ud, media, clans.pop()))
                        ## Varieties
                        limited_varieties = True
                        if limited_varieties == False:
                            for id_ud, ud in UD_dual_organization_al_inh.uds.items():
                                for _ in range(3):
                                    ud.varieties.append(Variety())
                        else:
                            initial_varieties = [Variety() for _ in range (int(varieties))]
                            for ud in UD_dual_organization_al_inh.uds.values():
                                for _ in range(3):
                                    ud.varieties.append(random.choice(initial_varieties))   
                        # Lists for graphs
                        vivas_puntos_vista = [int(iniciais)]
                        vivas_tasa_crecimiento = [int(iniciais)]
                        #For diversity
                        mean_var_ud = []
                        var_system = []
                        unique_system = []
                        var_ud = []
                        var_total = []
                        for ud in [ud for ud in UD_dual_organization_al_inh.uds.values() if ud.activa ==True]:
                            var_ud.append(len(ud.varieties))
                            for variety in ud.varieties:
                                var_total.append(variety.variety_id)
                        mean_var_ud.append(np.mean(var_ud))
                        var_system.append(len(var_total))
                        unique_system.append(len(set(var_total)))
                        # Simulation
                        for t in range(1, tiempo):
                            uds_copy = {id_ud: ud for id_ud, ud in UD_dual_organization_al_inh.uds.items() if ud.activa}
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
                            if not uds_copy: #Extintion
                                # Only 0
                                print(f"acabó en 0 el experimento {contador+1} con herencia {inherits[i]} con unidades {Dvalphas[j]}")
                                break         
                            # Cycle:
                            varieties_list = [var for ud in uds_copy.values() for var in ud.varieties]
                            for id_ud, ud in uds_copy.items():
                                ud.ter_filho()
                                ud.buscar_ud(uds_copy, int(media), varieties_list, True, 3, 0.2)
                                ud.incrementar_idade()
                                ud.death_probability(prob_morte)
                            # Collecting data
                            vivas_tasa_crecimiento.append(len([ud for id, ud in uds_copy.items() if ud.activa]))
                            if t % punto_vista == 0:
                                viv = len([ud for id, ud in uds_copy.items() if ud.activa])
                                vivas_puntos_vista.append(viv)
                                # For diversity
                                var_ud = []
                                var_total = []
                                for ud in [ud for ud in UD_dual_organization_al_inh.uds.values() if ud.activa ==True]:
                                    var_ud.append(len(ud.varieties))
                                    for variety in ud.varieties:
                                        var_total.append(variety.variety_id)
                                mean_var_ud.append(np.mean(var_ud))
                                var_system.append(len(var_total))
                                unique_system.append(len(set(var_total))) 
                        viv = len([ud for id, ud in UD_dual_organization_al_inh.uds.items() if ud.activa])
                        vivas_puntos_vista.append(viv)
                        # For diversity
                        var_ud = []
                        var_total = []
                        for ud in [ud for ud in UD_dual_organization_al_inh.uds.values() if ud.activa ==True]:
                            var_ud.append(len(ud.varieties))
                            for variety in ud.varieties:
                                var_total.append(variety.variety_id)
                        mean_var_ud.append(np.mean(var_ud))
                        var_system.append(len(var_total))
                        unique_system.append(len(set(var_total)))
                        alive = (len([ud for id, ud in uds_copy.items() if ud.activa]))
                        if alive >= 1:   
                            total_varieties = []
                            varieties_per_UD = []
                            for ud in [ud for ud in UD_dual_organization_al_inh.uds.values() if ud.activa ==True]:
                                varieties_per_UD.append(len(ud.varieties))
                                for variety in ud.varieties:
                                    total_varieties.append(variety.variety_id)
                            data_endo_mean_ud.append(np.mean(varieties_per_UD))
                            data_endo_com_level.append(len(set(total_varieties)))
                            data_endo_total_varieties.append(total_varieties)
                    # Final collection of the data after the simulation!
                    if len(uds_copy) > 0:  # Only collect data if the system is alive
                        list_alive_UDs.append(len([ud for id, ud in uds_copy.items() if ud.activa == True]))  # For heatmap
                        list_vivas_puntos_vista.append(vivas_puntos_vista)
                        data_step_var_system.append(var_system)
                        data_step_unique_system.append(unique_system)
                        data_step_mean_var_ud.append(mean_var_ud)
                        contador += 1
                    iterations += 1
                    print('succesful', contador)
                    print('iterations', iterations)
                    
                    data_inherit_endo = [data_endo_mean_ud, data_endo_com_level, data_endo_total_varieties]
                data_steps_inherit_endo = [data_step_var_system, data_step_unique_system, data_step_mean_var_ud]
                media = original_media
                end_config = time.time()
                if contador == experiments:
                    vM[i][j] = {
                        'alive': np.mean(list_alive_UDs),
                        'lstd': np.std(list_alive_UDs),
                        'time used': end_config - star_configuration,
                        'percentage_extinction': contador / experiments,
                        'tempo': tempo, 
                        'mean': np.mean(list_vivas_puntos_vista, axis=0), 
                        'std': np.std(list_vivas_puntos_vista, axis=0),
                        'growth rate': np.mean([np.mean(lista) for lista in tasas_crecimiento]),
                        'diversity_info': data_inherit_endo,
                        'diversity_info_steps': data_steps_inherit_endo,
                    }
                else:  # Handle extinction-only scenarios
                    vM[i][j] = {
                        'alive': None,
                        'lstd': None,
                        'time used': end_config - star_configuration,
                        'percentage_extinction': 1.0,  # All experiments went extinct
                        'tempo': None, 
                        'mean': None, 
                        'std': None,
                        'growth rate': None,
                        'diversity_info': None,
                        'diversity_info_steps': None,
                    }
                print(f"""
        The total time of the configuration of inherit percentage {inherit}, 
        initial UDs {iniciais} and Initial varieties {varieties} is  {end_config - star_configuration}
                """)
        # Folder
        heat_std = os.path.join(folder_name, 'Dual_Initial_Varieties.npy')
        np.save(heat_std, vM)
        now = datetime.now()
        finish = time.time()
        print(f"""
        It finished at: {now}
        It lasted {finish-start}
        """)
        print("done")
        heat_std = os.path.join(folder_name, 'Dual_Initial_Varieties.npy')
        DvM_datos = np.load(heat_std, allow_pickle=True)
        plot = transversal_changes(DvM_datos, inherits, Dvalphas, 'Dual Organization', variable='Initial Varieties')
        plot.savefig(os.path.join(folder_name, 'diversity_behavior.png'), dpi=300, bbox_inches="tight")
        plot = transversal_alive(DvM_datos, inherits, Dvalphas, 'Dual Organization', variable='Initial Varieties')
        plot.savefig(os.path.join(folder_name, 'populational_behavior.png'), dpi=300, bbox_inches="tight")
    elif variable == '3':
        #sub folder
        folder_name = os.path.join(folder_name, 'Mean of children by UD')
        # Create the sub-folder if it doesn't exist
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
        # This experiment has different values for Mean of children
        prob_morte = 0.06 #beta
        n = 10 # Mean
        m = 40 # Initial UDs
        inherits = [0,25,50, 'False']
        Dcalphas = np.linspace(1,n,n) # Mean of children from 1 to n
        # For data of behaviour
        cM = np.empty((len(inherits), len(Dcalphas)), dtype=object)
        punto_vista = 50
        tiempo = 1000
        tempo = list(range(0,tiempo+1,punto_vista))
        experiments = 100
        max_iterations = 400
        print(cM.shape)
        start = time.time()
        print(f"started at:  {datetime.now()}")
        for i, inherit in enumerate(inherits):
            for j, media  in enumerate(Dcalphas):
                star_configuration = time.time()
                #For population dynamics
                list_alive_UDs = []
                list_vivas_puntos_vista = []
                tasas_crecimiento = []
                #For diversity dynamics
                data_step_mean_var_ud = []
                data_step_var_system = []
                data_step_unique_system = []
                print(f"Experiments with inheritance {inherit} and Mean of Children {media}")
                #Lists to store experiments' diversity data
                data_endo_mean_ud = []
                data_endo_com_level = []
                data_endo_total_varieties = []
                original_media = media
                contador = 0
                iterations = 0
                while contador < experiments and iterations < max_iterations: 
                #for experiment in range(1, experiments+1):
                    print(f'experimento {contador+1}')
                    ## Clans
                    clans = (list(range(1, 2 + 1)) * (int(m) // 2)) # Just 2 clans
                    random.shuffle(clans)
                    if inherit != 'False':
                        #### Initialization
                        UD_dual_organization.uds = {}
                        instancias_ud = []
                        for id_ud in range(1, int(m) + 1):
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
                        vivas_puntos_vista = [int(m)]
                        vivas_tasa_crecimiento = [int(m)]
                #             mortas_puntos_vista = [0]
                        #For diversity
                        mean_var_ud = []
                        var_system = []
                        unique_system = []
                        var_ud = []
                        var_total = []
                        for ud in [ud for ud in UD_dual_organization.uds.values() if ud.activa ==True]:
                            var_ud.append(len(ud.varieties))
                            for variety in ud.varieties:
                                var_total.append(variety.variety_id)
                        mean_var_ud.append(np.mean(var_ud))
                        var_system.append(len(var_total))
                        unique_system.append(len(set(var_total)))
                        # Simulation
                        for t in range(1, tiempo):
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
                            if not uds_copy: #Extintion
                                # Only 0
                                print(f"acabó en 0 el experimento {contador+1} con herencia {inherits[i]} con mean {Dcalphas[j]}")
                                break         
                            # Cycle:
                            for id_ud, ud in uds_copy.items():
                                ud.ter_filho()
                                ud.buscar_ud(uds_copy, int(media), inherit, True, 0.2)
                                ud.incrementar_idade()
                                ud.death_probability(prob_morte)
                            # Collecting data
                            vivas_tasa_crecimiento.append(len([ud for id, ud in uds_copy.items() if ud.activa]))
                            if t % punto_vista == 0:
                                viv = len([ud for id, ud in uds_copy.items() if ud.activa])
                                vivas_puntos_vista.append(viv)
                                # For diversity
                                var_ud = []
                                var_total = []
                                for ud in [ud for ud in UD_dual_organization.uds.values() if ud.activa ==True]:
                                    var_ud.append(len(ud.varieties))
                                    for variety in ud.varieties:
                                        var_total.append(variety.variety_id)
                                mean_var_ud.append(np.mean(var_ud))
                                var_system.append(len(var_total))
                                unique_system.append(len(set(var_total))) 
                        viv = len([ud for id, ud in UD_dual_organization.uds.items() if ud.activa])
                        vivas_puntos_vista.append(viv)
                        # For diversity
                        var_ud = []
                        var_total = []
                        for ud in [ud for ud in UD_dual_organization.uds.values() if ud.activa ==True]:
                            var_ud.append(len(ud.varieties))
                            for variety in ud.varieties:
                                var_total.append(variety.variety_id)
                        mean_var_ud.append(np.mean(var_ud))
                        var_system.append(len(var_total))
                        unique_system.append(len(set(var_total)))
                        alive = (len([ud for id, ud in uds_copy.items() if ud.activa]))
                        if alive >= 1:   
                            total_varieties = []
                            varieties_per_UD = []
                            for ud in [ud for ud in UD_dual_organization.uds.values() if ud.activa ==True]:
                                varieties_per_UD.append(len(ud.varieties))
                                for variety in ud.varieties:
                                    total_varieties.append(variety.variety_id)
                            data_endo_mean_ud.append(np.mean(varieties_per_UD))
                            data_endo_com_level.append(len(set(total_varieties)))
                            data_endo_total_varieties.append(total_varieties)
                    else:# Now with inherit == False
                        #### Initialization
                        UD_dual_organization_al_inh.uds = {}
                        instancias_ud = []
                        for id_ud in range(1, int(m) + 1):
                            instancias_ud.append(UD_dual_organization_al_inh(id_ud, media, clans.pop()))
                        ## Varieties
                        limited_varieties = True
                        if limited_varieties == False:
                            for id_ud, ud in UD_dual_organization_al_inh.uds.items():
                                for _ in range(3):
                                    ud.varieties.append(Variety())
                        else:
                            initial_varieties = [Variety() for _ in range (10)]
                            for ud in UD_dual_organization_al_inh.uds.values():
                                for _ in range(3):
                                    ud.varieties.append(random.choice(initial_varieties))   
                        # Lists for graphs
                        vivas_puntos_vista = [int(m)]
                        vivas_tasa_crecimiento = [int(m)]
                        #For diversity
                        mean_var_ud = []
                        var_system = []
                        unique_system = []
                        var_ud = []
                        var_total = []
                        for ud in [ud for ud in UD_dual_organization_al_inh.uds.values() if ud.activa ==True]:
                            var_ud.append(len(ud.varieties))
                            for variety in ud.varieties:
                                var_total.append(variety.variety_id)
                        mean_var_ud.append(np.mean(var_ud))
                        var_system.append(len(var_total))
                        unique_system.append(len(set(var_total)))
                        # Simulation
                        for t in range(1, tiempo):
                            uds_copy = {id_ud: ud for id_ud, ud in UD_dual_organization_al_inh.uds.items() if ud.activa}
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
                            if not uds_copy: #Extintion
                                # Only 0
                                print(f"acabó en 0 el experimento {contador+1} con herencia {inherits[i]} con mean {Dcalphas[j]}")
                                break         
                            # Cycle:
                            varieties_list = [var for ud in uds_copy.values() for var in ud.varieties]
                            for id_ud, ud in uds_copy.items():
                                ud.ter_filho()
                                ud.buscar_ud(uds_copy, int(media), varieties_list, True, 3, 0.2)
                                ud.incrementar_idade()
                                ud.death_probability(prob_morte)
                            # Collecting data
                            vivas_tasa_crecimiento.append(len([ud for id, ud in uds_copy.items() if ud.activa]))
                            if t % punto_vista == 0:
                                viv = len([ud for id, ud in uds_copy.items() if ud.activa])
                                vivas_puntos_vista.append(viv)
                                # For diversity
                                var_ud = []
                                var_total = []
                                for ud in [ud for ud in UD_dual_organization_al_inh.uds.values() if ud.activa ==True]:
                                    var_ud.append(len(ud.varieties))
                                    for variety in ud.varieties:
                                        var_total.append(variety.variety_id)
                                mean_var_ud.append(np.mean(var_ud))
                                var_system.append(len(var_total))
                                unique_system.append(len(set(var_total))) 
                        viv = len([ud for id, ud in UD_dual_organization_al_inh.uds.items() if ud.activa])
                        vivas_puntos_vista.append(viv)
                        # For diversity
                        var_ud = []
                        var_total = []
                        for ud in [ud for ud in UD_dual_organization_al_inh.uds.values() if ud.activa ==True]:
                            var_ud.append(len(ud.varieties))
                            for variety in ud.varieties:
                                var_total.append(variety.variety_id)
                        mean_var_ud.append(np.mean(var_ud))
                        var_system.append(len(var_total))
                        unique_system.append(len(set(var_total)))
                        alive = (len([ud for id, ud in uds_copy.items() if ud.activa]))
                        if alive >= 1:   
                            total_varieties = []
                            varieties_per_UD = []
                            for ud in [ud for ud in UD_dual_organization_al_inh.uds.values() if ud.activa ==True]:
                                varieties_per_UD.append(len(ud.varieties))
                                for variety in ud.varieties:
                                    total_varieties.append(variety.variety_id)
                            data_endo_mean_ud.append(np.mean(varieties_per_UD))
                            data_endo_com_level.append(len(set(total_varieties)))
                            data_endo_total_varieties.append(total_varieties)
                    # Final collection of the data after the simulation!
                    if len(uds_copy) > 0:  # Only collect data if the system is alive
                        list_alive_UDs.append(len([ud for id, ud in uds_copy.items() if ud.activa == True])) 
                        list_vivas_puntos_vista.append(vivas_puntos_vista)
                        data_step_var_system.append(var_system)
                        data_step_unique_system.append(unique_system)
                        data_step_mean_var_ud.append(mean_var_ud)
                        contador += 1
                    iterations += 1
                    print('succesful', contador)
                    print('iterations', iterations) 
                    
                    data_inherit_endo = [data_endo_mean_ud, data_endo_com_level, data_endo_total_varieties]
                data_steps_inherit_endo = [data_step_var_system, data_step_unique_system, data_step_mean_var_ud]
                media = original_media
                end_config = time.time()
                if contador == experiments:
                    cM[i][j] = {
                        'alive': np.mean(list_alive_UDs),
                        'lstd': np.std(list_alive_UDs),
                        'time used': end_config - star_configuration,
                        'percentage_extinction': contador / experiments,
                        'tempo': tempo, 
                        'mean': np.mean(list_vivas_puntos_vista, axis=0), 
                        'std': np.std(list_vivas_puntos_vista, axis=0),
                        'growth rate': np.mean([np.mean(lista) for lista in tasas_crecimiento]),
                        'diversity_info': data_inherit_endo,
                        'diversity_info_steps': data_steps_inherit_endo,
                    }
                else:  # Handle extinction-only scenarios
                    cM[i][j] = {
                        'alive': None,
                        'lstd': None,
                        'time used': end_config - star_configuration,
                        'percentage_extinction': 1.0,  # All experiments went extinct
                        'tempo': None, 
                        'mean': None, 
                        'std': None,
                        'growth rate': None,
                        'diversity_info': None,
                        'diversity_info_steps': None,
                    }
                print(f"""
        The total time of the configuration of inherit percentage {inherit} and initial UDs {m} and mean {media} is  {end_config - star_configuration}
                """)
        # Data
        heat_std = os.path.join(folder_name, 'Dual_Mean_children.npy')
        np.save(heat_std, cM)
        now = datetime.now()
        finish = time.time()
        print(f"""
        It finished at: {now}
        It lasted {finish-start}
        """)
        print("done")
        heat_std = os.path.join(folder_name, 'Dual_Mean_children.npy')
        DcM_datos = np.load(heat_std, allow_pickle=True)
        plot = transversal_changes(DcM_datos, inherits, Dcalphas, 'Dual Organization', variable='Mean of children')
        plot.savefig(os.path.join(folder_name, 'diversity_behavior.png'), dpi=300, bbox_inches="tight")
        plot = transversal_alive(DcM_datos, inherits, Dcalphas, 'Dual Organization', variable='Mean of children')
        plot.savefig(os.path.join(folder_name, 'populational_behavior.png'), dpi=300, bbox_inches="tight")
    else:
        #sub folder
        folder_name = os.path.join(folder_name, 'Number of varieties for UD')
        # Create the sub-folder if it doesn't exist
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
        # This experiment has different values for Initial varieties mv
        prob_morte = 0.06 #beta
        media = 4 # Mean
        m = 40
        mv = 10
        inherits = [0,25,50, 'False'] #Values for inherit
        Dmvalphas = np.linspace(1,mv,mv)# Mean varieties from 1 to mv
        # For data of behaviour
        vM = np.empty((len(inherits), len(Dmvalphas)), dtype=object)
        punto_vista = 50
        tiempo = 1000
        tempo = list(range(0,tiempo+1,punto_vista))
        experiments = 100
        max_iterations = 400
        print(vM.shape)
        start = time.time()
        print(f"started at:  {datetime.now()}")
        for i, inherit in enumerate(inherits):
            for j, mvarieties  in enumerate(Dmvalphas):
                star_configuration = time.time()
                #For population dynamics
                list_alive_UDs = []
                list_vivas_puntos_vista = []
                tasas_crecimiento = []
                #For diversity dynamics
                data_step_mean_var_ud = []
                data_step_var_system = []
                data_step_unique_system = []
                print(f"Experiments with inheritance {inherit} Initial UDs {m} and Mean varieties {mvarieties}")
                #Lists to store experiments' diversity data
                data_endo_mean_ud = []
                data_endo_com_level = []
                data_endo_total_varieties = []
                original_media = media
                contador = 0
                iterations = 0
                while contador < experiments and iterations < max_iterations: 
                    print(f'experimento {contador+1}')
                    ## Clans
                    clans = (list(range(1, 2 + 1)) * (int(m) // 2)) # Just 2 clans
                    random.shuffle(clans)
                    if inherit != 'False':
                        #### Initialization
                        UD_dual_organization.uds = {}
                        instancias_ud = []
                        for id_ud in range(1, int(m) + 1):
                            instancias_ud.append(UD_dual_organization(id_ud, media, clans.pop()))
                        ## Varieties
                        limited_varieties = True
                        if limited_varieties == False:
                            for id_ud, ud in UD_dual_organization.uds.items():
                                for _ in range(3):
                                    ud.varieties.append(Variety())
                        else:
                            initial_varieties = [Variety() for _ in range (int(10))]
                            for ud in UD_dual_organization.uds.values():
                                for _ in range(int(mvarieties)):
                                    ud.varieties.append(random.choice(initial_varieties))   
                        # Lists for graphs
                        vivas_puntos_vista = [int(m)]
                        vivas_tasa_crecimiento = [int(m)]
                        #For diversity
                        mean_var_ud = []
                        var_system = []
                        unique_system = []
                        var_ud = []
                        var_total = []
                        for ud in [ud for ud in UD_dual_organization.uds.values() if ud.activa ==True]:
                            var_ud.append(len(ud.varieties))
                            for variety in ud.varieties:
                                var_total.append(variety.variety_id)
                        mean_var_ud.append(np.mean(var_ud))
                        var_system.append(len(var_total))
                        unique_system.append(len(set(var_total)))
                        # Simulation
                        for t in range(1, tiempo):
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
                            if not uds_copy: #Extintion
                                # Only 0
                                print(f"acabó en 0 el experimento {contador+1} con herencia {inherits[i]} con unidades {Dmvalphas[j]}")
                                break         
                            # Cycle:
                            for id_ud, ud in uds_copy.items():
                                ud.ter_filho()
                                ud.buscar_ud(uds_copy, int(media), inherit, True, 0.2)
                                ud.incrementar_idade()
                                ud.death_probability(prob_morte)
                            # Collecting data
                            vivas_tasa_crecimiento.append(len([ud for id, ud in uds_copy.items() if ud.activa]))
                            if t % punto_vista == 0:
                                viv = len([ud for id, ud in uds_copy.items() if ud.activa])
                                vivas_puntos_vista.append(viv)
                                # For diversity
                                var_ud = []
                                var_total = []
                                for ud in [ud for ud in UD_dual_organization.uds.values() if ud.activa ==True]:
                                    var_ud.append(len(ud.varieties))
                                    for variety in ud.varieties:
                                        var_total.append(variety.variety_id)
                                mean_var_ud.append(np.mean(var_ud))
                                var_system.append(len(var_total))
                                unique_system.append(len(set(var_total))) 
                        viv = len([ud for id, ud in UD_dual_organization.uds.items() if ud.activa])
                        vivas_puntos_vista.append(viv)
                        # For diversity
                        var_ud = []
                        var_total = []
                        for ud in [ud for ud in UD_dual_organization.uds.values() if ud.activa ==True]:
                            var_ud.append(len(ud.varieties))
                            for variety in ud.varieties:
                                var_total.append(variety.variety_id)
                        mean_var_ud.append(np.mean(var_ud))
                        var_system.append(len(var_total))
                        unique_system.append(len(set(var_total)))
                        alive = (len([ud for id, ud in uds_copy.items() if ud.activa]))
                        if alive >= 1:   
                            total_varieties = []
                            varieties_per_UD = []
                            for ud in [ud for ud in UD_dual_organization.uds.values() if ud.activa ==True]:
                                varieties_per_UD.append(len(ud.varieties))
                                for variety in ud.varieties:
                                    total_varieties.append(variety.variety_id)
                            data_endo_mean_ud.append(np.mean(varieties_per_UD))
                            data_endo_com_level.append(len(set(total_varieties)))
                            data_endo_total_varieties.append(total_varieties)
                    else:# Now with inherit == False
                        #### Initialization
                        UD_dual_organization_al_inh.uds = {}
                        instancias_ud = []
                        for id_ud in range(1, int(m) + 1):
                            instancias_ud.append(UD_dual_organization_al_inh(id_ud, media, clans.pop()))
                        ## Varieties
                        limited_varieties = True
                        if limited_varieties == False:
                            for id_ud, ud in UD_dual_organization_al_inh.uds.items():
                                for _ in range(3):
                                    ud.varieties.append(Variety())
                        else:
                            initial_varieties = [Variety() for _ in range (int(10))]
                            for ud in UD_dual_organization_al_inh.uds.values():
                                for _ in range(int(mvarieties)):
                                    ud.varieties.append(random.choice(initial_varieties))   
                        # Lists for graphs
                        vivas_puntos_vista = [int(m)]
                        vivas_tasa_crecimiento = [int(m)]
                        #For diversity
                        mean_var_ud = []
                        var_system = []
                        unique_system = []
                        var_ud = []
                        var_total = []
                        for ud in [ud for ud in UD_dual_organization_al_inh.uds.values() if ud.activa ==True]:
                            var_ud.append(len(ud.varieties))
                            for variety in ud.varieties:
                                var_total.append(variety.variety_id)
                        mean_var_ud.append(np.mean(var_ud))
                        var_system.append(len(var_total))
                        unique_system.append(len(set(var_total)))
                        # Simulation
                        for t in range(1, tiempo):
                            uds_copy = {id_ud: ud for id_ud, ud in UD_dual_organization_al_inh.uds.items() if ud.activa}
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
                            if not uds_copy: #Extintion
                                # Only 0
                                print(f"acabó en 0 el experimento {contador+1} con herencia {inherits[i]} con unidades {Dmvalphas[j]}")
                                break         
                            # Cycle:
                            varieties_list = [var for ud in uds_copy.values() for var in ud.varieties]
                            for id_ud, ud in uds_copy.items():
                                ud.ter_filho()
                                ud.buscar_ud(uds_copy, int(media), varieties_list, True, int(mvarieties), 0.2)
                                ud.incrementar_idade()
                                ud.death_probability(prob_morte)
                            # Collecting data
                            vivas_tasa_crecimiento.append(len([ud for id, ud in uds_copy.items() if ud.activa]))
                            if t % punto_vista == 0:
                                viv = len([ud for id, ud in uds_copy.items() if ud.activa])
                                vivas_puntos_vista.append(viv)
                                # For diversity
                                var_ud = []
                                var_total = []
                                for ud in [ud for ud in UD_dual_organization_al_inh.uds.values() if ud.activa ==True]:
                                    var_ud.append(len(ud.varieties))
                                    for variety in ud.varieties:
                                        var_total.append(variety.variety_id)
                                mean_var_ud.append(np.mean(var_ud))
                                var_system.append(len(var_total))
                                unique_system.append(len(set(var_total))) 
                        viv = len([ud for id, ud in UD_dual_organization_al_inh.uds.items() if ud.activa])
                        vivas_puntos_vista.append(viv)
                        # For diversity
                        var_ud = []
                        var_total = []
                        for ud in [ud for ud in UD_dual_organization_al_inh.uds.values() if ud.activa ==True]:
                            var_ud.append(len(ud.varieties))
                            for variety in ud.varieties:
                                var_total.append(variety.variety_id)
                        mean_var_ud.append(np.mean(var_ud))
                        var_system.append(len(var_total))
                        unique_system.append(len(set(var_total)))
                        alive = (len([ud for id, ud in uds_copy.items() if ud.activa]))
                        if alive >= 1:   
                            total_varieties = []
                            varieties_per_UD = []
                            for ud in [ud for ud in UD_dual_organization_al_inh.uds.values() if ud.activa ==True]:
                                varieties_per_UD.append(len(ud.varieties))
                                for variety in ud.varieties:
                                    total_varieties.append(variety.variety_id)
                            data_endo_mean_ud.append(np.mean(varieties_per_UD))
                            data_endo_com_level.append(len(set(total_varieties)))
                            data_endo_total_varieties.append(total_varieties)
                    # Final collection of the data after the simulation!
                    if len(uds_copy) > 0:  # Only collect data if the system is alive
                        list_alive_UDs.append(len([ud for id, ud in uds_copy.items() if ud.activa == True]))  # For heatmap
                        list_vivas_puntos_vista.append(vivas_puntos_vista)
                        data_step_var_system.append(var_system)
                        data_step_unique_system.append(unique_system)
                        data_step_mean_var_ud.append(mean_var_ud)
                        contador += 1
                    iterations += 1
                    print('succesful', contador)
                    print('iterations', iterations)   
                    
                    data_inherit_endo = [data_endo_mean_ud, data_endo_com_level, data_endo_total_varieties]
                data_steps_inherit_endo = [data_step_var_system, data_step_unique_system, data_step_mean_var_ud]
                media = original_media
                end_config = time.time()
                if contador == experiments:
                    vM[i][j] = {
                        'alive': np.mean(list_alive_UDs),
                        'lstd': np.std(list_alive_UDs),
                        'time used': end_config - star_configuration,
                        'percentage_extinction': contador / experiments,
                        'tempo': tempo, 
                        'mean': np.mean(list_vivas_puntos_vista, axis=0), 
                        'std': np.std(list_vivas_puntos_vista, axis=0),
                        'growth rate': np.mean([np.mean(lista) for lista in tasas_crecimiento]),
                        'diversity_info': data_inherit_endo,
                        'diversity_info_steps': data_steps_inherit_endo,
                    }
                else:  # Handle extinction-only scenarios
                    vM[i][j] = {
                        'alive': None,
                        'lstd': None,
                        'time used': end_config - star_configuration,
                        'percentage_extinction': 1.0,  # All experiments went extinct
                        'tempo': None, 
                        'mean': None, 
                        'std': None,
                        'growth rate': None,
                        'diversity_info': None,
                        'diversity_info_steps': None,
                    }
                print(f"""
        The total time of the configuration of inherit percentage {inherit}, 
        initial UDs {m} and Mean varieties {mvarieties} is  {end_config - star_configuration}
                """)
        # Folder
        heat_std = os.path.join(folder_name, 'Dual_Initial_Mean_varieties.npy')
        np.save(heat_std, vM)
        now = datetime.now()
        finish = time.time()
        print(f"""
        It finished at: {now}
        It lasted {finish-start}
        """)
        print("done")
        heat_std = os.path.join(folder_name, 'Dual_Initial_Mean_varieties.npy')
        DmvM_datos = np.load(heat_std, allow_pickle=True)
        plot = transversal_changes(DmvM_datos, inherits, Dmvalphas, 'Dual Organization', variable='Mean varieties')
        plot.savefig(os.path.join(folder_name, 'diversity_behavior.png'), dpi=300, bbox_inches="tight")
        plot = transversal_alive(DmvM_datos, inherits, Dmvalphas, 'Dual Organization', variable='Mean varieties')
        plot.savefig(os.path.join(folder_name, 'populational_behavior.png'), dpi=300, bbox_inches="tight")
else:
    print('Ok, lets go with generalized exchange')
    #sub folder
    folder_name = os.path.join(parent_folder, 'Second experiments', 'Generalized Exchange')
    # Create the sub-folder if it doesn't exist
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    if variable  == '1':
        #sub folder
        folder_name = os.path.join(folder_name, 'Initial UDs')
        # Create the sub-folder if it doesn't exist
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
        # This experiment has different values for Initial UDs
        prob_morte = 0.06 #beta
        media = 4 # Mean
        m = 100 # Initial UDs
        inherits = [0,25,50, 'False']
        Gmalphas = np.linspace(10,m,int(m/10)) # Initial UDs: from 10 to m
        # For data of behaviour
        mM = np.empty((len(inherits), len(Gmalphas)), dtype=object)
        punto_vista = 50
        tiempo = 1000
        tempo = list(range(0,tiempo+1,punto_vista))
        experiments = 100
        max_iterations = 400

        print(mM.shape)
        start = time.time()
        print(f"started at:  {datetime.now()}")
        for i, inherit in enumerate(inherits):
            for j, iniciais  in enumerate(Gmalphas):
                star_configuration = time.time()
                #For population dynamics
                list_alive_UDs = []
                list_vivas_puntos_vista = []
                tasas_crecimiento = []
                #For diversity dynamics
                data_step_mean_var_ud = []
                data_step_var_system = []
                data_step_unique_system = []
                print(f"Experiments with inheritance {inherit} and Initial UDs {iniciais}")
                #Lists to store experiments' diversity data
                data_endo_mean_ud = []
                data_endo_com_level = []
                data_endo_total_varieties = []
                original_media = media
                contador = 0
                iterations = 0
                while contador < experiments and iterations < max_iterations:
                    print(f'experimento {contador+1}')
                    ## Clans
                    clans = (list(range(1, 4)) * (int(iniciais) // 3 + 1))[:int(iniciais)] # Just 3 clans
                    random.shuffle(clans)
                    if inherit != 'False':          
                        #### Initialization
                        UD_generalized.uds = {}
                        instancias_ud = []
                        for id_ud in range(1, int(iniciais) + 1):
                            instancias_ud.append(UD_generalized(id_ud, media,clans.pop()))
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
                        #For diversity
                        mean_var_ud = []
                        var_system = []
                        unique_system = []
                        var_ud = []
                        var_total = []
                        for ud in [ud for ud in UD_generalized.uds.values() if ud.activa ==True]:
                            var_ud.append(len(ud.varieties))
                            for variety in ud.varieties:
                                var_total.append(variety.variety_id)
                        mean_var_ud.append(np.mean(var_ud))
                        var_system.append(len(var_total))
                        unique_system.append(len(set(var_total)))
                        # Simulation
                        for t in range(1, tiempo):
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
                            if not uds_copy: #Extintion
                                # Only 0
                                print(f"acabó en 0 el experimento {contador+1} con herencia {inherits[i]} con unidades {Gmalphas[j]}")
                                break         
                            # Cycle:
                            for id_ud, ud in uds_copy.items():
                                ud.ter_filho()
                                ud.buscar_ud(uds_copy, int(media), inherit, True, 0.2)
                                ud.incrementar_idade()
                                ud.death_probability(prob_morte)
                            # Collecting data
                            vivas_tasa_crecimiento.append(len([ud for id, ud in uds_copy.items() if ud.activa]))
                            if t % punto_vista == 0:
                                viv = len([ud for id, ud in uds_copy.items() if ud.activa])
                                vivas_puntos_vista.append(viv)
                                # For diversity
                                var_ud = []
                                var_total = []
                                for ud in [ud for ud in UD_generalized.uds.values() if ud.activa ==True]:
                                    var_ud.append(len(ud.varieties))
                                    for variety in ud.varieties:
                                        var_total.append(variety.variety_id)
                                mean_var_ud.append(np.mean(var_ud))
                                var_system.append(len(var_total))
                                unique_system.append(len(set(var_total))) 
                        viv = len([ud for id, ud in UD_generalized.uds.items() if ud.activa])
                        vivas_puntos_vista.append(viv)
                        # For diversity
                        var_ud = []
                        var_total = []
                        for ud in [ud for ud in UD_generalized.uds.values() if ud.activa ==True]:
                            var_ud.append(len(ud.varieties))
                            for variety in ud.varieties:
                                var_total.append(variety.variety_id)
                        mean_var_ud.append(np.mean(var_ud))
                        var_system.append(len(var_total))
                        unique_system.append(len(set(var_total)))
                        alive = (len([ud for id, ud in uds_copy.items() if ud.activa]))
                        if alive >= 1:   
                            total_varieties = []
                            varieties_per_UD = []
                            for ud in [ud for ud in UD_generalized.uds.values() if ud.activa ==True]:
                                varieties_per_UD.append(len(ud.varieties))
                                for variety in ud.varieties:
                                    total_varieties.append(variety.variety_id)
                            data_endo_mean_ud.append(np.mean(varieties_per_UD))
                            data_endo_com_level.append(len(set(total_varieties)))
                            data_endo_total_varieties.append(total_varieties)
                    else:# Now with inherit == False
                        #### Initialization
                        UD_generalized_al_inh.uds = {}
                        instancias_ud = []
                        for id_ud in range(1, int(iniciais) + 1):
                            instancias_ud.append(UD_generalized_al_inh(id_ud, media, clans.pop()))
                        ## Varieties
                        limited_varieties = True
                        if limited_varieties == False:
                            for id_ud, ud in UD_generalized_al_inh.uds.items():
                                for _ in range(3):
                                    ud.varieties.append(Variety())
                        else:
                            initial_varieties = [Variety() for _ in range (10)]
                            for ud in UD_generalized_al_inh.uds.values():
                                for _ in range(3):
                                    ud.varieties.append(random.choice(initial_varieties))   
                        # Lists for graphs
                        vivas_puntos_vista = [int(iniciais)]
                        vivas_tasa_crecimiento = [int(iniciais)]
                        #For diversity
                        mean_var_ud = []
                        var_system = []
                        unique_system = []
                        var_ud = []
                        var_total = []
                        for ud in [ud for ud in UD_generalized_al_inh.uds.values() if ud.activa ==True]:
                            var_ud.append(len(ud.varieties))
                            for variety in ud.varieties:
                                var_total.append(variety.variety_id)
                        mean_var_ud.append(np.mean(var_ud))
                        var_system.append(len(var_total))
                        unique_system.append(len(set(var_total)))
                        # Simulation
                        for t in range(1, tiempo):
                            uds_copy = {id_ud: ud for id_ud, ud in UD_generalized_al_inh.uds.items() if ud.activa}
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
                            if not uds_copy: #Extintion
                                # Only 0
                                print(f"acabó en 0 el experimento {contador+1} con herencia {inherits[i]} con unidades {Gmalphas[j]}")
                                break         
                            # Cycle:
                            varieties_list = [var for ud in uds_copy.values() for var in ud.varieties]
                            for id_ud, ud in uds_copy.items():
                                ud.ter_filho()
                                ud.buscar_ud(uds_copy, int(media), varieties_list, True, 3, 0.2)
                                ud.incrementar_idade()
                                ud.death_probability(prob_morte)
                            # Collecting data
                            vivas_tasa_crecimiento.append(len([ud for id, ud in uds_copy.items() if ud.activa]))
                            if t % punto_vista == 0:
                                viv = len([ud for id, ud in uds_copy.items() if ud.activa])
                                vivas_puntos_vista.append(viv)
                                # For diversity
                                var_ud = []
                                var_total = []
                                for ud in [ud for ud in UD_generalized_al_inh.uds.values() if ud.activa ==True]:
                                    var_ud.append(len(ud.varieties))
                                    for variety in ud.varieties:
                                        var_total.append(variety.variety_id)
                                mean_var_ud.append(np.mean(var_ud))
                                var_system.append(len(var_total))
                                unique_system.append(len(set(var_total))) 
                        viv = len([ud for id, ud in UD_generalized_al_inh.uds.items() if ud.activa])
                        vivas_puntos_vista.append(viv)
                        # For diversity
                        var_ud = []
                        var_total = []
                        for ud in [ud for ud in UD_generalized_al_inh.uds.values() if ud.activa ==True]:
                            var_ud.append(len(ud.varieties))
                            for variety in ud.varieties:
                                var_total.append(variety.variety_id)
                        mean_var_ud.append(np.mean(var_ud))
                        var_system.append(len(var_total))
                        unique_system.append(len(set(var_total)))
                        alive = (len([ud for id, ud in uds_copy.items() if ud.activa]))
                        if alive >= 1:   
                            total_varieties = []
                            varieties_per_UD = []
                            for ud in [ud for ud in UD_generalized_al_inh.uds.values() if ud.activa ==True]:
                                varieties_per_UD.append(len(ud.varieties))
                                for variety in ud.varieties:
                                    total_varieties.append(variety.variety_id)
                            data_endo_mean_ud.append(np.mean(varieties_per_UD))
                            data_endo_com_level.append(len(set(total_varieties)))
                            data_endo_total_varieties.append(total_varieties)
                    # Final collection of the data after the simulation!
                    if len(uds_copy) > 0:  # Only collect data if the system is alive
                        list_alive_UDs.append(len([ud for id, ud in uds_copy.items() if ud.activa == True]))  # For heatmap
                        list_vivas_puntos_vista.append(vivas_puntos_vista)
                        data_step_var_system.append(var_system)
                        data_step_unique_system.append(unique_system)
                        data_step_mean_var_ud.append(mean_var_ud)
                        contador += 1
                    iterations += 1
                    print('succesful', contador)
                    print('iterations', iterations) 
                    
                    data_inherit_endo = [data_endo_mean_ud, data_endo_com_level, data_endo_total_varieties]
                data_steps_inherit_endo = [data_step_var_system, data_step_unique_system, data_step_mean_var_ud]
                media = original_media
                end_config = time.time()
                if contador == experiments:
                    mM[i][j] = {
                        'alive': np.mean(list_alive_UDs),
                        'lstd': np.std(list_alive_UDs),
                        'time used': end_config - star_configuration,
                        'percentage_extinction': contador / experiments,
                        'tempo': tempo, 
                        'mean': np.mean(list_vivas_puntos_vista, axis=0), 
                        'std': np.std(list_vivas_puntos_vista, axis=0),
                        'growth rate': np.mean([np.mean(lista) for lista in tasas_crecimiento]),
                        'diversity_info': data_inherit_endo,
                        'diversity_info_steps': data_steps_inherit_endo,
                    }
                else:  # Handle extinction-only scenarios
                    mM[i][j] = {
                        'alive': None,
                        'lstd': None,
                        'time used': end_config - star_configuration,
                        'percentage_extinction': 1.0,  # All experiments went extinct
                        'tempo': None, 
                        'mean': None, 
                        'std': None,
                        'growth rate': None,
                        'diversity_info': None,
                        'diversity_info_steps': None,
                    }
                print(f"""
        The total time of the configuration of inherit percentage {inherit} and initial UDs {iniciais} is  {end_config - star_configuration}
                """)
        # Folder
        heat_std = os.path.join(folder_name, 'Generalized_Initial_UDs.npy')
        np.save(heat_std, mM)
        now = datetime.now()
        finish = time.time()
        print(f"""
        It finished at: {now}
        It lasted {finish-start}
        """)
        print("done")
        heat_std = os.path.join(folder_name, 'Generalized_Initial_UDs.npy')
        GmM_datos = np.load(heat_std, allow_pickle=True)
        plot = transversal_changes(GmM_datos, inherits, Gmalphas, 'Generalized', variable='Initial UDs')
        plot.savefig(os.path.join(folder_name, 'diversity_behavior.png'), dpi=300, bbox_inches="tight")
        plot = transversal_alive(GmM_datos, inherits, Gmalphas, 'Generalized', variable='Initial UDs')
        plot.savefig(os.path.join(folder_name, 'populational_behavior.png'), dpi=300, bbox_inches="tight")
    elif variable == '2':
        #sub folder
        folder_name = os.path.join(folder_name, 'Initial Varieties')
        # Create the sub-folder if it doesn't exist
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
        # This experiment has different values for Initial varieties 
        prob_morte = 0.06 #beta
        media = 4 # Mean
        m = 40
        v = 100 # Initial varieties
        inherits = [0,25,50, 'False']
        Dvalphas = np.linspace(10,v,int(v/10)) # Initial Varieties: from 10 to v
        # For data of behaviour
        vM = np.empty((len(inherits), len(Dvalphas)), dtype=object) 
        punto_vista = 50
        tiempo = 1000
        tempo = list(range(0,tiempo+1,punto_vista))
        experiments = 100
        max_iterations = 400 
        print(vM.shape)
        start = time.time()
        print(f"started at:  {datetime.now()}")
        for i, inherit in enumerate(inherits):
            for j, varieties  in enumerate(Dvalphas):
                star_configuration = time.time()
                #For population dynamics
                list_alive_UDs = []
                list_vivas_puntos_vista = []
                tasas_crecimiento = []
                #For diversity dynamics
                data_step_mean_var_ud = []
                data_step_var_system = []
                data_step_unique_system = []
                print(f"Experiments with inheritance {inherit} Initial UDs {m} and Initial varieties {varieties}")
                #Lists to store experiments' diversity data
                data_endo_mean_ud = []
                data_endo_com_level = []
                data_endo_total_varieties = []
                original_media = media
                contador = 0
                iterations = 0
                while contador < experiments and iterations < max_iterations:
                    print(f'experimento {contador+1}')
                    #### Initialization generalized_exchange
                    ## Clans
                    clans = (list(range(1, 4)) * (m // 3 + 1))[:m] # Just 3 clans
                    random.shuffle(clans)
                    if inherit != 'False':    
                        #### Initialization
                        UD_generalized.uds = {}
                        instancias_ud = []
                        for id_ud in range(1, int(m) + 1):
                            instancias_ud.append(UD_generalized(id_ud, media, clans.pop()))
                        ## Varieties
                        limited_varieties = True
                        if limited_varieties == False:
                            for id_ud, ud in UD_generalized.uds.items():
                                for _ in range(3):
                                    ud.varieties.append(Variety())
                        else:
                            initial_varieties = [Variety() for _ in range (int(varieties))]
                            for ud in UD_generalized.uds.values():
                                for _ in range(3):
                                    ud.varieties.append(random.choice(initial_varieties))   
                        # Lists for graphs
                        vivas_puntos_vista = [int(m)]
                        vivas_tasa_crecimiento = [int(m)]
                        #For diversity
                        mean_var_ud = []
                        var_system = []
                        unique_system = []
                        var_ud = []
                        var_total = []
                        for ud in [ud for ud in UD_generalized.uds.values() if ud.activa ==True]:
                            var_ud.append(len(ud.varieties))
                            for variety in ud.varieties:
                                var_total.append(variety.variety_id)
                        mean_var_ud.append(np.mean(var_ud))
                        var_system.append(len(var_total))
                        unique_system.append(len(set(var_total)))
                        # Simulation
                        for t in range(1, tiempo):
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
                            if not uds_copy: #Extintion
                                # Only 0
                                print(f"acabó en 0 el experimento {contador+1} con herencia {inherits[i]} con unidades {Dvalphas[j]}")
                                break         
                            # Cycle:
                            for id_ud, ud in uds_copy.items():
                                ud.ter_filho()
                                ud.buscar_ud(uds_copy, int(media), inherit, True, 0.2)
                                ud.incrementar_idade()
                                ud.death_probability(prob_morte)
                            # Collecting data
                            vivas_tasa_crecimiento.append(len([ud for id, ud in uds_copy.items() if ud.activa]))
                            if t % punto_vista == 0:
                                viv = len([ud for id, ud in uds_copy.items() if ud.activa])
                                vivas_puntos_vista.append(viv)
                                # For diversity
                                var_ud = []
                                var_total = []
                                for ud in [ud for ud in UD_generalized.uds.values() if ud.activa ==True]:
                                    var_ud.append(len(ud.varieties))
                                    for variety in ud.varieties:
                                        var_total.append(variety.variety_id)
                                mean_var_ud.append(np.mean(var_ud))
                                var_system.append(len(var_total))
                                unique_system.append(len(set(var_total))) 
                        viv = len([ud for id, ud in UD_generalized.uds.items() if ud.activa])
                        vivas_puntos_vista.append(viv)
                        # For diversity
                        var_ud = []
                        var_total = []
                        for ud in [ud for ud in UD_generalized.uds.values() if ud.activa ==True]:
                            var_ud.append(len(ud.varieties))
                            for variety in ud.varieties:
                                var_total.append(variety.variety_id)
                        mean_var_ud.append(np.mean(var_ud))
                        var_system.append(len(var_total))
                        unique_system.append(len(set(var_total)))
                        alive = (len([ud for id, ud in uds_copy.items() if ud.activa]))
                        if alive >= 1:   
                            total_varieties = []
                            varieties_per_UD = []
                            for ud in [ud for ud in UD_generalized.uds.values() if ud.activa ==True]:
                                varieties_per_UD.append(len(ud.varieties))
                                for variety in ud.varieties:
                                    total_varieties.append(variety.variety_id)
                            data_endo_mean_ud.append(np.mean(varieties_per_UD))
                            data_endo_com_level.append(len(set(total_varieties)))
                            data_endo_total_varieties.append(total_varieties)
                    else:# Now with inherit == False
                        #### Initialization
                        UD_generalized_al_inh.uds = {}
                        instancias_ud = []
                        for id_ud in range(1, int(m) + 1):
                            instancias_ud.append(UD_generalized_al_inh(id_ud, media, clans.pop()))
                        ## Varieties
                        limited_varieties = True
                        if limited_varieties == False:
                            for id_ud, ud in UD_generalized_al_inh.uds.items():
                                for _ in range(3):
                                    ud.varieties.append(Variety())
                        else:
                            initial_varieties = [Variety() for _ in range (int(varieties))]
                            for ud in UD_generalized_al_inh.uds.values():
                                for _ in range(3):
                                    ud.varieties.append(random.choice(initial_varieties))   
                        # Lists for graphs
                        vivas_puntos_vista = [int(m)]
                        vivas_tasa_crecimiento = [int(m)]
                        #For diversity
                        mean_var_ud = []
                        var_system = []
                        unique_system = []
                        var_ud = []
                        var_total = []
                        for ud in [ud for ud in UD_generalized_al_inh.uds.values() if ud.activa ==True]:
                            var_ud.append(len(ud.varieties))
                            for variety in ud.varieties:
                                var_total.append(variety.variety_id)
                        mean_var_ud.append(np.mean(var_ud))
                        var_system.append(len(var_total))
                        unique_system.append(len(set(var_total)))
                        # Simulation
                        for t in range(1, tiempo):
                            uds_copy = {id_ud: ud for id_ud, ud in UD_generalized_al_inh.uds.items() if ud.activa}
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
                            if not uds_copy: #Extintion
                                # Only 0
                                print(f"acabó en 0 el experimento {contador+1} con herencia {inherits[i]} con unidades {Dvalphas[j]}")
                                break         
                            # Cycle:
                            varieties_list = [var for ud in uds_copy.values() for var in ud.varieties]
                            for id_ud, ud in uds_copy.items():
                                ud.ter_filho()
                                ud.buscar_ud(uds_copy, int(media), varieties_list, True, 3, 0.2)
                                ud.incrementar_idade()
                                ud.death_probability(prob_morte)
                            # Collecting data
                            vivas_tasa_crecimiento.append(len([ud for id, ud in uds_copy.items() if ud.activa]))
                            if t % punto_vista == 0:
                                viv = len([ud for id, ud in uds_copy.items() if ud.activa])
                                vivas_puntos_vista.append(viv)
                                # For diversity
                                var_ud = []
                                var_total = []
                                for ud in [ud for ud in UD_generalized_al_inh.uds.values() if ud.activa ==True]:
                                    var_ud.append(len(ud.varieties))
                                    for variety in ud.varieties:
                                        var_total.append(variety.variety_id)
                                mean_var_ud.append(np.mean(var_ud))
                                var_system.append(len(var_total))
                                unique_system.append(len(set(var_total))) 
                        viv = len([ud for id, ud in UD_generalized_al_inh.uds.items() if ud.activa])
                        vivas_puntos_vista.append(viv)
                        # For diversity
                        var_ud = []
                        var_total = []
                        for ud in [ud for ud in UD_generalized_al_inh.uds.values() if ud.activa ==True]:
                            var_ud.append(len(ud.varieties))
                            for variety in ud.varieties:
                                var_total.append(variety.variety_id)
                        mean_var_ud.append(np.mean(var_ud))
                        var_system.append(len(var_total))
                        unique_system.append(len(set(var_total)))
                        alive = (len([ud for id, ud in uds_copy.items() if ud.activa]))
                        if alive >= 1:   
                            total_varieties = []
                            varieties_per_UD = []
                            for ud in [ud for ud in UD_generalized_al_inh.uds.values() if ud.activa ==True]:
                                varieties_per_UD.append(len(ud.varieties))
                                for variety in ud.varieties:
                                    total_varieties.append(variety.variety_id)
                            data_endo_mean_ud.append(np.mean(varieties_per_UD))
                            data_endo_com_level.append(len(set(total_varieties)))
                            data_endo_total_varieties.append(total_varieties)
                    # Final collection of the data after the simulation!
                    if len(uds_copy) > 0:  # Only collect data if the system is alive
                        list_alive_UDs.append(len([ud for id, ud in uds_copy.items() if ud.activa == True]))  # For heatmap
                        list_vivas_puntos_vista.append(vivas_puntos_vista)
                        data_step_var_system.append(var_system)
                        data_step_unique_system.append(unique_system)
                        data_step_mean_var_ud.append(mean_var_ud)
                        contador += 1
                    iterations += 1
                    print('succesful')
                    print(contador)
                    print('iterations')
                    print(iterations)
                    data_inherit_endo = [data_endo_mean_ud, data_endo_com_level, data_endo_total_varieties]
                data_steps_inherit_endo = [data_step_var_system, data_step_unique_system, data_step_mean_var_ud]
                media = original_media
                end_config = time.time()
                if contador == experiments: 
                    vM[i][j] = {
                        'alive': np.mean(list_alive_UDs),
                        'lstd': np.std(list_alive_UDs),
                        'time used': end_config - star_configuration,
                        'percentage_extinction': contador / experiments,
                        'tempo': tempo, 
                        'mean': np.mean(list_vivas_puntos_vista, axis=0), 
                        'std': np.std(list_vivas_puntos_vista, axis=0),
                        'growth rate': np.mean([np.mean(lista) for lista in tasas_crecimiento]),
                        'diversity_info': data_inherit_endo,
                        'diversity_info_steps': data_steps_inherit_endo,
                    }
                else:  # Handle extinction-only scenarios
                    vM[i][j] = {
                        'alive': None,
                        'lstd': None,
                        'time used': end_config - star_configuration,
                        'percentage_extinction': 1.0,  # All experiments went extinct
                        'tempo': None, 
                        'mean': None, 
                        'std': None,
                        'growth rate': None,
                        'diversity_info': None,
                        'diversity_info_steps': None,
                    }
                print(f"""
        The total time of the configuration of inherit percentage {inherit}, 
        initial UDs {m} and Initial varieties {varieties} is  {end_config - star_configuration}
                """)
        # Heatmap and std
        heat_std = os.path.join(folder_name, 'Generalized_Initial_Varieties.npy')
        np.save(heat_std, vM)
        now = datetime.now()
        finish = time.time()
        print(f"""
        It finished at: {now}
        It lasted {finish-start}
        """)
        print("done")
        heat_std = os.path.join(folder_name, 'Generalized_Initial_Varieties.npy')
        DvM_datos = np.load(heat_std, allow_pickle=True)
        plot = transversal_changes(DvM_datos, inherits, Dvalphas, 'Generalized', variable='Initial Varieties')
        plot.savefig(os.path.join(folder_name, 'diversity_behavior.png'), dpi=300, bbox_inches="tight")
        plot = transversal_alive(DvM_datos, inherits, Dvalphas, 'Generalized', variable='Initial Varieties')
        plot.savefig(os.path.join(folder_name, 'populational_behavior.png'), dpi=300, bbox_inches="tight")
    elif variable == '3':
        #sub folder
        folder_name = os.path.join(folder_name, 'Mean of children by UD')
        # Create the sub-folder if it doesn't exist
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
        # This experiment has different values for Mean of children
        prob_morte = 0.06 #beta
        n = 10 # Mean
        m = 40 # Initial UDs
        iniciais = m
        inherits = [0,25,50, 'False']
        Gcalphas = np.linspace(1,n,n) # Mean of children from 1 to n
        # For data of behaviour
        cM = np.empty((len(inherits), len(Gcalphas)), dtype=object)
        punto_vista = 50
        tiempo = 1000
        tempo = list(range(0,tiempo+1,punto_vista))
        experiments = 100
        max_iterations = 400
        print(cM.shape)
        start = time.time()
        print(f"started at:  {datetime.now()}")
        for i, inherit in enumerate(inherits):
            for j, media  in enumerate(Gcalphas):
                star_configuration = time.time()
                #For population dynamics
                list_alive_UDs = []
                list_vivas_puntos_vista = []
                tasas_crecimiento = []
                #For diversity dynamics
                data_step_mean_var_ud = []
                data_step_var_system = []
                data_step_unique_system = []
                print(f"Experiments with inheritance {inherit} and Mean of Children {media}")
                #Lists to store experiments' diversity data
                data_endo_mean_ud = []
                data_endo_com_level = []
                data_endo_total_varieties = []
                original_media = media
                contador = 0
                iterations = 0
                while contador < experiments and iterations < max_iterations: 
                    print(f'experimento {contador+1}')
                    ## Clans
                    clans = (list(range(1, 4)) * (int(iniciais) // 3 + 1))[:int(iniciais)] # Just 3 clans
                    random.shuffle(clans)
                    if inherit != 'False':
                        #### Initialization
                        UD_generalized.uds = {}
                        instancias_ud = []
                        for id_ud in range(1, int(m) + 1):
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
                        vivas_puntos_vista = [int(m)]
                        vivas_tasa_crecimiento = [int(m)]
                        #For diversity
                        mean_var_ud = []
                        var_system = []
                        unique_system = []
                        var_ud = []
                        var_total = []
                        for ud in [ud for ud in UD_generalized.uds.values() if ud.activa ==True]:
                            var_ud.append(len(ud.varieties))
                            for variety in ud.varieties:
                                var_total.append(variety.variety_id)
                        mean_var_ud.append(np.mean(var_ud))
                        var_system.append(len(var_total))
                        unique_system.append(len(set(var_total)))
                        # Simulation
                        for t in range(1, tiempo):
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
                            if not uds_copy: #Extintion
                                # Only 0
                                print(f"acabó en 0 el experimento {contador+1} con herencia {inherits[i]} con mean {Gcalphas[j]}")
                                break         
                            # Cycle:
                            for id_ud, ud in uds_copy.items():
                                ud.ter_filho()
                                ud.buscar_ud(uds_copy, int(media), inherit, True, 0.2)
                                ud.incrementar_idade()
                                ud.death_probability(prob_morte)
                            # Collecting data
                            vivas_tasa_crecimiento.append(len([ud for id, ud in uds_copy.items() if ud.activa]))
                            if t % punto_vista == 0:
                                viv = len([ud for id, ud in uds_copy.items() if ud.activa])
                                vivas_puntos_vista.append(viv)
                                # For diversity
                                var_ud = []
                                var_total = []
                                for ud in [ud for ud in UD_generalized.uds.values() if ud.activa ==True]:
                                    var_ud.append(len(ud.varieties))
                                    for variety in ud.varieties:
                                        var_total.append(variety.variety_id)
                                mean_var_ud.append(np.mean(var_ud))
                                var_system.append(len(var_total))
                                unique_system.append(len(set(var_total))) 
                        viv = len([ud for id, ud in UD_generalized.uds.items() if ud.activa])
                        vivas_puntos_vista.append(viv)
                        # For diversity
                        var_ud = []
                        var_total = []
                        for ud in [ud for ud in UD_generalized.uds.values() if ud.activa ==True]:
                            var_ud.append(len(ud.varieties))
                            for variety in ud.varieties:
                                var_total.append(variety.variety_id)
                        mean_var_ud.append(np.mean(var_ud))
                        var_system.append(len(var_total))
                        unique_system.append(len(set(var_total)))
                        alive = (len([ud for id, ud in uds_copy.items() if ud.activa]))
                        if alive >= 1:   
                            total_varieties = []
                            varieties_per_UD = []
                            for ud in [ud for ud in UD_generalized.uds.values() if ud.activa ==True]:
                                varieties_per_UD.append(len(ud.varieties))
                                for variety in ud.varieties:
                                    total_varieties.append(variety.variety_id)
                            data_endo_mean_ud.append(np.mean(varieties_per_UD))
                            data_endo_com_level.append(len(set(total_varieties)))
                            data_endo_total_varieties.append(total_varieties)
                    else:# Now with inherit == False
                        #### Initialization
                        UD_generalized_al_inh.uds = {}
                        instancias_ud = []
                        for id_ud in range(1, int(m) + 1):
                            instancias_ud.append(UD_generalized_al_inh(id_ud, media, clans.pop()))
                        ## Varieties
                        limited_varieties = True
                        if limited_varieties == False:
                            for id_ud, ud in UD_generalized_al_inh.uds.items():
                                for _ in range(3):
                                    ud.varieties.append(Variety())
                        else:
                            initial_varieties = [Variety() for _ in range (10)]
                            for ud in UD_generalized_al_inh.uds.values():
                                for _ in range(3):
                                    ud.varieties.append(random.choice(initial_varieties))   
                        # Lists for graphs
                        vivas_puntos_vista = [int(m)]
                        vivas_tasa_crecimiento = [int(m)]
                        #For diversity
                        mean_var_ud = []
                        var_system = []
                        unique_system = []
                        var_ud = []
                        var_total = []
                        for ud in [ud for ud in UD_generalized_al_inh.uds.values() if ud.activa ==True]:
                            var_ud.append(len(ud.varieties))
                            for variety in ud.varieties:
                                var_total.append(variety.variety_id)
                        mean_var_ud.append(np.mean(var_ud))
                        var_system.append(len(var_total))
                        unique_system.append(len(set(var_total)))
                        # Simulation
                        for t in range(1, tiempo):
                            uds_copy = {id_ud: ud for id_ud, ud in UD_generalized_al_inh.uds.items() if ud.activa}
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
                            if not uds_copy: #Extintion
                                # Only 0
                                print(f"acabó en 0 el experimento {contador+1} con herencia {inherits[i]} con mean {Gcalphas[j]}")
                                break         
                            # Cycle:
                            varieties_list = [var for ud in uds_copy.values() for var in ud.varieties]
                            for id_ud, ud in uds_copy.items():
                                ud.ter_filho()
                                ud.buscar_ud(uds_copy, int(media), varieties_list, True, 3, 0.2)
                                ud.incrementar_idade()
                                ud.death_probability(prob_morte)
                            # Collecting data
                            vivas_tasa_crecimiento.append(len([ud for id, ud in uds_copy.items() if ud.activa]))
                            if t % punto_vista == 0:
                                viv = len([ud for id, ud in uds_copy.items() if ud.activa])
                                vivas_puntos_vista.append(viv)
                                # For diversity
                                var_ud = []
                                var_total = []
                                for ud in [ud for ud in UD_generalized_al_inh.uds.values() if ud.activa ==True]:
                                    var_ud.append(len(ud.varieties))
                                    for variety in ud.varieties:
                                        var_total.append(variety.variety_id)
                                mean_var_ud.append(np.mean(var_ud))
                                var_system.append(len(var_total))
                                unique_system.append(len(set(var_total))) 
                        viv = len([ud for id, ud in UD_generalized_al_inh.uds.items() if ud.activa])
                        vivas_puntos_vista.append(viv)
                        # For diversity
                        var_ud = []
                        var_total = []
                        for ud in [ud for ud in UD_generalized_al_inh.uds.values() if ud.activa ==True]:
                            var_ud.append(len(ud.varieties))
                            for variety in ud.varieties:
                                var_total.append(variety.variety_id)
                        mean_var_ud.append(np.mean(var_ud))
                        var_system.append(len(var_total))
                        unique_system.append(len(set(var_total)))
                        alive = (len([ud for id, ud in uds_copy.items() if ud.activa]))
                        if alive >= 1:   
                            total_varieties = []
                            varieties_per_UD = []
                            for ud in [ud for ud in UD_generalized_al_inh.uds.values() if ud.activa ==True]:
                                varieties_per_UD.append(len(ud.varieties))
                                for variety in ud.varieties:
                                    total_varieties.append(variety.variety_id)
                            data_endo_mean_ud.append(np.mean(varieties_per_UD))
                            data_endo_com_level.append(len(set(total_varieties)))
                            data_endo_total_varieties.append(total_varieties)
                    # Final collection of the data after the simulation!
                    if len(uds_copy) > 0:  # Only collect data if the system is alive
                        list_alive_UDs.append(len([ud for id, ud in uds_copy.items() if ud.activa == True]))  # For heatmap
                        list_vivas_puntos_vista.append(vivas_puntos_vista)
                        data_step_var_system.append(var_system)
                        data_step_unique_system.append(unique_system)
                        data_step_mean_var_ud.append(mean_var_ud)
                        contador += 1
                    iterations += 1
                    print('succesful', contador)
                    print('iterations', iterations)            
                    data_inherit_endo = [data_endo_mean_ud, data_endo_com_level, data_endo_total_varieties]
                data_steps_inherit_endo = [data_step_var_system, data_step_unique_system, data_step_mean_var_ud]
                media = original_media
                end_config = time.time()
                if contador == experiments:
                    cM[i][j] = {
                        'alive': np.mean(list_alive_UDs),
                        'lstd': np.std(list_alive_UDs),
                        'time used': end_config - star_configuration,
                        'percentage_extinction': contador / experiments,
                        'tempo': tempo, 
                        'mean': np.mean(list_vivas_puntos_vista, axis=0), 
                        'std': np.std(list_vivas_puntos_vista, axis=0),
                        'growth rate': np.mean([np.mean(lista) for lista in tasas_crecimiento]),
                        'diversity_info': data_inherit_endo,
                        'diversity_info_steps': data_steps_inherit_endo,
                    }
                else:  # Handle extinction-only scenarios
                    cM[i][j] = {
                        'alive': None,
                        'lstd': None,
                        'time used': end_config - star_configuration,
                        'percentage_extinction': 1.0,  # All experiments went extinct
                        'tempo': None, 
                        'mean': None, 
                        'std': None,
                        'growth rate': None,
                        'diversity_info': None,
                        'diversity_info_steps': None,
                    }
                print(f"""
        The total time of the configuration of inherit percentage {inherit} and initial UDs {m} and mean {media} is  {end_config - star_configuration}
                """)
        heat_std = os.path.join(folder_name, 'Generalized_Mean_children.npy')
        np.save(heat_std, cM)
        now = datetime.now()
        finish = time.time()
        print(f"""
        It finished at: {now}
        It lasted {finish-start}
        """)
        print("done")
        heat_std = os.path.join(folder_name, 'Generalized_Mean_children.npy')
        GcM_datos = np.load(heat_std, allow_pickle=True)
        plot = transversal_changes(GcM_datos, inherits, Gcalphas, 'Generalized', variable='Mean of Children')
        plot.savefig(os.path.join(folder_name, 'diversity_behavior.png'), dpi=300, bbox_inches="tight")
        plot = transversal_alive(GcM_datos, inherits, Gcalphas, 'Generalized', variable='Mean of Children')
        plot.savefig(os.path.join(folder_name, 'populational_behavior.png'), dpi=300, bbox_inches="tight")
    else:
        #sub folder
        folder_name = os.path.join(folder_name, 'Number of varieties for UD')
        # Create the sub-folder if it doesn't exist
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
        # This experiment has different values for Initial varieties mv NEW TRY!
        prob_morte = 0.06 #beta
        media = 4 # Mean
        m = 40
        mv = 10
        inherits = [0,25,50, 'False']
        Gmvalphas = np.linspace(1,mv,mv)# Mean varieties from 1 to mv
        # For data of behaviour
        vM = np.empty((len(inherits), len(Gmvalphas)), dtype=object)
        punto_vista = 50
        tiempo = 1000
        tempo = list(range(0,tiempo+1,punto_vista))
        experiments = 100
        max_iterations = 400
        print(vM.shape)
        start = time.time()
        print(f"started at:  {datetime.now()}")
        for i, inherit in enumerate(inherits):
            for j, mvarieties  in enumerate(Gmvalphas):
                star_configuration = time.time()
                #For population dynamics
                list_alive_UDs = []
                list_vivas_puntos_vista = []
                tasas_crecimiento = []
                #For diversity dynamics
                data_step_mean_var_ud = []
                data_step_var_system = []
                data_step_unique_system = []
                print(f"Experiments with inheritance {inherit} Initial UDs {m} and Mean varieties {mvarieties}")
                #Lists to store experiments' diversity data
                data_endo_mean_ud = []
                data_endo_com_level = []
                data_endo_total_varieties = []
                original_media = media
                contador = 0
                iterations = 0
                while contador < experiments and iterations < max_iterations:
                    print(f'experimento {contador+1}')
                    ## Clans
                    clans = (list(range(1, 4)) * (int(m) // 3 + 1))[:int(m)] # Just 3 clans
                    random.shuffle(clans)
                    if inherit != 'False':
                        #### Initialization
                        UD_generalized.uds = {}
                        instancias_ud = []
                        for id_ud in range(1, int(m) + 1):
                            instancias_ud.append(UD_generalized(id_ud, media, clans.pop()))
                        ## Varieties
                        limited_varieties = True
                        if limited_varieties == False:
                            for id_ud, ud in UD_generalized.uds.items():
                                for _ in range(3):
                                    ud.varieties.append(Variety())
                        else:
                            initial_varieties = [Variety() for _ in range (int(10))]
                            for ud in UD_generalized.uds.values():
                                for _ in range(int(mvarieties)):
                                    ud.varieties.append(random.choice(initial_varieties))   
                        # Lists for graphs
                        vivas_puntos_vista = [int(m)]
                        vivas_tasa_crecimiento = [int(m)]
                #             mortas_puntos_vista = [0]
                        #For diversity
                        mean_var_ud = []
                        var_system = []
                        unique_system = []
                        var_ud = []
                        var_total = []
                        for ud in [ud for ud in UD_generalized.uds.values() if ud.activa ==True]:
                            var_ud.append(len(ud.varieties))
                            for variety in ud.varieties:
                                var_total.append(variety.variety_id)
                        mean_var_ud.append(np.mean(var_ud))
                        var_system.append(len(var_total))
                        unique_system.append(len(set(var_total)))
                        # Simulation
                        for t in range(1, tiempo):
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
                            if not uds_copy: #Extintion
                                # Only 0
                                print(f"acabó en 0 el experimento {contador+1}")
                                break         
                            # Cycle:
                            for id_ud, ud in uds_copy.items():
                                ud.ter_filho()
                                ud.buscar_ud(uds_copy, int(media), inherit, True, 0.2)
                                ud.incrementar_idade()
                                ud.death_probability(prob_morte)
                            # Collecting data
                            vivas_tasa_crecimiento.append(len([ud for id, ud in uds_copy.items() if ud.activa]))
                            if t % punto_vista == 0:
                                viv = len([ud for id, ud in uds_copy.items() if ud.activa])
                                vivas_puntos_vista.append(viv)
                                # For diversity
                                var_ud = []
                                var_total = []
                                for ud in [ud for ud in UD_generalized.uds.values() if ud.activa ==True]:
                                    var_ud.append(len(ud.varieties))
                                    for variety in ud.varieties:
                                        var_total.append(variety.variety_id)
                                mean_var_ud.append(np.mean(var_ud))
                                var_system.append(len(var_total))
                                unique_system.append(len(set(var_total))) 
                        viv = len([ud for id, ud in UD_generalized.uds.items() if ud.activa])
                        vivas_puntos_vista.append(viv)
                        # For diversity
                        var_ud = []
                        var_total = []
                        for ud in [ud for ud in UD_generalized.uds.values() if ud.activa ==True]:
                            var_ud.append(len(ud.varieties))
                            for variety in ud.varieties:
                                var_total.append(variety.variety_id)
                        mean_var_ud.append(np.mean(var_ud))
                        var_system.append(len(var_total))
                        unique_system.append(len(set(var_total)))
                        alive = (len([ud for id, ud in uds_copy.items() if ud.activa]))
                        if alive >= 1:   
                            total_varieties = []
                            varieties_per_UD = []
                            for ud in [ud for ud in UD_generalized.uds.values() if ud.activa ==True]:
                                varieties_per_UD.append(len(ud.varieties))
                                for variety in ud.varieties:
                                    total_varieties.append(variety.variety_id)
                            data_endo_mean_ud.append(np.mean(varieties_per_UD))
                            data_endo_com_level.append(len(set(total_varieties)))
                            data_endo_total_varieties.append(total_varieties)
                    else:# Now with inherit == False
                        #### Initialization
                        UD_generalized_al_inh.uds = {}
                        instancias_ud = []
                        for id_ud in range(1, int(m) + 1):
                            instancias_ud.append(UD_generalized_al_inh(id_ud, media, clans.pop()))
                        ## Varieties
                        limited_varieties = True
                        if limited_varieties == False:
                            for id_ud, ud in UD_generalized_al_inh.uds.items():
                                for _ in range(3):
                                    ud.varieties.append(Variety())
                        else:
                            initial_varieties = [Variety() for _ in range (int(10))]
                            for ud in UD_generalized_al_inh.uds.values():
                                for _ in range(int(mvarieties)):
                                    ud.varieties.append(random.choice(initial_varieties))   
                        # Lists for graphs
                        vivas_puntos_vista = [int(m)]
                        vivas_tasa_crecimiento = [int(m)]
                        #For diversity
                        mean_var_ud = []
                        var_system = []
                        unique_system = []
                        var_ud = []
                        var_total = []
                        for ud in [ud for ud in UD_generalized_al_inh.uds.values() if ud.activa ==True]:
                            var_ud.append(len(ud.varieties))
                            for variety in ud.varieties:
                                var_total.append(variety.variety_id)
                        mean_var_ud.append(np.mean(var_ud))
                        var_system.append(len(var_total))
                        unique_system.append(len(set(var_total)))
                        # Simulation
                        for t in range(1, tiempo):
                            uds_copy = {id_ud: ud for id_ud, ud in UD_generalized_al_inh.uds.items() if ud.activa}
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
                            if not uds_copy: #Extintion
                                # Only 0
                                print(f"acabó en 0 el experimento {contador+1} con herencia {inherits[i]}")
                                break         
                            # Cycle:
                            varieties_list = [var for ud in uds_copy.values() for var in ud.varieties]
                            for id_ud, ud in uds_copy.items():
                                ud.ter_filho()
                                ud.buscar_ud(uds_copy, int(media), varieties_list, True, int(mvarieties), 0.2)
                                ud.incrementar_idade()
                                ud.death_probability(prob_morte)
                            # Collecting data
                            vivas_tasa_crecimiento.append(len([ud for id, ud in uds_copy.items() if ud.activa]))
                            if t % punto_vista == 0:
                                viv = len([ud for id, ud in uds_copy.items() if ud.activa])
                                vivas_puntos_vista.append(viv)
                                # For diversity
                                var_ud = []
                                var_total = []
                                for ud in [ud for ud in UD_generalized_al_inh.uds.values() if ud.activa ==True]:
                                    var_ud.append(len(ud.varieties))
                                    for variety in ud.varieties:
                                        var_total.append(variety.variety_id)
                                mean_var_ud.append(np.mean(var_ud))
                                var_system.append(len(var_total))
                                unique_system.append(len(set(var_total))) 
                        viv = len([ud for id, ud in UD_generalized_al_inh.uds.items() if ud.activa])
                        vivas_puntos_vista.append(viv)
                        # For diversity
                        var_ud = []
                        var_total = []
                        for ud in [ud for ud in UD_generalized_al_inh.uds.values() if ud.activa ==True]:
                            var_ud.append(len(ud.varieties))
                            for variety in ud.varieties:
                                var_total.append(variety.variety_id)
                        mean_var_ud.append(np.mean(var_ud))
                        var_system.append(len(var_total))
                        unique_system.append(len(set(var_total)))
                        alive = (len([ud for id, ud in uds_copy.items() if ud.activa]))
                        if alive >= 1:   
                            total_varieties = []
                            varieties_per_UD = []
                            for ud in [ud for ud in UD_generalized_al_inh.uds.values() if ud.activa ==True]:
                                varieties_per_UD.append(len(ud.varieties))
                                for variety in ud.varieties:
                                    total_varieties.append(variety.variety_id)
                            data_endo_mean_ud.append(np.mean(varieties_per_UD))
                            data_endo_com_level.append(len(set(total_varieties)))
                            data_endo_total_varieties.append(total_varieties)
                    # Final collection of the data after the simulation!
                    if len(uds_copy) > 0:  # Only collect data if the system is alive
                        list_alive_UDs.append(len([ud for id, ud in uds_copy.items() if ud.activa == True]))  # For heatmap
                        list_vivas_puntos_vista.append(vivas_puntos_vista)
                        data_step_var_system.append(var_system)
                        data_step_unique_system.append(unique_system)
                        data_step_mean_var_ud.append(mean_var_ud)
                        contador += 1
                    iterations += 1
                    print('succesful')
                    print(contador)
                    print('iterations')
                    print(iterations)
                    
                    data_inherit_endo = [data_endo_mean_ud, data_endo_com_level, data_endo_total_varieties]
                data_steps_inherit_endo = [data_step_var_system, data_step_unique_system, data_step_mean_var_ud]
                media = original_media
                end_config = time.time()
                
                if contador == experiments:
                    vM[i][j] = {
                        'alive': np.mean(list_alive_UDs),
                        'lstd': np.std(list_alive_UDs),
                        'time used': end_config - star_configuration,
                        'percentage_extinction': contador / experiments,
                        'tempo': tempo, 
                        'mean': np.mean(list_vivas_puntos_vista, axis=0), 
                        'std': np.std(list_vivas_puntos_vista, axis=0),
                        'growth rate': np.mean([np.mean(lista) for lista in tasas_crecimiento]),
                        'diversity_info': data_inherit_endo,
                        'diversity_info_steps': data_steps_inherit_endo,
                    }
                else:  # Handle extinction-only scenarios
                    vM[i][j] = {
                        'alive': None,
                        'lstd': None,
                        'time used': end_config - star_configuration,
                        'percentage_extinction': 1.0,  # All experiments went extinct
                        'tempo': None, 
                        'mean': None, 
                        'std': None,
                        'growth rate': None,
                        'diversity_info': None,
                        'diversity_info_steps': None,
                    }
                print(f"""
        The total time of the configuration of inherit percentage {inherit}, 
        initial UDs {m} and Mean varieties {mvarieties} is  {end_config - star_configuration}
                """)
        heat_std = os.path.join(folder_name, 'Generalized_Initial_Mean_varieties.npy')
        np.save(heat_std, vM)
        now = datetime.now()
        finish = time.time()
        print(f"""
        It finished at: {now}
        It lasted {finish-start}
        """)
        print("done")
        heat_std = os.path.join(folder_name, 'Generalized_Initial_Mean_varieties.npy')
        DmvM_datos = np.load(heat_std, allow_pickle=True)
        plot = transversal_changes(DmvM_datos, inherits, Dmvalphas, 'Generalized', variable='Mean varieties')
        plot.savefig(os.path.join(folder_name, 'diversity_behavior.png'), dpi=300, bbox_inches="tight")
        plot = transversal_alive(DmvM_datos, inherits, Dmvalphas, 'Generalized', variable='Mean varieties')
        plot.savefig(os.path.join(folder_name, 'populational_behavior.png'), dpi=300, bbox_inches="tight")