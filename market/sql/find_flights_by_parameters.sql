SELECT flight_schedule.id                      AS schedule_id,
       flight.id                               as flight_id,
       DATE_FORMAT(departure_time, "%Y-%m-%d") as departure_date,
       TIME_FORMAT(departure_time, "%h:%m")    as departure_time,
       departure_city,
       departure_airport,
       DATE_FORMAT(arrival_time, "%Y-%m-%d")   AS arrival_date,
       TIME_FORMAT(arrival_time, "%h:%m")      AS arrival_time,
       arrival_city,
       arrival_airport,
       flight.price,
       max_seats - COUNT(flight_schedule.id)   AS seats_left
FROM flight_schedule
         JOIN flight ON flight_schedule.flight_id = flight.id
         JOIN ticket ON flight_schedule.id = ticket.flight_schedule_id
WHERE departure_city = '$departure_city'
  AND arrival_city = '$arrival_city'
  AND DATE(departure_time) = '$flight_time'
GROUP BY flight_schedule.id