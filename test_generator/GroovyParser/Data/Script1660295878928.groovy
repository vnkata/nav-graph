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

WebUI.callTestCase(findTestCase('add_two_beds_to_cart'), [:], FailureHandling.STOP_ON_FAILURE)

WebUI.click(findTestObject('Object Repository/Page_Bed/a_Checkout'))

WebUI.verifyElementAttributeValue(findTestObject('Page_Checkout/input_New Customer_account'), 'checked', 'true', 0)

WebUI.click(findTestObject('Object Repository/Page_Checkout/button_Continue'))

WebUI.setText(findTestObject('Object Repository/Page_Checkout/input_First name_first_name'), 'user')

WebUI.setText(findTestObject('Object Repository/Page_Checkout/input_Last name_last_name'), 'user')

WebUI.setText(findTestObject('Object Repository/Page_Checkout/input_Email_email'), 'user@mail.example.com')

WebUI.setText(findTestObject('Object Repository/Page_Checkout/input_Mobile_phone_2'), '0908555111')

WebUI.setText(findTestObject('Object Repository/Page_Checkout/input_Address Line 1_address_1'), '123 Le Hong Phong, Q10')

WebUI.setText(findTestObject('Object Repository/Page_Checkout/input_City_city'), 'TPHCM')

WebUI.setText(findTestObject('Object Repository/Page_Checkout/input_Zip  Postal code_zip'), '999')

WebUI.selectOptionByValue(findTestObject('Object Repository/Page_Checkout/select_AfghanistanAlbaniaAlgeriaAmerican Sa_79bd05'), 
    '230', true)

WebUI.selectOptionByValue(findTestObject('Object Repository/Page_Checkout/select_-- Select --An GiangBa Ria-Vung TauB_61c870'), 
    '3780', true)

WebUI.setEncryptedText(findTestObject('Object Repository/Page_Checkout/input__password'), 'RigbBhfdqOBGNlJIWM1ClA==')

WebUI.setEncryptedText(findTestObject('Object Repository/Page_Checkout/input__confirm'), 'RigbBhfdqOBGNlJIWM1ClA==')

WebUI.verifyElementAttributeValue(findTestObject('Page_Checkout/input_Zone  Region_shipping_address'), 'checked', 'true', 
    0)

WebUI.click(findTestObject('Object Repository/Page_Checkout/input_My delivery address is same as the bi_403b46'))

WebUI.click(findTestObject('Object Repository/Page_Checkout/label_Cash on Delivery'))

WebUI.click(findTestObject('Object Repository/Page_Checkout/input_By placing the order, you agree to ou_8f4401'))

WebUI.click(findTestObject('Object Repository/Page_Checkout/input_Cash on Delivery_cash-submit-button'))

WebUI.click(findTestObject('Object Repository/Page_Checkout/a_Go to order history'))

WebUI.verifyElementPresent(findTestObject('Object Repository/Page_My Account/td_2022-08-12 092618'), 0)

WebUI.verifyElementText(findTestObject('Object Repository/Page_My Account/td_230.00'), '$230.00')

WebUI.verifyElementText(findTestObject('Object Repository/Page_My Account/label_Pending'), 'Pending')

WebUI.closeBrowser()

