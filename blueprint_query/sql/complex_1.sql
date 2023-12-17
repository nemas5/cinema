select name, dt, sum(price) * coef from ticket join session using (ses_id) join hall using (h_id)
	where is_sold = 1 and date(dt) = '2023-03-23'
    group by ses_id;
