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

WebUI.setText(findTestObject('Object Repository/input_Username_username'), 'admin1')

WebUI.setEncryptedText(findTestObject('Object Repository/input_Password_password'), 'RigbBhfdqODKcAsiUrg+1Q==')

WebUI.click(findTestObject('Object Repository/input_Password_btn btn-primary'))

WebUI.setText(findTestObject('Object Repository/textarea_Post_post'), 'admin1 post')

WebUI.click(findTestObject('Object Repository/span_Privacy'))

WebUI.click(findTestObject('Object Repository/input_Privacy_privacy'))

WebUI.click(findTestObject('Object Repository/a_Save'))

WebUI.click(findTestObject('Object Repository/input_Tag Friends_btn btn-primary ossn-wall-post'))

WebUI.click(findTestObject('i_OSSN_fa fa-sort-down'))

WebUI.click(findTestObject('Object Repository/a_Log out'))

WebUI.click(findTestObject('Object Repository/a_Login'))

WebUI.setText(findTestObject('Object Repository/input_Username_username'), 'user1')

WebUI.setEncryptedText(findTestObject('Object Repository/input_Password_password'), 'RigbBhfdqODKcAsiUrg+1Q==')

WebUI.click(findTestObject('Object Repository/input_Password_btn btn-primary'))

WebUI.mouseOver(findTestObject('Object Repository/a_Like'))

WebUI.click(findTestObject('Object Repository/div_Like_emoji__hand'))

WebUI.click(findTestObject('Object Repository/i_OSSN_fa fa-sort-down'))

WebUI.click(findTestObject('Object Repository/a_Log out_1'))

WebUI.click(findTestObject('Object Repository/a_Login'))

WebUI.setText(findTestObject('Object Repository/input_Username_username'), 'admin1')

WebUI.setEncryptedText(findTestObject('Object Repository/input_Password_password'), 'S7CYZ2LRgTUFAGmcGkq/yw==')

WebUI.click(findTestObject('Object Repository/div_Login        Username          Password_9e7d53'))

WebUI.setEncryptedText(findTestObject('Object Repository/input_Password_password'), 'RigbBhfdqODKcAsiUrg+1Q==')

WebUI.click(findTestObject('Object Repository/input_Password_btn btn-primary'))

WebUI.click(findTestObject('Object Repository/a_1 Person'))

WebUI.verifyElementText(findTestObject('Object Repository/a_user 1'), 'user 1')

WebUI.click(findTestObject('Object Repository/div_X'))

WebUI.click(findTestObject('Object Repository/a_Privacy_btn btn-link'))

WebUI.click(findTestObject('Object Repository/a_Delete'))

WebUI.click(findTestObject('i_OSSN_fa fa-sort-down'))

WebUI.click(findTestObject('Object Repository/a_Log out_1_2'))

WebUI.closeBrowser()

