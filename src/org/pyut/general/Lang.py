
from logging import Logger
from logging import getLogger

import gettext

from wx import LANGUAGE_CHINESE_TRADITIONAL
from wx import LANGUAGE_DANISH
from wx import LANGUAGE_ENGLISH
from wx import LANGUAGE_ESPERANTO
from wx import LANGUAGE_FRENCH
from wx import LANGUAGE_GERMAN
from wx import LANGUAGE_INDONESIAN
from wx import LANGUAGE_POLISH
from wx import LANGUAGE_SPANISH
from wx import Locale

from org.pyut.PyutPreferences import PyutPreferences

from org.pyut.errorcontroller.ErrorManager import ErrorManager

# Constants
DEFAULT_LANG = "en"
LANGUAGES = {
        DEFAULT_LANG: (
            "English",              LANGUAGE_ENGLISH),
            "da": ("Danish",        LANGUAGE_DANISH),
            "de": ("Deutsch",       LANGUAGE_GERMAN),
            "eo": ("Esperanto",     LANGUAGE_ESPERANTO),
            "es": ("Spanish",       LANGUAGE_SPANISH),
            "fr": ("Francais",      LANGUAGE_FRENCH),
            "id": ("Indonesian",    LANGUAGE_INDONESIAN),
            "pl": ("Polish",        LANGUAGE_POLISH),
            "ci": ("chinese-utf8",  LANGUAGE_CHINESE_TRADITIONAL),
        }


def importLanguage():

    moduleLogger: Logger = getLogger(__name__)
    # Get language from preferences
    prefs = PyutPreferences()
    language = prefs['I18N']

    # Set default language?
    if language not in LANGUAGES:
        # Use default language
        language = DEFAULT_LANG

    # Set language for all application
    moduleLogger.debug(f'Installing language <{language}>')
    try:
        wxLangID   = LANGUAGES[language][1]
        domain    = "Pyut"
        localedir = "src"  # "./locale"     TODO: look this up via a resource directory
        # print "langid=", wxLangID

        method = 0          # Really ?
        if method == 0:
            # Possibility to load all languages, then do an install on fly
            tr = gettext.translation(domain, localedir, languages=[language])
            tr.install(True)
        elif method == 1:

            # Set locale for wxWidget
            loc = Locale(wxLangID)
            loc.AddCatalogLookupPathPrefix(localedir)
            loc.AddCatalog(domain)

            # Set up python's gettext
            moduleLogger.info(f'Encoding name is {loc.GetCanonicalName()}')
            mytrans = gettext.translation(domain, localedir, [loc.GetCanonicalName()], fallback=True)
            mytrans.install(unicode=True)
    except (ValueError, Exception) as e:
        # If there has been a problem with i18n
        moduleLogger.error(f'Warning: problem with gettext, i18n not used.  Error: {e}')
        errMsg = ErrorManager.getErrorInfo()
        moduleLogger.error(errMsg)
