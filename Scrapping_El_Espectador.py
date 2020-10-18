# Web Scrapping del periodico El Espectador de Colombia
# Autor: Juan Camilo Alfonso Mesquida
# Fecha: 17/10/2020


import requests
import os
import pandas as pd
from bs4 import BeautifulSoup
from datetime import date


def _main(url):
    print('-' * 50)  
    print('Inicio ejecución')  
    news = _get_news(url)
    notes_df = _get_notes(news)
    _save_data(notes_df)


def _get_news(url):
    print(f'Obteniendo información de {url}')

    try:
        newspaper_page = requests.get(url)

        if newspaper_page.status_code == 200:
            s = BeautifulSoup(newspaper_page.text, 'lxml')
            news = s.find_all('div', attrs = {'class': 'Card-title card-title h5'})
            print(f'Se obtuvieron {len(news)} noticias')

            return news
        else:
            print(f'Error obteniendo noticias de: {url}')
            print(f'Status code = {newspaper_page.status_code}')

            return None

    except Exception as e:
        print(f'Error al tratar de obtener información de {url} de tipo: {e}')

        return None
    

def _get_notes(news):
    notes_df = pd.DataFrame(columns=['Título', 'Autor', 'Cuerpo', 'Link'])

    for idx, note in enumerate(news):
        print(f'Obteniendo información de la  noticia {idx+1}')
        note_link, note_title = _get_note_info(note)
        note_author, note_body = _scrape_note(note_link)
        notes_df = notes_df.append({'Título': note_title, 'Autor': note_author, 'Cuerpo': note_body, 'Link': note_link}, ignore_index=True)      

    return notes_df                         


def _get_note_info(note):

    try:
        note_link = '{0}{1}'.format(url.replace('.com/', '.com'), note.a.get('href'))
        note_title = note.a.get_text()   

    except Exception as e:
        print(f'Error al tratar de obtener el link y el título de la noticia: {e}')
        note_link = None
        note_title = None
    
    finally:
        return note_link, note_title


def _scrape_note(note_link):

    try:
        note_content = requests.get(note_link)
        s_note = BeautifulSoup(note_content.text, 'lxml')
        author = s_note.find('span', attrs = {'class': 'Article-Author'})
        note_author = author.get_text().replace('Por: ', '')
        body = s_note.find('div', attrs = {'class': 'Article-Content'})
        note_body = body.get_text()  

    except Exception as e:
        print(f'Error al tratar de obtener información de la noticia: {e}')
        note_author = None
        note_body = None
    
    finally:
        return note_author, note_body


def _save_data(notes_df):
    
    try:
        export_path = f'Noticias_El_Espectador_{date.today()}.csv'
        print('Descargando información en la ruta: {0}\\{1}'.format(os.getcwd(), export_path))
        notes_df.to_csv(r'{0}'.format(export_path), encoding='utf-8-sig', sep = ';')

    except  Exception as e:
        print(f'Error al tratar de guardar la información: {e}')


if __name__ == "__main__":

    url = 'https://www.elespectador.com/'
    _main(url)