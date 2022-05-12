explain analyse
select distinct name, institution, conference, count, adjustedcount, year
from authors A, (select distinct year as max_Y, max(adjustedcount) as max_A
                 from authors
                 group by year) T
where A.year = T.max_Y and A.adjustedcount = T.max_A