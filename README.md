# IMDB - Sentiment Analysis
This project is about analyzing the comment sentiment of users in IMDB website.
We utilize Cinemagoer library formerly called PyIMDB for collecting some information related to the movies metadata including the user's comment. 
For the initial load, we did an ETL activity for extracting the data from csv flat file which has data movies, tv series, shows, etc.
In this project, we filtered the data only focusing for movies and the data only until March 2024. 
If you try to collect the recent movies, you would not be able to retrieve the list of the movies. 

## How to use the app. 

### - Movie Filter Text Field and Filter button
This app uses streamlit as the front-end framework tool. 
In the beginning, the user would see a filter movie text field. 
The user has to fill the field with three characters in minimum. 
Once user has typed the keyword of the movies, User could directly press on filter button to populate the list of movies that contain that word(s). 
This button would populate the information from sqlite database and insert the relevant movies to the dropdow list at the button of Filter button. 

### - Movie Dropdown and Process button 
Once the movies list being populated from the sqlite database. You can pick your movie information immediately and you can press process buton to start processing the movie information. 
Process button would do several processes in the background. 
At the beginning, it would collect the movie id information from selected combo box.Then, it would call Cinemagoer library function to populate movies metadata such as Title, Movie Picture, Writer, Director, Cast, Genre and Rating.

### - User Rating 
In this section, there are two information would be shown in the page. The total cummulative rating from whole comments and 25 lastest comments rating. 
After the movie title, writer, etc. being populated, the next process is system calls reviews function through Cinemagoer function library. 
For the rating, it is stored inside pandas DataFrame, it is summed based on the rating level and system visualize the rating data using matplotlib framework that embdedded through streamlit component.
For the reviews, it would be processed for sentiment analysis. 

### - User Comment Sentiment
In previous section, we have mentioned that the reviews being called through Cinemagoer get reviews function library. 
The reviews comment is stored inside Pandas DataFrame. System does the data cleansing, word-tokenizing and n-grams. 
And the information are stored inside the Pandas DataFrame columns. 
The system uses Spacy library for doing Sentiment Analysis and some tokenize words we visualize through the wordcloud library. 
And the output from the Spacy library is The Sentiment of comment either Positive / Negative and the comment itself is Subjective based or Objective based. 
After that, the system shows 10 top ngram words inside the check-box component. 
The user could easily select the preferable word to show the review that contains that kind of word through DataFrame component underneath this check-box component. 

