#!/usr/bin/env python
# coding: utf-8

import requests
from bs4 import BeautifulSoup
import io
from os import system

# Acesso o endpoint de notícias do site do Flamengo
host = "https://www.flamengorj.com.br"
MAX_BANNERS_PAGES = 10

responses = []
for i in range(1,MAX_BANNERS_PAGES+1):
    url = host + "/noticias"
    if i > 1:
        url = url + f'/{i}'
    r = requests.get(url)
    
    if r.status_code == 200:
        responses.append(r)
    elif r.status_code == 404:
        break
    


# Pego o conteúdo html recebido
htmls = [] 
for r in responses:
    htmls.append(r.content)


# Pego os banners de notícias dentro dos htmls 
banners = []
for html in htmls:
    bs = BeautifulSoup(html,features='html.parser')
    banners_page = bs.find_all("div",class_="post-grid__item col-12 col-md-6")
    for bpage in banners_page:
        banners.append(bpage)

qtd_noticias = len(banners)
print("Quantidade de notícias capturadas:",qtd_noticias)


# Pego os links para cada notícia capturada
links = []
for bn in banners:
  links.append(bn.find("a")['href'])

print(links)


# Trato cada link deixando-os completos
for i in range(len(links)):
  links[i] = host + links[i]

print(links)


# Crio a função que me ajudará a pegar o conteúdo de cada notícia em passos posteriores
def get_new(new_):
    title = new_.find('h2',class_='post__title').text
    time = new_.find('time').text
    content = new_.find_all('p')

    for i in range(len(content)-1,-1,-1):
        if content[i].text == '' or content[i].find('span') != None or len(content[i].text) <= 20:
            del content[i]
        else:
            content[i] = str(content[i].text)
    
    return {'title':title,'content':content,'time':time}


# Crio a função responsável por capturar cada uma das notícias via links passados
def get_all_news(links):
    news = []
    for link in links:
        r = BeautifulSoup(requests.get(link).content,features='html.parser')
        new_ = r.find('div',class_='card__content')
        post = get_new(new_)
        news.append(post)
    return news


# Utilizo as funções acima definidas para fazer o scrapping do conteúdo de cada uma das notícias

all_news = get_all_news(links)
print(all_news)


# Crio a função que salva todas as notícias em arquivos .txt na minha máquina
def save_news(all_news):
    system("mkdir crawled_news")
    for n in all_news:
       with  io.open('crawled_news/' + str(id(n)) + '.txt' , 'w',encoding='utf-8')  as file:
        file.write('[TITLE] >> ' + n['title'] + '\n')
        file.write('[TIME] >> ' + n['time'] + '\n')
        file.write('[CONTENT]\n')
        for p in n['content']:
            file.write('[PARAGRAPH]\n')
            file.write(p + '\n')


# Uso a função definida acima para salvar as notícias crawleadas
save_news(all_news)
