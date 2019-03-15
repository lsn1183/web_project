SELECT doc_id, doc_type, title, ver, model_id, create_time, update_time, 
       creator, editor, summary, proj_id, major_ver, minor_ver, micro_ver, 
       status
  FROM ds.ds_doc_old;

1. model做成 doc

SELECT doc_id, doc_type, title, ver, model_id, proj_id, create_time, 
       update_time, creator, editor, summary, major_ver, minor_ver, 
       micro_ver, status
  FROM ds.ds_doc

INSERT INTO ds.ds_doc(doc_type, model_id, proj_id, create_time, update_time)
(
	SELECT distinct doc_type, model_id,  proj_id, now(), now()
	  FROM ds.ds_doc_old
	  order by proj_id, model_id, doc_type
);

update ds.ds_doc set ver = '0.001', micro_ver = 1;

2. 旧文档 变以 section

DROP TABLE IF EXISTS  ds.ds_section_temp;

CREATE TABLE ds.ds_section_temp
(
  sec_id serial NOT NULL,
  sec_type character varying(30),
  content character varying,
  ver character varying(30),
  doc_id integer,
  required boolean,
  order_id integer,
  parent_sec_id integer,
  micro_ver integer,
  complement character varying,
  explain character varying,
  sec_title character varying,
  old_doc_id integer
);

insert into ds.ds_section_temp(sec_type, sec_title, doc_id,
                               parent_sec_id, micro_ver, old_doc_id)
(
	SELECT 'USERCASE' as sec_type, a.title, b.doc_id, 
	       0 AS parent_sec_id, 1 AS micro_ver, a.doc_id AS old_doc_Id
	  FROM ds.ds_doc_old as a
	  left join ds.ds_doc as b
	  on a.model_id = b.model_id and a.doc_type = b.doc_type 
);

insert into ds.ds_section(sec_id, sec_type, sec_title, doc_id,
                               parent_sec_id, micro_ver)
(
	SELECT sec_id, sec_type, sec_title, doc_id,
               parent_sec_id, micro_ver
	  FROM ds.ds_section_temp as a
);

--3. 移子section
-- top
insert into ds.ds_section(sec_id, sec_type, content, ver, 
	                  doc_id, required, order_id, parent_sec_id, 
	                  micro_ver)
(
	SELECT a.sec_id, a.sec_type, a.content, a.ver,
	       b.doc_id, a.required, a.order_id, b.sec_id as parent_sec_id, 
	       a.micro_ver
	  FROM ds.ds_section_old as a
	  left join ds.ds_section_temp as b
	  on a.doc_id = b.old_doc_id
	  where a.parent_sec_id = 0
	  order by b.sec_id
);
--子
insert into ds.ds_section(sec_id, sec_type, content, ver, 
	                  doc_id, required, order_id, parent_sec_id, 
	                  micro_ver)
(
	SELECT a.sec_id, a.sec_type, a.content, a.ver,
	       b.doc_id, a.required, a.order_id, a.parent_sec_id, 
	       a.micro_ver
	  FROM ds.ds_section_old as a
	  left join ds.ds_section_temp as b
	  on a.doc_id = b.old_doc_id
	  where a.parent_sec_id <> 0
	  order by b.sec_id
);


-- 
select max(sec_id) from ds.ds_section;

select setval('ds.ds_section_sec_id_seq',  21004)  -- 设成最大值	

select max(doc_id) from ds.ds_doc;

select setval('ds.ds_doc_doc_id_seq',  2920);  -- 设成最大值

-- 4. 资源表

INSERT INTO ds.ds_section_resource_rel(sec_id, resource_id, content, operator, unit)
(
SELECT sec_id, resource_id, '', '', ''
  FROM (
	select sec_id, 1 AS id
	  from ds.ds_section
	  where sec_type = 'SEQUENCE'
  ) AS seq
  left join (
	select resource_id, 1 as id
	  from ds.ds_resource
  ) as b
  on seq.id = b.id
  order by sec_id, resource_id
);


