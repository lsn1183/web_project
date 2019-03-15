# -*- coding: UTF-8 -*-
"""
Created on 2017-9-14

@author: hcz
"""
from Source.spec2db_server.arl.arl_base import ServiceBase
ARL_POWER_LIST = ["read_all",  # 查看所有记录。 1:是，0:否
                  "modify_all",  # 修改所有记录。 1：是，0：否。
                  "read_group",  # 看查组内所有记录。1：是，0：否。
                  "modify_group",  # 修改组员所有记录。1：是，0：否。
                  "read_self",  # 查看自己的记录。 1：是，0：否。
                  "modify_self",  # 修改自己的记录。1：是，0：否。
                  "mng_group",  # 管理组：添加、删除组。1：是，0：否。
                  "mng_member",  # 管理组员：添加，删除组员。1：是，0：否。
                  ]
ARL_PRE_POWER = {
    "Admin": {"read_all": 1, "modify_all": 1,
              "read_group": 1, "modify_group": 1,
              "read_self": 1, "modify_self": 1,
              "mng_group": 1, "mng_member": 1},
    "Leader": {"read_all": 0, "modify_all": 0,
               "read_group": 1, "modify_group": 1,
               "read_self": 1, "modify_self": 1,
               "mng_group": 0, "mng_member": 1},
    "Member": {"read_all": 1, "modify_all": 0,
               "read_group": 0, "modify_group": 0,
               "read_self": 1, "modify_self": 1,
               "mng_group": 0, "mng_member": 0
              },
    "Other": {"read_all": 1, "modify_all": 0,
              "read_group": 0, "modify_group": 0,
              "read_self": 1, "modify_self": 1,
              "mng_group": 0, "mng_member": 0
              },
}


class ArlGroup(ServiceBase):
    """
    """
    def __init__(self):
        ServiceBase.__init__(self)

    def add(self, group_name):
        sqlcmd = """
        INSERT INTO spec.arl_group(group_name)
            VALUES (%s);
        """
        data = {'result': 'NG'}
        if not group_name:
            return data
        group_data = self.get_group_by_name(group_name)
        if group_data and group_data.get("content"):
            data['result'] = 'NG'
            return data
        try:
            self._pg.connect()
            self._pg.execute(sqlcmd, (group_name,))
            self._pg.commit()
            data = {'result': 'OK'}
        except:
            pass
        finally:
            self._pg.close()
            return data

    def delete(self, group_id):
        if not group_id:
            return {'result': 'NG'}
        sqlcmd = """
        -- delete member
        DELETE FROM spec.arl_group_member WHERE group_id = %s;
        -- delete group
        DELETE FROM spec.arl_group WHERE group_id = %s;     
        """
        data = {'result': 'NG'}
        try:
            self._pg.connect()
            self._pg.execute(sqlcmd, (group_id, group_id))
            self._pg.commit()
            data['result'] = "OK"
        except:
            data['result'] = "OK"
        finally:
            if self._pg.connected:
                self._pg.close()
            return data

    def modify(self, group_id, new_group_name):
        data = {'result': 'NG'}
        if not group_id:
            return
        sqlcmd = """
        UPDATE spec.arl_group
           SET group_name = %s
         WHERE group_id= %s;
        """
        self._pg.connect()
        self._pg.execute(sqlcmd, (new_group_name, group_id))
        self._pg.commit()
        self._pg.close()
        data = {'result': 'OK'}
        return data

    def update_leader(self, group_id, user_id, role=0):
        data = {'result': 'NG'}
        sqlcmd = """
        INSERT INTO spec.arl_group_member(
                    group_id, user_id, role)
            VALUES (%s, %s, %s);
        """
        self._pg.connect()
        self._pg.execute(sqlcmd, (group_id, user_id, role))
        self._pg.commit()
        self._pg.close()
        return {'result': 'OK'}

    def add_member(self, req_data):
        data = {'result': 'NG'}
        try:
            self._pg.connect()
            # for member_data in req_data:
            #     group_id, user_id = member_data["group_id"], member_data['user_id']
            #     if self._exist_member(self._pg, group_id, user_id):
            #         data['result'] = "REPEAT"
            #         return data
            for member_data in req_data:
                group_id, user_id = member_data["group_id"], member_data['user_id']
                if group_id == 1:  # Admin
                    if self._exist_member(self._pg, group_id, user_id, 3):
                        data['result'] = "REPEAT"
                        return data
                    self._add_one_member(self._pg, group_id, user_id, 0, 3)
                elif group_id == 2:  # PL
                    if self._exist_member(self._pg, group_id, user_id, 7):
                        data['result'] = "REPEAT"
                        return data
                    self._add_one_member(self._pg, group_id, user_id, 0, 7)
                else:
                    if self._exist_member(self._pg, group_id, user_id, 5):
                        data['result'] = "REPEAT"
                        return data
                    self._add_one_member(self._pg, group_id, user_id, 0, 5)
            # for leader_data in req_data["leaders"]:
            #     if self._exist_member(self._pg, group_id, user_id):
            #         continue
            #     group_id, user_id = req_data["group_id"], leader_data['user_id']
            #     if group_id == 1:  # Admin
            #         self._add_one_member(self._pg, group_id, user_id, 1, 3)
            #     else:
            #         self._add_one_member(self._pg, group_id, user_id, 1, 4)
            self._pg.commit()
            self._pg.close()
            data['result'] = "OK"
        except:
            self._pg.conn.rollback()
            data['result'] = "NG"
        finally:
            return data

    def add_one_member(self, group_id, user_id, role, role_id, pg=None):
        if pg:
            if not self._exist_member(pg, group_id, user_id):
                self._add_one_member(pg, group_id, user_id, role, role_id)
        else:
            try:
                pg = self._pg
                pg.connect()
                if not self._exist_member(pg, group_id, user_id):
                    self._add_one_member(pg, group_id, user_id, role, role_id)
                    pg.commit()
            except:
                self._pg.conn.rollback()

    def _exist_member(self, pg, group_id, user_id, role_id):
        sqlcmd = """
        SELECT group_id, user_id
          FROM spec.arl_group_member
          WHERE group_id = %s AND user_id = %s AND role_id = %s
        """
        pg.execute(sqlcmd, (group_id, user_id, role_id))
        row = pg.fetchone()
        if row:
            return True
        return False

    def _add_one_member(self, pg, group_id, user_id, role, role_id):
        sqlcmd = """
        INSERT INTO spec.arl_group_member(
                    group_id, user_id, role, role_id)
            VALUES (%s, %s, %s, %s);
        """
        pg.execute(sqlcmd, (group_id, user_id, role, role_id))

    def _del_member(self, pg, group_id, user_id):
        sqlcmd = """
        DELETE FROM spec.arl_group_member
        WHERE group_id = %s and user_id = %s;
        """
        pg.execute(sqlcmd, (group_id, user_id))

    def _del_member_role(self, pg, group_id, user_id, role_id):
        sqlcmd = """
        DELETE FROM spec.arl_group_member
        WHERE group_id = %s and user_id = %s and role_id=%s;
        """
        pg.execute(sqlcmd, (group_id, user_id, role_id))

    def del_member(self, group_id, user_id):
        if not group_id and not user_id:
            return {'result': 'NG'}
        data = {'result': 'NG'}
        try:
            self._pg.connect()
            self._del_member(self._pg, group_id, user_id)
            self._pg.commit()
            data['result'] = "OK"
        except:
            self._pg.conn.rollback()
            data['result'] = "NG"
        finally:
            self._pg.close()
        return data

    def get_group_by_name(self, group_name):
        sqlcmd = """
        SELECT group_id, group_name
          FROM spec.arl_group
          where group_name = %s
        """
        data = {"result": "OK"}
        if not group_name:
            return
        self._pg.connect()
        self._pg.execute(sqlcmd, (group_name,))
        row = self._pg.fetchone()
        if row:
            content = {}
            content["group_id"] = row[0]
            content["group_name"] = row[1]
            data["content"] = content
        self._pg.commit()
        self._pg.close()
        return data

    def get_group_members(self, group_id):
        sqlcmd = """
            SELECT a.user_id, user_name, array_agg(c.role) as roles
            FROM spec.arl_group_member as a left join spec.arl_user as b on a.user_id = b.user_id
            left join spec.arl_role_power as c on a.role_id = c.role_id 
            GROUP BY a.user_id, group_id, user_name
            HAVING group_id = %s ORDER BY user_name
        """
        data = {"result": "NG"}
        self._pg.connect()
        try:
            self._pg.execute(sqlcmd, (group_id,))
            rows = self._pg.fetchall()
            member_list = []
            for row in rows:
                member_dict = dict()
                member_dict["user_id"] = row[0]
                member_dict["user_name"] = row[1]
                member_dict["role"] = row[2]
                member_list.append(member_dict)
                data["result"] = "OK"
                data["rontent"] = member_list
        except Exception as e:
            print e
            return data
        finally:
            self._pg.close()
        return data

    def get_one_member(self, pg, user_id):
        sqlcmd = """
            SELECT group_id, array_agg(role_id) FROM spec.arl_group_member 
            group by group_id, user_id HAVING user_id = %s
        """
        pg.execute(sqlcmd, (user_id,))
        rows = pg.fetchall()
        role_list = []
        role_dict = dict()
        for row in rows:
            role_dict["group_id"] = row[0]
            role_dict["roles"] = row[1]
            role_list.append(role_dict)
        return role_list

    def get_members(self, group_id):
        sqlcmd = """
        SELECT t1.user_id, t2.user_name, 
            t3.role, t3.read_all,
            t3.modify_all, t3.read_group, t3.modify_group, 
            t3.read_self, t3.modify_self, t3.mng_group, 
            t3.mng_member
          FROM spec.arl_group_member as t1
          LEFT JOIN spec.arl_user as t2
          ON t1.user_id = t2.user_id
          LEFT JOIN spec.arl_role_power as t3
          ON t1.role_id=t3.role_id
          WHERE t1.group_id = %s
          ORDER by user_name
        """
        data = {"result": "NG"}
        self._pg.connect()
        self._pg.execute(sqlcmd, (group_id,))
        rows = self._pg.fetchall()
        user_list = []
        ret_dict_keys = ["user_id","user_name","role","read_all", "modify_all",
                         "read_group","modify_group","read_self","modify_self",
                         "mng_group","mng_member"]
        for row in rows:
            user = {}
            # print 'aaa',row
            for i in range(0, len(ret_dict_keys)):
                user[ret_dict_keys[i]] = row[i]
            user_list.append(user)
        data["content"] = user_list
        data["result"] = "OK"
        self._pg.close()
        return data

    def get_all_groups(self):
        sqlcmd = """
        SELECT a.group_id, group_name, count(user_id) 
        FROM spec.arl_group as a LEFT JOIN 
        (select distinct user_id, group_id from spec.arl_group_member) as b 
        ON a.group_id = b.group_id GROUP BY a.group_id ORDER BY group_name
 
        """
        data = {"result": "NG"}
        self._pg.connect()
        self._pg.execute(sqlcmd)
        rows = self._pg.fetchall()
        group_list = []
        for row in rows:
            group_info = {}
            group_info["group_id"] = row[0]
            group_info["group_name"] = row[1]
            group_info["count"] = row[2]
            group_list.append(group_info)
        self._pg.close()
        if group_list:
            data["content"] = group_list
            data["total_count"] = len(rows)
            data["result"] = "OK"
        return data

    def update_group_name(self, group_id, new_group_name):
        record = {'result': 'NG'}
        sqlcmd1 = '''
        select group_name from spec.arl_group;       
        '''
        sqlcmd2 = """
        update spec.arl_group set group_name = %s
        where group_id = %s;
        """
        self._pg.connect()
        self._pg.execute(sqlcmd1)
        rows = self._pg.fetchall()
        for row in rows:
            if row[0] == new_group_name:
                return record
        self._pg.execute(sqlcmd2, (new_group_name, group_id))
        self._pg.commit()
        record['result'] = 'OK'
        self._pg.close()
        return record

    def update_group_role(self, req_json):
        result = {"result": "NG"}
        self._pg.connect()
        user_id = req_json.get("user_id")
        group_id = req_json.get("group_id")
        role_list = req_json.get("role")
        old_role = self.get_role_id(self._pg, group_id, user_id)
        old_roles_list = []
        for role in old_role:
            for r in role:
                old_roles_list.append(r)
        new_roles = set(role_list)
        old_roles = set(old_roles_list)
        add_role = list(new_roles.difference(old_roles))
        try:
            for role in add_role:
                self._add_one_member(self._pg, group_id, user_id, 0, role)
            del_role = list(old_roles.difference(new_roles))
            for role in del_role:
                self._del_member_role(self._pg, group_id, user_id, role)
            self._pg.commit()
            self._pg.close()
            result["result"] = "OK"
        except Exception as e:
            print e
            result["result"] = "NG"
        finally:
            self._pg.close()
        return result

    def get_role_id(self, pg, group_id, user_id):
        sqlcmd = """
            SELECT role_id FROM spec.arl_group_member 
            WHERE group_id = %s and  user_id = %s
        """
        pg.execute(sqlcmd, (group_id, user_id))
        rows = pg.fetchall()
        return rows

    # 获取所有组以及组下的所有人
    def get_groups_detail(self):
        group_detail_list = []
        group_list = self._get_groups_detail()
        for group in group_list:
            group_detail_dict = dict()
            user_list = []
            id_list = group.get("user_list")
            for _id in id_list:
                user_obj = ArlUser()
                user_info = user_obj.get_user_by_id(_id)
                user_info.pop("permission_list")
                user_list.append(user_info)
            group_detail_dict["group_id"] = group.get("group_id")
            group_detail_dict["group_name"] = group.get("group_name")
            group_detail_dict["user_list"] = user_list
            group_detail_list.append(group_detail_dict)
        return group_detail_list

    def _get_groups_detail(self):
        sqlcmd = """
            SELECT a.group_id, group_name , array_agg(user_id) FROM 
            spec.arl_group_member AS a LEFT JOIN spec.arl_group AS b ON 
            a.group_id = b.group_id GROUP BY a.group_id, group_name 
            HAVING a.group_id > 1 ORDER BY a.group_id
        """
        self._pg.connect()
        self._pg.execute(sqlcmd)
        rows = self._pg.fetchall()
        group_list = []
        for row in rows:
            group_dict = dict()
            group_dict["group_id"] = row[0]
            group_dict["group_name"] = row[1]
            group_dict["user_list"] = row[2]
            group_list.append(group_dict)
        return group_list

    def get_group_id(self,  user_id):
        sqlcmd = """
        SELECT group_id FROM spec.arl_group_member WHERE user_id = %s LIMIT 1
        """%(user_id)
        return sqlcmd


class ArlRole(ServiceBase):
    """
    """
    def __init__(self):
        ServiceBase.__init__(self)

    def get_all_roles(self):
        sqlcmd = """
        SELECT role_id, role
          FROM spec.arl_role_power
          ORDER BY role_id
        """
        data = {"result": "NG"}
        self._pg.connect()
        self._pg.execute(sqlcmd)
        rows = self._pg.fetchall()
        role_list = []
        for row in rows:
            role_info = dict()
            role_info["role_id"] = row[0]
            role_info["role"] = row[1]
            role_list.append(role_info)
        self._pg.close()
        if role_list:
            data["content"] = role_list
            data["total_count"] = len(rows)
            data["result"] = "OK"
        return data





class ArlUser(ServiceBase):
    """
    """
    def __init__(self):
        ServiceBase.__init__(self)

    def register(self, user_name, password, email):
        if self.get_user_by_name(user_name):
            return {}
        self._pg.connect()
        user_id = self._add(self._pg, user_name, password, email)
        if user_id:
            self._pg.commit()
            self._pg.close()
            user_info = self.get_user_by_id(user_id)
            return user_info

    def modify_user_info(self, data):
        """
        :param data: {"user_id": "id", "user_name": "",  "old_password": "", "new_password": ""}
        :return: True or False
        """
        if not data:
            return False
        try:
            self._pg.connect()
            user_id = data.get("user_id")
            old_password = data.get("old_password")
            if not self._check_user(user_id, old_password):
                return False
            user_name = data.get("user_name")
            new_password = data.get("new_password")
            if not user_name or not new_password:
                return False
            sqlcmd = """
            update spec.arl_user set user_name = %s, "password" = %s
              where user_id = %s
            """
            self._pg.execute(sqlcmd, (user_name, new_password, user_id))
            self._pg.commit()
            self._pg.close()
            return True
        except:
            self._pg.conn.rollback()
            self._pg.close()
            return False

    def _check_user(self, user_id, password):
        sqlcmd = """
        SELECT user_id, "password"
          FROM spec.arl_user
          where user_id = %s and "password"=%s
        """
        self._pg.execute(sqlcmd, (user_id, password))
        row = self._pg.fetchone()
        if row:
            return True
        return False

    def login(self, user_name, password):
        sqlcmd = """
        SELECT user_id
          FROM spec.arl_user
          where user_name = %s and password = %s
          limit 1
        """
        self._pg.connect()
        self._pg.execute(sqlcmd, (user_name, password))
        row = self._pg.fetchone()
        if row:
            user_id = row[0]
            user_info = self.get_user_by_id(user_id)
            return user_info
        self._pg.close()
        return None

    def update_userinfo_from_LDAP(self, username, password, email):
        sqlcmd = """
        UPDATE spec.arl_user
           SET password = %s, email = %s
         WHERE user_name= %s;
        """
        self._pg.connect()
        self._pg.execute(sqlcmd, (password, email, username))
        self._pg.commit()
        self._pg.close()
        return None

    def add(self, user_name, password=None):
        """
        :param user_name: storm user name
        :param password:
        :return: {user_name: '', user_id: ''}
        """
        data = {'result': "NG"}
        if not user_name:
            return data
        try:
            user_id = self._add(user_name, password)
            if user_id:
                user_info = self.get_user_by_id(user_id)
                data["content"] = user_info
                data["result"] = "OK"
            self._pg.commit()
        except:
            self._pg.conn.rollback()
        return data

    def _add(self, pg, user_name, password=None, email=None):
        if not user_name:
            return None
        sqlcmd = """
        INSERT INTO spec.arl_user(user_name, password, email)
        VALUES (%s, %s, %s) returning user_id;
        """
        user_id = None
        try:

            pg.execute(sqlcmd, (user_name, password, email))
            user_id = self.fetch_id()
        finally:
            # self._pg.close()
            pass
        return user_id

    def get_user(self, user):
        """
        :param user_id: user_id
        :return: {user_name: '', user_id: '', permission_list: [{group_id: '', group_name: '', read_all:1...},]}
        """
        data = {"result": "NG"}
        if type(user) in (int, ):
            user_info = self.get_user_by_id(user)
        else:
            user_info = self.get_user_by_name(user)
        if user_info:
            data["content"] = user_info
            data["result"] = "OK"
        return data

    def get_user_by_id(self, user_id):
        user_info = {}
        if not user_id:
            return user_info
        sqlcmd = """
        SELECT user_id, user_name
          FROM spec.arl_user
          WHERE user_id = %s
          limit 1
        """
        self._pg.connect()
        self._pg.execute(sqlcmd, (user_id, ))
        row = self._pg.fetchone()
        if row:
            attr_list = ["user_id", "user_name"]
            for i in range(0, len(row)):
                user_info[attr_list[i]] = row[i]
            user_info["permission_list"] = self.get_permission_list(user_info["user_id"])
        self._pg.close()
        return user_info

    def get_user_by_name(self, user_name):
        """
        :param user_id: user_id
        :return: {user_name: '', user_id: '', group_id: '', group_name: ''}
        """
        user_info = {}
        if not user_name:
            return user_info
        sqlcmd = """
        SELECT user_id, user_name
          FROM spec.arl_user
          WHERE user_name = %s
          limit 1
        """
        self._pg.connect()
        self._pg.execute(sqlcmd, (user_name, ))
        row = self._pg.fetchone()
        if row:
            attr_list = ["user_id", "user_name"]
            for i in range(0, len(row)):
                user_info[attr_list[i]] = row[i]
            user_info["permission_list"] = self.get_permission_list(user_info["user_id"])
        self._pg.close()
        return user_info
    
    def get_permission_list(self, user_id):
        result_permission_list = []
        sqlcmd = """
        SELECT group_id, array_agg(role_id) FROM spec.arl_group_member WHERE user_id = %s GROUP BY group_id 
        """
        self._pg.connect()
        self._pg.execute(sqlcmd, (user_id, ))
        rows = self._pg.fetchall()
        for row in rows:
            ret_dict = {}
            # ret_dict_keys = ["group_id", "group_name","read_all", "modify_all",
            #                  "read_group", "modify_group","read_self","modify_self",
            #                  "mng_group", "mng_member"]

            ret_dict["group_id"] = row[0]
            ret_dict["roles"] = row[1]
            result_permission_list.append(ret_dict)
        self._pg.close()
        return result_permission_list

    def get_all_user(self):
        sqlcmd = """
        SELECT user_id, user_name
          FROM spec.arl_user
          ORDER BY user_name;
        """
        data = {"result": "NG"}
        user_list = []
        self._pg.connect()
        self._pg.execute(sqlcmd)
        rows = self._pg.fetchall()
        for row in rows:
            user_info = dict()
            user_info["user_id"] = row[0]
            user_info["user_name"] = row[1]
            user_list.append(user_info)
        if user_list:
            data["content"] = user_list
            data["total_count"] = len(rows)
            data["result"] = "OK"
        self._pg.close()
        return data

    def delete(self, user_id):
        sqlcmd = """
        -- del member
        DELETE FROM spec.arl_group_member
          WHERE user_id = %s;
        -- del user
        DELETE FROM spec.arl_user
          WHERE user_id = %s;
        """
        result = {"result": "NG"}
        try:
            self._pg.connect()
            self._pg.execute(sqlcmd, (user_id, user_id))
            self._pg.commit()
            result = {"result": "OK"}
        finally:
            self._pg.close()
            return result

    def get_email(self, user_id):
        sqlcmd = """
        select email
         from spec.arl_user
         where user_id = %s
        """
        self._pg.connect()
        self._pg.execute(sqlcmd, (user_id,))
        row = self._pg.fetchone()
        if row:
            email = row[0]
            return email
        self._pg.close()
        return None

    def alter_email(self, user_id, email):
        sqlcmd = """update spec.arl_user 
                     set email = %s 
                     where user_id = %s
                  """
        self._pg.connect()
        self._pg.execute(sqlcmd, (email, user_id))
        self._pg.commit()
        self._pg.close()
        return {"result": "OK"}

    def find_user_by_name(self, user_name):
        sqlcmd1 = """
            SELECT user_id from spec.arl_user WHERE user_name = %s;
        """
        sqlcmd2 = """
            INSERT into spec.arl_user(user_name) VALUES (%s);
            RETURNING user_id;
        """
        self._pg.connect()
        self._pg.execute(sqlcmd1, (user_name,))
        row = self._pg.fetchone()
        if row:
            user_id = row[0]
            self._pg.close()
            return user_id
        else:
            self._pg.execute(sqlcmd2, (user_name,))
            self._pg.commit()
            user_id = self.fetch_id()
            self._pg.close()
            return user_id

    def find_group_by_userId(self, user_id):
        self._pg.connect()
        data = self._find_group_by_userId(self._pg, user_id)
        self._pg.close()
        return data

    def _find_group_by_userId(self, pg, user_id):
        sqlcmd = """
            SELECT a.group_id, group_name FROM spec.arl_group as a LEFT JOIN 
            spec.arl_group_member as b on a.group_id = b.group_id
            WHERE user_id = %s and role_id = 4
        """
        pg.execute(sqlcmd, (user_id,))
        rows = pg.fetchall()
        group_list = []
        if rows:
            for row in rows:
                group_dict = dict()
                group_dict["group_id"] = row[0]
                group_dict["group_name"] = row[1]
                group_list.append(group_dict)
        return group_list

    def get_user_powr(self, pg, role_id):
        sqlcmd = """
            SELECT read_all, modify_all, read_group, modify_group,
            read_self, modify_self, mng_group, mng_member FROM spec.arl_role_power 
            WHERE role_id = %s
        """
        ret_dict_keys = ["read_all", "modify_all", "read_group", "modify_group",
                         "read_self", "modify_self", "mng_group", "mng_member"]
        pg.execute(sqlcmd, (role_id,))
        rows = pg.fetchone()
        powr_dict = dict()
        if rows:
            for i in range(0, len(ret_dict_keys)):
                powr_dict[ret_dict_keys[i]] = rows[i]
        return powr_dict






