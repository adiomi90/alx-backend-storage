-- SQL script to rank country origins of bands by the number of non-unique fans
-- Assuming the bands table has been created and populated with metal_bands.sql
-- The table has columns: origin (country) and fans (number of fans)
SELECT origin, SUM(fans) as nb_fans FROM metal_bands
GROUP BY origin ORDER BY nb_fans DESC;