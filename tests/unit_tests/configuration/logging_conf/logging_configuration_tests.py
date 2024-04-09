import os
import json

from pathlib import Path

from unittest import IsolatedAsyncioTestCase

from helpers.configuration.logging_conf import log_conf
from helpers.work_classes import ReturnEntity
from helpers.work_classes import LogLevel, LogOutput, LogFormat


class LogConfTests(IsolatedAsyncioTestCase):
    """
    Class describing tests for helpers.configuration.logging_conf.log_conf
    """

    async def asyncTearDown(self):
        os.environ.pop('LOG_LVL', None)
        os.environ.pop('LOG_FMT', None)
        os.environ.pop('LOG_OUT', None)
        os.environ.pop('LOG_PTH', None)

    async def test_read_from_file(self):
        with open(Path('/conf/example-test.yaml'), 'w') as file:
            file.write('logging:\n  level: critical\n  format: json\n  output: file\n  path: /log/test.log')
        result: ReturnEntity = log_conf(Path('/conf/example-test.yaml'))
        if result.error:
            print(result.errorText)
        self.assertFalse(result.error)
        print(json.dumps(result.entity.to_dict(), indent=4, sort_keys=True))
        self.assertEqual(LogLevel.critical, result.entity.level)
        self.assertEqual(LogFormat.json, result.entity.format)
        self.assertEqual(LogOutput.file, result.entity.output)
        self.assertEqual('/log/test.log', str(result.entity.path))

    async def test_default_values(self):
        result: ReturnEntity = log_conf(Path('/conf/app-conf.yaml'))
        if result.error:
            print(result.errorText)
        self.assertTrue(result.error)
        self.assertEqual('Configuration file /conf/app-conf.yaml is missing', result.errorText)
        print(json.dumps(result.entity.to_dict(), indent=4, sort_keys=True))
        self.assertEqual(LogLevel.info, result.entity.level)
        self.assertEqual(LogFormat.string, result.entity.format)
        self.assertEqual(LogOutput.stream, result.entity.output)
        self.assertEqual('/log/app.log', str(result.entity.path))

    async def test_env_var(self):
        with open(Path('/conf/example-test.yaml'), 'w') as file:
            file.write('logging:\n  level: critical\n  format: json\n  output: stream')
        os.environ['LOG_LVL'] = 'debug'
        os.environ['LOG_FMT'] = 'string'
        os.environ['LOG_OUT'] = 'file'
        os.environ['LOG_PTH'] = '/log/test-env.log'
        result: ReturnEntity = log_conf(Path('/conf/example-test.yaml'))
        if result.error:
            print(result.errorText)
        self.assertFalse(result.error)
        print(json.dumps(result.entity.to_dict(), indent=4, sort_keys=True))
        self.assertEqual(LogLevel.debug, result.entity.level)
        self.assertEqual(LogFormat.string, result.entity.format)
        self.assertEqual(LogOutput.file, result.entity.output)
        self.assertEqual('/log/test-env.log', str(result.entity.path))

    async def test_level_D(self):
        os.environ['LOG_LVL'] = 'D'
        result: ReturnEntity = log_conf()
        if result.error:
            print(result.errorText)
        self.assertFalse(result.error)
        print(result.entity.level.value)
        self.assertEqual(LogLevel.debug, result.entity.level)

    async def test_level_dbg(self):
        os.environ['LOG_LVL'] = 'dbg'
        result: ReturnEntity = log_conf()
        if result.error:
            print(result.errorText)
        self.assertFalse(result.error)
        print(result.entity.level.value)
        self.assertEqual(LogLevel.debug, result.entity.level)

    async def test_level_DEBUG(self):
        os.environ['LOG_LVL'] = 'DEBUG'
        result: ReturnEntity = log_conf()
        if result.error:
            print(result.errorText)
        self.assertFalse(result.error)
        print(result.entity.level.value)
        self.assertEqual(LogLevel.debug, result.entity.level)

    async def test_level_10(self):
        os.environ['LOG_LVL'] = '10'
        result: ReturnEntity = log_conf()
        if result.error:
            print(result.errorText)
        self.assertFalse(result.error)
        print(result.entity.level.value)
        self.assertEqual(LogLevel.debug, result.entity.level)

    async def test_level_I(self):
        os.environ['LOG_LVL'] = 'I'
        result: ReturnEntity = log_conf()
        if result.error:
            print(result.errorText)
        self.assertFalse(result.error)
        print(result.entity.level.value)
        self.assertEqual(LogLevel.info, result.entity.level)

    async def test_level_inf(self):
        os.environ['LOG_LVL'] = 'inf'
        result: ReturnEntity = log_conf()
        if result.error:
            print(result.errorText)
        self.assertFalse(result.error)
        print(result.entity.level.value)
        self.assertEqual(LogLevel.info, result.entity.level)

    async def test_level_iNFo(self):
        os.environ['LOG_LVL'] = 'iNFo'
        result: ReturnEntity = log_conf()
        if result.error:
            print(result.errorText)
        self.assertFalse(result.error)
        print(result.entity.level.value)
        self.assertEqual(LogLevel.info, result.entity.level)

    async def test_level_20(self):
        os.environ['LOG_LVL'] = '20'
        result: ReturnEntity = log_conf()
        if result.error:
            print(result.errorText)
        self.assertFalse(result.error)
        print(result.entity.level.value)
        self.assertEqual(LogLevel.info, result.entity.level)

    async def test_level_w(self):
        os.environ['LOG_LVL'] = 'w'
        result: ReturnEntity = log_conf()
        if result.error:
            print(result.errorText)
        self.assertFalse(result.error)
        print(result.entity.level.value)
        self.assertEqual(LogLevel.warning, result.entity.level)

    async def test_level_Wrn(self):
        os.environ['LOG_LVL'] = 'Wrn'
        result: ReturnEntity = log_conf()
        if result.error:
            print(result.errorText)
        self.assertFalse(result.error)
        print(result.entity.level.value)
        self.assertEqual(LogLevel.warning, result.entity.level)

    async def test_level_warN(self):
        os.environ['LOG_LVL'] = 'warN'
        result: ReturnEntity = log_conf()
        if result.error:
            print(result.errorText)
        self.assertFalse(result.error)
        print(result.entity.level.value)
        self.assertEqual(LogLevel.warning, result.entity.level)

    async def test_level_warning(self):
        os.environ['LOG_LVL'] = 'warning'
        result: ReturnEntity = log_conf()
        if result.error:
            print(result.errorText)
        self.assertFalse(result.error)
        print(result.entity.level.value)
        self.assertEqual(LogLevel.warning, result.entity.level)

    async def test_level_30(self):
        os.environ['LOG_LVL'] = '30'
        result: ReturnEntity = log_conf()
        if result.error:
            print(result.errorText)
        self.assertFalse(result.error)
        print(result.entity.level.value)
        self.assertEqual(LogLevel.warning, result.entity.level)

    async def test_level_e(self):
        os.environ['LOG_LVL'] = 'e'
        result: ReturnEntity = log_conf()
        if result.error:
            print(result.errorText)
        self.assertFalse(result.error)
        print(result.entity.level.value)
        self.assertEqual(LogLevel.error, result.entity.level)

    async def test_level_err(self):
        os.environ['LOG_LVL'] = 'err'
        result: ReturnEntity = log_conf()
        if result.error:
            print(result.errorText)
        self.assertFalse(result.error)
        print(result.entity.level.value)
        self.assertEqual(LogLevel.error, result.entity.level)

    async def test_level_error(self):
        os.environ['LOG_LVL'] = 'error'
        result: ReturnEntity = log_conf()
        if result.error:
            print(result.errorText)
        self.assertFalse(result.error)
        print(result.entity.level.value)
        self.assertEqual(LogLevel.error, result.entity.level)

    async def test_level_40(self):
        os.environ['LOG_LVL'] = '40'
        result: ReturnEntity = log_conf()
        if result.error:
            print(result.errorText)
        self.assertFalse(result.error)
        print(result.entity.level.value)
        self.assertEqual(LogLevel.error, result.entity.level)

    async def test_level_c(self):
        os.environ['LOG_LVL'] = 'c'
        result: ReturnEntity = log_conf()
        if result.error:
            print(result.errorText)
        self.assertFalse(result.error)
        print(result.entity.level.value)
        self.assertEqual(LogLevel.critical, result.entity.level)

    async def test_level_crt(self):
        os.environ['LOG_LVL'] = 'crt'
        result: ReturnEntity = log_conf()
        if result.error:
            print(result.errorText)
        self.assertFalse(result.error)
        print(result.entity.level.value)
        self.assertEqual(LogLevel.critical, result.entity.level)

    async def test_level_crit(self):
        os.environ['LOG_LVL'] = 'crit'
        result: ReturnEntity = log_conf()
        if result.error:
            print(result.errorText)
        self.assertFalse(result.error)
        print(result.entity.level.value)
        self.assertEqual(LogLevel.critical, result.entity.level)

    async def test_level_critical(self):
        os.environ['LOG_LVL'] = 'critical'
        result: ReturnEntity = log_conf()
        if result.error:
            print(result.errorText)
        self.assertFalse(result.error)
        print(result.entity.level.value)
        self.assertEqual(LogLevel.critical, result.entity.level)

    async def test_level_50(self):
        os.environ['LOG_LVL'] = '50'
        result: ReturnEntity = log_conf()
        if result.error:
            print(result.errorText)
        self.assertFalse(result.error)
        print(result.entity.level.value)
        self.assertEqual(LogLevel.critical, result.entity.level)

    async def test_level_not_in_list(self):
        os.environ['LOG_LVL'] = 'crit506070'
        result: ReturnEntity = log_conf()
        if result.error:
            print(result.errorText)
        self.assertTrue(result.error)
        print(result.entity.level.value)
        self.assertEqual(LogLevel.info, result.entity.level)
        self.assertEqual('The specified logging level is not registered. The default logging level is set: info',
                         result.errorText)

    async def test_format_json(self):
        os.environ['LOG_FMT'] = 'json'
        result: ReturnEntity = log_conf()
        if result.error:
            print(result.errorText)
        self.assertFalse(result.error)
        print(result.entity.format.value)
        self.assertEqual(LogFormat.json, result.entity.format)

    async def test_format_jsN(self):
        os.environ['LOG_FMT'] = 'jsN'
        result: ReturnEntity = log_conf()
        if result.error:
            print(result.errorText)
        self.assertFalse(result.error)
        print(result.entity.format.value)
        self.assertEqual(LogFormat.json, result.entity.format)

    async def test_format_Js(self):
        os.environ['LOG_FMT'] = 'Js'
        result: ReturnEntity = log_conf()
        if result.error:
            print(result.errorText)
        self.assertFalse(result.error)
        print(result.entity.format.value)
        self.assertEqual(LogFormat.json, result.entity.format)

    async def test_format_j(self):
        os.environ['LOG_FMT'] = 'j'
        result: ReturnEntity = log_conf()
        if result.error:
            print(result.errorText)
        self.assertFalse(result.error)
        print(result.entity.format.value)
        self.assertEqual(LogFormat.json, result.entity.format)

    async def test_format_string(self):
        os.environ['LOG_FMT'] = 'string'
        result: ReturnEntity = log_conf()
        if result.error:
            print(result.errorText)
        self.assertFalse(result.error)
        print(result.entity.format.value)
        self.assertEqual(LogFormat.string, result.entity.format)

    async def test_format_str(self):
        os.environ['LOG_FMT'] = 'str'
        result: ReturnEntity = log_conf()
        if result.error:
            print(result.errorText)
        self.assertFalse(result.error)
        print(result.entity.format.value)
        self.assertEqual(LogFormat.string, result.entity.format)

    async def test_format_st(self):
        os.environ['LOG_FMT'] = 'st'
        result: ReturnEntity = log_conf()
        if result.error:
            print(result.errorText)
        self.assertFalse(result.error)
        print(result.entity.format.value)
        self.assertEqual(LogFormat.string, result.entity.format)

    async def test_format_s(self):
        os.environ['LOG_FMT'] = 's'
        result: ReturnEntity = log_conf()
        if result.error:
            print(result.errorText)
        self.assertFalse(result.error)
        print(result.entity.format.value)
        self.assertEqual(LogFormat.string, result.entity.format)

    async def test_format_not_in_list(self):
        os.environ['LOG_FMT'] = 'strjs'
        result: ReturnEntity = log_conf()
        if result.error:
            print(result.errorText)
        self.assertTrue(result.error)
        print(result.entity.format.value)
        self.assertEqual(LogFormat.string, result.entity.format)
        self.assertEqual('The specified logging format is not registered. '
                         'The default logging format is set: string', result.errorText)

    async def test_output_stream(self):
        os.environ['LOG_OUT'] = 'stream'
        result: ReturnEntity = log_conf()
        if result.error:
            print(result.errorText)
        self.assertFalse(result.error)
        print(result.entity.output.value)
        self.assertEqual(LogOutput.stream, result.entity.output)

    async def test_output_strm(self):
        os.environ['LOG_OUT'] = 'strm'
        result: ReturnEntity = log_conf()
        if result.error:
            print(result.errorText)
        self.assertFalse(result.error)
        print(result.entity.output.value)
        self.assertEqual(LogOutput.stream, result.entity.output)

    async def test_output_str(self):
        os.environ['LOG_OUT'] = 'str'
        result: ReturnEntity = log_conf()
        if result.error:
            print(result.errorText)
        self.assertFalse(result.error)
        print(result.entity.output.value)
        self.assertEqual(LogOutput.stream, result.entity.output)

    async def test_output_st(self):
        os.environ['LOG_OUT'] = 'st'
        result: ReturnEntity = log_conf()
        if result.error:
            print(result.errorText)
        self.assertFalse(result.error)
        print(result.entity.output.value)
        self.assertEqual(LogOutput.stream, result.entity.output)

    async def test_output_s(self):
        os.environ['LOG_OUT'] = 's'
        result: ReturnEntity = log_conf()
        if result.error:
            print(result.errorText)
        self.assertFalse(result.error)
        print(result.entity.output.value)
        self.assertEqual(LogOutput.stream, result.entity.output)

    async def test_output_file(self):
        os.environ['LOG_OUT'] = 'file'
        result: ReturnEntity = log_conf()
        if result.error:
            print(result.errorText)
        self.assertFalse(result.error)
        print(result.entity.output.value)
        self.assertEqual(LogOutput.file, result.entity.output)

    async def test_output_fl(self):
        os.environ['LOG_OUT'] = 'fl'
        result: ReturnEntity = log_conf()
        if result.error:
            print(result.errorText)
        self.assertFalse(result.error)
        print(result.entity.output.value)
        self.assertEqual(LogOutput.file, result.entity.output)

    async def test_output_f(self):
        os.environ['LOG_OUT'] = 'f'
        result: ReturnEntity = log_conf()
        if result.error:
            print(result.errorText)
        self.assertFalse(result.error)
        print(result.entity.output.value)
        self.assertEqual(LogOutput.file, result.entity.output)

    async def test_output_not_in_list(self):
        os.environ['LOG_OUT'] = 'flstr'
        result: ReturnEntity = log_conf()
        if result.error:
            print(result.errorText)
        self.assertTrue(result.error)
        print(result.entity.output.value)
        self.assertEqual(LogOutput.stream, result.entity.output)
        self.assertEqual('The specified logging output is not registered. '
                         'The default logging output is set: stream', result.errorText)

    async def test_path_exists(self):
        os.environ['LOG_OUT'] = 'f'
        os.environ['LOG_PTH'] = '/log/tests.log'
        result: ReturnEntity = log_conf()
        if result.error:
            print(result.errorText)
        self.assertFalse(result.error)
        print(str(result.entity.path))
        self.assertEqual(Path('/log/tests.log'), result.entity.path)

    async def test_path_not_exists(self):
        os.environ['LOG_OUT'] = 'f'
        os.environ['LOG_PTH'] = '/log/tests/tests.log'
        result: ReturnEntity = log_conf()
        if result.error:
            print(result.errorText)
        self.assertTrue(result.error)
        print(str(result.entity.path))
        self.assertEqual(Path('/log/app.log'), result.entity.path)
        self.assertEqual('The specified logging path is not exists. The default logging path is set: /log/app.log',
                         result.errorText)
