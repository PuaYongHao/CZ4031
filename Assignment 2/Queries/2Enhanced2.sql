select
	p_brand as brand,
	p_type as product_type,
	p_size as size_of_product,
	count(distinct ps_suppkey) as no_of_Supplier,
	AVG(p_retailprice) as average_expected_retail_price,
	(l_extendedprice/l_quantity) * (1-l_discount) * (1-l_tax) as actual_price
from
	lineitem,
	partsupp,
	part
where
	l_partkey = p_partkey and
	p_partkey = ps_partkey and
	p_brand <> 'Brand#13' and
	p_type not like 'SMALL%' and
	p_size in (1, 2, 3, 4, 5, 6, 7, 8)
group by
	p_brand,
	p_type,
	p_size,
	l_extendedprice,
	l_quantity,
	l_discount,
	l_tax
order by
	no_of_Supplier desc,
	p_brand,
	p_type,
	p_size;