from flask import Flask, render_template, request, redirect, url_for
from bs4 import BeautifulSoup
import requests as re

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        anime_title = request.form['anime_title']
        data = re.get('https://otakudesu.video/', params={'s': {anime_title}, 'post_type': 'anime'}).text
        soup = BeautifulSoup(data, 'lxml')
        anime = soup.find('ul', class_='chivsrc')
        anime_link = anime.li.h2.a['href']
        anime_info = re.get(anime_link).text
        soup2 = BeautifulSoup(anime_info, 'lxml')
        anime_ilist = soup2.find('div', class_='venser').find('div', class_='fotoanime').find('div', class_='infozin').find('div', class_='infozingle').find_all('p')
        img = soup2.find('div', class_='venser').find('div', class_='fotoanime').find('img')['src']
        anime_list = soup2.find('div', class_='episodelist')
        anime_bdlink = anime_list.ul.li.span.a['href']
        anime_binfo = re.get(anime_bdlink).text
        soup3 = BeautifulSoup(anime_binfo, 'lxml')
        batch = soup3.find('div', class_='batchlink')
        batch_link360p = batch.ul.li.a['href']
        batch_size360p = batch.ul.li.i.text
        batch_link480p = batch.find('ul').find_all('li')[1].find('a')['href']
        batch_size480p = batch.find('ul').find_all('li')[1].find('i').text
        batch_link720p = batch.find('ul').find_all('li')[2].find('a')['href']
        batch_size720p = batch.find('ul').find_all('li')[2].find('i').text
        return result(batch_link360p, batch_size360p, anime_ilist, img, batch_link480p, batch_size480p, batch_link720p, batch_size720p)
    else:
        return render_template('index.html')

@app.route('/result')
def result(batch360p, batchsize360p, anime_infos, img, batch480p, batchsize480p, batch720p, batchsize720p):
    return render_template('result.html', batch360p=batch360p, batchsize360p=batchsize360p, animfo=anime_infos, img=img, b480p=batch480p, bs480p=batchsize480p, b720p=batch720p, bs720p=batchsize720p)