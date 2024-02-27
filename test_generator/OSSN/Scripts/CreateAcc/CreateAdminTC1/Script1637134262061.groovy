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

WebUI.click(findTestObject('Object Repository/a_Add User'))

WebUI.setText(findTestObject('Object Repository/input_First Name_firstname'), 'Admin')

WebUI.setText(findTestObject('Object Repository/input_Last Name_lastname'), 'TC1')

WebUI.setText(findTestObject('Object Repository/input_Username_username'), 'admintc1')

WebUI.setText(findTestObject('Object Repository/input_Email_email'), 'admintc1@test.com')

WebUI.setEncryptedText(findTestObject('Object Repository/input_Password_password'), 'RigbBhfdqODKcAsiUrg+1Q==')

WebUI.click(findTestObject('Object Repository/input_Birthdate_birthdate'))

WebUI.click(findTestObject('a_1 (1)'))

WebUI.click(findTestObject('Object Repository/input_Gender_gender'))

WebUI.selectOptionByValue(findTestObject('Object Repository/select_Normal     Administrator'), 'admin', true)

WebUI.click(findTestObject('Object Repository/input_Type_btn btn-primary'))

WebUI.verifyElementText(findTestObject('Object Repository/div_Your account has been created'), 'Your account has been created.')

WebUI.click(findTestObject('Object Repository/i_Log out_fa fa-bars fa-3'))

WebUI.click(findTestObject('Object Repository/a_Log out'))

WebUI.navigateToUrl('localhost/login')

WebUI.setText(findTestObject('Object Repository/input_Username_username'), 'admintc1')

WebUI.setEncryptedText(findTestObject('Object Repository/input_Password_password'), 'RigbBhfdqODKcAsiUrg+1Q==')

WebUI.click(findTestObject('Object Repository/input_Password_btn btn-primary'))

WebUI.click(findTestObject('Object Repository/i_Groups_fa fa-th-list'))

WebUI.click(findTestObject('Object Repository/a_Admin TC1'))

WebUI.verifyElementText(findTestObject('Object Repository/div_Admin TC1'), 'Admin TC1')

WebUI.click(findTestObject('i_OSSN_fa fa-sort-down'))

WebUI.click(findTestObject('Object Repository/a_Log out'))

WebUI.closeBrowser()

