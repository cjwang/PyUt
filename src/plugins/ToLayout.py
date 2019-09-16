
# from StringIO import StringIO
from io import StringIO

# from PyutToPlugin import PyutToPlugin
from PyutClass import PyutClass
from OglClass import OglClass
from PyutMethod import PyutMethod
from PyutParam import PyutParam
from PyutField import PyutField
from PyutConsts import *
# from wxPython.wx import *
import wx

from plugins.PyutToPlugin import PyutToPlugin


class ToLayout(PyutToPlugin):
    """
    Python code generation/reverse engineering

    @version $Revision: 1.5 $
    """
    def __init__(self, umlObjects, umlFrame):
        """
        Constructor.

        @param String filename : name of the file to save to
        @param OglObject oglObjects : list of ogl objects
        @param UmlFrame umlFrame : the umlframe of pyut
        @author Laurent Burgbacher <lb@alawa.ch>
        @since 1.0
        """
        PyutToPlugin.__init__(self, umlObjects, umlFrame)
        self._umlFrame = umlFrame

    def getName(self):
        """
        This method returns the name of the plugin.

        @return string
        @since 1.1
        """
        return "Layout plugin (read)"

    def getAuthor(self):
        """
        This method returns the author of the plugin.

        @return string
        @since 1.1
        """
        return "C�dric DUTOIT <dutoitc@hotmail.com>"

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
        return "Layout"

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
        filename = wx.FileSelector(
            "Choose a layout file to import",
            wildcard = "Layout file (*.lay) | *.lay",
            # default_path = self.__ctrl.getCurrentDir(),
            flags = wx.OPEN | wx.FILE_MUST_EXIST | wx.CHANGE_DIR
        )

        f=open(filename, "r")
        lstFile = f.readlines()
        f.close()
        lst=[]
        for el in lstFile:
            spl = el.split(",")
            lst.append(spl)
        print(f"Read {lst}")

        for oglObject in umlObjects:
            for line in lst:
                if line[0] == oglObject.getPyutObject().getName():
                    oglObject.SetPosition(float(line[1]), float(line[2]))
                    oglObject.SetSize(float(line[3]), float(line[4]))
