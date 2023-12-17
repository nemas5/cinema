select ses_id, sum(price)
	from ticket
	where is_sold = 1
    group by ses_id;
