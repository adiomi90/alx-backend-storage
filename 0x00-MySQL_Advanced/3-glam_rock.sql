-- This would be done through the import process, assuming the provided file metal_bands.sql.zip
-- For the purpose of this script, we assume the data is already imported

SELECT band_name,
          (COALESCE(split, 2022) - formed) AS lifespan
	FROM metal_bands
	WHERE style like '%Glam rock%';
