create view table_year as
    select distinct year,  max(adjustedcount)
    from authores
    group by year;
