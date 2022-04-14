select region, (cast(count(*) as float) / cast(count(distinct country) as float)) as insAvg
from institutions
group by region
order by region;