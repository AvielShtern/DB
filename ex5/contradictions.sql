select distinct T.TransactionNo as TransactionNo, T.ProductNo as ProductNo
from sales T, sales S
where (T.TransactionNo = S.TransactionNo and T.date != S.date) or
      (T.TransactionNo = S.TransactionNo and T.CustomerNo != S.CustomerNo) or
      (T.ProductNo = S.ProductNo and T.ProductName != S.ProductName) or
      (T.CustomerNo = S.CustomerNo and T.country != S.country)
order by TransactionNo ProductNo