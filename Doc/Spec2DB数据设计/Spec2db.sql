
/* Drop Indexes */

DROP INDEX IF EXISTS spec_chapter_number_idx;
DROP INDEX IF EXISTS spec_chapter_func_rel_idx;
DROP INDEX IF EXISTS spec_chapter_model_rel_chapter_id_idx;
DROP INDEX IF EXISTS spec_functions_func_num_idx;
DROP INDEX IF EXISTS spec_func_func_rel_idx;
DROP INDEX IF EXISTS spec_func_relation_id_idx;
DROP INDEX IF EXISTS spec_func_model_rel_func_id_idx;
DROP INDEX IF EXISTS spec_image_name_idx;
DROP INDEX IF EXISTS spec_model_idx;
DROP INDEX IF EXISTS spec_specification_model_spec_num_idx;
DROP INDEX IF EXISTS spec_spec_chapter_rel_idx;



/* Drop Tables */

DROP TABLE IF EXISTS spec.req_spec_rel;
DROP TABLE IF EXISTS spec.req_spec_info;
DROP TABLE IF EXISTS spec.seq_spec;
DROP TABLE IF EXISTS spec.spec_chapter_chapter_rel;
DROP TABLE IF EXISTS spec.spec_chapter_func_rel;
DROP TABLE IF EXISTS spec.spec_chapter_model_rel;
DROP TABLE IF EXISTS spec.spec_spec_chapter_rel;
DROP TABLE IF EXISTS spec.spec_terminology_name;
DROP TABLE IF EXISTS spec.spec_chapter;
DROP TABLE IF EXISTS spec.spec_func_func_rel;
DROP TABLE IF EXISTS spec.spec_func_model_rel;
DROP TABLE IF EXISTS spec.spec_reference;
DROP TABLE IF EXISTS spec.spec_functions;
DROP TABLE IF EXISTS spec.spec_history;
DROP TABLE IF EXISTS spec.spec_image;
DROP TABLE IF EXISTS spec.spec_key_table;
DROP TABLE IF EXISTS spec.spec_model;
DROP TABLE IF EXISTS spec.spec_specification;
DROP TABLE IF EXISTS spec.spec_permanent_id;
DROP TABLE IF EXISTS spec.spec_proj;




/* Create Tables */

CREATE TABLE spec.req_spec_info
(
	req_spec_id serial NOT NULL,
	-- ReqSpec
	req_spec varchar(20),
	-- SpecNo.
	req_spec_no varchar(20),
	version varchar(20),
	-- ӛ����
	req_spec_name varchar(50),
	-- �˘�����
	req_spec_file_name varchar(50),
	PRIMARY KEY (req_spec_id)
) WITHOUT OIDS;


CREATE TABLE spec.req_spec_rel
(
	req_spec_id int NOT NULL,
	req_id int NOT NULL
) WITHOUT OIDS;


CREATE TABLE spec.seq_spec
(
	req_id serial NOT NULL,
	-- No.
	no int,
	-- �·���
	req_chapter_num varchar(50),
	-- �¥����ȥ�
	req_chapter_title varchar(30),
	-- �ک`��/���`����/����/��/���ŵ�
	req_page varchar(50),
	-- ������
	update_date date,
	-- ���
	category varchar(20),
	-- �˘�������
	spec_num varchar(20),
	-- �˘�����(Document��)
	spec_file_name varchar(50),
	-- version
	version varchar(20),
	-- �·���
	spec_chapter_num varchar(30),
	-- �ک`��/���`����/
	spec_chapter_title varchar(50),
	-- Ҫ/��Ҫ
	need varchar(4),
	-- ��Ҫ�ʈ��Ϥ�����
	reason varchar(100),
	-- ����
	belong_to varchar(20),
	-- Gr��
	group_name varchar(20),
	-- ����
	name varchar(20),
	-- ӛ�d��
	date date,
	-- �俼
	remark varchar(512),
	PRIMARY KEY (req_id)
) WITHOUT OIDS;


-- �����½�
CREATE TABLE spec.spec_chapter
(
	-- �����½�ID
	permanent_id int NOT NULL,
	chapter_id serial NOT NULL,
	-- �½ڱ��
	chapter_number varchar(100),
	title varchar(100),
	-- 'terminology' / 'chapter'
	chapter_type varchar(20) DEFAULT 'chapter',
	PRIMARY KEY (chapter_id)
) WITHOUT OIDS;


-- �½����½�֮��Ĺ�ϵ��
CREATE TABLE spec.spec_chapter_chapter_rel
(
	order_no serial,
	parent_chapter_id int NOT NULL,
	-- �����½�ID
	child_chapter_id int NOT NULL
) WITHOUT OIDS;


-- �½�����ܹ�ϵ��
CREATE TABLE spec.spec_chapter_func_rel
(
	-- ���к�
	order_no serial,
	chapter_id int NOT NULL,
	-- ���ܵ�ID
	func_id int NOT NULL
) WITHOUT OIDS;


CREATE TABLE spec.spec_chapter_model_rel
(
	order_no serial,
	chapter_id int NOT NULL,
	model_id int NOT NULL,
	val varchar(20)
) WITHOUT OIDS;


-- ���ܵ�
CREATE TABLE spec.spec_functions
(
	permanent_id int NOT NULL,
	-- ���ܵ�ID
	func_id serial NOT NULL,
	-- ���ʱʽ�����У�����ǰ��[id xx]��xx��ֵ��
	id varchar(20),
	-- �ֱ�: 
	-- summaryInfo': ���ܸ�Ҫ;
	-- 'preCondition': ǰ��;
	-- 'callInfo': ��������;
	-- "APPRANGE": �m�Ϲ���;
	-- "EXCEPT": ����;
	-- "SUPPLY": �a��;
	-- "TABLE": ��;
	-- "FUNCTION": �C��;
	-- "DESTINATION": ����;
	-- 
	func_type varchar(20),
	-- ��������(������ɾ����): ���ݵ���ʽ��xml��ʽ
	func_content varchar,
	image_id int,
	-- �������ڡ�
	update_date date DEFAULT now(),
	-- �������
	-- ���񣺲��������в��ԡ�
	-- ����+/: ��Ҫ�����鸨�����ܲ��ԡ�
	test_type varchar(10),
	-- ״̬
	status varchar(1),
	-- �����½ڱ��(��ʱ���ֶ�)
	parent_chapter_num varchar(20),
	PRIMARY KEY (func_id)
) WITHOUT OIDS;


-- ��������ܹ�ϵ��
CREATE TABLE spec.spec_func_func_rel
(
	order_no serial,
	-- ������ID.
	parent_func_id int NOT NULL,
	-- ���ܵ�ID
	child_func_id int NOT NULL
) WITHOUT OIDS;


-- �����복�͵Ĺ�ϵ
CREATE TABLE spec.spec_func_model_rel
(
	order_no serial,
	-- ���ܵ�ID
	func_id int NOT NULL,
	model_id int NOT NULL,
	-- '-' / 'O'
	val varchar(20)
) WITHOUT OIDS;


-- ʽ��������Ěs
CREATE TABLE spec.spec_history
(
	-- ���
	serial_no serial NOT NULL,
	-- �淬
	version varchar(100),
	-- ����
	region varchar(10),
	-- ָʾ��
	instruction_person varchar(20),
	-- (ָʾ����)�ĕ���
	instruction_doc_name varchar(100),
	-- (ָʾ����)Ver
	instruction_doc_ver varchar(255),
	-- (ָʾ����)������
	instruction_doc_num varchar(255),
	-- ָʾ��
	instruction_date date,
	-- ��������
	modify_reason varchar(255),
	-- ��������Ԕ��
	detail_reason varchar(1024),
	-- 헷�
	chapter varchar(100),
	-- ����ǰ����
	old_content varchar,
	-- ����������
	new_content varchar,
	-- ������
	modify_date date,
	-- ����
	responsible_person varchar(20),
	-- �俼
	note varchar(255),
	spec_id int NOT NULL,
	PRIMARY KEY (serial_no)
) WITHOUT OIDS;


CREATE TABLE spec.spec_image
(
	image_id serial NOT NULL,
	image_name varchar(50),
	image_type varchar(5),
	image_blob bytea,
	-- MD5
	hash_key varchar(32),
	PRIMARY KEY (image_id)
) WITHOUT OIDS;


CREATE TABLE spec.spec_key_table
(
	key varchar(20),
	val varchar(20)
) WITHOUT OIDS;


-- ����
CREATE TABLE spec.spec_model
(
	model_id serial NOT NULL,
	-- 17cy-ȫ��ǥ빲ͨ-DCU-&ZKxxx/XX;
	-- 
	model varchar(50),
	PRIMARY KEY (model_id)
) WITHOUT OIDS;


CREATE TABLE spec.spec_permanent_id
(
	permanent_id serial NOT NULL,
	-- 'spec' / 'function' / 'chapter'
	type varchar(20),
	PRIMARY KEY (permanent_id)
) WITHOUT OIDS;


CREATE TABLE spec.spec_proj
(
	-- ��ĿID.
	proj_id serial NOT NULL,
	-- ��Ŀ���ơ�
	proj_name varchar(20),
	PRIMARY KEY (proj_id)
) WITHOUT OIDS;


-- �������˘������
CREATE TABLE spec.spec_reference
(
	-- ���ܵ�ID
	func_id int NOT NULL,
	-- �˘�������
	spec_no varchar(30),
	-- Version
	version varchar(20),
	PRIMARY KEY (func_id)
) WITHOUT OIDS;


-- ����ʽ����
CREATE TABLE spec.spec_specification
(
	-- �����½�ID (ͬʱ������Ϊ�汾ʹ��)
	permanent_id int NOT NULL,
	spec_id serial NOT NULL,
	-- 17CY / 14Tmap
	proj_id int,
	-- ʽ������
	spec_num varchar(20),
	-- ����ʽ������.
	spec_name varchar(100),
	-- ʽ�����ļ�����
	spec_file_name varchar(100),
	-- ��дʽ���������
	language varchar(3),
	version varchar(100),
	-- �����Ƿ�������
	-- True: ��������
	-- False: ������
	dirty boolean DEFAULT 'True',
	PRIMARY KEY (spec_id)
) WITHOUT OIDS;


-- ʽ�������½ڹ�ϵ��
CREATE TABLE spec.spec_spec_chapter_rel
(
	order_no serial,
	spec_id int NOT NULL,
	chapter_id int
) WITHOUT OIDS;


CREATE TABLE spec.spec_terminology_name
(
	order_no serial,
	chapter_id int NOT NULL,
	name varchar(256),
	definition varchar(1024)
) WITHOUT OIDS;



/* Create Foreign Keys */

ALTER TABLE spec.req_spec_rel
	ADD FOREIGN KEY (req_spec_id)
	REFERENCES spec.req_spec_info (req_spec_id)
	ON UPDATE RESTRICT
	ON DELETE RESTRICT
;


ALTER TABLE spec.req_spec_rel
	ADD FOREIGN KEY (req_id)
	REFERENCES spec.seq_spec (req_id)
	ON UPDATE RESTRICT
	ON DELETE RESTRICT
;


ALTER TABLE spec.spec_chapter_chapter_rel
	ADD FOREIGN KEY (parent_chapter_id)
	REFERENCES spec.spec_chapter (chapter_id)
	ON UPDATE RESTRICT
	ON DELETE RESTRICT
;


ALTER TABLE spec.spec_chapter_func_rel
	ADD FOREIGN KEY (chapter_id)
	REFERENCES spec.spec_chapter (chapter_id)
	ON UPDATE RESTRICT
	ON DELETE RESTRICT
;


ALTER TABLE spec.spec_chapter_model_rel
	ADD FOREIGN KEY (chapter_id)
	REFERENCES spec.spec_chapter (chapter_id)
	ON UPDATE RESTRICT
	ON DELETE RESTRICT
;


ALTER TABLE spec.spec_spec_chapter_rel
	ADD FOREIGN KEY (chapter_id)
	REFERENCES spec.spec_chapter (chapter_id)
	ON UPDATE RESTRICT
	ON DELETE RESTRICT
;


ALTER TABLE spec.spec_terminology_name
	ADD FOREIGN KEY (chapter_id)
	REFERENCES spec.spec_chapter (chapter_id)
	ON UPDATE RESTRICT
	ON DELETE RESTRICT
;


ALTER TABLE spec.spec_chapter_func_rel
	ADD FOREIGN KEY (func_id)
	REFERENCES spec.spec_functions (func_id)
	ON UPDATE RESTRICT
	ON DELETE RESTRICT
;


ALTER TABLE spec.spec_func_func_rel
	ADD FOREIGN KEY (parent_func_id)
	REFERENCES spec.spec_functions (func_id)
	ON UPDATE RESTRICT
	ON DELETE RESTRICT
;


ALTER TABLE spec.spec_func_model_rel
	ADD FOREIGN KEY (func_id)
	REFERENCES spec.spec_functions (func_id)
	ON UPDATE RESTRICT
	ON DELETE RESTRICT
;


ALTER TABLE spec.spec_reference
	ADD FOREIGN KEY (func_id)
	REFERENCES spec.spec_functions (func_id)
	ON UPDATE RESTRICT
	ON DELETE RESTRICT
;


ALTER TABLE spec.spec_functions
	ADD FOREIGN KEY (image_id)
	REFERENCES spec.spec_image (image_id)
	ON UPDATE RESTRICT
	ON DELETE RESTRICT
;


ALTER TABLE spec.spec_chapter_model_rel
	ADD FOREIGN KEY (model_id)
	REFERENCES spec.spec_model (model_id)
	ON UPDATE RESTRICT
	ON DELETE RESTRICT
;


ALTER TABLE spec.spec_func_model_rel
	ADD FOREIGN KEY (model_id)
	REFERENCES spec.spec_model (model_id)
	ON UPDATE RESTRICT
	ON DELETE RESTRICT
;


ALTER TABLE spec.spec_chapter
	ADD FOREIGN KEY (permanent_id)
	REFERENCES spec.spec_permanent_id (permanent_id)
	ON UPDATE RESTRICT
	ON DELETE RESTRICT
;


ALTER TABLE spec.spec_functions
	ADD FOREIGN KEY (permanent_id)
	REFERENCES spec.spec_permanent_id (permanent_id)
	ON UPDATE RESTRICT
	ON DELETE RESTRICT
;


ALTER TABLE spec.spec_specification
	ADD FOREIGN KEY (permanent_id)
	REFERENCES spec.spec_permanent_id (permanent_id)
	ON UPDATE RESTRICT
	ON DELETE RESTRICT
;


ALTER TABLE spec.spec_history
	ADD FOREIGN KEY (spec_id)
	REFERENCES spec.spec_specification (spec_id)
	ON UPDATE RESTRICT
	ON DELETE RESTRICT
;


ALTER TABLE spec.spec_spec_chapter_rel
	ADD FOREIGN KEY (spec_id)
	REFERENCES spec.spec_specification (spec_id)
	ON UPDATE RESTRICT
	ON DELETE RESTRICT
;



/* Create Indexes */

CREATE INDEX spec_chapter_number_idx ON spec.spec_chapter USING BTREE (chapter_number);
CREATE INDEX spec_chapter_func_rel_idx ON spec.spec_chapter_func_rel USING BTREE (chapter_id, func_id);
CREATE INDEX spec_chapter_model_rel_chapter_id_idx ON spec.spec_chapter_model_rel USING BTREE (chapter_id);
CREATE INDEX spec_functions_func_num_idx ON spec.spec_functions USING BTREE (id);
CREATE INDEX spec_func_func_rel_idx ON spec.spec_func_func_rel USING BTREE (parent_func_id, child_func_id);
CREATE INDEX spec_func_relation_id_idx ON spec.spec_func_model_rel USING BTREE (model_id);
CREATE INDEX spec_func_model_rel_func_id_idx ON spec.spec_func_model_rel USING BTREE (func_id);
CREATE INDEX spec_image_name_idx ON spec.spec_image USING BTREE (image_name);
CREATE INDEX spec_model_idx ON spec.spec_model USING BTREE (model);
CREATE INDEX spec_specification_model_spec_num_idx ON spec.spec_specification USING BTREE (proj_id, spec_num);
CREATE INDEX spec_spec_chapter_rel_idx ON spec.spec_spec_chapter_rel USING BTREE (spec_id, chapter_id);



/* Comments */

COMMENT ON COLUMN spec.req_spec_info.req_spec IS 'ReqSpec';
COMMENT ON COLUMN spec.req_spec_info.req_spec_no IS 'SpecNo.';
COMMENT ON COLUMN spec.req_spec_info.req_spec_name IS 'ӛ����';
COMMENT ON COLUMN spec.req_spec_info.req_spec_file_name IS '�˘�����';
COMMENT ON COLUMN spec.seq_spec.no IS 'No.';
COMMENT ON COLUMN spec.seq_spec.req_chapter_num IS '�·���';
COMMENT ON COLUMN spec.seq_spec.req_chapter_title IS '�¥����ȥ�';
COMMENT ON COLUMN spec.seq_spec.req_page IS '�ک`��/���`����/����/��/���ŵ�';
COMMENT ON COLUMN spec.seq_spec.update_date IS '������';
COMMENT ON COLUMN spec.seq_spec.category IS '���';
COMMENT ON COLUMN spec.seq_spec.spec_num IS '�˘�������';
COMMENT ON COLUMN spec.seq_spec.spec_file_name IS '�˘�����(Document��)';
COMMENT ON COLUMN spec.seq_spec.version IS 'version';
COMMENT ON COLUMN spec.seq_spec.spec_chapter_num IS '�·���';
COMMENT ON COLUMN spec.seq_spec.spec_chapter_title IS '�ک`��/���`����/';
COMMENT ON COLUMN spec.seq_spec.need IS 'Ҫ/��Ҫ';
COMMENT ON COLUMN spec.seq_spec.reason IS '��Ҫ�ʈ��Ϥ�����';
COMMENT ON COLUMN spec.seq_spec.belong_to IS '����';
COMMENT ON COLUMN spec.seq_spec.group_name IS 'Gr��';
COMMENT ON COLUMN spec.seq_spec.name IS '����';
COMMENT ON COLUMN spec.seq_spec.date IS 'ӛ�d��';
COMMENT ON COLUMN spec.seq_spec.remark IS '�俼';
COMMENT ON TABLE spec.spec_chapter IS '�����½�';
COMMENT ON COLUMN spec.spec_chapter.permanent_id IS '�����½�ID';
COMMENT ON COLUMN spec.spec_chapter.chapter_number IS '�½ڱ��';
COMMENT ON COLUMN spec.spec_chapter.chapter_type IS '''terminology'' / ''chapter''';
COMMENT ON TABLE spec.spec_chapter_chapter_rel IS '�½����½�֮��Ĺ�ϵ��';
COMMENT ON COLUMN spec.spec_chapter_chapter_rel.child_chapter_id IS '�����½�ID';
COMMENT ON TABLE spec.spec_chapter_func_rel IS '�½�����ܹ�ϵ��';
COMMENT ON COLUMN spec.spec_chapter_func_rel.order_no IS '���к�';
COMMENT ON COLUMN spec.spec_chapter_func_rel.func_id IS '���ܵ�ID';
COMMENT ON TABLE spec.spec_functions IS '���ܵ�';
COMMENT ON COLUMN spec.spec_functions.func_id IS '���ܵ�ID';
COMMENT ON COLUMN spec.spec_functions.id IS '���ʱʽ�����У�����ǰ��[id xx]��xx��ֵ��';
COMMENT ON COLUMN spec.spec_functions.func_type IS '�ֱ�: 
summaryInfo'': ���ܸ�Ҫ;
''preCondition'': ǰ��;
''callInfo'': ��������;
"APPRANGE": �m�Ϲ���;
"EXCEPT": ����;
"SUPPLY": �a��;
"TABLE": ��;
"FUNCTION": �C��;
"DESTINATION": ����;
';
COMMENT ON COLUMN spec.spec_functions.func_content IS '��������(������ɾ����): ���ݵ���ʽ��xml��ʽ';
COMMENT ON COLUMN spec.spec_functions.update_date IS '�������ڡ�';
COMMENT ON COLUMN spec.spec_functions.test_type IS '�������
���񣺲��������в��ԡ�
����+/: ��Ҫ�����鸨�����ܲ��ԡ�';
COMMENT ON COLUMN spec.spec_functions.status IS '״̬';
COMMENT ON COLUMN spec.spec_functions.parent_chapter_num IS '�����½ڱ��(��ʱ���ֶ�)';
COMMENT ON TABLE spec.spec_func_func_rel IS '��������ܹ�ϵ��';
COMMENT ON COLUMN spec.spec_func_func_rel.parent_func_id IS '������ID.';
COMMENT ON COLUMN spec.spec_func_func_rel.child_func_id IS '���ܵ�ID';
COMMENT ON TABLE spec.spec_func_model_rel IS '�����복�͵Ĺ�ϵ';
COMMENT ON COLUMN spec.spec_func_model_rel.func_id IS '���ܵ�ID';
COMMENT ON COLUMN spec.spec_func_model_rel.val IS '''-'' / ''O''';
COMMENT ON TABLE spec.spec_history IS 'ʽ��������Ěs';
COMMENT ON COLUMN spec.spec_history.serial_no IS '���';
COMMENT ON COLUMN spec.spec_history.version IS '�淬';
COMMENT ON COLUMN spec.spec_history.region IS '����';
COMMENT ON COLUMN spec.spec_history.instruction_person IS 'ָʾ��';
COMMENT ON COLUMN spec.spec_history.instruction_doc_name IS '(ָʾ����)�ĕ���';
COMMENT ON COLUMN spec.spec_history.instruction_doc_ver IS '(ָʾ����)Ver';
COMMENT ON COLUMN spec.spec_history.instruction_doc_num IS '(ָʾ����)������';
COMMENT ON COLUMN spec.spec_history.instruction_date IS 'ָʾ��';
COMMENT ON COLUMN spec.spec_history.modify_reason IS '��������';
COMMENT ON COLUMN spec.spec_history.detail_reason IS '��������Ԕ��';
COMMENT ON COLUMN spec.spec_history.chapter IS '헷�';
COMMENT ON COLUMN spec.spec_history.old_content IS '����ǰ����';
COMMENT ON COLUMN spec.spec_history.new_content IS '����������';
COMMENT ON COLUMN spec.spec_history.modify_date IS '������';
COMMENT ON COLUMN spec.spec_history.responsible_person IS '����';
COMMENT ON COLUMN spec.spec_history.note IS '�俼';
COMMENT ON COLUMN spec.spec_image.hash_key IS 'MD5';
COMMENT ON TABLE spec.spec_model IS '����';
COMMENT ON COLUMN spec.spec_model.model IS '17cy-ȫ��ǥ빲ͨ-DCU-&ZKxxx/XX;
';
COMMENT ON COLUMN spec.spec_permanent_id.type IS '''spec'' / ''function'' / ''chapter''';
COMMENT ON COLUMN spec.spec_proj.proj_id IS '��ĿID.';
COMMENT ON COLUMN spec.spec_proj.proj_name IS '��Ŀ���ơ�';
COMMENT ON TABLE spec.spec_reference IS '�������˘������';
COMMENT ON COLUMN spec.spec_reference.func_id IS '���ܵ�ID';
COMMENT ON COLUMN spec.spec_reference.spec_no IS '�˘�������';
COMMENT ON COLUMN spec.spec_reference.version IS 'Version';
COMMENT ON TABLE spec.spec_specification IS '����ʽ����';
COMMENT ON COLUMN spec.spec_specification.permanent_id IS '�����½�ID (ͬʱ������Ϊ�汾ʹ��)';
COMMENT ON COLUMN spec.spec_specification.proj_id IS '17CY / 14Tmap';
COMMENT ON COLUMN spec.spec_specification.spec_num IS 'ʽ������';
COMMENT ON COLUMN spec.spec_specification.spec_name IS '����ʽ������.';
COMMENT ON COLUMN spec.spec_specification.spec_file_name IS 'ʽ�����ļ�����';
COMMENT ON COLUMN spec.spec_specification.language IS '��дʽ���������';
COMMENT ON COLUMN spec.spec_specification.dirty IS '�����Ƿ�������
True: ��������
False: ������';
COMMENT ON TABLE spec.spec_spec_chapter_rel IS 'ʽ�������½ڹ�ϵ��';



