-- 관리자 계정 추가
INSERT INTO `account` (id, store_id, email,username, password, role,created_at,updated_at,status)
VALUES
    (1, NULL,'test1@ssafy.io', '전아현', '$2a$10$kJJYLA3v7N6hxuGJ49IDz.ZdLTa0Dk2okd.iNUUPXVzKy17cm9XB6', 'SUPER',NOW(),NOW(), 'REGISTERED');


INSERT INTO store (id, name, status, address, created_at, updated_at) VALUES
                                                                          (1, '싸피 다방 강남점', 'REGISTERED', '서울 강남구', NOW(), NOW()),
                                                                          (2, '싸피 다방 판교점', 'REGISTERED', '경기 성남시', NOW(), NOW());

-- 2. account
INSERT INTO account (id, store_id, email,username, password, role, status, created_at, updated_at) VALUES
                                                                                                       (2, 1,'test2@ssafy.io', '강남점', '$2a$10$kJJYLA3v7N6hxuGJ49IDz.ZdLTa0Dk2okd.iNUUPXVzKy17cm9XB6', 'STORE', 'REGISTERED', NOW(), NOW()),
                                                                                                       (3, 2,'test3@ssafy.io', 'admin2', '$2a$10$kJJYLA3v7N6hxuGJ49IDz.ZdLTa0Dk2okd.iNUUPXVzKy17cm9XB6', 'STORE', 'REGISTERED', NOW(), NOW());

-- 3. category
INSERT INTO category (id, store_id, name_kr, name_en, status, created_at, updated_at) VALUES
                                                                                          (1, 1, '커피', 'coffee', 'REGISTERED', NOW(), NOW()),
                                                                                          (2, 1, '차', 'tea', 'REGISTERED', NOW(), NOW()),
                                                                                          (3, 2, '커피', 'coffee', 'REGISTERED', NOW(), NOW());

-- 4. menu
INSERT INTO menu (id, category_id, store_id, name_kr, name_en, description, price, image_url, status, created_at, updated_at) VALUES
                                                                                                                                  (1, 1, 1, '아메리카노', 'Americano', '깔끔한 맛', 4000, 'https://mylio/americano.jpg', 'SELLING', NOW(), NOW()),
                                                                                                                                  (2, 2, 1, '녹차', 'Green Tea', '부드러운 녹차', 4500, 'https://mylio/greentea.jpg', 'SELLING', NOW(), NOW()),
                                                                                                                                  (3, 3, 2, '카페라떼', 'Cafe Latte', '고소한 라떼', 5000, 'https://mylio/latte.jpg', 'SELLING', NOW(), NOW());

-- 5. menu_tag_map
INSERT INTO menu_tag_map (id, menu_id, store_id, tag_kr, tag_en, created_at, updated_at) VALUES
                                                                                             (1, 1, 1, '인기', 'popular', NOW(), NOW()),
                                                                                             (2, 1, 1, '시원해요', 'cool', NOW(), NOW()),
                                                                                             (3, 2, 1, '건강해요', 'healthy', NOW(), NOW()),
                                                                                             (4, 3, 2, '고소해요', 'nutty', NOW(), NOW());

-- 6. ingredient_template
INSERT INTO ingredient_template (id, name_kr, name_en, status, created_at, updated_at) VALUES
                                                                                           (1, '우유', 'milk', 'REGISTERED', NOW(), NOW()),
                                                                                           (2, '녹차 가루', 'green tea powder', 'REGISTERED', NOW(), NOW());

-- 7. menu_ingredient
INSERT INTO menu_ingredient (id, store_id, menu_id, ingredient_id, created_at, updated_at) VALUES
                                                                                               (1, 1, 1, 1, NOW(), NOW()),
                                                                                               (2, 1, 2, 2, NOW(), NOW());

-- 8. options
INSERT INTO options (id, store_id, option_name_kr, option_name_en, created_at, updated_at) VALUES
    (1, 1, '사이즈', 'SIZE', NOW(), NOW());

-- 9. option_detail
INSERT INTO option_detail (id, option_id, value, additional_price, created_at, updated_at) VALUES
                                                                                               (1, 1, 'S', 0, NOW(), NOW()),
                                                                                               (2, 1, 'M', 500, NOW(), NOW()),
                                                                                               (3, 1, 'L', 1000, NOW(), NOW());

-- 10. menu_option_map (⭐ 추가된 부분)
INSERT INTO menu_option_map (id, is_required, menu_id, option_detail_id, option_id, created_at, updated_at) VALUES
                                                                                                                (1, b'1', 1, 1, 1, NOW(), NOW()), -- 아메리카노 - 사이즈 S (필수)
                                                                                                                (2, b'1', 1, 2, 1, NOW(), NOW()), -- 아메리카노 - 사이즈 M (필수)
                                                                                                                (3, b'1', 1, 3, 1, NOW(), NOW()), -- 아메리카노 - 사이즈 L (필수)
                                                                                                                (4, b'0', 2, 1, 1, NOW(), NOW()); -- 녹차 - 사이즈 S (선택)
--
-- -- 11. orders
-- INSERT INTO orders (id, store_id, payment_method, total_price, is_to_go, created_at, updated_at) VALUES
--                                                                                                      (1, 1, 'CARD', 9000, true, NOW(), NOW()),
--                                                                                                      (2, 1, 'CASH', 4500, false, NOW(), NOW());
--
-- -- 12. order_item
-- INSERT INTO order_item (id, menu_id, order_id, price, created_at, updated_at) VALUES
--                                                                                   (1, 1, 1, 4000, NOW(), NOW()),
--                                                                                   (2, 2, 2, 4500, NOW(), NOW());
--
-- -- 13. order_item_option
-- INSERT INTO order_item_option (id, order_item_id, option_detail_id, price, created_at, updated_at) VALUES
--                                                                                                        (1, 1, 2, 500, NOW(), NOW()),
--                                                                                                        (2, 2, 1, 0, NOW(), NOW());
--
-- -- 14. payment
-- INSERT INTO payment (id, store_id, order_id, payment_method, amount, status, reason, tid, cid, created_at, updated_at) VALUES
--                                                                                                                            (1, 1, 1, 'CARD', 9000, 'SUCCESS', NULL, 'TID123', 'CID123', NOW(), NOW()),
--                                                                                                                            (2, 1, 2, 'CASH', 4500, 'SUCCESS', NULL, 'TID456', 'CID456', NOW(), NOW());

-- 15. nutrition_template
INSERT INTO nutrition_template (id, name_kr, name_en, unit_type, created_at, updated_at) VALUES
                                                                                             (1, '칼로리', 'calories', 'kcal', NOW(), NOW()),
                                                                                             (2, '단백질', 'protein', 'g', NOW(), NOW());

-- 16. nutrition_value
INSERT INTO nutrition_value (id, store_id, menu_id, nutrition_id, value, status, created_at, updated_at) VALUES
                                                                                                             (1, 1, 1, 1, 5.5, 'REGISTERED', NOW(), NOW()),
                                                                                                             (2, 1, 1, 2, 0.2, 'REGISTERED', NOW(), NOW());

-- 17. kiosk_session
INSERT INTO kiosk_session (id, store_id, account_id, start_order_number, name, is_active, created_at, updated_at, started_at) VALUES
    (1, 1, 2, 'A', '키오스크 A', true, NOW(),NOW(),NOW());

-- 키오스크 B 추가
INSERT INTO kiosk_session (id, store_id, account_id, start_order_number, name, is_active, created_at, updated_at, started_at)
VALUES (2, 1, 2, 'B', '키오스크 B', false, NOW(), NOW(), NOW());

-- 키오스크 C 추가
INSERT INTO kiosk_session (id, store_id, account_id, start_order_number, name, is_active, created_at, updated_at, started_at)
VALUES (3, 1, 2, 'C', '키오스크 C', false, NOW(), NOW(), NOW());

use mylio;

-- Store 데이터
INSERT INTO store (id,name, address, status, created_at, updated_at)
VALUES
    (3,'메가커피 강남점', '서울 강남구 역삼동 123-45', 'REGISTERED', NOW(), NOW()),
    (4,'메가커피 판교점', '경기 성남시 분당구 판교로 256', 'REGISTERED', NOW(), NOW()),
    (5,'메가커피 홍대점', '서울 마포구 와우산로 123', 'REGISTERED', NOW(), NOW());

-- Category 데이터
INSERT INTO category (store_id, name_kr, name_en, status, created_at, updated_at)
VALUES
    (3, '커피', 'Coffee', 'REGISTERED', NOW(), NOW()),
    (3, '음료', 'Beverage', 'REGISTERED', NOW(), NOW()),
    (3, '디저트', 'Dessert', 'REGISTERED', NOW(), NOW()),
    (3, '프라페', 'Frappe', 'REGISTERED', NOW(), NOW()),
    (3, '스무디', 'Smoothie', 'REGISTERED', NOW(), NOW());


-- 기본 계정 생성 (관리자 및 키오스크)
INSERT INTO account (store_id, email, username, password, role, status, created_at, updated_at)
VALUES
    (3, 'admin@megacoffee.com', '관리자', '$2a$10$kJJYLA3v7N6hxuGJ49IDz.ZdLTa0Dk2okd.iNUUPXVzKy17cm9XB6', 'SUPER', 'REGISTERED', NOW(), NOW());


-- 영양성분 템플릿 데이터
INSERT INTO nutrition_template (name_kr, name_en, unit_type, created_at, updated_at)
VALUES
    ('열량', 'Calories', 'kcal', NOW(), NOW()),
    ('탄수화물', 'Carbohydrate', 'g', NOW(), NOW()),
    ('당류', 'Sugar', 'g', NOW(), NOW()),
    ('단백질', 'Protein', 'g', NOW(), NOW()),
    ('지방', 'Fat', 'g', NOW(), NOW()),
    ('포화지방', 'Saturated Fat', 'g', NOW(), NOW()),
    ('트랜스지방', 'Trans Fat', 'g', NOW(), NOW()),
    ('콜레스테롤', 'Cholesterol', 'mg', NOW(), NOW()),
    ('나트륨', 'Sodium', 'mg', NOW(), NOW()),
    ('카페인', 'Caffeine', 'mg', NOW(), NOW());

-- 원재료 템플릿 데이터
INSERT INTO ingredient_template (name_kr, name_en, status, created_at, updated_at)
VALUES
    ('에스프레소', 'Espresso', 'REGISTERED', NOW(), NOW()),
    ('우유', 'Milk', 'REGISTERED', NOW(), NOW()),
    ('생크림', 'Whipped Cream', 'REGISTERED', NOW(), NOW()),
    ('초콜릿 시럽', 'Chocolate Syrup', 'REGISTERED', NOW(), NOW()),
    ('바닐라 시럽', 'Vanilla Syrup', 'REGISTERED', NOW(), NOW()),
    ('카라멜 시럽', 'Caramel Syrup', 'REGISTERED', NOW(), NOW()),
    ('헤이즐넛 시럽', 'Hazelnut Syrup', 'REGISTERED', NOW(), NOW()),
    ('알mond 시럽', 'Almond Syrup', 'REGISTERED', NOW(), NOW()),
    ('녹차 파우더', 'Green Tea Powder', 'REGISTERED', NOW(), NOW()),
    ('자몽 주스', 'Grapefruit Juice', 'REGISTERED', NOW(), NOW()),
    ('오렌지 주스', 'Orange Juice', 'REGISTERED', NOW(), NOW()),
    ('딸기 시럽', 'Strawberry Syrup', 'REGISTERED', NOW(), NOW()),
    ('블루베리', 'Blueberry', 'REGISTERED', NOW(), NOW()),
    ('망고', 'Mango', 'REGISTERED', NOW(), NOW()),
    ('바나나', 'Banana', 'REGISTERED', NOW(), NOW()),
    ('요거트 파우더', 'Yogurt Powder', 'REGISTERED', NOW(), NOW()),
    ('얼음', 'Ice', 'REGISTERED', NOW(), NOW()),
    ('복숭아 티백', 'Peach Tea Bag', 'REGISTERED', NOW(), NOW()),
    ('레몬', 'Lemon', 'REGISTERED', NOW(), NOW()),
    ('코코넛 시럽', 'Coconut Syrup', 'REGISTERED', NOW(), NOW()),
    ('초콜릿 칩', 'Chocolate Chip', 'REGISTERED', NOW(), NOW()),
    ('쿠키 크럼블', 'Cookie Crumble', 'REGISTERED', NOW(), NOW()),
    ('커피 원두', 'Coffee Bean', 'REGISTERED', NOW(), NOW());

-- 메뉴 데이터
INSERT INTO menu (store_id, category_id, name_kr, name_en, description, price, image_url, status, created_at, updated_at)
VALUES
-- 커피 카테고리
(3, 1, '아메리카노', 'Americano', '진한 에스프레소에 물을 더해 깔끔한 맛의 아메리카노', 1500, 'americano.jpg', 'SELLING', NOW(), NOW()),
(3, 1, '카페라떼', 'Cafe Latte', '진한 에스프레소와 부드러운 우유가 어우러진 라떼', 2500, 'cafelatte.jpg', 'SELLING', NOW(), NOW()),
(3, 1, '바닐라 라떼', 'Vanilla Latte', '바닐라 시럽이 달콤하게 어우러진 라떼', 3000, 'vanillalatte.jpg', 'SELLING', NOW(), NOW()),
(3, 1, '카라멜 마끼아또', 'Caramel Macchiato', '바닐라 시럽과 카라멜 소스의 달콤한 조화', 3500, 'caramelmacchiato.jpg', 'SELLING', NOW(), NOW()),
(3, 1, '카페모카', 'Cafe Mocha', '초콜릿과 에스프레소의 절묘한 조화', 3500, 'cafemocha.jpg', 'SELLING', NOW(), NOW()),

-- 음료 카테고리
(3, 2, '딸기 스무디', 'Strawberry Smoothie', '새콤달콤한 딸기 스무디', 3500, 'strawberrysmoothie.jpg', 'SELLING', NOW(), NOW()),
(3, 2, '블루베리 요거트 스무디', 'Blueberry Yogurt Smoothie', '새콤달콤한 블루베리와 요거트의 만남', 3800, 'blueberryyogurtsmoothie.jpg', 'SELLING', NOW(), NOW()),
(3, 2, '자몽 에이드', 'Grapefruit Ade', '상큼한 자몽 에이드', 3300, 'grapefruitade.jpg', 'SELLING', NOW(), NOW()),
(3, 2, '레몬 에이드', 'Lemon Ade', '상큼한 레몬 에이드', 3300, 'lemonade.jpg', 'SELLING', NOW(), NOW()),

-- 디저트 카테고리
(3, 3, '티라미수', 'Tiramisu', '부드러운 마스카포네 치즈와 에스프레소의 풍미', 4500, 'tiramisu.jpg', 'SELLING', NOW(), NOW()),
(3, 3, '초코 브라우니', 'Chocolate Brownie', '진한 초콜릿 브라우니', 3800, 'chocobrownie.jpg', 'SELLING', NOW(), NOW()),
(3, 3, '치즈 케이크', 'Cheese Cake', '부드러운 치즈 케이크', 4200, 'cheesecake.jpg', 'SELLING', NOW(), NOW()),

-- 프라페 카테고리
(3, 4, '쿠키 프라페', 'Cookie Frappe', '바삭한 쿠키가 들어간 프라페', 4000, 'cookiefrappe.jpg', 'SELLING', NOW(), NOW()),
(3, 4, '초코 프라페', 'Chocolate Frappe', '진한 초콜릿 맛의 프라페', 4000, 'chocofrappe.jpg', 'SELLING', NOW(), NOW()),
(3, 4, '카라멜 프라페', 'Caramel Frappe', '달콤한 카라멜 맛의 프라페', 4000, 'caramelfrappe.jpg', 'SELLING', NOW(), NOW());

-- 옵션 데이터
INSERT INTO options (store_id, option_name_kr, option_name_en, status, created_at, updated_at)
VALUES
    (3, '온도', 'Temperature', 'REGISTERED', NOW(), NOW()),
    (3, '얼음량', 'Ice Amount', 'REGISTERED', NOW(), NOW()),
    (3, '당도', 'Sweetness', 'REGISTERED', NOW(), NOW()),
    (3, '샷 추가', 'Extra Shot', 'REGISTERED', NOW(), NOW()),
    (3, '시럽 추가', 'Extra Syrup', 'REGISTERED', NOW(), NOW()),
    (3, '휘핑크림', 'Whipped Cream', 'REGISTERED', NOW(), NOW()),
    (3, '우유 변경', 'Milk Change', 'REGISTERED', NOW(), NOW());

-- 옵션 상세 데이터
INSERT INTO option_detail (option_id, value, additional_price, status, created_at, updated_at)
VALUES
-- 온도 옵션
(1, 'HOT', 0, 'REGISTERED', NOW(), NOW()),
(1, 'ICE', 0, 'REGISTERED', NOW(), NOW()),

-- 얼음량 옵션
(2, '얼음 없음', 0, 'REGISTERED', NOW(), NOW()),
(2, '얼음 적게', 0, 'REGISTERED', NOW(), NOW()),
(2, '얼음 보통', 0, 'REGISTERED', NOW(), NOW()),
(2, '얼음 많이', 0, 'REGISTERED', NOW(), NOW()),

-- 당도 옵션
(3, '당도 0%', 0, 'REGISTERED', NOW(), NOW()),
(3, '당도 30%', 0, 'REGISTERED', NOW(), NOW()),
(3, '당도 50%', 0, 'REGISTERED', NOW(), NOW()),
(3, '당도 70%', 0, 'REGISTERED', NOW(), NOW()),
(3, '당도 100%', 0, 'REGISTERED', NOW(), NOW()),

-- 샷 추가 옵션
(4, '샷 추가 없음', 0, 'REGISTERED', NOW(), NOW()),
(4, '샷 1개 추가', 500, 'REGISTERED', NOW(), NOW()),
(4, '샷 2개 추가', 1000, 'REGISTERED', NOW(), NOW()),

-- 시럽 추가 옵션
(5, '시럽 추가 없음', 0, 'REGISTERED', NOW(), NOW()),
(5, '바닐라 시럽 추가', 300, 'REGISTERED', NOW(), NOW()),
(5, '카라멜 시럽 추가', 300, 'REGISTERED', NOW(), NOW()),
(5, '헤이즐넛 시럽 추가', 300, 'REGISTERED', NOW(), NOW()),

-- 휘핑크림 옵션
(6, '휘핑크림 없음', 0, 'REGISTERED', NOW(), NOW()),
(6, '휘핑크림 추가', 500, 'REGISTERED', NOW(), NOW()),

-- 우유 변경 옵션
(7, '일반 우유', 0, 'REGISTERED', NOW(), NOW()),
(7, '저지방 우유', 500, 'REGISTERED', NOW(), NOW()),
(7, '두유', 500, 'REGISTERED', NOW(), NOW()),
(7, '오트 우유', 700, 'REGISTERED', NOW(), NOW());


-- 메뉴-옵션 매핑 (전체 메뉴)
INSERT INTO menu_option_map (menu_id, option_id, option_detail_id, is_required, created_at, updated_at)
VALUES
-- 1. 아메리카노 옵션
(1, 1, 1, TRUE, NOW(), NOW()),  -- 아메리카노 - HOT 옵션
(1, 1, 2, TRUE, NOW(), NOW()),  -- 아메리카노 - ICE 옵션
(1, 2, 3, FALSE, NOW(), NOW()), -- 아메리카노 - 얼음 없음
(1, 2, 4, FALSE, NOW(), NOW()), -- 아메리카노 - 얼음 적게
(1, 2, 5, FALSE, NOW(), NOW()), -- 아메리카노 - 얼음 보통
(1, 2, 6, FALSE, NOW(), NOW()), -- 아메리카노 - 얼음 많이
(1, 4, 12, FALSE, NOW(), NOW()), -- 아메리카노 - 샷 추가 없음
(1, 4, 13, FALSE, NOW(), NOW()), -- 아메리카노 - 샷 1개 추가
(1, 4, 14, FALSE, NOW(), NOW()), -- 아메리카노 - 샷 2개 추가

-- 2. 카페라떼 옵션
(2, 1, 1, TRUE, NOW(), NOW()),  -- 카페라떼 - HOT 옵션
(2, 1, 2, TRUE, NOW(), NOW()),  -- 카페라떼 - ICE 옵션
(2, 2, 3, FALSE, NOW(), NOW()), -- 카페라떼 - 얼음 없음
(2, 2, 4, FALSE, NOW(), NOW()), -- 카페라떼 - 얼음 적게
(2, 2, 5, FALSE, NOW(), NOW()), -- 카페라떼 - 얼음 보통
(2, 2, 6, FALSE, NOW(), NOW()), -- 카페라떼 - 얼음 많이
(2, 4, 12, FALSE, NOW(), NOW()), -- 카페라떼 - 샷 추가 없음
(2, 4, 13, FALSE, NOW(), NOW()), -- 카페라떼 - 샷 1개 추가
(2, 4, 14, FALSE, NOW(), NOW()), -- 카페라떼 - 샷 2개 추가
(2, 7, 21, FALSE, NOW(), NOW()), -- 카페라떼 - 일반 우유
(2, 7, 22, FALSE, NOW(), NOW()), -- 카페라떼 - 저지방 우유
(2, 7, 23, FALSE, NOW(), NOW()), -- 카페라떼 - 두유
(2, 7, 24, FALSE, NOW(), NOW()), -- 카페라떼 - 오트 우유

-- 3. 바닐라 라떼 옵션
(3, 1, 1, TRUE, NOW(), NOW()),  -- 바닐라 라떼 - HOT 옵션
(3, 1, 2, TRUE, NOW(), NOW()),  -- 바닐라 라떼 - ICE 옵션
(3, 2, 3, FALSE, NOW(), NOW()), -- 바닐라 라떼 - 얼음 없음
(3, 2, 4, FALSE, NOW(), NOW()), -- 바닐라 라떼 - 얼음 적게
(3, 2, 5, FALSE, NOW(), NOW()), -- 바닐라 라떼 - 얼음 보통
(3, 2, 6, FALSE, NOW(), NOW()), -- 바닐라 라떼 - 얼음 많이
(3, 3, 7, FALSE, NOW(), NOW()),  -- 바닐라 라떼 - 당도 0%
(3, 3, 8, FALSE, NOW(), NOW()),  -- 바닐라 라떼 - 당도 30%
(3, 3, 9, FALSE, NOW(), NOW()),  -- 바닐라 라떼 - 당도 50%
(3, 3, 10, FALSE, NOW(), NOW()), -- 바닐라 라떼 - 당도 70%
(3, 3, 11, FALSE, NOW(), NOW()), -- 바닐라 라떼 - 당도 100%
(3, 4, 12, FALSE, NOW(), NOW()), -- 바닐라 라떼 - 샷 추가 없음
(3, 4, 13, FALSE, NOW(), NOW()), -- 바닐라 라떼 - 샷 1개 추가
(3, 4, 14, FALSE, NOW(), NOW()), -- 바닐라 라떼 - 샷 2개 추가
(3, 7, 21, FALSE, NOW(), NOW()), -- 바닐라 라떼 - 일반 우유
(3, 7, 22, FALSE, NOW(), NOW()), -- 바닐라 라떼 - 저지방 우유
(3, 7, 23, FALSE, NOW(), NOW()), -- 바닐라 라떼 - 두유
(3, 7, 24, FALSE, NOW(), NOW()), -- 바닐라 라떼 - 오트 우유

-- 4. 카라멜 마끼아또 옵션
(4, 1, 1, TRUE, NOW(), NOW()),  -- 카라멜 마끼아또 - HOT 옵션
(4, 1, 2, TRUE, NOW(), NOW()),  -- 카라멜 마끼아또 - ICE 옵션
(4, 2, 3, FALSE, NOW(), NOW()), -- 카라멜 마끼아또 - 얼음 없음
(4, 2, 4, FALSE, NOW(), NOW()), -- 카라멜 마끼아또 - 얼음 적게
(4, 2, 5, FALSE, NOW(), NOW()), -- 카라멜 마끼아또 - 얼음 보통
(4, 2, 6, FALSE, NOW(), NOW()), -- 카라멜 마끼아또 - 얼음 많이
(4, 3, 7, FALSE, NOW(), NOW()),  -- 카라멜 마끼아또 - 당도 0%
(4, 3, 8, FALSE, NOW(), NOW()),  -- 카라멜 마끼아또 - 당도 30%
(4, 3, 9, FALSE, NOW(), NOW()),  -- 카라멜 마끼아또 - 당도 50%
(4, 3, 10, FALSE, NOW(), NOW()), -- 카라멜 마끼아또 - 당도 70%
(4, 3, 11, FALSE, NOW(), NOW()), -- 카라멜 마끼아또 - 당도 100%
(4, 4, 12, FALSE, NOW(), NOW()), -- 카라멜 마끼아또 - 샷 추가 없음
(4, 4, 13, FALSE, NOW(), NOW()), -- 카라멜 마끼아또 - 샷 1개 추가
(4, 4, 14, FALSE, NOW(), NOW()), -- 카라멜 마끼아또 - 샷 2개 추가
(4, 6, 19, FALSE, NOW(), NOW()), -- 카라멜 마끼아또 - 휘핑크림 없음
(4, 6, 20, FALSE, NOW(), NOW()), -- 카라멜 마끼아또 - 휘핑크림 추가
(4, 7, 21, FALSE, NOW(), NOW()), -- 카라멜 마끼아또 - 일반 우유
(4, 7, 22, FALSE, NOW(), NOW()), -- 카라멜 마끼아또 - 저지방 우유
(4, 7, 23, FALSE, NOW(), NOW()), -- 카라멜 마끼아또 - 두유
(4, 7, 24, FALSE, NOW(), NOW()), -- 카라멜 마끼아또 - 오트 우유

-- 5. 카페모카 옵션
(5, 1, 1, TRUE, NOW(), NOW()),  -- 카페모카 - HOT 옵션
(5, 1, 2, TRUE, NOW(), NOW()),  -- 카페모카 - ICE 옵션
(5, 2, 3, FALSE, NOW(), NOW()), -- 카페모카 - 얼음 없음
(5, 2, 4, FALSE, NOW(), NOW()), -- 카페모카 - 얼음 적게
(5, 2, 5, FALSE, NOW(), NOW()), -- 카페모카 - 얼음 보통
(5, 2, 6, FALSE, NOW(), NOW()), -- 카페모카 - 얼음 많이
(5, 3, 7, FALSE, NOW(), NOW()),  -- 카페모카 - 당도 0%
(5, 3, 8, FALSE, NOW(), NOW()),  -- 카페모카 - 당도 30%
(5, 3, 9, FALSE, NOW(), NOW()),  -- 카페모카 - 당도 50%
(5, 3, 10, FALSE, NOW(), NOW()), -- 카페모카 - 당도 70%
(5, 3, 11, FALSE, NOW(), NOW()), -- 카페모카 - 당도 100%
(5, 4, 12, FALSE, NOW(), NOW()), -- 카페모카 - 샷 추가 없음
(5, 4, 13, FALSE, NOW(), NOW()), -- 카페모카 - 샷 1개 추가
(5, 4, 14, FALSE, NOW(), NOW()), -- 카페모카 - 샷 2개 추가
(5, 6, 19, FALSE, NOW(), NOW()), -- 카페모카 - 휘핑크림 없음
(5, 6, 20, FALSE, NOW(), NOW()), -- 카페모카 - 휘핑크림 추가
(5, 7, 21, FALSE, NOW(), NOW()), -- 카페모카 - 일반 우유
(5, 7, 22, FALSE, NOW(), NOW()), -- 카페모카 - 저지방 우유
(5, 7, 23, FALSE, NOW(), NOW()), -- 카페모카 - 두유
(5, 7, 24, FALSE, NOW(), NOW()), -- 카페모카 - 오트 우유

-- 6. 딸기 스무디 옵션
(6, 3, 7, FALSE, NOW(), NOW()),  -- 딸기 스무디 - 당도 0%
(6, 3, 8, FALSE, NOW(), NOW()),  -- 딸기 스무디 - 당도 30%
(6, 3, 9, FALSE, NOW(), NOW()),  -- 딸기 스무디 - 당도 50%
(6, 3, 10, FALSE, NOW(), NOW()), -- 딸기 스무디 - 당도 70%
(6, 3, 11, FALSE, NOW(), NOW()), -- 딸기 스무디 - 당도 100%
(6, 6, 19, FALSE, NOW(), NOW()), -- 딸기 스무디 - 휘핑크림 없음
(6, 6, 20, FALSE, NOW(), NOW()), -- 딸기 스무디 - 휘핑크림 추가

-- 7. 블루베리 요거트 스무디 옵션
(7, 3, 7, FALSE, NOW(), NOW()),  -- 블루베리 요거트 스무디 - 당도 0%
(7, 3, 8, FALSE, NOW(), NOW()),  -- 블루베리 요거트 스무디 - 당도 30%
(7, 3, 9, FALSE, NOW(), NOW()),  -- 블루베리 요거트 스무디 - 당도 50%
(7, 3, 10, FALSE, NOW(), NOW()), -- 블루베리 요거트 스무디 - 당도 70%
(7, 3, 11, FALSE, NOW(), NOW()), -- 블루베리 요거트 스무디 - 당도 100%
(7, 6, 19, FALSE, NOW(), NOW()), -- 블루베리 요거트 스무디 - 휘핑크림 없음
(7, 6, 20, FALSE, NOW(), NOW()), -- 블루베리 요거트 스무디 - 휘핑크림 추가

-- 8. 자몽 에이드 옵션
(8, 2, 3, FALSE, NOW(), NOW()), -- 자몽 에이드 - 얼음 없음
(8, 2, 4, FALSE, NOW(), NOW()), -- 자몽 에이드 - 얼음 적게
(8, 2, 5, FALSE, NOW(), NOW()), -- 자몽 에이드 - 얼음 보통
(8, 2, 6, FALSE, NOW(), NOW()), -- 자몽 에이드 - 얼음 많이
(8, 3, 7, FALSE, NOW(), NOW()),  -- 자몽 에이드 - 당도 0%
(8, 3, 8, FALSE, NOW(), NOW()),  -- 자몽 에이드 - 당도 30%
(8, 3, 9, FALSE, NOW(), NOW()),  -- 자몽 에이드 - 당도 50%
(8, 3, 10, FALSE, NOW(), NOW()), -- 자몽 에이드 - 당도 70%
(8, 3, 11, FALSE, NOW(), NOW()), -- 자몽 에이드 - 당도 100%

-- 9. 레몬 에이드 옵션
(9, 2, 3, FALSE, NOW(), NOW()), -- 레몬 에이드 - 얼음 없음
(9, 2, 4, FALSE, NOW(), NOW()), -- 레몬 에이드 - 얼음 적게
(9, 2, 5, FALSE, NOW(), NOW()), -- 레몬 에이드 - 얼음 보통
(9, 2, 6, FALSE, NOW(), NOW()), -- 레몬 에이드 - 얼음 많이
(9, 3, 7, FALSE, NOW(), NOW()),  -- 레몬 에이드 - 당도 0%
(9, 3, 8, FALSE, NOW(), NOW()),  -- 레몬 에이드 - 당도 30%
(9, 3, 9, FALSE, NOW(), NOW()),  -- 레몬 에이드 - 당도 50%
(9, 3, 10, FALSE, NOW(), NOW()), -- 레몬 에이드 - 당도 70%
(9, 3, 11, FALSE, NOW(), NOW()), -- 레몬 에이드 - 당도 100%

-- 13. 쿠키 프라페 옵션
(13, 3, 7, FALSE, NOW(), NOW()),  -- 쿠키 프라페 - 당도 0%
(13, 3, 8, FALSE, NOW(), NOW()),  -- 쿠키 프라페 - 당도 30%
(13, 3, 9, FALSE, NOW(), NOW()),  -- 쿠키 프라페 - 당도 50%
(13, 3, 10, FALSE, NOW(), NOW()), -- 쿠키 프라페 - 당도 70%
(13, 3, 11, FALSE, NOW(), NOW()), -- 쿠키 프라페 - 당도 100%
(13, 6, 19, FALSE, NOW(), NOW()), -- 쿠키 프라페 - 휘핑크림 없음
(13, 6, 20, FALSE, NOW(), NOW()), -- 쿠키 프라페 - 휘핑크림 추가

-- 14. 초코 프라페 옵션
(14, 3, 7, FALSE, NOW(), NOW()),  -- 초코 프라페 - 당도 0%
(14, 3, 8, FALSE, NOW(), NOW()),  -- 초코 프라페 - 당도 30%
(14, 3, 9, FALSE, NOW(), NOW()),  -- 초코 프라페 - 당도 50%
(14, 3, 10, FALSE, NOW(), NOW()), -- 초코 프라페 - 당도 70%
(14, 3, 11, FALSE, NOW(), NOW()), -- 초코 프라페 - 당도 100%
(14, 6, 19, FALSE, NOW(), NOW()), -- 초코 프라페 - 휘핑크림 없음
(14, 6, 20, FALSE, NOW(), NOW()), -- 초코 프라페 - 휘핑크림 추가

-- 15. 카라멜 프라페 옵션
(15, 3, 7, FALSE, NOW(), NOW()),  -- 카라멜 프라페 - 당도 0%
(15, 3, 8, FALSE, NOW(), NOW()),  -- 카라멜 프라페 - 당도 30%
(15, 3, 9, FALSE, NOW(), NOW()),  -- 카라멜 프라페 - 당도 50%
(15, 3, 10, FALSE, NOW(), NOW()), -- 카라멜 프라페 - 당도 70%
(15, 3, 11, FALSE, NOW(), NOW()), -- 카라멜 프라페 - 당도 100%
(15, 6, 19, FALSE, NOW(), NOW()), -- 카라멜 프라페 - 휘핑크림 없음
(15, 6, 20, FALSE, NOW(), NOW()); -- 카라멜 프라페 - 휘핑크림 추가


-- 메뉴-원재료 매핑 (전체 메뉴)
INSERT INTO menu_ingredient (menu_id, ingredient_id, store_id, created_at, updated_at)
VALUES
-- 1. 아메리카노 원재료
(1, 1, 1, NOW(), NOW()),  -- 아메리카노 - 에스프레소
(1, 17, 1, NOW(), NOW()), -- 아메리카노 - 얼음 (ICE일 경우)

-- 2. 카페라떼 원재료
(2, 1, 1, NOW(), NOW()),  -- 카페라떼 - 에스프레소
(2, 2, 1, NOW(), NOW()),  -- 카페라떼 - 우유
(2, 17, 1, NOW(), NOW()), -- 카페라떼 - 얼음 (ICE일 경우)

-- 3. 바닐라 라떼 원재료
(3, 1, 1, NOW(), NOW()),  -- 바닐라 라떼 - 에스프레소
(3, 2, 1, NOW(), NOW()),  -- 바닐라 라떼 - 우유
(3, 5, 1, NOW(), NOW()),  -- 바닐라 라떼 - 바닐라 시럽
(3, 17, 1, NOW(), NOW()), -- 바닐라 라떼 - 얼음 (ICE일 경우)

-- 4. 카라멜 마끼아또 원재료
(4, 1, 1, NOW(), NOW()),  -- 카라멜 마끼아또 - 에스프레소
(4, 2, 1, NOW(), NOW()),  -- 카라멜 마끼아또 - 우유
(4, 5, 1, NOW(), NOW()),  -- 카라멜 마끼아또 - 바닐라 시럽
(4, 6, 1, NOW(), NOW()),  -- 카라멜 마끼아또 - 카라멜 시럽
(4, 3, 1, NOW(), NOW()),  -- 카라멜 마끼아또 - 생크림
(4, 17, 1, NOW(), NOW()), -- 카라멜 마끼아또 - 얼음 (ICE일 경우)

-- 5. 카페모카 원재료
(5, 1, 1, NOW(), NOW()),  -- 카페모카 - 에스프레소
(5, 2, 1, NOW(), NOW()),  -- 카페모카 - 우유
(5, 4, 1, NOW(), NOW()),  -- 카페모카 - 초콜릿 시럽
(5, 3, 1, NOW(), NOW()),  -- 카페모카 - 생크림
(5, 17, 1, NOW(), NOW()), -- 카페모카 - 얼음 (ICE일 경우)

-- 6. 딸기 스무디 원재료
(6, 12, 1, NOW(), NOW()), -- 딸기 스무디 - 딸기 시럽
(6, 16, 1, NOW(), NOW()), -- 딸기 스무디 - 요거트 파우더
(6, 17, 1, NOW(), NOW()), -- 딸기 스무디 - 얼음

-- 7. 블루베리 요거트 스무디 원재료
(7, 13, 1, NOW(), NOW()), -- 블루베리 요거트 스무디 - 블루베리
(7, 16, 1, NOW(), NOW()), -- 블루베리 요거트 스무디 - 요거트 파우더
(7, 17, 1, NOW(), NOW()), -- 블루베리 요거트 스무디 - 얼음

-- 8. 자몽 에이드 원재료
(8, 10, 1, NOW(), NOW()), -- 자몽 에이드 - 자몽 주스
(8, 17, 1, NOW(), NOW()), -- 자몽 에이드 - 얼음

-- 9. 레몬 에이드 원재료
(9, 19, 1, NOW(), NOW()), -- 레몬 에이드 - 레몬
(9, 17, 1, NOW(), NOW()), -- 레몬 에이드 - 얼음

-- 13. 쿠키 프라페 원재료
(13, 22, 1, NOW(), NOW()), -- 쿠키 프라페 - 쿠키 크럼블
(13, 2, 1, NOW(), NOW()),  -- 쿠키 프라페 - 우유
(13, 17, 1, NOW(), NOW()), -- 쿠키 프라페 - 얼음

-- 14. 초코 프라페 원재료
(14, 4, 1, NOW(), NOW()),  -- 초코 프라페 - 초콜릿 시럽
(14, 21, 1, NOW(), NOW()), -- 초코 프라페 - 초콜릿 칩
(14, 2, 1, NOW(), NOW()),  -- 초코 프라페 - 우유
(14, 17, 1, NOW(), NOW()), -- 초코 프라페 - 얼음

-- 15. 카라멜 프라페 원재료
(15, 6, 1, NOW(), NOW()),  -- 카라멜 프라페 - 카라멜 시럽
(15, 2, 1, NOW(), NOW()),  -- 카라멜 프라페 - 우유
(15, 17, 1, NOW(), NOW()); -- 카라멜 프라페 - 얼음


-- 메뉴-영양성분 값 (전체 메뉴)
INSERT INTO nutrition_value (menu_id, nutrition_id, store_id, value, status, created_at, updated_at)
VALUES
-- 1. 아메리카노 영양성분
(1, 1, 1, 10.0, 'REGISTERED', NOW(), NOW()),   -- 아메리카노 - 열량
(1, 2, 1, 2.0, 'REGISTERED', NOW(), NOW()),    -- 아메리카노 - 탄수화물
(1, 3, 1, 0.0, 'REGISTERED', NOW(), NOW()),    -- 아메리카노 - 당류
(1, 4, 1, 1.0, 'REGISTERED', NOW(), NOW()),    -- 아메리카노 - 단백질
(1, 5, 1, 0.0, 'REGISTERED', NOW(), NOW()),    -- 아메리카노 - 지방
(1, 9, 1, 5.0, 'REGISTERED', NOW(), NOW()),    -- 아메리카노 - 나트륨
(1, 10, 1, 75.0, 'REGISTERED', NOW(), NOW()),  -- 아메리카노 - 카페인

-- 2. 카페라떼 영양성분
(2, 1, 1, 110.0, 'REGISTERED', NOW(), NOW()),  -- 카페라떼 - 열량
(2, 2, 1, 10.0, 'REGISTERED', NOW(), NOW()),   -- 카페라떼 - 탄수화물
(2, 3, 1, 9.0, 'REGISTERED', NOW(), NOW()),    -- 카페라떼 - 당류
(2, 4, 1, 6.0, 'REGISTERED', NOW(), NOW()),    -- 카페라떼 - 단백질
(2, 5, 1, 4.0, 'REGISTERED', NOW(), NOW()),    -- 카페라떼 - 지방
(2, 9, 1, 70.0, 'REGISTERED', NOW(), NOW()),   -- 카페라떼 - 나트륨
(2, 10, 1, 75.0, 'REGISTERED', NOW(), NOW()),  -- 카페라떼 - 카페인

-- 3. 바닐라 라떼 영양성분
(3, 1, 1, 170.0, 'REGISTERED', NOW(), NOW()),  -- 바닐라 라떼 - 열량
(3, 2, 1, 27.0, 'REGISTERED', NOW(), NOW()),   -- 바닐라 라떼 - 탄수화물
(3, 3, 1, 25.0, 'REGISTERED', NOW(), NOW()),   -- 바닐라 라떼 - 당류
(3, 4, 1, 6.0, 'REGISTERED', NOW(), NOW()),    -- 바닐라 라떼 - 단백질
(3, 5, 1, 4.5, 'REGISTERED', NOW(), NOW()),    -- 바닐라 라떼 - 지방
(3, 9, 1, 120.0, 'REGISTERED', NOW(), NOW()),  -- 바닐라 라떼 - 나트륨
(3, 10, 1, 75.0, 'REGISTERED', NOW(), NOW()),  -- 바닐라 라떼 - 카페인

-- 4. 카라멜 마끼아또 영양성분
(4, 1, 1, 200.0, 'REGISTERED', NOW(), NOW()),  -- 카라멜 마끼아또 - 열량
(4, 2, 1, 32.0, 'REGISTERED', NOW(), NOW()),   -- 카라멜 마끼아또 - 탄수화물
(4, 3, 1, 29.0, 'REGISTERED', NOW(), NOW()),   -- 카라멜 마끼아또 - 당류
(4, 4, 1, 6.0, 'REGISTERED', NOW(), NOW()),    -- 카라멜 마끼아또 - 단백질
(4, 5, 1, 5.0, 'REGISTERED', NOW(), NOW()),    -- 카라멜 마끼아또 - 지방
(4, 9, 1, 150.0, 'REGISTERED', NOW(), NOW()),  -- 카라멜 마끼아또 - 나트륨
(4, 10, 1, 75.0, 'REGISTERED', NOW(), NOW()),  -- 카라멜 마끼아또 - 카페인

-- 5. 카페모카 영양성분
(5, 1, 1, 230.0, 'REGISTERED', NOW(), NOW()),  -- 카페모카 - 열량
(5, 2, 1, 28.0, 'REGISTERED', NOW(), NOW()),   -- 카페모카 - 탄수화물
(5, 3, 1, 25.0, 'REGISTERED', NOW(), NOW()),   -- 카페모카 - 당류
(5, 4, 1, 7.0, 'REGISTERED', NOW(), NOW()),    -- 카페모카 - 단백질
(5, 5, 1, 9.0, 'REGISTERED', NOW(), NOW()),    -- 카페모카 - 지방
(5, 9, 1, 130.0, 'REGISTERED', NOW(), NOW()),  -- 카페모카 - 나트륨
(5, 10, 1, 75.0, 'REGISTERED', NOW(), NOW()),  -- 카페모카 - 카페인

-- 6. 딸기 스무디 영양성분
(6, 1, 1, 280.0, 'REGISTERED', NOW(), NOW()),  -- 딸기 스무디 - 열량
(6, 2, 1, 58.0, 'REGISTERED', NOW(), NOW()),   -- 딸기 스무디 - 탄수화물
(6, 3, 1, 52.0, 'REGISTERED', NOW(), NOW()),   -- 딸기 스무디 - 당류
(6, 4, 1, 3.0, 'REGISTERED', NOW(), NOW()),    -- 딸기 스무디 - 단백질
(6, 5, 1, 2.5, 'REGISTERED', NOW(), NOW()),    -- 딸기 스무디 - 지방
(6, 9, 1, 45.0, 'REGISTERED', NOW(), NOW()),   -- 딸기 스무디 - 나트륨
(6, 10, 1, 0.0, 'REGISTERED', NOW(), NOW()),   -- 딸기 스무디 - 카페인

-- 7. 블루베리 요거트 스무디 영양성분
(7, 1, 1, 290.0, 'REGISTERED', NOW(), NOW()),  -- 블루베리 요거트 스무디 - 열량
(7, 2, 1, 55.0, 'REGISTERED', NOW(), NOW()),   -- 블루베리 요거트 스무디 - 탄수화물
(7, 3, 1, 47.0, 'REGISTERED', NOW(), NOW()),   -- 블루베리 요거트 스무디 - 당류
(7, 4, 1, 4.0, 'REGISTERED', NOW(), NOW()),    -- 블루베리 요거트 스무디 - 단백질
(7, 5, 1, 3.5, 'REGISTERED', NOW(), NOW()),    -- 블루베리 요거트 스무디 - 지방
(7, 9, 1, 55.0, 'REGISTERED', NOW(), NOW()),   -- 블루베리 요거트 스무디 - 나트륨
(7, 10, 1, 0.0, 'REGISTERED', NOW(), NOW()),   -- 블루베리 요거트 스무디 - 카페인

-- 8. 자몽 에이드 영양성분
(8, 1, 1, 150.0, 'REGISTERED', NOW(), NOW()),  -- 자몽 에이드 - 열량
(8, 2, 1, 36.0, 'REGISTERED', NOW(), NOW()),   -- 자몽 에이드 - 탄수화물
(8, 3, 1, 34.0, 'REGISTERED', NOW(), NOW()),   -- 자몽 에이드 - 당류
(8, 4, 1, 0.5, 'REGISTERED', NOW(), NOW()),    -- 자몽 에이드 - 단백질
(8, 5, 1, 0.1, 'REGISTERED', NOW(), NOW()),    -- 자몽 에이드 - 지방
(8, 9, 1, 15.0, 'REGISTERED', NOW(), NOW()),   -- 자몽 에이드 - 나트륨
(8, 10, 1, 0.0, 'REGISTERED', NOW(), NOW()),   -- 자몽 에이드 - 카페인

-- 9. 레몬 에이드 영양성분
(9, 1, 1, 140.0, 'REGISTERED', NOW(), NOW()),  -- 레몬 에이드 - 열량
(9, 2, 1, 34.0, 'REGISTERED', NOW(), NOW()),   -- 레몬 에이드 - 탄수화물
(9, 3, 1, 32.0, 'REGISTERED', NOW(), NOW()),   -- 레몬 에이드 - 당류
(9, 4, 1, 0.2, 'REGISTERED', NOW(), NOW()),    -- 레몬 에이드 - 단백질
(9, 5, 1, 0.1, 'REGISTERED', NOW(), NOW()),    -- 레몬 에이드 - 지방
(9, 9, 1, 10.0, 'REGISTERED', NOW(), NOW()),   -- 레몬 에이드 - 나트륨
(9, 10, 1, 0.0, 'REGISTERED', NOW(), NOW()),   -- 레몬 에이드 - 카페인

-- 10. 티라미수 영양성분
(10, 1, 1, 320.0, 'REGISTERED', NOW(), NOW()), -- 티라미수 - 열량
(10, 2, 1, 28.0, 'REGISTERED', NOW(), NOW()),  -- 티라미수 - 탄수화물
(10, 3, 1, 18.0, 'REGISTERED', NOW(), NOW()),  -- 티라미수 - 당류
(10, 4, 1, 6.0, 'REGISTERED', NOW(), NOW()),   -- 티라미수 - 단백질
(10, 5, 1, 20.0, 'REGISTERED', NOW(), NOW()),  -- 티라미수 - 지방
(10, 6, 1, 12.0, 'REGISTERED', NOW(), NOW()),  -- 티라미수 - 포화지방
(10, 8, 1, 65.0, 'REGISTERED', NOW(), NOW()),  -- 티라미수 - 콜레스테롤
(10, 9, 1, 120.0, 'REGISTERED', NOW(), NOW()), -- 티라미수 - 나트륨
(10, 10, 1, 10.0, 'REGISTERED', NOW(), NOW()), -- 티라미수 - 카페인

-- 11. 초코 브라우니 영양성분
(11, 1, 1, 380.0, 'REGISTERED', NOW(), NOW()), -- 초코 브라우니 - 열량
(11, 2, 1, 48.0, 'REGISTERED', NOW(), NOW()),  -- 초코 브라우니 - 탄수화물
(11, 3, 1, 32.0, 'REGISTERED', NOW(), NOW()),  -- 초코 브라우니 - 당류
(11, 4, 1, 5.0, 'REGISTERED', NOW(), NOW()),   -- 초코 브라우니 - 단백질
(11, 5, 1, 22.0, 'REGISTERED', NOW(), NOW()),  -- 초코 브라우니 - 지방
(11, 6, 1, 14.0, 'REGISTERED', NOW(), NOW()),  -- 초코 브라우니 - 포화지방
(11, 8, 1, 80.0, 'REGISTERED', NOW(), NOW()),  -- 초코 브라우니 - 콜레스테롤
(11, 9, 1, 220.0, 'REGISTERED', NOW(), NOW()), -- 초코 브라우니 - 나트륨
(11, 10, 1, 5.0, 'REGISTERED', NOW(), NOW()),  -- 초코 브라우니 - 카페인

-- 12. 치즈 케이크 영양성분
(12, 1, 1, 350.0, 'REGISTERED', NOW(), NOW()), -- 치즈 케이크 - 열량
(12, 2, 1, 30.0, 'REGISTERED', NOW(), NOW()),  -- 치즈 케이크 - 탄수화물
(12, 3, 1, 22.0, 'REGISTERED', NOW(), NOW()),  -- 치즈 케이크 - 당류
(12, 4, 1, 7.0, 'REGISTERED', NOW(), NOW()),   -- 치즈 케이크 - 단백질
(12, 5, 1, 24.0, 'REGISTERED', NOW(), NOW()),  -- 치즈 케이크 - 지방
(12, 6, 1, 15.0, 'REGISTERED', NOW(), NOW()),  -- 치즈 케이크 - 포화지방
(12, 8, 1, 110.0, 'REGISTERED', NOW(), NOW()), -- 치즈 케이크 - 콜레스테롤
(12, 9, 1, 230.0, 'REGISTERED', NOW(), NOW()), -- 치즈 케이크 - 나트륨
(12, 10, 1, 0.0, 'REGISTERED', NOW(), NOW()),  -- 치즈 케이크 - 카페인

-- 13. 쿠키 프라페 영양성분
(13, 1, 1, 410.0, 'REGISTERED', NOW(), NOW()), -- 쿠키 프라페 - 열량
(13, 2, 1, 70.0, 'REGISTERED', NOW(), NOW()),  -- 쿠키 프라페 - 탄수화물
(13, 3, 1, 58.0, 'REGISTERED', NOW(), NOW()),  -- 쿠키 프라페 - 당류
(13, 4, 1, 8.0, 'REGISTERED', NOW(), NOW()),   -- 쿠키 프라페 - 단백질
(13, 5, 1, 12.0, 'REGISTERED', NOW(), NOW()),  -- 쿠키 프라페 - 지방
(13, 6, 1, 7.0, 'REGISTERED', NOW(), NOW()),   -- 쿠키 프라페 - 포화지방
(13, 8, 1, 25.0, 'REGISTERED', NOW(), NOW()),  -- 쿠키 프라페 - 콜레스테롤
(13, 9, 1, 280.0, 'REGISTERED', NOW(), NOW()), -- 쿠키 프라페 - 나트륨
(13, 10, 1, 0.0, 'REGISTERED', NOW(), NOW()),  -- 쿠키 프라페 - 카페인

-- 14. 초코 프라페 영양성분
(14, 1, 1, 380.0, 'REGISTERED', NOW(), NOW()), -- 초코 프라페 - 열량
(14, 2, 1, 65.0, 'REGISTERED', NOW(), NOW()),  -- 초코 프라페 - 탄수화물
(14, 3, 1, 55.0, 'REGISTERED', NOW(), NOW()),  -- 초코 프라페 - 당류
(14, 4, 1, 7.0, 'REGISTERED', NOW(), NOW()),   -- 초코 프라페 - 단백질
(14, 5, 1, 10.0, 'REGISTERED', NOW(), NOW()),  -- 초코 프라페 - 지방
(14, 6, 1, 6.0, 'REGISTERED', NOW(), NOW()),   -- 초코 프라페 - 포화지방
(14, 8, 1, 20.0, 'REGISTERED', NOW(), NOW()),  -- 초코 프라페 - 콜레스테롤
(14, 9, 1, 150.0, 'REGISTERED', NOW(), NOW()), -- 초코 프라페 - 나트륨
(14, 10, 1, 5.0, 'REGISTERED', NOW(), NOW()),  -- 초코 프라페 - 카페인

-- 15. 카라멜 프라페 영양성분
(15, 1, 1, 400.0, 'REGISTERED', NOW(), NOW()), -- 카라멜 프라페 - 열량
(15, 2, 1, 68.0, 'REGISTERED', NOW(), NOW()),  -- 카라멜 프라페 - 탄수화물
(15, 3, 1, 62.0, 'REGISTERED', NOW(), NOW()),  -- 카라멜 프라페 - 당류
(15, 4, 1, 6.0, 'REGISTERED', NOW(), NOW()),   -- 카라멜 프라페 - 단백질
(15, 5, 1, 10.0, 'REGISTERED', NOW(), NOW()),  -- 카라멜 프라페 - 지방
(15, 6, 1, 6.0, 'REGISTERED', NOW(), NOW()),   -- 카라멜 프라페 - 포화지방
(15, 8, 1, 20.0, 'REGISTERED', NOW(), NOW()),  -- 카라멜 프라페 - 콜레스테롤
(15, 9, 1, 160.0, 'REGISTERED', NOW(), NOW()), -- 카라멜 프라페 - 나트륨
(15, 10, 1, 0.0, 'REGISTERED', NOW(), NOW());  -- 카라멜 프라페 - 카페인

-- 메뉴-태그 매핑
INSERT INTO menu_tag_map (menu_id, store_id, tag_kr, tag_en, created_at, updated_at)
VALUES
-- 1. 아메리카노 태그
(1, 3, '커피', 'Coffee', NOW(), NOW()),
(1, 3, '베스트셀러', 'Best Seller', NOW(), NOW()),

-- 2. 카페라떼 태그
(2, 3, '커피', 'Coffee', NOW(), NOW()),
(2, 3, '우유', 'Milk', NOW(), NOW()),
(2, 3, '베스트셀러', 'Best Seller', NOW(), NOW()),

-- 3. 바닐라 라떼 태그
(3, 3, '커피', 'Coffee', NOW(), NOW()),
(3, 3, '우유', 'Milk', NOW(), NOW()),
(3, 3, '달콤한', 'Sweet', NOW(), NOW()),

-- 4. 카라멜 마끼아또 태그
(4, 3, '커피', 'Coffee', NOW(), NOW()),
(4, 3, '우유', 'Milk', NOW(), NOW()),
(4, 3, '달콤한', 'Sweet', NOW(), NOW()),
(4, 3, '베스트셀러', 'Best Seller', NOW(), NOW()),

-- 5. 카페모카 태그
(5, 3, '커피', 'Coffee', NOW(), NOW()),
(5, 3, '우유', 'Milk', NOW(), NOW()),
(5, 3, '달콤한', 'Sweet', NOW(), NOW()),
(5, 3, '초콜릿', 'Chocolate', NOW(), NOW()),

-- 6. 딸기 스무디 태그
(6, 3, '스무디', 'Smoothie', NOW(), NOW()),
(6, 3, '딸기', 'Strawberry', NOW(), NOW()),
(6, 3, '달콤한', 'Sweet', NOW(), NOW()),
(6, 3, '베스트셀러', 'Best Seller', NOW(), NOW()),

-- 7. 블루베리 요거트 스무디 태그
(7, 3, '스무디', 'Smoothie', NOW(), NOW()),
(7, 3, '블루베리', 'Blueberry', NOW(), NOW()),
(7, 3, '요거트', 'Yogurt', NOW(), NOW()),

-- 8. 자몽 에이드 태그
(8, 3, '에이드', 'Ade', NOW(), NOW()),
(8, 3, '자몽', 'Grapefruit', NOW(), NOW()),
(8, 3, '상큼한', 'Refreshing', NOW(), NOW()),

-- 9. 레몬 에이드 태그
(9, 3, '에이드', 'Ade', NOW(), NOW()),
(9, 3, '레몬', 'Lemon', NOW(), NOW()),
(9, 3, '상큼한', 'Refreshing', NOW(), NOW()),

-- 10. 티라미수 태그
(10, 3, '디저트', 'Dessert', NOW(), NOW()),
(10, 3, '달콤한', 'Sweet', NOW(), NOW()),
(10, 3, '베스트셀러', 'Best Seller', NOW(), NOW()),

-- 11. 초코 브라우니 태그
(11, 3, '디저트', 'Dessert', NOW(), NOW()),
(11, 3, '초콜릿', 'Chocolate', NOW(), NOW()),
(11, 3, '달콤한', 'Sweet', NOW(), NOW()),

-- 12. 치즈 케이크 태그
(12, 3, '디저트', 'Dessert', NOW(), NOW()),
(12, 3, '치즈', 'Cheese', NOW(), NOW()),
(12, 3, '달콤한', 'Sweet', NOW(), NOW()),

-- 13. 쿠키 프라페 태그
(13, 3, '프라페', 'Frappe', NOW(), NOW()),
(13, 3, '쿠키', 'Cookie', NOW(), NOW()),
(13, 3, '달콤한', 'Sweet', NOW(), NOW()),
(13, 3, '베스트셀러', 'Best Seller', NOW(), NOW()),

-- 14. 초코 프라페 태그
(14, 3, '프라페', 'Frappe', NOW(), NOW()),
(14, 3, '초콜릿', 'Chocolate', NOW(), NOW()),
(14, 3, '달콤한', 'Sweet', NOW(), NOW()),

-- 15. 카라멜 프라페 태그
(15, 3, '프라페', 'Frappe', NOW(), NOW()),
(15, 3, '카라멜', 'Caramel', NOW(), NOW()),
(15, 3, '달콤한', 'Sweet', NOW(), NOW());
