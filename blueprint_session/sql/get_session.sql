select `session`.f_id, name, dt, ses_id, h_id, dt, coef from `session`
    join film using(f_id) where ses_id="$ses_id"