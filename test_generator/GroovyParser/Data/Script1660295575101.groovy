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

WebUI.click(findTestObject('Object Repository/Page_Home/a_Blog'))

WebUI.click(findTestObject('Object Repository/Page_Blog/a_Homepage using SiteOrigin Page Builder'))

WebUI.verifyElementText(findTestObject('Object Repository/Page_Homepage using SiteOrigin Page Builder/a_Homepage using SiteOrigin Page Builder'), 
    'Homepage using SiteOrigin Page Builder')

WebUI.verifyElementClickable(findTestObject('Object Repository/Page_Homepage using SiteOrigin Page Builder/span_Blog'))

WebUI.verifyElementVisible(findTestObject('Object Repository/Page_Homepage using SiteOrigin Page Builder/time_29 August 2017'))

WebUI.verifyElementVisible(findTestObject('Object Repository/Page_Homepage using SiteOrigin Page Builder/span_Super User'))

WebUI.verifyElementVisible(findTestObject('Object Repository/Page_Homepage using SiteOrigin Page Builder/img'))

WebUI.click(findTestObject('Object Repository/Page_Homepage using SiteOrigin Page Builder/span_Next'))

WebUI.verifyElementText(findTestObject('Object Repository/Page_Picking the Perfect Product/a_Picking the Perfect Product'), 
    'Picking the Perfect Product')

WebUI.verifyElementVisible(findTestObject('Object Repository/Page_Picking the Perfect Product/a_Prev'))

WebUI.click(findTestObject('Object Repository/Page_Picking the Perfect Product/span_Prev'))

WebUI.verifyElementText(findTestObject('Object Repository/Page_Homepage using SiteOrigin Page Builder/a_Homepage using SiteOrigin Page Builder'), 
    'Homepage using SiteOrigin Page Builder')

WebUI.closeBrowser()

