INSERT INTO ticket(name, surname, passport_info, price, sale_date, flight_schedule_id, user_id)
    VALUE (
           '$buyer_name',
           '$buyer_surname',
           '$passport_info',
           '$price',
           NOW(),
           '$schedule_id',
           $user_id)