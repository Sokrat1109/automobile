CREATE SCHEMA IF NOT EXISTS automobile;
SET search_path TO automobile;

DROP TABLE IF EXISTS automobile.owner CASCADE;
DROP TABLE IF EXISTS automobile.auto CASCADE;
DROP TABLE IF EXISTS automobile.brand CASCADE;
DROP TABLE IF EXISTS automobile.body_type CASCADE;
DROP TABLE IF EXISTS automobile.auto_type CASCADE;
DROP TABLE IF EXISTS automobile.factory CASCADE;
DROP TABLE IF EXISTS automobile.country CASCADE;
DROP TABLE IF EXISTS automobile.hall CASCADE;

SET search_path TO automobile;



-- создание таблиц
CREATE TABLE Country (
	id serial PRIMARY KEY,
	name text NOT NULL
);

CREATE TABLE Hall (
	id serial PRIMARY KEY,
	room_number text
);

CREATE TABLE Owner (
	id serial PRIMARY KEY,
	full_name text NOT NULL,
	country_id integer
);

CREATE TABLE body_type (
	id SERIAL PRIMARY KEY,
	name TEXT NOT NULL UNIQUE
);
CREATE TABLE auto_type (
	id SERIAL PRIMARY KEY,
	name TEXT NOT NULL UNIQUE
);
CREATE TABLE factory (
	id SERIAL PRIMARY KEY,
	name TEXT NOT NULL UNIQUE
);
CREATE TABLE brand (
	id SERIAL PRIMARY KEY,
	factory_id INTEGER REFERENCES factory(id),
	name TEXT NOT NULL UNIQUE
);

CREATE TABLE Auto (
	id serial PRIMARY KEY,
	brand_id INTEGER REFERENCES brand(id),
	model TEXT NOT NULL,
	year_prod integer,
	year_museum integer,
	engine_volume numeric(6,2),
	engine_power integer,
	body_type_id INTEGER REFERENCES body_type(id),
	auto_type_id INTEGER REFERENCES auto_type(id),
	world_left_count integer,
	original_parts_percent numeric(5,2),
	history text,
	hall_id integer,
	country_id integer,
	owner_id integer NOT NULL
);



-- Foreign keys
ALTER TABLE Owner
	ADD CONSTRAINT fk_owner_country FOREIGN KEY (country_id) REFERENCES country(id);
	
ALTER TABLE Auto
	ADD CONSTRAINT fk_auto_hall FOREIGN KEY (hall_id) REFERENCES hall(id);
	
ALTER TABLE Auto
	ADD CONSTRAINT fk_auto_country FOREIGN KEY (country_id) REFERENCES country(id);

ALTER TABLE Auto
	ADD CONSTRAINT fk_ao_owner FOREIGN KEY (owner_id) REFERENCES owner(id);


-- check
ALTER TABLE Auto
	ADD CONSTRAINT check_year_prod CHECK (year_prod <= EXTRACT(YEAR FROM CURRENT_DATE));

ALTER TABLE Auto
	ADD CONSTRAINT check_original_parts CHECK (original_parts_percent BETWEEN 0 AND 100);

-- unique

ALTER TABLE Auto
	ADD CONSTRAINT unique_brand_year UNIQUE (brand_id, year_prod);

ALTER TABLE Hall
	ADD CONSTRAINT unique_hall_number UNIQUE (room_number);

	

-- заводы изготовители
INSERT INTO factory(name) VALUES
	('BMW'), ('Ford'), ('Toyota'), ('Porsche'), ('AvtoVAZ'), ('GM'), ('Mercedes-Benz'), ('Cadillac');

-- марки машин
INSERT INTO brand(factory_id, name) VALUES
	((SELECT id FROM factory WHERE name='GM'), 'Chevrolet'),
	((SELECT id FROM factory WHERE name='AvtoVAZ'), 'Lada'),
	((SELECT id FROM factory WHERE name='Toyota'), 'Toyota'),
	((SELECT id FROM factory WHERE name='Mercedes-Benz'), 'Mercedes-Benz'),
	((SELECT id FROM factory WHERE name='Porsche'), 'Porsche'),
	((SELECT id FROM factory WHERE name='BMW'), 'BMW'),
	((SELECT id FROM factory WHERE name='Cadillac'), 'Cadillac'),
	((SELECT id FROM factory WHERE name='Ford'), 'Ford');

-- тип кузова
INSERT INTO body_type(name) VALUES ('Coupe'), ('Sedan'), ('Convertible'), ('Truck');

-- предназначение
INSERT INTO auto_type(name) VALUES ('Passenger'), ('Cargo');

-- номер зала
INSERT INTO Hall (room_number) VALUES (1), (2), (3), (4);

-- страны
INSERT INTO Country (name) VALUES ('USA'), ('Germany'), ('Russia'), ('Japan'), ('Italy'), ('France'),
	('UK'), ('Sweden'), ('South Korea');



-- создание владельцев

INSERT INTO Owner (full_name, country_id)
VALUES
('Elon Musk', (SELECT id FROM Country WHERE name='USA')),
('Henry Ford', (SELECT id FROM Country WHERE name='Germany')),
('Ivan Petrov', (SELECT id FROM Country WHERE name='Russia')),
('Akira Tanaka', (SELECT id FROM Country WHERE name='Japan')),
('John Miller', (SELECT id FROM Country WHERE name='USA')),
('Michael Schmidt', (SELECT id FROM Country WHERE name='Germany')),
('Sergey Ivanov', (SELECT id FROM Country WHERE name='Russia')),
('Kenji Sato', (SELECT id FROM Country WHERE name='Japan')),
('Luca Bianchi', (SELECT id FROM Country WHERE name='Italy')),
('Pierre Dubois', (SELECT id FROM Country WHERE name='France')),
('Oliver Brown', (SELECT id FROM Country WHERE name='UK')),
('Erik Johansson', (SELECT id FROM Country WHERE name='Sweden')),
('Alex Carter', (SELECT id FROM Country WHERE name='USA')),
('Dmitry Sokolov', (SELECT id FROM Country WHERE name='Russia'));



-- создание машин

INSERT INTO auto (
	year_prod, brand_id, model, year_museum, engine_volume, engine_power,
	body_type_id, auto_type_id, world_left_count, original_parts_percent,
	history, hall_id, country_id, owner_id
)
VALUES 
	-- 1
	(1985, (SELECT id FROM brand WHERE name='BMW'), 'E28',
	2005, 2.0, 125, (SELECT id FROM body_type WHERE name='Sedan'),
	(SELECT id FROM auto_type WHERE name='Passenger'), 800, 75, 'German sedan', 1, 2, 1),
	--2
	(1970, (SELECT id FROM brand WHERE name='Ford'), 'Mustang',
	1998, 4.7, 250, (SELECT id FROM body_type WHERE name='Coupe'),
	(SELECT id FROM auto_type WHERE name='Passenger'), 520, 85, 'Classic muscle car', 1, 1, 2),
	--3
	(1955, (SELECT id FROM brand WHERE name='Porsche'), '356',
	1980, 1.6, 70, (SELECT id FROM body_type WHERE name='Coupe'),
	(SELECT id FROM auto_type WHERE name='Passenger'), 120, 60, 'Early Porsche model', 2, 2, 1),
	--4
	(1967, (SELECT id FROM brand WHERE name='Chevrolet'), 'Impala',
	1995, 5.4, 300, (SELECT id FROM body_type WHERE name='Sedan'),
	(SELECT id FROM auto_type WHERE name='Passenger'), 3200, 90, 'The famous American sedan', 2, 1, 3),
	--5
	(1999, (SELECT id FROM brand WHERE name='Toyota'), 'Supra',
	2010, 3.0, 320, (SELECT id FROM body_type WHERE name='Coupe'),
	(SELECT id FROM auto_type WHERE name='Passenger'), 1500, 88, 'Japanese sport car', 3, 4, 4),
	--6
	(1974, (SELECT id FROM brand WHERE name='Lada'), '2101',
	1992, 1.2, 70, (SELECT id FROM body_type WHERE name='Sedan'),
	(SELECT id FROM auto_type WHERE name='Passenger'), 10000, 50, 'Classic Soviet car', 3, 3, 4),
	--7
	(1960, (SELECT id FROM brand WHERE name='Cadillac'), 'Eldorado',
	1985, 6.4, 375, (SELECT id FROM body_type WHERE name='Convertible'),
	(SELECT id FROM auto_type WHERE name='Passenger'), 900, 65, 'American luxury car', 4, 1, 1),
	--8
	(1985, (SELECT id FROM brand WHERE name='Mercedes-Benz'), '190E',
	2000, 2.3, 185, (SELECT id FROM body_type WHERE name='Sedan'),
	(SELECT id FROM auto_type WHERE name='Passenger'), 3000, 80, 'German compact car', 4, 2, 2),
	--9
	(1990, (SELECT id FROM brand WHERE name='BMW'), 'E30', 2005, 2.5, 170,
	 (SELECT id FROM body_type WHERE name='Sedan'),
	 (SELECT id FROM auto_type WHERE name='Passenger'), 2000, 82,
	 'Classic BMW sedan', 1, 2, 1),
	--10
	(2003, (SELECT id FROM brand WHERE name='BMW'), 'X5', 2015, 3.0, 230,
	 (SELECT id FROM body_type WHERE name='Truck'),
	 (SELECT id FROM auto_type WHERE name='Passenger'), 5000, 78,
	 'Early SUV', 2, 2, 2),
	--11
	(2010, (SELECT id FROM brand WHERE name='BMW'), 'M3 E92', 2020, 4.0, 420,
	 (SELECT id FROM body_type WHERE name='Coupe'),
	 (SELECT id FROM auto_type WHERE name='Passenger'), 3000, 90,
	 'Performance coupe', 3, 2, 1),
	--12
	(1995, (SELECT id FROM brand WHERE name='Ford'), 'Focus', 2008, 1.8, 115,
	 (SELECT id FROM body_type WHERE name='Sedan'),
	 (SELECT id FROM auto_type WHERE name='Passenger'), 8000, 70,
	 'Compact car', 1, 1, 3),
	--13
	(2015, (SELECT id FROM brand WHERE name='Ford'), 'Mustang GT', 2022, 5.0, 450,
	 (SELECT id FROM body_type WHERE name='Coupe'),
	 (SELECT id FROM auto_type WHERE name='Passenger'), 1500, 92,
	 'Modern muscle car', 2, 1, 4),
	--14
	(1988, (SELECT id FROM brand WHERE name='Toyota'), 'Corolla', 2000, 1.6, 90,
	 (SELECT id FROM body_type WHERE name='Sedan'),
	 (SELECT id FROM auto_type WHERE name='Passenger'), 12000, 60,
	 'Reliable sedan', 1, 4, 3),
	--15
	(2005, (SELECT id FROM brand WHERE name='Toyota'), 'Camry', 2015, 2.4, 167,
	 (SELECT id FROM body_type WHERE name='Sedan'),
	 (SELECT id FROM auto_type WHERE name='Passenger'), 9000, 75,
	 'Family car', 2, 4, 2),
	--16
	(2018, (SELECT id FROM brand WHERE name='Toyota'), 'Supra A90', 2023, 3.0, 335,
	 (SELECT id FROM body_type WHERE name='Coupe'),
	 (SELECT id FROM auto_type WHERE name='Passenger'), 2000, 95,
	 'Modern sports car', 3, 4, 1),
	--17
	(1975, (SELECT id FROM brand WHERE name='Chevrolet'), 'Camaro', 1990, 5.7, 275,
	 (SELECT id FROM body_type WHERE name='Coupe'),
	 (SELECT id FROM auto_type WHERE name='Passenger'), 600, 88,
	 'Classic muscle', 1, 1, 2),
	--18
	(2008, (SELECT id FROM brand WHERE name='Chevrolet'), 'Impala SS', 2018, 3.6, 260,
	 (SELECT id FROM body_type WHERE name='Sedan'),
	 (SELECT id FROM auto_type WHERE name='Passenger'), 3000, 80,
	 'Modern sedan', 2, 1, 3),
	--19
	(1992, (SELECT id FROM brand WHERE name='Lada'), 'Niva', 2005, 1.7, 80,
	 (SELECT id FROM body_type WHERE name='Truck'),
	 (SELECT id FROM auto_type WHERE name='Passenger'), 15000, 55,
	 'Off-road classic', 3, 3, 4),
	--20
	(2000, (SELECT id FROM brand WHERE name='Lada'), '2110', 2010, 1.6, 90,
	 (SELECT id FROM body_type WHERE name='Sedan'),
	 (SELECT id FROM auto_type WHERE name='Passenger'), 9000, 65,
	 'Russian sedan', 3, 3, 1),
	--21
	(2012, (SELECT id FROM brand WHERE name='Lada'), 'Granta', 2020, 1.6, 98,
	 (SELECT id FROM body_type WHERE name='Sedan'),
	 (SELECT id FROM auto_type WHERE name='Passenger'), 12000, 70,
	 'Budget car', 4, 3, 2),
	--22
	(1998, (SELECT id FROM brand WHERE name='Mercedes-Benz'), 'C-Class', 2010, 2.0, 150,
	 (SELECT id FROM body_type WHERE name='Sedan'),
	 (SELECT id FROM auto_type WHERE name='Passenger'), 4000, 85,
	 'Luxury compact', 1, 2, 3),
	--23
	(2006, (SELECT id FROM brand WHERE name='Mercedes-Benz'), 'E-Class', 2016, 3.0, 220,
	 (SELECT id FROM body_type WHERE name='Sedan'),
	 (SELECT id FROM auto_type WHERE name='Passenger'), 5000, 88,
	 'Executive sedan', 2, 2, 4),
	--24
	(2019, (SELECT id FROM brand WHERE name='Mercedes-Benz'), 'AMG GT', 2024, 4.0, 530,
	 (SELECT id FROM body_type WHERE name='Coupe'),
	 (SELECT id FROM auto_type WHERE name='Passenger'), 1000, 97,
	 'High performance', 3, 2, 1),
	--25
	(1980, (SELECT id FROM brand WHERE name='Porsche'), '911 SC', 1995, 3.0, 180,
	 (SELECT id FROM body_type WHERE name='Coupe'),
	 (SELECT id FROM auto_type WHERE name='Passenger'), 500, 85,
	 'Classic 911', 1, 2, 2),
	--26
	(2001, (SELECT id FROM brand WHERE name='Porsche'), 'Boxster', 2012, 2.7, 220,
	 (SELECT id FROM body_type WHERE name='Convertible'),
	 (SELECT id FROM auto_type WHERE name='Passenger'), 3000, 80,
	 'Roadster', 2, 2, 3),
	--27
	(2016, (SELECT id FROM brand WHERE name='Porsche'), 'Cayenne', 2023, 3.6, 440,
	 (SELECT id FROM body_type WHERE name='Truck'),
	 (SELECT id FROM auto_type WHERE name='Passenger'), 4000, 90,
	 'SUV Porsche', 3, 2, 4),
	--28
	(1997, (SELECT id FROM brand WHERE name='Cadillac'), 'DeVille', 2005, 4.6, 275,
	 (SELECT id FROM body_type WHERE name='Sedan'),
	 (SELECT id FROM auto_type WHERE name='Passenger'), 2000, 78,
	 'Luxury sedan', 1, 1, 1),
	--29
	(2010, (SELECT id FROM brand WHERE name='Cadillac'), 'Escalade', 2020, 6.2, 420,
	 (SELECT id FROM body_type WHERE name='Truck'),
	 (SELECT id FROM auto_type WHERE name='Passenger'), 2500, 85,
	 'Luxury SUV', 2, 1, 2),
	--30
	(2020, (SELECT id FROM brand WHERE name='Cadillac'), 'CT5-V', 2025, 3.0, 360,
	 (SELECT id FROM body_type WHERE name='Sedan'),
	 (SELECT id FROM auto_type WHERE name='Passenger'), 1200, 95,
	 'Modern performance sedan', 3, 1, 3),

	--31
	(2013, (SELECT id FROM brand WHERE name='Ford'), 'Explorer',
	2020, 3.5, 290,
	(SELECT id FROM body_type WHERE name='Truck'),
	(SELECT id FROM auto_type WHERE name='Passenger'),
	5000, 80, 'SUV', 1, 1,
	(SELECT id FROM Owner WHERE full_name='John Miller')),
	
	--32
	(2011, (SELECT id FROM brand WHERE name='BMW'), '5 Series',
	2018, 3.0, 245,
	(SELECT id FROM body_type WHERE name='Sedan'),
	(SELECT id FROM auto_type WHERE name='Passenger'),
	3000, 85, 'Executive sedan', 2, 2,
	(SELECT id FROM Owner WHERE full_name='Michael Schmidt')),
	
	--33
	(2014, (SELECT id FROM brand WHERE name='Toyota'), 'Prius',
	2021, 1.8, 122,
	(SELECT id FROM body_type WHERE name='Sedan'),
	(SELECT id FROM auto_type WHERE name='Passenger'),
	10000, 70, 'Hybrid', 3, 4,
	(SELECT id FROM Owner WHERE full_name='Kenji Sato')),
	
	--34
	(2016, (SELECT id FROM brand WHERE name='BMW'), 'i8',
	2022, 1.5, 369,
	(SELECT id FROM body_type WHERE name='Coupe'),
	(SELECT id FROM auto_type WHERE name='Passenger'),
	1500, 90, 'Hybrid sports car', 4, 3,
	(SELECT id FROM Owner WHERE full_name='Luca Bianchi')),
	
	--35
	(2010, (SELECT id FROM brand WHERE name='Mercedes-Benz'), 'GLA',
	2018, 2.0, 211,
	(SELECT id FROM body_type WHERE name='Truck'),
	(SELECT id FROM auto_type WHERE name='Passenger'),
	4000, 82, 'Compact SUV', 1, 3,
	(SELECT id FROM Owner WHERE full_name='Pierre Dubois')),
	
	--36
	(2012, (SELECT id FROM brand WHERE name='Ford'), 'Focus RS',
	2019, 2.3, 350,
	(SELECT id FROM body_type WHERE name='Coupe'),
	(SELECT id FROM auto_type WHERE name='Passenger'),
	2500, 88, 'Hot hatch', 2, 7,
	(SELECT id FROM Owner WHERE full_name='Oliver Brown')),
	
	--37
	(2015, (SELECT id FROM brand WHERE name='Toyota'), 'RAV4',
	2022, 2.5, 203,
	(SELECT id FROM body_type WHERE name='Truck'),
	(SELECT id FROM auto_type WHERE name='Passenger'),
	6000, 85, 'SUV', 3, 8,
	(SELECT id FROM Owner WHERE full_name='Erik Johansson')),
	
	--38
	(2013, (SELECT id FROM brand WHERE name='Lada'), 'Vesta SW',
	2020, 1.6, 106,
	(SELECT id FROM body_type WHERE name='Sedan'),
	(SELECT id FROM auto_type WHERE name='Passenger'),
	15000, 72, 'Station wagon', 4, 3,
	(SELECT id FROM Owner WHERE full_name='Dmitry Sokolov'));
