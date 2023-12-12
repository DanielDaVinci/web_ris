SELECT passport_info as 'Пасспортные данные',
       price as 'Цена'
FROM ticket
         JOIN flight_schedule on ticket.flight_schedule_id = flight_schedule.id
WHERE flight_schedule.flight_id = '$flight_id_name'
  AND YEAR(sale_date) = '$year'
  AND MONTH(sale_date) = '$month'
  AND price = (SELECT MAX(price)
               FROM ticket
                        JOIN flight_schedule on ticket.flight_schedule_id = flight_schedule.id
               WHERE flight_schedule.flight_id = '$flight_id_name'
                 AND YEAR(sale_date) = '$year'
                 AND MONTH(sale_date) = '$month')
