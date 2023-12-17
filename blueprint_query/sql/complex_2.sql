select date(dt), sum(sm) from (select dt, (sum(price) * coef) as sm from ticket join session using(ses_id)
	where is_sold = 1 and year(dt) = 2020
    group by ses_id)prep
    group by date(dt);
