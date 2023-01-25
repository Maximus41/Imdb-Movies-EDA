# DAP-Project-First-Semester-NCI
Project Source code for DAP Module - 1st Semester - MSc in Data Analytics - National College of Ireland
<h4>Steps to run the code:</h4>
<ul><b>1 -></b> Open <b>Anaconda Command Prompt</b></ul>
<ul><b>2 -></b> Goto Project folder</ul>
<ul><b>3 -></b> Run the command <b>"conda env create -f environment.yml"</b> to create conda environment</ul>
<ul><b>4 -></b> Run <b>"conda activate DAP"</b> to activate the environment</ul>
<ul><b>Note :<i></b> <b>MongoDB</b> and <b>PostgreSQL</b> should be already installed in the system to successfully run the code.</i></ul>


## Objective
Various study groups and institutions have 
conducted several studies on the criteria for success in the 
film business to date. According to one study, there are three 
factors by which a film's success can be measured. These are 
ratings given to a film by viewers and reviewers, as well as 
the picture's financial performance in its first few weeks and 
the number of awards it receives[1]. Using **ETL (*Extraction, Transformation and Loading*)** techniques, this project will organize various sources of unstructured data into structured format inorder to analyze 
datasets on the film industry based on aforementioned criterion. To 
extract information from the data, the project will use **EDA (*Exploratory Data Analysis*)** techniques available. The main objectives of EDA 
can be summarized as follows:
+ **Understand the dataset**
+ **Establish relationships between attributes**
+ **Find out abnormalities in the data**

## Methodology
Data collecting is the most important element of data 
analysis. This section mentions different types of data sources 
used in the project and takes through the different steps of 
the methodology employed to prepare them for exploratory 
analysis. The steps discussed here are taken from the KDD 
methodology used for the project. The following is a detailed 
description of the steps:

### *A.* Data Selection
The data was selected from four different sources. The 
sources are detailed in the table below **(Table 1)**

| Name | Type | Format | Tables | Link |
| :---- | :----: | :----: | :----: | :----: |
| Movielens | CSV | Structured | 4 | [Link](https://movielens.org/) |
| The Movie Database| API | JSON | NA | [Link](https://developers.themoviedb.org/3/movies/get-movie-details) |
| The Rapid API | API | JSON | NA | [Link](https://rapidapi.com/rapidapi/api/movie-database-alternative/) |
| Oscars| Website | Dictionary | NA | [Link](https://www.oscars.org/) |

***Table 1 : Data Sources***

Details of the tables used from the ***MovieLens*** Dataset are 
mentioned in the table **(Table 1.1)** below:

| Name | Attributes| Description |
| :---- | :----: | :----: |
| movies.csv | movieId, title, genre | Most basic details of the movie |
| links.csv | movieId, imdbId, tmdbId| Standard Imdb id and Tmdb id mapped to the movieId |

***Table 1.1 : MovieLens CSV Tables***

### *B.* Pre-processing
Jupyter Notebook was used to write and run the code 
for the entire project, using conda as its package manager. 
The packages used in the project for ETL and EDA are listed below:
Pandas
- **Pymongo**
- **Urllib3**
- **Selenium**
- **Psycopg2**
- **Sqlalchemy**
- **Seaborn**
- **Matplotlib**
- **missingno**

The conda environment containing the above mentioned packages were created from the *environment.yml* file by executing the following commands in *Conda prompt*:

```
• conda env create -f environment.yml
• conda env update -f environment.yml
• conda install ipykernel
• ipython kernel install --user --name=DAP
```

The final master dataset was obtained from all the four data sources following the ***ETL*** steps described below:

***Step 1 :*** \
The CSV files from the MovieLens dataset, was used to create a sorted list of 2000 movies released 
between 2009 to 2018. The data was sorted using the year 
value taken from the ***'title'*** column in the ***'movies.csv'*** file. 
Then, on the basis of ***'movieId'***, attribute, records from both the tables
***‘movies’*** and ***‘links’*** were merged to create a single collection. 
This combined table were then iteratively traversed to retrieve 
details from the APIs previously listed using the corresponding 
external ids.

***Step 2:***\
Both API responses have attributes that are both common 
and distinctive. They were both called to obtain detailed 
information about the films, and their responses were saved in 
MongoDB as JSON documents. In the data pipeline, 
MongoDB served as a good staging destination, allowing 
room to resume without having to contact the APIs again if 
data was corrupted during subsequent phases. The persistence 
of the data download state was another instance where 
MongoDB came through without any effort. One of the APIs 
has a daily limit of 1000 calls; thus, a JSON document was 
created to retain information about the latest state of the Http 
requests, which was then saved as a document in a separate 
collection titled 'State' in the MongoDB database.

***Step 3:***\
The final source of data provides raw data on Oscar wins 
and nominations under the categories of "Best 
Picture", "Directing", "Acting," and "Writing" for the years 
spanning between 2002 and 2018. The website for Academy 
Awards was scraped using Selenium to obtain this 
information. Selenium is a GUI testing tool that can automate 
web page clicks and extract data from the HTML content. The 
scraped data was then converted to JSON and placed in a 
MongoDB database as documents.

***Step 4:***\
ERDs (Entity Relationship Diagrams) were 
conceptualized to create tables in PostgreSQL with the data,
now available in MongoDB. By the end of this step, 6 SQL 
schemas and tables were created. These schemas are Movie, 
Director, Writer, Actor, Language, Genre, and 
Academy_awards. ‘Movie’ and ‘Academy_awards’ are the 
main tables whereas rest of them are multivalued attributes for 
‘Movie’.

***Step 5:***\
In the final step, following the creation of requisite SQL 
tables, the no-SQL documents were retrieved from the 
MongoDB database and transformed to corresponding Pandas
data frames as a preparatory stage before inserting data into 
the SQL database. The python package used for the purpose 
was 'sqlalchemy'. This Python library makes it easy to insert 
large amounts of data simultaneously into a PostgreSQL 
database. This is a quick operation for the project's 
relatively tiny amount of data (about 2k rows).