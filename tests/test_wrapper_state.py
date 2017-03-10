from __future__ import absolute_import, unicode_literals

import unittest

from draftjs_exporter.dom import DOM
from draftjs_exporter.wrapper_state import BlockException, Options, WrapperState


class TestOptions(unittest.TestCase):
    def test_str(self):
        self.assertEqual(str(Options('li')), '<Options li None None None>')

    def test_eq(self):
        self.assertEqual(Options('li'), Options('li'))

    def test_not_eq(self):
        self.assertNotEqual(Options('li'), Options('p'))

    def test_for_block_full(self):
        block_map = {'unordered-list-item': 'li'}
        self.assertEqual(Options.for_block(block_map, 'unordered-list-item'), Options('li'))

    def test_for_block_half(self):
        block_map = {'unordered-list-item': 'li'}
        self.assertEqual(Options.for_block(block_map, 'unordered-list-item'), Options('li'))

    def test_for_block_simplest(self):
        block_map = {'unordered-list-item': 'li'}
        self.assertEqual(Options.for_block(block_map, 'unordered-list-item'), Options('li'))

    def test_for_block_raises_missing_type(self):
        block_map = {'header-one': 'h1'}
        with self.assertRaises(BlockException):
            Options.for_block(block_map, 'header-two')

    def test_for_block_raises_missing_element(self):
        block_map = {'header-one': {}}
        with self.assertRaises(BlockException):
            Options.for_block(block_map, 'header-one')

    def test_for_block_raises_wrong_format(self):
        block_map = {'header-one': []}
        with self.assertRaises(BlockException):
            Options.for_block(block_map, 'header-one')


class TestWrapperState(unittest.TestCase):
    def setUp(self):
        self.wrapper_state = WrapperState({
            'header-one': 'h1',
            'unstyled': 'div',
        })

    def test_init(self):
        self.assertIsInstance(self.wrapper_state, WrapperState)

    def test_element_for_text(self):
        self.assertEqual(DOM.get_text_content(self.wrapper_state.element_for({
            'key': '5s7g9',
            'text': 'Header',
            'type': 'header-one',
            'depth': 0,
            'inlineStyleRanges': [],
            'entityRanges': []
        })), None)

    def test_element_for_tag(self):
        self.assertEqual(DOM.get_tag_name(self.wrapper_state.element_for({
            'key': '5s7g9',
            'text': 'Header',
            'type': 'header-one',
            'depth': 0,
            'inlineStyleRanges': [],
            'entityRanges': []
        })), 'h1')

    def test_to_string_empty(self):
        self.assertEqual(self.wrapper_state.to_string(), '')

    def test_to_string_elts(self):
        self.wrapper_state.element_for({
            'key': '5s7g9',
            'text': 'Header',
            'type': 'header-one',
            'depth': 0,
            'inlineStyleRanges': [],
            'entityRanges': []
        })

        self.assertEqual(self.wrapper_state.to_string(), '<h1></h1>')

    def test_str_empty(self):
        self.assertEqual(str(self.wrapper_state), '<WrapperState: >')

    def test_str_elts(self):
        self.wrapper_state.element_for({
            'key': '5s7g9',
            'text': 'Header',
            'type': 'header-one',
            'depth': 0,
            'inlineStyleRanges': [],
            'entityRanges': []
        })

        self.assertEqual(str(self.wrapper_state), '<WrapperState: <h1></h1>>')
