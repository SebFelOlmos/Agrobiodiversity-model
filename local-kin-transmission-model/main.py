from model import *
from plots import *
import pandas as pd 

print("Welcome to the Local Kin Transmission Model!")
print("\nWhat would you like to do?")
print("  1. Run simulations")
print("  2. Plot results")

action = input("\nOption (1/2): ").strip()

if action == "1":
    print("\nWhich experiment would you like to run?")
    print("  1. Community init")
    print("  2. Clan init")
    print("  3. Both")

    choice = input("\nOption (1/2/3): ").strip()

    if choice == "1":
        print("LEts go! Community init")
        exp_com_init_distrib(save_path='output/df_final_com_init.pkl')
        print("Its over! Look the results in the outputs")
    elif choice == "2":
        print("LEts go! Clan init")
        exp_clan_init_distrib('output/df_final_clan_init.pkl')
        print("Its over! Look the results in the outputs")
    elif choice == "3":
        print("LEts go! Community init")
        exp_com_init_distrib(save_path='output/df_final_com_init.pkl')
        print("OK, now lets go! Clan init")
        exp_clan_init_distrib('output/df_final_clan_init.pkl')
        print("Its over! Look the results in the outputs")
    else:
        print("Invalid option. Do it again")

    print("\nSimulations done! Would you like to plot the results?")
    plot = input("(yes/no): ").strip().lower()
    if plot in ("yes", "y"):
        pass
    
elif action == "2":
    df_com = pd.read_pickle('output/df_final_com_init.pkl')
    df_clan = pd.read_pickle('output/df_final_clan_init.pkl')
    print("Here we have a lot of plots... So if you want to see the specfic ones, you must go to the plots.py code")
    print("Remember, they already exist in the output folder. You are going to rewrite them")
    print("Here you can produce graphs for:")
    print("  1. Community init")
    print("  2. Clan init")
    print("  3. Both")
    action = input("\nOption (1/2/3): ").strip()
    if action == '1':
        #################### FOR INIT COM
        # ── n = 1 ────────────────────────────────────────────────────────────────────
        plot_n1_community_richness(df_com, save_path="output/images/com/com_rich_n1.png")
        plot_clan_measures(df_com, communities=(1, 2, 3), save_path="output/images/com/clan_rich.png")
        # ── n > 1 · Plot 1: community measures, four configs ─────────────────────────
        plot_community_measures(df_com, communities=[2, 3], save_path="output/images/com/com_rich.png")
        # ── n > 1 · Plot 2: com vs clan, separate figures per Dual config ─────────────
        plot_com_vs_clan_dual(df_com, dual_config='Dual-Parallel', save_path= "output/images/com/DU_paral_com_clan2n.png")
        #plot_com_vs_clan_dual(df_com, dual_config='Dual-Cross-33')
        #plot_com_vs_clan_dual(df_com,dual_config='Dual-Cross-66')
        plot_com_vs_clan_dual(df_com, dual_config='Dual-Cross-100', save_path= "output/images/com/DU_100_com_clan_ns.png")
        # ── n > 1 · Plot 2 alt: both Dual in one figure (single n) ───────────────────
        plot_com_vs_clan_both_dual(df_com, n=2, save_path= "output/images/com/DU_all_com_clan2.png")
        plot_com_vs_clan_both_dual(df_com, n=3, save_path= "output/images/com/DU_all_com_clan3.png")
        plot_all_moments(df_com, n=1, save_path="output/images/com/mat_netn1.png")
        plot_all_moments(df_com, n=2, save_path="output/images/com/mat_netn2.png")
        plot_all_moments(df_com, n=3, save_path="output/images/com/mat_netn3.png")
    elif action == '2':
            ################ FOR INIT CLAN
        # ── n = 1 ────────────────────────────────────────────────────────────────────
        plot_n1_community_richness(df_clan, configs=['Dual-Parallel', 'Dual-Cross-100',], save_path="output\images\clan\com_rich_n1.png")
        plot_clan_measures(df_clan, communities=(1, 2, 3), save_path="output\images\clan\clan_rich.png")
        # ── n > 1 · Plot 1: community measures, four configs ─────────────────────────
        plot_community_measures(df_clan, communities=[2, 3], configs=['Dual-Parallel', 'Dual-Cross-100'], save_path="output\images\clan\com_rich.png")
        # ── n > 1 · Plot 2: com vs clan, separate figures per Dual config ─────────────
        plot_com_vs_clan_dual(df_clan,dual_config='Dual-Parallel', save_path= "output\images\clan\DU_paral_com_clan2n.png")
        # plot_com_vs_clan_dual(df_clan, dual_config='Dual-Cross-33')
        # plot_com_vs_clan_dual(df_clan,dual_config='Dual-Cross-66')
        plot_com_vs_clan_dual(df_clan,dual_config='Dual-Cross-100', save_path= "output\images\clan\DU_100_com_clan_ns.png")
        # ── n > 1 · Plot 2 alt: both Dual in one figure (single n) ───────────────────
        plot_com_vs_clan_both_dual(df_clan, n=2, save_path= "output\images\clan\DU_all_com_clan2.png")
        plot_com_vs_clan_both_dual(df_clan, n=3, save_path= "output\images\clan\DU_all_com_clan3.png")
        ### Net
        plot_all_moments(df_clan, n=1, com_init= False, save_path="output\images\clan\mat_netn1.png")
        plot_all_moments(df_clan, n=2, com_init= False,  save_path="output\images\clan\mat_netn2.png")
        plot_all_moments(df_clan, n=3, com_init= False,  save_path="output\images\clan\mat_netn3.png")
    elif action =='3':
        print("Firts com")
        #################### FOR INIT COM
        # ── n = 1 ────────────────────────────────────────────────────────────────────
        plot_n1_community_richness(df_com, save_path="output\images\com\com_rich_n1.png")
        plot_clan_measures(df_com, communities=(1, 2, 3), save_path="output\images\com\clan_rich.png")
        # ── n > 1 · Plot 1: community measures, four configs ─────────────────────────
        plot_community_measures(df_com, communities=[2, 3], save_path="output\images\com\com_rich.png")
        # ── n > 1 · Plot 2: com vs clan, separate figures per Dual config ─────────────
        plot_com_vs_clan_dual(df_com, dual_config='Dual-Parallel', save_path= "output\images\com\DU_paral_com_clan2n.png")
        #plot_com_vs_clan_dual(df_com, dual_config='Dual-Cross-33')
        #plot_com_vs_clan_dual(df_com,dual_config='Dual-Cross-66')
        plot_com_vs_clan_dual(df_com, dual_config='Dual-Cross-100', save_path= "output\images\com\DU_100_com_clan_ns.png")
        # ── n > 1 · Plot 2 alt: both Dual in one figure (single n) ───────────────────
        plot_com_vs_clan_both_dual(df_com, n=2, save_path= "output\images\com\DU_all_com_clan2.png")
        plot_com_vs_clan_both_dual(df_com, n=3, save_path= "output\images\com\DU_all_com_clan3.png")
        plot_all_moments(df_com, n=1, save_path="output\images\com\mat_netn1.png")
        plot_all_moments(df_com, n=2, save_path="output\images\com\mat_netn2.png")
        plot_all_moments(df_com, n=3, save_path="output\images\com\mat_netn3.png")
        print("Then clan")
        ###################### FOR INIT CLAN
        # ── n = 1 ────────────────────────────────────────────────────────────────────
        plot_n1_community_richness(df_clan, configs=['Dual-Parallel', 'Dual-Cross-100',], save_path="output\images\clan\com_rich_n1.png")
        plot_clan_measures(df_clan, communities=(1, 2, 3), save_path="output\images\clan\clan_rich.png")
        # ── n > 1 · Plot 1: community measures, four configs ─────────────────────────
        plot_community_measures(df_clan, communities=[2, 3], configs=['Dual-Parallel', 'Dual-Cross-100'], save_path="output\images\clan\com_rich.png")
        # ── n > 1 · Plot 2: com vs clan, separate figures per Dual config ─────────────
        plot_com_vs_clan_dual(df_clan,dual_config='Dual-Parallel', save_path= "output\images\clan\DU_paral_com_clan2n.png")
        # plot_com_vs_clan_dual(df_clan, dual_config='Dual-Cross-33')
        # plot_com_vs_clan_dual(df_clan,dual_config='Dual-Cross-66')
        plot_com_vs_clan_dual(df_clan,dual_config='Dual-Cross-100', save_path= "output\images\clan\DU_100_com_clan_ns.png")
        # ── n > 1 · Plot 2 alt: both Dual in one figure (single n) ───────────────────
        plot_com_vs_clan_both_dual(df_clan, n=2, save_path= "output\images\clan\DU_all_com_clan2.png")
        plot_com_vs_clan_both_dual(df_clan, n=3, save_path= "output\images\clan\DU_all_com_clan3.png")
        ### Net
        plot_all_moments(df_clan, n=1, com_init= False, save_path="output\images\clan\mat_netn1.png")
        plot_all_moments(df_clan, n=2, com_init= False,  save_path="output\images\clan\mat_netn2.png")
        plot_all_moments(df_clan, n=3, com_init= False,  save_path="output\images\clan\mat_netn3.png")
    else:
        print("well, thats nothing! bye!")

else:
    print("Invalid option.")