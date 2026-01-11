-- Supabase 테이블 생성 SQL 스크립트
-- Supabase 대시보드의 SQL Editor에서 실행하세요

-- Donors 테이블 생성
CREATE TABLE IF NOT EXISTS donors (
    donor_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    skill TEXT NOT NULL,
    mode TEXT NOT NULL,
    availability TEXT,
    created_at TEXT NOT NULL
);

-- Requests 테이블 생성
CREATE TABLE IF NOT EXISTS requests (
    request_id TEXT PRIMARY KEY,
    email TEXT NOT NULL,
    needed_skill TEXT NOT NULL,
    description TEXT,
    status TEXT NOT NULL DEFAULT '대기',
    created_at TEXT NOT NULL
);

-- Matches 테이블 생성
CREATE TABLE IF NOT EXISTS matches (
    match_id TEXT PRIMARY KEY,
    donor_id TEXT NOT NULL,
    request_id TEXT NOT NULL,
    score INTEGER NOT NULL,
    status TEXT NOT NULL DEFAULT '대기',
    created_at TEXT NOT NULL,
    FOREIGN KEY (donor_id) REFERENCES donors(donor_id),
    FOREIGN KEY (request_id) REFERENCES requests(request_id)
);

-- RLS (Row Level Security) 정책 설정 (선택사항)
-- 공개 읽기, 인증된 사용자만 쓰기 권한
ALTER TABLE donors ENABLE ROW LEVEL SECURITY;
ALTER TABLE requests ENABLE ROW LEVEL SECURITY;
ALTER TABLE matches ENABLE ROW LEVEL SECURITY;

-- 모든 사용자가 읽기 가능
CREATE POLICY "Public read access" ON donors FOR SELECT USING (true);
CREATE POLICY "Public read access" ON requests FOR SELECT USING (true);
CREATE POLICY "Public read access" ON matches FOR SELECT USING (true);

-- 모든 사용자가 쓰기 가능 (인증 필요시 수정)
CREATE POLICY "Public insert access" ON donors FOR INSERT WITH CHECK (true);
CREATE POLICY "Public insert access" ON requests FOR INSERT WITH CHECK (true);
CREATE POLICY "Public insert access" ON matches FOR INSERT WITH CHECK (true);

-- 모든 사용자가 업데이트 가능 (인증 필요시 수정)
CREATE POLICY "Public update access" ON donors FOR UPDATE USING (true);
CREATE POLICY "Public update access" ON requests FOR UPDATE USING (true);
CREATE POLICY "Public update access" ON matches FOR UPDATE USING (true);
