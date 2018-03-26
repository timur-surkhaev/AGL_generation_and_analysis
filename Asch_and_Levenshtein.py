#!/usr/bin/python
# -*- coding: utf-8 -*-
# Считает расстояние Левенштейна и АСЧ для набора строк
# На выходе csv-файл с колонками:
# "Группа - Тип генерации - Строка - Левенштейн - АСЧ"

#--------- for python console --------
# execfile('Asch_and_Levenshtein.py')       

import Levenshtein as lv
#========================input_data==========================================
# обрабатываемые файлы должны быть перечислены строго в порядке, приведённом 
# ниже; последние 7 символов должны быть строго "INCLUDE" или "EXCLUDE", 
# в противном случае программа не сможет определить тип генерации

generated_strings_list = ["Group_1_INCLUDE",
                        "Group_1_EXCLUDE",
                        "Group_2_INCLUDE",
                        "Group_2_EXCLUDE",
                        "Group_3_INCLUDE",
                        "Group_3_EXCLUDE"]

gramm_strings = "gramm" # грамматический массив для расст. Левенштейна
train_strings = "train" # набор тренировочных строк для подсчёта АСЧ

#------------ for testing -----------
#processed_string_set = ["XMMMX","XVXMSM"]
#train_string_set = ["XMMMX", "XVXMXVX", "XMXVXM"]

#========================Levenshtein=========================================

def get_levnsht_array(pr_str_set, gr_str_set):
    levsh_array = []
    for pr_str in pr_str_set:
        lev_dist = 1000     # definetely max value
        for gr_str in gr_str_set:
            # trying to improve result - to find nearest string in gramm_set
            lev_dist = min(lev_dist, lv.distance(pr_str, gr_str)) 
        levsh_array.append([pr_str, lev_dist])
    
    return levsh_array    

#=========================ASCh===============================================

# рабочая лошадка, возвращает позиционную АСЧ отдельной строки
def count_asch (pr_str, tr_str_set):        
    reps = 0.0           
    for i in range(len(pr_str) - 1):        # (встречаемость биграмм)
        for tr_str in tr_str_set:
            if pr_str[i:i+2] == tr_str[i:i+2]: # выход за границу tr_str не
                                               # страшен, так как чанки просто 
                                               # обрезаются (вплоть до '')
                reps = reps + 1

    for i in range(len(pr_str) - 2):        # (+ встречаемость триграммам)
        for tr_str in tr_str_set:
            if pr_str[i:i+3] == tr_str[i:i+3]:
                reps = reps + 1
                
    return reps/(2*len(pr_str) - 3)         # нормируем на число чанков


# возвращает усреднённую позиционную АСЧ набора строк
def get_asch_array(pr_string_set, tr_string_set):
    asch_sum = 0.0
    asch_array = []
    for pr_string in pr_string_set:
        asch_array.append([pr_string, count_asch(pr_string, tr_string_set)])
        #asch_sum = asch_sum + count_asch(pr_string, tr_string_set)
    return asch_array

#========================programm============================================

header = 'Group, Type, String, Lev, Asch\n'
all_groups_final_list = open('./Output/all_groups_final_list.csv', 'w')
all_groups_final_list.write(header)

results = []
for generated_strings in generated_strings_list:

    processed_string_set = []
    ff = open('./Input/' + generated_strings).read().split('\n')
    for string  in ff:
        if string != '':
            processed_string_set.append(string)

    gramm_string_set = []
    ff = open('./Input/' + gramm_strings).read().split('\n')
    for string  in ff:
        if string != '':
            gramm_string_set.append(string)
            
    train_string_set = []
    ff = open('./Input/' + train_strings).read().split('\n')
    for string  in ff:
        if string != '':
            train_string_set.append(string) 
            
    levnsht_list = get_levnsht_array(processed_string_set, gramm_string_set)
    asch_list = get_asch_array(processed_string_set, train_string_set)
    
    sum_list = [levnsht_list[i][1] for i in range(len(levnsht_list))]
    results.append(sum(sum_list)/float(len(levnsht_list)))
    

    final_list = []
    for i in range(len(levnsht_list)):
        final_list.append([levnsht_list[i][0],
                           levnsht_list[i][1],
                           asch_list[i][1]])
        
    #======================= Output for str_set ===========================        
    
    output_filename = './Output/' + generated_strings + '_asch_lev.csv'
    output_file = open(output_filename, 'w')    
    
    output_file.write(header)
    
    for row in final_list:
        
        output_file.write(generated_strings[-9] + ',' +
                          generated_strings[-7:-4] + ',' +
                          row[0] + ',' + 
                          str(row[1]) + ',' +
                          str (round(row[2], 2)) + '\n')
        
        all_groups_final_list.write(generated_strings[-9] + ',' +
                                    generated_strings[-7:-4] + ',' +
                                    row[0] + ',' + 
                                    str(row[1]) + ',' +
                                    str (round(row[2], 2)) + '\n')
    output_file.close()
    
    print generated_strings    
    for row in final_list:
        print row[0] + '\t' + str(row[1]) + '  ' + str(round(row[2], 2))

all_groups_final_list.close()

print '\n===== Levenshtein ====='
print '\nINCLUDE:'
print 'Group_1\t' + str(results[0])
print 'Group_2\t' + str(results[2])
print 'Group_3\t' + str(results[4])

print '\nEXCLUDE:'
print 'Group_1\t' + str(results[1])
print 'Group_2\t' + str(results[3])
print 'Group_3\t' + str(results[5])

    
print '\nDifference (EXCLUDE - INCLUDE):'
print 'Group_1\t' + str(results[1] - results[0])
print 'Group_2\t' + str(results[3] - results[2])
print 'Group_3\t' + str(results[5] - results[4])
    
    
"""
INCLUDE:
Group_1	1.83333333333
Group_2	1.81481481481
Group_3	1.87719298246

EXCLUDE:
Group_1	2.23684210526
Group_2	2.33333333333
Group_3	2.24561403509

Difference (EXCLUDE - INCLUDE):
Group_1	0.40350877193
Group_2	0.518518518519
Group_3	0.368421052632
"""
