select
	o_orderpriority,
	count(*) as order_count
from
	orders
where
	o_orderdate < date '1993-05-13'
	and exists (
		select
				*
		from
				lineitem
		where
				l_orderkey = o_orderkey
)
		group by
			o_orderpriority
		order by
			o_orderpriority
LIMIT 10;