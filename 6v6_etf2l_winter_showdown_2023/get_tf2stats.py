import requests
import csv
import time

with open('steamIDs2.csv', 'r') as file:
    csvFile = csv.reader(file)
    ID_names_dict = {}

    for lines in csvFile:
        ID, name = lines
        ID_names_dict[ID] = name

stat_Totals_dds = {}
stat_Totals_meds = {}

for entry in ID_names_dict:
    if ID_names_dict[entry].endswith(".MEDIC"):
        stat_Totals_meds[entry] = {"name": ID_names_dict[entry], "kills": 0, "deaths": 0, "assists": 0, "dmg": 0,
                                   "dt": 0, "as": 0, "medkits_hp": 0, "cpc": 0, "ubers": 0, "drops": 0, "heal": 0,
                                   "length": 0}
    else:
        stat_Totals_dds[entry] = {"name": ID_names_dict[entry], "kills": 0, "deaths": 0, "assists": 0, "dmg": 0,
                                  "dt": 0, "hr": 0, "as": 0, "medkits_hp": 0, "cpc": 0, "backstabs": 0,
                                  "headshots_hit": 0, "headshots": 0, "length": 0}

logIDs = [3401981, 3401959, 3401911, 3401171, 3401192, 3395991, 3395947, 3394178, 3394145, 3389004, 3389042, 3382900,
          3382860, 3378318, 3378363, 3375533, 3375496, 3368697, 3368662, 3401770, 3401760, 3401055, 3401060, 3395362,
          3395387, 3390862, 3390825, 3382938, 3382897, 3378327, 3378376, 3373409, 3373366, 3368691, 3368657, 3387154,
          3387186, 3385442, 3385474, 3382240, 3382261, 3378385, 3368675, 3368713, 3390831, 3390865, 3389015, 3389041,
          3384858, 3377687, 3377641]

numberOfLogsProcessed = 0
for logID in logIDs:
    numberOfLogsProcessed += 1
    if numberOfLogsProcessed % 20 == 0:
        print("Waiting for 20 seconds.")
        time.sleep(20)
        print("Wait is over.")
    response_log = requests.get("http://logs.tf/api/v1/log/" + str(logID))
    log_json = response_log.json()
    for ID in stat_Totals_dds:
        if ID in log_json['players']:
            for key in stat_Totals_dds[ID]:
                if key == "name":
                    continue
                elif key == "length":
                    stat_Totals_dds[ID][key] += log_json[key]
                else:
                    stat_Totals_dds[ID][key] += log_json['players'][ID][key]
    for ID in stat_Totals_meds:
        if ID in log_json['players']:
            for key in stat_Totals_meds[ID]:
                if key == "name":
                    continue
                elif key == "length":
                    stat_Totals_meds[ID][key] += log_json[key]
                else:
                    stat_Totals_meds[ID][key] += log_json['players'][ID][key]


stat_pm_dds = {}
stat_pm_meds = {}

for entry in ID_names_dict:
    if ID_names_dict[entry].endswith(".MEDIC"):
        stat_pm_meds[entry] = {"name": ID_names_dict[entry], "kills_pm": 0, "deaths_pm": 0, "assists_pm": 0,
                               "dmg_pm": 0,
                               "dt_pm": 0, "as_pm": 0, "medkits_hp_pm": 0, "cpc_pm": 0, "ubers_pm": 0, "drops_pm": 0,
                               "heal_pm": 0,
                               "length_in_minutes": 0}
    else:
        stat_pm_dds[entry] = {"name": ID_names_dict[entry], "kills_pm": 0, "deaths_pm": 0, "assists_pm": 0, "dmg_pm": 0,
                              "dt_pm": 0, "hr_pm": 0, "as_pm": 0, "medkits_hp_pm": 0, "cpc_pm": 0, "backstabs_pm": 0,
                              "headshots_hit_pm": 0, "headshots_pm": 0, "length_in_minutes": 0}

for ID in stat_Totals_meds:
    for key in stat_Totals_meds[ID]:
        if key == "name":
            continue
        elif key == "length":
            key_pm = key + "_in_minutes"
            stat_pm_meds[ID][key_pm] = stat_Totals_meds[ID][key] / 60
        else:
            key_pm = key + "_pm"
            stat_pm_meds[ID][key_pm] = stat_Totals_meds[ID][key] / (stat_Totals_meds[ID]['length'] / 60)

for ID in stat_Totals_dds:
    for key in stat_Totals_dds[ID]:
        if key == "name":
            continue
        elif key == "length":
            key_pm = key + "_in_minutes"
            stat_pm_dds[ID][key_pm] = stat_Totals_dds[ID][key] / 60
        else:
            key_pm = key + "_pm"
            stat_pm_dds[ID][key_pm] = stat_Totals_dds[ID][key] / (stat_Totals_dds[ID]['length'] / 60)

# SAVING STAT DICTS
"""
import pickle
with open('med_totals_dict.pkl', 'wb') as f_med_totals:
    pickle.dump(stat_Totals_meds, f_med_totals)

with open('dd_totals_dict.pkl', 'wb') as f_dd_totals:
    pickle.dump(stat_Totals_dds, f_dd_totals)

with open('med_pm_dict.pkl', 'wb') as f_med_pm:
    pickle.dump(stat_pm_meds, f_med_pm)

with open('dd_pm_dict.pkl', 'wb') as f_dd_pm:
    pickle.dump(stat_pm_dds, f_dd_pm)
"""
