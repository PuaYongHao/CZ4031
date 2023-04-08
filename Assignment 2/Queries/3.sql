select 
	r_name,
	n_name,
	c_mktsegment
from
	customer,
	nation,
	region
where
	n_nationkey = c_nationkey
	and r_regionkey = n_regionkey