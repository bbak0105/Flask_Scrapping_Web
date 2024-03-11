# 플라스크와 크롤링(스크래퍼)를 활용한 웹사이트 제작

## 📌 Preivew

![KakaoTalk_Photo_2024-03-10-23-20-33 001](https://github.com/bbak0105/Flask_Scrapping_Web/assets/66405572/430e57aa-55b5-45f4-88c1-d24173578013)

![KakaoTalk_Photo_2024-03-10-23-20-34 002](https://github.com/bbak0105/Flask_Scrapping_Web/assets/66405572/36e2233a-76b4-4878-af83-f5a87939f4cd)

![KakaoTalk_Photo_2024-03-10-23-20-38](https://github.com/bbak0105/Flask_Scrapping_Web/assets/66405572/b2fe3359-360c-4980-8070-84110262517a)

<br/>

## 📌 Skills
### Language
<a><img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white"/></a>
<a><img src="https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=JavaScript&logoColor=white"/></a>

### Framework
<a><img src="https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white"/></a>

### IDE
<a><img src="https://img.shields.io/badge/PyCharm-000000.svg?&style=for-the-badge&logo=PyCharm&logoColor=white"/></a>

### Skills
<a><img src="https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white"/><a>
<a><img src="https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white"/></a>
<a><img src="https://img.shields.io/badge/CSS-239120?&style=for-the-badge&logo=css3&logoColor=white"/></a>
<a><img src="https://img.shields.io/badge/BeautifulSoup-ffffff?&style=for-the-badge&logoColor=black"/></a>
<a><img src="https://img.shields.io/badge/Konlpy-3366FF?&style=for-the-badge&logoColor=black"/></a>

### Deploy
<a><img src="https://img.shields.io/badge/Amazon_AWS-232F3E?style=for-the-badge&logo=amazon-aws&logoColor=white"/></a>

<br/>

<br/>

## 📌 Backend Descriptions
### `Crawler`
> ✏️ 네이버 검색창처럼 사용자에게 검색을 받고, 원하는 개수 만큼 '네이버 뉴스'의 내용을 BeautifulSoup을 사용하여 스크랩합니다. <br/>
> 1페이지당 10개씩이기 때문에, 91개로 설정시에 총 10페이지를 긁어 오게 됩니다. <br/>
> 양이 많아질 수록 대기 시간이 오래 걸립니다. <br/>
> 1. request 라이브러리를 사용하여 사용자가 form 태그(프론트)에서 검색한 키워드를 가져옵니다. 
> 2. contents_cleansing(contents=내용들) : 스크랩 된 내용을 정제화 해주는 함수 입니다.
> 3. crawler(maxNum=최대개수설정, query=사용자가검색한키워드쿼리, sort=정렬, s_date=시작날짜, e_date=종료날짜) 

<br/>

```python
import urllib.request

inputKeyword = request.args.get('keyword', default="알바트로스", type = str)
keyword = urllib.parse.quote(inputKeyword)
...

# 내용 정제화 함수
def contents_cleansing(contents):
    first_cleansing_contents = re.sub('<dl>.*?</a> </div> </dd> <dd>', '', str(contents)).strip()  # 앞에 필요없는 부분 제거
    second_cleansing_contents = re.sub('<ul class="relation_lst">.*?</dd>', '', first_cleansing_contents).strip()  # 뒤에 필요없는 부분 제거 
    third_cleansing_contents = re.sub('<.+?>', '', second_cleansing_contents).strip()
    contents_text.append(third_cleansing_contents)

# 크롤러 함수
def crawler(maxNum, query, sort, s_date, e_date):
    s_from = s_date.replace(".", "")
    e_to = e_date.replace(".", "")
    page = 1
    maxNum_t = (int(maxNum) - 1) * 10 + 1  # 11= 2페이지 21=3페이지 31=4페이지  ...81=9페이지 , 91=10페이지, 101=11페이지

    while page <= maxNum_t:
        url = "https://search.naver.com/search.naver?where=news&query=" + query + "&sort=" + sort + "&ds=" + s_date + "&de=" + e_date + "&nso=so%3Ar%2Cp%3Afrom" + s_from + "to" + e_to + "%2Ca%3A&start=" + str(page)

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

crawler("100", keyword, "0", "datetime.datetime.now()", "20220430" )
...
```
---

### `Data-To-DataFrame`
> 크롤러를 통해 긁어온 정보들을 토대로 데이터프레임을 생성합니다. <br/>
> date(날짜), title(제목), press(언론사), contents(내용), link(하이퍼링크)로 구성된 프레임으로 생성하였습니다.

<br/>

```python
col_name = ["date", "title", "press", "contents", "link"]
rows = maxNum * 10
target_articles = pd.DataFrame(np.reshape(df1, (rows, 5)), columns=col_name).T.to_dict()
```

---

### `Konlpy Analysis`
> konlpy를 활용하여 형태소 분석을 진행합니다. <br/>
> 형태소 분석이 끝나면, 워드클라우드와 데이터시각화 데이터를 넣어 render_template context에 넣어 함께 리턴합니다.

<br/>

```python
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
plt.rc('font', family='malgun')
plt.rcParams['axes.unicode_minus'] = False

plt.bar(df['keyword'],df['count'])
plt.ylabel("Count")
plt.xticks(rotation=90)

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

return render_template("naver.html", context=target_articles)
```

<br/>

## 📌 Frontend Descriptions
### `Search-Box`
> 사용자에게 검색어를 입력받는 form 입니다. <br/>
> get 방식으로 플라스크 서버에 보내지고 메인 사이트로 이동합니다.

<br/>

```javaScript
...
<div class="container">
   ...
   <form role="search" action="{{url_for('naver')}}" method="get">
        <div class="input-group mb-3">
            <input
                type="text"
                class="form-control"
                id="keyword"
                name="keyword"
                placeholder="검색어를 입력하세요"
                aria-label="Recipient's username"
                aria-describedby="button-addon2"
            >
            <button type="submit" class="btn btn-outline-info" onclick="handleOnClick()">
                Search
            </button>
        </div>
    </form>

    <!-- Loading -->
    <div class="text-center" id="spinner" style="display:none;">
        <div class="spinner-grow text-info" role="status" style="width: 3rem; height: 3rem;">
          <span class="visually-hidden">Loading...</span>
        </div>
    </div>
</div>

<script type="text/javascript">
    function handleOnClick() {
      let element = document.getElementById("spinner");
      element.style.display = "block";
    }
</script>
```

---

### `Mainboard`
> 상단에는 백엔드 서버에서 검색어를 바탕으로 생성한 플로우 차트, 워드클라우드를 보여줍니다. <br/>
> 하단에는 크롤링한 데이터를 for문을 사용하여 보여줍니다.

<br/>

```javaScript
...
<div class = "container">
    ...
    <!-- [2]. Card -->
    <div class="d-flex justify-content-center">
        <div class="card-group" style="margin:0;auto;">
            <!-- WordCloud 담는곳 -->
            <div class="card border-info mb-3" style="max-width: 18rem;">
              <div class="card-header bg-transparent border-info"><b>☁ Word Cloud</b></div>
              <div class="card-body">
                  {% if context %}
                    <img src={{context['cloud']}} width="100%">
                  {% endif %}
              </div>
            </div>
            ...
        </div>
    </div>
</div>
...

<div class = "container">
    <table class="table">
      <thead>
        <tr>
          <th scope="col">💙</th>
          <th scope="col">TITLE</th>
          <th scope="col">CLICK</th>
        </tr>
      </thead>
      <tbody>
      {% if context %}
        {% for key, item in context.items() %}
        <tr>
          <th scope="row">{{ key }}</th>
          <td>{{ item['title'] }}</td>
          <td><a href={{item['link']}}> 원문보기 </a> </td>
        </tr>
         {% endfor %}
      {% endif %}
      </tbody>
    </table>
</div>
```
