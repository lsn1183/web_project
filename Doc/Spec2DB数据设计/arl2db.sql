
/* Drop Indexes */

DROP INDEX IF EXISTS analysis_definition_id_idx;
DROP INDEX IF EXISTS analysis_rc_model_rel_idx;
DROP INDEX IF EXISTS arl_cat_id0_cat_id1_cat_id2_cat_id3_cat_id4_idx;
DROP INDEX IF EXISTS arl_arl_id_idx;
DROP INDEX IF EXISTS arl_user_id_idx;
DROP INDEX IF EXISTS arl_group_member_group_id_user_id_idx;
DROP INDEX IF EXISTS definition_definition_id_idx;



/* Drop Tables */

DROP TABLE IF EXISTS spec.analysis_model_rel;
DROP TABLE IF EXISTS spec.analysis;
DROP TABLE IF EXISTS spec.analysis_model_type;
DROP TABLE IF EXISTS spec.arl_model_rel;
DROP TABLE IF EXISTS spec.arl;
DROP TABLE IF EXISTS spec.arl_category;
DROP TABLE IF EXISTS spec.arl_group_member;
DROP TABLE IF EXISTS spec.arl_group;
DROP TABLE IF EXISTS spec.arl_log;
DROP TABLE IF EXISTS spec.arl_model_type;
DROP TABLE IF EXISTS spec.arl_role_power;
DROP TABLE IF EXISTS spec.arl_user;
DROP TABLE IF EXISTS spec.definition_model_rel;
DROP TABLE IF EXISTS spec.definition;
DROP TABLE IF EXISTS spec.definition_model_type;
DROP TABLE IF EXISTS spec.hu_model_rel;
DROP TABLE IF EXISTS spec.hu;
DROP TABLE IF EXISTS spec.hu_model_type;
DROP TABLE IF EXISTS spec.hu_option_item;




/* Create Tables */

-- Ҫ������
CREATE TABLE spec.analysis
(
	analysis_rc_id serial NOT NULL,
	-- ������
	author_name varchar(20),
	-- TAGLҪ�����xID
	definition_id varchar(30),
	-- ��˩`��ID
	unique_id int,
	-- ����
	exception varchar(1024),
	-- ���`���󥹇�
	seq_diagram varchar,
	-- ���ץꥱ�`�����
	application varchar,
	kernel varchar,
	systemd varchar,
	-- �a������˘���
	supple_spec varchar,
	-- δ���^
	uncheck varchar,
	-- �俼
	remark varchar,
	user_id int,
	cat_id0 int,
	cat_id1 int,
	cat_id2 int,
	cat_id3 int,
	cat_id4 int,
	PRIMARY KEY (analysis_rc_id)
) WITHOUT OIDS;


CREATE TABLE spec.analysis_model_rel
(
	order_no serial NOT NULL,
	analysis_rc_id int NOT NULL,
	model_id int NOT NULL,
	val varchar,
	PRIMARY KEY (order_no)
) WITHOUT OIDS;


CREATE TABLE spec.analysis_model_type
(
	model_id serial NOT NULL,
	-- APL ģ��
	model varchar(100),
	PRIMARY KEY (model_id)
) WITHOUT OIDS;


-- ARL
CREATE TABLE spec.arl
(
	arl_record_id serial NOT NULL,
	-- MM�ޥ����`�����������B��
	mm_new_num varchar(50),
	-- ��������`��
	charge varchar(20),
	-- MM�ޥ����`��������ӛ�d�Ŀ
	mm_item varchar(10),
	-- TAGL������
	tagl_exclude varchar(20),
	cat_id0 int,
	-- ���ƥ���
	category varchar(128),
	-- ID
	id1 varchar(16),
	cat_id1 int,
	-- ����
	major_category varchar(512),
	-- Level1
	Level1 varchar(512),
	id2 varchar(16),
	cat_id2 int,
	-- �з��
	medium_catetory varchar(512),
	level2 varchar(512),
	id3 varchar(16),
	cat_id3 int,
	-- С���
	small_category varchar(512),
	-- Level3
	Level3 varchar(512),
	id4 varchar(16),
	cat_id4 int,
	-- Ԕ��
	detail varchar(1024),
	-- level4
	level4 varchar(1024),
	-- �C��?�_�k�Ŀ�θ�Ҫ�h��
	func_summary_jp varchar(1024),
	-- Summary of Function and Development item
	func_summary_en varchar(1024),
	-- �a��
	supply varchar(128),
	-- SubID
	subid varchar(16),
	-- Ҫ��ID
	arl_id varchar(20),
	-- ܞӛ���Ƥ���Ҫ��
	req_post varchar,
	-- �俼��������
	remark varchar,
	-- ����
	exception varchar,
	-- ״�B
	status varchar(1024),
	-- �ȥꥬ�`
	trigger varchar(1024),
	-- ����
	action varchar,
	-- ��`���`
	arl_user varchar(2),
	-- �ǥ��`��`
	dealer varchar(2),
	-- �_�k��
	developer varchar(2),
	-- ���ץ饤��`
	supplier varchar(2),
	-- ����Ҏ��
	company_rule varchar(2),
	-- ��Ҏ���Թ���Ȥ򺬤ࣩ
	law varchar(2),
	-- �^ȥ���ߺό���
	old_bug varchar(2),
	-- Ŀ�ġ��������ݥꥷ�`
	policy varchar(512),
	-- �˘�������
	hmi_spec_no varchar(254),
	-- �Щ`�����
	hmi_version varchar(254),
	-- �ե�������
	hmi_file_name varchar(254),
	-- ��
	hmi_chapter varchar(254),
	-- Page
	hmi_page varchar(254),
	-- �˘�������
	func_spec_no varchar(1024),
	-- �Щ`�����
	func_version varchar(1024),
	-- �ե�������
	func_file_name varchar(1024),
	-- �C���˘���--��
	func_chapter varchar(1024),
	-- Page
	func_page varchar(256),
	-- I/F�˘�
	if_spec varchar(1024),
	-- Center�˘�
	center_spec varchar(1024),
	-- ���������˘�
	other_spec varchar(1024),
	-- ͬ������
	same_req varchar(1024),
	-- �����ƥ�����ID
	sys_conf_id varchar(1024),
	-- ����
	author varchar(20),
	-- δҪ������
	future_req varchar(2),
	-- Ҫ��©��
	req_omission varchar(2),
	user_id int,
	PRIMARY KEY (arl_record_id)
) WITHOUT OIDS;


-- ARL���ֱ�
CREATE TABLE spec.arl_category
(
	cat_id serial NOT NULL,
	category varchar(1024),
	-- 0: ���ƥ���; 1: ����; 2: �з��; 3: С���4: ��ϸ
	level_no int,
	PRIMARY KEY (cat_id)
) WITHOUT OIDS;


CREATE TABLE spec.arl_group
(
	-- ���ID�� 1: ����Ա��
	group_id serial NOT NULL,
	group_name varchar(30) NOT NULL,
	PRIMARY KEY (group_id)
) WITHOUT OIDS;


CREATE TABLE spec.arl_group_member
(
	order_id serial NOT NULL,
	-- ���ID�� 1: ����Ա��
	group_id int NOT NULL,
	-- �û�ID
	user_id int NOT NULL,
	-- 1: leader��0: member
	role int NOT NULL,
	role_id int NOT NULL,
	PRIMARY KEY (order_id)
) WITHOUT OIDS;


CREATE TABLE spec.arl_log
(
	order_id serial NOT NULL,
	-- �޸��ߡ�
	author_id int,
	-- �����ơ�
	table_name varchar(100),
	update_date date DEFAULT now() NOT NULL,
	id int,
	-- IP��ַ
	ip varchar(20),
	-- �������
	reason varchar(512),
	-- �޸����ݡ�
	content1 varchar,
	-- �޸�����2--��content1�治��ʱ���浽content2.
	content2 varchar,
	PRIMARY KEY (order_id)
) WITHOUT OIDS;


CREATE TABLE spec.arl_model_rel
(
	order_no serial,
	arl_record_id int NOT NULL,
	model_id int NOT NULL,
	val varchar(512)
) WITHOUT OIDS;


CREATE TABLE spec.arl_model_type
(
	model_id serial NOT NULL,
	model varchar,
	PRIMARY KEY (model_id)
) WITHOUT OIDS;


CREATE TABLE spec.arl_role_power
(
	role_id serial NOT NULL,
	-- Admin / Leader / Member.
	role varchar(30) NOT NULL,
	-- �鿴���м�¼�� 1:�ǣ�0:��
	read_all int NOT NULL,
	-- �޸����м�¼�� 1���ǣ�2����
	modify_all int NOT NULL,
	-- �����������м�¼��1���ǣ�2���� 
	read_group int NOT NULL,
	-- �޸���Ա���м�¼��1���ǣ�2���� 
	modify_group int NOT NULL,
	-- �鿴�Լ��ļ�¼��
	read_self int DEFAULT 1 NOT NULL,
	-- �޸��Լ��ļ�¼��
	modify_self int DEFAULT 1 NOT NULL,
	-- �����飺��ӡ�ɾ���顣
	mng_group int NOT NULL,
	-- ������Ա����ӣ�ɾ����Ա��
	mng_member int NOT NULL,
	PRIMARY KEY (role_id)
) WITHOUT OIDS;


CREATE TABLE spec.arl_user
(
	-- �û�ID
	user_id serial NOT NULL,
	-- �û�����
	user_name varchar(30) NOT NULL,
	PRIMARY KEY (user_id)
) WITHOUT OIDS;


-- Ҫ�����x��
CREATE TABLE spec.definition
(
	def_rc_id serial NOT NULL,
	-- ����
	author_name varchar(20),
	-- H/UҪ�����xID
	hu_def_id varchar(20),
	-- Ҫ�����xID -- ����ʽ�����½ں�
	definition_id varchar(30),
	-- ��˩`��ID
	unique_id int,
	exception varchar(1024),
	-- DCU/MEU�ɤ�����붨��
	dcu_meu varchar(1024),
	-- ״�B
	pf_status varchar(1024),
	-- �ȥꥬ�`
	pf_trigger varchar(1024),
	-- ����
	pf_action varchar(1024),
	-- �俼
	remark varchar,
	-- ؟�շֵ�����ӛ���
	notice varchar,
	-- �ο�HAL�OӋ��
	rel_hal_design varchar,
	-- �ο������`������`��
	rel_flow_diagram varchar(1024),
	-- �������˘�����ե��ϩ`���˘��ȣ�
	other_spec varchar(1024),
	-- ��ե���󥹥ϩ`���ϤǤΌg�F�ɷ�
	implementation varchar(1024),
	-- Ԕ�������ɷ�
	analysis varchar(100),
	-- δҪ������
	unrequire varchar(100),
	user_id int,
	cat_id0 int,
	cat_id1 int,
	cat_id2 int,
	cat_id3 int,
	cat_id4 int,
	PRIMARY KEY (def_rc_id)
) WITHOUT OIDS;


-- ����ǥХ���----����ʽ����(��ɫ��)
CREATE TABLE spec.definition_model_rel
(
	order_no serial,
	def_rc_id int,
	model_id int NOT NULL,
	val varchar(512)
) WITHOUT OIDS;


CREATE TABLE spec.definition_model_type
(
	model_id serial NOT NULL,
	model varchar(100),
	PRIMARY KEY (model_id)
) WITHOUT OIDS;


-- H/U
CREATE TABLE spec.hu
(
	hu_record_id serial NOT NULL,
	author varchar,
	-- Ҫ��ID
	arl_id varchar(20) NOT NULL,
	-- H/UҪ�����xID
	hu_id varchar(20),
	-- ��˩`��ID
	unique_id int,
	cat_id0 int,
	cat_id1 int,
	cat_id2 int,
	cat_id3 int,
	cat_id4 int,
	amp varchar,
	dsrc varchar,
	dcm varchar,
	rse varchar,
	touch_pad varchar,
	separate_disp varchar,
	-- �����ƥ�����(System configuration)
	system_conf varchar,
	-- �v�B����Ҫ��(Related Basic Requirements)
	rel_requirement varchar,
	-- ����
	exception varchar(1024),
	-- DCU-״�B
	dcu_status varchar(1024),
	-- DCU-�ȥꥬ�`
	dcu_trigger varchar(1024),
	-- DCU-����
	dcu_action varchar(1024),
	-- MEU-״�B
	meu_status varchar(1024),
	-- MEU-�ȥꥬ�`
	meu_trigger varchar(1024),
	-- MEU-����
	meu_action varchar(1024),
	-- H/U���ID
	hu_category_id varchar(10),
	-- �俼
	remark varchar,
	-- 001 �����ƥ��˘���--��Chapter/Section or �ک`������ Page No
	sys_spec_chapter varchar(1024),
	-- 003 ��ͨ���ץ�?AVC-LAN�˘���--�¡�Chapter/Section or �ک`������ Page No
	common_chapter varchar(1024),
	-- ���`�����˘� Sequence spec.
	common_seq_spec varchar(1024),
	-- ���`���󥹷���Sequence No.
	common_seq_no varchar(1024),
	-- ���ޥ�ɥ�����Command guide
	common_cmd_guide varchar(1024),
	-- OPC
	common_opc varchar(1024),
	-- 318 DCU-MEU�g�BЯ�˘���DCU-MEU interaction spec.--�C������?�C���˘� Function location and spec.
	inter_loc_spec varchar(1024),
	-- �¡�Chapter/Section or �ک`������ Page No
	inter_chapter varchar(1024),
	-- �ɥ�������� ���ȥ西�˘��Έ��Ϥ��˘����Ť�ӛ�d������
	other_chapter varchar(1024),
	-- �������Y��Other document --- �¡�Chapter/Section or �ک`������ Page No
	other_doc varchar(1024),
	test_results varchar,
	future_req varchar,
	current_group varchar(30),
	-- TAGLҪ�����
	submit varchar(100),
	user_id int,
	PRIMARY KEY (hu_record_id)
) WITHOUT OIDS;


-- ؟�շֵ�
CREATE TABLE spec.hu_model_rel
(
	order_no serial NOT NULL,
	hu_record_id int NOT NULL,
	model_id int NOT NULL,
	val varchar(512),
	PRIMARY KEY (order_no)
) WITHOUT OIDS;


CREATE TABLE spec.hu_model_type
(
	model_id serial NOT NULL,
	model varchar,
	PRIMARY KEY (model_id)
) WITHOUT OIDS;


CREATE TABLE spec.hu_option_item
(
	id int,
	-- AMP
	amp varchar(20),
	-- DSRC
	dsrc varchar(20),
	-- DCM
	dcm varchar(20),
	-- RSE
	rse varchar(20),
	touch_pad varchar(20),
	separate_disp varchar(20),
	-- �ꥢ�����
	rear_camera varchar(20),
	-- 17MM�Ǵ��ڤ���M�ߺϤ碌��
	mm17_exist varchar(20),
	-- �����ƥ�����(System configuration)
	system_conf varchar,
	-- �����ƥ��˘���ӛ�d�ک`��(��߃��ȤΤ�)
	page varchar(20)
) WITHOUT OIDS;



/* Create Foreign Keys */

ALTER TABLE spec.analysis_model_rel
	ADD FOREIGN KEY (analysis_rc_id)
	REFERENCES spec.analysis (analysis_rc_id)
	ON UPDATE RESTRICT
	ON DELETE RESTRICT
;


ALTER TABLE spec.analysis_model_rel
	ADD FOREIGN KEY (model_id)
	REFERENCES spec.analysis_model_type (model_id)
	ON UPDATE RESTRICT
	ON DELETE RESTRICT
;


ALTER TABLE spec.arl_model_rel
	ADD FOREIGN KEY (arl_record_id)
	REFERENCES spec.arl (arl_record_id)
	ON UPDATE RESTRICT
	ON DELETE RESTRICT
;


ALTER TABLE spec.arl_group_member
	ADD FOREIGN KEY (group_id)
	REFERENCES spec.arl_group (group_id)
	ON UPDATE RESTRICT
	ON DELETE RESTRICT
;


ALTER TABLE spec.arl_model_rel
	ADD FOREIGN KEY (model_id)
	REFERENCES spec.arl_model_type (model_id)
	ON UPDATE RESTRICT
	ON DELETE RESTRICT
;


ALTER TABLE spec.arl_group_member
	ADD FOREIGN KEY (user_id)
	REFERENCES spec.arl_user (user_id)
	ON UPDATE RESTRICT
	ON DELETE RESTRICT
;


ALTER TABLE spec.definition_model_rel
	ADD FOREIGN KEY (def_rc_id)
	REFERENCES spec.definition (def_rc_id)
	ON UPDATE RESTRICT
	ON DELETE RESTRICT
;


ALTER TABLE spec.definition_model_rel
	ADD FOREIGN KEY (model_id)
	REFERENCES spec.definition_model_type (model_id)
	ON UPDATE RESTRICT
	ON DELETE RESTRICT
;


ALTER TABLE spec.hu_model_rel
	ADD FOREIGN KEY (hu_record_id)
	REFERENCES spec.hu (hu_record_id)
	ON UPDATE RESTRICT
	ON DELETE RESTRICT
;


ALTER TABLE spec.hu_model_rel
	ADD FOREIGN KEY (model_id)
	REFERENCES spec.hu_model_type (model_id)
	ON UPDATE RESTRICT
	ON DELETE RESTRICT
;



/* Create Indexes */

CREATE INDEX analysis_definition_id_idx ON spec.analysis USING BTREE (definition_id);
CREATE INDEX analysis_rc_model_rel_idx ON spec.analysis_model_rel USING BTREE (analysis_rc_id);
CREATE INDEX arl_cat_id0_cat_id1_cat_id2_cat_id3_cat_id4_idx ON spec.arl USING BTREE (cat_id0, cat_id1, cat_id2, cat_id3, cat_id4);
CREATE INDEX arl_arl_id_idx ON spec.arl USING BTREE (arl_id);
CREATE INDEX arl_user_id_idx ON spec.arl USING BTREE (user_id);
CREATE INDEX arl_group_member_group_id_user_id_idx ON spec.arl_group_member USING BTREE (group_id, user_id);
CREATE INDEX definition_definition_id_idx ON spec.definition USING BTREE (definition_id);



/* Comments */

COMMENT ON TABLE spec.analysis IS 'Ҫ������';
COMMENT ON COLUMN spec.analysis.author_name IS '������';
COMMENT ON COLUMN spec.analysis.definition_id IS 'TAGLҪ�����xID';
COMMENT ON COLUMN spec.analysis.unique_id IS '��˩`��ID';
COMMENT ON COLUMN spec.analysis.exception IS '����';
COMMENT ON COLUMN spec.analysis.seq_diagram IS '���`���󥹇�';
COMMENT ON COLUMN spec.analysis.application IS '���ץꥱ�`�����';
COMMENT ON COLUMN spec.analysis.supple_spec IS '�a������˘���';
COMMENT ON COLUMN spec.analysis.uncheck IS 'δ���^';
COMMENT ON COLUMN spec.analysis.remark IS '�俼';
COMMENT ON COLUMN spec.analysis_model_type.model IS 'APL ģ��';
COMMENT ON TABLE spec.arl IS 'ARL';
COMMENT ON COLUMN spec.arl.mm_new_num IS 'MM�ޥ����`�����������B��';
COMMENT ON COLUMN spec.arl.charge IS '��������`��';
COMMENT ON COLUMN spec.arl.mm_item IS 'MM�ޥ����`��������ӛ�d�Ŀ';
COMMENT ON COLUMN spec.arl.tagl_exclude IS 'TAGL������';
COMMENT ON COLUMN spec.arl.category IS '���ƥ���';
COMMENT ON COLUMN spec.arl.id1 IS 'ID';
COMMENT ON COLUMN spec.arl.major_category IS '����';
COMMENT ON COLUMN spec.arl.Level1 IS 'Level1';
COMMENT ON COLUMN spec.arl.medium_catetory IS '�з��';
COMMENT ON COLUMN spec.arl.small_category IS 'С���';
COMMENT ON COLUMN spec.arl.Level3 IS 'Level3';
COMMENT ON COLUMN spec.arl.detail IS 'Ԕ��';
COMMENT ON COLUMN spec.arl.level4 IS 'level4';
COMMENT ON COLUMN spec.arl.func_summary_jp IS '�C��?�_�k�Ŀ�θ�Ҫ�h��';
COMMENT ON COLUMN spec.arl.func_summary_en IS 'Summary of Function and Development item';
COMMENT ON COLUMN spec.arl.supply IS '�a��';
COMMENT ON COLUMN spec.arl.subid IS 'SubID';
COMMENT ON COLUMN spec.arl.arl_id IS 'Ҫ��ID';
COMMENT ON COLUMN spec.arl.req_post IS 'ܞӛ���Ƥ���Ҫ��';
COMMENT ON COLUMN spec.arl.remark IS '�俼��������';
COMMENT ON COLUMN spec.arl.exception IS '����';
COMMENT ON COLUMN spec.arl.status IS '״�B';
COMMENT ON COLUMN spec.arl.trigger IS '�ȥꥬ�`';
COMMENT ON COLUMN spec.arl.action IS '����';
COMMENT ON COLUMN spec.arl.arl_user IS '��`���`';
COMMENT ON COLUMN spec.arl.dealer IS '�ǥ��`��`';
COMMENT ON COLUMN spec.arl.developer IS '�_�k��';
COMMENT ON COLUMN spec.arl.supplier IS '���ץ饤��`';
COMMENT ON COLUMN spec.arl.company_rule IS '����Ҏ��';
COMMENT ON COLUMN spec.arl.law IS '��Ҏ���Թ���Ȥ򺬤ࣩ';
COMMENT ON COLUMN spec.arl.old_bug IS '�^ȥ���ߺό���';
COMMENT ON COLUMN spec.arl.policy IS 'Ŀ�ġ��������ݥꥷ�`';
COMMENT ON COLUMN spec.arl.hmi_spec_no IS '�˘�������';
COMMENT ON COLUMN spec.arl.hmi_version IS '�Щ`�����';
COMMENT ON COLUMN spec.arl.hmi_file_name IS '�ե�������';
COMMENT ON COLUMN spec.arl.hmi_chapter IS '��';
COMMENT ON COLUMN spec.arl.hmi_page IS 'Page';
COMMENT ON COLUMN spec.arl.func_spec_no IS '�˘�������';
COMMENT ON COLUMN spec.arl.func_version IS '�Щ`�����';
COMMENT ON COLUMN spec.arl.func_file_name IS '�ե�������';
COMMENT ON COLUMN spec.arl.func_chapter IS '�C���˘���--��';
COMMENT ON COLUMN spec.arl.func_page IS 'Page';
COMMENT ON COLUMN spec.arl.if_spec IS 'I/F�˘�';
COMMENT ON COLUMN spec.arl.center_spec IS 'Center�˘�';
COMMENT ON COLUMN spec.arl.other_spec IS '���������˘�';
COMMENT ON COLUMN spec.arl.same_req IS 'ͬ������';
COMMENT ON COLUMN spec.arl.sys_conf_id IS '�����ƥ�����ID';
COMMENT ON COLUMN spec.arl.author IS '����';
COMMENT ON COLUMN spec.arl.future_req IS 'δҪ������';
COMMENT ON COLUMN spec.arl.req_omission IS 'Ҫ��©��';
COMMENT ON TABLE spec.arl_category IS 'ARL���ֱ�';
COMMENT ON COLUMN spec.arl_category.level_no IS '0: ���ƥ���; 1: ����; 2: �з��; 3: С���4: ��ϸ';
COMMENT ON COLUMN spec.arl_group.group_id IS '���ID�� 1: ����Ա��';
COMMENT ON COLUMN spec.arl_group_member.group_id IS '���ID�� 1: ����Ա��';
COMMENT ON COLUMN spec.arl_group_member.user_id IS '�û�ID';
COMMENT ON COLUMN spec.arl_group_member.role IS '1: leader��0: member';
COMMENT ON COLUMN spec.arl_log.author_id IS '�޸��ߡ�';
COMMENT ON COLUMN spec.arl_log.table_name IS '�����ơ�';
COMMENT ON COLUMN spec.arl_log.ip IS 'IP��ַ';
COMMENT ON COLUMN spec.arl_log.reason IS '�������';
COMMENT ON COLUMN spec.arl_log.content1 IS '�޸����ݡ�';
COMMENT ON COLUMN spec.arl_log.content2 IS '�޸�����2--��content1�治��ʱ���浽content2.';
COMMENT ON COLUMN spec.arl_role_power.role IS 'Admin / Leader / Member.';
COMMENT ON COLUMN spec.arl_role_power.read_all IS '�鿴���м�¼�� 1:�ǣ�0:��';
COMMENT ON COLUMN spec.arl_role_power.modify_all IS '�޸����м�¼�� 1���ǣ�2����';
COMMENT ON COLUMN spec.arl_role_power.read_group IS '�����������м�¼��1���ǣ�2���� ';
COMMENT ON COLUMN spec.arl_role_power.modify_group IS '�޸���Ա���м�¼��1���ǣ�2���� ';
COMMENT ON COLUMN spec.arl_role_power.read_self IS '�鿴�Լ��ļ�¼��';
COMMENT ON COLUMN spec.arl_role_power.modify_self IS '�޸��Լ��ļ�¼��';
COMMENT ON COLUMN spec.arl_role_power.mng_group IS '�����飺��ӡ�ɾ���顣';
COMMENT ON COLUMN spec.arl_role_power.mng_member IS '������Ա����ӣ�ɾ����Ա��';
COMMENT ON COLUMN spec.arl_user.user_id IS '�û�ID';
COMMENT ON COLUMN spec.arl_user.user_name IS '�û�����';
COMMENT ON TABLE spec.definition IS 'Ҫ�����x��';
COMMENT ON COLUMN spec.definition.author_name IS '����';
COMMENT ON COLUMN spec.definition.hu_def_id IS 'H/UҪ�����xID';
COMMENT ON COLUMN spec.definition.definition_id IS 'Ҫ�����xID -- ����ʽ�����½ں�';
COMMENT ON COLUMN spec.definition.unique_id IS '��˩`��ID';
COMMENT ON COLUMN spec.definition.dcu_meu IS 'DCU/MEU�ɤ�����붨��';
COMMENT ON COLUMN spec.definition.pf_status IS '״�B';
COMMENT ON COLUMN spec.definition.pf_trigger IS '�ȥꥬ�`';
COMMENT ON COLUMN spec.definition.pf_action IS '����';
COMMENT ON COLUMN spec.definition.remark IS '�俼';
COMMENT ON COLUMN spec.definition.notice IS '؟�շֵ�����ӛ���';
COMMENT ON COLUMN spec.definition.rel_hal_design IS '�ο�HAL�OӋ��';
COMMENT ON COLUMN spec.definition.rel_flow_diagram IS '�ο������`������`��';
COMMENT ON COLUMN spec.definition.other_spec IS '�������˘�����ե��ϩ`���˘��ȣ�';
COMMENT ON COLUMN spec.definition.implementation IS '��ե���󥹥ϩ`���ϤǤΌg�F�ɷ�';
COMMENT ON COLUMN spec.definition.analysis IS 'Ԕ�������ɷ�';
COMMENT ON COLUMN spec.definition.unrequire IS 'δҪ������';
COMMENT ON TABLE spec.definition_model_rel IS '����ǥХ���----����ʽ����(��ɫ��)';
COMMENT ON TABLE spec.hu IS 'H/U';
COMMENT ON COLUMN spec.hu.arl_id IS 'Ҫ��ID';
COMMENT ON COLUMN spec.hu.hu_id IS 'H/UҪ�����xID';
COMMENT ON COLUMN spec.hu.unique_id IS '��˩`��ID';
COMMENT ON COLUMN spec.hu.system_conf IS '�����ƥ�����(System configuration)';
COMMENT ON COLUMN spec.hu.rel_requirement IS '�v�B����Ҫ��(Related Basic Requirements)';
COMMENT ON COLUMN spec.hu.exception IS '����';
COMMENT ON COLUMN spec.hu.dcu_status IS 'DCU-״�B';
COMMENT ON COLUMN spec.hu.dcu_trigger IS 'DCU-�ȥꥬ�`';
COMMENT ON COLUMN spec.hu.dcu_action IS 'DCU-����';
COMMENT ON COLUMN spec.hu.meu_status IS 'MEU-״�B';
COMMENT ON COLUMN spec.hu.meu_trigger IS 'MEU-�ȥꥬ�`';
COMMENT ON COLUMN spec.hu.meu_action IS 'MEU-����';
COMMENT ON COLUMN spec.hu.hu_category_id IS 'H/U���ID';
COMMENT ON COLUMN spec.hu.remark IS '�俼';
COMMENT ON COLUMN spec.hu.sys_spec_chapter IS '001 �����ƥ��˘���--��Chapter/Section or �ک`������ Page No';
COMMENT ON COLUMN spec.hu.common_chapter IS '003 ��ͨ���ץ�?AVC-LAN�˘���--�¡�Chapter/Section or �ک`������ Page No';
COMMENT ON COLUMN spec.hu.common_seq_spec IS '���`�����˘� Sequence spec.';
COMMENT ON COLUMN spec.hu.common_seq_no IS '���`���󥹷���Sequence No.';
COMMENT ON COLUMN spec.hu.common_cmd_guide IS '���ޥ�ɥ�����Command guide';
COMMENT ON COLUMN spec.hu.common_opc IS 'OPC';
COMMENT ON COLUMN spec.hu.inter_loc_spec IS '318 DCU-MEU�g�BЯ�˘���DCU-MEU interaction spec.--�C������?�C���˘� Function location and spec.';
COMMENT ON COLUMN spec.hu.inter_chapter IS '�¡�Chapter/Section or �ک`������ Page No';
COMMENT ON COLUMN spec.hu.other_chapter IS '�ɥ�������� ���ȥ西�˘��Έ��Ϥ��˘����Ť�ӛ�d������';
COMMENT ON COLUMN spec.hu.other_doc IS '�������Y��Other document --- �¡�Chapter/Section or �ک`������ Page No';
COMMENT ON COLUMN spec.hu.submit IS 'TAGLҪ�����';
COMMENT ON TABLE spec.hu_model_rel IS '؟�շֵ�';
COMMENT ON COLUMN spec.hu_option_item.amp IS 'AMP';
COMMENT ON COLUMN spec.hu_option_item.dsrc IS 'DSRC';
COMMENT ON COLUMN spec.hu_option_item.dcm IS 'DCM';
COMMENT ON COLUMN spec.hu_option_item.rse IS 'RSE';
COMMENT ON COLUMN spec.hu_option_item.rear_camera IS '�ꥢ�����';
COMMENT ON COLUMN spec.hu_option_item.mm17_exist IS '17MM�Ǵ��ڤ���M�ߺϤ碌��';
COMMENT ON COLUMN spec.hu_option_item.system_conf IS '�����ƥ�����(System configuration)';
COMMENT ON COLUMN spec.hu_option_item.page IS '�����ƥ��˘���ӛ�d�ک`��(��߃��ȤΤ�)';



