-- Удаление существующих таблиц (если нужно начать с чистого листа)
DROP TABLE IF EXISTS excursion_in_trip, hotel_in_trip, trip, contract, tourist_group, station, city, country, hotel, excursion, route, client, "user" CASCADE;

-- Таблица пользователей (user)
CREATE TABLE "user" (
    id SERIAL PRIMARY KEY,
    login VARCHAR(25) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    role INTEGER NOT NULL DEFAULT 2, -- 1 для админа, 2 для клиента
    is_banned BOOLEAN DEFAULT FALSE
);

-- Таблица клиентов
CREATE TABLE client (
    id SERIAL PRIMARY KEY,
    user_id INTEGER UNIQUE REFERENCES "user"(id),
    phone_number VARCHAR(12),
    full_name VARCHAR(255),
    address VARCHAR(255),
    birth_date DATE
);

-- Таблица стран
CREATE TABLE country (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE
);

-- Таблица городов
CREATE TABLE city (
    id SERIAL PRIMARY KEY,
    country_id INTEGER REFERENCES country(id),
    name VARCHAR(255) NOT NULL
);

-- Таблица туров
CREATE TABLE route (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    duration INTEGER NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL
);

-- Таблица пунктов назначения
CREATE TABLE station (
    id SERIAL PRIMARY KEY,
    station_number INTEGER NOT NULL,
    route_id INTEGER REFERENCES route(id),
    duration INTEGER NOT NULL,
    city_id INTEGER REFERENCES city(id)
);

-- Таблица туристических групп
CREATE TABLE tourist_group (
    id SERIAL PRIMARY KEY,
    group_number INTEGER NOT NULL,
    travel_date DATE NOT NULL,
    route_id INTEGER REFERENCES route(id)
);

-- Таблица контрактов
CREATE TABLE contract (
    id SERIAL PRIMARY KEY,
    client_id INTEGER REFERENCES client(id),
    contract_number INTEGER NOT NULL,
    date_of_conclusion DATE NOT NULL,
    payment_method VARCHAR(50) NOT NULL
);

-- Таблица путевок
CREATE TABLE trip (
    id SERIAL PRIMARY KEY,
    trip_number INTEGER NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    group_id INTEGER REFERENCES tourist_group(id),
    client_id INTEGER REFERENCES client(id),
    contract_id INTEGER REFERENCES contract(id)
);

-- Таблица отелей
CREATE TABLE hotel (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    city_id INTEGER REFERENCES city(id)
);

-- Таблица экскурсий
CREATE TABLE excursion (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    city_id INTEGER REFERENCES city(id)
);

-- Таблица связи путевок и отелей
CREATE TABLE hotel_in_trip (
    trip_id INTEGER REFERENCES trip(id),
    hotel_id INTEGER REFERENCES hotel(id),
    PRIMARY KEY (trip_id, hotel_id)
);

-- Таблица связи путевок и экскурсий
CREATE TABLE excursion_in_trip (
    trip_id INTEGER REFERENCES trip(id),
    excursion_id INTEGER REFERENCES excursion(id),
    PRIMARY KEY (trip_id, excursion_id)
);

CREATE TABLE review (
	id serial4 NOT NULL,
	user_id int4 NULL,
	route_id int4 NULL,
	rating int4 NULL,
	"comment" text NULL,
	created_at timestamp NULL,
	CONSTRAINT review_pkey PRIMARY KEY (id),
	CONSTRAINT review_rating_check CHECK (((rating >= 1) AND (rating <= 5))),
	CONSTRAINT review_user_id_route_id_key UNIQUE (user_id, route_id)
);
