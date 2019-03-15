
import ldap
ldapServer = 'LDAP://apolo.storm'
domain = 'storm'


def login(username, password):
    try:
        from Source.collaboration.api_if import app
        conn = ldap.initialize(app.config["LDAP_PROVIDER_URL"])
        domain_username = domain + '\\' + username
        conn.simple_bind_s(domain_username, password)
        return {'result': True, "username": username}
    except Exception as e:
        print e
        return {'result': False, "username": ''}