select * from hall where seats = (select max(seats) from hall);