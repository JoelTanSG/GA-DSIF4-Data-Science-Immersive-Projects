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
import pickle
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
from sklearn.cluster import KMeans
from sklearn import neighbors
from sklearn.preprocessing import MinMaxScaler

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
    
# Remove duplicates in a string
def remove_duplicate_text(text):
    text_list=text.split()
    return " ".join(sorted(set(text_list),key=text_list.index))

# Train and save ball tree nearest neighbors model
def train_ball_tree(features):
    '''
    This take a dataframe, run it through MinMaxScaler and then train using ball tree nearest neighbors
    returning the 5 closest datapoint and then saving the model.
    Model returns two numpy array consisting of the distance and datapoints
    '''
    run = input('Warning! This may take 10-30mins to train.\nInput "Y" to train model else any other letter to skip.\n')
    if run.upper() == "Y":
        # Train model
        mms = MinMaxScaler()
        features = mms.fit_transform(features)
        ball_tree = neighbors.NearestNeighbors(n_neighbors=6, algorithm='ball_tree')
        ball_tree.fit(features)
        model = ball_tree.kneighbors(features)
        
        # Save model
        save_as = input('Save model as: ')
        pickle.dump(model,open("./"+save_as,"wb"))
        print(f'{save_as} has been saved to current folder')     
    else:
        print("You've chosen not to train the model.")
        
# Deploy ball tree algo
def ball_tree_recommender(book,df,id_list,col_title='title',col_author='author'):
    '''
    book = title of the book user would use to search for recommendation
    df = original dataframe used to train the model
    idlist = list of ids of titles generated from the model
    col_title = dataframes's column variable of the book's titles 
    col_author = dataframe's column variable of the book's author
    '''
    try:
        book = book.title()
        i = df[df[col_title] == book].index[0]
        recommendations = [df.loc[x][[col_title,col_author]] for x in id_list[i]]
        print('Book Recommendations:')
        count = 1
        for series in recommendations:
            if series[0] == book:
                count-=1
            else:
                print(count,series[0])
                print('  Author:',series[1].title(),'\n')
            count+=1
        return recommendations
    except:
        print(f'Sorry, the book, {book} is not in the recommender system')

# Cosine similarity using sentence transformer
def generating_cosine_similarity(numpy_array):
    '''
    This take a numpy array and returns the cosine similarity in the form of a dataframe
    '''
    run = input('Warning! This may take 1-2hours to generate.\nInput "Y" to run else any other letter to skip.\n')
    if run.upper() == "Y":
        st = SentenceTransformer('distilbert-base-nli-mean-tokens')
        encoding = st.encode(numpy_array, show_progress_bar=True)
        X = np.array(encoding)
        cs_df = pd.DataFrame(cosine_similarity(X))
        
        # Save model
        save_as = input('Save dataframe as: ')
        cs_df.to_pickle("./"+save_as+".pkl")
        print(f'{save_as} has been saved to current folder')     
    else:
        print("You've chosen not to generate the generator.")

# Run cosine_simlarity_recommender
def cosine_similarity_recommender(book,df,cs_df,col_title='title',col_author='author'):
    '''
    book = title of the book user would use to search for recommendation
    df = original dataframe used to train the model
    cs_df = cosine similarity dataframe generated by scf.generating_cosine_similarity()
    col_title = dataframes's column variable of the book's titles 
    col_author = dataframe's column variable of the book's author
    '''
    book = book.title()
    try:
        i = df[df[col_title] == book].index[0]
    except:
        print(f'Sorry, the book, {book} is not in the recommender system.')
        return None
    
    indices = list(cs_df.loc[i].sort_values(ascending=False).index)[1:6]
    books = df[col_title].loc[indices].values
    authors = df[col_author].loc[indices].values
    
    print('Book Recommendations:')
    count = 1
    for b,a in zip(books,authors):
        if b == book:
            count-=1
        else:
            print(count,b)
            print('  Author:',a.capitalize(),'\n')
        count+=1
        
    return books,authors

# Combine Recommender
def unpack_series(series):
    a=[]
    b=[]
    for x,y in series:
        a.append(x)
        b.append(y)
    return a,b

def combined_recommender(book_title,id_list1,id_list2,df,cs_df):
    print('Recommender 1')
    t1,a1 = unpack_series(ball_tree_recommender(book_title,df=df,id_list=id_list1))
    print('Recommender 2')
    t2,a2 = unpack_series(ball_tree_recommender(book_title,df=df,id_list=id_list2))
    print('Recommender 3')
    t3,a3 = cosine_similarity_recommender(book_title,df=df,cs_df=cs_df)
    
    combine_title = t1+t2+list(t3)
    combine_author = a1+a2+list(a3)
    result = pd.DataFrame({k:[v] for k,v in zip(combine_title,combine_author)}).T
    result.reset_index(inplace=True)
    result.rename(columns={'index':'Recommendations',0:'Author'},inplace=True)
    return result.iloc[1: , :]