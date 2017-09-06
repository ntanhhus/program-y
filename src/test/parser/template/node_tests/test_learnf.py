import xml.etree.ElementTree as ET
import os

from programy.parser.template.nodes.base import TemplateNode
from programy.parser.template.nodes.learn import LearnCategory
from programy.parser.template.nodes.learnf import TemplateLearnfNode
from programy.parser.template.nodes.word import TemplateWordNode
from programy.config.sections.brain.file import BrainFileConfiguration

from test.parser.template.base import TemplateTestsBaseClass

class MockTemplateLearnfNode(TemplateLearnfNode):
    def __init__(self):
        TemplateLearnfNode.__init__(self)

    def resolve_to_string(self, bot, clientid):
        raise Exception("This is an error")

class TemplateLearnfNodeTests(TemplateTestsBaseClass):

    def get_os_specific_filename(self):
        if os.name == 'posix':
            return '/tmp/learnf.aiml'
        elif os.name == 'nt':
            return 'C:\Windows\Temp\leanf.aiml'
        else:
            raise Exception("Unknown OS [%s]"%os.name)
        
    def test_node(self):

        if os.path.exists(self.get_os_specific_filename()):
            os.remove(self.get_os_specific_filename())

        root = TemplateNode()
        self.assertIsNotNone(root)

        learn = TemplateLearnfNode()
        self.assertIsNotNone(learn)
        learn_cat = LearnCategory(ET.fromstring("<pattern>HELLO LEARN</pattern>"),
                                  ET.fromstring("<topic>*</topic>"),
                                  ET.fromstring("<that>*</that>"),
                                  TemplateWordNode("LEARN"))
        learn.append(learn_cat)
        root.append(learn)
        self.assertEqual(1, len(root.children))

        self.bot.brain.configuration.defaults._learn_filename = self.get_os_specific_filename()
        resolved = root.resolve(self.bot, self.clientid)
        self.assertIsNotNone(resolved)
        self.assertEqual("", resolved)

        self.assertTrue(os.path.exists(self.get_os_specific_filename()))

    def test_to_xml(self):
        root = TemplateNode()
        learn = TemplateLearnfNode()
        learn_cat = LearnCategory(ET.fromstring("<pattern>HELLO LEARN</pattern>"),
                                  ET.fromstring("<topic>*</topic>"),
                                  ET.fromstring("<that>*</that>"),
                                  TemplateWordNode("LEARN"))
        learn.append(learn_cat)
        root.append(learn)

        xml = root.xml_tree(self.bot, self.clientid)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual("<template><learnf><category><pattern>HELLO LEARN</pattern><topic>*</topic><that>*</that><template>LEARN</template></category></learnf></template>", xml_str)

    def test_node_exception_handling(self):
        root = TemplateNode()
        node = MockTemplateLearnfNode()
        root.append(node)

        result = root.resolve(self.bot, self.clientid)
        self.assertIsNotNone(result)
        self.assertEquals("", result)