-- テーブル作成

CREATE TABLE IF NOT EXISTS Store (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    store_name VARCHAR(100) NOT NULL,
    address VARCHAR(200) NOT NULL,
    phone_number VARCHAR(20) NOT NULL,
    opening_times VARCHAR(100) NOT NULL,
    remarks VARCHAR(1000)
);

INSERT INTO Store (id, store_name, address, phone_number, opening_times, remarks) VALUES
('dfd7862a-9bab-ff0f-beac-b8a1d00a4b40', 'ガスゼリヤ御堂筋店', '大阪府大阪市中央区南船場3-100-100','123-4567-8901', '7:00~23:00', '乗用車での入店はお控えください。'),
('bb361297-10a2-c818-8fc1-c0d8347993ac', 'ガスゼリヤ萩島店' ,'萩島中区0-0-0', '000-0000-0000', '11:00~20:00', 'アルバイト募集中です'),
('7f69e3f3-d3c5-6f20-8f8b-a23396509d47', 'ガスゼリヤ都市大横浜キャンパス店', '神奈川県横浜市都筑区牛久保西3-3-1' ,'234-5678-9012', '8:00~22:00', '教科書の取り扱いを行っております'), 
('73a2cb55-170c-6c84-7d76-22efae89e077', 'ガスゼリヤ都市大世田谷キャンパス店', '東京都世田谷区玉堤1-28-1', '345-6789-0123', '8:00~22:00');