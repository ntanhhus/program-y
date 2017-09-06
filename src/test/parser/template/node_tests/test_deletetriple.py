import xml.etree.ElementTree as ET

from programy.parser.template.nodes.base import TemplateNode
from programy.parser.template.nodes.word import TemplateWordNode
from programy.parser.template.nodes.deletetriple import TemplateDeleteTripleNode
from programy.rdf.entity import RDFEntity

from test.parser.template.base import TemplateTestsBaseClass


class MockTemplateDeleteTripleNode(TemplateDeleteTripleNode):

    def __init__(self, entity=None):
        TemplateDeleteTripleNode.__init__(self, entity)

    def resolve_to_string(self, bot, clientid):
        raise Exception("This is a failure")

class TemplateDeleteTripleNodeTests(TemplateTestsBaseClass):

    def test_to_string(self):
        root = TemplateDeleteTripleNode()
        self.assertIsNotNone(root)
        self.assertEquals("DELETETRIPLE", root.to_string())

    def test_to_xml(self):
        root = TemplateNode()
        node = TemplateDeleteTripleNode(RDFEntity(subject="S", predicate="P", object="O"))
        root.append(node)

        xml = root.xml_tree(self.bot, self.clientid)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual("<template><deletetriple><subj>S</subj><pred>P</pred><obj>O</obj></deletetriple></template>", xml_str)

    def test_node(self):
        root = TemplateNode()
        node = TemplateDeleteTripleNode(RDFEntity(subject="S", predicate="P", object="O"))
        root.append(node)

        result = root.resolve(self.bot, self.clientid)
        self.assertIsNotNone(result)
        self.assertEquals("", result)

    def test_node_exception_handling(self):
        root = TemplateNode()
        node = MockTemplateDeleteTripleNode(RDFEntity(subject="S", predicate="P", object="O"))
        root.append(node)

        result = root.resolve(self.bot, self.clientid)
        self.assertIsNotNone(result)
        self.assertEquals("", result)
