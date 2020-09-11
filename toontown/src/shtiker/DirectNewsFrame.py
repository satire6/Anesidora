import os
import time
import datetime
from pandac.PandaModules import Filename, DSearchPath, TextNode
from pandac.PandaModules import HTTPClient, Ramfile, DocumentSpec
from direct.showbase import DirectObject
from direct.gui.DirectGui import DirectFrame, DGG #, DirectButton, DirectLabel
from direct.directnotify import DirectNotifyGlobal
from direct.task.Task import Task
from direct.showbase import AppRunnerGlobal
from toontown.shtiker import IssueFrame
from toontown.toonbase import TTLocalizer

class DirectNewsFrame(DirectObject.DirectObject):

    TaskName = 'HtmlViewUpdateTask'
    TaskChainName = "RedownladTaskChain"
    RedownloadTaskName = "RedownloadNewsTask"
    NewsBaseDir = config.GetString("news-base-dir", "phase_3.5/models/news")
    NewsStageDir = config.GetString("news-stage-dir", "news")
    # taken from In Game NewsFrame
    FrameDimensions = (-1.30666637421, 1.30666637421, -0.751666665077, 0.751666665077)
    notify = DirectNotifyGlobal.directNotify.newCategory("DirectNewsFrame")
    NewsIndexFilename = config.GetString("news-index-filename", "http_news_index.txt")
    NewsOverHttp = config.GetBool("news-over-http", True)
    CacheIndexFilename = 'cache_index.txt'

    # home page is considered one section, must always be first
    # home, news, events, talk of the town, ask toontown, toon resistance
    SectionIdents = ['hom', 'new', 'evt', 'tot', 'att', 'tnr']
    
    def __init__(self, parent = aspect2d):
        DirectObject.DirectObject.__init__(self)
        self.accept("newsSnapshot", self.doSnapshot)
        self.active = False
        self.parent = parent
        self.issues = []
        self.accept("newsChangeWeek", self.changeWeek)
        self.curIssueIndex = 0
        self.strFilenames = None
        self.redownloadingNews = False
        self.startRedownload = datetime.datetime.now() # just used for timing
        self.endRedownload = datetime.datetime.now() # just used for timing
        self.load()
        self.percentDownloaded = 0.0
        self.numIssuesExpected = 0
        self.needsParseNews = True
        if self.NewsOverHttp:
            self.redownloadNews()
        
        self.accept("newIssueOut", self.handleNewIssueOut)
        self.accept("clientCleanup", self.handleClientCleanup)

    def parseNewsContent(self):
        """Open up the directory, read all the files, and figure out the structure."""
        if not self.needsParseNews:
            return
        assert not self.redownloadingNews
        self.needsParseNews = False
        
        result = False
        newsDir = self.findNewsDir()
        if newsDir:
            allHomeFiles = self.getAllHomeFilenames(newsDir)
            self.notify.debug("len allHomeFiles = %s" % len(allHomeFiles))
            self.numIssuesExpected = len(allHomeFiles)
            if allHomeFiles:
                for myIssueIndex, oneHomeFile in enumerate(allHomeFiles):
                    if type(oneHomeFile) == type(""):
                        justFilename = oneHomeFile
                    else:
                        justFilename = oneHomeFile.getFilename().getBasename()
                    self.notify.debug("parseNewContent %s" % justFilename)
                    parts = justFilename.split('_')
                    dateStr = parts[3]
                    oneIssue = IssueFrame.IssueFrame(self.backFrame, newsDir, dateStr, myIssueIndex, len(allHomeFiles), self.strFilenames)
                    oneIssue.hide()
                    self.issues.append(oneIssue)
                if self.issues:
                    self.issues[-1].show()
                    self.curIssueIndex = len(self.issues) - 1
                    result = True

        if hasattr(base.cr, 'inGameNewsMgr') and base.cr.inGameNewsMgr:
            # we should get here only when a new issue comes out mid game
            self.createdTime = base.cr.inGameNewsMgr.getLatestIssue()
            self.notify.debug("setting created time to latest issue %s" % self.createdTime)
        else:            
            # this is sucky that at this point (initial load) we don't have in game news mgr
            self.createdTime = base.cr.toontownTimeManager.getCurServerDateTime()
            self.notify.debug("setting created time cur server time %s" % self.createdTime)
        return result

    def getAllHomeFilenames(self, newsDir):
        """Find all the issues that are available."""
            
        self.notify.debug("getAllHomeFilenames")
        newsDirAsFile = vfs.getFile(Filename(newsDir))
        fileList = newsDirAsFile.scanDirectory()
        fileNames = fileList.getFiles()
        self.notify.debug("filenames=%s" % fileNames)
        # scan through and find hom1. thats got to be a home page
        homeFileNames = set([])
        for name in fileNames:
            self.notify.debug("processing %s" % name)
            baseName = name.getFilename().getBasename()
            self.notify.debug("baseName=%s" % baseName)
            if "hom1." in baseName:
                homeFileNames.add(name)
            else:
                self.notify.debug("hom1. not in baseName")
                    
        if not homeFileNames:
            #self.notify.error("couldnt find hom1. in %s" % fileNames)
            self.notify.warning("couldnt find hom1. in %s" % fileNames)
            self.setErrorMessage(TTLocalizer.NewsPageNoIssues)
            return []

        def fileCmp( fileA, fileB):
            return fileA.getFilename().compareTo(fileB.getFilename())
        homeFileNames = list(homeFileNames)
        homeFileNames.sort(cmp = fileCmp)
        self.notify.debug("returned homeFileNames=%s" % homeFileNames)
        
        return homeFileNames

    def findNewsDir(self):
        """Returns the directory string for news content.

        Returns None if it cant find the directory
        """

        if self.NewsOverHttp:
            # If we're running news-over-http, we dump the news into a
            # staging directory.
            return self.NewsStageDir
        
        searchPath = DSearchPath()
        if AppRunnerGlobal.appRunner:
            # In the web-publish runtime, it will always be here:
            searchPath.appendDirectory(Filename.expandFrom('$TT_3_5_ROOT/phase_3.5/models/news'))
        else:
            # In the launcher or dev environment, look here:
            basePath = os.path.expandvars('$TTMODELS') or './ttmodels'
            searchPath.appendDirectory(
                Filename.fromOsSpecific(basePath+'/built/' + self.NewsBaseDir))
            searchPath.appendDirectory(Filename(self.NewsBaseDir))
        
        pfile = Filename(self.NewsIndexFilename)
        found = vfs.resolveFilename(pfile, searchPath)
        if not found:
            self.notify.warning('findNewsDir - no path: %s' % self.NewsIndexFilename)
            self.setErrorMessage(TTLocalizer.NewsPageErrorDownloadingFile % self.NewsIndexFilename)
            return None
        self.notify.debug("found index file %s" % pfile)
        realDir = pfile.getDirname()
        return realDir

    def load(self):
        """Create the gui objects we need."""
        self.loadBackground()
        #self.loadMainPage()

    def loadBackground(self):
        """Create a plain white background image, that covers over the shtickerbook"""
        # HtmlView: webFrame  = -1.30666637421 1.30666637421 -0.751666665077 0.751666665077
        upsellBackground = loader.loadModel("phase_3.5/models/gui/tt_m_gui_ign_newsStatusBackground")
        imageScaleX = self.FrameDimensions[1] - self.FrameDimensions[0]
        imageScaleY = self.FrameDimensions[3] - self.FrameDimensions[2]
        self.backFrame = DirectFrame(
            parent = self.parent,
            image = upsellBackground,
            image_scale = (imageScaleX, 1, imageScaleY),
            frameColor = (1,1,1,0),
            frameSize = self.FrameDimensions,
            pos = (0,0,0),
            relief = DGG.FLAT,
            text = TTLocalizer.NewsPageDownloadingNews1,
            text_scale = 0.06,
            text_pos = (0,-0.4),
            )

    def addDownloadingTextTask(self):
        """Add a simple little task to show in game news is downloading stuff."""
        self.removeDownloadingTextTask()
        task = taskMgr.doMethodLater(1,self.loadingTextTask, "DirectNewsFrameDownloadingTextTask")
        task.startTime = globalClock.getFrameTime()
        self.loadingTextTask(task)

    def removeDownloadingTextTask(self):
        """Add a simple little task to show in game news is downloading stuff."""
        taskMgr.remove("DirectNewsFrameDownloadingTextTask")        

    def loadMainPage(self):
        """Create the other gui for this."""
        self.mainFrame = DirectFrame(
            parent = self.backFrame,
            frameSize = self.FrameDimensions,
            frameColor = (1,0,0,1),
            )

    def activate(self):
        """
        Check if we have a new issue, and prompt the user if we have one.
        """
        if hasattr(self,"createdTime") and \
           self.createdTime < base.cr.inGameNewsMgr.getLatestIssue() and \
           self.NewsOverHttp and \
           not self.redownloadingNews:
            # we have a new issue, ask the user if he wants to download it
            # let's assume he clicked yes
            self.redownloadNews()
            pass
        
        else:
            self.addDownloadingTextTask()

        # Load up the news content the first time the user asks to see
        # it.
        if self.needsParseNews and not self.redownloadingNews:
            self.parseNewsContent()

        self.active = True

    def deactivate(self):
        """
        self.quad.hide()
        taskMgr.remove(self.TaskName)
        """
        self.removeDownloadingTextTask()
        self.active = False

    def unload(self):
        """
        self.deactivate()        
        HtmlView.HtmlView.unload(self)
        """
        self.removeDownloadingTextTask()
        result = taskMgr.remove(self.RedownloadTaskName)
        self.ignore("newsSnapshot")
        self.ignore("newsChangeWeek")
        self.ignore("newIssueOut")
        self.ignore("clientCleanup")

    def handleClientCleanup(self):
        """User killing toontown, detach the backframe."""
        pass
        
    def doSnapshot(self):
        "Save the current browser contents to a png file."""
        pass

    def changeWeek(self, issueIndex):
        """Change the issue we are displaying."""
        if 0 <= issueIndex and issueIndex < len(self.issues):
            self.issues[self.curIssueIndex].hide()
            self.issues[issueIndex].show()
            self.curIssueIndex = issueIndex

    def loadingTextTask(self, task):
        """Change a visual element to indicate we're still downloading."""
        timeIndex = int(globalClock.getFrameTime() - task.startTime) % 3
        timeStrs = (TTLocalizer.NewsPageDownloadingNews0,
                    TTLocalizer.NewsPageDownloadingNews1,
                    TTLocalizer.NewsPageDownloadingNews2)
        textToDisplay = timeStrs[timeIndex] % (int(self.percentDownloaded*100))

        if self.backFrame["text"] != textToDisplay:
            if TTLocalizer.NewsPageDownloadingNewsSubstr in self.backFrame["text"]:
                # don't change the text if we're displaying an error message
                self.backFrame["text"] = textToDisplay

        return task.again

    def setErrorMessage(self, errText):
        """Tell the user something has gone wrong."""
        self.backFrame["text"] = errText

    def redownloadNews(self):
        """Get the new issue that came out while he was playing."""
        if self.redownloadingNews:
            self.notify.warning("averting potential crash redownloadNews called twice, just returning")
            return
        # I know it's info, it's important enough I feel to appear in the logs
        self.percentDownloaded = 0.0
        self.notify.info("starting redownloadNews")
        self.startRedownload = datetime.datetime.now()

        self.redownloadingNews =True
        self.addDownloadingTextTask()

        # Clean up the old issues and start new stuff downloading.
        for issue in self.issues:
            issue.destroy()
        self.issues = []
        self.curIssueIndex = 0
        self.strFilenames = None
        self.needsParseNews = True

        # Start by downloading the index file.
        self.newsUrl = self.getInGameNewsUrl()
        self.newsDir = Filename(self.findNewsDir())

        # Ensure self.newsDir exists and is a directory.
        Filename(self.newsDir + '/.').makeDir()

        http = HTTPClient.getGlobalPtr()
        self.url = self.newsUrl + self.NewsIndexFilename
        self.ch = http.makeChannel(True)
        self.ch.beginGetDocument(self.url)
        self.rf = Ramfile()
        self.ch.downloadToRam(self.rf)

        taskMgr.remove(self.RedownloadTaskName)
        taskMgr.add(self.downloadIndexTask, self.RedownloadTaskName)

    def downloadIndexTask(self, task):
        """ Get the initial index file from the HTTP server. """
        if self.ch.run():
            return task.cont

        if not self.ch.isValid():
            self.notify.warning("Unable to download %s" % (self.url))
            self.redownloadingNews = False
            return task.done

        # OK, now we've got the list of files hosted by the server.
        # Parse the list.
        self.newsFiles = []
        filename = self.rf.readline()
        while filename:
            filename = filename.strip()
            if filename:
                self.newsFiles.append(filename)
            filename = self.rf.readline()
        del self.rf

        self.newsFiles.sort()
        self.notify.info("Server lists %s news files" % (len(self.newsFiles)))

        # Now see if we already have copies of these files we
        # downloaded previously.
        self.readNewsCache()

        # Clean up any unexpected files in this directory--they might
        # be old news files, or partial failed downloads from before.
        for basename in os.listdir(self.newsDir.toOsSpecific()):
            if basename != self.CacheIndexFilename and basename not in self.newsCache:
                junk = Filename(self.newsDir, basename)
                self.notify.info("Removing %s" % (junk))
                junk.unlink()

        # And start downloading the files.
        self.nextNewsFile = 0
        return self.downloadNextFile(task)

    def downloadNextFile(self, task):
        """ Starts the next news file downloading from the HTTP
        server. """

        if self.nextNewsFile >= len(self.newsFiles):
            # Hey, we're done!
            self.notify.info("Done downloading news.")
            self.percentDownloaded = 1
            
            del self.newsFiles
            del self.nextNewsFile
            del self.newsUrl
            del self.newsDir
            del self.ch
            del self.url
            if hasattr(self,'filename'):
                del self.filename
            self.redownloadingNews = False

            if self.active:
                # If we're looking at the page now, go ahead and load it.
                self.parseNewsContent()

            return task.done

        self.percentDownloaded = float(self.nextNewsFile) / float(len(self.newsFiles))
        
        # Get the next file on the list.
        self.filename = self.newsFiles[self.nextNewsFile]
        self.nextNewsFile += 1
        self.url = self.newsUrl + self.filename

        localFilename = Filename(self.newsDir, self.filename)
        doc = DocumentSpec(self.url)
        if self.filename in self.newsCache:
            # We have already downloaded this file.  Ask the
            # server to give us another copy only if the server's
            # copy is newer.
            size, date = self.newsCache[self.filename]
            if date and localFilename.exists() and (size == 0 or localFilename.getFileSize() == size):
                doc.setDate(date)
                doc.setRequestMode(doc.RMNewer)
        
        self.ch.beginGetDocument(doc)
        self.ch.downloadToFile(localFilename)

        taskMgr.remove(self.RedownloadTaskName)
        taskMgr.add(self.downloadCurrentFileTask, self.RedownloadTaskName)

    def downloadCurrentFileTask(self, task):
        """ Continues downloading the URL in self.url and self.filename. """

        if self.ch.run():
            return task.cont

        if self.ch.getStatusCode() == 304:
            # This file is still cached from before.  We don't need to
            # download it again.  Move on to the next file.
            self.notify.info("already cached: %s" % (self.filename))
            return self.downloadNextFile(task)

        localFilename = Filename(self.newsDir, self.filename)

        if not self.ch.isValid():
            self.notify.warning("Unable to download %s" % (self.url))
            localFilename.unlink()

            if self.filename in self.newsCache:
                del self.newsCache[self.filename]
                self.saveNewsCache()

            # Might as well see if we can get the next file.
            return self.downloadNextFile(task)

        # Successfully downloaded.
        self.notify.info("downloaded %s" % (self.filename))

        # The HTTP "Entity Tag" appears to be useless with our CDN:
        # different CDN servers will serve up different etag values
        # for the same file.  We rely on file size and date instead.
        
        size = self.ch.getFileSize()
        doc = self.ch.getDocumentSpec()
        date = ''
        if doc.hasDate():
            date = doc.getDate().getString()

        self.newsCache[self.filename] = (size, date)
        self.saveNewsCache()

        # Continue downloading files.
        return self.downloadNextFile(task)

    def readNewsCache(self):
        """ Reads cache_index.txt into self.newsCache. """
        
        cacheIndexFilename = Filename(self.newsDir, self.CacheIndexFilename)
        self.newsCache = {}
        if cacheIndexFilename.isRegularFile():
            file = open(cacheIndexFilename.toOsSpecific(), 'r')
            for line in file.readlines():
                line = line.strip()
                keywords = line.split('\t')
                if len(keywords) == 3:
                    filename, size, date = keywords
                    if filename in self.newsFiles:
                        try:
                            size = int(size)
                        except ValueError:
                            size = 0
                        self.newsCache[filename] = (size, date)

    def saveNewsCache(self):
        """ Saves self.newsCache to cache_index.txt """
        cacheIndexFilename = Filename(self.newsDir, self.CacheIndexFilename)

        file = open(cacheIndexFilename.toOsSpecific(), 'w')
        for filename, (size, date) in self.newsCache.items():
            print >> file, '%s\t%s\t%s' % (filename, size, date)
        
    def handleNewIssueOut(self):
        """Handle getting this newIssueOut message."""
        # we will get this immediately after DistributedInGameNewsManager gets created
        # we will get this again when a new issue comes out while we are playing
        if hasattr(self,"createdTime") and \
           base.cr.inGameNewsMgr.getLatestIssue()  < self.createdTime:
            self.createdTime =  base.cr.inGameNewsMgr.getLatestIssue()
        else:
            # we got a new issue while playing the game
            if self.NewsOverHttp and not self.redownloadingNews:
                # let's not abruptly yank the page if he's reading the news
                if not self.active:
                    self.redownloadNews()
            pass

    def getInGameNewsUrl(self):
        """Get the appropriate URL to use if we are in test, qa, or live."""
        # First if all else fails, we hard code the live news url
        result = base.config.GetString("fallback-news-url", "http://cdn.toontown.disney.go.com/toontown/en/gamenews/")
        # next check if we have an override, say they want to url to point to a file in their harddisk
        override = base.config.GetString("in-game-news-url", "")
        if override:
            self.notify.info("got an override url,  using %s for in game news" % override)
            result = override
        else:
            try:
                launcherUrl = base.launcher.getValue("GAME_IN_GAME_NEWS_URL", "")
                if launcherUrl:                    
                    result = launcherUrl
                    self.notify.info("got GAME_IN_GAME_NEWS_URL from launcher using %s" % result)
                else:
                    self.notify.info("blank GAME_IN_GAME_NEWS_URL from launcher, using %s" % result)
                    
            except:
                self.notify.warning("got exception getting GAME_IN_GAME_NEWS_URL from launcher, using %s" % result)
        return result
