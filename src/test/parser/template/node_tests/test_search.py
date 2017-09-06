import xml.etree.ElementTree as ET

from programy.parser.template.nodes.base import TemplateNode
from programy.parser.template.nodes.word import TemplateWordNode
from programy.parser.template.nodes.search import TemplateSearchNode

from test.parser.template.base import TemplateTestsBaseClass

class MockTemplateSearchNode(TemplateSearchNode):
    def __init__(self):
        TemplateSearchNode.__init__(self)

    def resolve_to_string(self, bot, clientid):
        raise Exception("This is an error")

class TemplateSearchNodeTests(TemplateTestsBaseClass):

    def test_to_string(self):
        root = TemplateSearchNode()
        self.assertIsNotNone(root)
        self.assertEquals("SEARCH", root.to_string())

    def test_to_xml(self):
        root = TemplateNode()
        node = TemplateSearchNode()
        root.append(node)
        node.append(TemplateWordNode("programy"))

        xml = root.xml_tree(self.bot, self.clientid)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual("<template><search>programy</search></template>", xml_str)

    def test_node(self):
        root = TemplateNode()
        node = TemplateSearchNode()
        root.append(node)
        node.append(TemplateWordNode("programy"))

        result = node.resolve(self.bot, self.clientid)
        self.assertIsNotNone(result)
        self.assertEqual("https://www.google.co.uk/search?q=programy", result)

    def test_node_exception_handling(self):
        root = TemplateNode()
        node = MockTemplateSearchNode()
        root.append(node)

        result = root.resolve(self.bot, self.clientid)
        self.assertIsNotNone(result)
        self.assertEquals("", result)