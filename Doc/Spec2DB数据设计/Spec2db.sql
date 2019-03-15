
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
	-- 記事名
	req_spec_name varchar(50),
	-- 仕様書名
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
	-- 章番号
	req_chapter_num varchar(50),
	-- 章タイトル
	req_chapter_title varchar(30),
	-- ページ/シート名/画面/表/番号等
	req_page varchar(50),
	-- 更新日
	update_date date,
	-- 分類
	category varchar(20),
	-- 仕様書番号
	spec_num varchar(20),
	-- 仕様書名(Document名)
	spec_file_name varchar(50),
	-- version
	version varchar(20),
	-- 章番号
	spec_chapter_num varchar(30),
	-- ページ/シート名/
	spec_chapter_title varchar(50),
	-- 要/不要
	need varchar(4),
	-- 不要な場合の理由
	reason varchar(100),
	-- 所属
	belong_to varchar(20),
	-- Gr名
	group_name varchar(20),
	-- 氏名
	name varchar(20),
	-- 記載日
	date date,
	-- 備考
	remark varchar(512),
	PRIMARY KEY (req_id)
) WITHOUT OIDS;


-- 机能章节
CREATE TABLE spec.spec_chapter
(
	-- 机能章节ID
	permanent_id int NOT NULL,
	chapter_id serial NOT NULL,
	-- 章节编号
	chapter_number varchar(100),
	title varchar(100),
	-- 'terminology' / 'chapter'
	chapter_type varchar(20) DEFAULT 'chapter',
	PRIMARY KEY (chapter_id)
) WITHOUT OIDS;


-- 章节与章节之间的关系表
CREATE TABLE spec.spec_chapter_chapter_rel
(
	order_no serial,
	parent_chapter_id int NOT NULL,
	-- 机能章节ID
	child_chapter_id int NOT NULL
) WITHOUT OIDS;


-- 章节与机能关系表
CREATE TABLE spec.spec_chapter_func_rel
(
	-- 序列号
	order_no serial,
	chapter_id int NOT NULL,
	-- 机能点ID
	func_id int NOT NULL
) WITHOUT OIDS;


CREATE TABLE spec.spec_chapter_model_rel
(
	order_no serial,
	chapter_id int NOT NULL,
	model_id int NOT NULL,
	val varchar(20)
) WITHOUT OIDS;


-- 机能点
CREATE TABLE spec.spec_functions
(
	permanent_id int NOT NULL,
	-- 机能点ID
	func_id serial NOT NULL,
	-- 存的时式样书中，机能前面[id xx]中xx的值。
	id varchar(20),
	-- 种别: 
	-- summaryInfo': 机能概要;
	-- 'preCondition': 前提;
	-- 'callInfo': 呼出条件;
	-- "APPRANGE": 適合範囲;
	-- "EXCEPT": 例外;
	-- "SUPPLY": 補足;
	-- "TABLE": 表;
	-- "FUNCTION": 機能;
	-- "DESTINATION": 仕向;
	-- 
	func_type varchar(20),
	-- 机能内容(不包括删除线): 内容的形式用xml形式
	func_content varchar,
	image_id int,
	-- 更新日期。
	update_date date DEFAULT now(),
	-- 测试类别
	-- 方格：测试组自行测试。
	-- 方格+/: 需要机能组辅助才能测试。
	test_type varchar(10),
	-- 状态
	status varchar(1),
	-- 所属章节编号(临时的字段)
	parent_chapter_num varchar(20),
	PRIMARY KEY (func_id)
) WITHOUT OIDS;


-- 机能与机能关系表。
CREATE TABLE spec.spec_func_func_rel
(
	order_no serial,
	-- 父机能ID.
	parent_func_id int NOT NULL,
	-- 机能点ID
	child_func_id int NOT NULL
) WITHOUT OIDS;


-- 机能与车型的关系
CREATE TABLE spec.spec_func_model_rel
(
	order_no serial,
	-- 机能点ID
	func_id int NOT NULL,
	model_id int NOT NULL,
	-- '-' / 'O'
	val varchar(20)
) WITHOUT OIDS;


-- 式样书更新履歴
CREATE TABLE spec.spec_history
(
	-- 序号
	serial_no serial NOT NULL,
	-- 版番
	version varchar(100),
	-- 仕向け
	region varchar(10),
	-- 指示者
	instruction_person varchar(20),
	-- (指示内容)文書名
	instruction_doc_name varchar(100),
	-- (指示内容)Ver
	instruction_doc_ver varchar(255),
	-- (指示内容)管理番号
	instruction_doc_num varchar(255),
	-- 指示日
	instruction_date date,
	-- 更新理由
	modify_reason varchar(255),
	-- 更新理由詳細
	detail_reason varchar(1024),
	-- 項番
	chapter varchar(100),
	-- 更新前内容
	old_content varchar,
	-- 更新後内容
	new_content varchar,
	-- 更新日
	modify_date date,
	-- 担当
	responsible_person varchar(20),
	-- 備考
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


-- 车型
CREATE TABLE spec.spec_model
(
	model_id serial NOT NULL,
	-- 17cy-全モデル共通-DCU-&ZKxxx/XX;
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
	-- 项目ID.
	proj_id serial NOT NULL,
	-- 项目名称。
	proj_name varchar(20),
	PRIMARY KEY (proj_id)
) WITHOUT OIDS;


-- 参照先仕様書情報
CREATE TABLE spec.spec_reference
(
	-- 机能点ID
	func_id int NOT NULL,
	-- 仕様書番号
	spec_no varchar(30),
	-- Version
	version varchar(20),
	PRIMARY KEY (func_id)
) WITHOUT OIDS;


-- 机能式样书
CREATE TABLE spec.spec_specification
(
	-- 机能章节ID (同时可以作为版本使用)
	permanent_id int NOT NULL,
	spec_id serial NOT NULL,
	-- 17CY / 14Tmap
	proj_id int,
	-- 式样书编号
	spec_num varchar(20),
	-- 机能式样名称.
	spec_name varchar(100),
	-- 式样书文件名称
	spec_file_name varchar(100),
	-- 书写式样书的语言
	language varchar(3),
	version varchar(100),
	-- 数据是否完整。
	-- True: 不完整；
	-- False: 完整；
	dirty boolean DEFAULT 'True',
	PRIMARY KEY (spec_id)
) WITHOUT OIDS;


-- 式样书与章节关系表
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
COMMENT ON COLUMN spec.req_spec_info.req_spec_name IS '記事名';
COMMENT ON COLUMN spec.req_spec_info.req_spec_file_name IS '仕様書名';
COMMENT ON COLUMN spec.seq_spec.no IS 'No.';
COMMENT ON COLUMN spec.seq_spec.req_chapter_num IS '章番号';
COMMENT ON COLUMN spec.seq_spec.req_chapter_title IS '章タイトル';
COMMENT ON COLUMN spec.seq_spec.req_page IS 'ページ/シート名/画面/表/番号等';
COMMENT ON COLUMN spec.seq_spec.update_date IS '更新日';
COMMENT ON COLUMN spec.seq_spec.category IS '分類';
COMMENT ON COLUMN spec.seq_spec.spec_num IS '仕様書番号';
COMMENT ON COLUMN spec.seq_spec.spec_file_name IS '仕様書名(Document名)';
COMMENT ON COLUMN spec.seq_spec.version IS 'version';
COMMENT ON COLUMN spec.seq_spec.spec_chapter_num IS '章番号';
COMMENT ON COLUMN spec.seq_spec.spec_chapter_title IS 'ページ/シート名/';
COMMENT ON COLUMN spec.seq_spec.need IS '要/不要';
COMMENT ON COLUMN spec.seq_spec.reason IS '不要な場合の理由';
COMMENT ON COLUMN spec.seq_spec.belong_to IS '所属';
COMMENT ON COLUMN spec.seq_spec.group_name IS 'Gr名';
COMMENT ON COLUMN spec.seq_spec.name IS '氏名';
COMMENT ON COLUMN spec.seq_spec.date IS '記載日';
COMMENT ON COLUMN spec.seq_spec.remark IS '備考';
COMMENT ON TABLE spec.spec_chapter IS '机能章节';
COMMENT ON COLUMN spec.spec_chapter.permanent_id IS '机能章节ID';
COMMENT ON COLUMN spec.spec_chapter.chapter_number IS '章节编号';
COMMENT ON COLUMN spec.spec_chapter.chapter_type IS '''terminology'' / ''chapter''';
COMMENT ON TABLE spec.spec_chapter_chapter_rel IS '章节与章节之间的关系表';
COMMENT ON COLUMN spec.spec_chapter_chapter_rel.child_chapter_id IS '机能章节ID';
COMMENT ON TABLE spec.spec_chapter_func_rel IS '章节与机能关系表';
COMMENT ON COLUMN spec.spec_chapter_func_rel.order_no IS '序列号';
COMMENT ON COLUMN spec.spec_chapter_func_rel.func_id IS '机能点ID';
COMMENT ON TABLE spec.spec_functions IS '机能点';
COMMENT ON COLUMN spec.spec_functions.func_id IS '机能点ID';
COMMENT ON COLUMN spec.spec_functions.id IS '存的时式样书中，机能前面[id xx]中xx的值。';
COMMENT ON COLUMN spec.spec_functions.func_type IS '种别: 
summaryInfo'': 机能概要;
''preCondition'': 前提;
''callInfo'': 呼出条件;
"APPRANGE": 適合範囲;
"EXCEPT": 例外;
"SUPPLY": 補足;
"TABLE": 表;
"FUNCTION": 機能;
"DESTINATION": 仕向;
';
COMMENT ON COLUMN spec.spec_functions.func_content IS '机能内容(不包括删除线): 内容的形式用xml形式';
COMMENT ON COLUMN spec.spec_functions.update_date IS '更新日期。';
COMMENT ON COLUMN spec.spec_functions.test_type IS '测试类别
方格：测试组自行测试。
方格+/: 需要机能组辅助才能测试。';
COMMENT ON COLUMN spec.spec_functions.status IS '状态';
COMMENT ON COLUMN spec.spec_functions.parent_chapter_num IS '所属章节编号(临时的字段)';
COMMENT ON TABLE spec.spec_func_func_rel IS '机能与机能关系表。';
COMMENT ON COLUMN spec.spec_func_func_rel.parent_func_id IS '父机能ID.';
COMMENT ON COLUMN spec.spec_func_func_rel.child_func_id IS '机能点ID';
COMMENT ON TABLE spec.spec_func_model_rel IS '机能与车型的关系';
COMMENT ON COLUMN spec.spec_func_model_rel.func_id IS '机能点ID';
COMMENT ON COLUMN spec.spec_func_model_rel.val IS '''-'' / ''O''';
COMMENT ON TABLE spec.spec_history IS '式样书更新履歴';
COMMENT ON COLUMN spec.spec_history.serial_no IS '序号';
COMMENT ON COLUMN spec.spec_history.version IS '版番';
COMMENT ON COLUMN spec.spec_history.region IS '仕向け';
COMMENT ON COLUMN spec.spec_history.instruction_person IS '指示者';
COMMENT ON COLUMN spec.spec_history.instruction_doc_name IS '(指示内容)文書名';
COMMENT ON COLUMN spec.spec_history.instruction_doc_ver IS '(指示内容)Ver';
COMMENT ON COLUMN spec.spec_history.instruction_doc_num IS '(指示内容)管理番号';
COMMENT ON COLUMN spec.spec_history.instruction_date IS '指示日';
COMMENT ON COLUMN spec.spec_history.modify_reason IS '更新理由';
COMMENT ON COLUMN spec.spec_history.detail_reason IS '更新理由詳細';
COMMENT ON COLUMN spec.spec_history.chapter IS '項番';
COMMENT ON COLUMN spec.spec_history.old_content IS '更新前内容';
COMMENT ON COLUMN spec.spec_history.new_content IS '更新後内容';
COMMENT ON COLUMN spec.spec_history.modify_date IS '更新日';
COMMENT ON COLUMN spec.spec_history.responsible_person IS '担当';
COMMENT ON COLUMN spec.spec_history.note IS '備考';
COMMENT ON COLUMN spec.spec_image.hash_key IS 'MD5';
COMMENT ON TABLE spec.spec_model IS '车型';
COMMENT ON COLUMN spec.spec_model.model IS '17cy-全モデル共通-DCU-&ZKxxx/XX;
';
COMMENT ON COLUMN spec.spec_permanent_id.type IS '''spec'' / ''function'' / ''chapter''';
COMMENT ON COLUMN spec.spec_proj.proj_id IS '项目ID.';
COMMENT ON COLUMN spec.spec_proj.proj_name IS '项目名称。';
COMMENT ON TABLE spec.spec_reference IS '参照先仕様書情報';
COMMENT ON COLUMN spec.spec_reference.func_id IS '机能点ID';
COMMENT ON COLUMN spec.spec_reference.spec_no IS '仕様書番号';
COMMENT ON COLUMN spec.spec_reference.version IS 'Version';
COMMENT ON TABLE spec.spec_specification IS '机能式样书';
COMMENT ON COLUMN spec.spec_specification.permanent_id IS '机能章节ID (同时可以作为版本使用)';
COMMENT ON COLUMN spec.spec_specification.proj_id IS '17CY / 14Tmap';
COMMENT ON COLUMN spec.spec_specification.spec_num IS '式样书编号';
COMMENT ON COLUMN spec.spec_specification.spec_name IS '机能式样名称.';
COMMENT ON COLUMN spec.spec_specification.spec_file_name IS '式样书文件名称';
COMMENT ON COLUMN spec.spec_specification.language IS '书写式样书的语言';
COMMENT ON COLUMN spec.spec_specification.dirty IS '数据是否完整。
True: 不完整；
False: 完整；';
COMMENT ON TABLE spec.spec_spec_chapter_rel IS '式样书与章节关系表';



