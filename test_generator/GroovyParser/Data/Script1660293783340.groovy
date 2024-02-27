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

WebUI.click(findTestObject('Object Repository/Page_Home/img_clothing'))

WebUI.selectOptionByLabel(findTestObject('Object Repository/Page_Shop/select_Sort Product byName (A - Z)Name (Z -_32ee88'), 
    'Name (A - Z)', false)

WebUI.click(findTestObject('Object Repository/Page_Shop/eur_header'))

WebUI.verifyElementAttributeValue(findTestObject('Object Repository/Page_Shop/eur_header'), 'class', 'active', 0)

WebUI.verifyElementText(findTestObject('Object Repository/Page_Shop/div_11'), '€11')

WebUI.click(findTestObject('Object Repository/Page_Shop/usd_header'))

WebUI.verifyElementAttributeValue(findTestObject('Object Repository/Page_Shop/usd_header'), 'class', 'active', 0)

WebUI.verifyElementText(findTestObject('Object Repository/Page_Shop/div_13.00'), '$13.00')

WebUI.click(findTestObject('Object Repository/Page_Shop/fkp_header'))

WebUI.verifyElementAttributeValue(findTestObject('Object Repository/Page_Shop/fkp_header'), 'class', 'active', 0)

WebUI.verifyElementText(findTestObject('Object Repository/Page_Shop/div_10'), '£10')

WebUI.click(findTestObject('Object Repository/Page_Shop/inr_header'))

WebUI.verifyElementAttributeValue(findTestObject('Object Repository/Page_Shop/inr_header'), 'class', 'active', 0)

WebUI.verifyElementText(findTestObject('Object Repository/Page_Shop/div_832'), '₹832')

WebUI.closeBrowser()

