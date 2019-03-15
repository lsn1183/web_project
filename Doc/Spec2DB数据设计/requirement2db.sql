
/* Drop Indexes */

DROP INDEX IF EXISTS analysis_rc_model_rel_idx;
DROP INDEX IF EXISTS requirement_spec_def_rel_idx;



/* Drop Tables */

DROP TABLE IF EXISTS spec.analysis_rc_model_rel;
DROP TABLE IF EXISTS spec.analysis_model;
DROP TABLE IF EXISTS spec.analysis_spec_rel;
DROP TABLE IF EXISTS spec.analysis_spec;
DROP TABLE IF EXISTS spec.analysis_spec_record;
DROP TABLE IF EXISTS spec.requirement_def_device;
DROP TABLE IF EXISTS spec.requirement_spec_def_rel;
DROP TABLE IF EXISTS spec.requirement_def_record;
DROP TABLE IF EXISTS spec.requirement_spec;




/* Create Tables */

CREATE TABLE spec.analysis_model
(
	model_id serial NOT NULL,
	-- APL ģ��
	model varchar(100),
	PRIMARY KEY (model_id)
) WITHOUT OIDS;


CREATE TABLE spec.analysis_rc_model_rel
(
	order_no serial NOT NULL,
	analysis_id int NOT NULL,
	model_id int NOT NULL,
	val varchar,
	PRIMARY KEY (order_no)
) WITHOUT OIDS;


CREATE TABLE spec.analysis_spec
(
	analysis_spec_id serial NOT NULL,
	proj varchar,
	-- ʽ��������
	spec_name varchar,
	-- �汾
	ver varchar,
	-- �ļ�����
	file_name varchar,
	PRIMARY KEY (analysis_spec_id)
) WITHOUT OIDS;


CREATE TABLE spec.analysis_spec_record
(
	analysis_id serial NOT NULL,
	-- ������
	author_name varchar(20),
	-- TAGLҪ�����xID
	requirement_id varchar(20),
	spec_chapter_num varchar(20),
	-- ����ID
	id varchar(20),
	-- ��˩`��ID
	unique_id int,
	major_category varchar(20),
	-- �з��
	medium_catetory varchar(20),
	small_category varchar(30),
	-- Ԕ��
	detail varchar(512),
	-- ����Ҫ��
	base varchar(32),
	-- �v�B����Ҫ��
	rel_requiremant varchar(256),
	-- ����
	exception varchar(32),
	-- DCU/MEU�ɤ�����붨��
	dcu_meu varchar(256),
	-- ״�B
	pf_status varchar(256),
	-- �ȥꥬ�`
	fp_trigger varchar(512),
	-- ����
	pf_action varchar(512),
	-- ���`���󥹇�
	seq_diagram varchar,
	application varchar,
	kernel varchar,
	systemd varchar,
	-- �a������˘���
	supple_spec varchar,
	-- δ���^
	uncheck varchar,
	-- �俼
	remark varchar,
	PRIMARY KEY (analysis_id)
) WITHOUT OIDS;


CREATE TABLE spec.analysis_spec_rel
(
	analysis_spec_id int,
	analysis_id int
) WITHOUT OIDS;


-- ����ǥХ���----����ʽ����(��ɫ��)
CREATE TABLE spec.requirement_def_device
(
	order_no serial,
	req_def_id int,
	device_type varchar(50),
	val varchar(512)
) WITHOUT OIDS;


-- Ҫ�����x��
CREATE TABLE spec.requirement_def_record
(
	req_def_id serial NOT NULL,
	-- ����
	author_name varchar(20),
	-- H/UҪ�����xID
	hu_def_id varchar(20),
	-- Ҫ�����xID -- ����ʽ�����½ں�
	requirement_id varchar(20),
	id varchar(20),
	spec_chapter_num varchar(20),
	-- ��˩`��ID
	unique_id int,
	-- ����
	major_category varchar(20),
	-- �з��
	medium_catetory varchar(20),
	-- С���
	small_category varchar(30),
	-- Ԕ��
	detail varchar(512),
	-- ����Ҫ��
	base varchar(32),
	-- �v�B����Ҫ��
	rel_requiremant varchar(256),
	exception varchar(32),
	-- DCU-״�B
	dcu_status varchar(256),
	-- DCU �ȥꥬ�`
	dcu_trigger varchar(512),
	-- DCU ����
	dcu_action varchar(512),
	-- MEU ״�B
	meu_status varchar(256),
	-- MEU-�ȥꥬ�`
	meu_trigger varchar(512),
	-- MEU-����
	meu_action varchar(512),
	-- �俼(HUҪ�����x)
	hu_req_remark varchar(512),
	-- DCU/MEU�ɤ�����붨��
	dcu_meu varchar(32),
	-- ״�B
	pf_status varchar(512),
	-- �ȥꥬ�`
	pf_trigger varchar(512),
	-- ����
	pf_action varchar(512),
	-- �俼
	remark varchar,
	-- ؟�շֵ�����ӛ���
	notice varchar,
	-- �ο�HAL�OӋ��
	rel_hal_design varchar,
	-- �ο������`������`��
	rel_flow_diagram varchar(50),
	-- �������˘�����ե��ϩ`���˘��ȣ�
	other_spec varchar(50),
	-- ��ե���󥹥ϩ`���ϤǤΌg�F�ɷ�
	implementation varchar(100),
	-- Ԕ�������ɷ�
	analysis varchar(20),
	-- δҪ������
	unrequire varchar(2),
	PRIMARY KEY (req_def_id)
) WITHOUT OIDS;


-- Ҫ�����x��
CREATE TABLE spec.requirement_spec
(
	requiremnt_spec_id serial NOT NULL,
	-- ��Ŀ
	proj varchar(50),
	-- ʽ��������
	spec_name varchar,
	-- �汾
	ver varchar(50),
	-- �ļ�����
	file_name varchar(50),
	PRIMARY KEY (requiremnt_spec_id)
) WITHOUT OIDS;


CREATE TABLE spec.requirement_spec_def_rel
(
	order_no serial NOT NULL,
	requirement_spec_id int NOT NULL,
	req_def_id int NOT NULL,
	PRIMARY KEY (order_no)
) WITHOUT OIDS;



/* Create Foreign Keys */

ALTER TABLE spec.analysis_rc_model_rel
	ADD FOREIGN KEY (model_id)
	REFERENCES spec.analysis_model (model_id)
	ON UPDATE RESTRICT
	ON DELETE RESTRICT
;


ALTER TABLE spec.analysis_spec_rel
	ADD FOREIGN KEY (analysis_spec_id)
	REFERENCES spec.analysis_spec (analysis_spec_id)
	ON UPDATE RESTRICT
	ON DELETE RESTRICT
;


ALTER TABLE spec.analysis_rc_model_rel
	ADD FOREIGN KEY (analysis_id)
	REFERENCES spec.analysis_spec_record (analysis_id)
	ON UPDATE RESTRICT
	ON DELETE RESTRICT
;


ALTER TABLE spec.analysis_spec_rel
	ADD FOREIGN KEY (analysis_id)
	REFERENCES spec.analysis_spec_record (analysis_id)
	ON UPDATE RESTRICT
	ON DELETE RESTRICT
;


ALTER TABLE spec.requirement_def_device
	ADD FOREIGN KEY (req_def_id)
	REFERENCES spec.requirement_def_record (req_def_id)
	ON UPDATE RESTRICT
	ON DELETE RESTRICT
;


ALTER TABLE spec.requirement_spec_def_rel
	ADD FOREIGN KEY (req_def_id)
	REFERENCES spec.requirement_def_record (req_def_id)
	ON UPDATE RESTRICT
	ON DELETE RESTRICT
;


ALTER TABLE spec.requirement_spec_def_rel
	ADD FOREIGN KEY (requirement_spec_id)
	REFERENCES spec.requirement_spec (requiremnt_spec_id)
	ON UPDATE RESTRICT
	ON DELETE RESTRICT
;



/* Create Indexes */

CREATE INDEX analysis_rc_model_rel_idx ON spec.analysis_rc_model_rel USING BTREE (analysis_id, model_id);
CREATE INDEX requirement_spec_def_rel_idx ON spec.requirement_spec_def_rel USING BTREE (requirement_spec_id, req_def_id);



/* Comments */

COMMENT ON COLUMN spec.analysis_model.model IS 'APL ģ��';
COMMENT ON COLUMN spec.analysis_spec.spec_name IS 'ʽ��������';
COMMENT ON COLUMN spec.analysis_spec.ver IS '�汾';
COMMENT ON COLUMN spec.analysis_spec.file_name IS '�ļ�����';
COMMENT ON COLUMN spec.analysis_spec_record.author_name IS '������';
COMMENT ON COLUMN spec.analysis_spec_record.requirement_id IS 'TAGLҪ�����xID';
COMMENT ON COLUMN spec.analysis_spec_record.id IS '����ID';
COMMENT ON COLUMN spec.analysis_spec_record.unique_id IS '��˩`��ID';
COMMENT ON COLUMN spec.analysis_spec_record.medium_catetory IS '�з��';
COMMENT ON COLUMN spec.analysis_spec_record.detail IS 'Ԕ��';
COMMENT ON COLUMN spec.analysis_spec_record.base IS '����Ҫ��';
COMMENT ON COLUMN spec.analysis_spec_record.rel_requiremant IS '�v�B����Ҫ��';
COMMENT ON COLUMN spec.analysis_spec_record.exception IS '����';
COMMENT ON COLUMN spec.analysis_spec_record.dcu_meu IS 'DCU/MEU�ɤ�����붨��';
COMMENT ON COLUMN spec.analysis_spec_record.pf_status IS '״�B';
COMMENT ON COLUMN spec.analysis_spec_record.fp_trigger IS '�ȥꥬ�`';
COMMENT ON COLUMN spec.analysis_spec_record.pf_action IS '����';
COMMENT ON COLUMN spec.analysis_spec_record.seq_diagram IS '���`���󥹇�';
COMMENT ON COLUMN spec.analysis_spec_record.supple_spec IS '�a������˘���';
COMMENT ON COLUMN spec.analysis_spec_record.uncheck IS 'δ���^';
COMMENT ON COLUMN spec.analysis_spec_record.remark IS '�俼';
COMMENT ON TABLE spec.requirement_def_device IS '����ǥХ���----����ʽ����(��ɫ��)';
COMMENT ON TABLE spec.requirement_def_record IS 'Ҫ�����x��';
COMMENT ON COLUMN spec.requirement_def_record.author_name IS '����';
COMMENT ON COLUMN spec.requirement_def_record.hu_def_id IS 'H/UҪ�����xID';
COMMENT ON COLUMN spec.requirement_def_record.requirement_id IS 'Ҫ�����xID -- ����ʽ�����½ں�';
COMMENT ON COLUMN spec.requirement_def_record.unique_id IS '��˩`��ID';
COMMENT ON COLUMN spec.requirement_def_record.major_category IS '����';
COMMENT ON COLUMN spec.requirement_def_record.medium_catetory IS '�з��';
COMMENT ON COLUMN spec.requirement_def_record.small_category IS 'С���';
COMMENT ON COLUMN spec.requirement_def_record.detail IS 'Ԕ��';
COMMENT ON COLUMN spec.requirement_def_record.base IS '����Ҫ��';
COMMENT ON COLUMN spec.requirement_def_record.rel_requiremant IS '�v�B����Ҫ��';
COMMENT ON COLUMN spec.requirement_def_record.dcu_status IS 'DCU-״�B';
COMMENT ON COLUMN spec.requirement_def_record.dcu_trigger IS 'DCU �ȥꥬ�`';
COMMENT ON COLUMN spec.requirement_def_record.dcu_action IS 'DCU ����';
COMMENT ON COLUMN spec.requirement_def_record.meu_status IS 'MEU ״�B';
COMMENT ON COLUMN spec.requirement_def_record.meu_trigger IS 'MEU-�ȥꥬ�`';
COMMENT ON COLUMN spec.requirement_def_record.meu_action IS 'MEU-����';
COMMENT ON COLUMN spec.requirement_def_record.hu_req_remark IS '�俼(HUҪ�����x)';
COMMENT ON COLUMN spec.requirement_def_record.dcu_meu IS 'DCU/MEU�ɤ�����붨��';
COMMENT ON COLUMN spec.requirement_def_record.pf_status IS '״�B';
COMMENT ON COLUMN spec.requirement_def_record.pf_trigger IS '�ȥꥬ�`';
COMMENT ON COLUMN spec.requirement_def_record.pf_action IS '����';
COMMENT ON COLUMN spec.requirement_def_record.remark IS '�俼';
COMMENT ON COLUMN spec.requirement_def_record.notice IS '؟�շֵ�����ӛ���';
COMMENT ON COLUMN spec.requirement_def_record.rel_hal_design IS '�ο�HAL�OӋ��';
COMMENT ON COLUMN spec.requirement_def_record.rel_flow_diagram IS '�ο������`������`��';
COMMENT ON COLUMN spec.requirement_def_record.other_spec IS '�������˘�����ե��ϩ`���˘��ȣ�';
COMMENT ON COLUMN spec.requirement_def_record.implementation IS '��ե���󥹥ϩ`���ϤǤΌg�F�ɷ�';
COMMENT ON COLUMN spec.requirement_def_record.analysis IS 'Ԕ�������ɷ�';
COMMENT ON COLUMN spec.requirement_def_record.unrequire IS 'δҪ������';
COMMENT ON TABLE spec.requirement_spec IS 'Ҫ�����x��';
COMMENT ON COLUMN spec.requirement_spec.proj IS '��Ŀ';
COMMENT ON COLUMN spec.requirement_spec.spec_name IS 'ʽ��������';
COMMENT ON COLUMN spec.requirement_spec.ver IS '�汾';
COMMENT ON COLUMN spec.requirement_spec.file_name IS '�ļ�����';



