import numpy as np
from collections import Counter
import matplotlib.pyplot as plt

#Function to get
    #Total of UDs alive
    #Total # of the varieties in the system
    #Total of unique varieties in the system, i.e., diversity at the community level
    #Plot var of varieties' frequencies
def community_level_agrobiodiversity(UD):
    viv = 0
    variedades_unicas = set()
    variedades_total = []
    for id_ud, ud in UD.uds.items():
        if ud.activa:
            viv += 1
            for variedad in ud.varieties:
                variedades_total.append(variedad.vid)
                variedades_unicas.add(variedad.vid)
    # Print the result
    print(f"Total of alive UDs: {viv}")
    print(f"Total the varieties in the system: {len(variedades_total)}")
    print(f"Total of unic varieties: {len(variedades_unicas)}")
    #Frecuency table
    if len([ud for id, ud in UD.uds.items() if ud.activa == True]) > 0:
        # Get them in str
        todos_los_vid_str = list(map(str, variedades_total))
         # Frecuences using Counter
        frecuencias = Counter(todos_los_vid_str)
        # Get them in order
        claves_ordenadas, valores_ordenados = zip(*sorted(frecuencias.items(), key=lambda item: item[1],reverse=True))
         # Barplot
        plt.bar(claves_ordenadas, valores_ordenados)
         # Labels
        plt.xlabel('Variety')
        plt.ylabel('Frecuence')
        plt.title("Varieties' Frecuence")
        plt.xticks(rotation=90)
        # Mostrar el gráfico
        plt.show()
    else:
        print('Nothing to graph')
    print("----------------------------")
    
#Function to get
    #Mean unique varieties at the UD level
    #Plot bar of the unique varieties at the UD level
def UD_level_agrobiodiversity(UD):
    viv = 0
    varieties_UD = []
    for id_ud, ud in UD.uds.items():
        if ud.activa:
            viv += 1
            unique = set()
            for variety in ud.varieties:
                #print(variety.vid)
                unique.add(variety.vid)
            varieties_UD.append(len(unique))
    #print(varieties_UD)
    print(np.mean(varieties_UD))
    todos_los_vid_str = list(map(str, varieties_UD))
     # Frecuences using Counter
    frecuencias = Counter(todos_los_vid_str)
    # Get them in order
    claves_ordenadas, valores_ordenados = zip(*sorted(frecuencias.items(), key=lambda item: item[1],reverse=True))
     # Barplot
    plt.bar(claves_ordenadas, valores_ordenados)
     # Labels
    plt.xlabel('# of unique varieties')
    plt.ylabel('Frecuence')
    plt.title("Unique varieties' Frecuence")
    plt.xticks(rotation=90)
    plt.show()
    print("----------------------------")