import os
import json

from pathlib import Path

from unittest import IsolatedAsyncioTestCase

from helpers.configuration.postgresql_conf import pg_conf
from helpers.work_classes import ReturnEntity
from helpers.work_classes import PgConf


class PgConfTests(IsolatedAsyncioTestCase):
    """
    Class describing tests for helpers.configuration.postgresql_conf.pg_conf
    """

    async def asyncSetUp(self):
        self.conf_path = Path('/conf/pg-test.yaml')
        with open(self.conf_path, 'w') as file:
            file.write('database:\n'
                       '  name: pg_test_db\n'
                       '  rw:\n'
                       '    host: postgresql\n'
                       '    port: 5432\n'
                       '    user: pg_test_user\n'
                       '    password: pgTestPassword\n'
                       '    maxConn: 4\n'
                       '  ro:\n'
                       '    host: postgresql_ro\n'
                       '    port: 5433\n'
                       '    user: pg_test_user_ro\n'
                       '    password: pgTestPasswordRo\n'
                       '    maxConn: 3')

    async def asyncTearDown(self):
        os.environ.pop('DB_NAME', None)
        os.environ.pop('DB_RW_HOST', None)
        os.environ.pop('DB_RW_PORT', None)
        os.environ.pop('DB_RW_USER', None)
        os.environ.pop('DB_RW_PAS', None)
        os.environ.pop('DB_RW_CON', None)
        os.environ.pop('DB_RO_HOST', None)
        os.environ.pop('DB_RO_PORT', None)
        os.environ.pop('DB_RO_USER', None)
        os.environ.pop('DB_RO_PAS', None)
        os.environ.pop('DB_RO_CON', None)
        os.remove(self.conf_path)

    async def test_read_from_file(self):
        result: ReturnEntity = pg_conf(self.conf_path)
        if result.error:
            for error in result.errorText.split('|'):
                print(error)
        self.assertFalse(result.error)
        result_entity: PgConf = result.entity
        print(json.dumps(result_entity.to_dict(), indent=4, sort_keys=True))
        self.assertEqual('pg_test_db', result_entity.name)
        self.assertEqual('postgresql', result_entity.rw.host)
        self.assertEqual(5432, result_entity.rw.port)
        self.assertEqual('pg_test_user', result_entity.rw.user)
        self.assertEqual('pgTestPassword', result_entity.rw.password)
        self.assertEqual(4, result_entity.rw.maxConn)
        self.assertEqual('postgresql_ro', result_entity.ro.host)
        self.assertEqual(5433, result_entity.ro.port)
        self.assertEqual('pg_test_user_ro', result_entity.ro.user)
        self.assertEqual('pgTestPasswordRo', result_entity.ro.password)
        self.assertEqual(3, result_entity.ro.maxConn)

    async def test_not_conf_file_not_env(self):
        result: ReturnEntity = pg_conf(Path('/conf/app-conf.yaml'))
        if result.error:
            for error in result.errorText.split('|'):
                print(error)
        self.assertTrue(result.error)
        self.assertIn('Configuration file /conf/app-conf.yaml is missing', result.errorText)
        self.assertIn('Database name not configured', result.errorText)
        self.assertIn('The database connection host is not configured for writing and reading', result.errorText)
        self.assertIn('The port for connecting to the database for writing and reading is not configured',
                      result.errorText)
        self.assertIn('The user for connecting to the database for writing and reading is not configured',
                      result.errorText)
        self.assertIn('The password for connecting to the database for writing and reading is not configured',
                      result.errorText)

    async def test_env_var(self):
        os.environ['DB_NAME'] = 'test_env_var_db'
        os.environ['DB_RW_HOST'] = 'pg_rw_host'
        os.environ['DB_RW_PORT'] = '654321'
        os.environ['DB_RW_USER'] = 'test_env_var_rw_user'
        os.environ['DB_RW_PAS'] = 'test_env_var_rw_password'
        os.environ['DB_RW_CON'] = '10'
        os.environ['DB_RO_HOST'] = 'pg_ro_host'
        os.environ['DB_RO_PORT'] = '654322'
        os.environ['DB_RO_USER'] = 'test_env_var_ro_user'
        os.environ['DB_RO_PAS'] = 'test_env_var_ro_password'
        os.environ['DB_RO_CON'] = '7'
        result: ReturnEntity = pg_conf(self.conf_path)
        if result.error:
            for error in result.errorText.split('|'):
                print(error)
        self.assertFalse(result.error)
        result_entity: PgConf = result.entity
        print(json.dumps(result_entity.to_dict(), indent=4, sort_keys=True))
        self.assertEqual('test_env_var_db', result_entity.name)
        self.assertEqual('pg_rw_host', result_entity.rw.host)
        self.assertEqual(654321, result_entity.rw.port)
        self.assertEqual('test_env_var_rw_user', result_entity.rw.user)
        self.assertEqual('test_env_var_rw_password', result_entity.rw.password)
        self.assertEqual(10, result_entity.rw.maxConn)
        self.assertEqual('pg_ro_host', result_entity.ro.host)
        self.assertEqual(654322, result_entity.ro.port)
        self.assertEqual('test_env_var_ro_user', result_entity.ro.user)
        self.assertEqual('test_env_var_ro_password', result_entity.ro.password)
        self.assertEqual(7, result_entity.ro.maxConn)

    async def test_not_db_name(self):
        os.environ['DB_RW_HOST'] = 'pg_rw_host'
        os.environ['DB_RW_PORT'] = '654321'
        os.environ['DB_RW_USER'] = 'test_env_var_rw_user'
        os.environ['DB_RW_PAS'] = 'test_env_var_rw_password'
        os.environ['DB_RW_CON'] = '50'
        os.environ['DB_RO_HOST'] = 'pg_ro_host'
        os.environ['DB_RO_PORT'] = '654322'
        os.environ['DB_RO_USER'] = 'test_env_var_ro_user'
        os.environ['DB_RO_PAS'] = 'test_env_var_ro_password'
        os.environ['DB_RO_CON'] = '30'
        result: ReturnEntity = pg_conf(Path('/conf/app-conf.yaml'))
        if result.error:
            for error in result.errorText.split('|'):
                print(error)
        self.assertTrue(result.error)
        self.assertIn('Configuration file /conf/app-conf.yaml is missing', result.errorText)
        self.assertIn('Database name not configured', result.errorText)

    async def test_not_rw_host(self):
        os.environ['DB_NAME'] = 'test_env_var_db'
        os.environ['DB_RW_PORT'] = '654321'
        os.environ['DB_RW_USER'] = 'test_env_var_rw_user'
        os.environ['DB_RW_PAS'] = 'test_env_var_rw_password'
        os.environ['DB_RW_CON'] = '50'
        os.environ['DB_RO_HOST'] = 'pg_ro_host'
        os.environ['DB_RO_PORT'] = '654322'
        os.environ['DB_RO_USER'] = 'test_env_var_ro_user'
        os.environ['DB_RO_PAS'] = 'test_env_var_ro_password'
        os.environ['DB_RO_CON'] = '30'
        result: ReturnEntity = pg_conf(Path('/conf/app-conf.yaml'))
        if result.error:
            for error in result.errorText.split('|'):
                print(error)
        self.assertTrue(result.error)
        self.assertIn('Configuration file /conf/app-conf.yaml is missing', result.errorText)
        self.assertIn('The database connection host is not configured for writing and reading', result.errorText)

    async def test_not_rw_port(self):
        os.environ['DB_NAME'] = 'test_env_var_db'
        os.environ['DB_RW_HOST'] = 'pg_rw_host'
        os.environ['DB_RW_USER'] = 'test_env_var_rw_user'
        os.environ['DB_RW_PAS'] = 'test_env_var_rw_password'
        os.environ['DB_RW_CON'] = '50'
        os.environ['DB_RO_HOST'] = 'pg_ro_host'
        os.environ['DB_RO_PORT'] = '654322'
        os.environ['DB_RO_USER'] = 'test_env_var_ro_user'
        os.environ['DB_RO_PAS'] = 'test_env_var_ro_password'
        os.environ['DB_RO_CON'] = '30'
        result: ReturnEntity = pg_conf(Path('/conf/app-conf.yaml'))
        if result.error:
            for error in result.errorText.split('|'):
                print(error)
        self.assertTrue(result.error)
        self.assertIn('Configuration file /conf/app-conf.yaml is missing', result.errorText)
        self.assertIn('The port for connecting to the database for writing and reading is not configured',
                      result.errorText)

    async def test_not_rw_user(self):
        os.environ['DB_NAME'] = 'test_env_var_db'
        os.environ['DB_RW_HOST'] = 'pg_rw_host'
        os.environ['DB_RW_PORT'] = '654321'
        os.environ['DB_RW_PAS'] = 'test_env_var_rw_password'
        os.environ['DB_RW_CON'] = '50'
        os.environ['DB_RO_HOST'] = 'pg_ro_host'
        os.environ['DB_RO_PORT'] = '654322'
        os.environ['DB_RO_USER'] = 'test_env_var_ro_user'
        os.environ['DB_RO_PAS'] = 'test_env_var_ro_password'
        os.environ['DB_RO_CON'] = '30'
        result: ReturnEntity = pg_conf(Path('/conf/app-conf.yaml'))
        if result.error:
            for error in result.errorText.split('|'):
                print(error)
        self.assertTrue(result.error)
        self.assertIn('Configuration file /conf/app-conf.yaml is missing', result.errorText)
        self.assertIn('The user for connecting to the database for writing and reading is not configured',
                      result.errorText)

    async def test_not_rw_password(self):
        os.environ['DB_NAME'] = 'test_env_var_db'
        os.environ['DB_RW_HOST'] = 'pg_rw_host'
        os.environ['DB_RW_PORT'] = '654321'
        os.environ['DB_RW_USER'] = 'test_env_var_rw_user'
        os.environ['DB_RW_CON'] = '50'
        os.environ['DB_RO_HOST'] = 'pg_ro_host'
        os.environ['DB_RO_PORT'] = '654322'
        os.environ['DB_RO_USER'] = 'test_env_var_ro_user'
        os.environ['DB_RO_PAS'] = 'test_env_var_ro_password'
        os.environ['DB_RO_CON'] = '30'
        result: ReturnEntity = pg_conf(Path('/conf/app-conf.yaml'))
        if result.error:
            for error in result.errorText.split('|'):
                print(error)
        self.assertTrue(result.error)
        self.assertIn('Configuration file /conf/app-conf.yaml is missing', result.errorText)
        self.assertIn('The password for connecting to the database for writing and reading is not configured',
                      result.errorText)

    async def test_not_rw_maxCon(self):
        os.environ['DB_NAME'] = 'test_env_var_db'
        os.environ['DB_RW_HOST'] = 'pg_rw_host'
        os.environ['DB_RW_PORT'] = '654321'
        os.environ['DB_RW_USER'] = 'test_env_var_rw_user'
        os.environ['DB_RW_PAS'] = 'test_env_var_rw_password'
        os.environ['DB_RO_HOST'] = 'pg_ro_host'
        os.environ['DB_RO_PORT'] = '654322'
        os.environ['DB_RO_USER'] = 'test_env_var_ro_user'
        os.environ['DB_RO_PAS'] = 'test_env_var_ro_password'
        os.environ['DB_RO_CON'] = '40'
        result: ReturnEntity = pg_conf(Path('/conf/app-conf.yaml'))
        if result.error:
            for error in result.errorText.split('|'):
                print(error)
        self.assertFalse(result.error)
        result_entity: PgConf = result.entity
        print(json.dumps(result_entity.to_dict(), indent=4, sort_keys=True))
        self.assertEqual('test_env_var_db', result_entity.name)
        self.assertEqual('pg_rw_host', result_entity.rw.host)
        self.assertEqual(654321, result_entity.rw.port)
        self.assertEqual('test_env_var_rw_user', result_entity.rw.user)
        self.assertEqual('test_env_var_rw_password', result_entity.rw.password)
        self.assertEqual(5, result_entity.rw.maxConn)
        self.assertEqual('pg_ro_host', result_entity.ro.host)
        self.assertEqual(654322, result_entity.ro.port)
        self.assertEqual('test_env_var_ro_user', result_entity.ro.user)
        self.assertEqual('test_env_var_ro_password', result_entity.ro.password)
        self.assertEqual(40, result_entity.ro.maxConn)

    async def test_not_ro_section(self):
        os.environ['DB_NAME'] = 'test_env_var_db'
        os.environ['DB_RW_HOST'] = 'pg_rw_host'
        os.environ['DB_RW_PORT'] = '654321'
        os.environ['DB_RW_USER'] = 'test_env_var_rw_user'
        os.environ['DB_RW_PAS'] = 'test_env_var_rw_password'
        os.environ['DB_RW_CON'] = '50'
        result: ReturnEntity = pg_conf(Path('/conf/app-conf.yaml'))
        if result.error:
            for error in result.errorText.split('|'):
                print(error)
        self.assertFalse(result.error)
        result_entity: PgConf = result.entity
        print(json.dumps(result_entity.to_dict(), indent=4, sort_keys=True))
        self.assertEqual('test_env_var_db', result_entity.name)
        self.assertEqual('pg_rw_host', result_entity.rw.host)
        self.assertEqual(654321, result_entity.rw.port)
        self.assertEqual('test_env_var_rw_user', result_entity.rw.user)
        self.assertEqual('test_env_var_rw_password', result_entity.rw.password)
        self.assertEqual(50, result_entity.rw.maxConn)
        self.assertEqual('pg_rw_host', result_entity.ro.host)
        self.assertEqual(654321, result_entity.ro.port)
        self.assertEqual('test_env_var_rw_user', result_entity.ro.user)
        self.assertEqual('test_env_var_rw_password', result_entity.ro.password)
        self.assertEqual(50, result_entity.ro.maxConn)

    async def test_not_ro_host(self):
        os.environ['DB_NAME'] = 'test_env_var_db'
        os.environ['DB_RW_HOST'] = 'pg_rw_host'
        os.environ['DB_RW_PORT'] = '654321'
        os.environ['DB_RW_USER'] = 'test_env_var_rw_user'
        os.environ['DB_RW_PAS'] = 'test_env_var_rw_password'
        os.environ['DB_RW_CON'] = '50'
        os.environ['DB_RO_PORT'] = '654322'
        os.environ['DB_RO_USER'] = 'test_env_var_ro_user'
        os.environ['DB_RO_PAS'] = 'test_env_var_ro_password'
        os.environ['DB_RO_CON'] = '40'
        result: ReturnEntity = pg_conf(Path('/conf/app-conf.yaml'))
        if result.error:
            for error in result.errorText.split('|'):
                print(error)
        self.assertFalse(result.error)
        result_entity: PgConf = result.entity
        print(json.dumps(result_entity.to_dict(), indent=4, sort_keys=True))
        self.assertEqual('test_env_var_db', result_entity.name)
        self.assertEqual('pg_rw_host', result_entity.rw.host)
        self.assertEqual(654321, result_entity.rw.port)
        self.assertEqual('test_env_var_rw_user', result_entity.rw.user)
        self.assertEqual('test_env_var_rw_password', result_entity.rw.password)
        self.assertEqual(50, result_entity.rw.maxConn)
        self.assertEqual('pg_rw_host', result_entity.ro.host)
        self.assertEqual(654322, result_entity.ro.port)
        self.assertEqual('test_env_var_ro_user', result_entity.ro.user)
        self.assertEqual('test_env_var_ro_password', result_entity.ro.password)
        self.assertEqual(40, result_entity.ro.maxConn)

    async def test_not_ro_port(self):
        os.environ['DB_NAME'] = 'test_env_var_db'
        os.environ['DB_RW_HOST'] = 'pg_rw_host'
        os.environ['DB_RW_PORT'] = '654321'
        os.environ['DB_RW_USER'] = 'test_env_var_rw_user'
        os.environ['DB_RW_PAS'] = 'test_env_var_rw_password'
        os.environ['DB_RW_CON'] = '50'
        os.environ['DB_RO_HOST'] = 'pg_ro_host'
        os.environ['DB_RO_USER'] = 'test_env_var_ro_user'
        os.environ['DB_RO_PAS'] = 'test_env_var_ro_password'
        os.environ['DB_RO_CON'] = '40'
        result: ReturnEntity = pg_conf(Path('/conf/app-conf.yaml'))
        if result.error:
            for error in result.errorText.split('|'):
                print(error)
        self.assertFalse(result.error)
        result_entity: PgConf = result.entity
        print(json.dumps(result_entity.to_dict(), indent=4, sort_keys=True))
        self.assertEqual('test_env_var_db', result_entity.name)
        self.assertEqual('pg_rw_host', result_entity.rw.host)
        self.assertEqual(654321, result_entity.rw.port)
        self.assertEqual('test_env_var_rw_user', result_entity.rw.user)
        self.assertEqual('test_env_var_rw_password', result_entity.rw.password)
        self.assertEqual(50, result_entity.rw.maxConn)
        self.assertEqual('pg_ro_host', result_entity.ro.host)
        self.assertEqual(654321, result_entity.ro.port)
        self.assertEqual('test_env_var_ro_user', result_entity.ro.user)
        self.assertEqual('test_env_var_ro_password', result_entity.ro.password)
        self.assertEqual(40, result_entity.ro.maxConn)

    async def test_not_ro_user(self):
        os.environ['DB_NAME'] = 'test_env_var_db'
        os.environ['DB_RW_HOST'] = 'pg_rw_host'
        os.environ['DB_RW_PORT'] = '654321'
        os.environ['DB_RW_USER'] = 'test_env_var_rw_user'
        os.environ['DB_RW_PAS'] = 'test_env_var_rw_password'
        os.environ['DB_RW_CON'] = '50'
        os.environ['DB_RO_HOST'] = 'pg_ro_host'
        os.environ['DB_RO_PORT'] = '654322'
        os.environ['DB_RO_PAS'] = 'test_env_var_ro_password'
        os.environ['DB_RO_CON'] = '40'
        result: ReturnEntity = pg_conf(Path('/conf/app-conf.yaml'))
        if result.error:
            for error in result.errorText.split('|'):
                print(error)
        self.assertFalse(result.error)
        result_entity: PgConf = result.entity
        print(json.dumps(result_entity.to_dict(), indent=4, sort_keys=True))
        self.assertEqual('test_env_var_db', result_entity.name)
        self.assertEqual('pg_rw_host', result_entity.rw.host)
        self.assertEqual(654321, result_entity.rw.port)
        self.assertEqual('test_env_var_rw_user', result_entity.rw.user)
        self.assertEqual('test_env_var_rw_password', result_entity.rw.password)
        self.assertEqual(50, result_entity.rw.maxConn)
        self.assertEqual('pg_ro_host', result_entity.ro.host)
        self.assertEqual(654322, result_entity.ro.port)
        self.assertEqual('test_env_var_rw_user', result_entity.ro.user)
        self.assertEqual('test_env_var_ro_password', result_entity.ro.password)
        self.assertEqual(40, result_entity.ro.maxConn)

    async def test_not_ro_password(self):
        os.environ['DB_NAME'] = 'test_env_var_db'
        os.environ['DB_RW_HOST'] = 'pg_rw_host'
        os.environ['DB_RW_PORT'] = '654321'
        os.environ['DB_RW_USER'] = 'test_env_var_rw_user'
        os.environ['DB_RW_PAS'] = 'test_env_var_rw_password'
        os.environ['DB_RW_CON'] = '50'
        os.environ['DB_RO_HOST'] = 'pg_ro_host'
        os.environ['DB_RO_PORT'] = '654322'
        os.environ['DB_RO_USER'] = 'test_env_var_ro_user'
        os.environ['DB_RO_CON'] = '40'
        result: ReturnEntity = pg_conf(Path('/conf/app-conf.yaml'))
        if result.error:
            for error in result.errorText.split('|'):
                print(error)
        self.assertFalse(result.error)
        result_entity: PgConf = result.entity
        print(json.dumps(result_entity.to_dict(), indent=4, sort_keys=True))
        self.assertEqual('test_env_var_db', result_entity.name)
        self.assertEqual('pg_rw_host', result_entity.rw.host)
        self.assertEqual(654321, result_entity.rw.port)
        self.assertEqual('test_env_var_rw_user', result_entity.rw.user)
        self.assertEqual('test_env_var_rw_password', result_entity.rw.password)
        self.assertEqual(50, result_entity.rw.maxConn)
        self.assertEqual('pg_ro_host', result_entity.ro.host)
        self.assertEqual(654322, result_entity.ro.port)
        self.assertEqual('test_env_var_ro_user', result_entity.ro.user)
        self.assertEqual('test_env_var_rw_password', result_entity.ro.password)
        self.assertEqual(40, result_entity.ro.maxConn)

    async def test_not_ro_maxCon(self):
        os.environ['DB_NAME'] = 'test_env_var_db'
        os.environ['DB_RW_HOST'] = 'pg_rw_host'
        os.environ['DB_RW_PORT'] = '654321'
        os.environ['DB_RW_USER'] = 'test_env_var_rw_user'
        os.environ['DB_RW_PAS'] = 'test_env_var_rw_password'
        os.environ['DB_RW_CON'] = '35'
        os.environ['DB_RO_HOST'] = 'pg_ro_host'
        os.environ['DB_RO_PORT'] = '654322'
        os.environ['DB_RO_USER'] = 'test_env_var_ro_user'
        os.environ['DB_RO_PAS'] = 'test_env_var_ro_password'
        result: ReturnEntity = pg_conf(Path('/conf/app-conf.yaml'))
        if result.error:
            for error in result.errorText.split('|'):
                print(error)
        self.assertFalse(result.error)
        result_entity: PgConf = result.entity
        print(json.dumps(result_entity.to_dict(), indent=4, sort_keys=True))
        self.assertEqual('test_env_var_db', result_entity.name)
        self.assertEqual('pg_rw_host', result_entity.rw.host)
        self.assertEqual(654321, result_entity.rw.port)
        self.assertEqual('test_env_var_rw_user', result_entity.rw.user)
        self.assertEqual('test_env_var_rw_password', result_entity.rw.password)
        self.assertEqual(35, result_entity.rw.maxConn)
        self.assertEqual('pg_ro_host', result_entity.ro.host)
        self.assertEqual(654322, result_entity.ro.port)
        self.assertEqual('test_env_var_ro_user', result_entity.ro.user)
        self.assertEqual('test_env_var_ro_password', result_entity.ro.password)
        self.assertEqual(35, result_entity.ro.maxConn)

    async def test_rw_port_negative_env(self):
        os.environ['DB_RW_PORT'] = '-5432'
        result: ReturnEntity = pg_conf(self.conf_path)
        if result.error:
            for error in result.errorText.split('|'):
                print(error)
        self.assertTrue(result.error)
        self.assertIn('Port must be a positive integer', result.errorText)

    async def test_ro_port_negative_env(self):
        os.environ['DB_RO_PORT'] = '-5433'
        result: ReturnEntity = pg_conf(self.conf_path)
        if result.error:
            for error in result.errorText.split('|'):
                print(error)
        self.assertFalse(result.error)
        result_entity: PgConf = result.entity
        print(json.dumps(result_entity.to_dict(), indent=4, sort_keys=True))
        self.assertEqual('pg_test_db', result_entity.name)
        self.assertEqual('postgresql', result_entity.rw.host)
        self.assertEqual(5432, result_entity.rw.port)
        self.assertEqual('pg_test_user', result_entity.rw.user)
        self.assertEqual('pgTestPassword', result_entity.rw.password)
        self.assertEqual('postgresql_ro', result_entity.ro.host)
        self.assertEqual(5432, result_entity.ro.port)
        self.assertEqual('pg_test_user_ro', result_entity.ro.user)
        self.assertEqual('pgTestPasswordRo', result_entity.ro.password)

    async def test_rw_port_float_env(self):
        os.environ['DB_RW_PORT'] = '5433.3268'
        result: ReturnEntity = pg_conf(self.conf_path)
        if result.error:
            for error in result.errorText.split('|'):
                print(error)
        self.assertTrue(result.error)
        self.assertIn('Port must be a positive integer', result.errorText)

    async def test_rw_port_boolean_env(self):
        os.environ['DB_RW_PORT'] = 'true'
        result: ReturnEntity = pg_conf(self.conf_path)
        if result.error:
            for error in result.errorText.split('|'):
                print(error)
        self.assertTrue(result.error)
        self.assertIn('Port must be a positive integer', result.errorText)

    async def test_ro_port_float_env(self):
        os.environ['DB_RO_PORT'] = '5465.33'
        result: ReturnEntity = pg_conf(self.conf_path)
        if result.error:
            for error in result.errorText.split('|'):
                print(error)
        self.assertFalse(result.error)
        result_entity: PgConf = result.entity
        print(json.dumps(result_entity.to_dict(), indent=4, sort_keys=True))
        self.assertEqual('pg_test_db', result_entity.name)
        self.assertEqual('postgresql', result_entity.rw.host)
        self.assertEqual(5432, result_entity.rw.port)
        self.assertEqual('pg_test_user', result_entity.rw.user)
        self.assertEqual('pgTestPassword', result_entity.rw.password)
        self.assertEqual('postgresql_ro', result_entity.ro.host)
        self.assertEqual(5432, result_entity.ro.port)
        self.assertEqual('pg_test_user_ro', result_entity.ro.user)
        self.assertEqual('pgTestPasswordRo', result_entity.ro.password)

    async def test_ro_port_boolean_env(self):
        os.environ['DB_RO_PORT'] = 'false'
        result: ReturnEntity = pg_conf(self.conf_path)
        if result.error:
            for error in result.errorText.split('|'):
                print(error)
        self.assertFalse(result.error)
        result_entity: PgConf = result.entity
        print(json.dumps(result_entity.to_dict(), indent=4, sort_keys=True))
        self.assertEqual('pg_test_db', result_entity.name)
        self.assertEqual('postgresql', result_entity.rw.host)
        self.assertEqual(5432, result_entity.rw.port)
        self.assertEqual('pg_test_user', result_entity.rw.user)
        self.assertEqual('pgTestPassword', result_entity.rw.password)
        self.assertEqual('postgresql_ro', result_entity.ro.host)
        self.assertEqual(5432, result_entity.ro.port)
        self.assertEqual('pg_test_user_ro', result_entity.ro.user)
        self.assertEqual('pgTestPasswordRo', result_entity.ro.password)

    async def test_rw_port_negative_file(self):
        with open(Path('/conf/pg-negative-test.yaml'), 'w') as file:
            file.write('database:\n'
                       '  name: pg_test_db\n'
                       '  rw:\n'
                       '    host: postgresql\n'
                       '    port: -5432\n'
                       '    user: pg_test_user\n'
                       '    password: pgTestPassword\n'
                       '  ro:\n'
                       '    host: postgresql_ro\n'
                       '    port: 5433\n'
                       '    user: pg_test_user_ro\n'
                       '    password: pgTestPasswordRo')
        result: ReturnEntity = pg_conf(Path('/conf/pg-negative-test.yaml'))
        os.remove(Path('/conf/pg-negative-test.yaml'))
        if result.error:
            for error in result.errorText.split('|'):
                print(error)
        self.assertTrue(result.error)
        self.assertIn('Port must be a positive integer', result.errorText)

    async def test_ro_port_negative_file(self):
        with open(Path('/conf/pg-negative-test.yaml'), 'w') as file:
            file.write('database:\n'
                       '  name: pg_test_db\n'
                       '  rw:\n'
                       '    host: postgresql\n'
                       '    port: 5432\n'
                       '    user: pg_test_user\n'
                       '    password: pgTestPassword\n'
                       '  ro:\n'
                       '    host: postgresql_ro\n'
                       '    port: -5433\n'
                       '    user: pg_test_user_ro\n'
                       '    password: pgTestPasswordRo')
        result: ReturnEntity = pg_conf(Path('/conf/pg-negative-test.yaml'))
        os.remove(Path('/conf/pg-negative-test.yaml'))
        if result.error:
            for error in result.errorText.split('|'):
                print(error)
        self.assertFalse(result.error)
        result_entity: PgConf = result.entity
        print(json.dumps(result_entity.to_dict(), indent=4, sort_keys=True))
        self.assertEqual('pg_test_db', result_entity.name)
        self.assertEqual('postgresql', result_entity.rw.host)
        self.assertEqual(5432, result_entity.rw.port)
        self.assertEqual('pg_test_user', result_entity.rw.user)
        self.assertEqual('pgTestPassword', result_entity.rw.password)
        self.assertEqual('postgresql_ro', result_entity.ro.host)
        self.assertEqual(5432, result_entity.ro.port)
        self.assertEqual('pg_test_user_ro', result_entity.ro.user)
        self.assertEqual('pgTestPasswordRo', result_entity.ro.password)

    async def test_rw_port_float_file(self):
        with open(Path('/conf/pg-negative-test.yaml'), 'w') as file:
            file.write('database:\n'
                       '  name: pg_test_db\n'
                       '  rw:\n'
                       '    host: postgresql\n'
                       '    port: 5433.3268\n'
                       '    user: pg_test_user\n'
                       '    password: pgTestPassword\n'
                       '  ro:\n'
                       '    host: postgresql_ro\n'
                       '    port: 5433\n'
                       '    user: pg_test_user_ro\n'
                       '    password: pgTestPasswordRo')
        result: ReturnEntity = pg_conf(Path('/conf/pg-negative-test.yaml'))
        os.remove(Path('/conf/pg-negative-test.yaml'))
        if result.error:
            for error in result.errorText.split('|'):
                print(error)
        self.assertTrue(result.error)
        self.assertIn('Port must be a positive integer', result.errorText)

    async def test_rw_port_boolean_file(self):
        with open(Path('/conf/pg-negative-test.yaml'), 'w') as file:
            file.write('database:\n'
                       '  name: pg_test_db\n'
                       '  rw:\n'
                       '    host: postgresql\n'
                       '    port: true\n'
                       '    user: pg_test_user\n'
                       '    password: pgTestPassword\n'
                       '  ro:\n'
                       '    host: postgresql_ro\n'
                       '    port: 5433\n'
                       '    user: pg_test_user_ro\n'
                       '    password: pgTestPasswordRo')
        result: ReturnEntity = pg_conf(Path('/conf/pg-negative-test.yaml'))
        os.remove(Path('/conf/pg-negative-test.yaml'))
        if result.error:
            for error in result.errorText.split('|'):
                print(error)
        self.assertTrue(result.error)
        self.assertIn('Port must be a positive integer', result.errorText)

    async def test_ro_port_float_file(self):
        with open(Path('/conf/pg-negative-test.yaml'), 'w') as file:
            file.write('database:\n'
                       '  name: pg_test_db\n'
                       '  rw:\n'
                       '    host: postgresql\n'
                       '    port: 5432\n'
                       '    user: pg_test_user\n'
                       '    password: pgTestPassword\n'
                       '  ro:\n'
                       '    host: postgresql_ro\n'
                       '    port: 5438.33\n'
                       '    user: pg_test_user_ro\n'
                       '    password: pgTestPasswordRo')
        result: ReturnEntity = pg_conf(Path('/conf/pg-negative-test.yaml'))
        os.remove(Path('/conf/pg-negative-test.yaml'))
        if result.error:
            for error in result.errorText.split('|'):
                print(error)
        self.assertFalse(result.error)
        result_entity: PgConf = result.entity
        print(json.dumps(result_entity.to_dict(), indent=4, sort_keys=True))
        self.assertEqual('pg_test_db', result_entity.name)
        self.assertEqual('postgresql', result_entity.rw.host)
        self.assertEqual(5432, result_entity.rw.port)
        self.assertEqual('pg_test_user', result_entity.rw.user)
        self.assertEqual('pgTestPassword', result_entity.rw.password)
        self.assertEqual('postgresql_ro', result_entity.ro.host)
        self.assertEqual(5432, result_entity.ro.port)
        self.assertEqual('pg_test_user_ro', result_entity.ro.user)
        self.assertEqual('pgTestPasswordRo', result_entity.ro.password)

    async def test_ro_port_boolean_file(self):
        with open(Path('/conf/pg-negative-test.yaml'), 'w') as file:
            file.write('database:\n'
                       '  name: pg_test_db\n'
                       '  rw:\n'
                       '    host: postgresql\n'
                       '    port: 5432\n'
                       '    user: pg_test_user\n'
                       '    password: pgTestPassword\n'
                       '  ro:\n'
                       '    host: postgresql_ro\n'
                       '    port: false\n'
                       '    user: pg_test_user_ro\n'
                       '    password: pgTestPasswordRo')
        result: ReturnEntity = pg_conf(Path('/conf/pg-negative-test.yaml'))
        os.remove(Path('/conf/pg-negative-test.yaml'))
        if result.error:
            for error in result.errorText.split('|'):
                print(error)
        self.assertFalse(result.error)
        result_entity: PgConf = result.entity
        print(json.dumps(result_entity.to_dict(), indent=4, sort_keys=True))
        self.assertEqual('pg_test_db', result_entity.name)
        self.assertEqual('postgresql', result_entity.rw.host)
        self.assertEqual(5432, result_entity.rw.port)
        self.assertEqual('pg_test_user', result_entity.rw.user)
        self.assertEqual('pgTestPassword', result_entity.rw.password)
        self.assertEqual('postgresql_ro', result_entity.ro.host)
        self.assertEqual(5432, result_entity.ro.port)
        self.assertEqual('pg_test_user_ro', result_entity.ro.user)
        self.assertEqual('pgTestPasswordRo', result_entity.ro.password)
