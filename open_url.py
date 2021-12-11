import webbrowser

def open_page(search):
    words=search.split(" ")
    url="https://music.163.com/#/search/m/?id=1880886636&s="
    for word in words:
        url=url + word + "%20"
    webbrowser.open(url)
open_page(input())
