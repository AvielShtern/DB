select distinct name, institution
from authors natural join institutions
where country = 'il'
order by institution, name;