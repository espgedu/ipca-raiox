"""
SELECT 
    mes, 
    categoria as Categoria, 
    valor as Valor
FROM 
    fato_ipca 
WHERE 
    (categoria LIKE '%Alimentação%' OR categoria LIKE '%Transporte%') 
    AND variavel_cod = 63
ORDER BY
    mes;
"""