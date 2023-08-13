-- A script that the country origin of bands and orders by the number of fans in descending order

SELECT origin, SUM(fans) AS nb_fans
FROM metal_bands
GROUP BY origin
ORDER BY nb_fans DESC;
