from itertools import groupby

from .command import Command
from .entity_state import EntityState
from .style_state import StyleState
from .wrapper_state import WrapperState


class HTML():
    def __init__(self, config):
        self.block_map = config.get('block_map', {})
        self.style_map = config.get('style_map', {})
        self.entity_decorators = config.get('entity_decorators', {})

        self.wrapper_state = WrapperState(self.block_map)

    def call(self, content_state):
        entity_map = content_state.get('entityMap', {})

        for block in content_state.get('blocks'):
            element = self.wrapper_state.element_for(block)
            self.block_contents(element, block, entity_map)

        return self.wrapper_state.to_string()

    def block_contents(self, element, block, entity_map):
        style_state = StyleState(self.style_map)
        entity_state = EntityState(element, self.entity_decorators, entity_map)
        for (text, commands) in self.build_command_groups(block):
            for command in commands:
                print command, text
                entity_state.apply(command)
                style_state.apply(command)

            # TODO Use entity_state.
            self.add_node(element, text, style_state)

    def add_node(self, element, text, style_state):
        pass
        # TODO Does not work ATM.
        # if style_state.is_unstyled():
        #     child = etree.SubElement(element, 'textnode')
        #     child.text = text
        # else:
        #     child = etree.SubElement(element, 'span', attrib=style_state.element_attributes())
        #     child.text = text
        # document = element.getroot()
        # node = if state.text?
        # document.create_text_node(text)
        # else
        # document.create_element('span', text, state.element_attributes)
        # end
        # element.add_child(node)

    def build_command_groups(self, block):
        text = block.get('text')
        commands = self.build_commands(block)
        # grouped = build_commands(block).group_by(&:index).sort
        # grouped = sorted(list(groupby(commands, lambda c: c.index)))
        grouped = groupby(commands, lambda c: c.index)
        listed = list(groupby(commands, lambda c: c.index))

        grouped_sliced = []
        i = 0
        # TODO sorting is wrong here. Need a debugger.
        for start_index, commands in grouped:
            next_group = listed[i + 1] if i + 1 < len(listed) else False
            # TODO stop_index should be set depending on the languages' slice. Check this is what we want.
            # stop_index = (next_group && next_group.first || 0) - 1
            # [text.slice(start_index..stop_index), commands]
            stop_index = next_group[0] if next_group else 0

            grouped_sliced.append((text[start_index:stop_index], list(commands)))
            i += 1

        # TODO Debug sorting
        # for text, coms in grouped_sliced:
        #     print text, coms

        return grouped_sliced

    def build_commands(self, block):
        style_commands = self.build_range_commands('inline_style', 'style', block.get('inlineStyleRanges'))
        entity_commands = self.build_range_commands('entity', 'key', block.get('entityRanges'))
        return [
            Command('start_text', 0),
            Command('stop_text', len(block.get('text'))),
        ] + style_commands + entity_commands

    def build_range_commands(self, name, data_key, ranges):
        commands = []
        for r in ranges:
            data = r.get(data_key)
            start = r.get('offset')
            stop = start + r.get('length')
            commands.append(Command('start_%s' % name, start, data))
            commands.append(Command('stop_%s' % name, stop, data))
        return commands