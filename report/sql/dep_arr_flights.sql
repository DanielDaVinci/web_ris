SELECT airport as 'Аэропорт',
        year as 'Год',
        month as 'Месяц',
        departure_number as 'Количество вылетов',
        arrival_number as 'Количество прилетов'
FROM dep_arr_flights
WHERE year = '$p1_required_year' AND month = '$p2_required_month'