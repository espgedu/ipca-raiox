"""
SELECT 
    categoria, valor 
FROM 
    fato_ipca 
WHERE 
    mes = (SELECT MAX(mes) FROM fato_ipca)
    AND categoria NOT LIKE '%Índice geral%' 
    AND variavel_cod = 63
    AND valor > 0;
"""