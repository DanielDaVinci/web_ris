SELECT name          as 'Имя покупателя',
       surname       as 'Фамилия покупателя',
       passport_info as 'Паспортные данные',
       price         as 'Цена',
       sale_date     as 'Дата продажи'
FROM ticket
WHERE TO_DAYS(CURDATE()) - TO_DAYS(sale_date) BETWEEN 0 AND '$days'
