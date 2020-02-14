'''============================================
Title:  Value Extraction
Author: @pragyan.das
Date:   Friday October 25 2019
Description : This code takes relevant parameters to identify the Value locations and return a valid Value of respective KeyName in dictionary
Main Function Block : find_values
Output : Dataframe
==============================================='''

import pandas as pd,re,time,json


def extract_post_json(posted_file):
    """
    Description : this takes the .json file as input , reads and organises it into array
    Input_Parameter  : JSON file(.json)
    Returns : arrays
    """
    Sub_Field = [];Key_field_Type = [];Main_Field = [];Direction = [];Max_Line = [];Width_multiplier = [];Height_multiplier=[]

    with open(posted_file, 'r') as j:
         post = json.load(j)


    for key in enumerate(post["KeyValue"]) :
        idx = key[0]
        x = post["KeyValue"][idx]["KeyName"]
        Sub_Field.append(x)
        y = post["KeyValue"][idx]["ValueType"]
        Key_field_Type.append(y)
        z = post["KeyValue"][idx]["MainKey"]
        Main_Field.append(z)
        k = post["KeyValue"][idx]["To_direction"]
        Direction.append(k)
        l = post["KeyValue"][idx]["MaxLine"]
        Max_Line.append(l)
        m = post["KeyValue"][idx]["Width_multiplier"]
        Width_multiplier.append(m)
        h = post["KeyValue"][idx]["Height_multiplier"]
        Height_multiplier.append(h)

    return Sub_Field,Key_field_Type,Main_Field,Direction,Max_Line,Width_multiplier,Height_multiplier


def is_date(input):
    """
    Description : this takes a string to check if its a valid date
    Input_Parameter: string
    Returns : boolean value
    """
    try :
       day,month,year = input.split('/')
       if day.isnumeric()==True & month.isnumeric()==True & year.isnumeric()== True:
           #print(input , "True")
           return True
    except ValueError :
       return False

def isTime(input):
    """
    Description : this takes a string to check if its a valid Time
    Input_Parameter: string
    Returns : boolean value
    """
    try:
        time.strptime(input, '%H:%M')
        return True
    except ValueError:
        return False

def isString(input):
    """
    Description : this takes a string to check if its a valid string
    Input_Parameter: string
    Returns : boolean value
    """
    try:
        result = isinstance(input,str)
        return result
    except ValueError:
        return  False

def isalnumeric(input):
    """
    Description : this takes a string to check if its a valid alphanumeric
    Input_Parameter: string
    Returns : boolean value
    """
    try:
        result = input.isalnum()
        return result
    except ValueError:
        return  False

def isNum(input):
    """
    Description : this takes a string to check if its an Integer
    Input_Parameter: string
    Returns : boolean value
    """
    try:
        result = input.isnumeric()
        return result
    except ValueError:
        return  False

def isfloat(value):
    """
    Description : this takes a string to check if its a float
    Input_Parameter: string
    Returns : boolean value
    """
    try:
        float(value)
        return True
    except ValueError:
        return False



def validate_values(value_list,value_type):
    """
    Description : this takes list of values to validate whether it belongs to respective type
    Input_Parameter:
           value_list: list
           value_type: string
    Returns : list
    """

    #print(value_list)
    value_clean = []
    for item in value_list:
        item = re.sub('[-(),["“”{}€<>=*|+‘;@$!¢~\\?°#§_»—]', '', item)
        res = bool()
        #print(item)
        if value_type == 'isNum':
            res = item.isnumeric()
            #print(item,res)
        elif value_type == "isString":
            res = isinstance(item,str)
            #print(item,res)
        elif value_type == "isalnumeric":
            res1 = item.isalnum()
            res2 = item.isalpha()
            res3 = item.isnumeric()
            if res1 == True and res2 == False and res3 == False:
                res = True
                #print(item,res)
        elif value_type == "is_date":
            res = is_date(item)
            #print(item,res)
        elif value_type == "isTime":
            res = isTime(item)
            #print(item,res)
        elif value_type == "price_str":
            res = isfloat(item)
            #print(item,res)
        else:
            pass

        if res == True:
            value_clean.append(item)

    return value_clean

def Down(x,y,w,h,width_m,height_m,lines):
    """
    Description : this takes (x,y,w,h)location of a KeyName and Max_Line to make a search to main dataframe with below conditions towards direction Down
    Input_Parameter:
           x,y,w,h: x-axis point , y-axis point , width of rectangle , height of rectangle
          lines: Max lines the value is covering
    Returns : dataframe
    Note: With below search conditions it searches the main dataframe and returns the True values
    """
    #print(x,y,w,h)
    #dist = 60
    offset_x_axis = 20
    x_min = x-offset_x_axis
    x_max = (x+(img_width*width_m))    ##sets the x axis search limit i.e towards right
    space = abs(h/2)

    y_min = y + space
    y_max = (y + h + (img_height*height_m*lines))

    #print(x_min,x_max,y_min,y_max)
    extracted_df['bool'] = (extracted_df['left']>=x_min) & (extracted_df['left']<=x_max) & (extracted_df['top'] > y_min) & (extracted_df['top'] < y_max)
    df2 = extracted_df.loc[extracted_df['bool'] == True]
    #df2.reset_index(inplace=True)
    #print(df2)
    return(df2)

def Right(x,y,w,h,width_m,height_m,lines):
    """
    Description : this takes (x,y,w,h)location of a KeyName and Max_Line to make a search to main dataframe with below conditions towards direction Right
    Input_Parameter:
           x,y,w,h: x-axis point , y-axis point , width of rectangle , height of rectangle
          lines: Max lines the value is covering
    Returns : dataframe
    Note: With below search conditions it searches the main dataframe and returns the True values
    """

    space = int(h/2)

    x_min = x+w
    x_max = int(x+(img_width*width_m))

    y_min = int(y - (img_height*height_m))
    y_max = int(y + h + space)

    #print(x_min,x_max,y_min,y_max)

    extracted_df['bool'] = (extracted_df['left']> x_min) & (extracted_df['left']< x_max) & ((extracted_df['top'] >= y_min) & (extracted_df['top'] <= y_max ))
    df2 = extracted_df.loc[extracted_df['bool'] == True]

    return (df2)

def Up(x,y,w,h,width_m,height_m,lines):
    """
    Description : this takes (x,y,w,h)location of a KeyName and Max_Line to make a search to main dataframe with below conditions towards direction Down
    Input_Parameter:
           x,y,w,h: x-axis point , y-axis point , width of rectangle , height of rectangle
          lines: Max lines the value is covering
    Returns : dataframe
    Note: With below search conditions it searches the main dataframe and returns the True values
    """

    space = int(h/2)

    x_min = x-10
    x_max = int(x+(img_width*width_m))    ##sets the x axis search limit i.e towards right

    y_min = (y - int(height_m*img_height))
    y_max = y-space

    extracted_df['bool'] = (extracted_df['left']>=x_min) & (extracted_df['left']<=x_max) & (extracted_df['top'] >= y_min) & (extracted_df['top'] < y_max)
    df2 = extracted_df.loc[extracted_df['bool'] == True]
    #df2.reset_index(inplace=True)
    #print(df2)
    return(df2)

def find_values(dict1,img,config_file_path,df):

    """
    Description : this takes below described parameters to search for value of respective KeyName in input dictionary
    Input_Parameter:
           dict1: dictinary of Keynames with (x,y,w,h) locations
           img: IMAGE file (.png,.jpg,.tiff, etc...)
           config_file_path : the path where the configuration file is stored for above image (type:json)
           df: main dataframe
    Returns : dataframe
    """

    global img_height,img_width,channels,extracted_df,Sub_Field,Key_field_Type,Direction,Max_Line,Width_multiplier
    img_height, img_width, channels = img.shape
    keys = [] ; values = [];Keyvalue_not_detected = set()
    extracted_df = df
    #key_value_tbf = pd.DataFrame()
    Sub_Field,Key_field_Type,Main_Field,Direction,Max_Line,Width_multiplier,Height_multiplier = extract_post_json(config_file_path)
    #print(Height_multiplier)

    for k,v in dict1.items():
        x = k[0] ; y = k[1] ; w = k[2] ; h = k[3] ; dist = 50
        txt_str = " "; direction  = " "; value_type = " "; lines_ = 0 ;

        if v in Sub_Field:
            indices = [i for i, x in enumerate(Sub_Field) if x == v]
            #print(v)
            for idx in indices:
                direction = Direction[idx]
                value_type = Key_field_Type[idx]
                lines_ = Max_Line[idx]
                width_m = Width_multiplier[idx]
                height_m = Height_multiplier[idx]

                df2 = eval('{}({},{},{},{},{},{},{})'.format(direction,x,y,w,h,width_m,height_m,lines_))
                #print(df2)

                if len(df2)!= 0:
                    #print(v)
                    txt_lst = df2['text'].to_list()
                    #print(txt_lst)
                    res = validate_values(txt_lst,value_type)
                    #print(res)

                    if len(res)!= 0:
                        res_str = ' '.join([str(elem) for elem in res])
                        keys.append(v)
                        values.append(res_str)

    d = {'Field':keys,'Values':values}
    key_value_tbf = pd.DataFrame(d)

    for k,v in dict1.items():
        if v not in keys:
            Keyvalue_not_detected.add(v)

    #print("Values not detected for Keys:" , Keyvalue_not_detected)

    return(key_value_tbf,Keyvalue_not_detected)
