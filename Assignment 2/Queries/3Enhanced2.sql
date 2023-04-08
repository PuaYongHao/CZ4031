select 
	r_name,
	n_name,
	c_mktsegment,
	AVG(c_acctbal)
from
	customer,
	nation,
	region
where
	n_nationkey = c_nationkey
	and r_regionkey = n_regionkey
group by
	r_name,
	n_name,
	c_mktsegment
order by
	r_name,
	n_name