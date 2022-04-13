select name
from authors natural join conferences
where area = 'systems'
group by name
having sum(count) >= 2 and max(year) >= 2014
order by name;