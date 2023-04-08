select
	s_suppkey,
	s_name,
	total
from
	supplier,
	(
		select
			l_suppkey,
			sum(l_extendedprice * (1 - l_discount)) AS total
		from
			lineitem
		group by
			l_suppkey
	) as revenue
where
	s_suppkey = l_suppkey
order by
	s_suppkey;