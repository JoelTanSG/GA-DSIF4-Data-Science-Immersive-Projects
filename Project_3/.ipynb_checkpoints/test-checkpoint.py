{
 "cells": [
  {
   "cell_type": "markdown",
   "id": "bd6da349",
   "metadata": {},
   "source": [
    "![](./assets/images/reddit_code_banner.png)\n",
    "[Image Source](https://preview.redd.it/k0ozkhhjubh31.jpg?width=2400&format=pjpg&auto=webp&s=6d44bf6a3a98bee16d1a70697b919fbd53a97796)"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "7b9281e2",
   "metadata": {},
   "source": [
    "## Problem Statement\n",
    "\n",
    "Is it clear what the goal of the project is?\n",
    "\n",
    "What type of model will be developed?\n",
    "\n",
    "How will success be evaluated?\n",
    "\n",
    "Is the scope of the project appropriate?\n",
    "\n",
    "Is it clear who cares about this or why this is important to investigate?\n",
    "\n",
    "Does the student consider the audience and the primary and secondary stakeholders?\n",
    "\n",
    "Data Scientist for a company looking to expand into Singapore and Malaysia. Tasked by the marketing department to look at reddit to see what are the hot topics of the day for both countries and if the citizens of these two countries have enough similiarities so that the marketing department would only need to create a single strategy. Or if they're starkly different, what are the difference so that the company would be better able to target the each country's populance. for an e commerce company that wants to speak the lingo of msia and sg online forum users\n",
    "\n",
    "I'll be webscrapping, eda, knives, drecisiontree, logisticReg..."
   ]
  },
  {
   "cell_type": "markdown",
   "id": "87ea9f6f",
   "metadata": {},
   "source": [
    "# Part 1 Data Collection and Cleaning"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "cd8bb1c3",
   "metadata": {},
   "source": [
    "## Table of Content\n",
    "\n",
    "1. [Data Collection](#Data-Collection)\n",
    "2. [Data Cleaning](#Data-Cleaning)\n",
    "\n",
    "\n",
    "\n",
    "\n",
    "\n",
    "\n",
    "\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 1,
   "id": "ccb5e125",
   "metadata": {},
   "outputs": [],
   "source": [
    "#Libraries\n",
    "import requests\n",
    "import pandas as pd\n",
    "import numpy as np\n",
    "import time\n",
    "import regex as re\n",
    "\n",
    "pd.options.mode.chained_assignment = None   # disable SettingWithCopyWarning: \n",
    "                                            # A value is trying to be set on a copy of a slice from a DataFrame"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "3c430f05",
   "metadata": {},
   "source": [
    "## Data Collection\n",
    "Scrapping reddit using a function that loops 15 times retrieving a 100 post each time to get 1,500 post for each chosen subreddit and then putting them each into a dataframe."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 2,
   "id": "4cea4ccd",
   "metadata": {},
   "outputs": [],
   "source": [
    "#Function to get 1,500 post from a subreddit and put it into a dataframe\n",
    "\n",
    "def webscrape_reddit(subreddit):\n",
    "    data = []\n",
    "    url = 'https://api.pushshift.io/reddit/search/submission'\n",
    "    header = {'User-agent':'GA DSIF-4 Student Project'}\n",
    "    count = 0\n",
    "    #starting from 0 loop 15 times to scrape 1,500 posts\n",
    "    while count < 15: \n",
    "        # set the parameter 'before' to get subsequent posts after the first 100\n",
    "        if count == 0:\n",
    "            params = {\n",
    "                'subreddit':subreddit,\n",
    "                'size':100\n",
    "            }\n",
    "        else:\n",
    "            params = {\n",
    "                'subreddit':subreddit,\n",
    "                'size':100,\n",
    "                'before': before #check last post ['created_utc'] to get time/date\n",
    "            }\n",
    "        count+=1\n",
    "        #actual requests/scrapping \n",
    "        res = requests.get(url,params,headers=header)\n",
    "        #Check if successful and if so to save to list called data and also extract the last post's date/time for params\n",
    "        if res.status_code == 200:\n",
    "            print('Status Code:',res.status_code,'of scrape count:',count)\n",
    "            post = res.json()['data']\n",
    "            before = post[-1]['created_utc']\n",
    "            data.extend(post)\n",
    "        else:\n",
    "            print('Error. Something when wrong. Status code:',res.status_code)\n",
    "            break\n",
    "        time.sleep(1)\n",
    "    #put results into a single dataframe    \n",
    "    df = pd.DataFrame(data)\n",
    "    print(f'Total number of post scrapped: {df.shape[0]}, from Subreddit: {subreddit}\\n')\n",
    "    return df"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 11,
   "id": "ff359872",
   "metadata": {
    "scrolled": false
   },
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Status Code: 200 of scrape count: 1\n",
      "Status Code: 200 of scrape count: 2\n",
      "Status Code: 200 of scrape count: 3\n",
      "Status Code: 200 of scrape count: 4\n",
      "Status Code: 200 of scrape count: 5\n",
      "Status Code: 200 of scrape count: 6\n",
      "Status Code: 200 of scrape count: 7\n",
      "Status Code: 200 of scrape count: 8\n",
      "Status Code: 200 of scrape count: 9\n",
      "Status Code: 200 of scrape count: 10\n",
      "Status Code: 200 of scrape count: 11\n",
      "Status Code: 200 of scrape count: 12\n",
      "Status Code: 200 of scrape count: 13\n",
      "Status Code: 200 of scrape count: 14\n",
      "Status Code: 200 of scrape count: 15\n",
      "Total number of post scrapped: 1500, from Subreddit: singapore\n",
      "\n",
      "Status Code: 200 of scrape count: 1\n",
      "Status Code: 200 of scrape count: 2\n",
      "Status Code: 200 of scrape count: 3\n",
      "Status Code: 200 of scrape count: 4\n",
      "Status Code: 200 of scrape count: 5\n",
      "Status Code: 200 of scrape count: 6\n",
      "Status Code: 200 of scrape count: 7\n",
      "Status Code: 200 of scrape count: 8\n",
      "Status Code: 200 of scrape count: 9\n",
      "Status Code: 200 of scrape count: 10\n",
      "Status Code: 200 of scrape count: 11\n",
      "Status Code: 200 of scrape count: 12\n",
      "Status Code: 200 of scrape count: 13\n",
      "Status Code: 200 of scrape count: 14\n",
      "Status Code: 200 of scrape count: 15\n",
      "Total number of post scrapped: 1499, from Subreddit: malaysia\n",
      "\n"
     ]
    }
   ],
   "source": [
    "# This cell is marked out to preserve the dataset used\n",
    "\n",
    "#scrape both subreddits\n",
    "\n",
    "#df_singapore = webscrape_reddit('singapore')\n",
    "#df_malaysia = webscrape_reddit('malaysia')\n",
    "\n",
    "#save the original scapped datasets\n",
    "\n",
    "#df_malaysia.to_csv('./assets/datasets/malaysia_raw.csv',index=False)\n",
    "#df_singapore.to_csv('./assets/datasets/singapore_raw.csv',index=False)"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "ec35a5fb",
   "metadata": {},
   "source": [
    "## Data Cleaning"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 2,
   "id": "37594985",
   "metadata": {},
   "outputs": [],
   "source": [
    "df_singapore = pd.read_csv('./assets/datasets/singapore_raw.csv')\n",
    "df_malaysia = pd.read_csv('./assets/datasets/malaysia_raw.csv')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 3,
   "id": "8125396f",
   "metadata": {
    "scrolled": true
   },
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Malaysia Dataset rows: 1499, columns: 86\n",
      "Singapore Dataset rows: 1500, columns: 81\n"
     ]
    }
   ],
   "source": [
    "# Check total columns and rows for each dataset\n",
    "datasets = {'Malaysia':df_malaysia,'Singapore':df_singapore}\n",
    "\n",
    "for c,df in datasets.items():\n",
    "    print(f'{c} Dataset rows: {df.shape[0]}, columns: {df.shape[1]}')"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "fec5fabb",
   "metadata": {},
   "source": [
    "Since there are extra variables in the Malaysian dataset, I shall drop them. And also drop any column within the Singapore dataset that does not match the Malaysian dataset."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 4,
   "id": "eea8a8be",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "dropped from Malaysia: crosspost_parent\n",
      "dropped from Malaysia: crosspost_parent_list\n",
      "dropped from Malaysia: poll_data\n",
      "dropped from Malaysia: collections\n",
      "dropped from Malaysia: call_to_action\n",
      "dropped from Malaysia: category\n",
      "dropped from Singapore: banned_by\n"
     ]
    }
   ],
   "source": [
    "# Isolate the extra variables in df_malaysia and drop them\n",
    "for col in list(df_malaysia.columns):\n",
    "    if col not in list(df_singapore.columns):\n",
    "        df_malaysia.drop(col,axis=1,inplace=True)\n",
    "        print(f'dropped from Malaysia: {col}')\n",
    "\n",
    "# Isolate the extra variables in df_singapore and drop them\n",
    "for col in list(df_singapore.columns):\n",
    "    if col not in list(df_malaysia.columns):\n",
    "        df_singapore.drop(col,axis=1,inplace=True)\n",
    "        print(f'dropped from Singapore: {col}')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 5,
   "id": "4caae817",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "After dropping duplicated posts, we're left with:\n",
      "Malaysia Dataset rows: 1476, columns: 80\n",
      "Singapore Dataset rows: 1437, columns: 80\n"
     ]
    }
   ],
   "source": [
    "# Check for duplicated posts by looking at the title and then dropping the duplicates\n",
    "for df in datasets.values():\n",
    "    df.drop_duplicates('title',keep='last',inplace=True)\n",
    "\n",
    "# Check shape of both \n",
    "print('After dropping duplicated posts, we\\'re left with:')\n",
    "for c,df in datasets.items():\n",
    "    print(f'{c} Dataset rows: {df.shape[0]}, columns: {df.shape[1]}')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 6,
   "id": "42329d95",
   "metadata": {},
   "outputs": [],
   "source": [
    "#save the datasets\n",
    "df_malaysia.to_csv('./assets/datasets/malaysia_cleaned.csv',index=False)\n",
    "df_singapore.to_csv('./assets/datasets/singapore_cleaned.csv',index=False)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 7,
   "id": "79ef7714",
   "metadata": {},
   "outputs": [],
   "source": [
    "# Combine both sets into a single dataset for further cleaning\n",
    "df_merge = pd.concat(datasets)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 8,
   "id": "d59a3e70",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th></th>\n",
       "      <th>title</th>\n",
       "      <th>author</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>Malaysia</th>\n",
       "      <th>585</th>\n",
       "      <td>1.FRESH VEGETABLES</td>\n",
       "      <td>Current_Green_6063</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>Singapore</th>\n",
       "      <th>514</th>\n",
       "      <td>1.FRESH VEGETABLES</td>\n",
       "      <td>Current_Green_6063</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>Malaysia</th>\n",
       "      <th>81</th>\n",
       "      <td>University degree</td>\n",
       "      <td>tysonreddit</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>Singapore</th>\n",
       "      <th>86</th>\n",
       "      <td>University degree</td>\n",
       "      <td>tysonreddit</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "                            title              author\n",
       "Malaysia  585  1.FRESH VEGETABLES  Current_Green_6063\n",
       "Singapore 514  1.FRESH VEGETABLES  Current_Green_6063\n",
       "Malaysia  81    University degree         tysonreddit\n",
       "Singapore 86    University degree         tysonreddit"
      ]
     },
     "execution_count": 8,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "#Check for duplicates between Singapore and Malaysia\n",
    "df_merge[['title','author']][df_merge.duplicated(['title'],keep=False)].sort_values(by=['title'])"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 9,
   "id": "fe80fa22",
   "metadata": {},
   "outputs": [],
   "source": [
    "# Drop duplicates between Singapore and Malaysia\n",
    "df_merge.drop_duplicates('title',keep='last',inplace=True) "
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 10,
   "id": "9f65fc84",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "Index(['all_awardings', 'allow_live_comments', 'author',\n",
       "       'author_flair_css_class', 'author_flair_richtext', 'author_flair_text',\n",
       "       'author_flair_type', 'author_fullname', 'author_is_blocked',\n",
       "       'author_patreon_flair', 'author_premium', 'awarders', 'can_mod_post',\n",
       "       'contest_mode', 'created_utc', 'domain', 'full_link', 'gildings', 'id',\n",
       "       'is_created_from_ads_ui', 'is_crosspostable', 'is_meta',\n",
       "       'is_original_content', 'is_reddit_media_domain', 'is_robot_indexable',\n",
       "       'is_self', 'is_video', 'link_flair_background_color',\n",
       "       'link_flair_richtext', 'link_flair_text_color', 'link_flair_type',\n",
       "       'locked', 'media_metadata', 'media_only', 'no_follow', 'num_comments',\n",
       "       'num_crossposts', 'over_18', 'parent_whitelist_status', 'permalink',\n",
       "       'pinned', 'pwls', 'retrieved_on', 'score', 'selftext', 'send_replies',\n",
       "       'spoiler', 'stickied', 'subreddit', 'subreddit_id',\n",
       "       'subreddit_subscribers', 'subreddit_type', 'thumbnail',\n",
       "       'thumbnail_height', 'thumbnail_width', 'title', 'total_awards_received',\n",
       "       'treatment_tags', 'upvote_ratio', 'url', 'whitelist_status', 'wls',\n",
       "       'author_flair_template_id', 'author_flair_text_color',\n",
       "       'link_flair_css_class', 'link_flair_template_id', 'link_flair_text',\n",
       "       'media', 'media_embed', 'post_hint', 'preview', 'secure_media',\n",
       "       'secure_media_embed', 'url_overridden_by_dest', 'removed_by_category',\n",
       "       'author_flair_background_color', 'gallery_data', 'is_gallery',\n",
       "       'suggested_sort', 'author_cakeday'],\n",
       "      dtype='object')"
      ]
     },
     "execution_count": 10,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "#Look at variables available and decide which to keep\n",
    "df_merge.columns"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "d117a366",
   "metadata": {},
   "source": [
    "There isn't an official document for the reddit parameters and one is left to make educated guesses on what each variable stand for from looking at the heading and content within.\n",
    "\n",
    "Some helpful guides I found on the subject matter:\n",
    "1. https://github.com/pushshift/api\n",
    "2. https://www.reddit.com/r/redditdev/comments/a1dn2p/any_documentation_on_post_properties_such_as/\n",
    "\n",
    "Some intial thoughts for EDA (Are there certain patterns that could be established of the different netizens?):\n",
    "1. Do one side embed more media then the other?\n",
    "2. Which side tend to upload more NSFW posts?\n",
    "3. Average number of comments per post?\n",
    "4. Which group tend to moderate more vigrously?\n",
    "\n",
    "Base on the above considerations I decided to retain the below few variables for EDA and ML purposes.\n",
    "* removed_by_category -> reason the post was removed\n",
    "* num_comments -> number of comments the post receive\n",
    "* over_18 -> tagged if post is NSFW\n",
    "* selftext -> content of the post \n",
    "* title -> title of the post\n",
    "* media_embed -> indicate if the post has a media embeded\n",
    "* subreddit -> identify whether the post is from Singapore or Malaysia"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 11,
   "id": "f4887b24",
   "metadata": {
    "scrolled": true
   },
   "outputs": [],
   "source": [
    "# Create final dataframe for part 2 EDA and ML\n",
    "df_final = df_merge[['removed_by_category',\n",
    "                     'num_comments','over_18','selftext',\n",
    "                     'title','media_embed','subreddit']]\n",
    "\n",
    "df_final.reset_index(inplace=True,drop=True)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 12,
   "id": "4109116e",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "removed_by_category    2063\n",
       "num_comments              0\n",
       "over_18                   0\n",
       "selftext               1799\n",
       "title                     0\n",
       "media_embed            2772\n",
       "subreddit                 0\n",
       "dtype: int64"
      ]
     },
     "execution_count": 12,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "#check for null values\n",
    "df_final.isnull().sum()"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "e6d02a20",
   "metadata": {},
   "source": [
    "As NaN refers to the fact that there was no attribute given for that variable/ post instead of being a missing value, I shall fill all NaN in removed_by_category as 'still_live' and for media to map it to 0 and 1"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 13,
   "id": "115eebb8",
   "metadata": {},
   "outputs": [],
   "source": [
    "df_final['removed_by_category'] = df_final['removed_by_category'].fillna('still_live')\n",
    "df_final['media_embed'] = df_final['media_embed'].apply(lambda x: 0 if x is np.nan else 1)"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "e084b62b",
   "metadata": {},
   "source": [
    "Finally I shall clean up the title and contents (selftext) of the posts using regular expression and lambda"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 31,
   "id": "58664e5b",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>removed_by_category</th>\n",
       "      <th>num_comments</th>\n",
       "      <th>over_18</th>\n",
       "      <th>selftext</th>\n",
       "      <th>title</th>\n",
       "      <th>media_embed</th>\n",
       "      <th>subreddit</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>0</th>\n",
       "      <td>still_live</td>\n",
       "      <td>0</td>\n",
       "      <td>False</td>\n",
       "      <td>Why non Slavs still decide to be in the Russia...</td>\n",
       "      <td>Why non Slavic ethnic in the Russian Federatio...</td>\n",
       "      <td>0</td>\n",
       "      <td>malaysia</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>1</th>\n",
       "      <td>still_live</td>\n",
       "      <td>0</td>\n",
       "      <td>False</td>\n",
       "      <td>How much revenue can hardware shop generate Se...</td>\n",
       "      <td>How much revenue can hardware shop generate</td>\n",
       "      <td>0</td>\n",
       "      <td>malaysia</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2</th>\n",
       "      <td>still_live</td>\n",
       "      <td>0</td>\n",
       "      <td>False</td>\n",
       "      <td>NaN</td>\n",
       "      <td>PRN Johor Perdana Menteri Tinjau Keadaan Anggo...</td>\n",
       "      <td>1</td>\n",
       "      <td>malaysia</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>3</th>\n",
       "      <td>still_live</td>\n",
       "      <td>0</td>\n",
       "      <td>False</td>\n",
       "      <td>NaN</td>\n",
       "      <td>PRN Johor Program Gotong Royong Bersama Pendud...</td>\n",
       "      <td>1</td>\n",
       "      <td>malaysia</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4</th>\n",
       "      <td>automod_filtered</td>\n",
       "      <td>0</td>\n",
       "      <td>False</td>\n",
       "      <td></td>\n",
       "      <td>Boleh pcaya ka puasa dan aidilfitri tak PKP</td>\n",
       "      <td>0</td>\n",
       "      <td>malaysia</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "  removed_by_category  num_comments  over_18  \\\n",
       "0          still_live             0    False   \n",
       "1          still_live             0    False   \n",
       "2          still_live             0    False   \n",
       "3          still_live             0    False   \n",
       "4    automod_filtered             0    False   \n",
       "\n",
       "                                            selftext  \\\n",
       "0  Why non Slavs still decide to be in the Russia...   \n",
       "1  How much revenue can hardware shop generate Se...   \n",
       "2                                                NaN   \n",
       "3                                                NaN   \n",
       "4                                                      \n",
       "\n",
       "                                               title  media_embed subreddit  \n",
       "0  Why non Slavic ethnic in the Russian Federatio...            0  malaysia  \n",
       "1        How much revenue can hardware shop generate            0  malaysia  \n",
       "2  PRN Johor Perdana Menteri Tinjau Keadaan Anggo...            1  malaysia  \n",
       "3  PRN Johor Program Gotong Royong Bersama Pendud...            1  malaysia  \n",
       "4        Boleh pcaya ka puasa dan aidilfitri tak PKP            0  malaysia  "
      ]
     },
     "execution_count": 31,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "# Remove Special characters\n",
    "df_final['title'] = df_final['title'].str.replace('[^0-9a-zA-Z]+',' ',regex=True)\n",
    "df_final['selftext'] = df_final['selftext'].str.replace('[^0-9a-zA-Z]+',' ',regex=True)\n",
    "\n",
    "# Remove digits\n",
    "df_final['title'] = df_final['title'].apply(lambda x:''.join(i for i in x if not i.isdigit()))\n",
    "\n",
    "# Remove white spaces at both ends\n",
    "df_final['title'] = df_final['title'].str.strip()\n",
    "df_final['selftext'] = df_final['selftext'].str.strip()\n",
    "\n",
    "# Replace the word removed from selftext \n",
    "# As it is just an indication that the post was deleted and not the actual content\n",
    "df_final['selftext'] = df_final['selftext'].apply(lambda x: '' if x =='removed' else x)\n",
    "\n",
    "df_final.head()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 32,
   "id": "fed79b50",
   "metadata": {},
   "outputs": [],
   "source": [
    "# Save final dataframe for part 2\n",
    "df_final.to_csv('./assets/datasets/combined_dataset.csv',index=False)"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.8.12"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
