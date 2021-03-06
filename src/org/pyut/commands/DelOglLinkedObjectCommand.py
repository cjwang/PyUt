
from org.pyut.commands.DelOglObjectCommand import DelOglObjectCommand

from org.pyut.history.HistoryUtils import getTokenValue


class DelOglLinkedObjectCommand(DelOglObjectCommand):
    """
    @author P. Dabrowski <przemek.dabrowski@destroy-display.com> (15.11.2005)
    This class is a part of the history system of PyUt.
    It execute/undo/redo the deletion of an OglLinkedObject(it doesn't exist
    but it represent every OglObject that has a pyutLinkedObject as pyutObject
    """

    def __init__(self, shape=None):
        """
        Constructor.
        @param shape  : object that is destroyed
        """

        super().__init__(shape)

    def serialize(self):
        """
        Serialize the data needed by the destroyed OglLinkedObject.
        @return a string representation of the data needed by the command.
        """

        # serialize the data common to all OglObjects
        serialShape = DelOglObjectCommand.serialize(self)

        fileName = self._shape.getPyutObject().getFilename()
        serialShape += getTokenValue("fileName", fileName)

        return serialShape

    def deserialize(self, serializedData: str):
        """
        deserialize the data needed by the destroyed OglLinkedObject.

        Args:
            serializedData:

        Returns:  deserialized data needed by the command.

        """
        # deserialize the data common to all OglObjects
        DelOglObjectCommand.deserialize(self, serializedData)

        fileName = getTokenValue("fileName", serializedData)
        self._shape.getPyutObject().setFilename(fileName)
