with recursive distance_from_noam(name, distance) as (
    VALUES ('Noam Nisan', 0)
    union
    select A.name, T.distance + 1
    from authors A, (select B.name, B.conference, B.year, D.distance
                     from authors B, distance_from_noam D
                     where B.name = D.name) T
    where A.year = T.year and A.conference = T.conference and T.distance + 1 <= 2
)
select distinct name
from distance_from_noam
order by name;