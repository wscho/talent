import sqlite3
import pandas as pd

DB_FILE = "talent_matching.db"

def get_connection():
    """SQLite 데이터베이스 연결"""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row  # 딕셔너리 형태로 결과 반환
    return conn

def init_database():
    """데이터베이스 초기화 및 테이블 생성"""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Donors 테이블 생성
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Donors (
            donor_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            skill TEXT NOT NULL,
            mode TEXT NOT NULL,
            availability TEXT,
            created_at TEXT NOT NULL
        )
    """)
    
    # Requests 테이블 생성
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Requests (
            request_id TEXT PRIMARY KEY,
            email TEXT NOT NULL,
            needed_skill TEXT NOT NULL,
            description TEXT,
            status TEXT NOT NULL DEFAULT '대기',
            created_at TEXT NOT NULL
        )
    """)
    
    # Matches 테이블 생성
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Matches (
            match_id TEXT PRIMARY KEY,
            donor_id TEXT NOT NULL,
            request_id TEXT NOT NULL,
            score INTEGER NOT NULL,
            status TEXT NOT NULL DEFAULT '대기',
            created_at TEXT NOT NULL,
            FOREIGN KEY (donor_id) REFERENCES Donors(donor_id),
            FOREIGN KEY (request_id) REFERENCES Requests(request_id)
        )
    """)
    
    conn.commit()
    conn.close()

def load_table(table_name):
    """테이블 데이터를 DataFrame으로 로드"""
    conn = get_connection()
    df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
    conn.close()
    return df

def append_row(table_name, row_data):
    """테이블에 행 추가
    
    Args:
        table_name: 테이블 이름 (Donors, Requests, Matches)
        row_data: 딕셔너리 형태의 데이터
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    if table_name == "Donors":
        cursor.execute("""
            INSERT INTO Donors (donor_id, name, email, skill, mode, availability, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            row_data.get("donor_id"),
            row_data.get("name"),
            row_data.get("email"),
            row_data.get("skill"),
            row_data.get("mode"),
            row_data.get("availability", ""),
            row_data.get("created_at")
        ))
    elif table_name == "Requests":
        cursor.execute("""
            INSERT INTO Requests (request_id, email, needed_skill, description, status, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            row_data.get("request_id"),
            row_data.get("email"),
            row_data.get("needed_skill"),
            row_data.get("description", ""),
            row_data.get("status", "대기"),
            row_data.get("created_at")
        ))
    elif table_name == "Matches":
        cursor.execute("""
            INSERT INTO Matches (match_id, donor_id, request_id, score, status, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            row_data.get("match_id"),
            row_data.get("donor_id"),
            row_data.get("request_id"),
            row_data.get("score"),
            row_data.get("status", "대기"),
            row_data.get("created_at")
        ))
    
    conn.commit()
    conn.close()

def get_donors():
    """모든 재능기부자 조회"""
    return load_table("Donors")

def get_requests():
    """모든 재능 수요 조회"""
    return load_table("Requests")

def get_matches():
    """모든 매칭 조회"""
    return load_table("Matches")

def update_donor(donor_id, name, email, skill, mode, availability):
    """재능기부자 정보 업데이트"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE Donors 
        SET name = ?, email = ?, skill = ?, mode = ?, availability = ?
        WHERE donor_id = ?
    """, (name, email, skill, mode, availability, donor_id))
    conn.commit()
    conn.close()

def update_request(request_id, email, needed_skill, description, status):
    """재능 수요 정보 업데이트"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE Requests 
        SET email = ?, needed_skill = ?, description = ?, status = ?
        WHERE request_id = ?
    """, (email, needed_skill, description, status, request_id))
    conn.commit()
    conn.close()

