import os

#Finds all the dictionary objects in the config file and pumps them out
#in a list of strings ready to be split, read, and evlauated
def _find_dicts(remain):
    dict_list = []
    while remain != []:
        end = _home_slice(remain)
        dict_list.append(''.join(_parse_dict(remain[:end])))
        remain = remain[end:]
    return dict_list

#Finds the line designating a dictionary end and passes that info back
#to the loop that slice it up
def _home_slice(lines):
    for index,line in enumerate(lines):
        if '}' in line:
            return index+1
        
#Cleans up all the messy lines that are necessary to keep the actual file readable
def _parse_dict(dicter):
    for index,line in enumerate(dicter):
        dicter[index] = line.strip().replace('\t','')
    return dicter

#Reads the config file (vaguely formed into python dictionaries already)
#and passes the lines it reads to functions that will pump out the dictionaries
def _create_dict_list(file_path): 
    with open(file_path, 'r') as config_file:
        all_lines = config_file.readlines()
        return(_find_dicts(all_lines))

#Main function to check the environment and create the appropiate dictionary of
#urls. Takes the file path to the text config file.
def get_urls(file_path, environ_name):       
    dict_list=_create_dict_list(file_path)
    name_spaces = {}

    for index, name in enumerate(dict_list):
        if name.split('=')[0].strip() == environ_name:
            name_spaces = eval(name.split('=')[1])
            return name_spaces


        

    


    
        
