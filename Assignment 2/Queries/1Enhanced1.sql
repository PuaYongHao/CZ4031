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
	n_regionkey = 2 AND
	c_custkey >= 10000 AND
	c_acctbal < 0 AND
	o_orderstatus = 'O' AND
	o_orderdate >= DATE '1998-01-27'	
group by
	c_custkey
order by
	total_spend DESC,
	n_name,
	c_name