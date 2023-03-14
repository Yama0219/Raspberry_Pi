from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome import service as fs
from selenium.webdriver.chrome.options import Options
import csv
import time
import os
import sys
import subprocess


def grade_to_point(grade):
    if grade == "ＡＡ":
        point = 4.0
    elif grade == "Ａ":
        point = 3.0
    elif grade == "Ｂ":
        point = 2.0
    elif grade == "Ｃ":
        point = 1.0
    else:
        point = 0
    return point


class Subject:
    def __init__(self, class_name, teacher_name, credit, grade, year, term):
        self.class_name = class_name
        self.teacher_name = teacher_name
        self.year = int(year)
        self.term = term
        self.credit = float(credit)
        self.grade = grade
        self.point = grade_to_point(grade)

# ある期間のGPA計算
def calc_GPA(datas):
    total_point = 0
    total_credit = 0
    for data in datas:
        total_point += data.point * data.credit
        total_credit += data.credit
    return round(float(total_point) / float(total_credit), 3)

# datasの授業数、単位数、取得単位数、評価の個数を返す
def calc_credit(datas):
    total_credit = 0
    AA_count = 0
    A_count = 0
    B_count = 0
    C_count = 0
    D_count = 0
    E_count = 0
    AA_credit_count = 0
    A_credit_count = 0
    B_credit_count = 0
    C_credit_count = 0
    D_credit_count = 0
    E_credit_count = 0
    class_num = 0
    get_credit = 0

    for data in datas:
        total_credit += data.credit
        class_num += 1
        if data.grade == "ＡＡ":
            AA_count += 1
            AA_credit_count += data.credit
            get_credit += data.credit
        elif data.grade == "Ａ":
            A_count += 1
            A_credit_count += data.credit
            get_credit += data.credit
        elif data.grade == "Ｂ":
            B_count += 1
            B_credit_count += data.credit
            get_credit += data.credit
        elif data.grade == "Ｃ":
            C_count += 1
            C_credit_count += data.credit
            get_credit += data.credit
        elif data.grade == "Ⅾ":
            D_count += 1
            D_credit_count += data.credit
        elif data.grade == "Ｅ":
            E_count += 1
            E_credit_count += data.credit

    return [class_num, total_credit, get_credit, AA_count, A_count, B_count, C_count, D_count, E_count, AA_credit_count, A_credit_count, B_credit_count, C_credit_count, D_credit_count, E_credit_count] 
    
# 期間ごとにdataframeを生成し、CSVに書き込み
def pandas(datas, writer):
    years = set([i.year for i in datas])
    terms = ["前期", "後期", "通年集中"]
    title = ["年度", "期間", "科目数", "総単位数", "取得単位数", "AA/科目数", "A/科目数", "B/科目数", "C/科目数", "D/科目数", "E/科目数","AA/単位数", "A/単位数", "B/単位数", "C/単位数", "D/単位数", "E/単位数", "GPA"]
    writer.writerow(title)
    for year in years:
        for term in terms:    
            datas_limit = [data for data in datas if ((data.year == year) & (term in data.term))]
            if len(datas_limit) != 0:
                credit_data = calc_credit(datas_limit)
                data = [year, term]
                data.extend(credit_data)
                data.append(calc_GPA(datas_limit))          
                writer.writerow(data)

    writer.writerow([])
    credit_data = calc_credit(datas)
    data = ["累積", ""]
    data.extend(credit_data) 
    data.append(calc_GPA(datas))          
    writer.writerow(data)



def main():
    try:
        Path = sys.argv[0]
        Path = Path[:Path.rfind("GPA")]
        f = open(os.path.join(Path, "GPA.csv"), "w", newline = "")
        writer = csv.writer(f)
        login_id = open(os.path.join(Path, "login_id.txt"), "r", encoding='UTF-8')
        login_info = login_id.readlines()
        ID = login_info[0].splitlines()
        PASS = login_info[1].splitlines()
        img_ids = login_info[2].split()

        chrome_option = webdriver.ChromeOptions()
        # Headlessで実行したい場合はheadlessオプションをつける
        chrome_option.add_argument('--headless')
        chrome_option.add_argument('--disable-gpu')
        chrome_option.add_argument('--no-sandbox')
        chrome_option.add_argument('--disable-setuid-sandbox')
        driver = webdriver.Chrome(executable_path=r"/usr/bin/chromedriver", options=chrome_option)
    except Exception as e:
        print(e)
        time.sleep(5)
        sys.exit()


    # ログイン
    try:
        print("accessing SRP")
        driver.get("https://www.srp.tohoku.ac.jp/")
        time.sleep(1)
        try:
            driver.find_element(By.NAME, "twuser").send_keys(ID)
            elem_search_word = driver.find_element(By.NAME, "twpassword")
            elem_search_word.send_keys(PASS)
            elem_search_word.submit()
        except :
            print("j_username")
            driver.find_element(By.NAME, "j_username").send_keys(ID)
            elem_search_word = driver.find_element(By.NAME, "j_password")
            elem_search_word.send_keys(PASS)
            driver.find_element(By.NAME, "_eventId_proceed").click()

        # イメージマトリクス
        try:
            print("trying Image Matrix")
            images = driver.find_elements(By.CLASS_NAME, "input_imgdiv_class")
            for img_id in img_ids:
                for image in images:
                    if img_id in image.get_attribute("style"):
                        image.click()
            driver.find_element(By.ID, "btnLogin").click()
        except:
            print("Image Matrix failed")

        print("accessing Portal Site")
        driver.implicitly_wait(10)
        WebDriverWait(driver, 10).until(EC.title_is, "東北大学ポータルサイト")

        # 学務情報システムにアクセス
        print("accessing Student Affairs Information System")
        elem = driver.find_element(By.PARTIAL_LINK_TEXT, "(Student Affairs Information System)")
        elem.click()

        driver.switch_to.window(driver.window_handles[1])

        WebDriverWait(driver, 10).until(EC.title_is, '学務情報システム')
        time.sleep(5)

        # 成績照会ページにアクセス
        elem = driver.find_element(By.XPATH, "/html/body/div[1]/div[1]/div[6]/ul/li[3]/a")
        elem.click()
        time.sleep(1)
        elem = driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/table/tbody/tr/td[2]/div[1]/div[2]/div[3]/ul[2]/li[2]/a")
        elem.click()
        time.sleep(1)

        # 成績情報を入手
        elements = driver.find_elements(By.CLASS_NAME, "column_odd")

        # データの整理
        datas = []

        GPA_point = 0
        credit = 0

        title = ["分野系列名／科目名", "担当教員", "必修／選択", "単位", "評価", "年度", "期間"]
        writer.writerow(title)

        for ele in elements:
            text = ele.text
            text = text.strip()
            text = text.replace("　","")
            text = text.split()
            if len(text) == 7:
                print(text)
                datas.append(Subject(text[0], text[1], text[3], text[4], text[5], text[6]))
                writer.writerow(text)
                GPA_point += grade_to_point(text[4])*float(text[3])
                credit += float(text[3])
        
        GPA = GPA_point / credit
        GPA = round(GPA, 2)
        print("GPA:{}".format(GPA))

        writer.writerow([])

        # 期間ごとのGPAを書き込み
        pandas(datas, writer)

        print("logging out")
        driver.find_element(By.NAME, "logout").click()
        Alert(driver).accept()
        time.sleep(1)
        driver.find_element(By.ID, "ssoCloseWindow").click()
        time.sleep(1)
        driver.switch_to.window(driver.window_handles[0])
        driver.find_element(By.ID, "logout").click()
        time.sleep(1)


    # 終了
    finally:
        print("driver close")
        driver.close()
        f.close()
        login_id.close()
        print("driver closed")

    subprocess.Popen(["start", os.path.join(Path, "GPA.csv")], shell = True)

if __name__ == "__main__":
    main()