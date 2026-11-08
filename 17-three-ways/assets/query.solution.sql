WITH cleaned AS (
  SELECT id, customer_id,
         UPPER(TRIM(country)) AS country,
         CAST(NULLIF(amount, '') AS REAL) AS amount,
         LOWER(TRIM(status)) AS status
  FROM orders
), paid AS (
  SELECT * FROM cleaned WHERE status = 'paid'
), ranked AS (
  SELECT *, ROW_NUMBER() OVER (
    PARTITION BY customer_id ORDER BY id DESC
  ) AS rn
  FROM paid
)
SELECT country, COALESCE(SUM(amount), 0) AS revenue
FROM ranked WHERE rn = 1
GROUP BY country ORDER BY country;
