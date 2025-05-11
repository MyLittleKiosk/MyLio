

-- 데이터베이스 선택
-- USE mylio;

-- 안전 모드 해제
-- SET SQL_SAFE_UPDATES = 0;

-- ============================
-- 기존 데이터 초기화
-- ============================

-- 종속성 있는 테이블부터 삭제
-- DELETE FROM nutrition_value WHERE menu_id IN (SELECT id FROM menu WHERE store_id = 3);
-- DELETE FROM menu_ingredient WHERE menu_id IN (SELECT id FROM menu WHERE store_id = 3);
-- DELETE FROM menu_tag_map WHERE menu_id IN (SELECT id FROM menu WHERE store_id = 3);
-- DELETE FROM menu_option_map WHERE menu_id IN (SELECT id FROM menu WHERE store_id = 3);
-- DELETE FROM nutrition_value WHERE store_id = 3;
-- DELETE FROM menu WHERE store_id = 3;
-- DELETE FROM category WHERE store_id = 3;
-- DELETE FROM option_detail WHERE option_id IN (SELECT id FROM options WHERE store_id = 3);
-- DELETE FROM options WHERE store_id = 3;
-- DELETE FROM account WHERE store_id = 3;

-- ============================
-- 기본 데이터 삽입
-- ============================

-- 0. 원재료, 영양성분
-- 영양성분 템플릿 데이터 (존재하지 않는 경우 추가)
INSERT IGNORE INTO nutrition_template (id, name_kr, name_en, unit_type, created_at, updated_at)
VALUES
(1, '열량', 'Calories', 'kcal', NOW(), NOW()),
(2, '탄수화물', 'Carbohydrate', 'g', NOW(), NOW()),
(3, '당류', 'Sugar', 'g', NOW(), NOW()),
(4, '단백질', 'Protein', 'g', NOW(), NOW()),
(5, '지방', 'Fat', 'g', NOW(), NOW()),
(6, '포화지방', 'Saturated Fat', 'g', NOW(), NOW()),
(7, '트랜스지방', 'Trans Fat', 'g', NOW(), NOW()),
(8, '콜레스테롤', 'Cholesterol', 'mg', NOW(), NOW()),
(9, '나트륨', 'Sodium', 'mg', NOW(), NOW()),
(10, '카페인', 'Caffeine', 'mg', NOW(), NOW());

-- 원재료 템플릿 데이터 (존재하지 않는 경우 추가)
INSERT IGNORE INTO ingredient_template (id, name_kr, name_en, status, created_at, updated_at)
VALUES
(1, '에스프레소', 'Espresso', 'REGISTERED', NOW(), NOW()),
(2, '우유', 'Milk', 'REGISTERED', NOW(), NOW()),
(3, '생크림', 'Whipped Cream', 'REGISTERED', NOW(), NOW()),
(4, '초콜릿 시럽', 'Chocolate Syrup', 'REGISTERED', NOW(), NOW()),
(5, '바닐라 시럽', 'Vanilla Syrup', 'REGISTERED', NOW(), NOW()),
(6, '카라멜 시럽', 'Caramel Syrup', 'REGISTERED', NOW(), NOW()),
(7, '헤이즐넛 시럽', 'Hazelnut Syrup', 'REGISTERED', NOW(), NOW()),
(8, '알mond 시럽', 'Almond Syrup', 'REGISTERED', NOW(), NOW()),
(9, '녹차 파우더', 'Green Tea Powder', 'REGISTERED', NOW(), NOW()),
(10, '자몽 주스', 'Grapefruit Juice', 'REGISTERED', NOW(), NOW()),
(11, '오렌지 주스', 'Orange Juice', 'REGISTERED', NOW(), NOW()),
(12, '딸기 시럽', 'Strawberry Syrup', 'REGISTERED', NOW(), NOW()),
(13, '블루베리', 'Blueberry', 'REGISTERED', NOW(), NOW()),
(14, '망고', 'Mango', 'REGISTERED', NOW(), NOW()),
(15, '바나나', 'Banana', 'REGISTERED', NOW(), NOW()),
(16, '요거트 파우더', 'Yogurt Powder', 'REGISTERED', NOW(), NOW()),
(17, '얼음', 'Ice', 'REGISTERED', NOW(), NOW()),
(18, '복숭아 티백', 'Peach Tea Bag', 'REGISTERED', NOW(), NOW()),
(19, '레몬', 'Lemon', 'REGISTERED', NOW(), NOW()),
(20, '코코넛 시럽', 'Coconut Syrup', 'REGISTERED', NOW(), NOW()),
(21, '초콜릿 칩', 'Chocolate Chip', 'REGISTERED', NOW(), NOW()),
(22, '쿠키 크럼블', 'Cookie Crumble', 'REGISTERED', NOW(), NOW()),
(23, '커피 원두', 'Coffee Bean', 'REGISTERED', NOW(), NOW());

-- 1. 매장 정보
-- Store 데이터 삽입
INSERT INTO store (id, name, address, status, created_at, updated_at)
VALUES
    (1, '매장1', '주소1', 'REGISTERED', NOW(), NOW()),
    (2, '매장2', '주소2', 'REGISTERED', NOW(), NOW()),
    (3, '메가커피 강남점', '서울 강남구 역삼동 123-45', 'REGISTERED', NOW(), NOW()),
    (4, '메가커피 판교점', '경기 성남시 분당구 판교로 256', 'REGISTERED', NOW(), NOW()),
    (5, '메가커피 홍대점', '서울 마포구 와우산로 123', 'REGISTERED', NOW(), NOW());

-- 2. 계정 생성
INSERT INTO account (id, store_id, email, username, password, role, status, created_at, updated_at)
VALUES
    (1, NULL,'test1@ssafy.io', '전아현', '$2a$10$kJJYLA3v7N6hxuGJ49IDz.ZdLTa0Dk2okd.iNUUPXVzKy17cm9XB6', 'SUPER', 'REGISTERED',NOW(),NOW()),
    (2, 1,'test2@ssafy.io', '강남점', '$2a$10$kJJYLA3v7N6hxuGJ49IDz.ZdLTa0Dk2okd.iNUUPXVzKy17cm9XB6', 'STORE', 'REGISTERED', NOW(), NOW()),
    (3, 2,'test3@ssafy.io', 'admin2', '$2a$10$kJJYLA3v7N6hxuGJ49IDz.ZdLTa0Dk2okd.iNUUPXVzKy17cm9XB6', 'STORE', 'REGISTERED', NOW(), NOW()),
    (100, 3, 'admin@megacoffee.com', '매장관리자', '$2a$10$kJJYLA3v7N6hxuGJ49IDz.ZdLTa0Dk2okd.iNUUPXVzKy17cm9XB6', 'STORE', 'REGISTERED', NOW(), NOW());


-- 3. 카테고리 데이터
INSERT INTO category (id, store_id, name_kr, name_en, status, created_at, updated_at)
VALUES
    (101, 3, '커피', 'Coffee', 'REGISTERED', NOW(), NOW()),
    (102, 3, '논커피', 'Non-Coffee', 'REGISTERED', NOW(), NOW()),
    (103, 3, '차', 'Tea', 'REGISTERED', NOW(), NOW()),
    (104, 3, '에이드', 'Ade', 'REGISTERED', NOW(), NOW()),
    (105, 3, '스무디', 'Smoothie', 'REGISTERED', NOW(), NOW()),
    (106, 3, '프라페', 'Frappe', 'REGISTERED', NOW(), NOW()),
    (107, 3, '디저트', 'Dessert', 'REGISTERED', NOW(), NOW()),
    (108, 3, '디카페인', 'Decaf', 'REGISTERED', NOW(), NOW());

-- 4. 메뉴 데이터
INSERT INTO menu (id, store_id, category_id, name_kr, name_en, description, price, image_url, status, created_at, updated_at)
VALUES
-- 커피 카테고리
(101, 3, 101, '아메리카노', 'Americano', '진한 에스프레소에 물을 더해 깔끔한 맛의 아메리카노', 1500, 'americano.jpg', 'SELLING', NOW(), NOW()),
(102, 3, 101, '카페라떼', 'Cafe Latte', '진한 에스프레소와 부드러운 우유가 어우러진 라떼', 2500, 'cafelatte.jpg', 'SELLING', NOW(), NOW()),
(103, 3, 101, '바닐라 라떼', 'Vanilla Latte', '바닐라 시럽이 달콤하게 어우러진 라떼', 3000, 'vanillalatte.jpg', 'SELLING', NOW(), NOW()),
(104, 3, 101, '카라멜 마끼아또', 'Caramel Macchiato', '바닐라 시럽과 카라멜 소스의 달콤한 조화', 3500, 'caramelmacchiato.jpg', 'SELLING', NOW(), NOW()),
(105, 3, 101, '카페모카', 'Cafe Mocha', '초콜릿과 에스프레소의 절묘한 조화', 3500, 'cafemocha.jpg', 'SELLING', NOW(), NOW()),
(106, 3, 101, '연유라떼', 'Condensed Milk Latte', '달콤한 연유와 에스프레소의 조화', 3200, 'condensedlatte.jpg', 'SELLING', NOW(), NOW()),
(107, 3, 101, '콜드브루', 'Cold Brew', '장시간 추출하여 깊고 부드러운 풍미의 콜드브루', 3000, 'coldbrew.jpg', 'SELLING', NOW(), NOW()),
(108, 3, 101, '콜드브루 라떼', 'Cold Brew Latte', '콜드브루와 우유의 부드러운 조화', 3500, 'coldbrewlatte.jpg', 'SELLING', NOW(), NOW()),

-- 논커피 카테고리
(109, 3, 102, '초코라떼', 'Chocolate Latte', '달콤한 초콜릿과 부드러운 우유의 조화', 3200, 'chocolatte.jpg', 'SELLING', NOW(), NOW()),
(110, 3, 102, '곡물라떼', 'Grain Latte', '건강한 곡물과 부드러운 우유의 조화', 3000, 'grainlatte.jpg', 'SELLING', NOW(), NOW()),
(111, 3, 102, '딸기라떼', 'Strawberry Latte', '상큼한 딸기와 부드러운 우유의 조화', 3500, 'strawberrylatte.jpg', 'SELLING', NOW(), NOW()),
(112, 3, 102, '밀크셰이크', 'Milk Shake', '진한 우유의 깊은 맛을 느낄 수 있는 밀크셰이크', 3700, 'milkshake.jpg', 'SELLING', NOW(), NOW()),

-- 차 카테고리
(113, 3, 103, '복숭아 아이스티', 'Peach Ice Tea', '달콤한 복숭아향이 가득한 아이스티', 2500, 'peachicetea.jpg', 'SELLING', NOW(), NOW()),
(114, 3, 103, '페퍼민트', 'Peppermint Tea', '상쾌한 페퍼민트향이 가득한 차', 2300, 'pepperminttea.jpg', 'SELLING', NOW(), NOW()),
(115, 3, 103, '히비스커스', 'Hibiscus Tea', '상큼한 히비스커스 차', 2300, 'hibiscustea.jpg', 'SELLING', NOW(), NOW()),
(116, 3, 103, '녹차', 'Green Tea', '은은한 향의 녹차', 2000, 'greentea.jpg', 'SELLING', NOW(), NOW()),
(117, 3, 103, '얼그레이', 'Earl Grey', '베르가못 향이 특징인 얼그레이 차', 2300, 'earlgrey.jpg', 'SELLING', NOW(), NOW()),
(118, 3, 103, '루이보스', 'Rooibos Tea', '풍부한 항산화 성분의 루이보스 차', 2500, 'rooibos.jpg', 'SELLING', NOW(), NOW()),
(119, 3, 103, '한라봉차', 'Hallabong Tea', '제주 한라봉의 향긋함이 살아있는 차', 2800, 'hallabongtea.jpg', 'SELLING', NOW(), NOW()),

-- 에이드 카테고리
(120, 3, 104, '자몽 에이드', 'Grapefruit Ade', '상큼한 자몽 에이드', 3300, 'grapefruitade.jpg', 'SELLING', NOW(), NOW()),
(121, 3, 104, '레몬 에이드', 'Lemon Ade', '상큼한 레몬 에이드', 3300, 'lemonade.jpg', 'SELLING', NOW(), NOW()),

-- 스무디 카테고리
(122, 3, 105, '딸기 스무디', 'Strawberry Smoothie', '새콤달콤한 딸기 스무디', 3500, 'strawberrysmoothie.jpg', 'SELLING', NOW(), NOW()),
(123, 3, 105, '블루베리 요거트 스무디', 'Blueberry Yogurt Smoothie', '새콤달콤한 블루베리와 요거트의 만남', 3800, 'blueberryyogurtsmoothie.jpg', 'SELLING', NOW(), NOW()),

-- 프라페 카테고리
(124, 3, 106, '쿠키 프라페', 'Cookie Frappe', '바삭한 쿠키가 들어간 프라페', 4000, 'cookiefrappe.jpg', 'SELLING', NOW(), NOW()),
(125, 3, 106, '초코 프라페', 'Chocolate Frappe', '진한 초콜릿 맛의 프라페', 4000, 'chocofrappe.jpg', 'SELLING', NOW(), NOW()),
(126, 3, 106, '카라멜 프라페', 'Caramel Frappe', '달콤한 카라멜 맛의 프라페', 4000, 'caramelfrappe.jpg', 'SELLING', NOW(), NOW()),

-- 디저트 카테고리
(127, 3, 107, '티라미수', 'Tiramisu', '부드러운 마스카포네 치즈와 에스프레소의 풍미', 4500, 'tiramisu.jpg', 'SELLING', NOW(), NOW()),
(128, 3, 107, '초코 브라우니', 'Chocolate Brownie', '진한 초콜릿 브라우니', 3800, 'chocobrownie.jpg', 'SELLING', NOW(), NOW()),
(129, 3, 107, '치즈 케이크', 'Cheese Cake', '부드러운 치즈 케이크', 4200, 'cheesecake.jpg', 'SELLING', NOW(), NOW()),

-- 디카페인 카테고리
(130, 3, 108, '디카페인 아메리카노', 'Decaf Americano', '카페인 걱정 없이 즐기는 아메리카노', 2000, 'decafamericano.jpg', 'SELLING', NOW(), NOW()),
(131, 3, 108, '디카페인 콜드브루', 'Decaf Cold Brew', '카페인 걱정 없이 즐기는 콜드브루', 3500, 'decafcoldbrew.jpg', 'SELLING', NOW(), NOW()),
(132, 3, 108, '디카페인 콜드브루 라떼', 'Decaf Cold Brew Latte', '카페인 걱정 없이 즐기는 콜드브루 라떼', 4000, 'decafcoldbrewlatte.jpg', 'SELLING', NOW(), NOW());

-- 5. 옵션 데이터
INSERT INTO options (id, store_id, option_name_kr, option_name_en, status, created_at, updated_at)
VALUES
    (101, 3, '사이즈', 'Size', 'REGISTERED', NOW(), NOW()),
    (102, 3, '온도', 'Temperature', 'REGISTERED', NOW(), NOW()),
    (103, 3, '얼음량', 'Ice Amount', 'REGISTERED', NOW(), NOW()),
    (104, 3, '당도', 'Sweetness', 'REGISTERED', NOW(), NOW()),
    (105, 3, '샷 옵션', 'Shot Option', 'REGISTERED', NOW(), NOW()),
    (106, 3, '시럽 추가', 'Extra Syrup', 'REGISTERED', NOW(), NOW()),
    (107, 3, '휘핑크림', 'Whipped Cream', 'REGISTERED', NOW(), NOW()),
    (108, 3, '우유 변경', 'Milk Change', 'REGISTERED', NOW(), NOW());

-- 6. 옵션 상세 데이터
INSERT INTO option_detail (id, option_id, value, additional_price, status, created_at, updated_at)
VALUES
-- 사이즈 옵션 (101)
(1001, 101, 'S', 0, 'REGISTERED', NOW(), NOW()),
(1002, 101, 'M', 500, 'REGISTERED', NOW(), NOW()),
(1003, 101, 'L', 1000, 'REGISTERED', NOW(), NOW()),

-- 온도 옵션 (102)
(1004, 102, 'HOT', 0, 'REGISTERED', NOW(), NOW()),
(1005, 102, 'ICE', 0, 'REGISTERED', NOW(), NOW()),

-- 얼음량 옵션 (103)
(1006, 103, '얼음 없음', 0, 'REGISTERED', NOW(), NOW()),
(1007, 103, '얼음 적게', 0, 'REGISTERED', NOW(), NOW()),
(1008, 103, '얼음 보통', 0, 'REGISTERED', NOW(), NOW()),
(1009, 103, '얼음 많이', 0, 'REGISTERED', NOW(), NOW()),

-- 당도 옵션 (104)
(1010, 104, '당도 0%', 0, 'REGISTERED', NOW(), NOW()),
(1011, 104, '당도 30%', 0, 'REGISTERED', NOW(), NOW()),
(1012, 104, '당도 50%', 0, 'REGISTERED', NOW(), NOW()),
(1013, 104, '당도 70%', 0, 'REGISTERED', NOW(), NOW()),
(1014, 104, '당도 100%', 0, 'REGISTERED', NOW(), NOW()),

-- 샷 옵션 (105)
(1015, 105, '샷 추가 없음', 0, 'REGISTERED', NOW(), NOW()),
(1016, 105, '연하게', -500, 'REGISTERED', NOW(), NOW()),  -- 샷 빼기 옵션은 가격 할인
(1017, 105, '샷 1개 추가', 500, 'REGISTERED', NOW(), NOW()),
(1018, 105, '샷 2개 추가', 1000, 'REGISTERED', NOW(), NOW()),

-- 시럽 추가 옵션 (106)
(1019, 106, '시럽 추가 없음', 0, 'REGISTERED', NOW(), NOW()),
(1020, 106, '바닐라 시럽 추가', 300, 'REGISTERED', NOW(), NOW()),
(1021, 106, '카라멜 시럽 추가', 300, 'REGISTERED', NOW(), NOW()),
(1022, 106, '헤이즐넛 시럽 추가', 300, 'REGISTERED', NOW(), NOW()),

-- 휘핑크림 옵션 (107)
(1023, 107, '휘핑크림 없음', 0, 'REGISTERED', NOW(), NOW()),
(1024, 107, '휘핑크림 추가', 500, 'REGISTERED', NOW(), NOW()),

-- 우유 변경 옵션 (108)
(1025, 108, '일반 우유', 0, 'REGISTERED', NOW(), NOW()),
(1026, 108, '저지방 우유', 500, 'REGISTERED', NOW(), NOW()),
(1027, 108, '두유', 500, 'REGISTERED', NOW(), NOW()),
(1028, 108, '오트 우유', 700, 'REGISTERED', NOW(), NOW());

-- 7. 메뉴-태그 매핑
INSERT INTO menu_tag_map (menu_id, store_id, tag_kr, tag_en, created_at, updated_at)
VALUES
-- 커피 카테고리 태그
(101, 3, '커피', 'Coffee', NOW(), NOW()),
(101, 3, '베스트셀러', 'Best Seller', NOW(), NOW()),
(101, 3, '깔끔한', 'Clean', NOW(), NOW()),

(102, 3, '커피', 'Coffee', NOW(), NOW()),
(102, 3, '고소한', 'Nutty', NOW(), NOW()),
(102, 3, '우유', 'Milk', NOW(), NOW()),

(103, 3, '커피', 'Coffee', NOW(), NOW()),
(103, 3, '달콤한', 'Sweet', NOW(), NOW()),
(103, 3, '바닐라', 'Vanilla', NOW(), NOW()),
(103, 3, '우유', 'Milk', NOW(), NOW()),

(104, 3, '커피', 'Coffee', NOW(), NOW()),
(104, 3, '달콤한', 'Sweet', NOW(), NOW()),
(104, 3, '카라멜', 'Caramel', NOW(), NOW()),
(104, 3, '우유', 'Milk', NOW(), NOW()),
(104, 3, '베스트셀러', 'Best Seller', NOW(), NOW()),

(105, 3, '커피', 'Coffee', NOW(), NOW()),
(105, 3, '달콤한', 'Sweet', NOW(), NOW()),
(105, 3, '초콜릿', 'Chocolate', NOW(), NOW()),
(105, 3, '우유', 'Milk', NOW(), NOW()),

(106, 3, '커피', 'Coffee', NOW(), NOW()),
(106, 3, '달콤한', 'Sweet', NOW(), NOW()),
(106, 3, '연유', 'Condensed Milk', NOW(), NOW()),
(106, 3, '우유', 'Milk', NOW(), NOW()),

(107, 3, '커피', 'Coffee', NOW(), NOW()),
(107, 3, '깊은', 'Deep', NOW(), NOW()),
(107, 3, '콜드브루', 'Cold Brew', NOW(), NOW()),

(108, 3, '커피', 'Coffee', NOW(), NOW()),
(108, 3, '부드러운', 'Smooth', NOW(), NOW()),
(108, 3, '콜드브루', 'Cold Brew', NOW(), NOW()),
(108, 3, '우유', 'Milk', NOW(), NOW()),

-- 논커피 카테고리 태그
(109, 3, '초콜릿', 'Chocolate', NOW(), NOW()),
(109, 3, '달콤한', 'Sweet', NOW(), NOW()),
(109, 3, '우유', 'Milk', NOW(), NOW()),

(110, 3, '건강한', 'Healthy', NOW(), NOW()),
(110, 3, '고소한', 'Nutty', NOW(), NOW()),
(110, 3, '곡물', 'Grain', NOW(), NOW()),
(110, 3, '우유', 'Milk', NOW(), NOW()),

(111, 3, '과일', 'Fruit', NOW(), NOW()),
(111, 3, '딸기', 'Strawberry', NOW(), NOW()),
(111, 3, '달콤한', 'Sweet', NOW(), NOW()),
(111, 3, '우유', 'Milk', NOW(), NOW()),

(112, 3, '달콤한', 'Sweet', NOW(), NOW()),
(112, 3, '우유', 'Milk', NOW(), NOW()),
(112, 3, '진한', 'Rich', NOW(), NOW()),

-- 차 카테고리 태그
(113, 3, '과일', 'Fruit', NOW(), NOW()),
(113, 3, '복숭아', 'Peach', NOW(), NOW()),
(113, 3, '달콤한', 'Sweet', NOW(), NOW()),
(113, 3, '차', 'Tea', NOW(), NOW()),

(114, 3, '상쾌한', 'Refreshing', NOW(), NOW()),
(114, 3, '허브', 'Herb', NOW(), NOW()),
(114, 3, '페퍼민트', 'Peppermint', NOW(), NOW()),
(114, 3, '차', 'Tea', NOW(), NOW()),

(115, 3, '상큼한', 'Tangy', NOW(), NOW()),
(115, 3, '허브', 'Herb', NOW(), NOW()),
(115, 3, '히비스커스', 'Hibiscus', NOW(), NOW()),
(115, 3, '차', 'Tea', NOW(), NOW()),

(116, 3, '은은한', 'Mild', NOW(), NOW()),
(116, 3, '녹차', 'Green Tea', NOW(), NOW()),
(116, 3, '차', 'Tea', NOW(), NOW()),
(116, 3, '건강한', 'Healthy', NOW(), NOW()),

(117, 3, '향긋한', 'Fragrant', NOW(), NOW()),
(117, 3, '얼그레이', 'Earl Grey', NOW(), NOW()),
(117, 3, '차', 'Tea', NOW(), NOW()),

(118, 3, '루이보스', 'Rooibos', NOW(), NOW()),
(118, 3, '차', 'Tea', NOW(), NOW()),
(118, 3, '건강한', 'Healthy', NOW(), NOW()),

(119, 3, '과일', 'Fruit', NOW(), NOW()),
(119, 3, '한라봉', 'Hallabong', NOW(), NOW()),
(119, 3, '차', 'Tea', NOW(), NOW()),
(119, 3, '상큼한', 'Tangy', NOW(), NOW()),

-- 에이드 카테고리 태그
(120, 3, '에이드', 'Ade', NOW(), NOW()),
(120, 3, '자몽', 'Grapefruit', NOW(), NOW()),
(120, 3, '상큼한', 'Refreshing', NOW(), NOW()),
(120, 3, '과일', 'Fruit', NOW(), NOW()),

(121, 3, '에이드', 'Ade', NOW(), NOW()),
(121, 3, '레몬', 'Lemon', NOW(), NOW()),
(121, 3, '상큼한', 'Refreshing', NOW(), NOW()),
(121, 3, '과일', 'Fruit', NOW(), NOW()),

-- 스무디 카테고리 태그
(122, 3, '스무디', 'Smoothie', NOW(), NOW()),
(122, 3, '딸기', 'Strawberry', NOW(), NOW()),
(122, 3, '과일', 'Fruit', NOW(), NOW()),
(122, 3, '달콤한', 'Sweet', NOW(), NOW()),

(123, 3, '스무디', 'Smoothie', NOW(), NOW()),
(123, 3, '블루베리', 'Blueberry', NOW(), NOW()),
(123, 3, '요거트', 'Yogurt', NOW(), NOW()),
(123, 3, '과일', 'Fruit', NOW(), NOW()),
(123, 3, '베스트셀러', 'Best Seller', NOW(), NOW()),

-- 프라페 카테고리 태그
(124, 3, '프라페', 'Frappe', NOW(), NOW()),
(124, 3, '쿠키', 'Cookie', NOW(), NOW()),
(124, 3, '달콤한', 'Sweet', NOW(), NOW()),

(125, 3, '프라페', 'Frappe', NOW(), NOW()),
(125, 3, '초콜릿', 'Chocolate', NOW(), NOW()),
(125, 3, '달콤한', 'Sweet', NOW(), NOW()),

(126, 3, '프라페', 'Frappe', NOW(), NOW()),
(126, 3, '카라멜', 'Caramel', NOW(), NOW()),
(126, 3, '달콤한', 'Sweet', NOW(), NOW()),

-- 디저트 카테고리 태그
(127, 3, '디저트', 'Dessert', NOW(), NOW()),
(127, 3, '티라미수', 'Tiramisu', NOW(), NOW()),
(127, 3, '달콤한', 'Sweet', NOW(), NOW()),
(127, 3, '커피', 'Coffee', NOW(), NOW()),

(128, 3, '디저트', 'Dessert', NOW(), NOW()),
(128, 3, '초콜릿', 'Chocolate', NOW(), NOW()),
(128, 3, '달콤한', 'Sweet', NOW(), NOW()),
(128, 3, '브라우니', 'Brownie', NOW(), NOW()),

(129, 3, '디저트', 'Dessert', NOW(), NOW()),
(129, 3, '치즈', 'Cheese', NOW(), NOW()),
(129, 3, '달콤한', 'Sweet', NOW(), NOW()),
(129, 3, '케이크', 'Cake', NOW(), NOW()),

-- 디카페인 카테고리 태그
(130, 3, '디카페인', 'Decaf', NOW(), NOW()),
(130, 3, '커피', 'Coffee', NOW(), NOW()),
(130, 3, '아메리카노', 'Americano', NOW(), NOW()),

(131, 3, '디카페인', 'Decaf', NOW(), NOW()),
(131, 3, '커피', 'Coffee', NOW(), NOW()),
(131, 3, '콜드브루', 'Cold Brew', NOW(), NOW()),

(132, 3, '디카페인', 'Decaf', NOW(), NOW()),
(132, 3, '커피', 'Coffee', NOW(), NOW()),
(132, 3, '콜드브루', 'Cold Brew', NOW(), NOW()),
(132, 3, '우유', 'Milk', NOW(), NOW());

-- 8. 메뉴-옵션 매핑
INSERT INTO menu_option_map (menu_id, option_id, option_detail_id, is_required, created_at, updated_at)
VALUES
-- 아메리카노(101) 옵션
(101, 101, 1001, TRUE, NOW(), NOW()),  -- 아메리카노 - S (필수)
(101, 101, 1002, TRUE, NOW(), NOW()),  -- 아메리카노 - M (필수)
(101, 101, 1003, TRUE, NOW(), NOW()),  -- 아메리카노 - L (필수)
(101, 102, 1004, TRUE, NOW(), NOW()),  -- 아메리카노 - HOT (필수)
(101, 102, 1005, TRUE, NOW(), NOW()),  -- 아메리카노 - ICE (필수)
(101, 103, 1006, FALSE, NOW(), NOW()), -- 아메리카노 - 얼음 없음
(101, 103, 1007, FALSE, NOW(), NOW()), -- 아메리카노 - 얼음 적게
(101, 103, 1008, FALSE, NOW(), NOW()), -- 아메리카노 - 얼음 보통
(101, 103, 1009, FALSE, NOW(), NOW()), -- 아메리카노 - 얼음 많이
(101, 105, 1015, FALSE, NOW(), NOW()), -- 아메리카노 - 샷 추가 없음
(101, 105, 1016, FALSE, NOW(), NOW()), -- 아메리카노 - 연하게
(101, 105, 1017, FALSE, NOW(), NOW()), -- 아메리카노 - 샷 1개 추가
(101, 105, 1018, FALSE, NOW(), NOW()); -- 아메리카노 - 샷 2개 추가

-- 이런 식으로 다른 메뉴에 대해서도 옵션 매핑을 계속 추가할 수 있습니다.
-- 카페라떼(102) 옵션 추가 예시:
INSERT INTO menu_option_map (menu_id, option_id, option_detail_id, is_required, created_at, updated_at)
VALUES
    (102, 101, 1001, TRUE, NOW(), NOW()),  -- 카페라떼 - S (필수)
    (102, 101, 1002, TRUE, NOW(), NOW()),  -- 카페라떼 - M (필수)
    (102, 101, 1003, TRUE, NOW(), NOW()),  -- 카페라떼 - L (필수)
    (102, 102, 1004, TRUE, NOW(), NOW()),  -- 카페라떼 - HOT (필수)
    (102, 102, 1005, TRUE, NOW(), NOW()),  -- 카페라떼 - ICE (필수)
    (102, 103, 1006, FALSE, NOW(), NOW()), -- 카페라떼 - 얼음 없음
    (102, 103, 1007, FALSE, NOW(), NOW()), -- 카페라떼 - 얼음 적게
    (102, 103, 1008, FALSE, NOW(), NOW()), -- 카페라떼 - 얼음 보통
    (102, 103, 1009, FALSE, NOW(), NOW()), -- 카페라떼 - 얼음 많이
-- 계속: 카페라떼(102) 나머지 옵션 추가
    (102, 105, 1015, FALSE, NOW(), NOW()), -- 카페라떼 - 샷 추가 없음
    (102, 105, 1016, FALSE, NOW(), NOW()), -- 카페라떼 - 연하게
    (102, 105, 1017, FALSE, NOW(), NOW()), -- 카페라떼 - 샷 1개 추가
    (102, 105, 1018, FALSE, NOW(), NOW()), -- 카페라떼 - 샷 2개 추가
    (102, 108, 1025, FALSE, NOW(), NOW()), -- 카페라떼 - 일반 우유
    (102, 108, 1026, FALSE, NOW(), NOW()), -- 카페라떼 - 저지방 우유
    (102, 108, 1027, FALSE, NOW(), NOW()), -- 카페라떼 - 두유
    (102, 108, 1028, FALSE, NOW(), NOW()); -- 카페라떼 - 오트 우유

-- 바닐라 라떼(103) 옵션
INSERT INTO menu_option_map (menu_id, option_id, option_detail_id, is_required, created_at, updated_at)
VALUES
    (103, 101, 1001, TRUE, NOW(), NOW()),  -- 바닐라 라떼 - S (필수)
    (103, 101, 1002, TRUE, NOW(), NOW()),  -- 바닐라 라떼 - M (필수)
    (103, 101, 1003, TRUE, NOW(), NOW()),  -- 바닐라 라떼 - L (필수)
    (103, 102, 1004, TRUE, NOW(), NOW()),  -- 바닐라 라떼 - HOT (필수)
    (103, 102, 1005, TRUE, NOW(), NOW()),  -- 바닐라 라떼 - ICE (필수)
    (103, 103, 1006, FALSE, NOW(), NOW()), -- 바닐라 라떼 - 얼음 없음
    (103, 103, 1007, FALSE, NOW(), NOW()), -- 바닐라 라떼 - 얼음 적게
    (103, 103, 1008, FALSE, NOW(), NOW()), -- 바닐라 라떼 - 얼음 보통
    (103, 103, 1009, FALSE, NOW(), NOW()), -- 바닐라 라떼 - 얼음 많이
    (103, 104, 1010, FALSE, NOW(), NOW()), -- 바닐라 라떼 - 당도 0%
    (103, 104, 1011, FALSE, NOW(), NOW()), -- 바닐라 라떼 - 당도 30%
    (103, 104, 1012, FALSE, NOW(), NOW()), -- 바닐라 라떼 - 당도 50%
    (103, 104, 1013, FALSE, NOW(), NOW()), -- 바닐라 라떼 - 당도 70%
    (103, 104, 1014, FALSE, NOW(), NOW()), -- 바닐라 라떼 - 당도 100%
    (103, 105, 1015, FALSE, NOW(), NOW()), -- 바닐라 라떼 - 샷 추가 없음
    (103, 105, 1016, FALSE, NOW(), NOW()), -- 바닐라 라떼 - 연하게
    (103, 105, 1017, FALSE, NOW(), NOW()), -- 바닐라 라떼 - 샷 1개 추가
    (103, 105, 1018, FALSE, NOW(), NOW()), -- 바닐라 라떼 - 샷 2개 추가
    (103, 108, 1025, FALSE, NOW(), NOW()), -- 바닐라 라떼 - 일반 우유
    (103, 108, 1026, FALSE, NOW(), NOW()), -- 바닐라 라떼 - 저지방 우유
    (103, 108, 1027, FALSE, NOW(), NOW()), -- 바닐라 라떼 - 두유
    (103, 108, 1028, FALSE, NOW(), NOW()); -- 바닐라 라떼 - 오트 우유

-- 나머지 커피 메뉴들에 대한 옵션도 유사하게 추가...

-- 디카페인 아메리카노(130) 옵션
INSERT INTO menu_option_map (menu_id, option_id, option_detail_id, is_required, created_at, updated_at)
VALUES
    (130, 101, 1001, TRUE, NOW(), NOW()),  -- 디카페인 아메리카노 - S (필수)
    (130, 101, 1002, TRUE, NOW(), NOW()),  -- 디카페인 아메리카노 - M (필수)
    (130, 101, 1003, TRUE, NOW(), NOW()),  -- 디카페인 아메리카노 - L (필수)
    (130, 102, 1004, TRUE, NOW(), NOW()),  -- 디카페인 아메리카노 - HOT (필수)
    (130, 102, 1005, TRUE, NOW(), NOW()),  -- 디카페인 아메리카노 - ICE (필수)
    (130, 103, 1006, FALSE, NOW(), NOW()), -- 디카페인 아메리카노 - 얼음 없음
    (130, 103, 1007, FALSE, NOW(), NOW()), -- 디카페인 아메리카노 - 얼음 적게
    (130, 103, 1008, FALSE, NOW(), NOW()), -- 디카페인 아메리카노 - 얼음 보통
    (130, 103, 1009, FALSE, NOW(), NOW()); -- 디카페인 아메리카노 - 얼음 많이

-- 9. 메뉴 원재료 데이터
INSERT INTO menu_ingredient (menu_id, ingredient_id, store_id, created_at, updated_at)
VALUES
-- 아메리카노(101) 원재료
(101, 1, 3, NOW(), NOW()),  -- 아메리카노 - 에스프레소
(101, 17, 3, NOW(), NOW()), -- 아메리카노 - 얼음 (ICE일 경우)
(101, 23, 3, NOW(), NOW()), -- 아메리카노 - 커피 원두

-- 카페라떼(102) 원재료
(102, 1, 3, NOW(), NOW()),  -- 카페라떼 - 에스프레소
(102, 2, 3, NOW(), NOW()),  -- 카페라떼 - 우유
(102, 17, 3, NOW(), NOW()), -- 카페라떼 - 얼음 (ICE일 경우)
(102, 23, 3, NOW(), NOW()), -- 카페라떼 - 커피 원두

-- 바닐라 라떼(103) 원재료
(103, 1, 3, NOW(), NOW()),  -- 바닐라 라떼 - 에스프레소
(103, 2, 3, NOW(), NOW()),  -- 바닐라 라떼 - 우유
(103, 5, 3, NOW(), NOW()),  -- 바닐라 라떼 - 바닐라 시럽
(103, 17, 3, NOW(), NOW()), -- 바닐라 라떼 - 얼음 (ICE일 경우)
(103, 23, 3, NOW(), NOW()), -- 바닐라 라떼 - 커피 원두

-- 카라멜 마끼아또(104) 원재료
(104, 1, 3, NOW(), NOW()),  -- 카라멜 마끼아또 - 에스프레소
(104, 2, 3, NOW(), NOW()),  -- 카라멜 마끼아또 - 우유
(104, 5, 3, NOW(), NOW()),  -- 카라멜 마끼아또 - 바닐라 시럽
(104, 6, 3, NOW(), NOW()),  -- 카라멜 마끼아또 - 카라멜 시럽
(104, 17, 3, NOW(), NOW()), -- 카라멜 마끼아또 - 얼음 (ICE일 경우)
(104, 23, 3, NOW(), NOW()), -- 카라멜 마끼아또 - 커피 원두

-- 카페모카(105) 원재료
(105, 1, 3, NOW(), NOW()),  -- 카페모카 - 에스프레소
(105, 2, 3, NOW(), NOW()),  -- 카페모카 - 우유
(105, 4, 3, NOW(), NOW()),  -- 카페모카 - 초콜릿 시럽
(105, 17, 3, NOW(), NOW()), -- 카페모카 - 얼음 (ICE일 경우)
(105, 23, 3, NOW(), NOW()), -- 카페모카 - 커피 원두

-- 연유라떼(106) 원재료
(106, 1, 3, NOW(), NOW()),  -- 연유라떼 - 에스프레소
(106, 2, 3, NOW(), NOW()),  -- 연유라떼 - 우유
(106, 17, 3, NOW(), NOW()), -- 연유라떼 - 얼음 (ICE일 경우)
(106, 23, 3, NOW(), NOW()), -- 연유라떼 - 커피 원두

-- 콜드브루(107) 원재료
(107, 17, 3, NOW(), NOW()), -- 콜드브루 - 얼음
(107, 23, 3, NOW(), NOW()), -- 콜드브루 - 커피 원두

-- 콜드브루 라떼(108) 원재료
(108, 2, 3, NOW(), NOW()),  -- 콜드브루 라떼 - 우유
(108, 17, 3, NOW(), NOW()), -- 콜드브루 라떼 - 얼음
(108, 23, 3, NOW(), NOW()), -- 콜드브루 라떼 - 커피 원두

-- 초코라떼(109) 원재료
(109, 2, 3, NOW(), NOW()),  -- 초코라떼 - 우유
(109, 4, 3, NOW(), NOW()),  -- 초코라떼 - 초콜릿 시럽
(109, 17, 3, NOW(), NOW()), -- 초코라떼 - 얼음 (ICE일 경우)

-- 곡물라떼(110) 원재료
(110, 2, 3, NOW(), NOW()),  -- 곡물라떼 - 우유
(110, 17, 3, NOW(), NOW()), -- 곡물라떼 - 얼음 (ICE일 경우)

-- 딸기라떼(111) 원재료
(111, 2, 3, NOW(), NOW()),  -- 딸기라떼 - 우유
(111, 12, 3, NOW(), NOW()), -- 딸기라떼 - 딸기 시럽
(111, 17, 3, NOW(), NOW()), -- 딸기라떼 - 얼음 (ICE일 경우)

-- 밀크셰이크(112) 원재료
(112, 2, 3, NOW(), NOW()),  -- 밀크셰이크 - 우유
(112, 17, 3, NOW(), NOW()), -- 밀크셰이크 - 얼음

-- 복숭아 아이스티(113) 원재료
(113, 17, 3, NOW(), NOW()), -- 복숭아 아이스티 - 얼음
(113, 18, 3, NOW(), NOW()), -- 복숭아 아이스티 - 복숭아 티백

-- 페퍼민트(114) 원재료
(114, 17, 3, NOW(), NOW()); -- 페퍼민트 - 얼음 (ICE일 경우)

-- 나머지 메뉴들도 유사한 방식으로 원재료 정보 추가...

-- 10. 메뉴 영양 성분 데이터
INSERT INTO nutrition_value (menu_id, nutrition_id, store_id, value, status, created_at, updated_at)
VALUES
-- 아메리카노(101) 영양성분
(101, 1, 3, 10.0, 'REGISTERED', NOW(), NOW()),   -- 아메리카노 - 열량(kcal)
(101, 2, 3, 2.0, 'REGISTERED', NOW(), NOW()),    -- 아메리카노 - 탄수화물(g)
(101, 3, 3, 0.0, 'REGISTERED', NOW(), NOW()),    -- 아메리카노 - 당류(g)
(101, 4, 3, 1.0, 'REGISTERED', NOW(), NOW()),    -- 아메리카노 - 단백질(g)
(101, 5, 3, 0.0, 'REGISTERED', NOW(), NOW()),    -- 아메리카노 - 지방(g)
(101, 9, 3, 5.0, 'REGISTERED', NOW(), NOW()),    -- 아메리카노 - 나트륨(mg)
(101, 10, 3, 75.0, 'REGISTERED', NOW(), NOW()),  -- 아메리카노 - 카페인(mg)

-- 카페라떼(102) 영양성분
(102, 1, 3, 110.0, 'REGISTERED', NOW(), NOW()),  -- 카페라떼 - 열량(kcal)
(102, 2, 3, 10.0, 'REGISTERED', NOW(), NOW()),   -- 카페라떼 - 탄수화물(g)
(102, 3, 3, 9.0, 'REGISTERED', NOW(), NOW()),    -- 카페라떼 - 당류(g)
(102, 4, 3, 6.0, 'REGISTERED', NOW(), NOW()),    -- 카페라떼 - 단백질(g)
(102, 5, 3, 4.0, 'REGISTERED', NOW(), NOW()),    -- 카페라떼 - 지방(g)
(102, 9, 3, 70.0, 'REGISTERED', NOW(), NOW()),   -- 카페라떼 - 나트륨(mg)
(102, 10, 3, 75.0, 'REGISTERED', NOW(), NOW()),  -- 카페라떼 - 카페인(mg)

-- 바닐라 라떼(103) 영양성분
(103, 1, 3, 170.0, 'REGISTERED', NOW(), NOW()),  -- 바닐라 라떼 - 열량(kcal)
(103, 2, 3, 27.0, 'REGISTERED', NOW(), NOW()),   -- 바닐라 라떼 - 탄수화물(g)
(103, 3, 3, 25.0, 'REGISTERED', NOW(), NOW()),   -- 바닐라 라떼 - 당류(g)
(103, 4, 3, 6.0, 'REGISTERED', NOW(), NOW()),    -- 바닐라 라떼 - 단백질(g)
(103, 5, 3, 4.5, 'REGISTERED', NOW(), NOW()),    -- 바닐라 라떼 - 지방(g)
(103, 9, 3, 120.0, 'REGISTERED', NOW(), NOW()),  -- 바닐라 라떼 - 나트륨(mg)
(103, 10, 3, 75.0, 'REGISTERED', NOW(), NOW()),  -- 바닐라 라떼 - 카페인(mg)

-- 카라멜 마끼아또(104) 영양성분
(104, 1, 3, 200.0, 'REGISTERED', NOW(), NOW()),  -- 카라멜 마끼아또 - 열량(kcal)
(104, 2, 3, 32.0, 'REGISTERED', NOW(), NOW()),   -- 카라멜 마끼아또 - 탄수화물(g)
(104, 3, 3, 29.0, 'REGISTERED', NOW(), NOW()),   -- 카라멜 마끼아또 - 당류(g)
(104, 4, 3, 6.0, 'REGISTERED', NOW(), NOW()),    -- 카라멜 마끼아또 - 단백질(g)
(104, 5, 3, 5.0, 'REGISTERED', NOW(), NOW()),    -- 카라멜 마끼아또 - 지방(g)
(104, 9, 3, 150.0, 'REGISTERED', NOW(), NOW()),  -- 카라멜 마끼아또 - 나트륨(mg)
(104, 10, 3, 75.0, 'REGISTERED', NOW(), NOW()),  -- 카라멜 마끼아또 - 카페인(mg)

-- 카페모카(105) 영양성분
(105, 1, 3, 230.0, 'REGISTERED', NOW(), NOW()),  -- 카페모카 - 열량(kcal)
(105, 2, 3, 28.0, 'REGISTERED', NOW(), NOW()),   -- 카페모카 - 탄수화물(g)
(105, 3, 3, 25.0, 'REGISTERED', NOW(), NOW()),   -- 카페모카 - 당류(g)
(105, 4, 3, 7.0, 'REGISTERED', NOW(), NOW()),    -- 카페모카 - 단백질(g)
(105, 5, 3, 9.0, 'REGISTERED', NOW(), NOW()),    -- 카페모카 - 지방(g)
(105, 9, 3, 130.0, 'REGISTERED', NOW(), NOW()),  -- 카페모카 - 나트륨(mg)
(105, 10, 3, 75.0, 'REGISTERED', NOW(), NOW()),  -- 카페모카 - 카페인(mg)

-- 연유라떼(106) 영양성분
(106, 1, 3, 220.0, 'REGISTERED', NOW(), NOW()),  -- 연유라떼 - 열량(kcal)
(106, 2, 3, 30.0, 'REGISTERED', NOW(), NOW()),   -- 연유라떼 - 탄수화물(g)
(106, 3, 3, 28.0, 'REGISTERED', NOW(), NOW()),   -- 연유라떼 - 당류(g)
(106, 4, 3, 7.0, 'REGISTERED', NOW(), NOW()),    -- 연유라떼 - 단백질(g)
(106, 5, 3, 7.0, 'REGISTERED', NOW(), NOW()),    -- 연유라떼 - 지방(g)
(106, 9, 3, 95.0, 'REGISTERED', NOW(), NOW()),   -- 연유라떼 - 나트륨(mg)
(106, 10, 3, 75.0, 'REGISTERED', NOW(), NOW()),  -- 연유라떼 - 카페인(mg)

-- 콜드브루(107) 영양성분
(107, 1, 3, 15.0, 'REGISTERED', NOW(), NOW()),   -- 콜드브루 - 열량(kcal)
(107, 2, 3, 2.5, 'REGISTERED', NOW(), NOW()),    -- 콜드브루 - 탄수화물(g)
(107, 3, 3, 0.0, 'REGISTERED', NOW(), NOW()),    -- 콜드브루 - 당류(g)
(107, 4, 3, 1.5, 'REGISTERED', NOW(), NOW()),    -- 콜드브루 - 단백질(g)
(107, 5, 3, 0.0, 'REGISTERED', NOW(), NOW()),    -- 콜드브루 - 지방(g)
(107, 9, 3, 8.0, 'REGISTERED', NOW(), NOW()),    -- 콜드브루 - 나트륨(mg)
(107, 10, 3, 100.0, 'REGISTERED', NOW(), NOW()), -- 콜드브루 - 카페인(mg)

-- 콜드브루 라떼(108) 영양성분
(108, 1, 3, 125.0, 'REGISTERED', NOW(), NOW()),  -- 콜드브루 라떼 - 열량(kcal)
(108, 2, 3, 11.0, 'REGISTERED', NOW(), NOW()),   -- 콜드브루 라떼 - 탄수화물(g)
(108, 3, 3, 10.0, 'REGISTERED', NOW(), NOW()),   -- 콜드브루 라떼 - 당류(g)
(108, 4, 3, 7.0, 'REGISTERED', NOW(), NOW()),    -- 콜드브루 라떼 - 단백질(g)
(108, 5, 3, 5.0, 'REGISTERED', NOW(), NOW()),    -- 콜드브루 라떼 - 지방(g)
(108, 9, 3, 80.0, 'REGISTERED', NOW(), NOW()),   -- 콜드브루 라떼 - 나트륨(mg)
(108, 10, 3, 100.0, 'REGISTERED', NOW(), NOW()); -- 콜드브루 라떼 - 카페인(mg)

-- 초코라떼부터 디카페인 콜드브루 라떼까지 나머지 메뉴의 영양 성분도 추가...
INSERT INTO nutrition_value (menu_id, nutrition_id, store_id, value, status, created_at, updated_at)
VALUES
-- 초코라떼(109) 영양성분
(109, 1, 3, 250.0, 'REGISTERED', NOW(), NOW()),  -- 초코라떼 - 열량(kcal)
(109, 2, 3, 35.0, 'REGISTERED', NOW(), NOW()),   -- 초코라떼 - 탄수화물(g)
(109, 3, 3, 32.0, 'REGISTERED', NOW(), NOW()),   -- 초코라떼 - 당류(g)
(109, 4, 3, 8.0, 'REGISTERED', NOW(), NOW()),    -- 초코라떼 - 단백질(g)
(109, 5, 3, 10.0, 'REGISTERED', NOW(), NOW()),   -- 초코라떼 - 지방(g)
(109, 9, 3, 100.0, 'REGISTERED', NOW(), NOW()),  -- 초코라떼 - 나트륨(mg)
(109, 10, 3, 0.0, 'REGISTERED', NOW(), NOW()),   -- 초코라떼 - 카페인(mg)

-- 디카페인 아메리카노(130) 영양성분
(130, 1, 3, 10.0, 'REGISTERED', NOW(), NOW()),   -- 디카페인 아메리카노 - 열량(kcal)
(130, 2, 3, 2.0, 'REGISTERED', NOW(), NOW()),    -- 디카페인 아메리카노 - 탄수화물(g)
(130, 3, 3, 0.0, 'REGISTERED', NOW(), NOW()),    -- 디카페인 아메리카노 - 당류(g)
(130, 4, 3, 1.0, 'REGISTERED', NOW(), NOW()),    -- 디카페인 아메리카노 - 단백질(g)
(130, 5, 3, 0.0, 'REGISTERED', NOW(), NOW()),    -- 디카페인 아메리카노 - 지방(g)
(130, 9, 3, 5.0, 'REGISTERED', NOW(), NOW()),    -- 디카페인 아메리카노 - 나트륨(mg)
(130, 10, 3, 5.0, 'REGISTERED', NOW(), NOW());   -- 디카페인 아메리카노 - 카페인(mg) (미량)

-- 캐시 초기화를 위한 명령 (프로그램 내에서 처리해야 함)
-- SET store_menus_cache = NULL;

-- 적용된 변경사항 확인
SELECT 'Database update completed!';