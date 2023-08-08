import pickle
import matplotlib.pyplot as plt

plt.style.use("seaborn")
plotFolder = "tf2Plots"
saveFigs = 1
showFigs = 0

with open('med_totals_dict.pkl', 'rb') as f_med_totals:
    med_totals = pickle.load(f_med_totals)
with open('dd_totals_dict.pkl', 'rb') as f_dd_totals:
    dd_totals = pickle.load(f_dd_totals)
with open('med_pm_dict.pkl', 'rb') as f_med_pm:
    med_pm = pickle.load(f_med_pm)
with open('dd_pm_dict.pkl', 'rb') as f_dd_pm:
    dd_pm = pickle.load(f_dd_pm)


def generate_stat_list(stat, dataset, class_name=""):
    result = []
    if class_name == "":
        for ID in dataset:
            name = dataset[ID]['name']
            name_wo_class_suffix = name.split('.')[0] + "." + name.split('.')[1]
            if dataset[ID][stat] != 0:
                result.append((name_wo_class_suffix, dataset[ID][stat]))

    else:
        for ID in dataset:
            if dataset[ID]['name'].endswith(class_name):
                name = dataset[ID]['name']
                name_wo_class_suffix = name.split('.')[0] + "." + name.split('.')[1]
                if dataset[ID][stat] != 0:
                    result.append((name_wo_class_suffix, dataset[ID][stat]))

    result_list_sorted = sorted(result, key=lambda x: x[1])
    result_list_grouped = list(
        zip(*result_list_sorted))  # groups names into one tuple and stat into another for easier plotting
    return result_list_grouped


def stat_dist_agg(dataset, stat, team_name=""):
    result_list = [0, 0, 0]  # scout, soldier, demo

    if team_name == "":
        for ID in dataset:
            if dataset[ID]['name'].endswith("SCOUT"):
                result_list[0] += dataset[ID][stat]
            elif dataset[ID]['name'].endswith("SOLDIER"):
                result_list[1] += dataset[ID][stat]
            elif dataset[ID]['name'].endswith("DEMO"):
                result_list[2] += dataset[ID][stat]

    else:
        for ID in dataset:
            if dataset[ID]['name'].startswith(team_name) and dataset[ID]['name'].endswith('SCOUT'):
                result_list[0] += dataset[ID][stat]
            elif dataset[ID]['name'].startswith(team_name) and dataset[ID]['name'].endswith('SOLDIER'):
                result_list[1] += dataset[ID][stat]
            elif dataset[ID]['name'].startswith(team_name) and dataset[ID]['name'].endswith('DEMO'):
                result_list[2] += dataset[ID][stat]

    return result_list


medic_stat_names = ['deaths_pm', 'assists_pm', 'dt_pm', 'medkits_hp_pm', 'cpc_pm', 'ubers_pm', 'drops_pm', 'heal_pm']
medic_titles = ['Deaths per minute', 'Assists per minute', 'Damage taken per minute', 'HP from medkits per minute',
                'Points captured per minute', 'Ubers per minute', 'Drops per minute', 'Heals per minute']

for i, stat in enumerate(medic_stat_names):
    plt.figure(figsize=(16, 9))
    name_med, val_med = generate_stat_list(stat, med_pm)[0], generate_stat_list(stat, med_pm)[1]
    plt.barh(name_med, val_med)
    plt.title(medic_titles[i])
    max_x_lim = max(val_med) * 1.15
    plt.xlim(0, max_x_lim)
    plotName = f"medic_{stat}"
    for index, value in enumerate(val_med):
        if value > 10 ** 3:
            plt.text(value, index, f'{float(f"{value:.5g}"):g}')
        elif 10 < value < 10 ** 3:
            plt.text(value, index, f'{float(f"{value:.4g}"):g}')
        else:
            plt.text(value, index, f'{float(f"{value:.3g}"):g}')
    if saveFigs == 1:
        plt.savefig(f"{plotFolder}/{plotName}.svg", format="svg")


list_of_stat_names = ['kills_pm', 'deaths_pm', 'assists_pm', 'dmg_pm', 'dt_pm', 'hr_pm', 'as_pm', 'medkits_hp_pm',
                      'cpc_pm', 'backstabs_pm', 'headshots_hit_pm', 'headshots_pm']

list_of_titles = ['Kills per minute', 'Deaths per minute', 'Assists per minute', 'Damage per minute',
                  'Damage taken per minute', 'Heals received per minute', 'Airshots per minute',
                  'HP from medkits per minute', 'Points captured per minute', 'Backstabs per minute',
                  'Headshots hit per minute', 'Headshot kills per minute']

for i, stat in enumerate(list_of_stat_names):
    plt.figure(figsize=(16, 9))
    name_dmg, val_dmg = generate_stat_list(stat, dd_pm)[0], generate_stat_list(stat, dd_pm)[1]
    plt.barh(name_dmg, val_dmg)
    plt.title(list_of_titles[i])
    max_x_lim = max(val_dmg) * 1.15
    plt.xlim(0, max_x_lim)
    plotName = f"dmg_{stat}"
    for index, value in enumerate(val_dmg):
        if value > 10 ** 3:
            plt.text(value, index, f'{float(f"{value:.5g}"):g}')
        elif 10 < value < 10 ** 3:
            plt.text(value, index, f'{float(f"{value:.4g}"):g}')
        else:
            plt.text(value, index, f'{float(f"{value:.3g}"):g}')
    if saveFigs == 1:
        plt.savefig(f"{plotFolder}/{plotName}.svg", format="svg")


combat_eff = []
for ID in dd_totals:
    stat_calc = (dd_totals[ID]['dmg'] - dd_totals[ID]['dt']) / dd_totals[ID]['hr']
    name = dd_totals[ID]['name']
    name_wo_class_suffix = name.split('.')[0] + "." + name.split('.')[1]
    combat_eff.append((name_wo_class_suffix, stat_calc))
combat_eff_ascending = sorted(combat_eff, key=lambda x: x[1])
combat_eff_grouped = list(zip(*combat_eff_ascending))
plt.figure(figsize=(16, 9))
for index, value in enumerate(combat_eff_grouped[1]):
    if value < 0:
        plt.text(0.001, index, f'{float(f"{value:.2g}"):g}')
    else:
        plt.text(value, index, f'{float(f"{value:.2g}"):g}')
plt.barh(combat_eff_grouped[0], combat_eff_grouped[1])
plt.title("Combat efficiency")
if saveFigs == 1:
    plt.savefig(f"{plotFolder}/combat_eff.svg", format="svg")


net_dpm = []
for ID in dd_pm:
    stat_calc = (dd_pm[ID]['dmg_pm'] - dd_pm[ID]['dt_pm'])
    name = dd_pm[ID]['name']
    name_wo_class_suffix = name.split('.')[0] + "." + name.split('.')[1]
    net_dpm.append((name_wo_class_suffix, stat_calc))
net_dpm_ascending = sorted(net_dpm, key=lambda x: x[1])
net_dpm_grouped = list(zip(*net_dpm_ascending))
plt.figure(figsize=(16, 9))
for index, value in enumerate(net_dpm_grouped[1]):
    if value < 0:
        plt.text(0.001, index, f'{float(f"{value:.3g}"):g}')
    else:
        plt.text(value, index, f'{float(f"{value:.3g}"):g}')
plt.barh(net_dpm_grouped[0], net_dpm_grouped[1])
plt.title("Net damage per minute")
if saveFigs == 1:
    plt.savefig(f"{plotFolder}/net_dpm.svg", format="svg")


labels_dmg_classes = ['Scouts', 'Soldiers', 'Demo']
kill_dist_all = stat_dist_agg(dd_totals, 'kills')
kill_dist_wG = stat_dist_agg(dd_totals, 'kills', 'wG')
kill_dist_tf2e = stat_dist_agg(dd_totals, 'kills', 'tf2e')
kill_dist_np = stat_dist_agg(dd_totals, 'kills', 'np')
kill_dist_csg = stat_dist_agg(dd_totals, 'kills', 'csg')

fig, ax = plt.subplots(1, 5)
ax[0].pie(kill_dist_all, labels=labels_dmg_classes, autopct='%1.1f%%')
ax[0].set_title('Total')
ax[1].pie(kill_dist_wG, labels=labels_dmg_classes, autopct='%1.1f%%')
ax[1].set_title('wG')
ax[2].pie(kill_dist_tf2e, labels=labels_dmg_classes, autopct='%1.1f%%')
ax[2].set_title('tf2easy')
ax[3].pie(kill_dist_np, labels=labels_dmg_classes, autopct='%1.1f%%')
ax[3].set_title('NOOBPANZER')
ax[4].pie(kill_dist_csg, labels=labels_dmg_classes, autopct='%1.1f%%')
ax[4].set_title('csg')
fig.set_figwidth(20)
fig.set_figwidth(15)
fig.suptitle('Kill distribution')
if saveFigs == 1:
    fig.savefig(f"{plotFolder}/Kill_distribution.svg", format="svg")


dmg_dist_all = stat_dist_agg(dd_totals, 'dmg')
dmg_dist_wG = stat_dist_agg(dd_totals, 'dmg', 'wG')
dmg_dist_tf2e = stat_dist_agg(dd_totals, 'dmg', 'tf2e')
dmg_dist_np = stat_dist_agg(dd_totals, 'dmg', 'np')
dmg_dist_csg = stat_dist_agg(dd_totals, 'dmg', 'csg')

fig2, ax2 = plt.subplots(1, 5)
ax2[0].pie(dmg_dist_all, labels=labels_dmg_classes, autopct='%1.1f%%')
ax2[0].set_title('Total')
ax2[1].pie(dmg_dist_wG, labels=labels_dmg_classes, autopct='%1.1f%%')
ax2[1].set_title('wG')
ax2[2].pie(dmg_dist_tf2e, labels=labels_dmg_classes, autopct='%1.1f%%')
ax2[2].set_title('tf2easy')
ax2[3].pie(dmg_dist_np, labels=labels_dmg_classes, autopct='%1.1f%%')
ax2[3].set_title('NOOBPANZER')
ax2[4].pie(dmg_dist_csg, labels=labels_dmg_classes, autopct='%1.1f%%')
ax2[4].set_title('csg')
fig2.set_figwidth(20)
fig2.set_figwidth(15)
fig2.suptitle('Damage done distribution')
if saveFigs == 1:
    fig2.savefig(f"{plotFolder}/dmg_done_distribution.svg", format="svg")


dt_dist_all = stat_dist_agg(dd_totals, 'dt')
dt_dist_wG = stat_dist_agg(dd_totals, 'dt', 'wG')
dt_dist_tf2e = stat_dist_agg(dd_totals, 'dt', 'tf2e')
dt_dist_np = stat_dist_agg(dd_totals, 'dt', 'np')
dt_dist_csg = stat_dist_agg(dd_totals, 'dt', 'csg')

fig3, ax3 = plt.subplots(1, 5)
ax3[0].pie(dt_dist_all, labels=labels_dmg_classes, autopct='%1.1f%%')
ax3[0].set_title('Total')
ax3[1].pie(dt_dist_wG, labels=labels_dmg_classes, autopct='%1.1f%%')
ax3[1].set_title('wG')
ax3[2].pie(dt_dist_tf2e, labels=labels_dmg_classes, autopct='%1.1f%%')
ax3[2].set_title('tf2easy')
ax3[3].pie(dt_dist_np, labels=labels_dmg_classes, autopct='%1.1f%%')
ax3[3].set_title('NOOBPANZER')
ax3[4].pie(dt_dist_csg, labels=labels_dmg_classes, autopct='%1.1f%%')
ax3[4].set_title('csg')
fig3.set_figwidth(20)
fig3.set_figwidth(15)
fig3.suptitle('Damage taken distribution')
if saveFigs == 1:
    fig3.savefig(f"{plotFolder}/dmg_taken_distribution.svg", format="svg")


death_dist_all = stat_dist_agg(dd_totals, 'deaths')
plt.figure()
plt.pie(death_dist_all, labels=labels_dmg_classes, autopct='%1.1f%%')
plt.title('Death distribution')
if saveFigs == 1:
    plt.savefig(f"{plotFolder}/total_deaths_distribution.svg", format="svg")


medkithp_dist_all = stat_dist_agg(dd_totals, 'medkits_hp')
plt.figure()
plt.pie(medkithp_dist_all, labels=labels_dmg_classes, autopct='%1.1f%%')
plt.title('HP received from medkits distribution')
if saveFigs == 1:
    plt.savefig(f"{plotFolder}/HP_from_medkits_distribution.svg", format="svg")

if showFigs == 1:
    plt.show()