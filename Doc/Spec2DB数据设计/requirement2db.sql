
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
	-- APL 模块
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
	-- 式样书名称
	spec_name varchar,
	-- 版本
	ver varchar,
	-- 文件名称
	file_name varchar,
	PRIMARY KEY (analysis_spec_id)
) WITHOUT OIDS;


CREATE TABLE spec.analysis_spec_record
(
	analysis_id serial NOT NULL,
	-- 担当者
	author_name varchar(20),
	-- TAGL要件定義ID
	requirement_id varchar(20),
	spec_chapter_num varchar(20),
	-- 机能ID
	id varchar(20),
	-- ユニークID
	unique_id int,
	major_category varchar(20),
	-- 中分類
	medium_catetory varchar(20),
	small_category varchar(30),
	-- 詳細
	detail varchar(512),
	-- 基本要件
	base varchar(32),
	-- 関連基本要件
	rel_requiremant varchar(256),
	-- 除外
	exception varchar(32),
	-- DCU/MEUどちらの想定か
	dcu_meu varchar(256),
	-- 状態
	pf_status varchar(256),
	-- トリガー
	fp_trigger varchar(512),
	-- 動作
	pf_action varchar(512),
	-- シーケンス図
	seq_diagram varchar,
	application varchar,
	kernel varchar,
	systemd varchar,
	-- 補足参照仕様書
	supple_spec varchar,
	-- 未検証
	uncheck varchar,
	-- 備考
	remark varchar,
	PRIMARY KEY (analysis_id)
) WITHOUT OIDS;


CREATE TABLE spec.analysis_spec_rel
(
	analysis_spec_id int,
	analysis_id int
) WITHOUT OIDS;


-- 抽象デバイス----定义式样书(绿色列)
CREATE TABLE spec.requirement_def_device
(
	order_no serial,
	req_def_id int,
	device_type varchar(50),
	val varchar(512)
) WITHOUT OIDS;


-- 要件定義書
CREATE TABLE spec.requirement_def_record
(
	req_def_id serial NOT NULL,
	-- 担当
	author_name varchar(20),
	-- H/U要件定義ID
	hu_def_id varchar(20),
	-- 要件定義ID -- 机能式样书章节号
	requirement_id varchar(20),
	id varchar(20),
	spec_chapter_num varchar(20),
	-- ユニークID
	unique_id int,
	-- 大分類
	major_category varchar(20),
	-- 中分類
	medium_catetory varchar(20),
	-- 小分類
	small_category varchar(30),
	-- 詳細
	detail varchar(512),
	-- 基本要件
	base varchar(32),
	-- 関連基本要件
	rel_requiremant varchar(256),
	exception varchar(32),
	-- DCU-状態
	dcu_status varchar(256),
	-- DCU トリガー
	dcu_trigger varchar(512),
	-- DCU 動作
	dcu_action varchar(512),
	-- MEU 状態
	meu_status varchar(256),
	-- MEU-トリガー
	meu_trigger varchar(512),
	-- MEU-動作
	meu_action varchar(512),
	-- 備考(HU要件定義)
	hu_req_remark varchar(512),
	-- DCU/MEUどちらの想定か
	dcu_meu varchar(32),
	-- 状態
	pf_status varchar(512),
	-- トリガー
	pf_trigger varchar(512),
	-- 動作
	pf_action varchar(512),
	-- 備考
	remark varchar,
	-- 責務分担の特記事項
	notice varchar,
	-- 参考HAL設計書
	rel_hal_design varchar,
	-- 参考ウォークスルー図
	rel_flow_diagram varchar(50),
	-- その他仕様（リファハード仕様等）
	other_spec varchar(50),
	-- リファレンスハード上での実現可否
	implementation varchar(100),
	-- 詳細分析可否
	analysis varchar(20),
	-- 未要件分析
	unrequire varchar(2),
	PRIMARY KEY (req_def_id)
) WITHOUT OIDS;


-- 要件定義書
CREATE TABLE spec.requirement_spec
(
	requiremnt_spec_id serial NOT NULL,
	-- 项目
	proj varchar(50),
	-- 式样书名称
	spec_name varchar,
	-- 版本
	ver varchar(50),
	-- 文件名称
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

COMMENT ON COLUMN spec.analysis_model.model IS 'APL 模块';
COMMENT ON COLUMN spec.analysis_spec.spec_name IS '式样书名称';
COMMENT ON COLUMN spec.analysis_spec.ver IS '版本';
COMMENT ON COLUMN spec.analysis_spec.file_name IS '文件名称';
COMMENT ON COLUMN spec.analysis_spec_record.author_name IS '担当者';
COMMENT ON COLUMN spec.analysis_spec_record.requirement_id IS 'TAGL要件定義ID';
COMMENT ON COLUMN spec.analysis_spec_record.id IS '机能ID';
COMMENT ON COLUMN spec.analysis_spec_record.unique_id IS 'ユニークID';
COMMENT ON COLUMN spec.analysis_spec_record.medium_catetory IS '中分類';
COMMENT ON COLUMN spec.analysis_spec_record.detail IS '詳細';
COMMENT ON COLUMN spec.analysis_spec_record.base IS '基本要件';
COMMENT ON COLUMN spec.analysis_spec_record.rel_requiremant IS '関連基本要件';
COMMENT ON COLUMN spec.analysis_spec_record.exception IS '除外';
COMMENT ON COLUMN spec.analysis_spec_record.dcu_meu IS 'DCU/MEUどちらの想定か';
COMMENT ON COLUMN spec.analysis_spec_record.pf_status IS '状態';
COMMENT ON COLUMN spec.analysis_spec_record.fp_trigger IS 'トリガー';
COMMENT ON COLUMN spec.analysis_spec_record.pf_action IS '動作';
COMMENT ON COLUMN spec.analysis_spec_record.seq_diagram IS 'シーケンス図';
COMMENT ON COLUMN spec.analysis_spec_record.supple_spec IS '補足参照仕様書';
COMMENT ON COLUMN spec.analysis_spec_record.uncheck IS '未検証';
COMMENT ON COLUMN spec.analysis_spec_record.remark IS '備考';
COMMENT ON TABLE spec.requirement_def_device IS '抽象デバイス----定义式样书(绿色列)';
COMMENT ON TABLE spec.requirement_def_record IS '要件定義書';
COMMENT ON COLUMN spec.requirement_def_record.author_name IS '担当';
COMMENT ON COLUMN spec.requirement_def_record.hu_def_id IS 'H/U要件定義ID';
COMMENT ON COLUMN spec.requirement_def_record.requirement_id IS '要件定義ID -- 机能式样书章节号';
COMMENT ON COLUMN spec.requirement_def_record.unique_id IS 'ユニークID';
COMMENT ON COLUMN spec.requirement_def_record.major_category IS '大分類';
COMMENT ON COLUMN spec.requirement_def_record.medium_catetory IS '中分類';
COMMENT ON COLUMN spec.requirement_def_record.small_category IS '小分類';
COMMENT ON COLUMN spec.requirement_def_record.detail IS '詳細';
COMMENT ON COLUMN spec.requirement_def_record.base IS '基本要件';
COMMENT ON COLUMN spec.requirement_def_record.rel_requiremant IS '関連基本要件';
COMMENT ON COLUMN spec.requirement_def_record.dcu_status IS 'DCU-状態';
COMMENT ON COLUMN spec.requirement_def_record.dcu_trigger IS 'DCU トリガー';
COMMENT ON COLUMN spec.requirement_def_record.dcu_action IS 'DCU 動作';
COMMENT ON COLUMN spec.requirement_def_record.meu_status IS 'MEU 状態';
COMMENT ON COLUMN spec.requirement_def_record.meu_trigger IS 'MEU-トリガー';
COMMENT ON COLUMN spec.requirement_def_record.meu_action IS 'MEU-動作';
COMMENT ON COLUMN spec.requirement_def_record.hu_req_remark IS '備考(HU要件定義)';
COMMENT ON COLUMN spec.requirement_def_record.dcu_meu IS 'DCU/MEUどちらの想定か';
COMMENT ON COLUMN spec.requirement_def_record.pf_status IS '状態';
COMMENT ON COLUMN spec.requirement_def_record.pf_trigger IS 'トリガー';
COMMENT ON COLUMN spec.requirement_def_record.pf_action IS '動作';
COMMENT ON COLUMN spec.requirement_def_record.remark IS '備考';
COMMENT ON COLUMN spec.requirement_def_record.notice IS '責務分担の特記事項';
COMMENT ON COLUMN spec.requirement_def_record.rel_hal_design IS '参考HAL設計書';
COMMENT ON COLUMN spec.requirement_def_record.rel_flow_diagram IS '参考ウォークスルー図';
COMMENT ON COLUMN spec.requirement_def_record.other_spec IS 'その他仕様（リファハード仕様等）';
COMMENT ON COLUMN spec.requirement_def_record.implementation IS 'リファレンスハード上での実現可否';
COMMENT ON COLUMN spec.requirement_def_record.analysis IS '詳細分析可否';
COMMENT ON COLUMN spec.requirement_def_record.unrequire IS '未要件分析';
COMMENT ON TABLE spec.requirement_spec IS '要件定義書';
COMMENT ON COLUMN spec.requirement_spec.proj IS '项目';
COMMENT ON COLUMN spec.requirement_spec.spec_name IS '式样书名称';
COMMENT ON COLUMN spec.requirement_spec.ver IS '版本';
COMMENT ON COLUMN spec.requirement_spec.file_name IS '文件名称';



