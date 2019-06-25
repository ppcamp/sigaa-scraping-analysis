
# ==============================================================
# Obsolete class used to generate xml's files.
# ==============================================================

class BasicXml(object):
    """
    Class used to create a basic parsed XML file.
    This class creates a string that contains the file
    with special chars '[\t\n]', in anoter words,
    a parsed document
    """

    __out = '<?xml version="1.0" encoding="UTF-8"?>\n'
    __stack = []

    def _indent(self):
        """ Used to parse tags"""
        return '\t'*len(self.__stack)

    def create_tag(self, tagname, value):
        """
        Create a new tag

        Parameters
        ----------
        tagname: string
            Name desired for xml's tags.
        value: string
            Value to be placed inside,an empty value '',
            means that will have a break

        Example
        -------
        >> create_tag('html','Test') # <html>test
        >> create_tag('html','')
        >> create_tag('data','test') # <html>\n\t<data>test
        """
        self.__out += self._indent() + '<{}>'.format(tagname)
        self.__stack.append(tagname)

        if value == '':
            self.__out += '\n'
        else:
            self.__out += value
            self.end_tag()

    def end_tag(self):
        """
        Pop's out from stack, and close last tag

        Example
        -------
        >> end_tag() # </html> e.g.
        """
        tagname = self.__stack.pop()
        if self.__out[-1] == '\n':
            self.__out += self._indent()
        self.__out += '</{}>\n'.format(tagname)

    def __init__(self):
        """
        Ctr for this class, it clears the env variables when called
        """
        self.clear()

    def getXml(self):
        """
        Get XML string

        Returns
        -------
        result: string
            Returns the string containing the xml.

        Example
        -------
        >> getXml() # <html></html>
        """
        return self.__out

    def clear(self):
        """
        Clear environment variables

        Example
        -------
        >> clear() # reset default xml code to <?xml ...>
        """
        self.__out = '<?xml version="1.0" encoding="UTF-8"?>\n'
        self.__stack.clear()

    def toFile(self, name):
        """
        Create XML file. You must pass a name containing path to file.

        Example
        -------
        >> toFile('/home/user/tes.xml') # generate file 'tes.xml'
        """

        f = open(name, 'w', encoding='utf-8')

        if not f.closed:
            f.write(self.getXml())
            f.close()
            return True
        else:
            return False
