'''============================================
Title:  IMAGE Extraction
Author: @pragyan.das
Date:   Friday October 25 2019
Description : This code reads the input path to a folder where the images are placed, file names and the config file location and returns a json file of extracted information
Main Function Block : extract_fields_and_values
Input : IMAGE files (format : .jpg,.png,.tiff)
Output : JSON file (format: .json)
==============================================='''

import pandas as pd,pickle
import cv2,pytesseract,time,os,json,ast
from pytesseract import Output
from field_search import find_field_locations
from value_search import find_values
from symspell import spell_corrector
import numpy as np
import sys,uuid

def create(dirPath_withNameofFolder):

    """
    Description : creates a folder at provided path
    Input_Parameter  : dirName(.png,.jpg,.tiff)
    Returns : dataframe
    """

    if not os.path.exists(dirPath_withNameofFolder):
        os.mkdir(dirPath_withNameofFolder)
        #print("Directory " ,dirPath_withNameofFolder ,  " Created ")
    else :
        #print("Directory " , dirPath_withNameofFolder ,  " already exists")
        pass


def run_hocr(image):
    """
    Description : runs ocr over an image and returns the output as a dataframe
    Input_Parameter  : IMAGE files(.png,.jpg,.tiff)
    Returns : dataframe
    Notes : The dataframe may change if you change the config here. The psm6 mode is set to read the document as a single text block line by line
    """
    df = pytesseract.image_to_data(image ,  config='--psm 6 --oem 1', output_type= Output.DATAFRAME)

    return df

def read_picklefile(pickle_filepath):
    """
    Description : reads the pickle file path and returns the word dictionary
    Input_Parameter  : pickle file path
    Returns : dictionary
    """

    dbfile = open(pickle_filepath, 'rb')
    vocab = pickle.load(dbfile)
    dbfile.close()
    words_dict = {k: 0 for k in vocab}
    return words_dict


def extract_post_json(posted_file):
    """
    Description : this takes the .json file as input , reads and organises it into array
    Input_Parameter  : JSON file(.json)
    Returns : arrays
    """
    Sub_Field = []

    with open(posted_file, 'r') as j:
         post = json.load(j)

    pickle_file = post["pickle_filepath"]
    Single = post['Single']

    for key in enumerate(post["KeyValue"]) :
        idx = key[0]
        x = post["KeyValue"][idx]["KeyName"]
        Sub_Field.append(x)

    return Sub_Field,pickle_file,Single

def map_characters_to_wordindex(text_str):

    """
    Description : Takes a string and maps each character to word index {ex: input_string = "Hello A" , output = [0,0,0,0,0,1,1]
    Input_Parameter  : string
    Returns : array
    """

    charcaters = [];word_arr = [];word = 0

    for i,c in enumerate(text_str) :
        charcaters.append(i)
        if c == " ":
            word+= 1
            word_arr.append(word)
        else :
            word_arr.append(word)

    return (word_arr)

def iterate_through_lines(total_lines):

    """
    Description : Takes the maximum line number in a dataframe , iterates over it to find keys and returns the found keys with the location information
    Input_Parameter : integer (i.e the maximum line number in a dataframe)
    Returns : dictionary (i.e if the config file keys matches in dataframe it updates to dictionary)
    """
    extracted_field_dictionary = dict()
    #print("Total Keys Present:" , len(Sub_Field))
    Keys_not_detected = set()

    for i in range(0,total_lines):
        df2 = df.loc[df['line_num'] == i]
        list_str = df2['text'].to_list()
        text_str = ' '.join(map(str, list_str))
        word_arr_index = map_characters_to_wordindex(text_str)
        #print(text_str)
        keys_with_locations,keys_detected = find_field_locations(Sub_Field,text_str,word_arr_index,df2,img)
        Keys_detected.update(keys_detected)
                #print(x)
        if len(keys_with_locations)!= 0:
            for items in keys_with_locations:
              extracted_field_dictionary.update({(items[0],items[1],items[2],items[3]):items[4]})

    for item in Sub_Field:
        if item not in Keys_detected:
            Keys_not_detected.add(item)

    #print("Keys detected:", len(Keys_detected))
    #acc = (len(Keys_detected)/len(Sub_Field))*100
    #print("Key Accuracy :",acc,"%")

    return extracted_field_dictionary

def find_accuracy(final_df):
     Keys_detected = set()
     df_keys = final_df['Field'].to_list()
     for item in df_keys:
        Keys_detected.add(item)
     Total_keys_present = len(Sub_Field)
     Keys_not_detected = Total_keys_present - len(Keys_detected)

     print("Total keys present:",Total_keys_present)
     print("Key value detected:",len(Keys_detected))
     accuracy = (len(Keys_detected)/Total_keys_present) * 100
     print("Accuracy:",accuracy,"%")


def extract_fields_and_values(ip_path,f_names,config_file_path,unique_id = None):

    global df,df2,img,Sub_Field,pickle_file,Keys_detected,final_table
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    start_time = time.time();Keys_detected = set();final_table = pd.DataFrame()

    path=os.path.join(os.getcwd(),'image')

    if config_file_path == "NA":
        with open(os.path.join(path,'config_claim.json')) as f:
            data_string = json.load(f)
    else:
        with open(config_file_path) as f:
            data_string = json.load(f)
    if unique_id == None:
        op_final_path=os.path.join(ip_path,'hocr')
        #create(op_final_path)

    else:
        final_path=os.path.join(ip_path,unique_id)
        create(final_path)
        create(os.path.join(final_path,'hocr'))
        op_final_path=os.path.join(final_path,'hocr')

    tbf_json = {}

    #Extracts the config file and saves it to arrays
    Sub_Field,pickle_file,Single = extract_post_json(config_file_path)
    f_names = ast.literal_eval(f_names)
    word_dict = read_picklefile(pickle_file)

    for file in f_names :

        f = os.path.join(ip_path,file)
        df2 = pd.DataFrame()

        #Reading the image
        img = cv2.imread(f)

        if img is not None:



            #Running hocr
            df = run_hocr(img)
            df.dropna(inplace=True)

            #Apply spell corrector to the text coloumn
            text_list = df['text'].to_list()
            corrected_text_list = spell_corrector(text_list,word_dict)
            df['text'] = corrected_text_list
            #print(corrected_text_list)
            #print(df.shape)
            df = df.replace('nan', np.nan)
            df.dropna(inplace = True)
            #df.to_csv("uniform.csv")
            #print(df.shape)
            #print(len(text_list), len(corrected_text_list))

            #Finding the maximum line number in the dataframe
            max_line_num_in_df = df.loc[df['line_num'].idxmax()]['line_num']
            #print(max_line_num_in_df)

            #Iterating through lines to search fields in config file
            extracted_field_dictionary= iterate_through_lines(max_line_num_in_df)
            #print(extracted_field_dictionary)

            #Iterating through extracted_field_dictionary to find values
            table,keyvalue_not_detected = find_values(extracted_field_dictionary,img,config_file_path,df)
            no_of_values_detected = len(Keys_detected) - len(keyvalue_not_detected)
            #print("Values detected:",no_of_values_detected)
            #print("Values not detected for keys:", keyvalue_not_detected)

            val_acc = (no_of_values_detected / len(Keys_detected))*100
            #print("Value Accuracy:",val_acc,"%")
            #table.to_excel("{}{}".format(os.path.join(op_final_path,file),'.xlsx'))

            if Single == 'No':
              final_table = final_table.append(table,ignore_index=True)
            else:
                final_table = table

        else:
            print("No image found")


    print(final_table)
    find_accuracy(final_table)
    tbf_json = final_table.to_json(orient='records')

    print("--- %s seconds ---" % (time.time() - start_time))

    return (tbf_json)

extract_fields_and_values('C:\\Users\\pragyan.das\\Desktop\\Automatic Information Extraction from Image',"['sample_form.png']","C:\\Users\\pragyan.das\\Desktop\\Automatic Information Extraction from Image\\config_sample.json")

