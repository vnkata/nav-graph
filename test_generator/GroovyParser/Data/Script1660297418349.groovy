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

WebUI.navigateToUrl('http://j2store.net/demo/')

WebUI.click(findTestObject('Object Repository/Page_Home/a_My Account'))

WebUI.setText(findTestObject('Page_My Account/input_Username_username'), 'user@mail.example.com')

WebUI.setEncryptedText(findTestObject('Object Repository/Page_My Account/input_Password_password'), 'RigbBhfdqOBGNlJIWM1ClA==')

WebUI.click(findTestObject('Object Repository/Page_My Account/input_Remember me_submit'))

WebUI.mouseOver(findTestObject('Object Repository/Page_My Account/a_My Account'))

WebUI.verifyElementPresent(findTestObject('Object Repository/Page_My Account/a_Logout'), 0)

WebUI.verifyElementText(findTestObject('Object Repository/Page_My Account/h3_My Profile'), 'My Profile')

WebUI.verifyElementPresent(findTestObject('Object Repository/Page_My Account/a_Orders'), 0)

WebUI.verifyElementPresent(findTestObject('Object Repository/Page_My Account/a_Downloads'), 0)

WebUI.verifyElementPresent(findTestObject('Object Repository/Page_My Account/a_Address'), 0)

WebUI.closeBrowser()

