# coding: utf-8

import os
import json
import requests
from bs4 import BeautifulSoup

base_url = "http://music.163.com"
start_url = base_url + "/artist/album?id={}&limit=100"  # 根据歌手的id，抓取其专辑列表
song_url = base_url + "/api/song/lyric?id={}&lv=1&kv=1&tv=-1"  # 根据歌曲的id，抓取歌词

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
    "Referer": "http://music.163.com",
    "Host": "music.163.com"
}


def get_html(url):  # requests抓取
    resp = requests.get(url, headers=headers)
    html = str(resp.content, encoding='utf-8', errors='ignore')
    return html


def crawl_lyrics(art_id):
    """抓取一整个歌手的所有歌词"""
    html = get_html(start_url.format(art_id))  # 先抓该歌手的专辑列表
    soup = BeautifulSoup(html, 'lxml')

    artist = soup.find('h2', id='artist-name').text.strip().replace(' ', '_')
    artist_dir = 'data/' + artist
    if not os.path.exists(artist_dir):  # 歌手目录
        os.mkdir(artist_dir)
    print("歌手名：", artist)

    albums = soup.find('ul', class_='m-cvrlst').find_all('a', class_='msk')  # 专辑列表
    for album in albums:
        html = get_html(base_url + album.get('href'))  # 再抓取该专辑下歌曲列表
        soup = BeautifulSoup(html, 'lxml')

        album_title = soup.find('h2', class_='f-ff2').text.strip().replace(' ', '_').replace('/', '_')  # '/'会影响目录
        album_dir = os.path.join(artist_dir, album_title)
        if not os.path.exists(album_dir):  # 专辑目录
            os.mkdir(album_dir)
        print("  " + artist + "---" + album_title)

        links = soup.find('ul', class_='f-hide').find_all('a')  # 歌曲列表
        for link in links:
            song_name = link.text.strip().replace(' ', '_').replace('/', '_')
            song_id = link.get('href').split('=')[1]
            html = get_html(song_url.format(song_id))  # 抓取歌词

            try:  # 存在无歌词的歌曲，直接忽略
                lyric_json = json.loads(html)
                lyric_text = lyric_json['lrc']['lyric']

                open(os.path.join(album_dir, song_name + '.txt'), 'w', encoding='utf-8').write(lyric_text)
                print("    " + song_name + ", URL: " + song_url.format(song_id))
            except:
                print("    " + song_name + ": 无歌词, URL: " + song_url.format(song_id))
        print()


def find_artist_ids():
    """只能拿到前100位的歌手ID"""
    url = 'http://music.163.com/api/artist/top?limit=100&offset=0'
    html = get_html(url)
    artists = json.loads(html)['artists']
    with open('artists.txt', 'w', encoding='utf-8', errors='ignore') as fa:
        for artist in artists:
            artist_name = artist['name'].strip().replace(" ", "_")
            fa.write(artist_name + ' ' + str(artist['id']) + '\n')


if __name__ == '__main__':
    with open('artists.txt', 'r', encoding='utf-8') as f:
        for line in f:
            art_id = line.strip().split()[1]
            crawl_lyrics(art_id)
