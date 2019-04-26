from ..db import db
from sqlalchemy.orm import relationship
import datetime


#创建唯一的序列，保存文件时使用
class FileSeq(db.Model):
    __table_args__ = {"schema": "public"}
    __tablename__ = 'file_seq'

    file_seq_id = db.Column(db.Integer, primary_key=True)

class Projects(db.Model):
    __table_args__ = {"schema": "public"}
    __tablename__ = 'projects'

    proj_id = db.Column(db.Integer, primary_key=True)
    proj_name = db.Column(db.String(1024), index=True)
    describe = db.Column(db.String(1024))
    create_time = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    update_time = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    # resourcesinfo = relationship("InputResourceInfo", backref="projects")

    def __repr__(self):
        return '<Project proj_id:%r, proj_name:%r>' % (self.proj_id, self.proj_name)

    def to_dict(self):
        d = {}
        for column in self.__table__.columns:
            attr = getattr(self, column.name)
            if isinstance(attr, datetime.datetime) or isinstance(attr, datetime.time) or isinstance(attr, datetime.date):
                attr = attr.strftime("%Y-%m-%d %H:%M:%S")
            d[column.name] = attr
        return d


class Users(db.Model):
    __table_args__ = {"schema": "public"}
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True)
    user_emp_id = db.Column(db.String(100))  # 员工号
    user_name = db.Column(db.String(100), index=True)
    email = db.Column(db.String(100))

    # projects = relationship('Projects', backref='users')

    def __repr__(self):
        return '<user_name:%r>' % self.user_name

    def to_dict(self):
        d = {}
        for column in self.__table__.columns:
            d[column.name] = getattr(self, column.name)
        return d


class Screen(db.Model):
    __table_args__ = {"schema": "public"}
    __tablename__ = 'screen'

    screen_gid = db.Column(db.Integer, primary_key=True)
    proj_id = db.Column(db.Integer, db.ForeignKey('public.projects.proj_id'), index=True)
    screen_uuid = db.Column(db.String(100))       # ScreenUUID
    screen_id = db.Column(db.String(100))         # ScreenID
    screen_name = db.Column(db.String(50))        # ScreenName
    outline = db.Column(db.String(1024))
    screen_disp_rect = db.Column(db.String(1024))   # ScreenDispRect
    screen_disp_pic = db.Column(db.String(1024))    # ScreenDispPic
    image_dir = db.Column(db.String(256))
    create_time = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    update_time = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    locked = db.Column(db.Boolean, index=True)    # 是否为锁定状态
    update_user = db.Column(db.Integer, db.ForeignKey('public.users.user_id'), index=True) # 当前更新人

    projects = relationship('Projects', backref='users')

    def __repr__(self):
        return '<Screen g_id:%r id:%r name:%r>' % (self.screen_gid, self.screen_id, self.screen_name)

    def to_dict(self):
        d = {}
        for column in self.__table__.columns:
            d[column.name] = getattr(self, column.name)
        return d


class AvailableModel(db.Model):
    __table_args__ = {"schema": "public"}
    __tablename__ = 'available_model'

    model_id = db.Column(db.Integer, primary_key=True)
    screen_id = db.Column(db.Integer, db.ForeignKey('public.screen.screen_gid'), index=True)
    model_info = db.Column(db.String()) # 整个对像都存起来

    def to_dict(self):
        d = {}
        for column in self.__table__.columns:
            d[column.name] = getattr(self, column.name)
        return d

#条件
class Conditions(db.Model):
    __table_args__ = {"schema": "public"}
    __tablename__ = 'conditions'

    condition_id = db.Column(db.Integer, primary_key=True)
    proj_id = db.Column(db.Integer, db.ForeignKey('public.projects.proj_id'), index=True)
    condition = db.Column(db.String(1024))
    view_model = db.Column(db.String(1024))

    def to_dict(self):
        d = {}
        for column in self.__table__.columns:
            d[column.name] = getattr(self, column.name)
        return d

db.Index('conditions_proj_id_condition',
         Conditions.proj_id, Conditions.condition,
         unique=True
         )

#函数
class Displays(db.Model):
    __table_args__ = {"schema": "public"}
    __tablename__ = 'displays'

    display_id = db.Column(db.Integer, primary_key=True)
    proj_id = db.Column(db.Integer, db.ForeignKey('public.projects.proj_id'), index=True)
    display = db.Column(db.String(256))
    fun_of_model = db.Column(db.String())

    def to_dict(self):
        d = {}
        for column in self.__table__.columns:
            d[column.name] = getattr(self, column.name)
        return d

db.Index('displays_proj_id_display',
         Displays.proj_id, Displays.display,
         unique=True
         )


class Properties(db.Model):
    __table_args__ = {"schema": "public"}
    __tablename__ = 'properties'

    property_id = db.Column(db.Integer, primary_key=True)
    proj_id = db.Column(db.Integer, db.ForeignKey('public.projects.proj_id'), index=True)
    property_type = db.Column(db.String(256))
    property = db.Column(db.String(256))

    def to_dict(self):
        d = {}
        for column in self.__table__.columns:
            d[column.name] = getattr(self, column.name)
        return d

db.Index('properties_proj_id_property_type',
         Properties.proj_id, Properties.property_type,
         unique=True
         )


class OpeTypes(db.Model):
    __table_args__ = {"schema": "public"}
    __tablename__ = 'ope_types'

    ope_id = db.Column(db.Integer, primary_key=True)
    proj_id = db.Column(db.Integer, db.ForeignKey('public.projects.proj_id'), index=True)
    ope_type = db.Column(db.String(256))
    ope_event = db.Column(db.String(256))

    def to_dict(self):
        d = {}
        for column in self.__table__.columns:
            d[column.name] = getattr(self, column.name)
        return d

db.Index('ope_types_proj_id_ope_type',
         OpeTypes.proj_id, OpeTypes.ope_type,
         unique=True
         )

#事件
class Events(db.Model):
    __table_args__ = {"schema": "public"}
    __tablename__ = 'events'

    event_id = db.Column(db.Integer, primary_key=True)
    proj_id = db.Column(db.Integer, db.ForeignKey('public.projects.proj_id'), index=True)
    event = db.Column(db.String(256)) # 事件名称
    trigger = db.Column(db.String())

    def to_dict(self):
        d = {}
        for column in self.__table__.columns:
            d[column.name] = getattr(self, column.name)
        return d

db.Index('events_proj_id_event',
         Events.proj_id, Events.event,
         unique=True
         )

#8张chapter表
class Chapter1(db.Model):
    __table_args__ = {"schema": "public"}
    __tablename__ = 'chapter1'

    chapter1_id = db.Column(db.Integer, primary_key=True)
    screen_gid = db.Column(db.Integer, db.ForeignKey('public.screen.screen_gid'), index=True)
    display_chapter = db.Column(db.String(10))
    display_state_no = db.Column(db.String(10))
    parts_number = db.Column(db.String(256))
    display_sub_chapter = db.Column(db.String(10))
    parts_name = db.Column(db.String(256))
    display_content = db.Column(db.String(256))
    display_formula = db.Column(db.String(256))
    display_condition_branch = db.Column(db.String(256))
    display_action = db.Column(db.Integer, db.ForeignKey('public.displays.display_id'), index=True) # display ID化
    display_condition = db.Column(db.Integer, db.ForeignKey('public.conditions.condition_id'), index=True)  # condition ID化
    display_property = db.Column(db.Integer, db.ForeignKey('public.properties.property_id'), index=True)  # property ID化
    data_range = db.Column(db.String(256))
    display_remark = db.Column(db.String(256))
    display_uuid = db.Column(db.String(1024))              # UUID
    display_parts_type = db.Column(db.String(256))
    display_condition_model_branch = db.Column(db.String(256))
    string_id = db.Column(db.String(256))
    display_default_value = db.Column(db.String(256))
    display_states = db.Column(db.String(1024))
    visible = db.Column(db.String(256))
    has_disp_info = db.Column(db.String(10), index=True)
    parts_id = db.Column(db.String(256))
    display_rect = db.Column(db.String(1024))

    # resourcesinfo = relationship("InputResourceInfo", backref="projects")
    displays = relationship("Displays", backref="chapter1")
    conditions = relationship("Conditions", backref="chapter1")
    properties = relationship("Properties", backref="chapter1")

    def to_dict(self):
        d = {}
        for column in self.__table__.columns:
            d[column.name] = getattr(self, column.name)
        return d

class Chapter2(db.Model):
    __table_args__ = {"schema": "public"}
    __tablename__ = 'chapter2'

    chapter2_id = db.Column(db.Integer, primary_key=True)
    screen_gid = db.Column(db.Integer, db.ForeignKey('public.screen.screen_gid'), index=True)
    active_chapter = db.Column(db.String(10))
    active_sub_chapter = db.Column(db.String(10))
    active_state_no = db.Column(db.String(10))
    active_no = db.Column(db.String(10))
    active_btn_name = db.Column(db.String(256))
    active_formula = db.Column(db.String(256))
    active_condition_branch = db.Column(db.String(256))
    active_condition = db.Column(db.Integer, db.ForeignKey('public.conditions.condition_id'), index=True)  # condition ID化
    active_action = db.Column(db.Integer, db.ForeignKey('public.displays.display_id'), index=True) # display ID化
    active_property = db.Column(db.Integer, db.ForeignKey('public.properties.property_id'), index=True) # property ID化
    active_during_driving = db.Column(db.String(256))
    active_remark = db.Column(db.String(256))
    active_uuid = db.Column(db.String(1024))              # UUID
    active_parts_type = db.Column(db.String(256))
    active_condition_model_branch = db.Column(db.String(256))  # condition ID化
    active_default_value = db.Column(db.String(256))
    active_states = db.Column(db.String(1024))
    has_disp_info = db.Column(db.String(10), index=True)
    active = db.Column(db.String(256))

    displays = relationship("Displays", backref="chapter2")
    conditions = relationship("Conditions", backref="chapter2")
    properties = relationship("Properties", backref="chapter2")

    def to_dict(self):
        d = {}
        for column in self.__table__.columns:
            d[column.name] = getattr(self, column.name)
        return d

class Chapter3(db.Model):
    __table_args__ = {"schema": "public"}
    __tablename__ = 'chapter3'

    chapter3_id = db.Column(db.Integer, primary_key=True)
    screen_gid = db.Column(db.Integer, db.ForeignKey('public.screen.screen_gid'), index=True)
    action_chapter = db.Column(db.String(10))
    action_sub_chapter = db.Column(db.String(10))
    action_state_no = db.Column(db.String(10))
    action_no = db.Column(db.String(10))
    action_btn_name = db.Column(db.String(256))
    action_ope = db.Column(db.Integer, db.ForeignKey('public.ope_types.ope_id'), index=True) # Ope ID化
    action_formula = db.Column(db.String(256))
    action_condition_branch = db.Column(db.String(256))
    action_condition = db.Column(db.Integer, db.ForeignKey('public.conditions.condition_id'), index=True)  # condition ID化
    action_action = db.Column(db.Integer, db.ForeignKey('public.displays.display_id'), index=True) # display ID化
    action_trans = db.Column(db.String(256))
    action_sound = db.Column(db.String(256))
    action_remark = db.Column(db.String(256))
    action_uuid = db.Column(db.String(1024))              # UUID
    action_parts_type = db.Column(db.String(256))
    action_condition_model_branch = db.Column(db.String(256))
    action_observer = db.Column(db.String(256))
    action_reply = db.Column(db.String(256))
    action_trans_type = db.Column(db.String(256))
    action_trans_id = db.Column(db.String(256))
    active_states = db.Column(db.String(1024))
    has_action_info = db.Column(db.String(10), index=True)

    displays = relationship("Displays", backref="chapter3")
    conditions = relationship("Conditions", backref="chapter3")
    opetypes = relationship("OpeTypes", backref="chapter3")

    def to_dict(self):
        d = {}
        for column in self.__table__.columns:
            d[column.name] = getattr(self, column.name)
        return d

class Chapter4(db.Model):
    __table_args__ = {"schema": "public"}
    __tablename__ = 'chapter4'

    chapter4_id = db.Column(db.Integer, primary_key=True)
    screen_gid = db.Column(db.Integer, db.ForeignKey('public.screen.screen_gid'), index=True)
    hk_chapter = db.Column(db.String(10))
    hk_sub_chapter = db.Column(db.String(10))
    hk_state_no = db.Column(db.String(10))
    hk_no = db.Column(db.String(10))
    hk_name = db.Column(db.String(256))
    hk_dev_name = db.Column(db.String(256))
    hk_ope = db.Column(db.Integer, db.ForeignKey('public.ope_types.ope_id'), index=True) # Ope ID化
    hk_formula = db.Column(db.String(256))
    hk_condition_branch = db.Column(db.String(256))
    hk_condition = db.Column(db.Integer, db.ForeignKey('public.conditions.condition_id'), index=True)  # condition ID化
    hk_action = db.Column(db.Integer, db.ForeignKey('public.displays.display_id'), index=True) # display ID化
    hk_trans = db.Column(db.String(256))
    hk_sound = db.Column(db.String(256))
    hk_during_driving = db.Column(db.String(256))
    hk_remark = db.Column(db.String(256))
    hk_uuid = db.Column(db.String(1024))                  # UUID
    hk_condition_model_branch = db.Column(db.String(256))
    hk_observer = db.Column(db.String(256))
    hk_reply = db.Column(db.String(256))
    hk_trans_type = db.Column(db.String(256))
    hk_trans_id = db.Column(db.String(256))
    hk_dev_type = db.Column(db.String(256))

    displays = relationship("Displays", backref="chapter4")
    conditions = relationship("Conditions", backref="chapter4")
    opetypes = relationship("OpeTypes", backref="chapter4")

    def to_dict(self):
        d = {}
        for column in self.__table__.columns:
            d[column.name] = getattr(self, column.name)
        return d

class Chapter5(db.Model):
    __table_args__ = {"schema": "public"}
    __tablename__ = 'chapter5'

    chapter5_id = db.Column(db.Integer, primary_key=True)
    screen_gid = db.Column(db.Integer, db.ForeignKey('public.screen.screen_gid'), index=True)
    init_chapter = db.Column(db.String(10)) #InitChapter
    init_no = db.Column(db.String(10)) #InitNo
    init_state_no = db.Column(db.String(10)) #InitStateNo
    init_status  = db.Column(db.String(256)) #InitStatus
    init_formula = db.Column(db.String(256)) #InitFormula
    init_condition = db.Column(db.Integer, db.ForeignKey('public.conditions.condition_id'), index=True)
    init_condition_branch = db.Column(db.String(256))
    init_action = db.Column(db.Integer, db.ForeignKey('public.displays.display_id'), index=True)
    init_trans = db.Column(db.String(1024)) #InitTrans
    init_remark  = db.Column(db.String(1024)) #InitRemark
    init_uuid = db.Column(db.String(1024)) # InitUUID
    init_event = db.Column(db.String(256)) #InitEvent
    init_condition_model_branch = db.Column(db.String(256))
    init_observer = db.Column(db.String(1024)) #InitObserver
    init_reply = db.Column(db.String(1024)) #InitReply
    init_trans_type = db.Column(db.String(256)) #InitTransType
    init_trans_id = db.Column(db.String(256)) #InitTransID

    displays = relationship("Displays", backref="chapter5")
    conditions = relationship("Conditions", backref="chapter5")

    def to_dict(self):
        d = {}
        for column in self.__table__.columns:
            d[column.name] = getattr(self, column.name)
        return d

class Chapter6(db.Model):
    __table_args__ = {"schema": "public"}
    __tablename__ = 'chapter6'

    chapter6_id = db.Column(db.Integer, primary_key=True)
    screen_gid = db.Column(db.Integer, db.ForeignKey('public.screen.screen_gid'), index=True)
    status_change_chapter = db.Column(db.String(10)) #StatusChangeChapter
    status_change_sub_chapter = db.Column(db.String(10)) #StatusChangeSubChapter
    status_change_no = db.Column(db.String(10)) #StatusChangeNo
    status_change_state_no = db.Column(db.String(10))  # StatusChangeStateNo
    status_change_name  = db.Column(db.String(256)) #StatusChangeName
    status_change_f_formula = db.Column(db.String(256)) #StatusChangeFFormula
    status_change_f_condition = db.Column(db.Integer, db.ForeignKey('public.conditions.condition_id'), index=True)
    status_change_f_condition_branch = db.Column(db.String(256))
    status_change_f_action = db.Column(db.Integer, db.ForeignKey('public.displays.display_id'), index=True)
    status_change_b_formula = db.Column(db.String(1024)) #StatusChangeBFormula
    status_change_b_condition = db.Column(db.Integer, db.ForeignKey('public.conditions.condition_id'), index=True)
    status_change_b_condition_branch = db.Column(db.String(256))
    status_change_b_action = db.Column(db.Integer, db.ForeignKey('public.displays.display_id'), index=True)
    status_change_i_formula = db.Column(db.String(1024))  # StatusChangeIFormula
    status_change_i_condition = db.Column(db.Integer, db.ForeignKey('public.conditions.condition_id'), index=True)
    status_change_i_condition_branch = db.Column(db.String(256))
    status_change_i_action = db.Column(db.Integer, db.ForeignKey('public.displays.display_id'), index=True)
    status_change_uuid = db.Column(db.String(1024)) # StatusChangeUUID
    status_change_event = db.Column(db.String(256)) #StatusChangeEvent
    status_change_f_condition_model_branch = db.Column(db.String(256))
    status_change_f_observer = db.Column(db.String(1024))  # StatusChangeFActionModel
    status_change_f_reply = db.Column(db.String(1024))  # StatusChangeFReply
    status_change_b_condition_model_branch = db.Column(db.String(256))
    status_change_b_observer = db.Column(db.String(1024)) #StatusChangeBObserver
    status_change_b_reply = db.Column(db.String(1024)) #StatusChangeBReply
    status_change_i_condition_model_branch = db.Column(db.String(256))
    status_change_i_observer = db.Column(db.String(1024))  # StatusChangeBObserver
    status_change_i_reply = db.Column(db.String(1024))  # StatusChangeBReply
    status_change_b_trans = db.Column(db.String(256)) #StatusChangeBTrans
    status_change_f_trans = db.Column(db.String(256)) #StatusChangeFTrans
    status_change_i_trans = db.Column(db.String(256)) #StatusChangeITrans

    def to_dict(self):
        d = {}
        for column in self.__table__.columns:
            d[column.name] = getattr(self, column.name)
        return d

class Chapter7(db.Model):
    __table_args__ = {"schema": "public"}
    __tablename__ = 'chapter7'

    chapter7_id = db.Column(db.Integer, primary_key=True)
    screen_gid = db.Column(db.Integer, db.ForeignKey('public.screen.screen_gid'), index=True)
    transition_chapter = db.Column(db.String(10)) #TransitionChapter
    transition_sub_chapter = db.Column(db.String(10)) #TransitionSubChapter
    transition_no = db.Column(db.String(10)) #TransitionNo
    transition_state_no = db.Column(db.String(10))  # TransitionStateNo
    transition_name  = db.Column(db.String(256)) #TransitionName
    transition_f_formula = db.Column(db.String(256)) #TransitionFCondition
    transition_f_condition = db.Column(db.Integer, db.ForeignKey('public.conditions.condition_id'), index=True)
    transition_f_condition_branch = db.Column(db.String(256))
    transition_f_action = db.Column(db.Integer, db.ForeignKey('public.displays.display_id'), index=True)
    transition_b_formula = db.Column(db.String(1024)) #TransitionBFormula
    transition_b_condition = db.Column(db.Integer, db.ForeignKey('public.conditions.condition_id'), index=True)
    transition_b_condition_branch = db.Column(db.String(256))
    transition_b_action = db.Column(db.Integer, db.ForeignKey('public.displays.display_id'), index=True)
    transition_i_formula = db.Column(db.String(1024))  # TransitionIFormula
    transition_i_condition = db.Column(db.Integer, db.ForeignKey('public.conditions.condition_id'), index=True)
    transition_i_condition_branch = db.Column(db.String(256))
    transition_i_action = db.Column(db.Integer, db.ForeignKey('public.displays.display_id'), index=True)
    transition_uuid = db.Column(db.String(1024)) # TransitionUUID
    transition_event = db.Column(db.String(256)) #TransitionEvent
    transition_b_condition_model_branch = db.Column(db.String(256))
    transition_b_observer = db.Column(db.String(1024)) #TransitionBObserver
    transition_b_reply = db.Column(db.String(1024)) #TransitionBReply
    transition_f_condition_model_branch = db.Column(db.String(256))
    transition_f_observer = db.Column(db.String(1024))  # TransitionFObserver
    transition_f_reply = db.Column(db.String(1024))  # TransitionFReply
    transition_i_condition_model_branch = db.Column(db.String(256))
    transition_i_observer = db.Column(db.String(1024))  # TransitionIObserver
    transition_i_reply = db.Column(db.String(1024))  # TransitionIReply
    transition_b_trans = db.Column(db.String(256)) #TransitionBTrans
    transition_f_trans = db.Column(db.String(256)) #TransitionFTrans
    transition_i_trans = db.Column(db.String(256)) #TransitionITrans

    def to_dict(self):
        d = {}
        for column in self.__table__.columns:
            d[column.name] = getattr(self, column.name)
        return d

class Chapter8(db.Model):
    __table_args__ = {"schema": "public"}
    __tablename__ = 'chapter8'

    chapter8_id = db.Column(db.Integer, primary_key=True)
    screen_gid = db.Column(db.Integer, db.ForeignKey('public.screen.screen_gid'), index=True)
    trig_chapter = db.Column(db.String(10)) #TrigChapter
    trig_sub_chapter = db.Column(db.String(10)) #TrigSubChapter
    trig_state_no = db.Column(db.String(10)) #TrigStateNo
    trig_no = db.Column(db.String(10))  # TrigNo
    trig_formula = db.Column(db.String(256)) #TrigFormula
    trig_condition = db.Column(db.Integer, db.ForeignKey('public.conditions.condition_id'), index=True)
    trig_condition_branch = db.Column(db.String(256))
    trig_action = db.Column(db.Integer, db.ForeignKey('public.displays.display_id'), index=True)
    trig_trans = db.Column(db.String(256)) #TrigTrans
    trig_sound = db.Column(db.String(256)) #TrigSound
    trig_timer = db.Column(db.String(256)) #TrigTimer
    trig_remark = db.Column(db.String(1024)) #TrigRemark
    trig_uuid = db.Column(db.String(1024)) # TransitionUUID
    trig_trig = db.Column(db.Integer, db.ForeignKey('public.events.event_id'), index=True) #TrigTrig
    trig_event = db.Column(db.String(256))  # TrigEvent
    trig_condition_model_branch = db.Column(db.String(256))
    trig_observer = db.Column(db.String(1024))  # TrigObserver
    trig_reply = db.Column(db.String(1024))  # TrigReply
    trig_trans_type = db.Column(db.String(256)) #TrigTransType
    trig_trans_id = db.Column(db.String(256)) #TrigTransID
    trig_signal = db.Column(db.String(256)) #TrigSignal

    displays = relationship("Displays", backref="chapter8")
    conditions = relationship("Conditions", backref="chapter8")
    events = relationship("Events", backref="chapter8")

    def to_dict(self):
        d = {}
        for column in self.__table__.columns:
            d[column.name] = getattr(self, column.name)
        return d




