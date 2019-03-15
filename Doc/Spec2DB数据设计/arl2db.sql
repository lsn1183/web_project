
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

-- 要件分析
CREATE TABLE spec.analysis
(
	analysis_rc_id serial NOT NULL,
	-- 担当者
	author_name varchar(20),
	-- TAGL要件定義ID
	definition_id varchar(30),
	-- ユニークID
	unique_id int,
	-- 除外
	exception varchar(1024),
	-- シーケンス図
	seq_diagram varchar,
	-- アプリケーション
	application varchar,
	kernel varchar,
	systemd varchar,
	-- 補足参照仕様書
	supple_spec varchar,
	-- 未検証
	uncheck varchar,
	-- 備考
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
	-- APL 模块
	model varchar(100),
	PRIMARY KEY (model_id)
) WITHOUT OIDS;


-- ARL
CREATE TABLE spec.arl
(
	arl_record_id serial NOT NULL,
	-- MMマスターカタスペ新連番
	mm_new_num varchar(50),
	-- 担当グループ
	charge varchar(20),
	-- MMマスターカタスペ記載項目
	mm_item varchar(10),
	-- TAGL対象外
	tagl_exclude varchar(20),
	cat_id0 int,
	-- カテゴリ
	category varchar(128),
	-- ID
	id1 varchar(16),
	cat_id1 int,
	-- 大分類
	major_category varchar(512),
	-- Level1
	Level1 varchar(512),
	id2 varchar(16),
	cat_id2 int,
	-- 中分類
	medium_catetory varchar(512),
	level2 varchar(512),
	id3 varchar(16),
	cat_id3 int,
	-- 小分類
	small_category varchar(512),
	-- Level3
	Level3 varchar(512),
	id4 varchar(16),
	cat_id4 int,
	-- 詳細
	detail varchar(1024),
	-- level4
	level4 varchar(1024),
	-- 機能?開発項目の概要説明
	func_summary_jp varchar(1024),
	-- Summary of Function and Development item
	func_summary_en varchar(1024),
	-- 補足
	supply varchar(128),
	-- SubID
	subid varchar(16),
	-- 要件ID
	arl_id varchar(20),
	-- 転記してきた要件
	req_post varchar,
	-- 備考、不明点
	remark varchar,
	-- 除外
	exception varchar,
	-- 状態
	status varchar(1024),
	-- トリガー
	trigger varchar(1024),
	-- 動作
	action varchar,
	-- ユーザー
	arl_user varchar(2),
	-- ディーラー
	dealer varchar(2),
	-- 開発者
	developer varchar(2),
	-- サプライヤー
	supplier varchar(2),
	-- 社内規定
	company_rule varchar(2),
	-- 法規（自工会等を含む）
	law varchar(2),
	-- 過去不具合対応
	old_bug varchar(2),
	-- 目的、背景、ポリシー
	policy varchar(512),
	-- 仕様書番号
	hmi_spec_no varchar(254),
	-- バージョン
	hmi_version varchar(254),
	-- ファイル名
	hmi_file_name varchar(254),
	-- 章
	hmi_chapter varchar(254),
	-- Page
	hmi_page varchar(254),
	-- 仕様書番号
	func_spec_no varchar(1024),
	-- バージョン
	func_version varchar(1024),
	-- ファイル名
	func_file_name varchar(1024),
	-- 機能仕様書--章
	func_chapter varchar(1024),
	-- Page
	func_page varchar(256),
	-- I/F仕様
	if_spec varchar(1024),
	-- Center仕様
	center_spec varchar(1024),
	-- その他の仕様
	other_spec varchar(1024),
	-- 同件管理
	same_req varchar(1024),
	-- システム構成ID
	sys_conf_id varchar(1024),
	-- 担当
	author varchar(20),
	-- 未要件分析
	future_req varchar(2),
	-- 要件漏れ
	req_omission varchar(2),
	user_id int,
	PRIMARY KEY (arl_record_id)
) WITHOUT OIDS;


-- ARL的种别
CREATE TABLE spec.arl_category
(
	cat_id serial NOT NULL,
	category varchar(1024),
	-- 0: カテゴリ; 1: 大分類; 2: 中分類; 3: 小分類；4: 详细
	level_no int,
	PRIMARY KEY (cat_id)
) WITHOUT OIDS;


CREATE TABLE spec.arl_group
(
	-- 组别ID。 1: 管理员。
	group_id serial NOT NULL,
	group_name varchar(30) NOT NULL,
	PRIMARY KEY (group_id)
) WITHOUT OIDS;


CREATE TABLE spec.arl_group_member
(
	order_id serial NOT NULL,
	-- 组别ID。 1: 管理员。
	group_id int NOT NULL,
	-- 用户ID
	user_id int NOT NULL,
	-- 1: leader、0: member
	role int NOT NULL,
	role_id int NOT NULL,
	PRIMARY KEY (order_id)
) WITHOUT OIDS;


CREATE TABLE spec.arl_log
(
	order_id serial NOT NULL,
	-- 修改者。
	author_id int,
	-- 表单名称。
	table_name varchar(100),
	update_date date DEFAULT now() NOT NULL,
	id int,
	-- IP地址
	ip varchar(20),
	-- 変更理由
	reason varchar(512),
	-- 修改内容。
	content1 varchar,
	-- 修改内容2--当content1存不下时，存到content2.
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
	-- 查看所有记录。 1:是，0:否
	read_all int NOT NULL,
	-- 修改所有记录。 1：是，2：否。
	modify_all int NOT NULL,
	-- 看查组内所有记录。1：是，2：否。 
	read_group int NOT NULL,
	-- 修改组员所有记录。1：是，2：否。 
	modify_group int NOT NULL,
	-- 查看自己的记录。
	read_self int DEFAULT 1 NOT NULL,
	-- 修改自己的记录。
	modify_self int DEFAULT 1 NOT NULL,
	-- 管理组：添加、删除组。
	mng_group int NOT NULL,
	-- 管理组员：添加，删除组员。
	mng_member int NOT NULL,
	PRIMARY KEY (role_id)
) WITHOUT OIDS;


CREATE TABLE spec.arl_user
(
	-- 用户ID
	user_id serial NOT NULL,
	-- 用户名称
	user_name varchar(30) NOT NULL,
	PRIMARY KEY (user_id)
) WITHOUT OIDS;


-- 要件定義書
CREATE TABLE spec.definition
(
	def_rc_id serial NOT NULL,
	-- 担当
	author_name varchar(20),
	-- H/U要件定義ID
	hu_def_id varchar(20),
	-- 要件定義ID -- 机能式样书章节号
	definition_id varchar(30),
	-- ユニークID
	unique_id int,
	exception varchar(1024),
	-- DCU/MEUどちらの想定か
	dcu_meu varchar(1024),
	-- 状態
	pf_status varchar(1024),
	-- トリガー
	pf_trigger varchar(1024),
	-- 動作
	pf_action varchar(1024),
	-- 備考
	remark varchar,
	-- 責務分担の特記事項
	notice varchar,
	-- 参考HAL設計書
	rel_hal_design varchar,
	-- 参考ウォークスルー図
	rel_flow_diagram varchar(1024),
	-- その他仕様（リファハード仕様等）
	other_spec varchar(1024),
	-- リファレンスハード上での実現可否
	implementation varchar(1024),
	-- 詳細分析可否
	analysis varchar(100),
	-- 未要件分析
	unrequire varchar(100),
	user_id int,
	cat_id0 int,
	cat_id1 int,
	cat_id2 int,
	cat_id3 int,
	cat_id4 int,
	PRIMARY KEY (def_rc_id)
) WITHOUT OIDS;


-- 抽象デバイス----定义式样书(绿色列)
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
	-- 要件ID
	arl_id varchar(20) NOT NULL,
	-- H/U要件定義ID
	hu_id varchar(20),
	-- ユニークID
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
	-- システム構成(System configuration)
	system_conf varchar,
	-- 関連基本要件(Related Basic Requirements)
	rel_requirement varchar,
	-- 除外
	exception varchar(1024),
	-- DCU-状態
	dcu_status varchar(1024),
	-- DCU-トリガー
	dcu_trigger varchar(1024),
	-- DCU-動作
	dcu_action varchar(1024),
	-- MEU-状態
	meu_status varchar(1024),
	-- MEU-トリガー
	meu_trigger varchar(1024),
	-- MEU-動作
	meu_action varchar(1024),
	-- H/U分類ID
	hu_category_id varchar(10),
	-- 備考
	remark varchar,
	-- 001 システム仕様書--章Chapter/Section or ページ番号 Page No
	sys_spec_chapter varchar(1024),
	-- 003 共通アプリ?AVC-LAN仕様書--章　Chapter/Section or ページ番号 Page No
	common_chapter varchar(1024),
	-- シーケンス仕様 Sequence spec.
	common_seq_spec varchar(1024),
	-- シーケンス番号Sequence No.
	common_seq_no varchar(1024),
	-- コマンドガイドCommand guide
	common_cmd_guide varchar(1024),
	-- OPC
	common_opc varchar(1024),
	-- 318 DCU-MEU間連携仕様書DCU-MEU interaction spec.--機能配置?機能仕様 Function location and spec.
	inter_loc_spec varchar(1024),
	-- 章　Chapter/Section or ページ番号 Page No
	inter_chapter varchar(1024),
	-- ドキュメント名 ※トヨタ仕様の場合は仕様番号も記載する事
	other_chapter varchar(1024),
	-- その他資料Other document --- 章　Chapter/Section or ページ番号 Page No
	other_doc varchar(1024),
	test_results varchar,
	future_req varchar,
	current_group varchar(30),
	-- TAGL要件提出
	submit varchar(100),
	user_id int,
	PRIMARY KEY (hu_record_id)
) WITHOUT OIDS;


-- 責務分担
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
	-- リアカメラ
	rear_camera varchar(20),
	-- 17MMで存在する組み合わせか
	mm17_exist varchar(20),
	-- システム構成(System configuration)
	system_conf varchar,
	-- システム仕様書記載ページ(最高優先のみ)
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

COMMENT ON TABLE spec.analysis IS '要件分析';
COMMENT ON COLUMN spec.analysis.author_name IS '担当者';
COMMENT ON COLUMN spec.analysis.definition_id IS 'TAGL要件定義ID';
COMMENT ON COLUMN spec.analysis.unique_id IS 'ユニークID';
COMMENT ON COLUMN spec.analysis.exception IS '除外';
COMMENT ON COLUMN spec.analysis.seq_diagram IS 'シーケンス図';
COMMENT ON COLUMN spec.analysis.application IS 'アプリケーション';
COMMENT ON COLUMN spec.analysis.supple_spec IS '補足参照仕様書';
COMMENT ON COLUMN spec.analysis.uncheck IS '未検証';
COMMENT ON COLUMN spec.analysis.remark IS '備考';
COMMENT ON COLUMN spec.analysis_model_type.model IS 'APL 模块';
COMMENT ON TABLE spec.arl IS 'ARL';
COMMENT ON COLUMN spec.arl.mm_new_num IS 'MMマスターカタスペ新連番';
COMMENT ON COLUMN spec.arl.charge IS '担当グループ';
COMMENT ON COLUMN spec.arl.mm_item IS 'MMマスターカタスペ記載項目';
COMMENT ON COLUMN spec.arl.tagl_exclude IS 'TAGL対象外';
COMMENT ON COLUMN spec.arl.category IS 'カテゴリ';
COMMENT ON COLUMN spec.arl.id1 IS 'ID';
COMMENT ON COLUMN spec.arl.major_category IS '大分類';
COMMENT ON COLUMN spec.arl.Level1 IS 'Level1';
COMMENT ON COLUMN spec.arl.medium_catetory IS '中分類';
COMMENT ON COLUMN spec.arl.small_category IS '小分類';
COMMENT ON COLUMN spec.arl.Level3 IS 'Level3';
COMMENT ON COLUMN spec.arl.detail IS '詳細';
COMMENT ON COLUMN spec.arl.level4 IS 'level4';
COMMENT ON COLUMN spec.arl.func_summary_jp IS '機能?開発項目の概要説明';
COMMENT ON COLUMN spec.arl.func_summary_en IS 'Summary of Function and Development item';
COMMENT ON COLUMN spec.arl.supply IS '補足';
COMMENT ON COLUMN spec.arl.subid IS 'SubID';
COMMENT ON COLUMN spec.arl.arl_id IS '要件ID';
COMMENT ON COLUMN spec.arl.req_post IS '転記してきた要件';
COMMENT ON COLUMN spec.arl.remark IS '備考、不明点';
COMMENT ON COLUMN spec.arl.exception IS '除外';
COMMENT ON COLUMN spec.arl.status IS '状態';
COMMENT ON COLUMN spec.arl.trigger IS 'トリガー';
COMMENT ON COLUMN spec.arl.action IS '動作';
COMMENT ON COLUMN spec.arl.arl_user IS 'ユーザー';
COMMENT ON COLUMN spec.arl.dealer IS 'ディーラー';
COMMENT ON COLUMN spec.arl.developer IS '開発者';
COMMENT ON COLUMN spec.arl.supplier IS 'サプライヤー';
COMMENT ON COLUMN spec.arl.company_rule IS '社内規定';
COMMENT ON COLUMN spec.arl.law IS '法規（自工会等を含む）';
COMMENT ON COLUMN spec.arl.old_bug IS '過去不具合対応';
COMMENT ON COLUMN spec.arl.policy IS '目的、背景、ポリシー';
COMMENT ON COLUMN spec.arl.hmi_spec_no IS '仕様書番号';
COMMENT ON COLUMN spec.arl.hmi_version IS 'バージョン';
COMMENT ON COLUMN spec.arl.hmi_file_name IS 'ファイル名';
COMMENT ON COLUMN spec.arl.hmi_chapter IS '章';
COMMENT ON COLUMN spec.arl.hmi_page IS 'Page';
COMMENT ON COLUMN spec.arl.func_spec_no IS '仕様書番号';
COMMENT ON COLUMN spec.arl.func_version IS 'バージョン';
COMMENT ON COLUMN spec.arl.func_file_name IS 'ファイル名';
COMMENT ON COLUMN spec.arl.func_chapter IS '機能仕様書--章';
COMMENT ON COLUMN spec.arl.func_page IS 'Page';
COMMENT ON COLUMN spec.arl.if_spec IS 'I/F仕様';
COMMENT ON COLUMN spec.arl.center_spec IS 'Center仕様';
COMMENT ON COLUMN spec.arl.other_spec IS 'その他の仕様';
COMMENT ON COLUMN spec.arl.same_req IS '同件管理';
COMMENT ON COLUMN spec.arl.sys_conf_id IS 'システム構成ID';
COMMENT ON COLUMN spec.arl.author IS '担当';
COMMENT ON COLUMN spec.arl.future_req IS '未要件分析';
COMMENT ON COLUMN spec.arl.req_omission IS '要件漏れ';
COMMENT ON TABLE spec.arl_category IS 'ARL的种别';
COMMENT ON COLUMN spec.arl_category.level_no IS '0: カテゴリ; 1: 大分類; 2: 中分類; 3: 小分類；4: 详细';
COMMENT ON COLUMN spec.arl_group.group_id IS '组别ID。 1: 管理员。';
COMMENT ON COLUMN spec.arl_group_member.group_id IS '组别ID。 1: 管理员。';
COMMENT ON COLUMN spec.arl_group_member.user_id IS '用户ID';
COMMENT ON COLUMN spec.arl_group_member.role IS '1: leader、0: member';
COMMENT ON COLUMN spec.arl_log.author_id IS '修改者。';
COMMENT ON COLUMN spec.arl_log.table_name IS '表单名称。';
COMMENT ON COLUMN spec.arl_log.ip IS 'IP地址';
COMMENT ON COLUMN spec.arl_log.reason IS '変更理由';
COMMENT ON COLUMN spec.arl_log.content1 IS '修改内容。';
COMMENT ON COLUMN spec.arl_log.content2 IS '修改内容2--当content1存不下时，存到content2.';
COMMENT ON COLUMN spec.arl_role_power.role IS 'Admin / Leader / Member.';
COMMENT ON COLUMN spec.arl_role_power.read_all IS '查看所有记录。 1:是，0:否';
COMMENT ON COLUMN spec.arl_role_power.modify_all IS '修改所有记录。 1：是，2：否。';
COMMENT ON COLUMN spec.arl_role_power.read_group IS '看查组内所有记录。1：是，2：否。 ';
COMMENT ON COLUMN spec.arl_role_power.modify_group IS '修改组员所有记录。1：是，2：否。 ';
COMMENT ON COLUMN spec.arl_role_power.read_self IS '查看自己的记录。';
COMMENT ON COLUMN spec.arl_role_power.modify_self IS '修改自己的记录。';
COMMENT ON COLUMN spec.arl_role_power.mng_group IS '管理组：添加、删除组。';
COMMENT ON COLUMN spec.arl_role_power.mng_member IS '管理组员：添加，删除组员。';
COMMENT ON COLUMN spec.arl_user.user_id IS '用户ID';
COMMENT ON COLUMN spec.arl_user.user_name IS '用户名称';
COMMENT ON TABLE spec.definition IS '要件定義書';
COMMENT ON COLUMN spec.definition.author_name IS '担当';
COMMENT ON COLUMN spec.definition.hu_def_id IS 'H/U要件定義ID';
COMMENT ON COLUMN spec.definition.definition_id IS '要件定義ID -- 机能式样书章节号';
COMMENT ON COLUMN spec.definition.unique_id IS 'ユニークID';
COMMENT ON COLUMN spec.definition.dcu_meu IS 'DCU/MEUどちらの想定か';
COMMENT ON COLUMN spec.definition.pf_status IS '状態';
COMMENT ON COLUMN spec.definition.pf_trigger IS 'トリガー';
COMMENT ON COLUMN spec.definition.pf_action IS '動作';
COMMENT ON COLUMN spec.definition.remark IS '備考';
COMMENT ON COLUMN spec.definition.notice IS '責務分担の特記事項';
COMMENT ON COLUMN spec.definition.rel_hal_design IS '参考HAL設計書';
COMMENT ON COLUMN spec.definition.rel_flow_diagram IS '参考ウォークスルー図';
COMMENT ON COLUMN spec.definition.other_spec IS 'その他仕様（リファハード仕様等）';
COMMENT ON COLUMN spec.definition.implementation IS 'リファレンスハード上での実現可否';
COMMENT ON COLUMN spec.definition.analysis IS '詳細分析可否';
COMMENT ON COLUMN spec.definition.unrequire IS '未要件分析';
COMMENT ON TABLE spec.definition_model_rel IS '抽象デバイス----定义式样书(绿色列)';
COMMENT ON TABLE spec.hu IS 'H/U';
COMMENT ON COLUMN spec.hu.arl_id IS '要件ID';
COMMENT ON COLUMN spec.hu.hu_id IS 'H/U要件定義ID';
COMMENT ON COLUMN spec.hu.unique_id IS 'ユニークID';
COMMENT ON COLUMN spec.hu.system_conf IS 'システム構成(System configuration)';
COMMENT ON COLUMN spec.hu.rel_requirement IS '関連基本要件(Related Basic Requirements)';
COMMENT ON COLUMN spec.hu.exception IS '除外';
COMMENT ON COLUMN spec.hu.dcu_status IS 'DCU-状態';
COMMENT ON COLUMN spec.hu.dcu_trigger IS 'DCU-トリガー';
COMMENT ON COLUMN spec.hu.dcu_action IS 'DCU-動作';
COMMENT ON COLUMN spec.hu.meu_status IS 'MEU-状態';
COMMENT ON COLUMN spec.hu.meu_trigger IS 'MEU-トリガー';
COMMENT ON COLUMN spec.hu.meu_action IS 'MEU-動作';
COMMENT ON COLUMN spec.hu.hu_category_id IS 'H/U分類ID';
COMMENT ON COLUMN spec.hu.remark IS '備考';
COMMENT ON COLUMN spec.hu.sys_spec_chapter IS '001 システム仕様書--章Chapter/Section or ページ番号 Page No';
COMMENT ON COLUMN spec.hu.common_chapter IS '003 共通アプリ?AVC-LAN仕様書--章　Chapter/Section or ページ番号 Page No';
COMMENT ON COLUMN spec.hu.common_seq_spec IS 'シーケンス仕様 Sequence spec.';
COMMENT ON COLUMN spec.hu.common_seq_no IS 'シーケンス番号Sequence No.';
COMMENT ON COLUMN spec.hu.common_cmd_guide IS 'コマンドガイドCommand guide';
COMMENT ON COLUMN spec.hu.common_opc IS 'OPC';
COMMENT ON COLUMN spec.hu.inter_loc_spec IS '318 DCU-MEU間連携仕様書DCU-MEU interaction spec.--機能配置?機能仕様 Function location and spec.';
COMMENT ON COLUMN spec.hu.inter_chapter IS '章　Chapter/Section or ページ番号 Page No';
COMMENT ON COLUMN spec.hu.other_chapter IS 'ドキュメント名 ※トヨタ仕様の場合は仕様番号も記載する事';
COMMENT ON COLUMN spec.hu.other_doc IS 'その他資料Other document --- 章　Chapter/Section or ページ番号 Page No';
COMMENT ON COLUMN spec.hu.submit IS 'TAGL要件提出';
COMMENT ON TABLE spec.hu_model_rel IS '責務分担';
COMMENT ON COLUMN spec.hu_option_item.amp IS 'AMP';
COMMENT ON COLUMN spec.hu_option_item.dsrc IS 'DSRC';
COMMENT ON COLUMN spec.hu_option_item.dcm IS 'DCM';
COMMENT ON COLUMN spec.hu_option_item.rse IS 'RSE';
COMMENT ON COLUMN spec.hu_option_item.rear_camera IS 'リアカメラ';
COMMENT ON COLUMN spec.hu_option_item.mm17_exist IS '17MMで存在する組み合わせか';
COMMENT ON COLUMN spec.hu_option_item.system_conf IS 'システム構成(System configuration)';
COMMENT ON COLUMN spec.hu_option_item.page IS 'システム仕様書記載ページ(最高優先のみ)';



