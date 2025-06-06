from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os

app = Flask(__name__)

# 환경 변수에서 시트 이름을 가져옴
SHEET_NAME = os.getenv("GOOGLE_SHEET_NAME", "마비노기 길드원 랭킹")

# 구글 시트 인증
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
credentials = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
gc = gspread.authorize(credentials)
sheet = gc.open(SHEET_NAME).sheet1

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    nickname = data.get('nickname')
    row = data.get('row')

    url = f"https://mabinogimobile.nexon.com/Ranking/Search?searchType=1&keyword={nickname}&worldname=Alissa"
    headers = {"User-Agent": "Mozilla/5.0"}
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')

    characters = soup.select('li.item')
    found = False

    for char in characters:
        name_tag = char.select_one('dd[data-charactername]')
        if name_tag and name_tag['data-charactername'] == nickname:
            job_tag = char.select_one('dl:has(dt:contains("클래스")) dd')
            power_tag = char.select_one('dl:has(dt:contains("전투력")) dd')
            job = job_tag.text.strip() if job_tag else "N/A"
            power = power_tag.text.strip() if power_tag else "N/A"
            sheet.update_cell(row, 2, power)
            sheet.update_cell(row, 3, job)
            found = True
            break

    if not found:
        sheet.update_cell(row, 2, "없음")
        sheet.update_cell(row, 3, "없음")

    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(debug=True)
