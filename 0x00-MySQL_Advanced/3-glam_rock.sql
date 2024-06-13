-- This would be done through the import process, assuming the provided file metal_bands.sql.zip
-- For the purpose of this script, we assume the data is already imported

SELECT
    name AS band_name,
    CASE
        WHEN split IS NULL THEN 2022 - formed
        ELSE split - formed
    END AS lifespan
FROM
    metal_bands
WHERE
    style LIKE '%Glam rock%'
ORDER BY
    lifespan DESC;
