select
	p_brand as brand,
	p_type as product_type,
	p_size as size_of_product,
	count(distinct ps_suppkey) as no_of_Supplier
from
	supplier,
	partsupp,
	part
where
	s_suppkey = ps_suppkey and
	p_partkey = ps_partkey and
	p_brand <> 'Brand#13' and
	p_type not like 'SMALL%' and
	p_size in (1, 2, 3, 4, 5, 6, 7, 8) and
	not s_nationkey <= 10
group by
	p_brand,
	p_type,
	p_size
order by
	no_of_Supplier desc,
	p_brand,
	p_type,
	p_size;