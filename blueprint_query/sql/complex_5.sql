select * from (select * from session where year(dt) = "$dt")ses20 left join ticket using(ses_id)
	where t_id is null;
