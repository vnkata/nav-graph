import static com.kms.katalon.core.checkpoint.CheckpointFactory.findCheckpoint
import static com.kms.katalon.core.testcase.TestCaseFactory.findTestCase
import static com.kms.katalon.core.testdata.TestDataFactory.findTestData
import static com.kms.katalon.core.testobject.ObjectRepository.findTestObject
import static com.kms.katalon.core.testobject.ObjectRepository.findWindowsObject
import com.kms.katalon.core.checkpoint.Checkpoint as Checkpoint
import com.kms.katalon.core.cucumber.keyword.CucumberBuiltinKeywords as CucumberKW
import com.kms.katalon.core.mobile.keyword.MobileBuiltInKeywords as Mobile
import com.kms.katalon.core.model.FailureHandling as FailureHandling
import com.kms.katalon.core.testcase.TestCase as TestCase
import com.kms.katalon.core.testdata.TestData as TestData
import com.kms.katalon.core.testng.keyword.TestNGBuiltinKeywords as TestNGKW
import com.kms.katalon.core.testobject.TestObject as TestObject
import com.kms.katalon.core.webservice.keyword.WSBuiltInKeywords as WS
import com.kms.katalon.core.webui.keyword.WebUiBuiltInKeywords as WebUI
import com.kms.katalon.core.windows.keyword.WindowsBuiltinKeywords as Windows
import internal.GlobalVariable as GlobalVariable
import org.openqa.selenium.Keys as Keys

WebUI.openBrowser('')

WebUI.navigateToUrl('http://localhost/login')

WebUI.setText(findTestObject('Object Repository/input_Username_username'), 'user1')

WebUI.setEncryptedText(findTestObject('Object Repository/input_Password_password'), 'RigbBhfdqODKcAsiUrg+1Q==')

WebUI.click(findTestObject('Object Repository/input_Password_btn btn-primary'))

WebUI.click(findTestObject('Object Repository/i_Groups_fa fa-th-list'))

WebUI.click(findTestObject('Object Repository/a_user 1'))

WebUI.setText(findTestObject('Object Repository/textarea_Post_post'), 'user1 post')

WebUI.click(findTestObject('Object Repository/input_Tag Friends_btn btn-primary ossn-wall-post'))

WebUI.click(findTestObject('Object Repository/i_OSSN_fa fa-sort-down'))

WebUI.click(findTestObject('Object Repository/a_Log out'))

WebUI.click(findTestObject('Object Repository/a_Login'))

WebUI.setText(findTestObject('Object Repository/input_Username_username'), 'admin1')

WebUI.setEncryptedText(findTestObject('Object Repository/input_Password_password'), 'RigbBhfdqODKcAsiUrg+1Q==')

WebUI.click(findTestObject('Object Repository/input_Password_btn btn-primary'))

WebUI.click(findTestObject('Object Repository/i_Groups_fa fa-th-list'))

WebUI.click(findTestObject('Object Repository/li_Groups'))

WebUI.click(findTestObject('Object Repository/li_Groups_1'))

WebUI.click(findTestObject('Object Repository/div_People'))

WebUI.click(findTestObject('Object Repository/a_user 1'))

WebUI.mouseOver(findTestObject('Object Repository/a_Like'))

WebUI.click(findTestObject('Object Repository/div_Like_emoji  emoji--like'))

WebUI.click(findTestObject('Object Repository/a_Unlike'))

WebUI.click(findTestObject('i_Privacy_fa fa fa-ellipsis-h (1)'))

WebUI.click(findTestObject('a_Delete (2)'))

WebUI.click(findTestObject('Object Repository/i_OSSN_fa fa-sort-down'))

WebUI.click(findTestObject('Object Repository/a_Log out_1'))

WebUI.closeBrowser()

