
from typing import List

from logging import Logger
from logging import getLogger

from org.pyut.ogl.OglClass import OglClass
from org.pyut.plugins.orthogonal.TulipMaker import TulipMaker
from org.pyut.ui.UmlFrame import UmlFrame


from org.pyut.plugins.PyutToPlugin import PyutToPlugin


class ToOrthogonalLayout(PyutToPlugin):
    """
    Layout the UML class diagram by changing the links to an orthogonal layout
    """
    def __init__(self, umlObjects: List[OglClass], umlFrame: UmlFrame):
        """

        Args:
            umlObjects:  list of ogl objects
            umlFrame:    A Pyut umlFrame
        """
        super().__init__(umlObjects, umlFrame)

        self.logger: Logger = getLogger(__name__)

    def getName(self):
        """
        Returns: the name of the plugin.
        """
        return "Orthogonal Layout"

    def getAuthor(self):
        """
        Returns:
            The author's name
        """
        return "Humberto A. Sanchez II"

    def getVersion(self):
        """
        Returns:
            The plugin version string
        """
        return "1.0"

    def getMenuTitle(self):
        """
        Returns:
            The menu title for this plugin
        """
        return "Orthogonal Layout"

    def setOptions(self):
        """
        Prepare the import.
        This can be used to ask some questions to the user.

        Returns:
            If False, the import will be cancelled.
        """
        return True

    def doAction(self, umlObjects: List[OglClass], selectedObjects: List[OglClass], umlFrame: UmlFrame):
        """
        Do the tool's action

        Args:
            umlObjects:         list of the uml objects of the diagram
            selectedObjects:    list of the selected objects
            umlFrame:           The diagram frame
        """
        if umlFrame is None:
            self.displayNoUmlFrame()
            return
        if len(umlObjects) == 0:
            self.displayNoUmlObjects()
            return

        self.logger.info(f'Begin Orthogonal algorithm')

        tulipMaker: TulipMaker = TulipMaker()

        tulipMaker.translate(umlObjects)
