SELECT name          as 'Имя покупателя',
       surname       as 'Фамилия покупателя',
       passport_info as 'Паспортные данные',
       price         as 'Цена',
       sale_date     as 'Дата продажи'
FROM ticket
WHERE YEAR(sale_date) = '$year'
  AND MONTH(sale_date) = '$month'
