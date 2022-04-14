with count_per_country_and_region(region, country, totalCount) as
(select region, country, sum(count) as totalCount
from authors natural join institutions
group by region, country)
select region, country, totalCount
from count_per_country_and_region A
where totalCount = (select max(totalCount)
                        from count_per_country_and_region B
                        where A.region = B.region)
order by region, country

