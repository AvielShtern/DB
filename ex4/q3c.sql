create index try1 on authors(year, adjustedcount desc);
explain analyse
select distinct *
from authors a1
where adjustedcount = (
                        select max(adjustedcount)
                        from authors a2
                        where a2.year = a1.year
                    );

drop index try1;
