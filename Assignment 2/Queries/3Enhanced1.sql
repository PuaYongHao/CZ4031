select 
	r_name,
	n_name,
	c_mktsegment,
	count(c_mktsegment) as segment_count
from
	customer,
	region,
	nation
where
	r_regionkey = n_regionkey
	and n_nationkey = c_nationkey 
group by
	r_name,
	n_name,
	c_mktsegment
order by
	r_name,
	n_name,
	c_mktsegment