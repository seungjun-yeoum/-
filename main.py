from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os

app = Flask(__name__)

# 환경 변수에서 시트 이름을 가져옴
SHEET_NAME = os.getenv("GOOGLE_SHEET_NAME", "마비노기 랭킹")

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

characters = soup.select("ul.ranking_list > li")  # ← 수정 포인트

for char in characters:
    name_tag = char.select_one("dd.data-charactername")
    if name_tag and name_tag.text.strip() == nickname:
        job, power = "없음", "없음"
        dts = char.select("dt")
        dds = char.select("dd")

        for i, dt in enumerate(dts):
            dt_text = dt.get_text(strip=True)
            if dt_text == "전투력":
                power = dds[i].get_text(strip=True)
            elif dt_text == "클래스":
                job = dds[i].get_text(strip=True)

        sheet.update_cell(row, 2, power)
        sheet.update_cell(row, 3, job)
        break


    if not found:
        sheet.update_cell(row, 2, "없음")
        sheet.update_cell(row, 3, "없음")

    return jsonify({"status": "ok"})  # ✅ 들여쓰기 되어 있어야 함
if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
