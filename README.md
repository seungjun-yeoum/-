# 마비노기 모바일 랭킹 크롤러 (Flask)

## 기능
- 구글 시트에 닉네임이 입력되면 웹훅 호출
- 해당 닉네임의 전투력과 직업을 마비노기 모바일 랭킹 사이트에서 가져와 시트에 업데이트

## 사용 방법

### 1. 패키지 설치
```
pip install -r requirements.txt
```

### 2. 환경 변수 설정
`.env` 파일에 아래 내용 포함
```
GOOGLE_SHEET_NAME=마비노기 길드원 랭킹
```

### 3. 서버 실행
```
python main.py
```

### 4. Render 배포
- 이 코드를 GitHub에 업로드하고 Render로 웹서버 생성
- 환경 변수 설정: `GOOGLE_SHEET_NAME` = 마비노기 길드원 랭킹

## Webhook URL
- `/webhook` 로 POST 요청
- body 예시:
```json
{
  "nickname": "휘짱",
  "row": 2
}
```
