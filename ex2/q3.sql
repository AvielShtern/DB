select distinct institution, name
from institutions natural join authors natural join conferences
where (area = 'ai' or subarea = 'db') and adjustedcount >= 2
order by institution, name;