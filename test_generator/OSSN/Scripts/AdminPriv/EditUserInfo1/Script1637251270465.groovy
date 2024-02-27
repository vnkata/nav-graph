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

WebUI.navigateToUrl('http://localhost/administrator')

WebUI.setText(findTestObject('Object Repository/input_Username_username'), 'admin1')

WebUI.setEncryptedText(findTestObject('Object Repository/input_Password_password'), 'RigbBhfdqODKcAsiUrg+1Q==')

WebUI.click(findTestObject('Object Repository/input_Password_btn btn-primary'))

WebUI.verifyElementText(findTestObject('Object Repository/div_You are now logged in'), 'You are now logged in!')

WebUI.click(findTestObject('Object Repository/i_Log out_fa fa-bars'))

WebUI.click(findTestObject('Object Repository/a_User Manager'))

WebUI.click(findTestObject('Object Repository/a_List Users'))

WebUI.click(findTestObject('a_Edit (2)'))

WebUI.setEncryptedText(findTestObject('Object Repository/input_Password_password'), 'tzH6RvlfSTg=')

WebUI.selectOptionByValue(findTestObject('Object Repository/select_Normal     Administrator'), 'admin', true)

WebUI.selectOptionByValue(findTestObject('Object Repository/select_Normal     Administrator'), 'normal', true)

WebUI.click(findTestObject('Object Repository/input_Type_btn btn-success btn-sm'))

WebUI.verifyElementText(findTestObject('div_The password must be more than 5 characters (1)'), 'The password must be more than 5 characters.')

WebUI.setEncryptedText(findTestObject('Object Repository/input_Password_password'), 'aeHFOx8jV/A=')

WebUI.selectOptionByValue(findTestObject('Object Repository/select_Normal     Administrator'), 'admin', true)

WebUI.selectOptionByValue(findTestObject('Object Repository/select_Normal     Administrator'), 'normal', true)

WebUI.click(findTestObject('Object Repository/input_Type_btn btn-success btn-sm'))

WebUI.click(findTestObject('Object Repository/i_Log out_fa fa-bars fa-3'))

WebUI.click(findTestObject('Object Repository/a_Log out'))

WebUI.navigateToUrl('localhost/login')

WebUI.setText(findTestObject('Object Repository/input_Username_username'), 'user1')

WebUI.setEncryptedText(findTestObject('Object Repository/input_Password_password'), 'RigbBhfdqODKcAsiUrg+1Q==')

WebUI.click(findTestObject('Object Repository/input_Password_btn btn-primary'))

WebUI.setText(findTestObject('Object Repository/input_Username_username'), 'user1')

WebUI.setEncryptedText(findTestObject('Object Repository/input_Password_password'), 'aeHFOx8jV/A=')

WebUI.click(findTestObject('Object Repository/input_Password_btn btn-primary'))

WebUI.click(findTestObject('i_OSSN_fa fa-sort-down'))

WebUI.click(findTestObject('Object Repository/a_Log out'))

WebUI.navigateToUrl('http://localhost/administrator')

WebUI.setText(findTestObject('Object Repository/input_Username_username'), 'admin1')

WebUI.setEncryptedText(findTestObject('Object Repository/input_Password_password'), 'RigbBhfdqODKcAsiUrg+1Q==')

WebUI.click(findTestObject('Object Repository/input_Password_btn btn-primary'))

WebUI.click(findTestObject('Object Repository/i_Log out_fa fa-bars'))

WebUI.click(findTestObject('Object Repository/a_User Manager'))

WebUI.click(findTestObject('Object Repository/a_List Users'))

WebUI.click(findTestObject('a_Edit (2)'))

WebUI.setEncryptedText(findTestObject('Object Repository/input_Password_password'), 'RigbBhfdqODKcAsiUrg+1Q==')

WebUI.selectOptionByValue(findTestObject('Object Repository/select_Normal     Administrator'), 'admin', true)

WebUI.selectOptionByValue(findTestObject('Object Repository/select_Normal     Administrator'), 'normal', true)

WebUI.click(findTestObject('Object Repository/input_Type_btn btn-success btn-sm'))

WebUI.click(findTestObject('Object Repository/i_Log out_fa fa-bars fa-3'))

WebUI.click(findTestObject('Object Repository/a_Log out'))

WebUI.closeBrowser()

