import numpy as np
import pandas as pd
import random
import matplotlib.pyplot as plt
import seaborn as sns
# - Diversit measures y of different vareties at the Clan Level Beta

def div_com_clan_gamma_alfa_beta(matriz, n=1, clans=True):
    num_varieties = len(matriz[0])
    N_farms = len(matriz) // n

    result = {}
    # Clan diversity
    if clans:
        clan_A = [farm for i, farm in enumerate(matriz) if i % 2 == 0]
        clan_B = [farm for i, farm in enumerate(matriz) if i % 2 != 0]

        div_A = sum(
            1 for j in range(num_varieties)
            if any(farm[j][0] >= 1 for farm in clan_A)
        )

        div_B = sum(
            1 for j in range(num_varieties)
            if any(farm[j][0] >= 1 for farm in clan_B)
        )

        result['div_A'] = div_A
        result['div_B'] = div_B


    # Gamma diversity (total)

    gamma = sum(
        1 for j in range(num_varieties)
        if any(matriz[i][j][0] >= 1 for i in range(len(matriz)))
    )

    result['div_total'] = gamma


    # Alpha and Beta clan
    if clans:
        alpha_clan = (div_A + div_B) / 2
        beta_clan = gamma / alpha_clan if alpha_clan > 0 else np.nan 

        result['alpha_clan'] = alpha_clan
        result['beta_clan'] = beta_clan

    # Community diversity

    community_divs = []
    if n > 1:
        for c in range(n):
            community_farms = matriz[c * N_farms : (c + 1) * N_farms]

            div_com = sum(
                1 for j in range(num_varieties)
                if any(farm[j][0] >= 1 for farm in community_farms)
            )

            result[f'div_com_{c}'] = div_com
            community_divs.append(div_com)

        alpha_com = sum(community_divs) / len(community_divs)
        beta_com = gamma / alpha_com if alpha_com > 0 else np.nan
        result['alpha_com'] = alpha_com
        result['beta_com'] = beta_com

    return result

# - Jaccard community and Clan

def jaccard_clan_com(matriz, n=1, clans=True):

    num_varieties = len(matriz[0])
    N_farms = len(matriz) // n

    result = {}

    # JACCARD CLANS

    if clans:

        clan_A = [farm for i, farm in enumerate(matriz) if i % 2 == 0]
        clan_B = [farm for i, farm in enumerate(matriz) if i % 2 != 0]

        set_A = set()
        set_B = set()

        for j in range(num_varieties):

            if any(farm[j][0] >= 1 for farm in clan_A):
                set_A.add(j)

            if any(farm[j][0] >= 1 for farm in clan_B):
                set_B.add(j)

        intersection = len(set_A.intersection(set_B))
        union = len(set_A.union(set_B))

        result['jaccard_clan'] = (
            intersection / union if union > 0 else 0
        )


    # JACCARD  COMMUNITIES

    if n > 1:
        community_sets = []

        for c in range(n):
            community_farms = matriz[c * N_farms : (c + 1) * N_farms]
            variety_set = set()

            for j in range(num_varieties):
                if any(farm[j][0] >= 1 for farm in community_farms):
                    variety_set.add(j)

            community_sets.append(variety_set)

        for i in range(n):
            for j in range(i + 1, n):
                intersection = len(community_sets[i].intersection(community_sets[j]))
                union        = len(community_sets[i].union(community_sets[j]))
                result[f'jaccard_com_{i}_{j}'] = (
                    intersection / union if union > 0 else 0
                )

    return result

##################################### VISUALIZATION.
# Simple graph, uses a list . One simulation 
def simple_graph(data):
    time      = [d['time']      for d in data]
    diversity = [d['diversity'] for d in data]
    plt.plot(time, diversity, marker='o')
    plt.xlabel('Time')
    plt.ylabel('Diversity')
    plt.title('Community Diversity Over Time')

# Heatmap. It uses a list, so its for one simulation only
def plot_heatmap(data):
    """
This plot shows a heatmap of the distribution of the diversity. When we have different communitites and distribute the varieties accordingly, you can use it after the initialization to amaze yourselve at the distribution! :D
    """
    # Flatten the innermost lists (each cell is a single-element list)
    matrix = np.array([[cell[0] for cell in row] for row in data])

    plt.figure(figsize=(14, 6))

    sns.heatmap(
        matrix,
        annot=True,
        fmt="d",
        cmap="YlOrRd",
        linewidths=0.5,
        linecolor="gray",
        cbar_kws={"label": "Value"},
        vmin=0,
        vmax=matrix.max()
    )

    plt.title("Heatmap", fontsize=14, fontweight="bold", pad=12)
    plt.xlabel("Column Index")
    plt.ylabel("Row Index")
    plt.tight_layout()

# plot all simulations. Uses dataframe
def plot_all_sim(data):
    for s, group in data.groupby('simulation'):
        plt.plot(group['time'], group['div_total'], alpha=0.2, color='blue')

# plat mean across simulations. Uses dataframe
def plot_mean_simul (data):
    mean = data.groupby('time')['div_total'].mean()
    std = data.groupby('time')['div_total'].std()
    plt.plot(mean, label='mean')
    plt.fill_between(mean.index, mean - std, mean + std, alpha=0.3, label='±1 std')
    plt.xlabel('Time')
    plt.ylabel('Diversity')
    plt.legend()

############################################## Initialization
################################ Different varieties for community
def init_bench_sum(N=20, n=1, v_total=30, initial_var=9, seed=None):
    """
    Initialization for N farms and n communities.
    v_total is the TOTAL number of varieties across the system.
    Each community gets v_total // n varieties, always exclusive to that community.
    """
    if seed is not None:
        random.seed(seed)

    varieties_per_com = v_total // n 

    matriz = [[[0] for _ in range(v_total)] for _ in range(N * n)]

    for i in range(N * n):
        community_idx = i // N
        offset        = community_idx * varieties_per_com

        for _ in range(initial_var):
            pos = offset + random.choice(range(varieties_per_com))
            matriz[i][pos][0] += 1

    return matriz

def init_bench_sum_clan(N=20, n=1, v_total=30, initial_var=9, seed=None):
    if seed is not None:
        random.seed(seed)

    clan_offset = 15

    matriz = [[[0] for _ in range(v_total)] for _ in range(N * n)]

    for i in range(N * n):
        # Clan según paridad del índice dentro de la comunidad
        local_idx = i % N
        clan_shift = clan_offset if local_idx % 2 == 0 else 0

        for _ in range(initial_var):
            pos = clan_shift + random.choice(range(clan_offset))
            matriz[i][pos][0] += 1

    return matriz

################################ 
################### ENDOGAMY
####### Cross 100
def simul_cross_100_EN(matriz, steps=100, n=1):
    data = []

    div_dict     = div_com_clan_gamma_alfa_beta(matriz, n=n, clans=False)
    jaccard_dict = jaccard_clan_com(matriz, n=n, clans=False)
    data.append({
        'time'  : 0,
        'matriz': np.array(matriz).copy(),
        **div_dict,
        **jaccard_dict
    })

    for t in range(1, steps + 1):
        daughters = [random.randint(1, 3) for _ in range(len(matriz))]
        sons      = [random.randint(1, 3) for _ in range(len(matriz))]

        farm_order = list(range(len(matriz)))
        random.shuffle(farm_order)

        for farm in farm_order:
            origin = [i for i, spot in enumerate(matriz[farm]) if spot[0] > 0]

            candidates = [i for i in range(len(matriz)) if i != farm and sons[i] > 0]
            n_others   = min(daughters[farm], len(candidates))

            if n_others == 0:
                for _ in range(3):
                    origin = [i for i, spot in enumerate(matriz[farm]) if spot[0] > 0]
                    pos_remove = random.choice(origin)
                    matriz[farm][pos_remove][0] -= 1

                    origin = [i for i, spot in enumerate(matriz[farm]) if spot[0] > 0]
                    pos_add = random.choice(origin)
                    matriz[farm][pos_add][0] += 1
                continue

            others = random.sample(candidates, n_others)

            for other_farm in others:
                sons[other_farm] -= 1

                for _ in range(3):
                    origin   = [i for i, spot in enumerate(matriz[farm])       if spot[0] > 0]
                    receiver = [i for i, spot in enumerate(matriz[other_farm]) if spot[0] > 0]

                    pos_delete = random.choice(receiver)
                    pos_pass   = random.choice(origin)

                    matriz[other_farm][pos_delete][0] -= 1
                    matriz[other_farm][pos_pass][0]   += 1

        if t % 1 == 0:
            div_dict     = div_com_clan_gamma_alfa_beta(matriz, n=n, clans=False)
            jaccard_dict = jaccard_clan_com(matriz, n=n, clans=False)
            data.append({
                'time'  : t,
                'matriz': np.array(matriz).copy(),
                **div_dict,
                **jaccard_dict
            })

    return data, matriz

### Cross 66
def simul_cross_66_EN(matriz, steps=100, n=1):
    data = []

    div_dict     = div_com_clan_gamma_alfa_beta(matriz, n=n, clans=False)
    jaccard_dict = jaccard_clan_com(matriz, n=n, clans=False)
    data.append({
        'time'  : 0,
        'matriz': np.array(matriz).copy(),
        **div_dict,
        **jaccard_dict
    })

    for t in range(1, steps + 1):
        daughters = [random.randint(1, 3) for _ in range(len(matriz))]
        sons      = [random.randint(1, 3) for _ in range(len(matriz))]

        farm_order = list(range(len(matriz)))
        random.shuffle(farm_order)

        for farm in farm_order:
            origin = [i for i, spot in enumerate(matriz[farm]) if spot[0] > 0]

            candidates = [i for i in range(len(matriz)) if i != farm and sons[i] > 0]
            n_others   = min(daughters[farm], len(candidates))

            if n_others == 0:
                for _ in range(3):
                    origin = [i for i, spot in enumerate(matriz[farm]) if spot[0] > 0]
                    pos_remove = random.choice(origin)
                    matriz[farm][pos_remove][0] -= 1

                    origin = [i for i, spot in enumerate(matriz[farm]) if spot[0] > 0]
                    pos_add = random.choice(origin)
                    matriz[farm][pos_add][0] += 1
                continue

            others = random.sample(candidates, n_others)

            for other_farm in others:
                sons[other_farm] -= 1

                # 3 deletes — uno a la vez recalculando receiver
                for _ in range(3):
                    receiver = [i for i, spot in enumerate(matriz[other_farm]) if spot[0] > 0]
                    if not receiver:
                        break
                    pos = random.choice(receiver)
                    matriz[other_farm][pos][0] -= 1

                # 1 reinforce — desde receiver
                receiver = [i for i, spot in enumerate(matriz[other_farm]) if spot[0] > 0]
                if receiver:
                    pos = random.choice(receiver)
                    matriz[other_farm][pos][0] += 1

                # 2 pass — desde origin (columnas del farm) hacia other_farm
                for _ in range(2):
                    origin = [i for i, spot in enumerate(matriz[farm]) if spot[0] > 0]
                    if not origin:
                        break
                    pos = random.choice(origin)
                    matriz[other_farm][pos][0] += 1

        if t % 1 == 0:
            div_dict     = div_com_clan_gamma_alfa_beta(matriz, n=n, clans=False)
            jaccard_dict = jaccard_clan_com(matriz, n=n, clans=False)
            data.append({
                'time'  : t,
                'matriz': np.array(matriz).copy(),
                **div_dict,
                **jaccard_dict
            })

    return data, matriz

### Cross 33
def simul_cross_33_EN(matriz, steps=100, n=1):
    data = []

    div_dict     = div_com_clan_gamma_alfa_beta(matriz, n=n, clans=False)
    jaccard_dict = jaccard_clan_com(matriz, n=n, clans=False)
    data.append({
        'time'  : 0,
        'matriz': np.array(matriz).copy(),
        **div_dict,
        **jaccard_dict
    })

    for t in range(1, steps + 1):
        daughters = [random.randint(1, 3) for _ in range(len(matriz))]
        sons      = [random.randint(1, 3) for _ in range(len(matriz))]

        farm_order = list(range(len(matriz)))
        random.shuffle(farm_order)

        for farm in farm_order:
            origin = [i for i, spot in enumerate(matriz[farm]) if spot[0] > 0]

            candidates = [i for i in range(len(matriz)) if i != farm and sons[i] > 0]
            n_others   = min(daughters[farm], len(candidates))

            if n_others == 0:
                for _ in range(3):
                    origin = [i for i, spot in enumerate(matriz[farm]) if spot[0] > 0]
                    pos_remove = random.choice(origin)
                    matriz[farm][pos_remove][0] -= 1

                    origin = [i for i, spot in enumerate(matriz[farm]) if spot[0] > 0]
                    pos_add = random.choice(origin)
                    matriz[farm][pos_add][0] += 1
                continue

            others = random.sample(candidates, n_others)

            for other_farm in others:
                sons[other_farm] -= 1

                # 3 deletes — uno a la vez recalculando receiver
                for _ in range(3):
                    receiver = [i for i, spot in enumerate(matriz[other_farm]) if spot[0] > 0]
                    if not receiver:
                        break
                    pos = random.choice(receiver)
                    matriz[other_farm][pos][0] -= 1

                # 2 reinforce — desde receiver
                for _ in range(2):
                    receiver = [i for i, spot in enumerate(matriz[other_farm]) if spot[0] > 0]
                    if not receiver:
                        break
                    pos = random.choice(receiver)
                    matriz[other_farm][pos][0] += 1

                # 1 pass — desde origin (columnas del farm) hacia other_farm
                origin = [i for i, spot in enumerate(matriz[farm]) if spot[0] > 0]
                if origin:
                    pos = random.choice(origin)
                    matriz[other_farm][pos][0] += 1

        if t % 1 == 0:
            div_dict     = div_com_clan_gamma_alfa_beta(matriz, n=n, clans=False)
            jaccard_dict = jaccard_clan_com(matriz, n=n, clans=False)
            data.append({
                'time'  : t,
                'matriz': np.array(matriz).copy(),
                **div_dict,
                **jaccard_dict
            })

    return data, matriz

################### Simulation parallel. This means that is either matrilocal and matrilinear or patrilocal and patrilinear
def simul_paralel_EN(matriz, steps=100, n=1):
    data = []

    div_dict     = div_com_clan_gamma_alfa_beta(matriz, n=n, clans=False)
    jaccard_dict = jaccard_clan_com(matriz, n=n, clans=False)
    data.append({
        'time'  : 0,
        'matriz': np.array(matriz).copy(),
        **div_dict,
        **jaccard_dict
    })

    for t in range(1, steps + 1):
        daughters = [random.randint(1, 3) for _ in range(len(matriz))]
        sons      = [random.randint(1, 3) for _ in range(len(matriz))]

        farm_order = list(range(len(matriz)))
        random.shuffle(farm_order)

        for farm in farm_order:
            candidates = [i for i in range(len(matriz)) if i != farm and sons[i] > 0]
            n_others   = min(daughters[farm], len(candidates))

            if n_others == 0:
                for _ in range(3):
                    own_active = [i for i, spot in enumerate(matriz[farm]) if spot[0] > 0]
                    pos_remove = random.choice(own_active)
                    matriz[farm][pos_remove][0] -= 1

                    own_active = [i for i, spot in enumerate(matriz[farm]) if spot[0] > 0]
                    pos_add = random.choice(own_active)
                    matriz[farm][pos_add][0] += 1
                continue

            others = random.sample(candidates, n_others)

            for other_farm in others:
                sons[other_farm] -= 1

                for _ in range(3):
                    own_active = [i for i, spot in enumerate(matriz[farm]) if spot[0] > 0]
                    pos_remove = random.choice(own_active)
                    matriz[farm][pos_remove][0] -= 1

                    own_active = [i for i, spot in enumerate(matriz[farm]) if spot[0] > 0]
                    pos_add = random.choice(own_active)
                    matriz[farm][pos_add][0] += 1

        if t % 1 == 0:
            div_dict     = div_com_clan_gamma_alfa_beta(matriz, n=n, clans=False)
            jaccard_dict = jaccard_clan_com(matriz, n=n, clans=False)
            data.append({
                'time'  : t,
                'matriz': np.array(matriz).copy(),
                **div_dict,
                **jaccard_dict
            })

    return data, matriz

################### DUAL ORGANIZATION
####### Cross 100
def simul_cross_100_DU(matriz, steps=100, n=1):
    data = []

    div_dict     = div_com_clan_gamma_alfa_beta(matriz, n=n, clans=True)
    jaccard_dict = jaccard_clan_com(matriz, n=n, clans=True)
    data.append({
        'time'  : 0,
        'matriz': np.array(matriz).copy(),
        **div_dict,
        **jaccard_dict
    })

    for t in range(1, steps + 1):
        daughters = [random.randint(1, 3) for _ in range(len(matriz))]
        sons      = [random.randint(1, 3) for _ in range(len(matriz))]

        farm_order = list(range(len(matriz)))
        random.shuffle(farm_order)

        for farm in farm_order:
            origin = [i for i, spot in enumerate(matriz[farm]) if spot[0] > 0]

            opposite_clan = [i for i in range(len(matriz)) if i % 2 != farm % 2]
            same_clan     = [i for i in range(len(matriz)) if i % 2 == farm % 2 and i != farm]

            married_any = False

            for _ in range(daughters[farm]):
                allowed = [i for i in opposite_clan if sons[i] > 0]
                incest  = [i for i in same_clan     if sons[i] > 0]

                if random.random() < 0.2 and len(incest) > 0:
                    candidates = incest
                elif len(allowed) > 0:
                    candidates = allowed
                else:
                    candidates = []

                if len(candidates) == 0:
                    continue

                other_farm = random.choice(candidates)
                sons[other_farm] -= 1
                married_any = True

                for _ in range(3):
                    origin   = [i for i, spot in enumerate(matriz[farm])       if spot[0] > 0]
                    receiver = [i for i, spot in enumerate(matriz[other_farm]) if spot[0] > 0]

                    pos_delete = random.choice(receiver)
                    pos_pass   = random.choice(origin)

                    matriz[other_farm][pos_delete][0] -= 1
                    matriz[other_farm][pos_pass][0]   += 1

            if not married_any:
                for _ in range(3):
                    origin = [i for i, spot in enumerate(matriz[farm]) if spot[0] > 0]
                    pos_remove = random.choice(origin)
                    matriz[farm][pos_remove][0] -= 1

                    origin = [i for i, spot in enumerate(matriz[farm]) if spot[0] > 0]
                    pos_add = random.choice(origin)
                    matriz[farm][pos_add][0] += 1

        if t % 1 == 0:
            div_dict     = div_com_clan_gamma_alfa_beta(matriz, n=n, clans=True)
            jaccard_dict = jaccard_clan_com(matriz, n=n, clans=True)
            data.append({
                'time'  : t,
                'matriz': np.array(matriz).copy(),
                **div_dict,
                **jaccard_dict
            })

    return data, matriz

### Cross 66
def simul_cross_66_DU(matriz, steps=100, n=1):
    data = []

    div_dict     = div_com_clan_gamma_alfa_beta(matriz, n=n, clans=True)
    jaccard_dict = jaccard_clan_com(matriz, n=n, clans=True)
    data.append({
        'time'  : 0,
        'matriz': np.array(matriz).copy(),
        **div_dict,
        **jaccard_dict
    })

    for t in range(1, steps + 1):
        daughters = [random.randint(1, 3) for _ in range(len(matriz))]
        sons      = [random.randint(1, 3) for _ in range(len(matriz))]

        farm_order = list(range(len(matriz)))
        random.shuffle(farm_order)

        for farm in farm_order:
            origin = [i for i, spot in enumerate(matriz[farm]) if spot[0] > 0]

            opposite_clan = [i for i in range(len(matriz)) if i % 2 != farm % 2]
            same_clan     = [i for i in range(len(matriz)) if i % 2 == farm % 2 and i != farm]

            married_any = False

            for _ in range(daughters[farm]):
                allowed = [i for i in opposite_clan if sons[i] > 0]
                incest  = [i for i in same_clan     if sons[i] > 0]

                if random.random() < 0.2 and len(incest) > 0:
                    candidates = incest
                elif len(allowed) > 0:
                    candidates = allowed
                else:
                    candidates = []

                if len(candidates) == 0:
                    continue

                other_farm = random.choice(candidates)
                sons[other_farm] -= 1
                married_any = True

                # 3 deletes — uno a la vez recalculando receiver
                for _ in range(3):
                    receiver = [i for i, spot in enumerate(matriz[other_farm]) if spot[0] > 0]
                    if not receiver:
                        break
                    pos = random.choice(receiver)
                    matriz[other_farm][pos][0] -= 1

                # 1 reinforce — desde receiver
                receiver = [i for i, spot in enumerate(matriz[other_farm]) if spot[0] > 0]
                if receiver:
                    pos = random.choice(receiver)
                    matriz[other_farm][pos][0] += 1

                # 2 pass — desde origin hacia other_farm
                for _ in range(2):
                    origin = [i for i, spot in enumerate(matriz[farm]) if spot[0] > 0]
                    if not origin:
                        break
                    pos = random.choice(origin)
                    matriz[other_farm][pos][0] += 1

            if not married_any:
                for _ in range(3):
                    origin = [i for i, spot in enumerate(matriz[farm]) if spot[0] > 0]
                    pos_remove = random.choice(origin)
                    matriz[farm][pos_remove][0] -= 1

                    origin = [i for i, spot in enumerate(matriz[farm]) if spot[0] > 0]
                    pos_add = random.choice(origin)
                    matriz[farm][pos_add][0] += 1

        if t % 1 == 0:
            div_dict     = div_com_clan_gamma_alfa_beta(matriz, n=n, clans=True)
            jaccard_dict = jaccard_clan_com(matriz, n=n, clans=True)
            data.append({
                'time'  : t,
                'matriz': np.array(matriz).copy(),
                **div_dict,
                **jaccard_dict
            })

    return data, matriz

### Cros 33 
def simul_cross_33_DU(matriz, steps=100, n=1):
    data = []

    div_dict     = div_com_clan_gamma_alfa_beta(matriz, n=n, clans=True)
    jaccard_dict = jaccard_clan_com(matriz, n=n, clans=True)
    data.append({
        'time'  : 0,
        'matriz': np.array(matriz).copy(),
        **div_dict,
        **jaccard_dict
    })

    for t in range(1, steps + 1):
        daughters = [random.randint(1, 3) for _ in range(len(matriz))]
        sons      = [random.randint(1, 3) for _ in range(len(matriz))]

        farm_order = list(range(len(matriz)))
        random.shuffle(farm_order)

        for farm in farm_order:
            origin = [i for i, spot in enumerate(matriz[farm]) if spot[0] > 0]

            opposite_clan = [i for i in range(len(matriz)) if i % 2 != farm % 2]
            same_clan     = [i for i in range(len(matriz)) if i % 2 == farm % 2 and i != farm]

            married_any = False

            for _ in range(daughters[farm]):
                allowed = [i for i in opposite_clan if sons[i] > 0]
                incest  = [i for i in same_clan     if sons[i] > 0]

                if random.random() < 0.2 and len(incest) > 0:
                    candidates = incest
                elif len(allowed) > 0:
                    candidates = allowed
                else:
                    candidates = []

                if len(candidates) == 0:
                    continue

                other_farm = random.choice(candidates)
                sons[other_farm] -= 1
                married_any = True

                # 3 deletes — uno a la vez recalculando receiver
                for _ in range(3):
                    receiver = [i for i, spot in enumerate(matriz[other_farm]) if spot[0] > 0]
                    if not receiver:
                        break
                    pos = random.choice(receiver)
                    matriz[other_farm][pos][0] -= 1

                # 2 reinforce — desde receiver
                for _ in range(2):
                    receiver = [i for i, spot in enumerate(matriz[other_farm]) if spot[0] > 0]
                    if not receiver:
                        break
                    pos = random.choice(receiver)
                    matriz[other_farm][pos][0] += 1

                # 1 pass — desde origin hacia other_farm
                origin = [i for i, spot in enumerate(matriz[farm]) if spot[0] > 0]
                if origin:
                    pos = random.choice(origin)
                    matriz[other_farm][pos][0] += 1

            if not married_any:
                for _ in range(3):
                    origin = [i for i, spot in enumerate(matriz[farm]) if spot[0] > 0]
                    pos_remove = random.choice(origin)
                    matriz[farm][pos_remove][0] -= 1

                    origin = [i for i, spot in enumerate(matriz[farm]) if spot[0] > 0]
                    pos_add = random.choice(origin)
                    matriz[farm][pos_add][0] += 1

        if t % 1 == 0:
            div_dict     = div_com_clan_gamma_alfa_beta(matriz, n=n, clans=True)
            jaccard_dict = jaccard_clan_com(matriz, n=n, clans=True)
            data.append({
                'time'  : t,
                'matriz': np.array(matriz).copy(),
                **div_dict,
                **jaccard_dict
            })

    return data, matriz

### Simulation parallel. This means that is either matrilocal and matrilinear or patrilocal and patrilinear
def simul_paralel_DU(matriz, steps=100, n=1):
    data = []

    div_dict     = div_com_clan_gamma_alfa_beta(matriz, n=n, clans=True)
    jaccard_dict = jaccard_clan_com(matriz, n=n, clans=True)
    data.append({
        'time'  : 0,
        'matriz': np.array(matriz).copy(),
        **div_dict,
        **jaccard_dict
    })

    for t in range(1, steps + 1):
        daughters = [random.randint(1, 3) for _ in range(len(matriz))]
        sons      = [random.randint(1, 3) for _ in range(len(matriz))]

        farm_order = list(range(len(matriz)))
        random.shuffle(farm_order)

        for farm in farm_order:
            opposite_clan = [i for i in range(len(matriz)) if i % 2 != farm % 2]
            same_clan     = [i for i in range(len(matriz)) if i % 2 == farm % 2 and i != farm]

            married_any = False

            for _ in range(daughters[farm]):
                allowed = [i for i in opposite_clan if sons[i] > 0]
                incest  = [i for i in same_clan     if sons[i] > 0]

                if random.random() < 0.2 and len(incest) > 0:
                    candidates = incest
                elif len(allowed) > 0:
                    candidates = allowed
                else:
                    candidates = []

                if len(candidates) == 0:
                    continue

                other_farm = random.choice(candidates)
                sons[other_farm] -= 1
                married_any = True

                for _ in range(3):
                    own_active = [i for i, spot in enumerate(matriz[farm]) if spot[0] > 0]
                    pos_remove = random.choice(own_active)
                    matriz[farm][pos_remove][0] -= 1

                    own_active = [i for i, spot in enumerate(matriz[farm]) if spot[0] > 0]
                    pos_add = random.choice(own_active)
                    matriz[farm][pos_add][0] += 1

            if not married_any:
                for _ in range(3):
                    own_active = [i for i, spot in enumerate(matriz[farm]) if spot[0] > 0]
                    pos_remove = random.choice(own_active)
                    matriz[farm][pos_remove][0] -= 1

                    own_active = [i for i, spot in enumerate(matriz[farm]) if spot[0] > 0]
                    pos_add = random.choice(own_active)
                    matriz[farm][pos_add][0] += 1

        if t % 1 == 0:
            div_dict     = div_com_clan_gamma_alfa_beta(matriz, n=n, clans=True)
            jaccard_dict = jaccard_clan_com(matriz, n=n, clans=True)
            data.append({
                'time'  : t,
                'matriz': np.array(matriz).copy(),
                **div_dict,
                **jaccard_dict
            })

    return data, matriz

#### Para varias simulaciones sin comunidades
def various_simul(simul_func, N=20, v_total=30, steps=30, simulations=100, n=1, com_init = True):
    all_data = []
    for s in range(simulations):
        if com_init:
            matriz = init_bench_sum(N=N, v_total=v_total, n=n)
        else:
            matriz = init_bench_sum_clan(N=N, v_total=v_total, n=n)
        data, _ = simul_func(matriz, steps=steps, n=n)
        for record in data:
            record['simulation'] = s
            record['n']          = n
            record['func']       = simul_func.__name__
            record['init'] = 'com' if com_init else 'clan'
            all_data.append(record)
    return pd.DataFrame(all_data)

def plot_mean_simul_test(datasets: list, col: str, extinction_time: int = 15):
    fig, ax = plt.subplots(figsize=(10, 5))

    for i, data in enumerate(datasets):
        mean = data.groupby('time')[col].mean()
        std  = data.groupby('time')[col].std()

        ax.plot(mean, label=f'Dataset {i}')
        ax.fill_between(mean.index, mean - std, mean + std, alpha=0.2)

    # Vertical line at extinction time
    ax.axvline(x=extinction_time, color='red', linestyle='--', linewidth=1.5, label=f'Extinction (t={extinction_time})')

    # Red shading for everything to the right
    ax.axvspan(extinction_time, ax.get_xlim()[1], color='red', alpha=0.08)

    ax.set_xlabel('Time')
    ax.set_ylabel(col)
    ax.set_title(f'{col} over time')
    ax.legend()
    plt.tight_layout()
    plt.show()


######################### All config Experiments Com init distribution
def exp_com_init_distrib(save_path = 'local-kin-transmission-model/output/df_final_com_init.pkl'):
    communities = [1,2,3]
    functions = [simul_cross_100_EN, 
    simul_cross_66_EN, simul_cross_33_EN, simul_paralel_EN, 
    simul_cross_100_DU, simul_cross_66_DU, simul_cross_33_DU, simul_paralel_DU]
    all_dfs = []
    for funct in functions:
        for n in communities:
            df = various_simul(funct, n=n, simulations=100, steps=150)
            all_dfs.append(df)

    df_final_original_com = pd.concat(all_dfs, ignore_index=True)
    df_final_original_com.to_pickle(save_path)

######################### All config Experiments clan init distribution
def exp_clan_init_distrib(save_path = 'local-kin-transmission-model\output\df_final_clan_init.pkl'):
    communities = [1,2,3]
    functions = [simul_cross_100_DU, simul_cross_66_DU, simul_cross_33_DU, simul_paralel_DU]
    all_dfs = []
    for funct in functions:
        for n in communities:
            df = various_simul(funct, n=n, simulations=100, steps=150, com_init=False)
            all_dfs.append(df)

    df_final_original_clan = pd.concat(all_dfs, ignore_index=True)
    df_final_original_clan.to_pickle(save_path)

# Call them if you want!
if __name__ == "__main__":
    exp_com_init_distrib()
    #df_final_original_clan = pd.read_pickle('local-kin-transmission-model\output\df_final_clan_init.pkl')
    exp_clan_init_distrib()
    #df_final_original_com = pd.read_pickle('local-kin-transmission-model\output\df_final_test.pkl')
