# 여기서 코드로 작성한 것이 실행이 되어서 크롬 브라우저 상에서 동작한다. (chrome driver 버전에 맞게 설치 후 개발환경 내 넣는다.)

# assert "Python" in driver.title
# elem = driver.find_element_by_name("q") -> 특정 요소를 찾을 수 있다.
# elem.clear()
# elem.send_keys("pycon")
# elem.send_keys(Keys.RETURN)
# assert "No results found." not in driver.page_source
# driver.close()

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import urllib.request

driver = webdriver.Chrome() # chromedriver를 가져와서 driver란 변수에 넣는다.
driver.get("https://www.google.co.kr/imghp?hl=ko&ogbl")

elem = driver.find_element_by_name("q")     # 검색창을 찾는 것까지 구현
elem.send_keys("거상 지국천왕")              # 원하는 것이 입력되도록 구현
elem.send_keys(Keys.RETURN)                 # enter 키를 눌러준다.

# # class 명으로 이미지를 클릭하는 것 구현 (가장 첫번째 요소만 클릭하도록 함 [0])
# driver.find_elements_by_css_selector(".rg_i.Q4LuWd")[0].click() 
# # 3초간 기다린다. (이미지 주소를 불러오는 시간을 벌기 위해)
# time.sleep(3)
# # 이미지를 선택하면, 큰 이미지가 나오는데 그 이미지의 src를 받아오는 것 구현
# imgUrl = driver.find_element_by_css_selector(".n3VNCb").get_attribute("src")

# # 이미지 다운로드 방법
# urllib.request.urlretrieve(imgUrl, "test.jpg")

# --------------------- 자동화 ---------------------------
# 스크롤 자동으로 내리는 것 구현
SCROLL_PAUSE_SEC = 1

# 스크롤 높이 가져옴 js 실행하는 code ( 브라우저의 높이를 찾아서 변수에 저장)
last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    # 끝까지 스크롤 다운 (스크롤을 끝까지 내리겠다)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # 1초 대기
    time.sleep(SCROLL_PAUSE_SEC)

    # 스크롤 다운 후 스크롤 높이 다시 가져옴
    new_height = driver.execute_script("return document.body.scrollHeight")

    # 만약 new 와 last 값이 똑같다면, 스크롤이 끝까지 내려간 것이다.
    if new_height == last_height:
        # try를 하다가 없으면 except로 가서 반복문을 빠져나간다. (결과더보기 버튼 없으면 except로!)
        try:
            driver.find_element_by_css_selector(".my4qd").click()
        except:
            break
    last_height = new_height

count = 1
images = driver.find_elements_by_css_selector(".rg_i.Q4LuWd")
for image in images:    # image들(images) 중에서 개별 image를 뽑아서
    try:
        image.click()       # 이미지를 클릭함
        time.sleep(2)       # 2초 있다가 url 찾아서 imgUrl에 넣는다.
        imgUrl = driver.find_element_by_xpath('//*[@id="Sva75c"]/div/div/div[3]/div[2]/c-wiz/div/div[1]/div[1]/div/div[2]/a/img').get_attribute("src")
        # count는 숫자형이기 때문에 문자열로 만들어준다, 그리고 다운받는다
        urllib.request.urlretrieve(imgUrl, str(count) + ".jpg")
        count = count + 1
    except:
        pass

# 브라우저 종료
driver.close()

# google 이미지는 처음에는 50장의 이미지만 가지고있어서 다운을 받으면 50장밖에 못받는다.
# 즉 50장 이상 다운받으려면 스크롤을 내리면서 다운해야한다.