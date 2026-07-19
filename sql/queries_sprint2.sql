-- ====================================================================
-- SPRINT 2 - CONSULTAS SQL COMPLEXAS
-- Objetivo: Identificar os TOP 3 produtos mais lucrativos por categoria
-- Conceitos Utilizados: CTEs (WITH), Window Functions (DENSE_RANK), Group By
-- ====================================================================

WITH FaturamentoProdutos AS (
    SELECT 
        Categoria_Produto,
        Nome_Produto,
        SUM(Quantidade) as Total_Itens,
        SUM(Quantidade * Valor_Unitario) as Faturamento_Total
    FROM vendas
    GROUP BY Categoria_Produto, Nome_Produto
),
RankeamentoProdutos AS (
    SELECT 
        Categoria_Produto,
        Nome_Produto,
        Total_Itens,
        Faturamento_Total,
        DENSE_RANK() OVER (PARTITION BY Categoria_Produto ORDER BY Faturamento_Total DESC) as Rank_Faturamento
    FROM FaturamentoProdutos
)
SELECT 
    Categoria_Produto,
    Nome_Produto,
    Total_Itens,
    Faturamento_Total,
    Rank_Faturamento
FROM RankeamentoProdutos
WHERE Rank_Faturamento <= 3;