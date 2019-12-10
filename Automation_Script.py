"""
Created on Mon Sept 16 06:40:40 2019

Author: Juan Leonardo Moctezuma-Flores
"""
# Modules need to be imported in order for some functions to be able to operate. Code lines: 7 - 10.
import glob
import itertools
import os
import re

# Some variables will be initially declared. Code lines: 13 - 18.
bde = re.compile("BDE.*")
current_quarter_placeholder = 'BDE: N/A THIS QUARTER'
pipe = "|"
previous_quarter_placeholder = 'BDE: N/A LAST QUARTER'
table_dash = "--------------------------------------------------------------------------------------"
white_space = "       "

# The first step of this code will be to prompt the user. Code lines: 23 - 37.
# The analyst must select a client and the current quarter.
# The while-loops are included in case the user's input has a typo.
while True:
    client_id = str(input("Enter the name of the folder of your iPad client (for instance, Client_X): "))
    if (client_id == 'Client_X') or (client_id == 'Client_Z'):
        break
    else:
        print("You entered an invalid folder name, please try again:")
        continue

while True:
    c = str(input("Enter the name of the folder corresponding to the current quarter (for instance, 2019 Q1): "))
    if (c == '2019 Q1'):
        break
    else:
        print("You entered an invalid folder name or a non-existent quarter, please try again.")
        continue

# Basic math will be computed in order to calculate the previous quarter. Code Lines: 41 - 62.
# In this program the user will not be prompted to select the previous quarter.
year, qtr = c.split(" ")
year = int(year)
qtr = str(qtr)

pq_year = year - 1
quarter = int(re.search(r'\d+', qtr).group(0))

pq_year = str(pq_year)
year = str(year)

if quarter == 1:
    p = str(pq_year + ' Q4')
elif quarter == 2:
    p = str(year + ' Q1')
elif quarter == 3:
    p = str(year + ' Q2')
elif quarter == 4:
    p = str(year + ' Q3')
else:
    pass

print("Please note that the previous quarter based on your selection is: " + p)

# This next line will separate the prompting phase with the actual results!. Code line: 65.
print("___________________________________________________________________________________________________")

# Letters "pq" stands for previous quarter, "cq" refers to current quarter and "bde" means Broker Dealer Exclusion.
# In addition, "ws" stands for wholesaler, "mgr" stands for manager, "dmgr" stands for divisional manager.
# Some variables used throughout the rest of the script will include these abbreviations.

# What the following variables are doing is to read the text files from absolute folders' path. Code lines: 74 - 87.
# All clients from the consortium have both wholesalers' and the managers' data.
# However not all of them have a broker dealer exclusions requested by a divisional manager.
path_ws_pq = os.path.abspath('Automation_Testing_Folder/' + client_id + '/' + p + '/Wholesaler-Request/' + client_id +
                             '-WS-Requested Exclusions List-' + p)
path_ws_cq = os.path.abspath('Automation_Testing_Folder/' + client_id + '/' + c + '/Wholesaler-Request/' + client_id +
                             '-WS-Requested Exclusions List-' + c)

path_mgr_pq = os.path.abspath('Automation_Testing_Folder/' + client_id + '/' + p + '/Manager-Request/' + client_id +
                              '-MGR-Requested Exclusions List-' + p)
path_mgr_cq = os.path.abspath('Automation_Testing_Folder/' + client_id + '/' + c + '/Manager-Request/' + client_id +
                              '-MGR-Requested Exclusions List-' + c)

path_dmgr_pq = os.path.abspath('Automation_Testing_Folder/' + client_id + '/' + p + '/Divisional_Manager-Request/' +
                               client_id + '-DIV-MGR-Requested Exclusions List-' + p)
path_dmgr_cq = os.path.abspath('Automation_Testing_Folder/' + client_id + '/' + c + '/Divisional_Manager-Request/' +
                               client_id + '-DIV-MGR-Requested Exclusions List-' + c)

# Sometimes a folder was named incorrectly or placed in the wrong path.
# The try and except blocks will warn the user if that is the case, which means the results will not get displayed.
# Without these code blocks, the program will crash. Code Lines: 92 - 126.
try:
    read_path_ws_pq = open(path_ws_pq, 'r')
except FileNotFoundError:
    print("Your file or folders linked to the wholesalers' previous quarter txt files are named or set up incorrectly.")

try:
    read_path_ws_cq = open(path_ws_cq, 'r')
except FileNotFoundError:
    print("Your file or folders linked to the wholesalers' current quarter txt files are named or set up incorrectly.")

try:
    read_path_mgr_pq = open(path_mgr_pq, 'r')
except FileNotFoundError:
    print("Your file or folders linked to the managers' previous quarter txt files are named or set up incorrectly.")

try:
    read_path_mgr_cq = open(path_mgr_cq, 'r')
except FileNotFoundError:
    print("Your file or folders linked to the managers' current quarter txt files are named or set up incorrectly.")

try:
    read_path_dmgr_pq = open(path_dmgr_pq, 'r')
except FileNotFoundError:
    if client_id != 'Client_Z':
        print(" ")
    else:
        print("Your file and folders linked to the divisional managers' previous quarter txt files are named or set up incorrectly")

try:
    read_path_dmgr_cq = open(path_dmgr_cq, 'r')
except FileNotFoundError:
    if client_id != 'Client_Z':
        print(" ")
    else:
        print("Your file and folders linked to the divisional managers' current quarter txt files are named or set up incorrectly")

# At this point we define a function in order to avoid writing repeated code blocks. Code Lines: 132 - 278.
# This object will read the files for each folder (wholesaler, manager, & divisional manager (if available)).
# The only arguments we need are the variables containing data from the previous and current quarter.

def ReportByCategory(previous_quarter,current_quarter):
    # We define the following function to remove repeated Broker Dealer Exclusions (BDE) ID's. Code Lines: 134 - 139.
    def RemoveDuplicates(ListOfElements):
        UniqueList = []
        for element in ListOfElements:
            if element not in UniqueList:
                UniqueList.append(element)
        return UniqueList

    ############################################################################################################
    # Two columns with data from 'pq' and 'cq' will have its data processed and displayed. Code Lines: 146 - 278.
    ############################################################################################################
    # Empty lists will store data corresponding from txt files. Code Lines: 146 - 156.
    # Each txt file is located in the folder with wholesaler, manager, and divisional manager data.
    pq_txt_result = []
    with previous_quarter as previous_file:
        for txt_line_pq in previous_file:
            txt_line_pq = txt_line_pq.split()
            pq_txt_result.append(txt_line_pq)

    cq_txt_result = []
    with current_quarter as current_file:
        for txt_line_cq in current_file:
            txt_line_cq = txt_line_cq.split()
            cq_txt_result.append(txt_line_cq)

    # RemoveDuplicates will remove duplicated rows (BDEs) within the text files. Code Lines: 159 - 160.
    pq_txt_result = RemoveDuplicates(pq_txt_result)
    cq_txt_result = RemoveDuplicates(cq_txt_result)

    # Elements will get removed from sub-lists and separate by semi-colon. Code Lines: 163 - 164.
    pq_txt_result_split = ";".join(map(" ".join, pq_txt_result))
    cq_txt_result_split = ";".join(map(" ".join, cq_txt_result))

    # Split will remove semi-colons and move all elements into 1 list, free of sub-listed items. Code Lines: 167 - 168.
    pq_txt_result_list = pq_txt_result_split.split(';')
    cq_txt_result_list = cq_txt_result_split.split(';')

    # Tuples are now created within a list when each element gets tagged to a No. with enumerate. Code Lines 171 - 172.
    pq_txt_result_enumerate = list(enumerate(pq_txt_result_list))
    cq_txt_result_enumerate = list(enumerate(cq_txt_result_list))

    # Each list might have a different length since the client might requested a different amount of exclusions.
    # If the client requested more exclusions during 'cq', we would need to know the length. Code Lines: 176 - 177.
    pq_txt_result_length = [x[0] for x in pq_txt_result_enumerate]
    cq_txt_result_length = [x[0] for x in cq_txt_result_enumerate]

    # Each row on the text file will get arranged or sorted in the same order as in the file.
    # Please note that looping using x[0] was used to measure length of lists.
    # All elements in place x[1] contains exclusions that will get sorted. Code Lines: 182 - 183.
    pq_txt_result_arrange = [x[1] for x in pq_txt_result_enumerate]
    cq_txt_result_arrange = [x[1] for x in cq_txt_result_enumerate]

    #####################################################################################################
    # Code lines 189 - 202 will compile the rest of the data from each txt file that will get displayed.
    #####################################################################################################
    # The four quarters at the very top of each txt file will get displayed. Code Lines: 189 - 190.
    client_date_pq = pq_txt_result_arrange[1:6]
    client_date_cq = cq_txt_result_arrange[1:6]

    # BDE IDs will get extracted only. Code Lines: 193 - 194.
    bde_list_pq = list(filter(bde.match, pq_txt_result_arrange))
    bde_list_cq = list(filter(bde.match, cq_txt_result_arrange))

    # BDE IDs get sorted in ascending order. Code Lines: 197 - 198.
    bde_list_pq_sort = sorted(bde_list_pq, key=lambda elem: int(elem.split('BDE')[1]))
    bde_list_cq_sort = sorted(bde_list_cq, key=lambda elem: int(elem.split('BDE')[1]))

    # Category and email will get displayed at the very end. Code Lines: 201 - 202.
    category_email_pq = pq_txt_result_arrange[-2:]
    category_email_cq = cq_txt_result_arrange[-2:]

    ################################################################################################################
    # This section with code lines 209 to 250 will arrange the BDE IDs depending on their status.
    # The 3 types of status are N/A (only in 'pq'), Available (in both 'pq' and 'cq') and Available (only in 'cq').
    ################################################################################################################

    pq_item_not_in_cq = [item for item in bde_list_pq_sort if item not in bde_list_cq_sort]
    cq_item_not_in_pq = [item for item in bde_list_cq_sort if item not in bde_list_pq_sort]

    pq_item_in_cq = [item for item in bde_list_pq_sort if item in bde_list_cq_sort]
    cq_item_in_pq = [item for item in bde_list_cq_sort if item in bde_list_pq_sort]

    item_in_common = pq_item_in_cq + cq_item_in_pq
    item_in_common = RemoveDuplicates(item_in_common)

    # This process will require to measure the length of the new lists again.
    # The goal is to put a placeholder on either list (the list with 'cq' or 'pq' BDE IDs).
    # Placeholders' location will vary depending on their status.
    bde_pq_len = len(pq_item_not_in_cq)
    bde_cq_len = len(cq_item_not_in_pq)

    # The current quarter placeholder refers to the fact that a BDE ID is not currently in use.
    # Empty lists will need to be created again. Code Lines: 226 - 241.
    bde_cq_ph = []
    i = 0
    while i < bde_pq_len:
        bde_cq_ph.append(current_quarter_placeholder)
        i += 1
        if i == bde_pq_len:
            break

    # The previous quarter placeholder refers to the fact that a BDE ID was not used last quarter.
    bde_pq_ph = []
    i = 0
    while i < bde_cq_len:
        bde_pq_ph.append(previous_quarter_placeholder)
        i += 1
        if i == bde_cq_len:
            break

    # Two lists with 'pq' and 'cq' data get aligned to show how these would look like in Excel. Code Lines: 245 - 250.
    # In addition, a 3rd list with Boolean data will simulate the True/False formula on Excel.
    bde_pq_final = item_in_common + pq_item_not_in_cq + bde_pq_ph
    bde_cq_final = item_in_common + bde_cq_ph + cq_item_not_in_pq

    # Once again, data will get compiled in a similar order as the txt files were originally.
    result_pq_compiled = client_date_pq + bde_pq_final + category_email_pq
    result_cq_compiled = client_date_cq + bde_cq_final + category_email_cq

    # The 3rd column will get inserted at this point, BDE IDs from 'pq' and 'cq' will get compared.
    # Ideally BDE IDs from 'pq' and 'cq' should be the same (True instead of False).
    # Only the quarters from the 'pq' and 'cq' text files are expected to get a False. Code Lines: 255 - 266.
    try:
        bde_true_false = []
        for x in range(len(result_pq_compiled)) and range(len(result_cq_compiled)):
            if result_pq_compiled[x] == result_cq_compiled[x]:
                bde_true_false.insert(x, 'TRUE')
            else:
                bde_true_false.insert(x, '\033[01;31mFALSE\033[m')
                x += 1
    # Sometimes programs crash when looping through lists or array that don't have the same dimensions.
    # This try-except block was initially inserted for testing purposes. Code Line: 263.
    except IndexError:
        print("Warning: lists do not have matching dimensions and the reports can't be generated.")

    ################################################################################################################
    # The final section of the function arranges how the 3 compiled lists will get displayed. Code Lines: 271 - 278.
    ################################################################################################################
    print('\n')
    print(pipe + '\033[1m{}\033[0m'.format(p) + '\033[1m{}\033[0m'.format(" Rolling Quarters Data") + white_space + pipe
    + '\033[1m{}\033[0m'.format(c) + '\033[1m{}\033[0m'.format(" Rolling Quarters Data") + white_space + pipe +
    '\033[1m{}\033[0m'.format("True/False"))
    print(table_dash)
    # The three lists will get iterated in parallel with zip. Code Lines: 274 -275.
    for bde_pq, bde_cq, bde_t_f in zip(result_pq_compiled, result_cq_compiled, bde_true_false):
        print(pipe + "{0:<35}".format(bde_pq), pipe + "{0:<35}".format(bde_cq),pipe + "{0:<35}".format(bde_t_f))

# The ReportByCategory function is finally over! variables x1, x2, and x3 will require arguments in order to function.
# The arguments are the variables containing the absolute path for the txt files.
# We use the try-except in case there is an error with the folder paths; this prevents the code from crushing.
# Please see lines: 285 - 299.

try:
    x1 = ReportByCategory(read_path_ws_pq,read_path_ws_cq)
except NameError:
    print(" ")

try:
    x2 = ReportByCategory(read_path_mgr_pq,read_path_mgr_cq)
except NameError:
    print(" ")

try:
    x3 = ReportByCategory(read_path_dmgr_pq,read_path_dmgr_cq)
except NameError:
    print('\n')
    print(client_id + " does not have a Divisional Manager category.")