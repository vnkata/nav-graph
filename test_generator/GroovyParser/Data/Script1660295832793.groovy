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

WebUI.click(findTestObject('Object Repository/Page_Home/img_Recent products_j2store-img-responsive _cded70'))

WebUI.click(findTestObject('Object Repository/Page_Bed2/a_Specifications'))

WebUI.verifyElementVisible(findTestObject('Object Repository/Page_Bed2/td_Dimension (L x W x H)'))

WebUI.verifyElementVisible(findTestObject('Object Repository/Page_Bed2/td_Weight'))

WebUI.click(findTestObject('Object Repository/Page_Bed2/a_Description'))

WebUI.verifyElementText(findTestObject('Object Repository/Page_Bed2/h2_Product Description'), 'Product Description')

WebUI.verifyElementVisible(findTestObject('Object Repository/Page_Bed2/p_Lorem Ipsum is simply dummy text of the p_695810'))

WebUI.closeBrowser()

