SELECT ROUTINE_NAME                                                 as proc_name,
       SUBSTRING(ROUTINE_COMMENT, LOCATE('.', ROUTINE_COMMENT) + 1) as data
FROM information_schema.ROUTINES
WHERE ROUTINE_SCHEMA = 'agentstvo'
  AND ROUTINE_COMMENT LIKE 'otchet.%';