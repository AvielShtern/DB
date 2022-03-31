select distinct A1.name
from authors A1
where not exists (select conference
                  from authors natural join conferences
                  where name = 'Noam Nisan' and area = 'ai'
                  except
                  select A2.conference
                  from authors A2
                  where A1.name = A2.name);