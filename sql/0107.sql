USE sakila;

-- SELECT 절 사용으로 데이터 조회

-- customer 테이블에서 모든 열 조회
SELECT * FROM customer;

-- customer 테이블에서 first_name 열 조회
SELECT first_name FROM customer;

-- 2개 이상의 열 조회(first_name, last_name)
SELECT first_name, last_name FROM customer;

-- 시스템 함수를 사용해 테이블 열 정보 확인
SHOW COLUMNS FROM sakila.customer;


-- WHERE 절 사용으로 조건에 맞는 데이터 조회

-- 특정값 조회( 비교 연산자 사용 )
SELECT * FROM customer WHERE first_name = 'MARIA';

SELECT * FROM customer WHERE address_id = 200;

SELECT * FROM customer WHERE address_id < 200;

-- 데이터가 A, B, C 순으로 MARIA 보다 앞에 위치한 행 조회
SELECT * FROM customer WHERE first_name < 'MARIA';

SELECT * FROM payment WHERE payment_date = '2005-07-09 13:24:07';

SELECT * FROM payment WHERE payment_date < '2005-07-09';

-- 논리 연산자 사용

-- 데이터가 5~10 범위에 해당하는 행 조회
SELECT * FROM customer 
WHERE address_id BETWEEN 5 AND 10;

SELECT * FROM payment
WHERE payment_date BETWEEN '2005-06-17' AND '2005-07-19';

SELECT * FROM customer 
WHERE first_name BETWEEN 'M' AND 'O';

-- 범위를 포함하지 않는 연산자(NOT BETWEEN)
SELECT * FROM customer WHERE first_name NOT BETWEEN 'M' AND 'O';


-- AND, OR 연산자 사용

SELECT * FROM city WHERE city = 'Sunnyvale' AND country_id = 103;

SELECT * FROM payment 
WHERE payment_date >= '2005-06-01' AND payment_date <= '2005-07-05';

SELECT * FROM customer
WHERE first_name = 'MARIA' OR first_name = 'LINDA';

-- OR 두개 이상 사용한 경우
-- IN 사용
-- SELECT * FROM customer WHERE first_name = 'MARIA' OR first_name = 'LINDA' OR first_name = 'NANCY;
SELECT * FROM customer WHERE first_name IN ('MARIA', 'LINDA', 'NANCY');

-- AND, OR, IN 조합
SELECT * FROM city
WHERE country_id IN (103, 86) AND city IN ('Cheju', 'Sunnyvale', 'Dallas');

SELECT * FROM city
WHERE country_id = 103 OR country_id = 86 
	AND city IN ('Cheju', 'Sunnyvale', 'Dallas');
    
-- NULL
SELECT * FROM address;

-- =연산자로 NULL 값 추출 불가능
SELECT * FROM address WHERE address2 = 'NULL';

-- IS NULL 사용
SELECT * FROM address WHERE address2 IS NULL;

-- IS NOT NULL 사용
SELECT * FROM address WHERE address2 IS NOT NULL;

-- address2가 공백인 행 조회(공백은 =연산자 사용 가능)
SELECT * FROM address
WHERE address2 = '';


-- ORDER BY 절로 데이터 정렬

-- default : 오름차순
SELECT * FROM customer ORDER BY first_name;

-- 내림차순
SELECT * FROM customer ORDER BY last_name DESC;

-- 2개 이상의 열 정렬( 먼저 쓰는 열이 우선순위 높음)
-- 1) store_id 열을 기준으로 정렬  2) store_id 열에 같은 값이 있는 경우 first_name 열 기준으로 정
SELECT * FROM customer ORDER BY store_id, first_name;

-- 1) first_name 기준 정렬 2) store_id 기준 정렬
SELECT * FROM customer ORDER BY first_name, store_id;

-- store_id 열을 내림차순, first_name 열은 오름차순
SELECT * FROM customer ORDER BY store_id DESC, first_name ASC;


-- LIMIT으로 조회하고 싶은 상위 N개 설정
SELECT * FROM customer
ORDER BY store_id DESC, first_name LIMIT 10;

-- 범위 지정해서 데이터 조회(상위 N1 다음 행부터 N2개의 행 조회)
SELECT * FROM customer ORDER BY customer_id ASC LIMIT 100, 10;


-- OFFSET으로 특정 구간의 데이터 조회
SELECT * FROM customer ORDER BY customer_id LIMIT 10 OFFSET 100;


-- 와일드 카드로 문자열 조회

-- 1. LIKE와 % 사용
-- A로 시작
SELECT * FROM customer WHERE first_name LIKE 'A%';

-- AA로 시작
SELECT * FROM customer WHERE first_name LIKE 'AA%';

-- A로 끝나는 
SELECT * FROM customer WHERE first_name LIKE '%A';

-- RA로 끝나는
SELECT * FROM customer WHERE first_name LIKE '%RA';

-- A를 포함
SELECT * FROM customer WHERE first_name LIKE '%A%';

-- 특정 문자열 제외(NOT LIKE)
SELECT * FROM customer WHERE first_name NOT LIKE 'A%';


-- 2. ESCAPE로 특수 문자를 포함한 데이터 조회

-- 특수 문자 포함한 임의의 테이블 생성
WITH CTE (col_1) AS (
SELECT 'A%BC' UNION ALL
SELECT 'A_BC' UNION ALL
SELECT 'ABC'
)

SELECT * FROM CTE;

-- 특수 문자 %를 포함한 데이터 조회
WITH CTE (col_1) AS (
SELECT 'A%BC' UNION ALL
SELECT 'A_BC' UNION ALL
SELECT 'ABC'
)

SELECT * FROM CTE WHERE col_1 LIKE '%/%%' ESCAPE '/';

-- 3. LIKE와 _로 길이가 정해진 데이터 조회

SELECT * FROM customer WHERE first_name LIKE 'A_';  -- 문자열 길이 : 2

SELECT * FROM customer WHERE first_name LIKE 'A__';  -- 문자열 길이 : 3

SELECT * FROM customer WHERE first_name LIKE '__A';

SELECT * FROM customer WHERE first_name LIKE 'A__A';

SELECT * FROM customer WHERE first_name LIKE '_____';  -- 문자 길이 5개인 데이터 조


-- 4. _ 와 % 로 문자열 조회

SELECT * FROM customer WHERE first_name LIKE 'A_R%';

SELECT * FROM customer WHERE first_name LIKE '__R%';

SELECT * FROM customer WHERE first_name LIKE 'A%R_';

-- 5. REGEXP로 다양하게 데이터 조회

-- K로 시작하거나 N으로 끝나는 데이터
SELECT * FROM customer WHERE first_name REGEXP '^K|N$';

-- K와 함께 L과 N 사이의 글자를 포함한 데이터
-- K 뒤에 L과 N 사이의 글자 포함
SELECT * FROM customer WHERE first_name REGEXP 'K[L-N]';

-- K와 함께 L과 N 사이의 글자 미포함
-- K 뒤에 L과 N 사이의 글자 미포
SELECT * FROM customer WHERE first_name REGEXP 'K[^L-N]';


-- 6. 와일드 카드 더 활용(와일드카드 조합)
SELECT * FROM customer WHERE first_name LIKE 'S%' AND first_name REGEXP 'A[L-N]';

SELECT * FROM customer WHERE first_name 
LIKE '_______' AND 
first_name REGEXP 'A[L-N]' AND
first_name LIKE '%O';  -- REGEXP 'O$'로 써도 됨
