"""
SELECT 
    categoria as Categoria, 
    SUM(valor) as "Total Acumulado" 
FROM 
    fato_ipca 
WHERE 
    Categoria NOT LIKE '%Índice geral%' AND variavel_cod = 63
GROUP BY 
    Categoria 
ORDER BY 
    Total Acumulado DESC 
LIMIT 6;
"""