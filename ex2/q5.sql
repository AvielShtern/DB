select name
from authors natural join conferences
except
select name
from authors natural join conferences
where area != 'system' or year >= 1990
order by name;
