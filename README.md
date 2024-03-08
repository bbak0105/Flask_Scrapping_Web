# 플라스크와 크롤링(스크래퍼)를 활용한 웹사이트 제작

<br/>

## 📌 Skills
### Language
<a><img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white"/></a>
<a><img src="https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=JavaScript&logoColor=white"/></a>

### Framework
<a><img src="https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white"/></a>

### IDE
<a><img src="https://img.shields.io/badge/PyCharm-000000.svg?&style=for-the-badge&logo=PyCharm&logoColor=white"/></a>
<a><img src="https://img.shields.io/badge/Visual_Studio_Code-0078D4?style=for-the-badge&logo=visual%20studio%20code&logoColor=white"/></a>

### Skills
<a><img src="https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white"/><a>
<a><img src="https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white"/></a>
<a><img src="https://img.shields.io/badge/CSS-239120?&style=for-the-badge&logo=css3&logoColor=white"/></a>
<a><img src="https://img.shields.io/badge/BeautifulSoup-ffffff?&style=for-the-badge&logoColor=black"/></a>
<a><img src="https://img.shields.io/badge/Konlpy-3366FF?&style=for-the-badge&logoColor=black"/></a>
<br/>

<br/>

## 📌 Backend Descriptions
### `Search-Box`
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

## 📌 Frontend Descriptions

---

