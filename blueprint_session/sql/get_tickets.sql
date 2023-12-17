select t_id, `row`, seat, price, is_sold from ticket join session on `session`.ses_id=`ticket`.ses_id
    where `session`.ses_id="$ses_id"