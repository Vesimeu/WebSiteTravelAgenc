-- Очистка таблиц (если нужно)
DELETE FROM excursion_in_trip;
DELETE FROM hotel_in_trip;
DELETE FROM trip;
DELETE FROM contract;
DELETE FROM tourist_group;
DELETE FROM station;
DELETE FROM hotel;
DELETE FROM excursion;
DELETE FROM route;
DELETE FROM city;
DELETE FROM country;
DELETE FROM client;
DELETE FROM "user";

-- Таблица user
INSERT INTO "user" (login, email, password, role, is_banned)
VALUES
    ('john_doe', 'john@example.com', '$2b$12$Q8z7o1z3X4Y5Z6A7B8C9D0E1F2G3H4I5J6K7L8M9N0', 2, FALSE), -- пароль: password123
    ('jane_smith', 'jane@example.com', '$2b$12$R9A0B1C2D3E4F5G6H7I8J9K0L1M2N3O4P5Q6R7S8T9', 2, FALSE), -- пароль: password456
    ('admin', 'admin@example.com', '$2b$12$U0V1W2X3Y4Z5A6B7C8D9E0F1G2H3I4J5K6L7M8N9O0', 1, FALSE), -- пароль: admin123
    ('bob_wilson', 'bob@example.com', '$2b$12$V1W2X3Y4Z5A6B7C8D9E0F1G2H3I4J5K6L7M8N9O0P1', 2, TRUE); -- пароль: password789

-- Таблица client
INSERT INTO client (user_id, phone_number, full_name, address, birth_date)
VALUES
    (1, '1234567890', 'John Doe', '123 Main St, NY', '1990-05-15'),
    (2, '0987654321', 'Jane Smith', '456 Oak Ave, CA', '1985-08-22'),
    (4, '4444444444', 'Bob Wilson', '321 Elm St, FL', '1995-03-10');

-- Таблица country
INSERT INTO country (name)
VALUES
    ('Франция'),
    ('Япония'),
    ('Италия'),
    ('Испания');

-- Таблица city
INSERT INTO city (country_id, name)
VALUES
    (1, 'Париж'),
    (1, 'Лион'),
    (2, 'Токио'),
    (2, 'Киото'),
    (3, 'Рим'),
五、(3, 'Флоренция'),
    (4, 'Мадрид'),
    (4, 'Барселона');

-- Таблица route
INSERT INTO route (name, price, duration, start_date, end_date)
VALUES
    ('Тайланд', 1500.00, 7, '2025-06-01', '2025-06-08'),
    ('Абхазия', 2000.00, 10, '2025-07-01', '2025-07-11'),
    ('Австралия', 1800.00, 8, '2025-08-01', '2025-08-09'),
    ('Испания', 1600.00, 6, '2025-09-01', '2025-09-07');

-- Таблица tourist_group
INSERT INTO tourist_group (group_number, travel_date, route_id)
VALUES
    (10001, '2025-06-01', 1), -- Тур по Франции
    (10002, '2025-07-01', 2), -- Японское приключение
    (10003, '2025-08-01', 3), -- Итальянская классика
    (10004, '2025-09-01', 4); -- Испанское путешествие

-- Таблица station
INSERT INTO station (station_number, route_id, duration, city_id)
VALUES
    (20001, 1, 3, 1), -- Париж, Тур по Франции
    (20002, 1, 2, 2), -- Лион, Тур по Франции
    (20003, 2, 4, 3), -- Токио, Японское приключение
    (20004, 2, 3, 4), -- Киото, Японское приключение
    (20005, 3, 3, 5), -- Рим, Итальянская классика
    (20006, 3, 2, 6), -- Флоренция, Итальянская классика
    (20007, 4, 3, 7), -- Мадрид, Испанское путешествие
    (20008, 4, 2, 8); -- Барселона, Испанское путешествие

-- Таблица hotel
INSERT INTO hotel (name, city_id)
VALUES
    ('Hilton Paris', 1),
    ('Mercure Lyon', 2),
    ('Tokyo Marriott', 3),
    ('Kyoto Granvia', 4),
    ('Rome Cavalieri', 5),
    ('Florentine Palace', 6),
    ('InterContinental Madrid', 7),
    ('Barcelona Princess', 8);

-- Таблица excursion
INSERT INTO excursion (name, city_id)
VALUES
    ('Экскурсия по Лувру', 1),
    ('Эйфелева башня', 1),
    ('Лионский собор', 2),
    ('Тур по храмам Киото', 4),
    ('Колизей и Римский форум', 5),
    ('Галерея Уффици', 6),
    ('Саграда Фамилия', 8),
    ('Королевский дворец Мадрида', 7);

-- Таблица contract
INSERT INTO contract (client_id, contract_number, date_of_conclusion, payment_method)
VALUES
    (1, 30001, '2025-05-01', 'Банковская карта'), -- John Doe
    (2, 30002, '2025-05-02', 'Наличные'), -- Jane Smith
    (1, 30003, '2025-05-03', 'Банковская карта'); -- John Doe

-- Таблица trip
INSERT INTO trip (trip_number, price, group_id, client_id, contract_id)
VALUES
    (40001, 1500.00, 1, 1, 1), -- John Doe, Тур по Франции
    (40002, 2000.00, 2, 2, 2), -- Jane Smith, Японское приключение
    (40003, 1800.00, 3, 1, 3); -- John Doe, Итальянская классика

-- Таблица hotel_in_trip
INSERT INTO hotel_in_trip (trip_id, hotel_id)
VALUES
    (1, 1), -- Путевка 1: Hilton Paris
    (2, 3), -- Путевка 2: Tokyo Marriott
    (3, 5); -- Путевка 3: Rome Cavalieri

-- Таблица excursion_in_trip
INSERT INTO excursion_in_trip (trip_id, excursion_id)
VALUES
    (1, 1), -- Путевка 1: Экскурсия по Лувру
    (1, 2), -- Путевка 1: Эйфелева башня
    (2, 4), -- Путевка 2: Тур по храмам Киото
    (3, 5); -- Путевка 3: Колизей и Римский форум