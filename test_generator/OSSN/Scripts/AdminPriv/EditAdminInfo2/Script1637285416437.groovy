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

WebUI.click(findTestObject('Object Repository/a'))

WebUI.verifyElementText(findTestObject('Object Repository/a_Admin 1'), 'Admin 1')

WebUI.click(findTestObject('Object Repository/a_Edit Profile'))

WebUI.verifyElementText(findTestObject('Object Repository/div_Admin 1'), 'Admin 1')

WebUI.verifyElementText(findTestObject('Object Repository/div_Administrator'), 'Administrator')

WebUI.setEncryptedText(findTestObject('Object Repository/input_Password_password'), 'tzH6RvlfSTg=')

WebUI.selectOptionByValue(findTestObject('Object Repository/select_GermanGreekEnglishEsperantoSpanishFr_204776'), 'de', 
    true)

WebUI.selectOptionByValue(findTestObject('Object Repository/select_GermanGreekEnglishEsperantoSpanishFr_204776'), 'en', 
    true)

WebUI.click(findTestObject('Object Repository/input_Language_btn btn-primary'))

WebUI.verifyElementText(findTestObject('div_The password must be more than 5 characters'), 'The password must be more than 5 characters.')

WebUI.setEncryptedText(findTestObject('Object Repository/input_Password_password'), 'aeHFOx8jV/A=')

WebUI.selectOptionByValue(findTestObject('Object Repository/select_GermanGreekEnglishEsperantoSpanishFr_204776'), 'el', 
    true)

WebUI.selectOptionByValue(findTestObject('Object Repository/select_GermanGreekEnglishEsperantoSpanishFr_204776'), 'en', 
    true)

WebUI.click(findTestObject('Object Repository/input_Language_btn btn-primary'))

WebUI.verifyElementText(findTestObject('Object Repository/div_User updated'), 'User updated!')

WebUI.click(findTestObject('Object Repository/i_OSSN_fa fa-sort-down'))

WebUI.click(findTestObject('Object Repository/a_Log out'))

WebUI.click(findTestObject('Object Repository/a_Login'))

WebUI.setText(findTestObject('Object Repository/input_Username_username'), 'admin1')

WebUI.setEncryptedText(findTestObject('Object Repository/input_Password_password'), 'RigbBhfdqODKcAsiUrg+1Q==')

WebUI.click(findTestObject('Object Repository/input_Password_btn btn-primary'))

WebUI.verifyElementText(findTestObject('Object Repository/p_We couldnt log you in. Please check your _8fbd06'), 'We couldn\'t log you in. Please check your username or password and try again.')

WebUI.setText(findTestObject('Object Repository/input_Username_username'), 'admin1')

WebUI.setEncryptedText(findTestObject('Object Repository/input_Password_password'), 'aeHFOx8jV/A=')

WebUI.click(findTestObject('Object Repository/input_Password_btn btn-primary'))

WebUI.click(findTestObject('Object Repository/a'))

WebUI.verifyElementText(findTestObject('Object Repository/a_Admin 1'), 'Admin 1')

WebUI.click(findTestObject('Object Repository/a_Edit Profile'))

WebUI.setEncryptedText(findTestObject('Object Repository/input_Password_password'), 'RigbBhfdqODKcAsiUrg+1Q==')

WebUI.selectOptionByValue(findTestObject('Object Repository/select_GermanGreekEnglishEsperantoSpanishFr_204776'), 'de', 
    true)

WebUI.selectOptionByValue(findTestObject('Object Repository/select_GermanGreekEnglishEsperantoSpanishFr_204776'), 'en', 
    true)

WebUI.click(findTestObject('Object Repository/input_Language_btn btn-primary'))

WebUI.verifyElementText(findTestObject('Object Repository/div_User updated'), 'User updated!')

WebUI.click(findTestObject('Object Repository/i_OSSN_fa fa-sort-down'))

WebUI.click(findTestObject('Object Repository/a_Log out_1'))

WebUI.closeBrowser()

