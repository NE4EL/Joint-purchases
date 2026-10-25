-- =========================================================
-- Платформа совместных покупок: SQL-запросы проекта
-- Запросы проверены в SQLite CLI на базе data/joint_purchases.sqlite.
-- =========================================================


-- ---------------------------------------------------------
-- Выборка списков объектов
-- ---------------------------------------------------------

-- 1. Список всех совместных покупок (страница /purchases/)
SELECT
    id,
    product,
    price,
    min_participants,
    max_participants
FROM purchases
ORDER BY product;

-- 2. Список всех пользователей
SELECT
    id,
    name,
    email
FROM users
ORDER BY name;


-- ---------------------------------------------------------
-- Фильтрация данных (WHERE)
-- ---------------------------------------------------------

-- 3. Покупка по идентификатору (страница /purchases/<id>/),
--    значение передаётся параметром
SELECT
    id,
    product,
    price,
    min_participants,
    max_participants
FROM purchases
WHERE id = ?;

-- 4. Подбор покупок в пределах бюджета (страница /purchases/search/),
--    максимальная цена передаётся параметром
SELECT
    id,
    product,
    price,
    max_participants
FROM purchases
WHERE price <= ?
ORDER BY price;


-- ---------------------------------------------------------
-- Соединение таблиц (JOIN)
-- ---------------------------------------------------------

-- 5. Полная информация обо всех участиях: товар и пользователь
--    (страница /participations/)
SELECT
    participations.id,
    participations.is_cancelled,
    purchases.product,
    users.name AS user_name
FROM participations
JOIN purchases ON participations.purchase_id = purchases.id
JOIN users ON participations.user_id = users.id
ORDER BY participations.id;

-- 6. Одно участие по идентификатору (страница /participations/<id>/),
--    значение передаётся параметром
SELECT
    participations.id,
    participations.is_cancelled,
    purchases.product,
    users.name AS user_name
FROM participations
JOIN purchases ON participations.purchase_id = purchases.id
JOIN users ON participations.user_id = users.id
WHERE participations.id = ?;


-- ---------------------------------------------------------
-- Агрегатные функции
-- ---------------------------------------------------------

-- 7. Число активных участий (информационный блок статистики)
SELECT COUNT(*) AS active_count
FROM participations
WHERE is_cancelled = 0;

-- 8. Минимальная, средняя и максимальная цена покупок
SELECT
    MIN(price) AS min_price,
    AVG(price) AS avg_price,
    MAX(price) AS max_price
FROM purchases;


-- ---------------------------------------------------------
-- Группировка (GROUP BY) и фильтрация групп (HAVING)
-- ---------------------------------------------------------

-- 9. Число активных участников по каждой покупке
--    (страница /participations/statistics/).
--    LEFT JOIN сохраняет покупки без участников.
SELECT
    purchases.product,
    purchases.min_participants,
    COUNT(participations.id) AS participants_count
FROM purchases
LEFT JOIN participations
    ON purchases.id = participations.purchase_id
    AND participations.is_cancelled = 0
GROUP BY purchases.id, purchases.product
ORDER BY participants_count DESC;

-- 10. Покупки, набравшие минимальное число участников
--     (фильтрация групп через HAVING)
SELECT
    purchases.product,
    purchases.min_participants,
    COUNT(participations.id) AS participants_count
FROM purchases
JOIN participations
    ON purchases.id = participations.purchase_id
    AND participations.is_cancelled = 0
GROUP BY purchases.id, purchases.product, purchases.min_participants
HAVING COUNT(participations.id) >= purchases.min_participants
ORDER BY participants_count DESC;


-- ---------------------------------------------------------
-- Дополнительный запрос с подзапросом
-- ---------------------------------------------------------

-- 11. Покупки без единого активного участника
--     (операция NOT IN исключает покупки, где уже есть участники)
SELECT
    id,
    product,
    price
FROM purchases
WHERE id NOT IN (
    SELECT purchase_id
    FROM participations
    WHERE is_cancelled = 0
)
ORDER BY product;
