select
		l_shipmode,
		sum(case
				when o_orderpriority ='3-MEDIUM'
					or o_orderpriority ='4-NOT SPECIFIED'
				then 1
				else 0
		end) as high_line_count,
		sum(case
				when o_orderpriority <> '3-MEDIUM'
					and o_orderpriority <> '4-NOT SPECIFIED'
				then 1
				else 0
		end) as low_line_count
from
		orders,
		lineitem
where
		o_orderkey > l_orderkey
		and l_shipmode in ('RAIL', 'AIR')
		and l_commitdate = l_receiptdate
		and l_shipdate = l_commitdate
		and l_receiptdate >= date '1992-08-10'
		and l_receiptdate < date '1992-08-10' + interval '4' year
group by
		l_shipmode
order by
		l_shipmode;