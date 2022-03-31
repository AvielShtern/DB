select name, yesr
from authors natural join conferences
where institution = 'Hebrew University of Jerusalem' and subarea 'vision'
intersect
select name, yesr
from authors natural join conferences
where institution = 'Hebrew University of Jerusalem' and subarea 'ai'
order by name, year;