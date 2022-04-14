with old_conferences(conference) as
(select conference
from authors natural join conferences
group by conference
having count(distinct year) >= 10
)
select distinct name
from authors
where conference in (select * from old_conferences)
order by name