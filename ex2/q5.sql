select name
from authors natural join conferences
except
select name
from authors natural join conferences
where area != 'systems' or year >= 1990
order by name;