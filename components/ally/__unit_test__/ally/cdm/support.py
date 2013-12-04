'''
Created on Nov 29, 2013

@author: mihaigociu
'''
# Required in order to register the package extender whenever the unit test is run.
if True:
    import package_extender
    package_extender.PACKAGE_EXTENDER.setForUnitTest(True)

# --------------------------------------------------------------------
from ally.cdm.support import VersioningCDM
from ally.cdm.impl.local_filesystem import HTTPDelivery, LocalFileSystemCDM
from ally.cdm.spec import PathNotFound
from ally.zip.util_zip import normOSPath
from os import makedirs, remove, sep, stat
from os.path import join, dirname, isfile
from shutil import rmtree
from tempfile import NamedTemporaryFile, TemporaryDirectory
import re
import unittest

normpath = lambda txt: re.sub('[\\W]+', '', txt)

class TestCdmVersioning(unittest.TestCase):

    def testCDMWithVersioning(self):
        d = HTTPDelivery()
        rootDir = TemporaryDirectory()
        d.serverURI = 'http://localhost/content/'
        d.repositoryPath = rootDir.name
#        d.repositoryPath = '/var/www/repository'
#        ioc.Initializer.initialize(d)
        cdm = VersioningCDM(LocalFileSystemCDM())
        cdm.wrapped.delivery = d

        # test publish from a file from the file system
        try:
            srcTmpFile = NamedTemporaryFile(delete=False)
            srcTmpFile.close()
            dstPath = 'testdir1/tempfile.txt'
            cdm.publishFromFile(dstPath, srcTmpFile.name)
            dstFilePath = join(d.getRepositoryPath(), normOSPath(dstPath))
            
            cdm.publishFromFile(dstPath, srcTmpFile.name)
            cdm.publishFromFile(dstPath, srcTmpFile.name)
            
            uri = cdm.getURI(dstPath)
            
            #TODO: test that the uri points to the last version of the file
            #also test that there is only one last-version of the file
            
            self.assertTrue(isfile(dstFilePath))
            self.assertEqual(cdm.getMetadata(dstPath)['lastModified'], stat(dstFilePath).st_mtime)
        finally:
            rmtree(dirname(dstFilePath))
            remove(srcTmpFile.name)

