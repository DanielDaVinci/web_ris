SELECT flight_id as 'Номер рейса',
       sale_date as 'Дата продажи',
       sum_price as 'Общий доход'
FROM total_price_perday
WHERE sale_date = '$required_date';