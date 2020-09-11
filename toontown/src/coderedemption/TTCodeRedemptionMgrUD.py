from direct.distributed.DistributedObjectGlobalUD import DistributedObjectGlobalUD
from direct.directnotify.DirectNotifyGlobal import directNotify
from direct.http.WebRequest import WebRequestDispatcher
from direct.showbase import ElementTree as ET
from direct.showbase.HTMLTree import HTMLTree
from direct.showbase.PythonUtil import unescapeHtmlString as uhs
from direct.showbase.PythonUtil import str2elements
from direct.http import recaptcha
from direct.task import Task
from otp.distributed import OtpDoGlobals
from toontown.catalog import CatalogItemTypes
from toontown.coderedemption.TTCodeRedemptionDB import TTCodeRedemptionDBTester, TTCodeRedemptionDB
from toontown.coderedemption.TTCodeDict import TTCodeDict
from toontown.coderedemption import TTCodeRedemptionConsts
from toontown.coderedemption import TTCodeRedemptionSpamDetector
from toontown.rpc.AwardManagerUD import AwardManagerUD
from toontown.rpc import AwardManagerConsts
from toontown.uberdog import PartiesUdConfig
from StringIO import StringIO
import datetime
import random
import socket
import string
import re

SE = ET.SubElement

class FormErrors:
    class Null:
        pass

    def __init__(self):
        self._item2errs = {}

    def isEmpty(self, item=Null):
        if item is FormErrors.Null:
            return len(self._item2errs) == 0
        return len(self._item2errs.get(item, [])) == 0

    def get(self, item):
        return set(self._item2errs.get(item, []))

    def add(self, item, error):
        if item not in self._item2errs:
            self._item2errs[item] = set()
        self._item2errs[item].add(error)

class TTCodeRedemptionMgrUD(DistributedObjectGlobalUD):
    notify = directNotify.newCategory('TTCodeRedemptionMgrUD')

    Ops = Enum('menu, create, doCreate, view, doView, modify, doModify, delete, doDelete, lookup, doLookup, redeem, doRedeem')

    MaxLotSize = 10000000

    ReCAPTCHADomainName = 'localhost'
    ReCAPTCHAPublicKey = '6Ld8gwkAAAAAALtgzi9Y0q8DqflAK7DwfeiKfTGN'
    ReCAPTCHAPrivateKey = '6Ld8gwkAAAAAAEtBhL2sblZNm4SFy3B8g-6PDIUI'

    Disabled = config.GetBool('disable-code-redemption', 0)

    class GenericErrors:
        EmptyInput = 'This field is required'
        InvalidNumber = 'Please enter a number'
        FieldsMustMatch = 'This field must match the previous field'

    class CreateErrors:
        InvalidCharInLotName = 'Name can only contain lowercase ASCII letters, numbers, and underscores'
        UsedLotName = 'Lot name is already in use'

    class CodeErrors:
        InvalidCharInCode = 'Code can only contain alphanumeric characters and dashes'
        InvalidCode = 'Invalid code'
        MustContainManualChar = ('Code must contain at least one of the following: %s' %
                                 TTCodeDict.ManualOnlyCharacters)
        CodeAlreadyExists = 'Code already exists'
        CodeTooLong = 'Code must be %s characters or less' % TTCodeRedemptionConsts.MaxCustomCodeLen

    class RedeemErrors:
        InvalidCharInAvId = 'AvId can only contain numbers'
        CodeIsExpired = 'Code is expired'
        CodeAlreadyRedeemed = 'Code has already been redeemed'
        AwardCouldntBeGiven = 'Award could not be given, code not processed'

    if __dev__:
        TestRedemptionSpamAvIdMin = 6
        TestRedemptionSpamAvIdMax = 9999999
        TestRedemptions = (
            # non-ascii
            ('\xff', (TTCodeRedemptionConsts.RedeemErrors.CodeDoesntExist, 0)),
            # invalid characters
            ('.', (TTCodeRedemptionConsts.RedeemErrors.CodeDoesntExist, 0)),
            )
        DisabledTestRedemptions = (
            ('HWF', (TTCodeRedemptionConsts.RedeemErrors.SystemUnavailable, 0)),
            (',', (TTCodeRedemptionConsts.RedeemErrors.SystemUnavailable, 0)),
            )
        # spam detection
        TestSpamRedemptions = (([('!!!', (TTCodeRedemptionConsts.RedeemErrors.CodeDoesntExist, 0)),] * TTCodeRedemptionSpamDetector.Settings.DetectThreshold) +
                               [('!!!', (TTCodeRedemptionConsts.RedeemErrors.TooManyAttempts, 0)),]
                               )
    
    def __init__(self, air):
        DistributedObjectGlobalUD.__init__(self, air)

        self.HTTPListenPort = uber.codeRedemptionMgrHTTPListenPort

        self.webDispatcher = WebRequestDispatcher()
        self.webDispatcher.landingPage.setTitle("TTCodeRedemptionMgr")
        self.webDispatcher.landingPage.setDescription("TTCodeRedemptionMgr enables generation and retrieval of reward codes.")
        self.webDispatcher.registerGETHandler(
            "codeManagement",self.handleHTTPcodeManagement,returnsResponse=False,autoSkin=True)
        self.webDispatcher.landingPage.addTab("CodeMgmt","/codeManagement")
        self.webDispatcher.listenOnPort(self.HTTPListenPort)

        self.DBuser = uber.config.GetString("mysql-user", PartiesUdConfig.ttDbUser)
        self.DBpasswd = uber.config.GetString("mysql-passwd", PartiesUdConfig.ttDbPasswd)

        self.DBhost = uber.config.GetString("tt-code-db-host", uber.mysqlhost)
        self.DBport = uber.config.GetInt("tt-code-db-port", PartiesUdConfig.ttDbPort)
        self.DBname = choice(uber.crDbName != '', uber.crDbName, TTCodeRedemptionConsts.DefaultDbName)

        self._rewardSerialNumGen = SerialNumGen()
        self._rewardContextTable = {}

        self._redeemContextGen = SerialNumGen()
        self._redeemContext2session = {}

        self._db = TTCodeRedemptionDB(self.air, self.DBhost, self.DBport, self.DBuser, self.DBpasswd, self.DBname)

        if __debug__:
            self._db.runTests()

        self.air.setConnectionName("TTCodeRedemptionMgr")
        self.air.setConnectionURL("http://%s:%s/" % (socket.gethostbyname(socket.gethostname()),self.HTTPListenPort))

        self._createLotSerialGen = SerialNumGen()
        self._createLotId2task = {}

        self._randSampleContext2callback = {}
        self._randSampleContextGen = SerialMaskedGen((1L<<32)-1)

        self._spamDetector = TTCodeRedemptionSpamDetector.TTCodeRedemptionSpamDetector()
        self._wantSpamDetect = config.GetBool('want-code-redemption-spam-detect', 1)

        if __dev__:
            self._testAvId = random.randrange(self.TestRedemptionSpamAvIdMin, self.TestRedemptionSpamAvIdMax)
            self._avId2table = {self._testAvId: self.TestRedemptions,
                                }
            self._disabledAvId2table = {self._testAvId: self.DisabledTestRedemptions,
                                        }
            if self._wantSpamDetect:
                self._spamAvId = random.randrange(self.TestRedemptionSpamAvIdMin, self.TestRedemptionSpamAvIdMax)
                self._avId2table[self._spamAvId] = self.TestSpamRedemptions

    if __dev__:
        def _sendTestRedemptions(self):
            for avId in self._avId2table.iterkeys():
                redemptions = self._avId2table[avId]
                for i in xrange(len(redemptions)):
                    redemption = redemptions[i]
                    code, results = redemption
                    self.redeemCodeAiToUd(0, 0, i, code, avId, self._resolveTestRedemption)

        def _sendDisabledTestRedemptions(self):
            saved = TTCodeRedemptionMgrUD.Disabled
            TTCodeRedemptionMgrUD.Disabled = True
            for avId in self._disabledAvId2table.iterkeys():
                redemptions = self._disabledAvId2table[avId]
                for i in xrange(len(redemptions)):
                    redemption = redemptions[i]
                    code, results = redemption
                    self.redeemCodeAiToUd(0, 0, i, code, avId, self._resolveDisabledTestRedemption)
            TTCodeRedemptionMgrUD.Disabled = saved

        def _resolveTestRedemption(self, serial, context, avId, result, awardMgrResult):
            if avId in self._avId2table:
                redemptions = self._avId2table.get(avId)
                redemption = redemptions[context]
                code, results = redemption
                assert result == results[0]
                assert awardMgrResult == results[1]

        def _resolveDisabledTestRedemption(self, serial, context, avId, result, awardMgrResult):
            if avId in self._disabledAvId2table:
                redemptions = self._disabledAvId2table.get(avId)
                redemption = redemptions[context]
                code, results = redemption
                assert result == results[0]
                assert awardMgrResult == results[1]

    def announceGenerate(self):
        """Start accepting http requests."""
        assert self.notify.debugCall()
        DistributedObjectGlobalUD.announceGenerate(self)
        self.webDispatcher.startCheckingIncomingHTTP()
        if __dev__ and TTCodeRedemptionDB.DoSelfTest:
            if not self.Disabled:
                self._sendTestRedemptions()
            self._sendDisabledTestRedemptions()

    def delete(self):
        for task in self._createLotId2task.values():
            self.removeTask(task)
        self._createLotId2task = {}

    def _reply(self, page, replyTo):
        # everything is already under the landing page's body tag
        """
        fileStr = StringIO()
        page.write(fileStr)
        replyTo.respond(fileStr.getvalue())
        """
        replyTo.respond('')

    def _addErrorsCell(self, row, errors, fieldName):
        errorSet = errors.get(fieldName)
        if len(errorSet):
            errorCell = SE(row, 'td')
            errorsTable = SE(errorCell, 'table')
            for error in errorSet:
                row = SE(errorsTable, 'tr')
                data = SE(row, 'td')
                data.set('style', 'color:red')
                dataBold = SE(data, 'b')
                # allow __str__ overload
                dataBold.text = str(error)

    def _addRecaptcha(self, form, errors):
        rError = None
        rErrors = errors.get('recaptcha')
        if len(rErrors):
            rError = list(rErrors)[0]
        ieNotice = ET.Element('b')
        ieNotice.text = 'NOTE: doesn\'t work with IE. Please use FireFox/Google Chrome/Safari/etc.'
        form.append(ieNotice)
        cError = None
        cErrors = errors.get('recaptchaCustom')
        if len(cErrors):
            cError = list(cErrors)[0]
        if cError:
            brk = ET.Element('br')
            form.append(brk)
            crNotice = ET.Element('b')
            crNotice.set('style', 'color:red')
            crNotice.text = '\n' + cError
            form.append(crNotice)
        recaptchaHTML = recaptcha.displayhtml(self.ReCAPTCHAPublicKey, use_ssl=True, error=rError)
        for el in str2elements(recaptchaHTML):
            form.append(el)
        SE(form, 'br')

    def _addExpirationControls(self, table, values, yearName, monthName, dayName):
        expDateRow = SE(table, 'tr')

        edDescCell = SE(expDateRow, 'td')
        edDescCell.text = 'Expiration date'

        edInputCell = SE(expDateRow, 'td')
        edYearInput = SE(edInputCell, 'select', name=yearName)
        edMonthInput = SE(edInputCell, 'select', name=monthName)
        edDayInput = SE(edInputCell, 'select', name=dayName)

        thisYear = datetime.date.today().year
        for i in xrange(thisYear, thisYear+100):
            option = SE(edYearInput, 'option', value=str(i))
            option.text = str(i)
            if values.get('expYear') == str(i):
                option.set('selected', 'selected')
        for i, name in ((1, 'Jan'), (2, 'Feb'), (3, 'Mar'), (4, 'Apr'), (5, 'May'), (6, 'Jun'),
                        (7, 'Jul'), (8, 'Aug'), (9, 'Sep'), (10, 'Oct'), (11, 'Nov'), (12, 'Dec'), ):
            option = SE(edMonthInput, 'option', value=str(i))
            option.text = '%02i: %s' % (i, name)
            if values.get('expMonth') == str(i):
                option.set('selected', 'selected')
        for i in xrange(1, 31+1):
            option = SE(edDayInput, 'option', value=str(i))
            option.text = str(i)
            if values.get('expDay') == str(i):
                option.set('selected', 'selected')

        return expDateRow

    def _addSubmitButtonDisable(self, headTag, bodyTag, parentTag, submitButton, formName, ):
        buttonName = submitButton.get('name')
        assert buttonName is not None
        normalText = submitButton.get('value')
        assert normalText is not None
        submitScript = ET.Element('script', type='text/javascript')
        enableSubmitFuncName = 'enableSubmitButton'
        submitScript.text = """
        function %(funcName)s(enable) {
          var submitButton = document.%(formName)s.%(buttonName)s;
          if (enable) {
            submitButton.disabled = false;
            submitButton.value = '%(normalText)s';
          } else {
            submitButton.disabled = true;
            submitButton.value = 'Please wait...';
          }
        }
        function resetSubmitButton() {
          %(funcName)s(true);
        }
        """ % ({
            'funcName': enableSubmitFuncName,
            'formName': formName,
            'buttonName': buttonName,
            'normalText': normalText,
            })
        # put the javascript in the HEAD tag
        headTag.append(submitScript)
        # disable the submit button on click
        submitButton.set('onclick',
                         '%(funcName)s(false);' % ({
            'funcName': enableSubmitFuncName,
            }))
        # enable the submit button on page load
        SE(parentTag, 'script', type='text/javascript', text='%s(true);' % (enableSubmitFuncName, ))
        bodyTag.set('onUnload', 'resetSubmitButton();'); 

    def _isValidManualCodeRewardType(self, rewardType):
        isPermanent = rewardType not in CatalogItemTypes.NonPermanentItemTypes
        multipleAllowed = CatalogItemTypes.CatalogItemType2multipleAllowed[rewardType]
        return (isPermanent and (not multipleAllowed))

    def _doCreateForm(self, parent, body, replyTo, values=None, errors=None):
        # values is dict of element->string
        if values is None:
            values = {}
        # errors is sparse dict of sets of FormErrors
        if errors is None:
            errors = FormErrors()

        formName = 'createForm'
        mainForm = SE(parent, 'form', name=formName, action='codeManagement', method='GET')
        hiddenOp = SE(mainForm, 'input', type='hidden', name='op', value='doCreate')

        formTable = SE(mainForm, 'table')

        # code lot name
        lotNameRow = SE(formTable, 'tr')

        lnDescCell = SE(lotNameRow, 'td')
        lnDescCell.text = 'Name of code lot'

        lnInputCell = SE(lotNameRow, 'td')

        lotName = SE(lnInputCell, 'input', type='text', name='lotName')
        if 'lotName' in values:
            lotName.set('value', values['lotName'])

        self._addErrorsCell(lotNameRow, errors, 'lotName')

        # code type
        codeTypeRow = SE(formTable, 'tr')

        ctDescCell = SE(codeTypeRow, 'td')
        ctDescCell.text = 'Code type'

        codeTypeDropdownCell = SE(codeTypeRow, 'td')

        codeTypeName = 'codeType'
        codeTypeDropdown = SE(codeTypeDropdownCell, 'select', name=codeTypeName)

        codeTypes = [('manual', 'Manually-created code, many toons use same code'), ]
        if config.GetBool('want-unique-code-generation', 0):
            codeTypes.append(('auto', 'Auto-generated codes, one redemption per code'))

        for formVal, desc in codeTypes:
            option = SE(codeTypeDropdown, 'option', value=formVal)
            option.text = desc
            if values.get('codeType') == formVal:
                option.set('selected', 'selected')

        self._addErrorsCell(codeTypeRow, errors, 'codeType')

        # number of codes
        numCodesRow = SE(formTable, 'tr')

        ncDescCell = SE(numCodesRow, 'td')
        ncDescCell.text = 'Number of codes'

        ncInputCell = SE(numCodesRow, 'td')

        numCodesName = 'numCodes'
        numCodes = SE(ncInputCell, 'input', type='text', name=numCodesName)
        if 'numCodes' in values:
            numCodes.set('value', values['numCodes'])

        self._addErrorsCell(numCodesRow, errors, 'numCodes')

        # number of codes 2 (verify)
        numCodes2Row = SE(formTable, 'tr')

        nc2DescCell = SE(numCodes2Row, 'td')
        nc2DescCell.text = 'Number of codes (again)'

        nc2InputCell = SE(numCodes2Row, 'td')

        numCodes2Name = 'numCodes2'
        numCodes2 = SE(nc2InputCell, 'input', type='text', name=numCodes2Name)
        if 'numCodes2' in values:
            numCodes2.set('value', values['numCodes2'])

        self._addErrorsCell(numCodes2Row, errors, 'numCodes2')

        # manual code
        manualCodeRow = SE(formTable, 'tr')

        mcDescCell = SE(manualCodeRow, 'td')
        mcDescCell.text = 'Manual code'

        mcInputCell = SE(manualCodeRow, 'td')

        manualCodeName = 'manualCode'
        manualCode = SE(mcInputCell, 'input', type='text', name=manualCodeName)
        if 'manualCode' in values:
            manualCode.set('value', values['manualCode'])

        self._addErrorsCell(manualCodeRow, errors, 'manualCode')

        # manual code 2
        manualCode2Row = SE(formTable, 'tr')

        mc2DescCell = SE(manualCode2Row, 'td')
        mc2DescCell.text = 'Manual code (again)'

        mc2InputCell = SE(manualCode2Row, 'td')

        manualCode2Name = 'manualCode2'
        manualCode2 = SE(mc2InputCell, 'input', type='text', name=manualCode2Name)
        if 'manualCode2' in values:
            manualCode2.set('value', values['manualCode2'])

        self._addErrorsCell(manualCode2Row, errors, 'manualCode2')

        # reward type
        awardChoices = AwardManagerUD.getReversedAwardChoices()

        rewardTypeRow = SE(formTable, 'tr')

        rtDescCell = SE(rewardTypeRow, 'td')
        rtDescCell.text = 'Reward type'

        rtChoiceCell = SE(rewardTypeRow, 'td')

        rtSelectName = 'rewardType'
        rtChoice = SE(rtChoiceCell, 'select', name=rtSelectName)

        rewardTypes = awardChoices.keys()
        rewardTypes.sort()
        manualRewardTypes = []
        for rewardType in rewardTypes:
            if self._isValidManualCodeRewardType(rewardType):
                manualRewardTypes.append(rewardType)

        """ this is done by the javascript method defined below that handles code type changes
        for rewardType in rewardTypes:
            option = SE(rtChoice, 'option', value=str(rewardType))
            option.text = AwardManagerUD.getAwardTypeName(rewardType)
            if values.get('rewardType') == str(rewardType):
                option.set('selected', 'selected')
                """

        self._addErrorsCell(rewardTypeRow, errors, 'rewardType')

        # add javascript to change the interface based on code generation method
        # (number of codes or manual code string)
        genMethodScript = ET.Element('script', type='text/javascript')
        genMethodChangeFuncName = 'handleGenerationMethodChange'
        setRewardTypesCode = ''
        for codeType in ('auto', 'manual', ):
            setRewardTypesCode += 'if (genMethod.value == "%s") {' % codeType
            if (codeType == 'auto'):
                rts = rewardTypes
            else:
                rts = manualRewardTypes
            for rewardType in rts:
                value = str(rewardType)
                text = AwardManagerUD.getAwardTypeName(rewardType)
                setRewardTypesCode += ('rewardType.options[rewardType.options.length] = new Option('
                                       '"%s", "%s");' % (text, value))
            setRewardTypesCode += '}'
        genMethodScript.text = """
        function %(genMethodChangeFuncName)s() {
          var genMethod = document.%(formName)s.%(genMethodName)s;
          var numCodes = document.%(formName)s.%(numCodesName)s;
          var numCodes2 = document.%(formName)s.%(numCodes2Name)s;
          var manualCode = document.%(formName)s.%(manualCodeName)s;
          var manualCode2 = document.%(formName)s.%(manualCode2Name)s;
          var rewardType = document.%(formName)s.%(rewardTypeName)s;
          rewardType.options.length = 0;
          if (genMethod.value == 'auto') {
            numCodes.disabled = false;
            numCodes2.disabled = false;
            manualCode.disabled = true;
            manualCode2.disabled = true;
          } else {
            numCodes.disabled = true;
            numCodes2.disabled = true;
            manualCode.disabled = false;
            manualCode2.disabled = false;
          }
          %(setRewardTypes)s
          handleRewardTypeChange();
        }
        """ % ({
            'genMethodChangeFuncName': genMethodChangeFuncName,
            'formName': formName,
            'genMethodName': codeTypeName,
            'numCodesName': numCodesName,
            'numCodes2Name': numCodes2Name,
            'manualCodeName': manualCodeName,
            'manualCode2Name': manualCode2Name,
            'rewardTypeName': rtSelectName,
            'setRewardTypes': setRewardTypesCode,
            })
        # put the javascript inside the HEAD tag
        replyTo.getHeadTag().append(genMethodScript)
        # hook up the onchange method so that the interface changes when a generation
        # method is selected
        codeTypeDropdown.set('onchange', '%s();' % genMethodChangeFuncName)
        # adjust the interface properly on page load
        rewardTypeSelectIndex = 0
        if 'codeType' in values and 'rewardType' in values:
            if (values.get('codeType') == 'auto'):
                rts = rewardTypes
            else:
                rts = manualRewardTypes
            rewardTypeSelectIndex = rts.index(int(values.get('rewardType')))
        initGenMethodOptions = SE(parent, 'script', type='text/javascript')
        initGenMethodOptions.text = '%(codeTypeChangeFunc)s(); document.%(formName)s.%(rewardTypeSelectName)s.selectedIndex = %(index)s;' % {
            'codeTypeChangeFunc': genMethodChangeFuncName,
            'formName': formName,
            'rewardTypeSelectName': rtSelectName,
            'index': rewardTypeSelectIndex,
            }

        # reward itemId
        rewardItemRow = SE(formTable, 'tr')

        riDescCell = SE(rewardItemRow, 'td')
        riDescCell.text = 'Reward item'

        riChoiceCell = SE(rewardItemRow, 'td')

        riSelectName = 'rewardItemId'
        riChoice = SE(riChoiceCell, 'select', name=riSelectName)

        # this selection is filled in automatically based on the reward type selection
        """
        id2item = awardChoices[1]
        itemIds = id2item.keys()
        itemIds.sort()
        for itemId in itemIds:
            option = SE(riChoice, 'option', value=str(itemId))
            option.text = id2item[itemId]
            if values.get('rewardItemId') == str(itemId):
                option.set('selected', 'selected')
                """

        self._addErrorsCell(rewardItemRow, errors, 'rewardItemId')

        # add javascript to change the reward item list based on the reward type selection
        rewardTypeScript = ET.Element('script', type='text/javascript')
        rewardTypeChangeFuncName = 'handleRewardTypeChange'
        setRewardItemsCode = ''
        for rewardType in rewardTypes:
            setRewardItemsCode += 'if (typeValue == "%s") {' % rewardType
            id2item = awardChoices[rewardType]
            itemIds = id2item.keys()
            itemIds.sort()
            for itemId in itemIds:
                value = str(itemId)
                text = id2item[itemId]
                setRewardItemsCode += ('itemSel.options[itemSel.options.length] = new Option('
                                       '"%s", "%s");' % (text, value))
            setRewardItemsCode += '}'
        rewardTypeScript.text = """
        function %(rewardChangeFuncName)s() {
          var typeSel = document.%(formName)s.%(rewardTypeSelectName)s;
          var itemSel = document.%(formName)s.%(rewardItemSelectName)s;
          var typeValue = typeSel[typeSel.selectedIndex].value;
          itemSel.options.length = 0;
          %(setRewardItems)s
        }
        """ % ({
            'rewardChangeFuncName': rewardTypeChangeFuncName,
            'formName': formName,
            'rewardTypeSelectName': rtSelectName,
            'rewardItemSelectName': riSelectName,
            'setRewardItems': setRewardItemsCode,
            })
        # put the javascript inside the HEAD tag
        replyTo.getHeadTag().append(rewardTypeScript)
        # load the correct items into the reward item selection when the reward type
        # selection is changed
        rtChoice.set('onchange',
                     '%(rewardChangeFuncName)s();' % ({
            'rewardChangeFuncName': rewardTypeChangeFuncName,
            }))
        # load the correct items into the reward item selection on page load
        rewardItemSelectIndex = 0
        if 'rewardType' in values and 'rewardItemId' in values:
            id2item = awardChoices[int(values.rewardType)]
            itemIds = id2item.keys()
            itemIds.sort()
            rewardItemSelectIndex = itemIds.index(int(values.rewardItemId))
        initRewardItems = SE(parent, 'script', type='text/javascript')
        initRewardItems.text = '%(rewardChangeFuncName)s(); document.%(formName)s.%(rewardItemSelectName)s.selectedIndex = %(index)s;' % (
            {'rewardChangeFuncName': rewardTypeChangeFuncName,
             'formName': formName,
             'rewardItemSelectName': riSelectName,
             'index': rewardItemSelectIndex,
             })

        # has expiration date
        hasExpRow = SE(formTable, 'tr')

        heDescCell = SE(hasExpRow, 'td')
        heDescCell.text = 'Has expiration date'

        heInputCell = SE(hasExpRow, 'td')
        hasExpirationName = 'hasExpiration'
        heInput = SE(heInputCell, 'select', name=hasExpirationName)
        
        for formVal, desc in (('yes', 'Yes'),
                              ('no', 'No'),
                              ):
            option = SE(heInput, 'option', value=formVal)
            option.text = desc
            if 'hasExpiration' not in values:
                if formVal == 'no':
                    option.set('selected', 'selected')
            elif values.get('hasExpiration') == formVal:
                option.set('selected', 'selected')

        # expiration date
        yearName = 'expYear'
        monthName = 'expMonth'
        dayName = 'expDay'
        expDateRow = self._addExpirationControls(formTable, values, yearName, monthName, dayName)
        self._addErrorsCell(expDateRow, errors, 'expiration')

        # add javascript to disable the date entry if expiration date is turned off
        dateScript = ET.Element('script', type='text/javascript')
        dateEnableFuncName = 'enableDateEntry'
        dateScript.text = """
        function %(funcName)s() {
          var disabled = false;
          if (document.%(formName)s.%(hasExpName)s.value == 'no') {
            disabled = true;
          }
          document.%(formName)s.%(yearName)s.disabled = disabled;
          document.%(formName)s.%(monthName)s.disabled = disabled;
          document.%(formName)s.%(dayName)s.disabled = disabled;
        }
        """ % ({
            'funcName': dateEnableFuncName,
            'formName': formName,
            'hasExpName': hasExpirationName,
            'yearName': yearName,
            'monthName': monthName,
            'dayName': dayName,
            })
        # put the javascript in the HEAD tag
        replyTo.getHeadTag().append(dateScript)
        # handle changes to the expiration enable field
        heInput.set('onchange',
                    '%(funcName)s();' % ({
            'funcName': dateEnableFuncName,
            }))
        # set the correct date enable state on page load
        initDate = SE(parent, 'script', type='text/javascript')
        initDate.text = '%(funcName)s();' % ({
            'funcName': dateEnableFuncName,
            })

        SE(mainForm, 'br')

        self._addRecaptcha(mainForm, errors)

        buttonName = 'submitButton'
        submitText = 'Create Code Lot'
        submitButton = SE(mainForm, 'input', name=buttonName, type='submit', value=submitText)
        self._addSubmitButtonDisable(replyTo.getHeadTag(), replyTo.getBodyTag(), parent,
                                     submitButton, formName, )

    def _startCreateLotTask(self, replyTo, page, body, values, manualCode, numCodes, manualCodeStr, expDate):
        assert self.notify.debugCall()
        if manualCode:
            self._db.createManualLot(values.lotName, manualCodeStr, values.rewardType, values.rewardItemId,
                                     expirationDate=expDate)
            self._showCreateLotResults(replyTo, page, body, values)
        else:
            createLotId = self._createLotSerialGen.next()
            gen = self._db.createLot(self._requestRandomSamples, values.lotName, numCodes,
                                     values.rewardType, values.rewardItemId,
                                     expirationDate=expDate)
            t = self.addTask(self._createLotTask, '%s-createLot-%s' % (self.__class__.__name__, createLotId))
            t.createLotId = createLotId
            t.gen = gen
            t.replyTo = replyTo
            t.page = page
            t.body = body
            t.values = values
            self._createLotId2task[createLotId] = t

    def _createLotTask(self, task):
        for result in task.gen:
            break

        if result is True:
            self._showCreateLotResults(task.replyTo, task.page, task.body, task.values)
            del self._createLotId2task[task.createLotId]
            return Task.done

        return Task.cont

    def _showCreateLotResults(self, replyTo, page, body, values):
        assert self.notify.debugCall()
        self._doViewLot(values.lotName, body)
        self._reply(page, replyTo)

    def _requestRandomSamples(self, callback, numSamples):
        assert self.notify.debugCall()
        context = self._randSampleContextGen.next()
        self._randSampleContext2callback[context] = callback
        self.air.dispatchUpdateToGlobalDoId(
            "NonRepeatableRandomSourceUD", "getRandomSamples",
            OtpDoGlobals.OTP_DO_ID_TOONTOWN_NON_REPEATABLE_RANDOM_SOURCE,
            [self.doId, 'TTCodeRedemptionMgr', context, numSamples])

    def getRandomSamplesReply(self, context, samples):
        assert self.notify.debugCall()
        callback = self._randSampleContext2callback.pop(context)
        callback(samples)

    def _createCodeTable(self, parent, fieldRows, justCode=False, manual=False):
        internalFields = ('name','lot.lot_id','lot_id','size',
                          'reward.reward_id','reward_id',)
        nameTransform = {
            'av_id': 'redeemed.av_id',
            TTCodeRedemptionDB.RewardTypeFieldName: 'reward.category',
            TTCodeRedemptionDB.RewardItemIdFieldName: 'reward.item',
            }
        transAndField = []
        if justCode:
            transAndField.append(['code','code'])
        else:
            fieldSet = set()
            for row in fieldRows:
                for field in row:
                    if field not in fieldSet:
                        if field not in internalFields:
                            transAndField.append([nameTransform.get(field, field), field])
                            fieldSet.add(field)

        # sort by transformed name, keep track of original field name
        transAndField.sort()

        table = SE(parent, 'table')

        titleRow = SE(table, 'tr')
        for trans, field in transAndField:
            fieldTitle = SE(titleRow, 'th')
            fieldTitle.text = trans.upper()

        for row in fieldRows:
            tableRow = SE(table, 'tr')
            for trans, field in transAndField:
                if justCode:
                    value = row
                else:
                    value = row[field]
                tableData = SE(tableRow, 'td')
                if field == 'code':
                    # if the code is manually-entered, don't modify it to make it readable
                    # if the code row has a manual field, go by that,
                    # otherwise use the keyword arg to this method
                    if 'manual' in row:
                        isManual = row['manual'] == 'T'
                    else:
                        isManual = manual
                    if not isManual:
                        value = TTCodeDict.getReadableCode(value)
                else:
                    if trans == 'reward.category':
                        value = AwardManagerUD.getAwardTypeName(row[field])
                    if trans == 'reward.item':
                        typeId = int(row[TTCodeRedemptionDB.RewardTypeFieldName])
                        itemId = int(row[field])
                        value = AwardManagerUD.getAwardText(typeId, itemId);
                    if field in ('manual_code', 'redeemed'):
                        value = {'T': 'Yes',
                                 'F': 'No',
                                 }[row[field]]
                    value = str(value)
                tableData.text = value

    def _doViewForm(self, parent, replyTo, values=None, errors=None):
        formName = 'viewForm'
        mainForm = SE(parent, 'form', name=formName)
        mainForm.set('action', 'codeManagement')
        mainForm.set('method', 'GET')

        hiddenOp = SE(mainForm, 'input')
        hiddenOp.set('type', 'hidden')
        hiddenOp.set('name', 'op')
        hiddenOp.set('value', 'doView')

        lotNames = self._db.getLotNames()

        viewTable = SE(mainForm, 'table')

        lotNameRow = SE(viewTable, 'tr')

        lnDesc = SE(lotNameRow, 'td')
        lnDesc.text = 'Code lot'

        lnSelect = SE(lotNameRow, 'td')
        lotNameDropdown = SE(lnSelect, 'select')
        lotNameDropdown.set('name', 'lotName')
        for name in lotNames:
            lnOnePer = SE(lotNameDropdown, 'option')
            lnOnePer.set('value', name)
            lnOnePer.text = name

        filterRow = SE(viewTable, 'tr')

        frDesc = SE(filterRow, 'td')
        frDesc.text = 'Filter by'

        fSelect = SE(filterRow, 'td')
        filterDropdown = SE(fSelect, 'select')
        filterDropdown.set('name', 'filter')
        fElements = ((self._db.LotFilter.All, 'all codes'),
                     (self._db.LotFilter.Redeemable, 'redeemable codes'),
                     (self._db.LotFilter.NonRedeemable, 'non-redeemable codes'),
                     (self._db.LotFilter.Redeemed, 'redeemed codes'),
                     (self._db.LotFilter.Expired, 'expired codes'),
                     )
        for name, desc in fElements:
            fOption = SE(filterDropdown, 'option')
            fOption.set('value', name)
            fOption.text = desc

        showFieldsRow = SE(viewTable, 'tr')

        sfDesc = SE(showFieldsRow, 'td')
        sfDesc.text = 'Show fields'

        sfSelect = SE(showFieldsRow, 'td')
        sfDropdown = SE(sfSelect, 'select')
        sfDropdown.set('name', 'showFields')
        sfElements = (('codeOnly', 'code only'),
                      ('all', 'all fields'),
                      )
        for name, desc in sfElements:
            sfOption = SE(sfDropdown, 'option')
            sfOption.set('value', name)
            sfOption.text = desc

        SE(mainForm, 'br')

        submitButton = SE(mainForm, 'input', name='submitButton')
        submitButton.set('type', 'submit')
        submitButton.set('value', 'View Code Lot')
        self._addSubmitButtonDisable(replyTo.getHeadTag(), replyTo.getBodyTag(), parent,
                                     submitButton, formName, )

    def _doViewLot(self, lotName, body, justCode=None, filter=None):
        if justCode is None:
            justCode = True
        if filter is None:
            filter = self._db.LotFilter.All

        results = self._db.getCodesInLot(lotName, justCode, filter)

        manual = (lotName in self._db.getManualLotNames())

        tableTitle = SE(body, 'h1')
        tableTitle.text = 'Code Lot: %s%s, %s results' % (
            lotName, choice(filter == self._db.LotFilter.All, '', ' (%s)' % filter), len(results))

        self._createCodeTable(body, results, justCode=justCode, manual=manual)

    def _doModifyForm(self, parent, replyTo, values=None, errors=None):
        # values is dict of element->string
        if values is None:
            values = {}
        # errors is sparse dict of sets of FormErrors
        if errors is None:
            errors = FormErrors()

        formName = 'modifyForm'
        mainForm = SE(parent, 'form', name=formName)
        mainForm.set('action', 'codeManagement')
        mainForm.set('method', 'GET')

        hiddenOp = SE(mainForm, 'input')
        hiddenOp.set('type', 'hidden')
        hiddenOp.set('name', 'op')
        hiddenOp.set('value', 'doModify')

        modifyTable = SE(mainForm, 'table')

        modificationRow = SE(modifyTable, 'tr')

        mrDesc = SE(modificationRow, 'td')
        mrDesc.text = 'Modification'

        mSelect = SE(modificationRow, 'td')
        modificationDropdown = SE(mSelect, 'select')
        modificationDropdown.set('name', 'modification')
        fElements = (('expiration', 'Change expiration date'),
                     )
        for name, desc in fElements:
            fOption = SE(modificationDropdown, 'option')
            fOption.set('value', name)
            fOption.text = desc
            if 'modification' in values:
                if values.modification == name:
                    fOption.set('selected', 'selected')

        self._addErrorsCell(modificationRow, errors, 'modification')

        lotNameRow = SE(modifyTable, 'tr')

        lnDesc = SE(lotNameRow, 'td')
        lnDesc.text = 'Code lot'

        # TODO: change the lot filtering based on the modification selected
        lotNames = self._db.getExpirationLotNames()

        lnSelect = SE(lotNameRow, 'td')
        lotNameDropdown = SE(lnSelect, 'select')
        lotNameDropdown.set('name', 'lotName')
        for name in lotNames:
            lnOnePer = SE(lotNameDropdown, 'option')
            lnOnePer.set('value', name)
            lnOnePer.text = name
            if 'lotName' in values:
                if name == values.lotName:
                    lnOnePer.set('selected', 'selected')

        self._addErrorsCell(lotNameRow, errors, 'lotName')

        yearName = 'expYear'
        monthName = 'expMonth'
        dayName = 'expDay'
        expDateRow = self._addExpirationControls(modifyTable, values, yearName, monthName, dayName)

        self._addErrorsCell(expDateRow, errors, 'expiration')

        SE(mainForm, 'br')

        self._addRecaptcha(mainForm, errors)

        submitButton = SE(mainForm, 'input', name='submitButton')
        submitButton.set('type', 'submit')
        submitButton.set('value', 'Modify Code Lot')
        self._addSubmitButtonDisable(replyTo.getHeadTag(), replyTo.getBodyTag(), parent,
                                     submitButton, formName, )

    def _doModifyLot(self, parent, replyTo, page, values):
        if values.modification == 'expiration':
            exp = '%s-%02d-%02d' % (values.expYear, int(values.expMonth), int(values.expDay), )
            self._db.setExpiration(values.lotName, exp)
            resultHeading = SE(parent, 'h2')
            resultHeading.text = 'expiration date set to %s' % (exp, )

        self._doViewLot(values.lotName, parent, justCode=False)

    def _doDeleteForm(self, parent, replyTo, values=None, errors=None):
        if values is None:
            values = {}
        if errors is None:
            errors = FormErrors()
            
        formName = 'deleteForm'
        mainForm = SE(parent, 'form', name=formName)
        mainForm.set('action', 'codeManagement')
        mainForm.set('method', 'GET')

        hiddenOp = SE(mainForm, 'input')
        hiddenOp.set('type', 'hidden')
        hiddenOp.set('name', 'op')
        hiddenOp.set('value', 'doDelete')

        deleteTable = SE(mainForm, 'table')

        lotNames = self._db.getLotNames()

        lotNameRow = SE(deleteTable, 'tr')

        lnDesc = SE(lotNameRow, 'td')
        lnDesc.text = 'Code lot'

        lnSelect = SE(lotNameRow, 'td')
        lotNameDropdown = SE(lnSelect, 'select')
        lotNameDropdown.set('name', 'lotName')
        for name in lotNames:
            lnOnePer = SE(lotNameDropdown, 'option')
            lnOnePer.set('value', name)
            lnOnePer.text = name
            if 'lotName' in values:
                if name == values.lotName:
                    lnOnePer.set('selected', 'selected')

        self._addErrorsCell(lotNameRow, errors, 'lotName')

        lotName2Row = SE(deleteTable, 'tr')

        ln2Desc = SE(lotName2Row, 'td')
        ln2Desc.text = 'Code lot (again)'

        ln2Select = SE(lotName2Row, 'td')
        lotName2Dropdown = SE(ln2Select, 'select')
        lotName2Dropdown.set('name', 'lotName2')
        for name in (['',] + lotNames):
            lnOnePer = SE(lotName2Dropdown, 'option')
            lnOnePer.set('value', name)
            lnOnePer.text = name

        self._addErrorsCell(lotName2Row, errors, 'lotName2')

        SE(mainForm, 'br')

        self._addRecaptcha(mainForm, errors)

        submitButton = SE(mainForm, 'input', name='submitButton')
        submitButton.set('type', 'submit')
        submitButton.set('value', 'Delete Lot')
        self._addSubmitButtonDisable(replyTo.getHeadTag(), replyTo.getBodyTag(), parent,
                                     submitButton, formName, )

    def _doDelete(self, parent, replyTo, page, values):
        success = False
        preLotNames = self._db.getLotNames()
        if values.lotName in preLotNames:
            self._db.deleteLot(values.lotName)
            postLotNames = self._db.getLotNames()
            if values.lotName not in postLotNames:
                success = True
            
        resultHeading = SE(parent, 'h2')
        resultHeading.text = choice(success,
                                    'code lot %s deleted' % (values.lotName, ),
                                    'could not delete lot %s' % (values.lotName, ))
            
        SE(parent, 'br')

        backToMenu = SE(parent, 'a')
        backToMenu.set('href', '/codeManagement')
        backToMenu.text = 'Back to Menu'

    def _doLookupForm(self, parent, replyTo, values=None, errors=None):
        if values is None:
            values = {}
        if errors is None:
            errors = FormErrors()

        formName = 'lookupForm'
        mainForm = SE(parent, 'form', name=formName, action='codeManagement', method='GET')
        hiddenOp = SE(mainForm, 'input', type='hidden', name='op', value='doLookup')

        formTable = SE(mainForm, 'table')

        # mode selection (look up by X)
        modeRow = SE(formTable, 'tr')

        modeDescCell = SE(modeRow, 'td')
        modeDescCell.text = 'Lookup by'

        modeSelectCell = SE(modeRow, 'td')
        modeSelectName = 'mode'
        modeSelect = SE(modeSelectCell, 'select', name=modeSelectName)
        for name, value in (('Code', 'Code'), ('Redeemer AvId', 'AvId'), ):
            msOption = SE(modeSelect, 'option', value=value)
            msOption.text = name

        # code
        codeRow = SE(formTable, 'tr')

        codeDescCell = SE(codeRow, 'td')
        codeDescCell.text = 'Code'

        codeInputCell = SE(codeRow, 'td')
        codeInputName = 'code'
        codeInput = SE(codeInputCell, 'input', type='text', name=codeInputName)
        if 'code' in values:
            codeInput.set('value', values[codeInputName])

        self._addErrorsCell(codeRow, errors, codeInputName)

        # avId
        avIdRow = SE(formTable, 'tr')

        avIdDescCell = SE(avIdRow, 'td')
        avIdDescCell.text = 'Redeemer AvId'

        avIdInputCell = SE(avIdRow, 'td')
        avIdInputName = 'avId'
        avIdInput = SE(avIdInputCell, 'input', type='text', name=avIdInputName)
        if 'avId' in values:
            avIdInput.set('value', values[avIdInputName])

        self._addErrorsCell(avIdRow, errors, avIdInputName)

        # add javascript to disable/enable fields as appropriate
        enableScript = ET.Element('script', type='text/javascript')
        enableFuncName = 'enableEntries'
        enableScript.text = """
        function %(funcName)s() {
          var codeDisabled = false;
          var avIdDisabled = false;
          if (document.%(formName)s.%(modeSelectName)s.value == 'AvId') {
            codeDisabled = true;
          } else {
            avIdDisabled = true;
          }
          document.%(formName)s.%(codeInputName)s.disabled = codeDisabled;
          document.%(formName)s.%(avIdInputName)s.disabled = avIdDisabled;
        }
        """ % ({
            'funcName': enableFuncName,
            'formName': formName,
            'modeSelectName': modeSelectName,
            'codeInputName': codeInputName,
            'avIdInputName': avIdInputName,
            })
        # put the javascript in the HEAD tag
        replyTo.getHeadTag().append(enableScript)
        # handle changes to the mode selection
        modeSelect.set('onchange',
                       '%(funcName)s();' % ({
            'funcName': enableFuncName,
            }))
        # set the correct enable state on page load
        initMode = SE(parent, 'script', type='text/javascript')
        initMode.text = '%(funcName)s();' % ({
            'funcName': enableFuncName,
            })

        SE(mainForm, 'br')

        submitButton = SE(mainForm, 'input', name='submitButton')
        submitButton.set('type', 'submit')
        submitButton.set('value', 'Look Up Code(s)')
        self._addSubmitButtonDisable(replyTo.getHeadTag(), replyTo.getBodyTag(), parent,
                                     submitButton, formName, )

    def _doLookup(self, parent, avId=None, code=None):
        if avId is not None:
            codes = self._db.lookupCodesRedeemedByAvId(avId)
        else:
            codes = [code,]
        codeFields = []
        for cd in codes:
            codeFields.append(self._db.getCodeDetails(cd))

        if avId is not None:
            queryType = 'avId=%s' % avId
        else:
            queryType = 'code=%s' % code
        tableTitle = SE(parent, 'h1')
        tableTitle.text = 'Code Lookup: %s, %s results' % (queryType, len(codeFields))

        self._createCodeTable(parent, codeFields)

    def _doRedeemForm(self, parent, replyTo, values=None, errors=None):
        if values is None:
            values = {}
        if errors is None:
            errors = FormErrors()
            
        formName = 'redeemForm'
        mainForm = SE(parent, 'form', name=formName)
        mainForm.set('action', 'codeManagement')
        mainForm.set('method', 'GET')

        hiddenOp = SE(mainForm, 'input')
        hiddenOp.set('type', 'hidden')
        hiddenOp.set('name', 'op')
        hiddenOp.set('value', 'doRedeem')

        formTable = SE(mainForm, 'table')

        # code
        codeRow = SE(formTable, 'tr')

        codeDescCell = SE(codeRow, 'td')
        codeDescCell.text = 'Code'

        codeInputCell = SE(codeRow, 'td')
        codeInput = SE(codeInputCell, 'input')
        codeInput.set('type', 'text')
        codeInput.set('name', 'code')
        if 'code' in values:
            codeInput.set('value', values['code'])

        self._addErrorsCell(codeRow, errors, 'code')

        # avId
        avIdRow = SE(formTable, 'tr')

        avIdDescCell = SE(avIdRow, 'td')
        avIdDescCell.text = 'AvId'

        avIdInputCell = SE(avIdRow, 'td')
        avIdInput = SE(avIdInputCell, 'input')
        avIdInput.set('type', 'text')
        avIdInput.set('name', 'avId')
        if 'avId' in values:
            avIdInput.set('value', values['avId'])

        self._addErrorsCell(avIdRow, errors, 'avId')

        SE(mainForm, 'br')

        self._addRecaptcha(mainForm, errors)

        submitButton = SE(mainForm, 'input', name='submitButton')
        submitButton.set('type', 'submit')
        submitButton.set('value', 'Redeem Code')
        self._addSubmitButtonDisable(replyTo.getHeadTag(), replyTo.getBodyTag(), parent,
                                     submitButton, formName, )

    def _doRedeemResult(self, body, replyTo, avId, result, awardMgrResult, values, errors):
        RE = TTCodeRedemptionConsts.RedeemErrors
        errMap = {RE.CodeDoesntExist: self.CodeErrors.InvalidCode,
                  RE.CodeIsExpired: self.RedeemErrors.CodeIsExpired,
                  RE.CodeAlreadyRedeemed: self.RedeemErrors.CodeAlreadyRedeemed,
                  RE.AwardCouldntBeGiven: self.RedeemErrors.AwardCouldntBeGiven,
                  }
        if result in (errMap):
            errStr = errMap[result]
            if result == RE.AwardCouldntBeGiven:
                errStr += ': %s' % AwardManagerConsts.GiveAwardErrors.getString(awardMgrResult)
            errors.add('code', errStr)
            self._doRedeemForm(body, replyTo, values, errors)
        else:
            resultTable = SE(body, 'table')

            headingRow = SE(resultTable, 'tr')
            headingData = SE(headingRow, 'th')
            headingCenter = SE(headingData, 'center')
            headingCenter.text = 'Success!'

            rewardType, rewardId = self._db.getRewardFromCode(values.code)

            resultRow = SE(resultTable, 'tr')
            resultData = SE(resultRow, 'td')
            resultCenter = SE(resultData, 'center')
            resultCenter.text = ('Redeemed code %s for avId %s, awarded [%s | %s].' % (
                values.code, avId,
                AwardManagerUD.getAwardTypeName(rewardType),
                AwardManagerUD.getAwardText(rewardType, rewardId)))

            delayRow = SE(resultTable, 'tr')
            delayData = SE(delayRow, 'td')
            delayCenter = SE(delayData, 'center')
            delayCenter.text = 'Reward will arrive in mailbox in a few minutes.'
            
            SE(body, 'br')

            backToMenu = SE(body, 'a')
            backToMenu.set('href', '/codeManagement')
            backToMenu.text = 'Back to Menu'

    def _codeHasInvalidChars(self, code):
        return not TTCodeDict.isLegalCode(code)

    def _errorCheckCode(self, errors, code, fieldName='code'):
        if len(code.strip()) == 0:
            errors.add(fieldName, self.GenericErrors.EmptyInput)
                
        if self._codeHasInvalidChars(code):
            errors.add(fieldName, self.CodeErrors.InvalidCharInCode)

    def _errorCheckAvId(self, errors, avId, fieldName='avId'):
        if len(avId.strip()) == 0:
            errors.add(fieldName, self.GenericErrors.EmptyInput)

        for char in avId:
            if (char not in string.digits):
                errors.add(fieldName, self.RedeemErrors.InvalidCharInAvId)

    def _doRecaptcha(self, replyTo, values, errors):
        """
        rResponse = recaptcha.submit(values.recaptchaChallenge, values.recaptchaResponse,
                                     self.ReCAPTCHAPrivateKey, replyTo.getSourceAddress())
        if not rResponse.is_valid:
            errors.add('recaptcha', rResponse.error_code)
            """
        # make sure it's two words
        valid = re.match(r'[ ]*[\w]+[ ]+[\w]+[ ]*', values.recaptchaResponse)
        if not valid:
            errors.add('recaptchaCustom', 'Invalid entry')

    def _doSystemUnavailablePage(self, page):
        page.text = 'System is unavailable, please try again later.'

    def handleHTTPcodeManagement(self, replyTo=None, **kw):
        replyNow = True

        #page = HTMLTree('Toontown Code Management')
        body = replyTo.getBodyTag()
        # we're using the landing page so the body 'is' the page
        page = ET.ElementTree(body)

        try:
            op = None

            if 'op' in kw:
                opStr = kw['op']
                if self.Ops.hasString(opStr):
                    op = self.Ops.fromString(opStr)
            if op is None:
                op = self.Ops.menu

            if op == self.Ops.menu:
                newLot = SE(body, 'a', href='/codeManagement?op=create')
                newLot.text = 'Create a new code lot'
                SE(body, 'br')

                if len(self._db.getLotNames()):
                    viewLot = SE(body, 'a', href='/codeManagement?op=view')
                    viewLot.text = 'View an existing code lot'
                    SE(body, 'br')

                    modifyLot = SE(body, 'a', href='/codeManagement?op=modify')
                    modifyLot.text = 'Modify an existing code lot'
                    SE(body, 'br')

                    deleteLot = SE(body, 'a', href='/codeManagement?op=delete')
                    deleteLot.text = 'Delete an existing code lot'
                    SE(body, 'br')

                    viewLot = SE(body, 'a', href='/codeManagement?op=lookup')
                    viewLot.text = 'Look up existing codes'
                    SE(body, 'br')

                    redeemCode = SE(body, 'a', href='/codeManagement?op=redeem')
                    redeemCode.text = 'Redeem a code'
                    SE(body, 'br')

                SE(body, 'br')
                SE(body, 'br')

                img = SE(body, 'img', title='relevant this is',
                         src='http://icanhascheezburger.files.wordpress.com/2007/01/2000455272489756911_rs.jpg')

            elif op == self.Ops.create:
                self._doCreateForm(body, body, replyTo)

            elif op == self.Ops.doCreate:
                values = ScratchPad(
                    lotName = uhs(kw['lotName']),
                    codeType = uhs(kw['codeType']),
                    rewardType = uhs(kw['rewardType']),
                    rewardItemId = uhs(kw['rewardItemId']),
                    hasExpiration = uhs(kw['hasExpiration']),
                    recaptchaChallenge = uhs(kw['recaptcha_challenge_field']),
                    recaptchaResponse = uhs(kw['recaptcha_response_field']),
                    )
                if values.codeType == 'auto':
                    values.add(numCodes = uhs(kw['numCodes']))
                    values.add(numCodes2 = uhs(kw['numCodes2']))
                else:
                    values.add(manualCode = uhs(kw['manualCode']))
                    values.add(manualCode2 = uhs(kw['manualCode2']))
                    values.manualCode = unicode(values.manualCode, 'utf-8')
                    values.manualCode2 = unicode(values.manualCode2, 'utf-8')
                if values.hasExpiration == 'yes':
                    values.add(
                        expYear = uhs(kw['expYear']),
                        expMonth = uhs(kw['expMonth']),
                        expDay = uhs(kw['expDay']),
                        )

                errors = FormErrors()

                if len(values.lotName.strip()) == 0:
                    errors.add('lotName', self.GenericErrors.EmptyInput)

                for char in values.lotName:
                    # lot names can only contain lowercase ASCII letters, numbers, and underscores
                    if ((char not in (string.letters + string.digits + '_')) or
                        ((char in string.letters) and (string.upper(char) == char))):
                        errors.add('lotName', self.CreateErrors.InvalidCharInLotName)

                if values.lotName in self._db.getLotNames():
                    errors.add('lotName', self.CreateErrors.UsedLotName)

                if not TTCodeRedemptionDBTester.isLotNameValid(values.lotName):
                    errors.add('lotName', self.CreateErrors.UsedLotName)

                manualCode = (values.codeType == 'manual')

                if not manualCode:
                    manualCodeStr = None
                    try:
                        numCodes = int(values.numCodes)
                    except ValueError:
                        errors.add('numCodes', self.GenericErrors.InvalidNumber)
                    else:
                        if numCodes <= 0:
                            errors.add('numCodes', 'Number must be 1 or greater')
                        if numCodes > self.MaxLotSize:
                            errors.add('numCodes', 'Number cannot be larger than %s' % self.MaxLotSize)
                    if values.numCodes != values.numCodes2:
                        errors.add('numCodes2', self.GenericErrors.FieldsMustMatch)
                else:
                    numCodes = 1
                    manualCodeStr = values.manualCode
                    # manual codes can only contain ManualCharacters and must contain at least one
                    # ManualOnlyCharacter
                    foundManualOnlyChar = False
                    foundInvalidChar = False
                    for char in values.manualCode:
                        char = char.upper()
                        if not TTCodeDict.isValidManualChar(char):
                            foundInvalidChar = True
                            errors.add('manualCode', self.CodeErrors.InvalidCharInCode)
                        if TTCodeDict.isManualOnlyChar(char):
                            foundManualOnlyChar = True
                    # only show this error if all chars are valid (too confusing otherwise)
                    if (not foundInvalidChar) and (not foundManualOnlyChar):
                        errors.add('manualCode', self.CodeErrors.MustContainManualChar)
                    # check if the code is too long
                    if len(values.manualCode) > TTCodeRedemptionConsts.MaxCustomCodeLen:
                        errors.add('manualCode', self.CodeErrors.CodeTooLong)
                    # check if the code already exists
                    if (not foundInvalidChar) and (foundManualOnlyChar):
                        if self._db.codeExists(values.manualCode):
                            errors.add('manualCode', self.CodeErrors.CodeAlreadyExists)
                    if values.manualCode != values.manualCode2:
                        errors.add('manualCode2', self.GenericErrors.FieldsMustMatch)

                expDate = None
                if values.hasExpiration == 'yes':
                    try:
                        expDate = datetime.date(int(values.expYear), int(values.expMonth), int(values.expDay))
                    except ValueError, e:
                        errors.add('expiration', str(e).capitalize())

                    # disable this check until we have 'active' flag or activation date
                    """
                    if expDate is not None:
                        if expDate < datetime.date.today():
                            errors.add('expiration', 'Expiration date must be in the future')
                            """

                self._doRecaptcha(replyTo, values, errors)

                if not errors.isEmpty():
                    self._doCreateForm(body, body, replyTo, values, errors)
                else:
                    self._startCreateLotTask(replyTo, page, body, values,
                                             manualCode, numCodes, manualCodeStr, expDate)
                    replyNow = False

            elif op == self.Ops.view:
                self._doViewForm(body, replyTo)

            elif op == self.Ops.doView:
                lotName = kw['lotName']
                filter = kw['filter']
                showFields = kw['showFields']

                justCode = (showFields != 'all')

                self._doViewLot(lotName, body, justCode, filter)

            elif op == self.Ops.modify:
                self._doModifyForm(body, replyTo)

            elif op == self.Ops.doModify:
                values = ScratchPad(
                    modification = uhs(kw['modification']),
                    recaptchaChallenge = uhs(kw['recaptcha_challenge_field']),
                    recaptchaResponse = uhs(kw['recaptcha_response_field']),
                    )
                if 'lotName' in kw:
                    values.add(
                        lotName = kw['lotName'],
                        )
                if values.modification == 'expiration':
                    values.add(
                        expYear = kw['expYear'],
                        expMonth = kw['expMonth'],
                        expDay = kw['expDay'],
                        )

                errors = FormErrors()

                if 'lotName' not in values:
                    errors.add('lotName', 'Invalid lot')

                self._doRecaptcha(replyTo, values, errors)

                if not errors.isEmpty():
                    self._doModifyForm(body, replyTo, values, errors)
                else:
                    self._doModifyLot(body, replyTo, page, values)

            elif op == self.Ops.delete:
                self._doDeleteForm(body, replyTo)

            elif op == self.Ops.doDelete:
                values = ScratchPad(
                    lotName = kw['lotName'],
                    lotName2 = kw['lotName2'],
                    recaptchaChallenge = uhs(kw['recaptcha_challenge_field']),
                    recaptchaResponse = uhs(kw['recaptcha_response_field']),
                    )
                errors = FormErrors()

                if values.lotName != values.lotName2:
                    errors.add('lotName2', self.GenericErrors.FieldsMustMatch)

                self._doRecaptcha(replyTo, values, errors)

                if not errors.isEmpty():
                    self._doDeleteForm(body, replyTo, values, errors)
                else:
                    self._doDelete(body, replyTo, page, values)

            elif op == self.Ops.lookup:
                self._doLookupForm(body, replyTo)

            elif op == self.Ops.doLookup:
                values = ScratchPad(
                    mode = uhs(kw['mode']),
                    )
                avIdMode = (values.mode == 'AvId')
                if avIdMode:
                    values.add(avId = uhs(kw['avId']))
                else:
                    values.add(code = uhs(kw['code']))
                    values.code = unicode(values.code, 'utf-8')

                errors = FormErrors()
                if avIdMode:
                    self._errorCheckAvId(errors, values.avId)
                else:
                    self._errorCheckCode(errors, values.code)
                    if not self._db.codeExists(values.code):
                        errors.add('code', self.CodeErrors.InvalidCode)

                if not errors.isEmpty():
                    self._doLookupForm(body, replyTo, values, errors)
                else:
                    if avIdMode:
                        self._doLookup(body, avId=values.avId)
                    else:
                        self._doLookup(body, code=values.code)

            elif op == self.Ops.redeem:
                self._doRedeemForm(body, replyTo)

            elif op == self.Ops.doRedeem:
                values = ScratchPad(
                    code = uhs(kw['code']),
                    avId = uhs(kw['avId']),
                    recaptchaChallenge = uhs(kw['recaptcha_challenge_field']),
                    recaptchaResponse = uhs(kw['recaptcha_response_field']),
                    )
                values.code = unicode(values.code, 'utf-8')

                errors = FormErrors()
                self._errorCheckCode(errors, values.code)
                self._errorCheckAvId(errors, values.avId)

                self._doRecaptcha(replyTo, values, errors)

                if not errors.isEmpty():
                    self._doRedeemForm(body, replyTo, values, errors)
                else:
                    avId = int(values.avId)
                    context = self._redeemContextGen.next()
                    self._redeemContext2session[context] = ScratchPad(
                        result = None,
                        avId = avId,
                        values = values,
                        errors = errors,
                        )
                    result = self.redeemCode(values.code, avId, Functor(
                        self._handleRedeemResult, context, page, body, replyTo, ))
                    if result is None:
                        replyNow = False
                    else:
                        error = {
                            TTCodeRedemptionConsts.RedeemErrors.CodeDoesntExist: self.CodeErrors.InvalidCode,
                            TTCodeRedemptionConsts.RedeemErrors.CodeIsExpired: self.RedeemErrors.CodeIsExpired,
                            TTCodeRedemptionConsts.RedeemErrors.CodeAlreadyRedeemed: self.RedeemErrors.CodeAlreadyRedeemed,
                            TTCodeRedemptionConsts.RedeemErrors.AwardCouldntBeGiven: self.RedeemErrors.AwardCouldntBeGiven,
                            }[result]
                        errors.add('code', error)
                        self._doRedeemForm(body, replyTo, values, errors)

            if replyNow:
                self._reply(page, replyTo)

        except TTCodeRedemptionDB.TryAgainLater, e:
            self._warnTryAgainLater(e)
            body.clear()
            self._doSystemUnavailablePage(body)
            self._reply(page, replyTo)

    def _handleRedeemResult(self, context, page, body, replyTo, result, awardMgrResult):
        assert self.notify.debugCall()
        session = self._redeemContext2session.pop(context)
        session.result = result
        session.awardMgrResult = awardMgrResult
        self._doRedeemResult(body, replyTo, session.avId, session.result, session.awardMgrResult,
                             session.values, session.errors)
        self._reply(page, replyTo)

    def redeemCodeAiToUd(self, serial, rmDoId, context, code, senderId, callback=None):
        assert self.notify.debugCall()
        avId = senderId

        # context is supplied by the client and there are no invalid values for it
        # code comes from the client and could be any string

        try:
            result = None

            if self.Disabled:
                result = TTCodeRedemptionConsts.RedeemErrors.SystemUnavailable
            else:
                while 1:
                    try:
                        code = unicode(code, 'utf-8')
                    except UnicodeDecodeError, e:
                        # code is not utf-8-able
                        self.air.writeServerEvent('suspicious', avId, 'non-utf-8 code redemption: %s' % repr(code))
                        result = TTCodeRedemptionConsts.RedeemErrors.CodeDoesntExist
                        break

                    if self._codeHasInvalidChars(code):
                        # code has non-letter/digit/dash characters
                        result = TTCodeRedemptionConsts.RedeemErrors.CodeDoesntExist
                        break

                    break

                if (result or (not self._db.codeExists(code))):
                    # check to make sure this avatar isn't submitting incorrect codes too often
                    self._spamDetector.codeSubmitted(senderId)

                if self._wantSpamDetect and self._spamDetector.avIsBlocked(senderId):
                    self.air.writeServerEvent('suspicious', avId,
                                              'too many invalid code redemption attempts, '
                                              'submission rejected: %s' % u2ascii(code))
                    result = TTCodeRedemptionConsts.RedeemErrors.TooManyAttempts

            if result is not None:
                awardMgrResult = 0
                self._handleRedeemCodeAiToUdResult(callback, serial, rmDoId, context, avId, result, awardMgrResult)
            else:
                """
                'code' came from a client and therefore should be considered to be any potential string
                (apart from any checks that have already been done), in particular strings intended
                to cause trouble
                """
                self._db.redeemCode(code, avId, self, Functor(
                    self._handleRedeemCodeAiToUdResult, callback, serial, rmDoId, context, avId, ))

        except TTCodeRedemptionDB.TryAgainLater, e:
            self._warnTryAgainLater(e)

    def _handleRedeemCodeAiToUdResult(self, callback, serial, rmDoId, context, avId, result, awardMgrResult):
        assert self.notify.debugCall()
        if callback:
            callback(serial, context, avId, result, awardMgrResult)
        else:
            self.air.sendUpdateToDoId('TTCodeRedemptionMgr',
                                      'redeemCodeResultUdToAi',
                                      rmDoId,
                                      [serial, context, avId, result, awardMgrResult]
                                      )

    def redeemCode(self, code, avId, callback):
        assert self.notify.debugCall()
        # callback takes TTCodeRedemptionConsts.RedeemErrors value
        return self._db.redeemCode(code, avId, self, callback)
        
    def _giveReward(self, avId, rewardType, rewardItemId, callback):
        assert self.notify.debugCall()
        # callback takes result
        context = self._rewardSerialNumGen.next()
        self._rewardContextTable[context] = callback
        self.air.dispatchUpdateToGlobalDoId(
            "AwardManagerUD", "giveAwardToToon",
            OtpDoGlobals.OTP_DO_ID_TOONTOWN_AWARD_MANAGER,
            [context, self.doId, "TTCodeRedemptionMgrUD", avId, rewardType, rewardItemId, ])
        
    def giveAwardToToonResult(self, context, result):
        assert self.notify.debugCall()
        callback = self._rewardContextTable.pop(context)
        try:
            callback(result)
        except TTCodeRedemptionDB.TryAgainLater, e:
            self._warnTryAgainLater(e)
        
    def _warnTryAgainLater(self, exception):
        # if we catch a TryAgainLater, drop this code submission on the floor. The AI
        # will resubmit the code shortly
        self.notify.warning('%s' % exception)
        self.notify.warning(
            'caught TryAgainLater exception from TTCodeRedemptionDB. Dropping request')
