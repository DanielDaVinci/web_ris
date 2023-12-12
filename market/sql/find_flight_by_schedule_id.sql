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
       price
FROM flight_schedule
         JOIN flight ON flight_schedule.flight_id = flight.id
WHERE flight_schedule.id = '$schedule_id'