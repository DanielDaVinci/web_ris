SELECT MAX(price) FROM Ticket
    WHERE flight_id = 'SU2 2' AND YEAR(saleDate) = 2020
