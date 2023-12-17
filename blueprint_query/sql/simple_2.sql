select * from session
	where dt < curdate() and date_add(curdate(), interval -3 day) <= dt;
