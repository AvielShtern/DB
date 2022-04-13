select region, count(distinct country) as countryCount
from institutions
group by region
order by region