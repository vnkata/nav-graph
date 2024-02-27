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

WebUI.mouseOver(findTestObject('Object Repository/Page_Home/a_Shop'))

WebUI.click(findTestObject('Object Repository/Page_Home/a_Bed'))

WebUI.click(findTestObject('Object Repository/Page_Bed/input_Checkout_j2store-cart-button btn btn-primary_1'))

WebUI.click(findTestObject('Object Repository/Page_Bed/input_Checkout_j2store-cart-button btn btn-primary_2'))

WebUI.verifyElementText(findTestObject('Object Repository/Page_Bed/span_2 item(s) - 230.00'), '2 item(s) - $230.00')

WebUI.mouseOver(findTestObject('Object Repository/Page_Bed/div_2 item(s) - 230.00'))

WebUI.verifyElementText(findTestObject('Object Repository/Page_Bed/strong_Bed2'), 'Bed2')

WebUI.verifyElementText(findTestObject('Object Repository/Page_Bed/strong_Bed1'), 'Bed1')

