-- 관리자 계정 추가
INSERT INTO `account` (id, store_id, username, password, role,created_at,updated_at,status)
VALUES
    (1, NULL, '전아현', 'qwer1234', 'SUPER',NOW(),NOW(), 'REGISTERED'),
    (2, NULL, '신지혜', 'qwer1234', 'SUPER',NOW(),NOW(), 'REGISTERED'),
    (3, NULL, '이병조', 'qwer1234', 'SUPER',NOW(),NOW(), 'REGISTERED'),
    (4, NULL, '이하영', 'qwer1234', 'SUPER',NOW(),NOW(), 'REGISTERED'),
    (5, NULL, '이해루', 'qwer1234', 'SUPER',NOW(),NOW(), 'REGISTERED'),
    (6, NULL, '강성엽', 'qwer1234', 'SUPER',NOW(),NOW(), 'REGISTERED');


INSERT INTO store (id, name, status, address, created_at, updated_at) VALUES
                                                                          (1, '싸피 다방 강남점', 'REGISTERED', '서울 강남구', NOW(), NOW()),
                                                                          (2, '싸피 다방 판교점', 'REGISTERED', '경기 성남시', NOW(), NOW());

-- 2. account
INSERT INTO account (id, store_id, username, password, role, status, created_at, updated_at) VALUES
                                                                                                 (7, 1, '강남점', 'qwer1234', 'STORE', 'REGISTERED', NOW(), NOW()),
                                                                                                 (8, 2, 'admin2', 'ssafycoffee', 'STORE', 'REGISTERED', NOW(), NOW());

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

-- 11. orders
INSERT INTO orders (id, store_id, payment_method, total_price, is_to_go, created_at, updated_at) VALUES
                                                                                                     (1, 1, 'CARD', 9000, true, NOW(), NOW()),
                                                                                                     (2, 1, 'CASH', 4500, false, NOW(), NOW());

-- 12. order_item
INSERT INTO order_item (id, menu_id, order_id, price, created_at, updated_at) VALUES
                                                                                  (1, 1, 1, 4000, NOW(), NOW()),
                                                                                  (2, 2, 2, 4500, NOW(), NOW());

-- 13. order_item_option
INSERT INTO order_item_option (id, order_item_id, option_detail_id, price, created_at, updated_at) VALUES
                                                                                                       (1, 1, 2, 500, NOW(), NOW()),
                                                                                                       (2, 2, 1, 0, NOW(), NOW());

-- 14. payment
INSERT INTO payment (id, store_id, order_id, payment_method, amount, status, reason, tid, cid, created_at, updated_at) VALUES
                                                                                                                           (1, 1, 1, 'CARD', 9000, 'SUCCESS', NULL, 'TID123', 'CID123', NOW(), NOW()),
                                                                                                                           (2, 1, 2, 'CASH', 4500, 'SUCCESS', NULL, 'TID456', 'CID456', NOW(), NOW());

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
    (1, 1, 1, 'A', '키오스크 A', true, NOW(),NOW(),NOW());