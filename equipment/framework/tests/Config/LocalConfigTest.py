import unittest
from os import sep
from uuid import uuid4
from equipment.framework.tests.TestCase import TestCase
from equipment.framework.Config.AbstractConfig import AbstractConfig
from equipment.framework.Config.LocalConfig import LocalConfig


class LocalConfigTest(TestCase):
    def setUp(self):
        super().setUp()
        self.app.config.override(LocalConfig(
            self.app.environment(),
            f'tests{sep}_stubs{sep}config'
        ))

    def test_extends_from_abstract_config(self):
        self.assertTrue(
            isinstance(self.app.config(), AbstractConfig)
        )

    def test_it_reads_local_config_files(self):
        content = self.faker.name()
        self.assertIsInstance(content, str)

        self.app.config().set('APP', 'name', content)
        result = self.app.config().get('APP', 'name')

        self.assertEqual(result, content)

    def test_it_reads_environment_variables(self):
        content = 'BAR'
        self.app.environment().set('FOO', content)
        self.app.config().set('APP', 'name', 'env:FOO')

        result = self.app.config().get('APP', 'name')

        self.assertEqual(result, content)

    def test_it_reads_correct_types(self):
        section = str(uuid4())
        self.app.config().load()

        # pylint: disable=consider-using-f-string
        self.app.config().config.read_string('''
        [{section}]
        should_be_none = None
        should_be_int = 123
        should_be_string = asdf
        should_be_list = ['a','b','c']
        should_be_dict = {{'a': 123}}
        should_be_tuple = ('a', 'b', 'c')
        should_be_bool = True
        '''.format(section=section))

        self.assertEqual(
            type(None),
            type(self.app.config().get(section, 'should_be_none'))
        )

        self.assertEqual(
            type(123),
            type(self.app.config().get(section, 'should_be_int'))
        )

        self.assertEqual(
            type('asdf'),
            type(self.app.config().get(section, 'should_be_string'))
        )

        self.assertEqual(
            type(['a', 'b', 'c']),
            type(self.app.config().get(section, 'should_be_list'))
        )

        self.assertEqual(
            type({'a': 123}),
            type(self.app.config().get(section, 'should_be_dict'))
        )

        self.assertEqual(
            type(('a', 'b', 'c')),
            type(self.app.config().get(section, 'should_be_tuple'))
        )

        self.assertEqual(
            type(True),
            type(self.app.config().get(section, 'should_be_bool'))
        )


if __name__ == '__main__':
    unittest.main()
