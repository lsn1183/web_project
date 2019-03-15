SELECT arl_id, "group", author, charger
  FROM public.arl_schedule_20170929;



update spec.arl_group set group_name = 'Navi Traffic' where group_name = 'Traffic';
update spec.arl_group set group_name = 'Navi Data' where group_name = 'navi data';
update spec.arl_group set group_name = 'Navi Location' where group_name = 'navi loc';
update spec.arl_group set group_name = 'Navi Map' where group_name = 'navi map';
update spec.arl_group set group_name = 'Navi Path' where group_name = 'navi path';
update spec.arl_group set group_name = 'Navi Guide' where group_name = 'Guide';
update public.arl_schedule_20170929  set "group"  = 'Navi Map' where "group" = 'navi map';
update public.arl_schedule_20170929  set "group"  = 'MICON' where "group" = 'micon';
-------
update public.arl_schedule_20170929  set "group"  = 'Navi-Data' where "group" = 'Navi Data';
update public.arl_schedule_20170929  set "group"  = 'Navi-Guide' where "group" = 'Navi Guide';
update public.arl_schedule_20170929  set "group"  = 'Navi-Location' where "group" = 'Navi Location';
update public.arl_schedule_20170929  set "group"  = 'Navi-Map' where "group" = 'Navi Map';
update public.arl_schedule_20170929  set "group"  = 'Navi-Path' where "group" = 'Navi Path';
update public.arl_schedule_20170929  set "group"  = 'Navi-Search' where "group" = 'Navi Search';
update public.arl_schedule_20170929  set "group"  = 'Navi-Traffic' where "group" = 'Navi Traffic';


insert into spec.arl_group(group_name)
(
SELECT distinct "group"
  FROM public.arl_schedule_20170929
  where "group" not in (
	select group_name
	  from spec.arl_group
  )
  and "group" <> '-'
  order by "group"
);

INSERT INTO spec.arl_user(user_name, password)
(
SELECT distinct author, '111111' AS password
  FROM public.arl_schedule_20170929
  WHERE author NOT IN (
   SELECT user_name
     FROM spec.arl_user as t2
  )
  AND author <> '-'
  order by author
 );


INSERT INTO spec.arl_user(user_name, password)
(
SELECT distinct charger, '111111' AS password
  FROM public.arl_schedule_20170929
  WHERE charger NOT IN (
   SELECT user_name
     FROM spec.arl_user as t2
  )
  AND charger <> '-'
  order by charger
 );
 


update spec.arl a set user_id = tt1.user_id
  from (
	SELECT arl_record_id, t1.arl_id, t3.user_id, user_name
	  FROM spec.arl as t1
	  inner join arl_schedule_20170929 as t2
	  on t1.arl_id = t2.arl_id
	  left join spec.arl_user as t3
	  on t2.author = t3.user_name
	  --where t3.user_id is  null
  ) as tt1
  where a.arl_record_id = tt1.arl_record_id;
  

-- 对象外
update  spec.arl set exclude_flag = True
  where mm_item is not null or exception is not null;


INSERT INTO spec.arl_group_member(group_id, user_id,
                                  "role", role_id)
(
SELECT distinct t2.group_id, t3.user_id, 1, 4
  FROM public.arl_schedule_20170929 t1
  LEFT JOIN spec.arl_group t2
  ON t1."group" = t2.group_name
  LEFT JOIN spec.arl_user t3
  on t1.charger = t3.user_name
  WHERE t3.user_id is not null
  order by t2.group_id
);

---- Leader
INSERT INTO spec.arl_group_member(group_id, user_id,
                                  "role", role_id)
(
SELECT distinct t2.group_id, t3.user_id, 1, 4
  FROM public.arl_schedule_20170929 t1
  LEFT JOIN spec.arl_group t2
  ON t1."group" = t2.group_name
  LEFT JOIN spec.arl_user t3
  on t1.charger = t3.user_name
  WHERE t3.user_id is not null
  order by t2.group_id
);

---- Member
INSERT INTO spec.arl_group_member(group_id, user_id,
                                  "role", role_id)
(
SELECT distinct t2.group_id, t3.user_id, 0, 5
  FROM public.arl_schedule_20170929 t1
  LEFT JOIN spec.arl_group t2
  ON t1."group" = t2.group_name
  LEFT JOIN spec.arl_user t3
  on t1.author = t3.user_name
  WHERE t3.user_id is not null  
        and (t2.group_id, t3.user_id) not in (
		select group_id, user_id
		  from spec.arl_group_member
        )
  order by t2.group_id, t3.user_id
);

