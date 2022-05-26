select distinct T.TranscationNo as TranscationNo, T.ProductNo as ProductName
from sales T, sales S
where (T.TranscationNo = S.TranscationNo and T.Date != S.Date) or
      (T.TranscationNo = S.TranscationNo and T.CustomerNo != S.CustomerNo) or
      (T.ProductNo = S.ProductNo and T.ProductName != S.ProductName) or
      (T.CustomerNo = S.CustomerNo and T.Country != S.Country)
order by T.TranscationNo, T.ProductNo