

from logging import Logger
from logging import getLogger

from xml.dom.minidom import parse
from xml.dom.minidom import Document


from io import StringIO

from wx import Dialog
from wx import Gauge
from wx import ICON_INFORMATION
from wx import Point
from wx import RESIZE_BORDER
from wx import STAY_ON_TOP
from wx import Size

from PyutActor import PyutActor
from PyutClass import PyutClass
from PyutConsts import diagramTypeFromString
from PyutField import PyutField
from PyutLink import PyutLink
from PyutMethod import PyutMethod
from PyutNote import PyutNote

from MiniOgl import ControlPoint

from OglLinkFactory import getOglLinkFactory
from OglActor import OglActor
from OglAssociation import CENTER
from OglAssociation import DEST_CARD
from OglAssociation import OglAssociation
from OglAssociation import SRC_CARD

from OglClass import OglClass
from OglLink import OglLink
from OglNote import OglNote
from OglSDInstance import OglSDInstance
from OglSDMessage import OglSDMessage
from OglUseCase import OglUseCase

from PyutStereotype import getPyutStereotype
from pyutUtils import displayError
from PyutConsts import diagramTypeAsString
from PyutParam import PyutParam
from PyutSDInstance import PyutSDInstance
from PyutSDMessage import PyutSDMessage
from PyutUseCase import PyutUseCase

from mediator import getMediator
from globals import _


def secure_int(x):
    try:
        if x is not None:
            return int(x)
        else:
            return 0
    finally:
        return 0


def secure_bool(x):
    try:
        if x is not None:
            if x in [True, "True", "true", 1, "1"]:
                return True
    except:
        pass
    return False


class IDFactory:
    nextID = 1

    def __init__(self):
        self._dicID = {}

    def getID(self, aclass):
        # print "getID : ", self._dicID
        # print "klass:", aclass
        # print type(aclass)
        if aclass in self._dicID:
            return self._dicID[aclass]
        else:
            id = IDFactory.nextID
            self._dicID[aclass] = id
            IDFactory.nextID+=1
            return id


class PyutXml:
    """
    Class for saving and loading a PyUT UML diagram in XML.
    This class offers two main methods that are save() and load().
    Using the dom XML model, you can, with the saving method, get the
    diagram corresponding XML view. For loading, you have to parse
    the file and indicate the UML frame on which you want to draw
    (See `UmlFrame`).

    Sample use::

        # Write
        pyutXml = PyutXml()
        text = pyutXml.save(oglObjects)
        file.write(text)

        # Read
        dom = parse(StringIO(file.read()))
        pyutXml = PyutXml()
        myXml.open(dom, umlFrame)

    Changelog in PyutXmlV8 :
    - Merged PyutXmlV 7, 6, 5, 4, 3 in PyutXml
    - Set classes ID at save-time and load-time

    :version: $Revision: 1.11 $
    :author: C.Dutoit
    :contact: dutoitc@hotmail.com
    """
    def __init__(self):
        """
        Constructor
        @author C.Dutoit
        """
        self.logger: Logger = getLogger(__name__)

        self._this_version = 8
        self._idFactory = IDFactory()

    def _PyutSDInstance2xml(self, pyutSDInstance, xmlDoc):
        """
        Exporting an PyutSDInstance to an miniDom Element.

        @param PyutMethod pyutSDInstance : Class to save
        @param xmlDoc : xml document
        @return Element : XML Node
        @author Deve Roux
        @modified C.Dutoit/20021121 added display properties
        """
        root = xmlDoc.createElement('SDInstance')
        eltId = self._idFactory.getID(pyutSDInstance)

        root.setAttribute('id',           str(eltId))
        root.setAttribute('instanceName', pyutSDInstance.getInstanceName())
        root.setAttribute('lifeLineLength', str(pyutSDInstance.getInstanceLifeLineLength()))
        return root

    def _OglSDInstance2xml(self, oglSDInstance, xmlDoc):
        """
        Exporting an OglSDInstance to a miniDom Element.

        @param OglSDInstance oglSDInstance : Instance to save
        @param xmlDoc : xml document
        @return Element : XML Node
        @author C.Dutoit
        """
        root = xmlDoc.createElement('GraphicSDInstance')

        # Append OGL object base (size and pos)
        self._appendOglBase(oglSDInstance, root)

        # adding the data layer object
        root.appendChild(self._PyutSDInstance2xml(oglSDInstance.getPyutObject(), xmlDoc))

        return root

    def _PyutSDMessage2xml(self, pyutSDMessage, xmlDoc):
        """
        Exporting an PyutSDMessage to an miniDom Element.

        @param PyutMethod pyutSDMessage : SDMessage to save
        @param xmlDoc : xml document
        @return Element : XML Node
        @author C.Dutoit
        """
        root = xmlDoc.createElement('SDMessage')

        # ID
        eltId = self._idFactory.getID(pyutSDMessage)
        root.setAttribute('id', str(eltId))

        # message
        root.setAttribute('message', pyutSDMessage.getMessage())

        # time
        idSrc = self._idFactory.getID(pyutSDMessage.getSource())
        idDst = self._idFactory.getID(pyutSDMessage.getDest())
        root.setAttribute('srcTime', str(pyutSDMessage.getSrcTime()))
        root.setAttribute('dstTime', str(pyutSDMessage.getDstTime()))
        root.setAttribute('srcID', str(idSrc))
        root.setAttribute('dstID', str(idDst))

        return root

    def _OglSDMessage2xml(self, oglSDMessage, xmlDoc):
        """
        Exporting an OglSDMessage to an miniDom Element.

        @param oglSDMessage : Message to save
        @param xmlDoc
        @return Element : XML Node
        @author C.Dutoit
        """
        root = xmlDoc.createElement('GraphicSDMessage')

        # adding the data layer object
        root.appendChild(self._PyutSDMessage2xml(oglSDMessage.getPyutObject(), xmlDoc))

        return root

    def _PyutField2xml(self, pyutField, xmlDoc):
        """
        Exporting a PyutField to an miniDom Element

        @param PyutField pyutField : Field to save
        @param xmlDoc Document : xml document
        @return Element : XML Node
        @author Deve Roux <droux@eivd.ch>
        """
        root = xmlDoc.createElement('Field')

        # adding the parent XML
        # pyutField is a param
        root.appendChild(self._PyutParam2xml(pyutField, xmlDoc))

        # field visibility
        root.setAttribute('visibility', str(pyutField.getVisibility()))

        return root

    def _PyutParam2xml(self, pyutParam, xmlDoc):
        """
        Exporting a PyutParam to an miniDom Element.

        @param pyutParam : Parameters to save
        @param xmlDoc  : xml document
        @return Element : XML Node
        @author Deve Roux <droux@eivd.ch>
        """
        root = xmlDoc.createElement('Param')

        # param name
        root.setAttribute('name', pyutParam.getName())

        # param type
        root.setAttribute('type', str(pyutParam.getType()))

        # param defaulf value
        defaultValue = pyutParam.getDefaultValue()
        if defaultValue is not None:
            root.setAttribute('defaultValue', defaultValue)

        return root

    def _PyutLink2xml(self, pyutLink, xmlDoc):
        """
        Exporting an PyutLink to a miniDom Element.

        @param PyutLink pyutLink : Link to save
        @param xmlDoc : xml document
        @return Element : XML Node
        @author Deve Roux <droux@eivd.ch>
        """

        root = xmlDoc.createElement('Link')
        # link name
        root.setAttribute('name', pyutLink.getName() )

        # link type
        root.setAttribute('type', str(pyutLink.getType()))

        # link cardinality source
        root.setAttribute('cardSrc', pyutLink.getSrcCard())

        # link cardinality destination
        root.setAttribute('cardDestination', pyutLink.getDestCard())

        # link bidir
        root.setAttribute('bidir', str(pyutLink.getBidir()))

        # link source
        srcLinkId = self._idFactory.getID(pyutLink.getSource())
        root.setAttribute('sourceId', str(srcLinkId))

        # link destination
        destLinkId = self._idFactory.getID(pyutLink.getDestination())
        root.setAttribute('destId', str(destLinkId))

        return root

    def _PyutMethod2xml(self, pyutMethod, xmlDoc):
        """
        Exporting an PyutMethod to an miniDom Element.

        @param PyutMethod pyutMethod : Method to save
        @param xmlDoc : xml document
        @return Element : XML Node
        @author Deve Roux <droux@eivd.ch>
        """
        root = xmlDoc.createElement('Method')

        # method name
        root.setAttribute('name', pyutMethod.getName() )

        # method visibility
        visibility = pyutMethod.getVisibility()
        if visibility is not None:
            root.setAttribute('visibility', str(visibility.getVisibility()))

        # for all modifiers
        for modifier in pyutMethod.getModifiers():
            xmlModifier = xmlDoc.createElement('Modifier')
            xmlModifier.setAttribute('name', modifier.getName())
            root.appendChild(xmlModifier)

        # method return type
        returnType = pyutMethod.getReturns()
        if returnType is not None:
            xmlReturnType = xmlDoc.createElement('Return')
            xmlReturnType.setAttribute('type', str(returnType))
            root.appendChild(xmlReturnType)

        # method params
        for param in pyutMethod.getParams() :
            root.appendChild(self._PyutParam2xml(param, xmlDoc))

        return root

    def _PyutClass2xml(self, pyutClass, xmlDoc):
        """
        Exporting an PyutClass to an miniDom Element.

        @param PyutMethod pyutClass : Class to save

        @param xmlDoc : xml document

        @return Element : XML Node

        @author Deve Roux <droux@eivd.ch>
        @modified C.Dutoit/20021121 added display properties
        """
        root = xmlDoc.createElement('Class')

        # ID
        classId = self._idFactory.getID(pyutClass)
        root.setAttribute('id', str(classId))

        # class name
        root.setAttribute('name', pyutClass.getName())

        # classs stereotype
        stereotype = pyutClass.getStereotype()
        if stereotype is not None:
            root.setAttribute('stereotype', stereotype.getStereotype())

        # description (pwaelti@eivd.ch)
        root.setAttribute('description', pyutClass.getDescription())

        # filename (lb@alawa.ch)
        root.setAttribute('filename', pyutClass.getFilename())

        # display properties (cd)
        root.setAttribute('showMethods', str(pyutClass.getShowMethods()))
        root.setAttribute('showFields',  str(pyutClass.getShowFields()))
        root.setAttribute('showStereotype', str(pyutClass.getShowStereotype()))

        # methods
        for method in pyutClass.getMethods():
            root.appendChild(self._PyutMethod2xml(method, xmlDoc))

        # fields
        for field in pyutClass.getFields():
            root.appendChild(self._PyutField2xml(field, xmlDoc))

        return root

    def _PyutNote2xml(self, pyutNote, xmlDoc):
        """
        Exporting an PyutNote to an miniDom Element.

        @param pyutNote : Note to convert
        @param xmlDoc : xml document
        @return Element          : New miniDom element
        @author Philippe Waelti
        @modified C.Dutoit 2002-12-26, added multiline support
        """

        root = xmlDoc.createElement('Note')

        # ID
        noteId = self._idFactory.getID(pyutNote)
        root.setAttribute('id', str(noteId))

        # Note
        name = pyutNote.getName()
        name = name.replace('\n', "\\\\\\\\")
        root.setAttribute('name', name)

        # filename (added by LB)
        root.setAttribute('filename', pyutNote.getFilename())

        return root

    def _PyutActor2xml(self, pyutActor, xmlDoc):
        """
        Exporting an PyutActor to an miniDom Element.

        @param PyutNote pyutActor : Note to convert
        @param xmlDoc : xml document
        @return Element : New miniDom element
        @author Philippe Waelti <pwaelti@eivd.ch>
        """

        root = xmlDoc.createElement('Actor')

        # ID
        id = self._idFactory.getID(pyutActor)
        root.setAttribute('id', str(id))

        # Note
        root.setAttribute('name', pyutActor.getName())

        # filename (lb@alawa.ch)
        root.setAttribute('filename', pyutActor.getFilename())

        return root

    def _PyutUseCase2xml(self, pyutUseCase, xmlDoc):
        """
        Exporting an PyutUseCase to an miniDom Element.

        @param PyutNote pyutUseCase : Note to convert
        @param xmlDoc Document : xml document
        @return Element : New miniDom element
        @author Philippe Waelti <pwaelti@eivd.ch>
        """
        root = xmlDoc.createElement('UseCase')

        # ID
        id = self._idFactory.getID(pyutUseCase)
        root.setAttribute('id', str(id))

        # Note
        root.setAttribute('name', pyutUseCase.getName())

        # filename (lb@alawa.ch)
        root.setAttribute('filename', pyutUseCase.getFilename())

        return root

    def _appendOglBase(self, oglObject, root):
        """
        Saves the position and size of the OGL object in XML node.

        @param OglObject oglObject : OGL Object
        @param Element root : XML node to write
        @author Philippe Waelti <pwaelti@eivd.ch>
        """

        # Saving size
        w, h = oglObject.GetModel().GetSize()
        root.setAttribute('width', str(float(w)))
        root.setAttribute('height', str(float(h)))

        # Saving position
        x, y = oglObject.GetModel().GetPosition()
        root.setAttribute('x', str(x))
        root.setAttribute('y', str(y))

    def _OglLink2xml(self, oglLink, xmlDoc):
        """
        """
        root = xmlDoc.createElement('GraphicLink')

        # Append OGL object base
        # save src and dst anchor points
        x, y = oglLink.GetSource().GetModel().GetPosition()
        root.setAttribute('srcX', str(x))
        root.setAttribute('srcY', str(y))

        x, y = oglLink.GetDestination().GetModel().GetPosition()
        root.setAttribute('dstX', str(x))
        root.setAttribute('dstY', str(y))

        root.setAttribute('spline', str(oglLink.GetSpline()))

        if isinstance(oglLink, OglAssociation):
            center = oglLink.getLabels()[CENTER]
            src = oglLink.getLabels()[SRC_CARD]
            dst = oglLink.getLabels()[DEST_CARD]
            label = xmlDoc.createElement("LabelCenter")
            root.appendChild(label)
            x, y = center.GetModel().GetPosition()
            label.setAttribute("x", str(x))
            label.setAttribute("y", str(y))
            label = xmlDoc.createElement("LabelSrc")
            root.appendChild(label)
            x, y = src.GetModel().GetPosition()
            label.setAttribute("x", str(x))
            label.setAttribute("y", str(y))
            label = xmlDoc.createElement("LabelDst")
            root.appendChild(label)
            x, y = dst.GetModel().GetPosition()
            label.setAttribute("x", str(x))
            label.setAttribute("y", str(y))

        # save control points (not anchors!)
        for x, y in oglLink.GetSegments()[1:-1]:
            item = xmlDoc.createElement('ControlPoint')
            item.setAttribute('x', str(x))
            item.setAttribute('y', str(y))
            root.appendChild(item)

        # adding the data layer object
        root.appendChild(self._PyutLink2xml(oglLink.getPyutObject(), xmlDoc))

        return root

    def _OglClass2xml(self, oglClass, xmlDoc):
        """
        Exporting an OglClass to an miniDom Element.

        @param PyutMethod oglClass : Class to save
        @param xmlDoc xmlDoc : xml document
        @return Element : XML Node
        @author Deve Roux <droux@eivd.ch>
        """
        root = xmlDoc.createElement('GraphicClass')

        # Append OGL object base (size and pos)
        self._appendOglBase(oglClass, root)

        # adding the data layer object
        root.appendChild(self._PyutClass2xml(oglClass.getPyutObject(), xmlDoc))

        return root

    def _OglNote2xml(self, oglNote, xmlDoc):
        """
        Exporting an OglNote to an miniDom Element.

        @param OglNote oglNote : Note to convert
        @param xmlDoc xmlDoc : xml document

        @return Element        : New miniDom element
        @author Philippe Waelti <pwaelti@eivd.ch>
        """
        root = xmlDoc.createElement('GraphicNote')

        # Append OGL object base (size and pos)
        self._appendOglBase(oglNote, root)

        # adding the data layer object
        root.appendChild(self._PyutNote2xml(oglNote.getPyutObject(), xmlDoc))

        return root

    def _OglActor2xml(self, oglActor, xmlDoc):
        """
        Exporting an OglActor to an miniDom Element.

        @param OglActor oglActor : Actor to convert
        @param xmlDoc Document : xml document
        @return Element : New miniDom element
        @author Philippe Waelti <pwaelti@eivd.ch>
        """
        root = xmlDoc.createElement('GraphicActor')

        # Append OGL object base (size and pos)
        self._appendOglBase(oglActor, root)

        # adding the data layer object
        root.appendChild(self._PyutActor2xml(oglActor.getPyutObject(), xmlDoc))

        return root

    def _OglUseCase2xml(self, oglUseCase, xmlDoc):
        """
        Exporting an OglUseCase to an miniDom Element.

        @param oglUseCase : UseCase to convert
        @param xmlDoc xmlDoc : xml document
        @return Element : New miniDom element
        @author Philippe Waelti <pwaelti@eivd.ch>
        """
        root = xmlDoc.createElement('GraphicUseCase')

        # Append OGL object base (size and pos)
        self._appendOglBase(oglUseCase, root)

        # adding the data layer object
        root.appendChild(self._PyutUseCase2xml(
                                        oglUseCase.getPyutObject(), xmlDoc))

        return root

    def save(self, project):
        """
        To save diagram in XML file.

        @param project

        @author Deve Roux
        @modified Laurent Burgbacher <lb@alawa.ch> : add version support
        @modified C.Dutoit 20021122 : added document container tag
        """

        dlgGauge = None
        gauge    = None
        try:
            xmlDoc  = Document()
            top     = xmlDoc.createElement("PyutProject")
            top.setAttribute('version', str(self._this_version))
            top.setAttribute('CodePath', project.getCodePath())

            xmlDoc.appendChild(top)

            # Gauge
            dlg   = Dialog(None, -1, "Saving...", style=STAY_ON_TOP | ICON_INFORMATION | RESIZE_BORDER, size=Size(207, 70))
            gauge = Gauge(dlg, -1, 100, pos=Point(2, 5), size=Size(200, 30))
            dlg.Show(True)

            # Save all documents in the project
            for document in project.getDocuments():
                documentNode = xmlDoc.createElement("PyutDocument")
                documentNode.setAttribute('type', diagramTypeAsString(document.getType()))
                top.appendChild(documentNode)

                oglObjects = document.getFrame().getUmlObjects()
                for i in range(len(oglObjects)):
                    gauge.SetValue(i*100/len(oglObjects))
                    oglObject = oglObjects[i]
                    if isinstance(oglObject, OglClass):
                        documentNode.appendChild(self._OglClass2xml(oglObject, xmlDoc))
                    elif isinstance(oglObject, OglNote):
                        documentNode.appendChild(self._OglNote2xml(oglObject, xmlDoc))
                    elif isinstance(oglObject, OglActor):
                        documentNode.appendChild(self._OglActor2xml(oglObject, xmlDoc))
                    elif isinstance(oglObject, OglUseCase):
                        documentNode.appendChild(self._OglUseCase2xml(oglObject, xmlDoc))
                    elif isinstance(oglObject, OglLink):
                        documentNode.appendChild(self._OglLink2xml(oglObject, xmlDoc))
                    elif isinstance(oglObject, OglSDInstance):
                        documentNode.appendChild(self._OglSDInstance2xml(oglObject, xmlDoc))
                    elif isinstance(oglObject, OglSDMessage):
                        documentNode.appendChild(self._OglSDMessage2xml(oglObject, xmlDoc))
        except (ValueError, Exception) as e:
            try:
                dlg.Destroy()
                self.logger.error(f'{e}')
            except (ValueError, Exception) as e:
                self.logger.error(f'{e}')
            displayError(_("Can't save file"))
            return xmlDoc

        dlg.Destroy()

        return xmlDoc

    def _getParam(self, Param):
        aParam = PyutParam()
        if Param.hasAttribute('defaultValue'):
            aParam.setDefaultValue(Param.getAttribute('defaultValue'))
        aParam.setName(Param.getAttribute('name'))
        aParam.setType(Param.getAttribute('type'))
        return aParam

    def _getOglSDInstances(self, xmlOglSDInstances, dicoOglObjects, dicoLink, dicoFather, umlFrame):
        """
        Parse the XML elements given and build data layer for PyUT classes.
        If file is version 1.0, the dictionary given will contain, for key,
        the name of the OGL object. Otherwise, it will be the ID
        (multi-same-name support from version 1.1). Everything is fixed
        later.

        @param Element[] xmlOglSDInstances : XML 'GraphicSDInstance' elements

        @param {id / srcName, OglObject} dicoOglObjects : OGL objects loaded

        @param {id / srcName, OglLink} dicoLink : OGL links loaded

        @param {id / srcName, id / srcName} dicoFather: Inheritance

        @param UmlFrame umlFrame : Where to draw

        @author Philippe Waelti <pwaelti@eivd.ch>
        @modified C.Dutoit/20021121 added display properties
        """
        for xmlOglSDInstance in xmlOglSDInstances:
            # Main objects
            pyutSDInstance = PyutSDInstance()
            oglSDInstance = OglSDInstance(pyutSDInstance, umlFrame)

            # Data layer
            xmlSDInstance = xmlOglSDInstance.getElementsByTagName(
                                                            'SDInstance')[0]

            # Pyut Data
            pyutSDInstance.setId(int(xmlSDInstance.getAttribute('id')))
            pyutSDInstance.setInstanceName(xmlSDInstance.getAttribute(
                                            'instanceName').encode("charmap"))
            pyutSDInstance.setInstanceLifeLineLength(
                    secure_int(xmlSDInstance.getAttribute('lifeLineLength')))


            dicoOglObjects[pyutSDInstance.getId()] = oglSDInstance

            # Adding OGL class to UML Frame
            x = float(xmlOglSDInstance.getAttribute('x'))
            y = float(xmlOglSDInstance.getAttribute('y'))
            w = float(xmlOglSDInstance.getAttribute('width'))
            h = float(xmlOglSDInstance.getAttribute('height'))
            oglSDInstance.SetSize(w, h)
            umlFrame.addShape(oglSDInstance, x, y)

    def _getOglSDMessages(self, xmlOglSDMessages, dicoOglObjects, dicoLink, dicoFather, umlFrame):
        """
        Parse the XML elements given and build data layer for PyUT classes.
        If file is version 1.0, the dictionary given will contain, for key,
        the name of the OGL object. Otherwise, it will be the ID
        (multi-same-name support from version 1.1). Everything is fixed
        later.

        @param Element[] xmlOglSDMessages : XML 'GraphicSDInstance elements

        @param {id / srcName, OglObject} dicoOglObjects : OGL objects loaded

        @param {id / srcName, OglLink} dicoLink : OGL links loaded

        @param {id / srcName, id / srcName} dicoFather: Inheritance

        @param UmlFrame umlFrame : Where to draw

        @author Philippe Waelti <pwaelti@eivd.ch>
        @modified C.Dutoit/20021121 added display properties
        """
        for xmlOglSDMessage in xmlOglSDMessages:

            # Data layer class
            xmlPyutSDMessage = xmlOglSDMessage.getElementsByTagName('SDMessage')[0]

            # Building OGL
            pyutSDMessage = PyutSDMessage()
            srcID = int(xmlPyutSDMessage.getAttribute('srcID'))
            dstID = int(xmlPyutSDMessage.getAttribute('dstID'))
            srcTime = int(float(xmlPyutSDMessage.getAttribute('srcTime')))
            dstTime = int(float(xmlPyutSDMessage.getAttribute('dstTime')))
            srcOgl = dicoOglObjects[srcID]
            dstOgl = dicoOglObjects[dstID]
            oglSDMessage = OglSDMessage(srcOgl, pyutSDMessage, dstOgl)
            pyutSDMessage.setOglObject(oglSDMessage)
            pyutSDMessage.setSource(srcOgl.getPyutObject(), srcTime)
            pyutSDMessage.setDestination(dstOgl.getPyutObject(), dstTime)

            # Pyut Data
            pyutSDMessage.setId(int(xmlPyutSDMessage.getAttribute('id')))
            pyutSDMessage.setMessage(xmlPyutSDMessage.getAttribute('message').encode("charmap"))

            dicoOglObjects[pyutSDMessage.getId()] = pyutSDMessage

            # Adding OGL class to UML Frame
            # x = float(xmlOglSDMessage.getAttribute('x'))
            # y = float(xmlOglSDMessage.getAttribute('y'))
            diagram = umlFrame.GetDiagram()
            dicoOglObjects[srcID].addLink(oglSDMessage)
            dicoOglObjects[dstID].addLink(oglSDMessage)
            diagram.AddShape(oglSDMessage)
            # umlFrame.addShape(oglSDMessage, x, y)

    def _getControlPoints(self, link):
        """
        To extract control points from links.

        Python 3:  This method does not seem to be used;  I'll comment it out and raise an
        exception;  Especially, since I don't know where the `Class` class comes
        from == hasii

        @since 1.0
        @author Laurent Burgbacher <lb@alawa.ch>
        """
        raise NotImplementedError('I guess this method is used after all.  See the comments')
        # class methods for this current class
        # allControlPoints = []
        #
        # for cp in Class.getElementsByTagName('ControlPoint'):
        #
        #     # point position
        #     x = cp.getAttribute('x')
        #     y = cp.getAttribute('y')
        #
        #     point = ControlPoint(x, y)
        #     allControlPoints.append(point)
        #
        # return allControlPoints

    def _getMethods(self, Class):
        """
        To extract methods form interface.

        @since 1.0
        @author Deve Roux <droux@eivd.ch>
        """
        # class methods for this currente class
        allMethods = []
        for Method in Class.getElementsByTagName("Method") :

            # method name
            aMethod = PyutMethod(Method.getAttribute('name'))

            # method visibility
            aMethod.setVisibility(Method.getAttribute('visibility'))

            # for method return type
            Return = Method.getElementsByTagName("Return")[0]
            aMethod.setReturns(Return.getAttribute('type'))

            # for methods param
            allParams = []
            for Param in  Method.getElementsByTagName("Param"):
                allParams.append(self._getParam(Param))

            # setting de params for thiy method
            aMethod.setParams(allParams)
            # hadding this method in all class methods
            allMethods.append(aMethod)

        return allMethods

    def _getFields(self, Class):
        """
        To extract fields form Class.

        @since 1.0
        @author Deve Roux <droux@eivd.ch>
        """
        # for class fields
        allFields = []
        for Field in Class.getElementsByTagName("Field"):

            aField = PyutField()
            aField.setVisibility(Field.getAttribute('visibility'))
            Param = Field.getElementsByTagName("Param")[0]

            if Param.hasAttribute('defaultValue'):
                aField.setDefaultValue(Param.getAttribute('defaultValue'))
            aField.setName(Param.getAttribute('name'))
            aField.setType(Param.getAttribute('type'))

            allFields.append(aField)
        return allFields

    def _getPyutLink(self, obj):
        """
        To extract a PyutLink from an OglLink object.

        @param String obj : Name of the object.
        @since 1.0
        @author Deve Roux <droux@eivd.ch>
        @changed Philippe Waelti <pwaelti@eivd.ch> : Refactoring campain
        @changed Laurent Burgbacher <lb@alawa.ch> : miniogl support
        """
        link = obj.getElementsByTagName("Link")[0]

        aLink = PyutLink()

        aLink.setBidir(int(link.getAttribute('bidir')))
        aLink.setDestCard(link.getAttribute('cardDestination'))
        aLink.setSrcCard(link.getAttribute('cardSrc'))
        aLink.setName(link.getAttribute('name'))
        aLink.setType(int(link.getAttribute('type')))
        # source and destination will be reconstructed by _getOglLinks

        sourceId = int(link.getAttribute('sourceId'))
        destId = int(link.getAttribute('destId'))

        return sourceId, destId, aLink

    def _getOglLinks(self, xmlOglLinks, dicoOglObjects, dicoLink, dicoFather, umlFrame):
        """
        To extract the links from an OGL object.

        @param String obj : Name of the object.
        @since 1.0
        @author Laurent Burgbacher <lb@alawa.ch>
        """
        def secure_float(x):
            if x is not None: return float(x)
            return 0.0

        def secure_int(x):
            if x is None:
                return 0
            elif x == "_DeprecatedNonBool: False" or x=="False":
                return 0
            elif x == "_DeprecatedNonBool: True" or x=="True":
                return 1
            else:
                return int(x)

        for link in xmlOglLinks:
            # src and dst anchor position
            sx = secure_float(link.getAttribute("srcX"))
            sy = secure_float(link.getAttribute("srcY"))
            dx = secure_float(link.getAttribute("dstX"))
            dy = secure_float(link.getAttribute("dstY"))
            spline = secure_int(link.getAttribute("spline"))

            # create a list of ControlPoints
            ctrlpts = []
            for ctrlpt in link.getElementsByTagName("ControlPoint"):
                x = secure_float(ctrlpt.getAttribute("x"))
                y = secure_float(ctrlpt.getAttribute("y"))
                ctrlpts.append(ControlPoint(x, y))

            # get the associated PyutLink
            srcId, dstId, pyutLink = self._getPyutLink(link)

            # CD 20060218
            src = dicoOglObjects[srcId]
            dst = dicoOglObjects[dstId]
            linkType = pyutLink.getType()
            pyutLink = PyutLink("", linkType=linkType, source=src.getPyutObject(), destination=dst.getPyutObject())

            oglLinkFactory = getOglLinkFactory()
            oglLink = oglLinkFactory.getOglLink(src, pyutLink, dst, linkType)
            src.addLink(oglLink)
            dst.addLink(oglLink)
            umlFrame.GetDiagram().AddShape(oglLink, withModelUpdate=False)

            # create the OglLink
            # oglLink = umlFrame.createNewLink(
            #    dicoOglObjects[srcId],
            #    dicoOglObjects[dstId],
            #    pyutLink.getType())
            oglLink.SetSpline(spline)

            # give it the PyutLink
            # newPyutLink = oglLink.getPyutObject()
            # set the destination PyutObject
            # newPyutLink.setDestination(dicoOglObjects[dstId].getPyutObject())
            # newPyutLink.setSource(dicoOglObjects[srcId].getPyutObject())
            newPyutLink = pyutLink

            # copy the good information from the read link
            newPyutLink.setBidir(pyutLink.getBidir())
            newPyutLink.setDestCard(pyutLink.getDestCard())
            newPyutLink.setSrcCard(pyutLink.getSrcCard())
            newPyutLink.setName(pyutLink.getName())

            # put the anchors at the right position
            srcAnchor = oglLink.GetSource()
            dstAnchor = oglLink.GetDestination()
            srcAnchor.SetPosition(sx, sy)
            dstAnchor.SetPosition(dx, dy)

            # add the control points to the line
            line = srcAnchor.GetLines()[0] # only 1 line per anchor in pyut
            parent = line.GetSource().GetParent()
            selfLink = parent is line.GetDestination().GetParent()
            # print parent
            # print line.GetDestination().GetParent()
            for ctrl in ctrlpts:
                line.AddControl(ctrl)
                if selfLink:
                    x, y = ctrl.GetPosition()
                    ctrl.SetParent(parent)
                    ctrl.SetPosition(x, y)

            if isinstance(oglLink, OglAssociation):
                center = oglLink.getLabels()[CENTER]
                src = oglLink.getLabels()[SRC_CARD]
                dst = oglLink.getLabels()[DEST_CARD]

                label = link.getElementsByTagName("LabelCenter")[0]
                x = float(label.getAttribute("x"))
                y = float(label.getAttribute("y"))
                center.SetPosition(x, y)

                label = link.getElementsByTagName("LabelSrc")[0]
                x = float(label.getAttribute("x"))
                y = float(label.getAttribute("y"))
                src.SetPosition(x, y)

                label = link.getElementsByTagName("LabelDst")[0]
                x = float(label.getAttribute("x"))
                y = float(label.getAttribute("y"))
                dst.SetPosition(x, y)

    def _getOglActors(self, xmlOglActors, dicoOglObjects, dicoLink, dicoFather, umlFrame):
        """
        Parse the XML elements given and build data layer for PyUT actors.

        @param Element[] xmlOglActors : XML 'GraphicActor' elements
        @param {id / srcName, OglObject} dicoOglObjects : OGL objects loaded
        @param {id / srcName, OglLink} dicoLink : OGL links loaded
        @param {id / srcName, id / srcName} fathers: Inheritance
        @param UmlFrame umlFrame : Where to draw
        @since 2.0
        @author Philippe Waelti <pwaelti@eivd.ch>
        """
        for xmlOglActor in xmlOglActors:
            pyutActor = PyutActor()

            # Building OGL Actor
            height = float(xmlOglActor.getAttribute('height'))
            width = float(xmlOglActor.getAttribute('width'))
            oglActor = OglActor(pyutActor, width, height)

            xmlActor = xmlOglActor.getElementsByTagName('Actor')[0]

            pyutActor.setId(int(xmlActor.getAttribute('id')))

            # adding name for this class
            pyutActor.setName(xmlActor.getAttribute('name').encode("charmap"))

            # adding associated filename (lb@alawa.ch)
            pyutActor.setFilename(xmlActor.getAttribute('filename'))

            # Update dicos
            dicoOglObjects[pyutActor.getId()] = oglActor

            # Update UML Frame
            x = float(xmlOglActor.getAttribute('x'))
            y = float(xmlOglActor.getAttribute('y'))
            umlFrame.addShape(oglActor, x, y)

    def _getOglUseCases(self, xmlOglUseCases, dicoOglObjects, dicoLink, dicoFather, umlFrame):
        """
        Parse the XML elements given and build data layer for PyUT actors.

        @param Element[] xmlOglUseCases : XML 'GraphicUseCase' elements
        @param {id / srcName, OglObject} dicoOglObjects : OGL objects loaded
        @param {id / srcName, OglLink} dicoLink : OGL links loaded
        @param {id / srcName, id / srcName} fathers: Inheritance
        @param UmlFrame umlFrame : Where to draw
        @since 2.0
        @author Philippe Waelti <pwaelti@eivd.ch>
        """
        for xmlOglUseCase in xmlOglUseCases:
            pyutUseCase = PyutUseCase()

            # Building OGL UseCase
            height = float(xmlOglUseCase.getAttribute('height'))
            width = float(xmlOglUseCase.getAttribute('width'))
            oglUseCase = OglUseCase(pyutUseCase, width, height)

            xmlUseCase = xmlOglUseCase.getElementsByTagName('UseCase')[0]

            pyutUseCase.setId(int(xmlUseCase.getAttribute('id')))

            # adding name for this class
            pyutUseCase.setName(xmlUseCase.getAttribute('name').encode("charmap"))

            # adding associated filename (lb@alawa.ch)
            pyutUseCase.setFilename(xmlUseCase.getAttribute('filename'))

            # Update dicos
            dicoOglObjects[pyutUseCase.getId()] = oglUseCase

            # Update UML Frame
            x = float(xmlOglUseCase.getAttribute('x'))
            y = float(xmlOglUseCase.getAttribute('y'))
            umlFrame.addShape(oglUseCase, x, y)

    def open(self, dom, project):
        """
        To open a file and creating diagram.

        @author Deve Roux
        @modified Laurent Burgbacher : version 2
        @modified C.Dutoit : version 5, 7
        """
        dlgGauge = None
        gauge = None
        try:
            root = dom.getElementsByTagName("PyutProject")[0]
            if root.hasAttribute('version'):
                version = int(root.getAttribute("version"))
            else:
                version = 1
            if version != self._this_version:
                self.logger.error("Wrong version of the file loader")
                eMsg: str = f'This is version {self._this_version} and the file version is {version}'
                self.logger.error(eMsg)
                raise Exception(f'VERSION_ERROR:  {eMsg}')
            project.setCodePath(root.getAttribute("CodePath"))

            # Create and init gauge
            dlgGauge = Dialog(None, -1, "Loading...", style=STAY_ON_TOP | ICON_INFORMATION | RESIZE_BORDER, size=Size(207, 70))
            gauge    = Gauge(dlgGauge, -1, 5, pos=Point(2, 5), size=Size(200, 30))
            dlgGauge.Show(True)

            # for all elements il xml file
            dlgGauge.SetTitle("Reading file...")
            gauge.SetValue(1)

            for documentNode in dom.getElementsByTagName("PyutDocument"):

                dicoOglObjects = {}     # format {id/name : oglClass}
                dicoLink       = {}     # format [id/name : PyutLink}
                dicoFather     = {}     # format {id child oglClass : [id fathers]}

                # docType = documentNode.getAttribute("type").encode("charmap")
                docType = documentNode.getAttribute("type")     # Python 3 update

                document = project.newDocument(diagramTypeFromString(docType))
                umlFrame = document.getFrame()
                # print "PyutXml/open-4c"

                ctrl = getMediator()
                ctrl.getFileHandling().showFrame(umlFrame)

                self._getOglClasses(documentNode.getElementsByTagName('GraphicClass'),    dicoOglObjects, dicoLink, dicoFather, umlFrame)
                self._getOglNotes(documentNode.getElementsByTagName('GraphicNote'),       dicoOglObjects, dicoLink, dicoFather, umlFrame)
                self._getOglActors(documentNode.getElementsByTagName('GraphicActor'),     dicoOglObjects, dicoLink, dicoFather, umlFrame)
                self._getOglUseCases(documentNode.getElementsByTagName('GraphicUseCase'), dicoOglObjects, dicoLink, dicoFather, umlFrame)
                self._getOglLinks(documentNode.getElementsByTagName("GraphicLink"),       dicoOglObjects, dicoLink, dicoFather, umlFrame)
                self._getOglSDInstances(documentNode.getElementsByTagName("GraphicSDInstance"), dicoOglObjects, dicoLink, dicoFather, umlFrame)
                self._getOglSDMessages(documentNode.getElementsByTagName("GraphicSDMessage"),   dicoOglObjects, dicoLink, dicoFather, umlFrame)

                # fix the link's destination field
                gauge.SetValue(2)

                dlgGauge.SetTitle("Fixing link's destination...")
                for links in list(dicoLink.values()):
                    for link in links:
                        link[1].setDestination(dicoOglObjects[link[0]].getPyutObject())

                # adding fathers
                dlgGauge.SetTitle("Adding fathers...")
                gauge.SetValue(3)
                for child, fathers in list(dicoFather.items()):
                    for father in fathers:
                        umlFrame.createInheritanceLink(\
                                dicoOglObjects[child], dicoOglObjects[father])

                # adding links to this OGL object
                dlgGauge.SetTitle("Adding Links...")
                gauge.SetValue(4)
                # print "PyutXml/open-6"
                for src, links in list(dicoLink.items()):
                    for link in links:
                        createdLink = umlFrame.createNewLink(dicoOglObjects[src], dicoOglObjects[link[1].getDestination().getId()], link[1].getType())

                        # fix link with the loaded information
                        pyutLink = createdLink.getPyutObject()
                        pyutLink.setBidir(link[1].getBidir())
                        pyutLink.setDestCard(link[1].getDestCard())
                        pyutLink.setSrcCard(link[1].getSrcCard())
                        pyutLink.setName(link[1].getName())
        except (ValueError, Exception) as e:
            if dlgGauge is not None:
                dlgGauge.Destroy()
            displayError(_(f"Can't load file {e}"))
            umlFrame.Refresh()
            return

        # to draw diagram
        umlFrame.Refresh()
        gauge.SetValue(5)

        if dlgGauge is not None:
            dlgGauge.Destroy()

    def _getOglClasses(self, xmlOglClasses, dicoOglObjects, dicoLink, dicoFather, umlFrame):
        """
        Parse the XML elements given and build data layer for PyUT classes.
        If file is version 1.0, the dictionary given will contain, for key,
        the name of the OGL object. Otherwise, it will be the ID
        (multi-same-name support from version 1.1). Everything is fixed
        later.

        @param Element[] xmlOglClasses : XML 'GraphicClass' elements

        @param {id / srcName, OglObject} dicoOglObjects : OGL objects loaded

        @param {id / srcName, OglLink} dicoLink : OGL links loaded

        @param {id / srcName, id / srcName} dicoFather: Inheritance

        @param UmlFrame umlFrame : Where to draw
        @author Philippe Waelti <pwaelti@eivd.ch>
        @modified C.Dutoit/20021121 added display properties
        """
        # print "PyutXml/open-4d00a"
        for xmlOglClass in xmlOglClasses:

            # print "PyutXml/open-4d00b"
            pyutClass = PyutClass()
            # print "PyutXml/open-4d00b1"
            # print xmlOglClass.getAttribute('height')
            # print float
            # print dir(float)
            # print type(xmlOglClass.getAttribute('height'))
            # print float(xmlOglClass.getAttribute('height'))
            # Building OGL class
            height = float(xmlOglClass.getAttribute('height'))
            # print "PyutXml/open-4d00b2"
            width = float(xmlOglClass.getAttribute('width'))
            # print "PyutXml/open-4d00b3"
            oglClass = OglClass(pyutClass, width, height)

            # Data layer class
            # print "PyutXml/open-4d00c"
            xmlClass = xmlOglClass.getElementsByTagName('Class')[0]

            pyutClass.setId(int(xmlClass.getAttribute('id')))

            # adding name for this class
            pyutClass.setName(xmlClass.getAttribute('name').encode("charmap"))
            # print "PyutXml/open-4d00d"

            # adding description
            pyutClass.setDescription(xmlClass.getAttribute('description'))

            # adding stereotype
            if xmlClass.hasAttribute('stereotype'):
                pyutClass.setStereotype(getPyutStereotype(xmlClass.getAttribute('stereotype')))
            #print "PyutXml/open-4d00e"

            # adding display properties (cd)
            value = secure_bool(xmlClass.getAttribute('showStereotype'))
            pyutClass.setShowStereotype(value)
            value = secure_bool(xmlClass.getAttribute('showMethods'))
            pyutClass.setShowMethods(value)
            value = secure_bool(xmlClass.getAttribute('showFields'))
            pyutClass.setShowFields(value)
            #print "PyutXml/open-4d00f"

            # adding associated filename (lb@alawa.ch)
            pyutClass.setFilename(xmlClass.getAttribute('filename'))

            # adding methods for this class
            pyutClass.setMethods(self._getMethods(xmlClass))
            # print "PyutXml/open-4d00g"

            # adding fields for this class
            pyutClass.setFields(self._getFields(xmlClass))

            dicoOglObjects[pyutClass.getId()] = oglClass
            # print "PyutXml/open-4d00h"

            # Adding OGL class to UML Frame
            x = float(xmlOglClass.getAttribute('x'))
            y = float(xmlOglClass.getAttribute('y'))
            # print "PyutXml/open-4d00i"
            umlFrame.addShape(oglClass, x, y)

    def _getOglNotes(self, xmlOglNotes, dicoOglObjects, dicoLink, dicoFather, umlFrame):
        """
        Parse the XML elements given and build data layer for PyUT notes.
        If file is version 1.0, the dictionary given will contain, for key,
        the name of the OGL object. Otherwise, it will be the ID
        (multi-same-name support from version 1.1). Everything is fixed
        later.

        @param Element[] xmlOglNotes : XML 'GraphicNote' elements

        @param {id / srcName, OglObject} dicoOglObjects : OGL objects loaded

        @param {id / srcName, OglLink} dicoLink : OGL links loaded

        @param {id / srcName, id / srcName} dicoFather: Inheritance

        @param UmlFrame umlFrame : Where to draw

        @author Philippe Waelti
        @modified C.Dutoit 2002-12-26, added multiline support
        """
        for xmlOglNote in xmlOglNotes:
            pyutNote = PyutNote()

            # Building OGL Note
            height = float(xmlOglNote.getAttribute('height'))
            width = float(xmlOglNote.getAttribute('width'))
            oglNote = OglNote(pyutNote, width, height)

            xmlNote = xmlOglNote.getElementsByTagName('Note')[0]

            pyutNote.setId(int(xmlNote.getAttribute('id')))

            # adding name for this class
            name = xmlNote.getAttribute('name')
            name = name.replace("\\\\\\\\", "\n")
            pyutNote.setName(name.encode("charmap"))

            # adding associated filename (lb@alawa.ch)
            pyutNote.setFilename(xmlNote.getAttribute('filename'))

            # Update dicos
            dicoOglObjects[pyutNote.getId()] = oglNote

            # Update UML Frame
            x = float(xmlOglNote.getAttribute('x'))
            y = float(xmlOglNote.getAttribute('y'))
            umlFrame.addShape(oglNote, x, y)

    def joli(self, fileName):
        """
        To open a file and creating diagram.

        @since 1.0
        @author Deve Roux <droux@eivd.ch>
        """
        dom = parse(StringIO(open(fileName).read()))
        # PrettyPrint(dom, open("joli.xml", 'w'))
        print(f"{dom.toprettyxml()}")                            # Maybe this ?