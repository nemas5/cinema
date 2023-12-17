select h_id, sum(price * (last - first + 1))
	from scheme
    group by h_id;
