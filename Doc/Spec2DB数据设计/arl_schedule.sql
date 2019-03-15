
INSERT INTO spec.arl_user(user_name, password)
(
SELECT distinct author, '111111' AS password
  FROM public.arl_schedule
  WHERE author NOT IN (
   SELECT user_name
     FROM spec.arl_user as t2
  )
  AND author <> '-'
  order by author
 )


INSERT INTO spec.arl_user(user_name, password)
(
SELECT distinct charger, '111111' AS password
  FROM public.arl_schedule
  WHERE charger NOT IN (
   SELECT user_name
     FROM spec.arl_user as t2
  )
  AND charger <> '-'
  order by charger
 );
 

insert into spec.arl_group(group_name)
(
SELECT distinct "group"
  FROM public.arl_schedule
  where "group" not in (
	select group_name
	  from spec.arl_group
  )
  and "group" <> '-'
  order by "group"
);


update spec.arl a set user_id = tt1.user_id
  from (
	SELECT arl_record_id, t1.arl_id, t3.user_id, user_name
	  FROM spec.arl as t1
	  inner join arl_schedule as t2
	  on t1.arl_id = t2.arl_id
	  left join spec.arl_user as t3
	  on t2.author = t3.user_name
  ) as tt1
  where a.arl_record_id = tt1.arl_record_id
  

-- 对象外
update  spec.arl set exclude_flag = True
  where mm_item is not null or exception is not null;
