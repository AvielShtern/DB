select name, instetusion
from authors natural join institutions
where country = 'il'
order by institutions, name;