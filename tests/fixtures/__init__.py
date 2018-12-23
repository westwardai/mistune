import os
import re

ROOT = os.path.join(os.path.dirname(__file__))

EXAMPLE_PATTERN = re.compile(
    r'^`{32} example\n([\s\S]*?)'
    r'^\.\n([\s\S]*?)'
    r'^`{32}$|^#{1,6} *(.*)$',
    flags=re.M
)


def load_cases(TestClass, assert_method, filename, prefix=None):
    def test_case(self):
        assert_method(self, text, html)

    for n, text, html in load_examples(filename, prefix):
        name = 'test_{}'.format(n)
        setattr(TestClass, name, test_case)


def load_examples(filename, prefix=None):
    with open(os.path.join(ROOT, filename), 'rb') as f:
        content = f.read()
        text = content.decode('utf-8')

    return parse_examples(text, prefix)


def parse_examples(text, prefix=None):
    data = EXAMPLE_PATTERN.findall(text)

    section = None
    count = 0
    for md, html, title in data:
        if title:
            count = 0
            section = title.lower().replace(' ', '_')

        if prefix and not section.startswith(prefix):
            continue

        if md and html:
            count += 1
            n = '%s_%02d' % (section, count)
            md = md.replace(u'\u2192', '\t')
            html = html.replace(u'\u2192', '\t')
            yield n, md, html
