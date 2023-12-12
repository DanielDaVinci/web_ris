SELECT saleDate, COUNT(*) AS saleCount FROM Ticket
    WHERE YEAR(saleDate) = 2020 AND MONTH(saleDate)=3 AND (flight_id = 'SU2 2')
    GROUP BY saleDate
