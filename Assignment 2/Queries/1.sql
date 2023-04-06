select
	c_name as customer_name,
	n_name as nation_name,
	c_phone,
	sum(o_totalprice) as total_spend
from
	nation,customer,orders
where
	c_custkey = o_custkey AND
	c_nationkey = n_nationkey AND
	NOT n_regionkey = 0 AND
	NOT n_regionkey >=3
group by
	c_custkey,
	n_name
order by
	total_spend DESC,
	n_name,
	c_name
