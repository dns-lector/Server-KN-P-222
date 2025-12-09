import base64, data.helper as helper, datetime, hashlib, hmac, json, mysql.connector, os, uuid

class DataAccessor:
    def __init__(self, ini_file:str='/data/db_ini.json') :
        try :
            path = os.path.abspath('./')
            with open(path + ini_file, mode="r", encoding='utf-8') as file :
                ini_data = json.load(file)
            self.db_connection = mysql.connector.connect(**ini_data)
        except Exception as err :
            raise RuntimeError(str(err))


    def authenticate(self, login:str, password:str) :
        sql = """SELECT 
        * 
        FROM user_accesses ua 
            JOIN users u ON ua.user_id = u.user_id
        WHERE 
            ua.ua_login = ? """
        with self.db_connection.cursor(prepared=True, dictionary=True) as cursor :
            cursor.execute( sql, (login,) )
            user = next(cursor, None)
        if user and user['ua_dk'] == helper.kdf(password, user['ua_salt']) :
            # return user
            # генеруємо токен:
            # формуємо дані
            token_header = {
                "alg": "HS256",
                "typ": "JWT"
            }
            now = datetime.datetime.now()
            token_payload = {
                'jti': uuid.uuid4(),
                'sub': user['user_id'],
                'iat': int(now.timestamp()),
                'exp': int((now + datetime.timedelta(minutes=1)).timestamp()),
                'name': user['user_name'],
                'email': user['user_email'],
            }
            token_body = ( 
                base64.urlsafe_b64encode(json.dumps(token_header).encode()).decode("ascii")
                + '.' 
                + base64.urlsafe_b64encode(json.dumps(token_payload, ensure_ascii=False, default=str).encode()).decode("ascii")
            )
            token_signature = base64.urlsafe_b64encode( 
                hmac.new(
                    b"secret",
                    token_body.encode(),
                    hashlib.sha256
                ).digest()
            ).decode("ascii")
            # sql = "INSERT INTO tokens(token_id, ua_id, token_issued_at, token_expired_at) VALUES(?,?,?,?) "
            return token_body + '.' + token_signature
        return None

    
    def install(self, with_seed:bool=False) -> bool :
        try :
            self._install_users() 
            self._install_user_roles()
            self._install_user_accesses()
            self._install_user_tokens()
            if with_seed :
                self._seed()
        except mysql.connector.Error as err :
            print(err)
            return False
        else :
            return True


    def _seed(self) :
        self._seed_roles()
        self._seed_users()
        self._seed_user_accesses()


    def _seed_roles(self) :
        sql = """
        INSERT INTO user_roles(
            role_id, role_description, role_can_create, 
            role_can_read, role_can_update, role_can_delete)            
        VALUES(?, ?, ?, ?, ?, ?)
        ON DUPLICATE KEY UPDATE
            role_description = VALUES(role_description),
            role_can_create  = VALUES(role_can_create),
            role_can_read    = VALUES(role_can_read),
            role_can_update  = VALUES(role_can_update),
            role_can_delete  = VALUES(role_can_delete)"""
        
        with self.db_connection.cursor(prepared=True) as cursor :
            cursor.executemany(sql, [
                ('admin', 'Root Administrator',   1, 1, 1, 1),
                ('guest', 'Self Registered User', 0, 0, 0, 0),
            ])
        self.db_connection.commit()


    def _seed_users(self) :
        sql = """INSERT INTO users(user_id, user_name, user_email) VALUES(?, ?, ?)
        ON DUPLICATE KEY UPDATE 
            user_name  = VALUES(user_name),
            user_email = VALUES(user_email)"""
        
        with self.db_connection.cursor(prepared=True) as cursor :
            cursor.execute(sql,
                ('69231c55-9851-11f0-b1b7-62517600596c', 'Default Administrator', 'admin@localhost')
            )
        self.db_connection.commit()


    def _seed_user_accesses(self) :
        sql = """INSERT INTO user_accesses(ua_id, user_id, role_id, ua_login, ua_salt, ua_dk)
        VALUES(?, ?, ?, ?, ?, ?) 
        ON DUPLICATE KEY UPDATE 
            user_id  = VALUES(user_id),
            role_id  = VALUES(role_id),
            ua_login = VALUES(ua_login),
            ua_salt  = VALUES(ua_salt),
            ua_dk    = VALUES(ua_dk)"""
        
        with self.db_connection.cursor(prepared=True) as cursor :
            cursor.execute(sql,
                ('35326873-9852-11f0-b1b7-62517600596c', 
                '69231c55-9851-11f0-b1b7-62517600596c', 
                'admin', 
                'admin',
                'Xlx7sUpjQamRQamR', 
                helper.kdf("admin", "Xlx7sUpjQamRQamR"))
            )
        self.db_connection.commit()


    def _install_users(self) :
        sql = """CREATE TABLE  IF NOT EXISTS  users(
            user_id            CHAR(36)     PRIMARY KEY,
            user_name          VARCHAR(64)  NOT NULL,
            user_email         VARCHAR(128) NOT NULL,
            user_birthdate     DATETIME     NULL,
            user_registered_at DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
            user_deleted_at    DATETIME     NULL
        ) ENGINE = InnoDb, 
          DEFAULT CHARSET = utf8mb4,
          COLLATE utf8mb4_unicode_ci"""
        with self.db_connection.cursor() as cursor :
            cursor.execute(sql)


    def _install_user_roles(self) :
        sql = """CREATE TABLE  IF NOT EXISTS  user_roles(
            role_id          VARCHAR(16)  PRIMARY KEY,
            role_description VARCHAR(256) NOT NULL,
            role_can_create  TINYINT      NOT NULL DEFAULT 0,
            role_can_read    TINYINT      NOT NULL DEFAULT 0,
            role_can_update  TINYINT      NOT NULL DEFAULT 0,
            role_can_delete  TINYINT      NOT NULL DEFAULT 0
        ) ENGINE = InnoDb, 
          DEFAULT CHARSET = utf8mb4,
          COLLATE utf8mb4_unicode_ci"""
        with self.db_connection.cursor() as cursor :
            cursor.execute(sql)


    def _install_user_accesses(self) :
        sql = """CREATE TABLE  IF NOT EXISTS  user_accesses(
            ua_id     CHAR(36)    PRIMARY KEY,
            user_id   CHAR(36)    NOT NULL,
            role_id   VARCHAR(16) NOT NULL,
            ua_login  VARCHAR(32) NOT NULL,
            ua_salt   CHAR(16)    NOT NULL,
            ua_dk     CHAR(32)    NOT NULL,
            UNIQUE(ua_login)
        ) ENGINE = InnoDb, 
          DEFAULT CHARSET = utf8mb4,
          COLLATE utf8mb4_unicode_ci"""
        with self.db_connection.cursor() as cursor :
            cursor.execute(sql)


    def _install_user_tokens(self) :
        sql = """CREATE TABLE  IF NOT EXISTS  tokens(
            token_id         CHAR(36) PRIMARY KEY,
            ua_id            CHAR(36) NOT NULL COMMENT 'user_access_id',
            token_issued_at  DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            token_expired_at DATETIME NULL
        ) ENGINE = InnoDb, 
          DEFAULT CHARSET = utf8mb4,
          COLLATE utf8mb4_unicode_ci"""
        with self.db_connection.cursor() as cursor :
            cursor.execute(sql)

