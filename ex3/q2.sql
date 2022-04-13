select region, count(*) / count(distinct country) as insAvg
from institutions
group by region
order by region