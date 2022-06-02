import pandas as pd
import numpy as np
import os
import wptools
import time
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import matplotlib.pyplot as plt
import seaborn as sns

# Read json file given
def read_df(filepath):
    df = pd.read_json(filepath,lines=True)
    print("List Loaded: ",filepath[2:-3])
    print(f"Rows: {df.shape[0]}, Columns: {df.shape[1]}")
    try:
        print(f"Data not captured from url: {df.title.isnull().sum()}")
    except:
        pass
    return df

# Create and Save a dataframe from a list of json files
def create_df_from_json_files(typ):
    '''typ = The type of json list to load
    in this case either book or author.
    ---
    This function grabs the type of json files indicated,
    loop through the directory to concat them together into a single dataframe
    '''
    print("---START---")
    lst_json = [json for json in os.listdir("./raw_datasets/scrapped_json_files/") if (json.endswith(".jl")) & (json.startswith(typ))]
    lst_df = [read_df("./raw_datasets/scrapped_json_files/"+json) for json in lst_json]
    df = pd.concat(lst_df,ignore_index=True)
    df.to_csv(f"./raw_datasets/{typ}.csv",index=False)
    print("\nConcatenated Dataframe")
    print(f"Rows: {df.shape[0]}, Columns: {df.shape[1]}")
    print(f"Total Null Values: {df.isnull().sum().sum()}")
    print(f"Saved to: raw_datasets/{typ}.csv\n---END---\n")
    return df

# Scrape wikipedia infobox
def wiki_infobox(item):
    search = wptools.page(item,slient=True).get_parse(show=False)
    time.sleep(1)
    return search.data['infobox'] 

# Clean the key pages from the info box scrapped.
def clean_pages(value):
    to_remove = ["*","{","}","[","]","(",")"]
    value = [x for x in value if x not in to_remove]
    value = ''.join(i for i in value if (i.isnumeric()) | (i == ' '))
    return value.split(" ",1)[0]

# Add spacing to title/name
def add_space_if_capital(strng):
    strng = strng+" Abc"
    for i in range(len(strng)):
        if (strng[i].isupper()) & (strng[i-1] != " ") & (i !=0):
            print(strng[i])
            strng= (strng[:i])+" "+(strng[i:])
    return strng[:-4]

# Remove special characters in genre
def remove_special_characters(s):
    to_remove = ["[","{","}","[","]","|","(",")"]
    for x in s:
        if x in to_remove:
            s = s.replace(x,' ')
    s = s.replace('genre',' ')
    s = s.replace('flatlist',' ')
    s = s.replace('\n*',' ')
    s = re.sub('[^A-Za-z0-9]+ ', ' ',s)
    return ', '.join(s.split())

# Scrape wikipedia info-box
def wptools_scrape_save_tocsv(df,save_to):
    instruct = input("WARNING: This takes 1-2 hours to run!\nInput Y to run, or any other letters to skip: ") #Prevent running if not needed.
    if instruct.casefold() == 'y':
        missing_info = []
        for book_ in df['title'][df['num_pages'].isnull()]:
            try:
                missing_info.append(wiki_infobox(book_))
            except:
                pass
        #remove None from list
        missing_info = [x for x in missing_info if x != None]

        # Some titles are captured as other items then books.
        # Drop those by keeping only those with the key 'pages'
        missing_info = [item for item in missing_info if 'pages' in item]

        '''#Keep only info that's needed
        to_keep = ['name','language','pages','genre','publication date']
        for info in missing_info:
            for key in info.copy():
                if key not in to_keep:
                    del info[key]
                else:
                    pass'''

        # Clean up info scrapped from info box
        for index,info in enumerate(missing_info):
            try:
                info['pages'] = clean_pages(info['pages']) # clean pages
            except:
                pass
            try:
                info['language'] = missing_info[index]['language'].split()[0] # clean language
            except:
                pass
        # Clean name
            info['name'] = missing_info[index]['name'].replace('<br>',' ') 
        # Add spacing to name
            info['name'] = add_space_if_capital(info['name'])
        # Clean genre 
            try:
                info['genre'] = remove_special_characters(info['genre'])
            except:
                pass

        #remove duplicate dicts
        missing_info = [dict(t) for t in {tuple(d.items()) for d in missing_info}]

        #some results returned are not the same books as such drop them
        for m in missing_info:
            if m['name'] not in list(df['title']):
                missing_info.remove(m)

        #Convert and Save to csv to concat with main df: books
        pd.DataFrame(missing_info).to_csv(save_to,index=False)
    else:
        pass
    
# Comparing two dataframes, replace the reference dataframe
# with the main dataframes index so that I can use combine_first
# to fill in the null value for the main dataframe
def index_conversion(df1,df2,refcolumn,nullcolumn):
    '''
    df1 = main dataframe with null values
    df2 = reference dataframe with values to plug into main
    refcolumn = name of column that is the same in both dataframes
    nullcolumn = name of column with null values
    '''
    for title in df1[refcolumn][df1[nullcolumn].isnull()]:
        if title in list(df2[refcolumn]):
            x = df1[df1[refcolumn]==title].index[0]
            y = df2[refcolumn][df2[refcolumn]==title].index[0]
            df2.rename(index={y:x},inplace=True) 

# Functions from project 3 Reddit Classification

#----#
#Function to lemma column in dataframe
def lemma_column(dataframe,column):
    wl = WordNetLemmatizer()    
    #Lemmatize
    dataframe[column]=dataframe[column].apply(lambda x: [wl.lemmatize(word,pos='v') for word in x])
    return dataframe

# Function to filter out stopwords
def remove_stopwords(dataframe,column):
    #assign variable to stopwords
    sw = stopwords.words('english')
    
    #extend additional stopwords
    sw.extend(['rus','th','hi','nd', 'k', 'de', 'bd', 'f', 'fi', 'x', 'ii', 'n', 'go', 'r', 'us', 'e', 'dc', 'tv', 'st'])
    
    #apply lambda to remove stopwords.
    dataframe[column] = dataframe[column].apply(lambda x:' '.join([i for i in x.split() if i not in sw]))
    
    return dataframe

# Flatten nested items
def flatten(object):
    for item in object:
        if isinstance(item,(list,tuple,set)):
            yield from flatten(item)
        else:
            yield item
#----#

# find index position of first blank in string
def blank_index(text):
    for i in range(len(text)-1):
        if text[i] ==" ":
            return i
    return None

# Bar plots
def plot_df(df,x,y,title):
    df.reset_index(inplace=True)
    df.rename(index={y:''},inplace=True)
    df.rename(columns={'index':y},inplace=True)
    plt.figure(figsize=(15,5))
    plt.title(title,size=20)
    sns.set_style('white')
    plot = sns.barplot(y=y,x=x,data=df,palette="rocket")
    plt.xlabel("")
    plt.ylabel("")

    values = [x for x in df[x]]
    index = df.index

    for i,v in zip(index,values):
        plot.text(y=i+0.2,x=v+0.05,s=int(v),size=12)

    sns.despine(left=True,bottom=True)

    plot.grid(False)
    plot.tick_params(axis='x',labelbottom=False)
    plt.savefig("./images/"+title+".png",bbox_inches='tight',dpi=150);
    
    return list(df[y])

def plot_df_books(df,x,title,p):
    plt.figure(figsize=(15,5))
    plt.title(title,size=20)
    sns.set_style('white')
    plot = sns.barplot(y='title',x=x,data=df,palette="rocket")
    plt.xlabel("")
    plt.ylabel("")

    values = [x for x in df[x]]
    au = [x for x in df['author']]
    index = df.index

    for i,v,a in zip(index,values,au):
        plot.text(y=i+0.2,x=v+0.05,s=str(p(v))+" "+a,size=12)

    sns.despine(left=True,bottom=True)

    plot.grid(False)
    plot.tick_params(axis='x',labelbottom=False)
    plt.savefig("./images/"+title+".png",bbox_inches='tight',dpi=150);