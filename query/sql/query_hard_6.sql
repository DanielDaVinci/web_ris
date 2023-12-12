SELECT passportInfo, employmentDate, dismissalDate FROM cashier
 WHERE id IN (SELECT id FROM tickets_sold
  WHERE amount = (SELECT MAX(amount) tickets_sold FROM tickets_sold2))
