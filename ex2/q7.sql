select year, name
from authors
where institution = 'Hebrew University of Jerusalem' and conference = 'focs' and (year >= 2000 and year <= 2020)
except
select A1.year, A1.name
from authors A1, authors A2
where A1.institution = 'Hebrew University of Jerusalem' and
      A2.institution = 'Hebrew University of Jerusalem' and
      A1.conference = 'focs' and
      A2.conference = 'focs' and
      (A1.year >= 2000 and A1.year <= 2020) and
      A1.name != A2.name and
      A1.count < A2.count and
      A1.year = A2.year
order by year, name;
