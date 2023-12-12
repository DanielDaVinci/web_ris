SELECT cashier.id, cashier.passportInfo, employmentDate, dismissalDate from cashier
LEFT JOIN ticket on cashier_id=cashier.id
 WHERE cashier_id is NULL;
