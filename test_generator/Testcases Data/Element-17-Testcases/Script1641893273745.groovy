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

WebUI.navigateToUrl('http://localhost:8080/')

WebUI.click(findTestObject('Object Repository/Page_Element/div_Sign In'))

WebUI.setText(findTestObject('Object Repository/Page_Element/input_Sign in with_username'), 'vntuan19@apcs.vn')

WebUI.setEncryptedText(findTestObject('Object Repository/Page_Element/input_Username_password'), 'vDUYGrCeFogm4fIl1OPC0g==')

WebUI.click(findTestObject('Object Repository/Page_Element/input_Forgot password_mx_Login_submit'))

WebUI.click(findTestObject('Object Repository/Page_Element/div_Verify with Security Key or Phrase'))

WebUI.setEncryptedText(findTestObject('Object Repository/Page_Element/input_use your Security Key_mx_passPhraseInput'), 
    'T5dL0dZa3GcY/MrlN7YOn6WOTrovA4jj9xOYEG/i3Z769E9Kq/X7+gryZqF4ov+opBHLAWv3wACasluLqCMBHw==')

WebUI.click(findTestObject('Object Repository/Page_Element/button_Continue'))

WebUI.click(findTestObject('Object Repository/Page_Element/div_Done'))

WebUI.click(findTestObject('Object Repository/Page_Element/img_Review_mx_BaseAvatar_image'))

WebUI.verifyElementText(findTestObject('Object Repository/Page_Element/span_ptnha19'), 'ptnha19')

WebUI.click(findTestObject('Object Repository/Page_Element/span_All settings'))

WebUI.setEncryptedText(findTestObject('Object Repository/Page_Element/input_Account_mx_Field_6'), 'vDUYGrCeFogm4fIl1OPC0g==')

WebUI.setEncryptedText(findTestObject('Object Repository/Page_Element/input_Current password_mx_Field_7'), '5Ed5CIkj9UTx0aA2FxJD8A==')

WebUI.setEncryptedText(findTestObject('Object Repository/Page_Element/input_New Password_mx_Field_8'), '8WJgueGhnXxsj8l3w7OfT/LRenlEwIfbqUrueo8H6hM=')

WebUI.click(findTestObject('Object Repository/Page_Element/div_Change Password'))

WebUI.click(findTestObject('Object Repository/Page_Element/div_GeneralProfileDisplay Namevntuan13579ma_84fc11'))

WebUI.click(findTestObject('Object Repository/Page_Element/div_Settings_mx_AccessibleButton mx_Dialog__4987e8'))

WebUI.rightClick(findTestObject('Object Repository/Page_Element/img_Review_mx_BaseAvatar_image'))

WebUI.click(findTestObject('Object Repository/Page_Element/span_ptnha19'))

WebUI.verifyElementText(findTestObject('Object Repository/Page_Element/span_ptnha19'), 'ptnha19')

WebUI.click(findTestObject('Object Repository/Page_Element/span_Sign out'))

WebUI.setText(findTestObject('Object Repository/Page_Element/input_Sign in with_username_1'), 'vntuan19@apcs.vn')

WebUI.setEncryptedText(findTestObject('Object Repository/Page_Element/input_Username_password_1'), 'vDUYGrCeFogm4fIl1OPC0g==')

WebUI.click(findTestObject('Object Repository/Page_Element/input_Forgot password_mx_Login_submit'))

WebUI.verifyElementText(findTestObject('Object Repository/Page_Element/div_Verify with Security Key or Phrase'), 'Verify with Security Key or Phrase')

WebUI.closeBrowser()

