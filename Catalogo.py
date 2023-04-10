# coding=utf-8
import urllib.request, json, brotli, time
import pandas as pd




def getGenres(url):
    req = urllib.request.Request(url)
    req.add_header("Host", "www.filmin.es")
    req.add_header("User-Agent",
                   "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18362")
    req.add_header("Accept", "application/json, text/plain, */*")
    req.add_header("Accept-Language", "en-US,en;q=0.5")
    req.add_header("Accept-Encoding", "gzip, deflate, br")
    req.add_header("X-CSRF-TOKEN", "uVCgCcSg3jNMtFM8GdWCm48HbC7SgEKYZul1Nf7g")
    req.add_header("X-Requested-With", "XMLHttpRequest")
    req.add_header("X-XSRF-TOKEN", "uVCgCcSg3jNMtFM8GdWCm48HbC7SgEKYZul1Nf7g")
    req.add_header("Alt-Used", "www.filmin.es")
    req.add_header("Connection", "keep-alive")
    req.add_header("Referer", "https://www.filmin.es/catalogo")
    req.add_header("Cookie",
                   "cookieyesID=eWFJUFp6N01ldU9YNVo4QzNkenZJd3pjQlNEOExWMXE=; cky-consent=yes; cookieyes-necessary=yes; cookieyes-functional=no; cookieyes-analytics=no; cookieyes-performance=no; cookieyes-advertisement=no; cookieyes-other=no; cky-action=yes; XSRF-TOKEN=uVCgCcSg3jNMtFM8GdWCm48HbC7SgEKYZul1Nf7g; filmin_session=vFMoCwprp0hN3wf7wfS1meRMaO6DsLjuMbgRv7aC; __cf_bm=PnWNdtlfr5ZyLxr1CTGCgz32R7SrqpkK97kVvFrjggk-1680597662-0-AbkwX8B/4T+Xifuof2R7MnWVgBz2n2nX8IPbBYu8Z89/YC/UlPJY27kFw+GXdwx8cCKPngTuwQGPtNRcsTdgZSY=")
    req.add_header("Sec-Fetch-Dest", "empty")
    req.add_header("Sec-Fetch-Mode", "cors")
    req.add_header("Sec-Fetch-Site", "same-origin")
    req.add_header("TE", "trailers")

    response = urllib.request.urlopen(req)
    decompressed = brotli.decompress(response.read())
    datos_json = json.loads(decompressed)
    print("Downloading catalog")
    return datos_json

def getUrls(URL):
    page = 23
    has_more_data = True
    listaSlug = list()
    listaType = list()
    listaCompleta = pd.DataFrame(['slug', 'type'])
    while has_more_data:
        rsp = getGenres(f"https://www.filmin.es/wapi/catalog/browse?rights=svod&page={page}&limit=500")
        lista = rsp['data']
        if not lista:
            has_more_data = False
        else:
            for content in lista:
                slug = content['slug']
                type = content['type']
                listaSlug.append(slug)
                if type == "pelicula": ## Se cambia a film porque en www.filmin.es/wapi/medias/ cambia de pelicula a film
                    type = "film"
                listaType.append(type)
        page += 1
    time.sleep(2)
    listaCompleta = pd.DataFrame(list(zip(listaSlug, listaType)), columns=['slug', 'type'])
    print("Downloading slug and type for urls")
    return listaCompleta

def getData(url):
    req = urllib.request.Request(url)
    req.add_header("Host", "www.filmin.es")
    req.add_header("User-Agent",
                   "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18362")
    req.add_header("Accept", "application/json, text/plain, */*")
    req.add_header("Accept-Language", "en-US,en;q=0.5")
    req.add_header("Accept-Encoding", "gzip, deflate, br")
    req.add_header("X-CSRF-TOKEN", "uVCgCcSg3jNMtFM8GdWCm48HbC7SgEKYZul1Nf7g")
    req.add_header("X-Requested-With", "XMLHttpRequest")
    req.add_header("X-XSRF-TOKEN", "uVCgCcSg3jNMtFM8GdWCm48HbC7SgEKYZul1Nf7g")
    req.add_header("Alt-Used", "www.filmin.es")
    req.add_header("Connection", "keep-alive")
    req.add_header("Referer", "https://www.filmin.es/catalogo")
    req.add_header("Cookie",
                   "cookieyesID=eWFJUFp6N01ldU9YNVo4QzNkenZJd3pjQlNEOExWMXE=; cky-consent=yes; cookieyes-necessary=yes; cookieyes-functional=no; cookieyes-analytics=no; cookieyes-performance=no; cookieyes-advertisement=no; cookieyes-other=no; cky-action=yes; XSRF-TOKEN=uVCgCcSg3jNMtFM8GdWCm48HbC7SgEKYZul1Nf7g; filmin_session=vFMoCwprp0hN3wf7wfS1meRMaO6DsLjuMbgRv7aC; __cf_bm=PnWNdtlfr5ZyLxr1CTGCgz32R7SrqpkK97kVvFrjggk-1680597662-0-AbkwX8B/4T+Xifuof2R7MnWVgBz2n2nX8IPbBYu8Z89/YC/UlPJY27kFw+GXdwx8cCKPngTuwQGPtNRcsTdgZSY=")
    req.add_header("Sec-Fetch-Dest", "empty")
    req.add_header("Sec-Fetch-Mode", "cors")
    req.add_header("Sec-Fetch-Site", "same-origin")
    req.add_header("TE", "trailers")

    response = urllib.request.urlopen(req)
    decompressed = brotli.decompress(response.read())
    datos_json = json.loads(decompressed)
    return datos_json


def getCsv(URL):
    listaCatalogo = getUrls(URL)
    listaTitle = list()
    listaType = list()
    listaYear = list()
    listaActors = list()
    listaLanguage = list()
    listaSubtitles = list()
    for i in range(len(listaCatalogo)):
        slug = listaCatalogo.iloc[i]['slug']
        type = listaCatalogo.iloc[i]['type']
        datos_JSON = getData(f"https://www.filmin.es/wapi/medias/{type}/{slug}")
        data = datos_JSON['data']
        title = data['title']
        type = data['type']
        year = data['year']
        actor = data['actors']
        actorList = list()
        for i in actor:
            actorList.append(i['full_name'])
        languageList = list()
        language = data['versions'][0]['language_audios']
        for j in language:
            languageList.append(j['name'])
        subtitlesList = list()
        subtitles = data['versions'][0]['language_subtitles']
        for k in subtitles:
            subtitlesList.append(k['name'])
        listaTitle.append(title)
        listaType.append(type)
        listaYear.append(year)
        listaActors.append(actorList)
        listaLanguage.append(languageList)
        listaSubtitles.append(subtitlesList)
    listaCompleta = pd.DataFrame(list(zip(listaTitle, listaType, listaYear, listaActors, listaLanguage, listaSubtitles)), columns=['Title', 'Type', 'year', 'actors_info', 'language', 'subtitles'])
    return listaCompleta.to_csv('dataset.csv')


getCsv("https://www.filmin.es/catalgo")
