import pandas as pd

#Document's format:
# If clan == True, it gets the clan.
    #List [step, id, age, parentes, community, clan (or not), varieties, variedades únicas]
def general_charactersitics_data(step, uds, dataset, final = False, clan = False):
    if clan == False: 
        if final == False:
            for ud in uds.values():
                dataset.append([step, ud.id, ud.age, ud.parentes, ud.community, ud.varieties])   
            return dataset
        else:
            df = pd.DataFrame(dataset)
            df.columns = ["Step", "ID", "Age", "Parents", "Community", "Varieties"]
            return df
    else:
        if final == False:
            for ud in uds.values():
                dataset.append([step, ud.id, ud.age, ud.parentes, ud.community, ud.clan, ud.varieties]) 
            return dataset
        else:
            df = pd.DataFrame(dataset)
            df.columns = ["Step", "ID", "Age", "Parents", "Community", "Clan", "Varieties"]
            return df

def generate_puck(uds, clan = False):
    if clan == False:
        puck_dataset_individuals = []
        puck_dataset_families = []
        for ud in uds.values():
            id_male = ud.male[0]
            name_male = f" H {ud.male[0]}"
            gender_male = "H"
            puck_dataset_individuals.append([id_male, name_male, gender_male])
            id_female = ud.female[0]
            name_female = f" F {ud.female[0]}"
            gender_female = "F"
            puck_dataset_individuals.append([id_female, name_female, gender_female])

            id_family = ud.id
            Status = "M"
            FatherID = ud.male[0]
            MotherID = ud.female[0]
            Children = ';'.join(map(str, ud.parentes[2]))
            puck_dataset_families.append([id_family, "M", FatherID, MotherID, Children])

        df_individuals = pd.DataFrame(puck_dataset_individuals, columns=["ID", "Name", "Gender"])
        df_families = pd.DataFrame(puck_dataset_families, columns=["ID", "Status", 'FatherID', "MotherID", "Children"])
        return df_individuals, df_families
    else:
        puck_dataset_individuals = []
        puck_dataset_families = []
        for ud in uds.values():
            id_male = ud.male[0]
            clan_male = ud.male[1]
            name_male = f" H {ud.male[0]}"
            gender_male = "H"
            puck_dataset_individuals.append([id_male, name_male, gender_male, clan_male])
            id_female = ud.female[0]
            clan_female = ud.female[1]
            name_female = f" F {ud.female[0]}"
            gender_female = "F"
            puck_dataset_individuals.append([id_female, name_female, gender_female, clan_female])

            id_family = ud.id
            Status = "M"
            FatherID = ud.male[0]
            MotherID = ud.female[0]
            Children = ';'.join(map(str, ud.parentes[2]))
            puck_dataset_families.append([id_family, "M", FatherID, MotherID, Children])

        df_individuals = pd.DataFrame(puck_dataset_individuals, columns=["ID", "Name", "Gender", "Clan"])
        df_families = pd.DataFrame(puck_dataset_families, columns=["ID", "Status", 'FatherID', "MotherID", "Children"])
        return df_individuals, df_families