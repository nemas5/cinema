create view sold_2020 (ses_id, coef, dt, f_id, h_id, sold_count)
	as select ses_id, coef, dt, f_id, h_id, count(t_id) from `session` join ticket using(ses_id)
    where year(dt) = "$dt" and is_sold = 1
	group by ses_id

select ses_id, coef, dt, f_id, h_id from sold_2020 where sold_count = (select max(sold_count) from sold_2020)

drop view sold_2020