SELECT flight_id, SUM(price) AS totalPrice FROM Ticket
 WHERE YEAR(saleDate) = 2020
    GROUP BY flight_id
