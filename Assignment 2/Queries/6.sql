select
	sum(l_extendedprice * l_discount) as revenue
from
	lineitem
where
	l_shipdate >= '1996-03-13'
	and l_shipdate < '1997-03-13'
	and l_discount between 0.04 and 0.06
	and l_quantity < 10.00;
