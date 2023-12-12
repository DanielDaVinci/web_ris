SELECT departure_airport as 'Аэропорт отбытия',
       MONTH(departure_time) as 'Месяц отбытия',
       COUNT(ticket.id)         as 'Количество проданных билетов'
FROM flight
         JOIN flight_schedule ON flight.id = flight_schedule.flight_id
         JOIN ticket ON flight_schedule.id = ticket.flight_schedule_id
WHERE YEAR(departure_time) = '$year'
GROUP BY departure_airport, MONTH(departure_time)
