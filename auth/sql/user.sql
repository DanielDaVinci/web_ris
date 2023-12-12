select id as user_id, group_name as user_group
from user
where login = "$login"
  and password = "$password"
