from rest_framework_xml.renderers import XMLRenderer
from django.utils.xmlutils import SimplerXMLGenerator
from django.utils.six.moves import StringIO


class OEmbedXMLRenderer(XMLRenderer):
    """
    Renderer which serializes to XML.
    """

    media_type = 'application/xml'
    format = 'xml'
    charset = 'utf-8'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        """
        Renders `data` into serialized XML.
        """
        if data is None:
            return ''

        stream = StringIO()

        xml = SimplerXMLGenerator(stream, self.charset)
        xml.startDocument()
        xml.startElement("oembed", {})

        self._to_xml(xml, data)

        xml.endElement("oembed")
        xml.endDocument()
        return stream.getvalue()