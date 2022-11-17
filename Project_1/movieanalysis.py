#!/usr/bin/env python
# coding: utf-8

# 
# 
# # Project: Investigate a Dataset - [TMDB Movies]
# 
# ## Table of Contents
# <ul>
# <li><a href="#intro">Introduction</a></li>
# <li><a href="#wrangling">Data Wrangling</a></li>
# <li><a href="#eda">Exploratory Data Analysis</a></li>
# <li><a href="#conclusions">Conclusions</a></li>
# </ul>

# <a id='intro'></a>
# ## Introduction
# 
# ### Dataset Description 
# 
# > The dataset contains information on movies collected from The Movie Database (TMDb), including user ratings and revenue. The dataset contains different columns that will be useful to the analysis, said columns include popularity, budget, revenue, title, director, genre, production company, release date, release year, vote average, budget and revenue. 
# The dataset contains 10866 rows and 21 columns. The colums listed above will be used to answer the questins and pesent a thorough analysis of the dataset.
# 
# 
# ### Question(s) for Analysis
# > 1. Which year has the highest average votes?
# 
# > 2. Which year had the highest average revenue?
# 
# >3. How many movies are made per year?
# 
# >4. Which movie is the most popular and which are the top ten most popular movies?
# 
# >5. Which are the top ten movies with the highest revenue?
# 
# >6. Which movies are the top ten highest rated and who are the directors?
# 
# >7. Who are the top ten most popular diercros and which moves did they direct?
# 
# >8. Does popularity and vote average affect the revenue of the movies?
# 
# >9. Which are the top ten production companies based on the 
# 
# >10. Which are the top ten most profitable production comapnies?
# 
# >11. Which are th most commercially succesful movies years in movie production?

# In[156]:


#import statements for the package that will be used in tha analysis
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


# In[ ]:


# Upgrade pandas to use dataframe.explode() function. 
get_ipython().system('pip install --upgrade pandas==0.25.0')


# <a id='wrangling'></a>
# ## Data Wrangling

# In[ ]:


#uploading the dataset that will be used for the analysis
moviesdata = pd.read_csv("tmdbmovies.csv")


# In[159]:


#checking for the first rows of the dataset
moviesdata.head(10)


# In[160]:


#check the last rows of the dataset which will help check which is the last entry
moviesdata.tail(10)


# In[161]:


#checking the shape of the dataset to find the nuber of rows and columns
moviesdata.shape


# In[162]:


#check the information about the dataset, the datatypes ad others
moviesdata.info()


# In[163]:


#checking the missing values in the dataset
moviesdata.isnull().sum()


# In[164]:


#get the percentage of missing values to see if they can be dropped or filled with mean.
moviesdata.isnull().sum() * 100/len(moviesdata)


# From that analysis, missing values with the highest percentage are in columns that may be dropped since they will not be used in the analysis and for the production_companies, those missing values may be dropped as they are less than ten percent. 

# In[165]:


#drop columns
moviesdata.drop(columns=['imdb_id', 'cast','homepage', 'tagline','runtime', 'keywords', 'overview', 'budget_adj', 'revenue_adj'], inplace = True)


# In[166]:


#drop null values
moviesdata.dropna(inplace = True)
moviesdata.isnull().sum()


# In[167]:


#check duplicate values
moviesdata.duplicated().sum()


# In[168]:


#drop duplicate values
moviesdata.drop_duplicates(inplace = True)
moviesdata.duplicated().sum()


# Having removed the duplicates, null values, and dropped unnecessary columns, the data is ready for cleaning.

# 
# ### Data Cleaning
# > In this step, changing data types to ones that I can work with.

# In[169]:


#check the data type of the dataset
moviesdata.dtypes


# From the dataypes release date needs to be changed to the datetime format.

# In[170]:


#change the release_date to a datetime format
moviesdata['release_date'] = pd.to_datetime(moviesdata['release_date'])
#check to see if it has worked
moviesdata.dtypes


# Create a profits colums since most of the questions require that data

# In[171]:


#find the profit and create a column
moviesdata['profits'] = moviesdata.revenue - moviesdata.budget

#check to see if it was created
moviesdata.head()


# In[172]:


#describe the data
moviesdata.describe()


# <a id='eda'></a>
# ## Exploratory Data Analysis

# ### Question 1: Which year has the highest average votes?

# In[173]:


moviesdata.columns


# In[174]:


#check for the highest average votes
moviesdata.vote_average.max()


# In[175]:


#the question wants to display the year
moviesdata[moviesdata['vote_average']>=8.7]['release_year']


# In[176]:


#check for popluriry to compare if by having alot of vote average means you are the most popular.
pop_movies = moviesdata.popularity.max()


# In[177]:


moviesdata[moviesdata['popularity']>=pop_movies]['release_year']


# To answer the question, 2006 had the highest average votes but the data also showed that having the highest average votes does not make the movies popular.

# ###  Question 2  Which year had the highest average profits?

# In[178]:


#check the maximum profits earned by the movies
max_profit = moviesdata.profits.max()


# In[179]:


moviesdata[moviesdata['profits']>=max_profit]['release_year']


# 2009 had the highest average profits. From that it goes to show that even though 2006 and 2015 had the highest average votes and most popular it does not reciproate to high revenues.

# ###  Question 3   How many movies are made per year?

# In[180]:


#It is important to run this so as to get the columns names correctly.
moviesdata.columns


# In[181]:


#solve the question
moviesperyear= moviesdata['release_year'].value_counts()
moviesperyear


# ###  Question 4 Which movie is the most popular and which are the top ten most popular?

# The question seeks to find out of all the movies made for all those years, which is the most popular and which are the top ten most popular.

# In[182]:


moviesdata.columns


# In[183]:


#In question one, I had already ran the most popular average which was stored in the variable `pop_movies`. 
#Using that variable, I will run the most popular movie by name.
moviesdata[moviesdata['popularity']>=pop_movies]['original_title']


# In[184]:


#find the top ten most popular movies and the years they were released
top_ten=moviesdata.nlargest(10, 'popularity')[['original_title', 'release_year']].set_index('release_year')
top_ten


# The most popular movie is Jurrastic world whih was made in 2015 and also shows the other nine top movies.

# ###  Question 5 Which are the top ten movies with the highest revenue?

# In[185]:


top_ten_rev= moviesdata.nlargest(10, 'revenue')[['original_title', 'release_year','revenue']].set_index('release_year')
top_ten_rev


# In[186]:


#visualize the data
sns.set_style('darkgrid')
sns.set_palette('Set2')
sns.barplot(x='revenue', y = 'original_title', data = top_ten_rev,palette="winter_r", dodge = False);
sns.despine()


# ###  Question 6 Which movies are the top ten highest rated and who are the directors?

# The result has brought out the number of movies made each year starting with the most movies to the least. 2014ha the highest made movies which were 638

# In[187]:


moviesdata.columns


# In[188]:


topten_voteavg= moviesdata.nlargest(10, 'vote_average')[['original_title', 'director', 'vote_average']].set_index('director')
topten_voteavg


# In[189]:


sns.set_style('darkgrid')
sns.set_palette('Set2')
sns.barplot(x='vote_average',y='original_title', data = topten_voteavg, dodge = False, palette="tab10");


# ## Question 7 Who are the top ten most popular directors and which movies did they direct?

# In[190]:


moviesdata.columns


# In[202]:


popular_directors= moviesdata.nlargest(10, 'popularity')[['director','original_title', 'genres']].set_index('director')
popular_directors


# ## Question 8 Does popularity and vote average affect the revenue of the movies? 

# In[192]:


moviesdata.columns


# In[193]:


#for this question we need to create a scatter plot of the two.
#the first plot os for popularity and revenue
sns.scatterplot(x='popularity', y='revenue', data = moviesdata)


# In[194]:


#this plot is for vote_average and revenue
sns.scatterplot(x='vote_average', y='revenue', data = moviesdata)


# The scatterplot shows that popularity does affect revenue. Low popularity shows less revenues from the movies.

# # Question 9 Which are the top ten production companies based on the number of movies they have produced?

# In[195]:


moviesdata.columns


# In[196]:


movies_counts = moviesdata['production_companies'].value_counts()
movies_counts


# In[197]:


topcompany=movies_counts.head(10)
topcompany


# From the analysis, the data shows that the top production company with the most number of movies Paramount pictures

# # Question 10 Top ten most profitable production companies.

# In[198]:


moviesdata.columns


# In[199]:


prof_companies= moviesdata.nlargest(10, 'profits')[['production_companies', 'profits','genres']].set_index('profits')
prof_companies


# # Question 11 Which are the top ten most commercially succesful years in movie production

# In[200]:


succesful_years = moviesdata.nlargest(10, 'revenue')[['revenue', 'release_date', 'release_year']].set_index('release_year')
succesful_years


# <a id='conclusions'></a>
# ## Conclusions

# > The questions were a great way to analyze the data and get to understand it even more. From my analysis I have made a few conclusions which are going to be analysed in this section.
# 
# > The data showed that popularity and the highest vote average does not make the the movie profitable, 2006 and 2015 were the years that had the highest vote average and most popular cosequetivley yet they awere not the most popular. Which showed by the scatterplot in **Question 8** both of these variables do affect the revenue. The lower the revenue in both instances popularity was low and so was the vote average.
# 
# > 2014 had the most number of movies made of all the years and 1969 had the least number of movies made. The analysis showed that the number of movies made each year has increased since 1969 and following that trend the numbers ae sure to increase.
# 
# > The most popular movie was Jurrasic World and among the top ten most popular movies,yet it was not the commercially succesful movie although it was in the top ten categories.  What I found interesting is that for the commercially sucesful movies only one of them was among the top commercially succesful movies. Goes to prove the first point that popularity does not equal to a movie being commercially successful.
# 
# >The highest rated top ten movies was also an interesting analysis as the top ten highest rated movies none of them made it as the top ten commercially succesfull movies proving that best ratings do not equal profits.
# 
# > On director popularity, **Colin Trevorrow** is the most popular based on the movie **Jurrasic World** and the genres vary.
# > **Paramount Pictures** has produced the most movies over the years yet it is not the most profitable production company showing that a prpduction company is not necessarity bring in alot of revenue based on the number of moves they have done.
# 
# ## Limitations
# > The dataset had a lot of null values.
# 
# ## Resources
# > https://stackoverflow.com/questions/22219004/how-to-group-dataframe-rows-into-list-in-pandas-groupby
# >https://indianaiproduction.com/seaborn-scatter-plot/
# >https://machinelearningknowledge.ai/seaborn-bar-plot-with-sns-barplot-examples-for-beginners/
# >https://stackoverflow.com/questions/43178137/how-do-i-plot-a-bar-graph-using-pandas
# >https://pythonspot.com/pandas-groupby/
# >https://book4you.org/book/3367370/62327b
# 
# 
# 

# In[203]:


from subprocess import call
call(['python', '-m', 'nbconvert', 'Investigate_a_Dataset.ipynb'])


# In[ ]:




