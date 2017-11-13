"# Parser_and_Flask" 

Used Libraries: psycopg2, requests, zipfile, BeautifulSoup and Flask

There is too modules here:
Parser.py for downloading, unzipping, parsing an xml file
and second - flask application for displaying information in the browser (can start it with running run.py)

Parser.py contains 5 functions:
Download() function downloading an archiv from given source

unarchiv() unzipping file in that archiv

CreateDb() is a function for creating table on data base

Filling_table() is a function that parse and fills the table

Ìaster() - master function which calls all other functions

I used postgrass for bd with user: alex_korentsvit and password: qwerty. DB name: uo_db2.