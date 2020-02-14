'''============================================
Title:  Key Extraction
Author: @pragyan.das
Date:   Friday October 25 2019
Description : This code takes extracted relevant parameters to identify the KeyName locations in respective json file of the form and returns a dictionary
Main Function Block : find_field_locations
Output : Dictionary
==============================================='''

import pandas as pd,cv2
from fuzzysearch import find_near_matches


def drawrectangle(rectangle_df,colour,img):
    """
    Description : this takes dataframe to draw rectangle and returns the x,y,w,h of the total dataframe
    Input_Parameter:
           rectangle_df: dataframe
           colour: tuple of colour (Ex: (0,0,255))
           img: IMAGE file
    Returns : x,y,w,h (i.e location of complete dataframe)
    """
    x= rectangle_df['left'].iloc[0]
    y= rectangle_df['top'].iloc[0]
    h= rectangle_df['height'].iloc[0]
    w = (rectangle_df['left'].iloc[-1] - x) + rectangle_df['width'].iloc[-1]
    cv2.rectangle(img, (x, y), (x + w, y + h), colour , thickness=3)

    return (x,y,w,h)

def slice_dataframe_to_matched_indexes(matched_dictionary,word_arr_index):
    """
    Description : this takes the dictionary and list of indexes of word array to slice the df2 ie Lined Dataframe and return back a new dataframe
    Input_Parameter:
           matched_dictionary : dictionary (type:dict())
           word_arr_index: list
    Returns : dataframe
    Note: It may return an empty dataframe sometime when the start index and end index are same
    """
    df3 = pd.DataFrame()
    for j, each_match_item in enumerate(matched_dictionary):
        start_idx = each_match_item[0]
        end_idx = each_match_item[1]
        #print(start_idx,end_idx)
        #print(len(word_arr)-1)
        #print(end_idx)
        #print("--------")
        try:
            df_start = word_arr_index[start_idx]
            df_end = word_arr_index[end_idx]
        except IndexError:
            #this is set to sympell distance...if max_edit_distance=1 in symspell_2.py, then set here max_indx_dist = 2
            try:
                max_indx_dis = 2
                df_start = word_arr_index[start_idx-max_indx_dis]
                df_end = word_arr_index[end_idx-max_indx_dis]
            except IndexError:
                pass



        #print(df_start,df_end)
        df3 = Line_dataframe.iloc[df_start:df_end]
        #print(df3)

    return df3


def find_field_locations(Sub_Field,line_str,word_arr_index,df2,img):
    """
    Description : this takes the .json file as input , reads and organises it into array
    Input_Parameter:
           Sub_Field : List of "KeyName" in config file (type:List)
           line_str: scentence (type: string)
           word_arr_index: List of index of words (type:List)
           df2 : sliced dataframe of the particular line   (Later referred as Line_dataframe in below section)
           img: IMAGE file (type:.png,.jpg,.tiff)
    Returns : array of tuples with field location (x,y,w,h) and KeyName
    """
    global Line_dataframe
    field_arr = [];Line_dataframe = pd.DataFrame(); keys_detected = set()
    Line_dataframe = df2

    for i,KeyName in enumerate(Sub_Field):

        #Running fuzzy search to match KeyNames to OCR line
        returned_match_dictionary = find_near_matches(KeyName.lower(), line_str.lower(), max_l_dist=1)

        if len(returned_match_dictionary)!=0:

            #Checkpoint to check which KeyName are being detected

            #print(KeyName)
            #print(line_str)
            #print(returned_match_dictionary)

            # iterate over the match dictionary to slice its positions over Line_dataframe
            df3 = slice_dataframe_to_matched_indexes(returned_match_dictionary,word_arr_index)

            if len(df3)!=0 :
                text_ = df3['text'].to_string()
                text_ = text_.replace('/', ' ')
                #list_word = df3['text'].to_list()
                list_word = text_.split(' ')
                no_of_words_in_str = len(list_word)
                no_of_words_in_item = len(KeyName.split(' '))

                if no_of_words_in_item <= no_of_words_in_str:
                    colour_red = (0,0,255)
                    x,y,w,h = drawrectangle(df3,colour_red,img)
                    field_tup = (x,y,w,h,KeyName)
                    keys_detected.add(KeyName)
                    field_arr.append(field_tup)

    return field_arr,keys_detected
