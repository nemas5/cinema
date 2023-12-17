select h_id, count(*) from session
	where '2020-03-01' <= dt and dt < '2020-04-01'
	group by h_id;
