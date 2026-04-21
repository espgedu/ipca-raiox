"""
SELECT 
    mes, 
    valor 
FROM
    fato_ipca 
WHERE 
    categoria LIKE '%Índice geral%' AND variavel_cod = 63 
ORDER BY 
    mes;
"""