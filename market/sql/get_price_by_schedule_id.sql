SELECT price FROM flight
WHERE flight.id = (SELECT flight_id FROM flight_schedule WHERE flight_schedule.id = '$schedule_id')