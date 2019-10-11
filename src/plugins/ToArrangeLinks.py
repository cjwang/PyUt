

from org.pyut.ogl.OglLink import OglLink

from plugins.PyutToPlugin import PyutToPlugin


class ToArrangeLinks(PyutToPlugin):
    """
    Plugin to arrange all links
    Python code generation/reverse engineering

    @version $Revision: 1.2 $
    """
    def __init__(self, umlObjects, umlFrame):
        """
        Constructor.

        @param umlObjects  : list of ogl objects
        @param umlFrame : the umlframe of pyut
        """
        PyutToPlugin.__init__(self, umlObjects, umlFrame)
        self._umlFrame = umlFrame

    def getName(self):
        """
        This method returns the name of the plugin.

        @return string
        @since 1.1
        """
        return "Arrange links"

    def getAuthor(self):
        """
        This method returns the author of the plugin.

        @return string
        @since 1.1
        """
        return "C�dric DUTOIT <dutoitc@shimbawa.ch>"

    def getVersion(self):
        """
        This method returns the version of the plugin.

        @return string
        @since 1.1
        """
        return "1.0"

    def getMenuTitle(self):
        """
        Return a menu title string

        @return string
        @author Laurent Burgbacher <lb@alawa.ch>
        @since 1.0
        """
        # Return the menu title as it must be displayed
        return "Arrange links"

    def setOptions(self):
        """
        Prepare the import.
        This can be used to ask some questions to the user.

        @return Boolean : if False, the import will be cancelled.
        @author Laurent Burgbacher <lb@alawa.ch>
        @since 1.0
        """
        return True

    def doAction(self, umlObjects, selectedObjects, umlFrame):
        """
        Do the tool's action

        @param OglObject [] umlObjects : list of the uml objects of the diagram
        @param OglObject [] selectedObjects : list of the selected objects
        @param UmlFrame umlFrame : the frame of the diagram
        @since 1.0
        @author C.Dutoit <dutoitc@hotmail.com>
        """
        for oglObject in umlObjects:
            if isinstance(oglObject, OglLink):
                print("1")
                oglObject.optimizeLine()
            else:
                print("0")
