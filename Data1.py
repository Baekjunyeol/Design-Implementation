from flask import Flask, request, jsonify
from flask_cors import CORS  # CORS 지원을 위한 라이브러리
import sqlite3

app = Flask(__name__)
CORS(app)  # CORS 문제를 해결

# 데이터베이스 연결 및 테이블 생성
def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS orders (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        phone TEXT NOT NULL,
                        address TEXT NOT NULL,
                        payment_method TEXT NOT NULL,
                        product TEXT NOT NULL,
                        quantity INTEGER NOT NULL)''')
    conn.commit()
    conn.close()

@app.route('/save_customer', methods=['POST'])
def save_customer():
    try:
        # 클라이언트로부터 JSON 데이터를 받음
        form_data = request.get_json()

        이름 = form_data.get('이름')
        전화번호 = form_data.get('전화번호')
        배송지 = form_data.get('배송지')
        결제수단 = form_data.get('결제수단')
        상품 = form_data.get('상품')
        수량 = form_data.get('수량')

        # 데이터베이스에 저장하는 부분
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO orders (name, phone, address, payment_method, product, quantity) 
                          VALUES (?, ?, ?, ?, ?, ?)''', 
                       (이름, 전화번호, 배송지, 결제수단, 상품, 수량))
        conn.commit()
        conn.close()

        # 성공적으로 처리되었음을 클라이언트에게 응답
        return jsonify({"message": "주문이 성공적으로 완료되었습니다!"}), 200

    except Exception as e:
        print("Error:", e)
        return jsonify({"message": "서버 오류가 발생했습니다. 다시 시도해주세요."}), 500

if __name__ == '__main__':
    init_db()  # 서버 시작 시 데이터베이스 테이블 초기화
    app.run(debug=True)
