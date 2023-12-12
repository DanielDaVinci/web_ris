SELECT id                as 'Номер',
       departure_airport as 'Аэропорт отбытия',
       arrival_airport   as 'Аэропорт прибытия',
       price             as 'Цена'
FROM flight
WHERE id LIKE '$start_flight_id%'
