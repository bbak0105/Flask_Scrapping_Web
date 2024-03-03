from flask import Flask, render_template, request

import pandas as pd
import numpy as np
from datetime import datetime
import re
import requests as req
from bs4 import BeautifulSoup
from konlpy.tag import Okt
import nltk
nltk.download('stopwords')
import pandas as pd
import datetime

app = Flask(__name__)

#gloabal variable
target_articles = {}

@app.route('/')
def index():
    return render_template("index.html", context=target_articles)

@app.route('/naver')
def naver():
    import urllib.request

    inputKeyword = request.args.get('keyword', default="알바트로스", type = str)
    keyword = urllib.parse.quote(inputKeyword)

    title_text = []
    link_text = []
    source_text = []
    date_text = []
    contents_text = []
    df1 = []

    # 날짜 정제화 함수
    def date_cleansing(test):
        try:
            # 지난 뉴스
            pattern = '\d+.(\d+).(\d+).'  # 정규표현식

            r = re.compile(pattern)
            match = r.search(test).group(0)
            date_text.append(match)

        except AttributeError:
            # 최근 뉴스
            pattern = '\w* (\d\w*)'  # 정규표현식

            r = re.compile(pattern)
            match = r.search(test).group(1)
            date_text.append(match)

    # 내용 정제화 함수
    def contents_cleansing(contents):
        first_cleansing_contents = re.sub('<dl>.*?</a> </div> </dd> <dd>', '',
                                          str(contents)).strip()  # 앞에 필요없는 부분 제거
        second_cleansing_contents = re.sub('<ul class="relation_lst">.*?</dd>', '',
                                           first_cleansing_contents).strip()  # 뒤에 필요없는 부분 제거 (새끼 기사)
        third_cleansing_contents = re.sub('<.+?>', '', second_cleansing_contents).strip()
        contents_text.append(third_cleansing_contents)

    def crawler(maxpage, query, sort, s_date, e_date):

        s_from = s_date.replace(".", "")
        e_to = e_date.replace(".", "")
        page = 1
        maxpage_t = (int(maxpage) - 1) * 10 + 1  # 11= 2페이지 21=3페이지 31=4페이지  ...81=9페이지 , 91=10페이지, 101=11페이지

        while page <= maxpage_t:
            url = "https://search.naver.com/search.naver?where=news&query=" + query + "&sort=" + sort + "&ds=" + s_date + "&de=" + e_date + "&nso=so%3Ar%2Cp%3Afrom" + s_from + "to" + e_to + "%2Ca%3A&start=" + str(
                page)

            response = req.get(url)
            html = response.text

            # 뷰티풀소프의 인자값 지정
            soup = BeautifulSoup(html, 'html.parser')

            # <a>태그에서 제목과 링크주소 추출
            atags = soup.select('.news_tit')
            for atag in atags:
                title_text.append(atag.text)  # 제목
                link_text.append(atag['href'])  # 링크주소

            # 신문사 추출
            source_lists = soup.select('.info_group > .press')
            for source_list in source_lists:
                source_text.append(source_list.text)  # 신문사

            # 날짜 추출
            date_lists = soup.select('.info_group > span.info')
            for date_list in date_lists:
                # 1면 3단 같은 위치 제거
                if date_list.text.find("면") == -1:
                    date_text.append(date_list.text)

            # 본문요약본
            contents_lists = soup.select('.news_dsc')
            for contents_list in contents_lists:
                contents_cleansing(contents_list)  # 본문요약 정제화

            # 모든 리스트 딕셔너리형태로 저장
            result = {"date": date_text, "title": title_text, "press": source_text, "contents": contents_text,
                      "link": link_text}

            df = pd.DataFrame(result)
            page += 10

        df1.append(df)

        # 새로 만들 파일이름 지정
        filename = datetime.datetime.now().strftime('%Y%m%d-%H') + ".csv"
        df.to_csv(filename, encoding='utf-8-sig')

    def main():
        crawler("100", keyword, "0", "datetime.datetime.now()", "20220430" )

    main()

    col_name = ["date", "title", "press", "contents", "link"]
    target_articles = pd.DataFrame(np.reshape(df1, (1000, 5)), columns=col_name).T.to_dict()

    from konlpy.tag import Kkma
    from collections import Counter
    from wordcloud import WordCloud

    filename = datetime.datetime.now().strftime('%Y%m%d-%H') + ".csv"
    df = pd.read_csv(filename)
    content_origin = df['contents']
    content = list(content_origin)
    content_list = [str(item) for item in content if isinstance(item, str)]
    ana_text = " ".join(content_list)

    # 형태소 분석
    # https://konlpy.org/en/latest/api/konlpy.tag/#mecab-class
    okt = Okt()
    df_noun = okt.nouns(ana_text)
    noun_list = [n for n in df_noun if len(n) > 1]  # 한글자 단어 삭제

    # 명사들을 카운팅 해보자
    counts = Counter(noun_list)

    # 가장 많이 나온 단어부터 30개만 가져오자
    target_words = counts.most_common(30)

    # window : r"C:\Windows\Fonts\malgun.ttf"
    wc = WordCloud(font_path="malgun",
                   background_color="white",
                   max_font_size=60)

    cloud = wc.generate_from_frequencies(dict(target_words))
    cloud_filename = './static/images/'+ inputKeyword.replace(" ","") + '_wc.jpg'
    cloud.to_file(cloud_filename)

    board_info = {
        'card_title': "오늘 뉴스기사 크롤링",
        'card_desc': f"가장 높은 카운팅 키워드는 {target_words[0]} 입니다.",
        'card_date': datetime.datetime.now().strftime('%Y-%m-%d')
    }

    ## Graph 파일 만들기
    df = pd.DataFrame(data=target_words, columns=['keyword', 'count'])

    import matplotlib.pyplot as plt
    import seaborn as sns
    plt.switch_backend('Agg')

    ## 한글폰트 설정
    # plt.rc('font', family='malgun')
    # plt.rcParams['axes.unicode_minus'] = False

    # plt.bar(df['keyword'],df['count'])
    # plt.ylabel("Count")
    # plt.xticks(rotation=90)

    plt.rcParams['axes.unicode_minus'] = False
    plt.rcParams['figure.figsize'] = (10, 8)
    plt.rc('font', family='Gulim')
    ax = sns.barplot(x=df['count'], y=df['keyword'])

    for p in ax.patches:
        ax.text(p.get_x() + p.get_width(),
                p.get_y() + p.get_height(),
                f"{p.get_width():.0f}" + '건',
                ha='left')

    plt_filename = './static/images/'+ inputKeyword.replace(" ","") + '_chart.png'
    plt.title("Comparing wordcount")
    plt.savefig(plt_filename)

    # target_articles에 마지막 혹은 컬럼에 plt 넣고 plt_filename 보내주기
    # target_articles에 마지막 혹은 컬럼에 cloud 넣기 cloud_filename 보내주기
    target_articles['plt'] = plt_filename
    target_articles['cloud'] = cloud_filename

    print(target_articles)

    return render_template("naver.html", context=target_articles)

if __name__ == '__main__':
    app.run(host='0.0.0.0')