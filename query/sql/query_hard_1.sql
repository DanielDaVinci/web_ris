SELECT departure_airport as 'Аэропорт отбытия',
       arrival_airport   as 'Аэропорт прибытия',
       COUNT(*)          as 'Количество проданных билетов',
       SUM(price)        as 'Сумма'
FROM (SELECT departure_airport, arrival_airport, flight.id as fl_id, flight.price
      FROM flight
               JOIN flight_schedule ON flight.id = flight_schedule.flight_id
               JOIN ticket ON flight_schedule.id = ticket.flight_schedule_id
      WHERE YEAR(sale_date) = '$year'
        AND MONTH(sale_date) = '$month') z
GROUP BY fl_id
