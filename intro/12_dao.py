# Data Accessor - проміжний "шар" (layer) між контролерами та даними (БД)
import json
import mysql.connector
import helper

class DataAccessor:
    def __init__(self, ini_file:str='db_ini.json') :
        try :
            with open(ini_file, mode="r", encoding='utf-8') as file :
                ini_data = json.load(file)
            self.db_connection = mysql.connector.connect(**ini_data)
        except Exception as err :
            raise RuntimeError(str(err))
        
    
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



def main() :
    try :
        dataAccessor = DataAccessor()
    except RuntimeError as err :
        print(err)
        return
    else :
        print("Connection OK")

    if dataAccessor.install(with_seed=True) :
        print("Install OK")
    else :
        return
    
    print( helper.salt() )


if __name__ == '__main__' :
    main()

'''
Д.З. Створити метод _seed_token, реалізувати внесення токена
для адміністратора, що є у БД. Тривалість токена - 1 день

Встановити XAMPP https://www.apachefriends.org/download.html
Головний модуль - Apache, все інше - за бажанням
'''