SELECT flight_id  as 'Номер рейса',
       sale_year  as 'Год',
       sale_month as 'Месяц',
       sum_price  as 'Общий доход'
FROM total_price_perday
WHERE sale_year = '$p1_required_year'
  AND sale_month = '$p2_required_month';