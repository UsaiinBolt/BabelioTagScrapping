# -*- coding: utf-8 -*-
"""
Created on Wed Mar 22 19:34:25 2023

@author: UsaiinBolt
"""
import requests
from bs4 import BeautifulSoup
import re
import sqlite3

#request the page data
def get_pages_data(url):
    response = requests.get(url)
    if response.status_code == 200:
        content = response.content
    else :
        return print('error request url')
    soup = BeautifulSoup(content,'html.parser')
    return soup

#scrap the title
def get_title(soup):
    corps = soup.find('h1',attrs = {'itemprop':'name'})
    a_tag=corps.find('a')
    title=a_tag.text.strip()
    return title

#scrap the author
def get_author(soup):
    corps = soup.find('span',attrs = {'itemprop':'author'})
    a_tag=corps.find('span')
    author=a_tag.text.strip()
    return author

#scrap the ean that will be used as id
def get_ean(soup):
    corps = soup.find('div',attrs = {'class':'livre_refs grey_light'})
    ean=corps.text.strip()
    return ean[6:19]

#get the rating, the number of rating and the number of review
def get_rating(soup):
    corps = soup.find('span',attrs = {'itemprop':'ratingValue'})
    rating = corps.text.strip()
    corps = soup.find('span',attrs = {'itemprop':'ratingCount'})
    nbrating = corps.text.strip()
    corps = soup.find('meta',attrs = {'itemprop':'reviewCount'})
    nbreview = corps['content']
    return rating,nbrating,nbreview

#get the tags associated with the book
def get_tag(soup):
    corps = soup.find('p',attrs = {'class':'tags'})
    tags = corps.find_all('a')
    tag=[]
    for i in range(len(tags)):
        href = tags[i]['href']
        tag_id = re.findall(r'\d+', href)
        if len(tag_id)>2:
            tag_id = tag_id[len(tag_id)-1]
        else:
            tag_id=tag_id[0]
        tag.append([int(tag_id),tags[i].text.strip()])
    return tag

#export the data ready to be put in the database
def export_data(soup):
    r = get_rating(soup)
    try:
        rating=float(r[0])
    except:
        rating=None
    book = (get_ean(soup),get_title(soup),get_author(soup),rating,int(r[1]),int(r[2]))
    tags = get_tag(soup)
    return book,tags

#create the database 
db = sqlite3.connect('Babelio.db')

"""
#création de la table de livre
db.execute('''CREATE TABLE Book
           (id INTEGER PRIMARY KEY,
            Ean TEXT,
            Title TEXT,
            Author TEXT,
            Rating FLOAT,
            RatingNumber INT,
            ReviewNumber INT,
            Url TEXT,
            Babelio_id INT)''')
           
#création de la table de tags
db.execute('''CREATE TABLE Tags
           (id INTEGER PRIMARY KEY,
            idtag INT,
            tag TEXT)''')
           
#Création de la table faisant la liaison entre les livres et les tags
db.execute('''CREATE TABLE LiaisonTagBook
           (book_ean TEXT,
            book_title TEXT,
            tag_id INTEGER,
            PRIMARY KEY (book_ean, tag_id),
            FOREIGN KEY (book_ean) REFERENCES Book(Ean),
            FOREIGN KEY (book_title) REFERENCES Book(Title),
            FOREIGN KEY (tag_id) REFERENCES Tags(idtag))''')
"""

def Add_to_DB(url):
    print(url)
    soup = get_pages_data(url)   
    try:
        book,tags = export_data(soup)
    except:
        return print('erreur avec le livre :',url)
    
    c=db.cursor()
    #ajout du livre dans la base de donnée
    
    #detection de l'id babelio du livre
    babelio_id = re.findall(r'\d+',url)
    babelio_id = int(babelio_id[len(babelio_id)-1])
    
    c.execute("SELECT * FROM Book WHERE Ean=?",(book[0],))
    result = c.fetchone()
    if result:
        return print('le livre ',book[1],' existe deja dans la base de donnée')
    else:
        c.execute("INSERT INTO Book (Ean,Title,Author,Rating,RatingNumber,ReviewNumber,Url,Babelio_id) VALUES (?,?,?,?,?,?,?,?)",(book[0],book[1],book[2],book[3],book[4],book[5],url,babelio_id))
        db.commit()
        
    #ajout des tags dans la base de donnée et création des liens
    for i in range(len(tags)):
        #création du tag si inexistant
        c.execute("SELECT * FROM Tags WHERE idtag=?",(tags[i][0],))
        result = c.fetchone()
        if not(result):
            c.execute("INSERT INTO Tags (idtag,tag) VALUES(?,?)",(tags[i][0],tags[i][1]))
        #création du lien
        try:
            c.execute("INSERT INTO LiaisonTagBook (book_ean,book_title,tag_id) VALUES (?,?,?)",(book[0],book[1],tags[i][0]))
        except:
            print('erreur liaison livre ',book[1],' avec l etiquette ', tags[i][0])
        db.commit()
    
    return #print('le livre ',book[1],' a été ajouté avec succes à la base de donnée')
