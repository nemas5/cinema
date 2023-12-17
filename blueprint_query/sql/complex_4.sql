select h_id, name, seats from hall left join session using(h_id)
	where ses_id is null;
