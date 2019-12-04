from org.pyut.PyutUtils import PyutUtils

from org.pyut.general.Mediator import ACTION_NEW_ACTOR
from org.pyut.general.Mediator import ACTION_NEW_INHERIT_LINK
from org.pyut.general.Mediator import ACTION_NEW_NOTE_LINK
from org.pyut.general.Mediator import ACTION_NEW_AGGREGATION_LINK
from org.pyut.general.Mediator import ACTION_SELECTOR
from org.pyut.general.Mediator import ACTION_NEW_CLASS
from org.pyut.general.Mediator import ACTION_NEW_NOTE
from org.pyut.general.Mediator import ACTION_NEW_IMPLEMENT_LINK
from org.pyut.general.Mediator import ACTION_NEW_COMPOSITION_LINK
from org.pyut.general.Mediator import ACTION_NEW_ASSOCIATION_LINK
from org.pyut.general.Mediator import ACTION_ZOOM_OUT
from org.pyut.general.Mediator import ACTION_ZOOM_IN
from org.pyut.general.Mediator import ACTION_NEW_SD_MESSAGE
from org.pyut.general.Mediator import ACTION_NEW_SD_INSTANCE
from org.pyut.general.Mediator import ACTION_NEW_USECASE


class SharedIdentifiers:
    [
        ID_MNUFILENEWPROJECT, ID_MNUFILEOPEN, ID_MNUFILESAVE,
        ID_MNUFILESAVEAS, ID_MNUFILEEXIT, ID_MNUEDITCUT,
        ID_MNUEDITCOPY, ID_MNUEDITPASTE, ID_MNUHELPABOUT,
        ID_MNUFILEIMP, ID_MNUFILE, ID_MNUFILEDIAGRAMPROPER,
        ID_MNUFILEPRINTSETUP, ID_MNUFILEPRINTPREV, ID_MNUFILEPRINT,
        ID_MNUADDPYUTHIERARCHY, ID_MNUADDOGLHIERARCHY,
        ID_MENU_GRAPHIC_ERROR_VIEW, ID_MENU_TEXT_ERROR_VIEW, ID_MENU_RAISE_ERROR_VIEW,
        ID_MNUHELPINDEX,
        ID_MNUHELPWEB, ID_MNUFILEEXP, ID_MNUFILEEXPBMP,
        ID_MNUEDITSHOWTOOLBAR, ID_ARROW, ID_CLASS,
        ID_REL_INHERITANCE, ID_REL_REALISATION, ID_REL_COMPOSITION,
        ID_REL_AGGREGATION, ID_REL_ASSOCIATION, ID_MNUFILEEXPJPG,
        ID_MNUPROJECTCLOSE, ID_NOTE, ID_ACTOR,
        ID_USECASE, ID_REL_NOTE, ID_MNUHELPVERSION,
        ID_MNUFILEEXPPS, ID_MNUFILEEXPPNG, ID_MNUFILEPYUTPROPER,
        ID_MNUFILEEXPPDF, ID_MNUFILENEWCLASSDIAGRAM, ID_MNUFILENEWSEQUENCEDIAGRAM,
        ID_MNUFILENEWUSECASEDIAGRAM, ID_SD_INSTANCE,
        ID_MNUFILEINSERTPROJECT, ID_SD_MESSAGE, ID_MNUEDITSELECTALL,
        ID_MNUFILEREMOVEDOCUMENT, ID_DEBUG,
        ID_ZOOMIN, ID_ZOOMOUT, ID_ZOOM_VALUE,
        ID_MNUREDO, ID_MNUUNDO
    ] = PyutUtils.assignID(57)

    ACTIONS = {
        ID_ARROW:             ACTION_SELECTOR,
        ID_CLASS:             ACTION_NEW_CLASS,
        ID_NOTE:              ACTION_NEW_NOTE,
        ID_REL_INHERITANCE:   ACTION_NEW_INHERIT_LINK,
        ID_REL_REALISATION:   ACTION_NEW_IMPLEMENT_LINK,
        ID_REL_COMPOSITION:   ACTION_NEW_COMPOSITION_LINK,
        ID_REL_AGGREGATION:   ACTION_NEW_AGGREGATION_LINK,
        ID_REL_ASSOCIATION:   ACTION_NEW_ASSOCIATION_LINK,
        ID_REL_NOTE:          ACTION_NEW_NOTE_LINK,
        ID_ACTOR:             ACTION_NEW_ACTOR,
        ID_USECASE:           ACTION_NEW_USECASE,
        ID_SD_INSTANCE:       ACTION_NEW_SD_INSTANCE,
        ID_SD_MESSAGE:        ACTION_NEW_SD_MESSAGE,
        ID_ZOOMIN:            ACTION_ZOOM_IN,
        ID_ZOOMOUT:           ACTION_ZOOM_OUT
}
