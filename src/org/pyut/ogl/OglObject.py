
from logging import Logger
from logging import getLogger

from wx import MouseEvent
from wx import Point
from wx import Font
from wx import FONTFAMILY_SWISS
from wx import FONTSTYLE_NORMAL
from wx import FONTWEIGHT_NORMAL

from org.pyut.miniogl.RectangleShape import RectangleShape
from org.pyut.miniogl.ShapeEventHandler import ShapeEventHandler

from org.pyut.PyutUtils import PyutUtils

from org.pyut.model.PyutObject import PyutObject

from org.pyut.preferences.PyutPreferences import PyutPreferences

DEFAULT_FONT_SIZE = 10


class OglObject(RectangleShape, ShapeEventHandler):
    """
    This is the base class for new OGL objects.
    Every new OGL class must inherit this class and redefine methods if
    necessary. OGL Objects are automatically a RectangleShape for
    global link management.
    """
    def __init__(self, pyutObject=None, width: float = 0, height: float = 0):
        """

        Args:
            pyutObject: Associated PyutObject
            width:      Initial width
            height:     Initial height
        """
        self._pyutObject = pyutObject
        RectangleShape.__init__(self, 0, 0, width, height)

        self.logger: Logger = getLogger(__name__)

        # Default font
        self._defaultFont: Font            = Font(DEFAULT_FONT_SIZE, FONTFAMILY_SWISS, FONTSTYLE_NORMAL, FONTWEIGHT_NORMAL)
        self._prefs:       PyutPreferences = PyutPreferences()

        self._oglLinks = []     # Connected links
        self._modifyCommand = None

    def setPyutObject(self, pyutObject: PyutObject):
        """
        Set the associated pyut object.

        @param PyutObject pyutObject : Associated PyutObject
        """
        self._pyutObject = pyutObject

    def getPyutObject(self) -> PyutObject:
        """
        Return the associated pyut object.

        @return PyutObject : Associated PyutObject
        """
        return self._pyutObject

    @property
    def pyutObject(self):
        return self._pyutObject

    @pyutObject.setter
    def pyutObject(self, pyutObject):
        self._pyutObject = pyutObject

    def addLink(self, link):
        """
        Add a link to an ogl object.

        @param OglLink link : the link to add
        @since 1.0
        @author Philippe Waelti <pwaelti@eivd.ch>
        """
        self._oglLinks.append(link)

    def getLinks(self):
        """
        Return the links.

        @return OglLink[] : Links connected to object
        @since 1.0
        @author Philippe Waelti <pwaelti@eivd.ch>
        """
        return self._oglLinks

    def OnLeftDown(self, event: MouseEvent):
        """
        Handle event on left click.

        Args:
            event:
        """
        self.logger.debug(f'OnLeftDown - event - {event}')

        from org.pyut.general.Mediator import getMediator   # avoid circular import

        med = getMediator()
        if med.actionWaiting():
            position: Point = event.GetPosition()
            med.shapeSelected(self, position)
            return
        event.Skip()

    def OnLeftUp(self, event: MouseEvent):
        """
        Implement this method so we can snap Ogl objects

        Args:
            event:  the mouse event
        """
        gridInterval: int = self._prefs.backgroundGridInterval
        x, y = self.GetPosition()
        if self._prefs.snapToGrid is True:
            snappedX, snappedY = PyutUtils.snapCoordinatesToGrid(x=x, y=y, gridInterval=gridInterval)
            self.SetPosition(snappedX, snappedY)
        else:
            self.SetPosition(x, y)

    def autoResize(self):
        """
        Find the right size to see all the content, and resize self.

        @since 1.0
        @author Philippe Waelti <pwaelti@eivd.ch>
        """
        pass

    def SetPosition(self, x, y):
        """
        Define new position for the object

        Args:
            x:  The new abscissa
            y:  The new ordinate
        """
        from org.pyut.general import Mediator
        fileHandling = Mediator.getMediator().getFileHandling()
        if fileHandling is not None:
            fileHandling.setModified(True)
        RectangleShape.SetPosition(self, x, y)

    def SetSelected(self, state=True):

        from org.pyut.general.Mediator import getMediator       # avoid circular import
        from org.pyut.general.Mediator import ACTION_ZOOM_OUT   # avoid circular import

        if getMediator().getCurrentAction() != ACTION_ZOOM_OUT:
            RectangleShape.SetSelected(self, state)
