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

WebUI.click(findTestObject('Object Repository/Page_Home/a_Go Shopping'))

WebUI.click(findTestObject('Object Repository/Page_Shop/img_Shop_j2store-img-responsive j2store-pro_3c5d32'))

WebUI.selectOptionByValue(findTestObject('Object Repository/Page_Simple/select_-- Select --                        _880746'), 
    '13', true)

WebUI.click(findTestObject('Object Repository/Page_Simple/label_Large                     (          _ef0628'))

WebUI.click(findTestObject('Object Repository/Page_Simple/input_Expected Delivery date_product_option7'))

WebUI.click(findTestObject('Object Repository/Page_Simple/button_Now'))

WebUI.click(findTestObject('Object Repository/Page_Simple/button_Done'))

WebUI.setText(findTestObject('Object Repository/Page_Simple/textarea_Additional information_product_option8'), 'abcdefgh')

WebUI.click(findTestObject('Object Repository/Page_Simple/label_Adidas                           (   _748489'))

WebUI.click(findTestObject('Object Repository/Page_Simple/label_Hat                           (      _e8e9be'))

WebUI.setText(findTestObject('Object Repository/Page_Simple/input_Checkout_product_qty'), '2')

WebUI.click(findTestObject('Object Repository/Page_Simple/input_Checkout_j2store-cart-button btn btn-primary'))

WebUI.verifyElementText(findTestObject('Object Repository/Page_Simple/p_Item added to cart.Checkout'), 'Item added to cart. Checkout')

WebUI.click(findTestObject('Object Repository/Page_Simple/a_Checkout'))

WebUI.verifyElementPresent(findTestObject('Object Repository/Page_Cart/a_200.00_btn btn-small btn-danger btn-xs j2_e2024e'), 
    0)

