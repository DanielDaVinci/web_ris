SELECT cashier.id, cashier.passportInfo, employmentDate, dismissalDate from cashier LEFT JOIN
(SELECT saleDate, cashier_id from ticket WHERE MONTH(saleDate)=3 and YEAR(saleDate)=2023)
tickets on cashier_id = cashier.id
    WHERE cashier_id is NULL
