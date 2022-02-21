import docutils.nodes
import docutils.parsers.rst
import docutils.utils
import docutils.frontend
import pkg_resources

from typing import Dict


def parse_rst(text: str) -> docutils.nodes.document:
    """Parse RST file.

    Args:
        text (str): RST file as string.

    Returns:
        docutils.nodes.document: Parsed document.
    """
    parser = docutils.parsers.rst.Parser()
    components = (docutils.parsers.rst.Parser,)
    settings = docutils.frontend.OptionParser(components=components).get_default_values()
    document = docutils.utils.new_document("<rst-doc>", settings=settings)
    parser.parse(text, document)
    return document


class MachineAttributesVisitor(docutils.nodes.NodeVisitor):
    def __init__(self, doc: docutils.nodes.document) -> None:
        """Init Reader to parse RST files for machine readable attributes.

        Args:
            doc (docutils.nodes.document): Document to parse through.
        """
        super().__init__(doc)
        self.tables = 0
        self._machine_readable_attributes = {}

    def visit_table(self, node: docutils.nodes.table) -> None:
        """Called for table nodes."""
        self.tables += 1

    def visit_row(self, node: docutils.nodes.tbody) -> None:
        """Called for row nodes."""
        if (
            self.tables > 1
            or len(node.children) < 2
            or len(node.children[0].children) < 1
            or len(node.children[1].children) < 1
        ):
            return

        self._machine_readable_attributes[str(node.children[0][0][0])] = str(node.children[1][0][0])

    def unknown_visit(self, node: docutils.nodes.Node) -> None:
        """Called for other nodes."""
        pass

    def machine_readable_attributes(self) -> Dict[str, str]:
        """Machine readable summary of attributes.

        Returns:
            Dict[str, str]: Parsed summary.
        """
        return self._machine_readable_attributes


def parse_readme(name: str) -> Dict[str, str]:
    """Parse readme in the current directory and extract attributes.

    Args:
        name (str): path to dataset directory.

    Returns:
        _type_: Machine readable summary of attributes.
    """
    stream = pkg_resources.resource_stream(name, "README.rst")
    doc = parse_rst(stream.read().decode("utf-8"))
    visitor = MachineAttributesVisitor(doc)
    doc.walk(visitor)

    return visitor.machine_readable_attributes()
