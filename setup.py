"""
This is a setup.py script generated by py2applet

Usage:
    python setup.py py2app
"""

from setuptools import setup

APP = ['src/Pyut.py']
DATA_FILES = [('org/pyut/resources', ['src/org/pyut/resources/loggingConfiguration.json']),
              ('org/pyut/resources', ['src/org/pyut/resources/Kilroy-Pyut.txt']),
              ('org/pyut/resources', ['src/org/pyut/resources/Help.txt']),
              ('org/pyut/resources', ['src/org/pyut/resources/Kudos.txt']),

              ('org/pyut/resources/img', ['src/org/pyut/resources/img/pyut.ico']),
              ('org/pyut/resources/img', ['src/org/pyut/resources/img/ImgSplash.py']),
              ('org/pyut/resources/img', ['src/org/pyut/resources/img/ImgTipsFrameTipsLogo.py']),
              ('org/pyut/resources/img', ['src/org/pyut/resources/img/ImgToolboxActor.py']),
              ('org/pyut/resources/img', ['src/org/pyut/resources/img/ImgToolboxArrow.py']),
              ('org/pyut/resources/img', ['src/org/pyut/resources/img/ImgToolboxClass.py']),
              ('org/pyut/resources/img', ['src/org/pyut/resources/img/ImgToolboxNewClassDiagram.py']),
              ('org/pyut/resources/img', ['src/org/pyut/resources/img/ImgToolboxNewProject.py']),
              ('org/pyut/resources/img', ['src/org/pyut/resources/img/ImgToolboxNewSequenceDiagram.py']),
              ('org/pyut/resources/img', ['src/org/pyut/resources/img/ImgToolboxNewUseCaseDiagram.py']),
              ('org/pyut/resources/img', ['src/org/pyut/resources/img/ImgToolboxNote.py']),
              ('org/pyut/resources/img', ['src/org/pyut/resources/img/ImgToolboxOpenFile.py']),
              ('org/pyut/resources/img', ['src/org/pyut/resources/img/ImgToolboxRedo.py']),
              ('org/pyut/resources/img', ['src/org/pyut/resources/img/ImgToolboxRelationshipAggregation.py']),
              ('org/pyut/resources/img', ['src/org/pyut/resources/img/ImgToolboxRelationshipAssociation.py']),
              ('org/pyut/resources/img', ['src/org/pyut/resources/img/ImgToolboxRelationshipComposition.py']),
              ('org/pyut/resources/img', ['src/org/pyut/resources/img/ImgToolboxRelationshipInheritance.py']),
              ('org/pyut/resources/img', ['src/org/pyut/resources/img/ImgToolboxRelationshipNote.py']),
              ('org/pyut/resources/img', ['src/org/pyut/resources/img/ImgToolboxRelationshipRealization.py']),
              ('org/pyut/resources/img', ['src/org/pyut/resources/img/ImgToolboxSaveDiagram.py']),
              ('org/pyut/resources/img', ['src/org/pyut/resources/img/ImgToolboxSequenceDiagramInstance.py']),
              ('org/pyut/resources/img', ['src/org/pyut/resources/img/ImgToolboxSequenceDiagramMessage.py']),
              ('org/pyut/resources/img', ['src/org/pyut/resources/img/ImgToolboxSystem.py']),
              ('org/pyut/resources/img', ['src/org/pyut/resources/img/ImgToolboxUndo.py']),
              ('org/pyut/resources/img', ['src/org/pyut/resources/img/ImgToolboxUnknown.py']),
              ('org/pyut/resources/img', ['src/org/pyut/resources/img/ImgToolboxZoomIn.py']),
              ('org/pyut/resources/img', ['src/org/pyut/resources/img/ImgToolboxZoomOut.py']),

              ]
OPTIONS = {}

setup(
    app=APP,
    data_files=DATA_FILES,
    packages=['org',
              'org.pyut',
              'org.pyut.commands',
              'org.pyut.dialogs',
              'org.pyut.enums',
              'org.pyut.errorcontroller',
              'org.pyut.experimental',
              'org.pyut.general', 'org.pyut.general.exceptions',
              'org.pyut.history',
              'org.pyut.miniogl',
              'org.pyut.model',
              'org.pyut.ogl', 'org.pyut.ogl.sd',
              'org.pyut.persistence', 'org.pyut.persistence.converters',
              'org.pyut.plugins',
              'org.pyut.plugins.base',
              'org.pyut.plugins.common',
              'org.pyut.plugins.dtd',
              'org.pyut.plugins.fastedit',
              'org.pyut.plugins.gml',
              'org.pyut.plugins.io',
              'org.pyut.plugins.iopythonsupport',
              'org.pyut.plugins.orthogonal',
              'org.pyut.plugins.sugiyama',
              'org.pyut.plugins.tools',
              'org.pyut.plugins.xmi',
              'org.pyut.plugins.xsd',
              'org.pyut.resources', 'org.pyut.resources.img', 'org.pyut.resources.locale',
              'org.pyut.ui', 'org.pyut.ui.tools'
              ],
    include_package_data=True,
    zip_safe=False,
    package_dir={'': 'src'},

    url='https://github.com/hasii2011/PyUt',
    author='Humberto A. Sanchez II',
    author_email='Humberto.A.Sanchez.II@gmail.com',
    description='The Python UML Tool',
    options={},
    setup_requires=['py2app'],
    install_requires=['antlr4-python3-runtime',
                      'fpdf2',
                      'networkx',
                      'orthogonal',
                      'pygmlparser',
                      'pyumldiagrams',
                      'wxPython',
                      'xmlschema',
                      ]
)
