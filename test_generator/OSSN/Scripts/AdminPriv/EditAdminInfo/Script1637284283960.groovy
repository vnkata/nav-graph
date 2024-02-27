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

WebUI.click(findTestObject('Object Repository/button_Log out_navbar-toggler'))

WebUI.click(findTestObject('Object Repository/a_User Manager'))

WebUI.click(findTestObject('Object Repository/a_List Users'))

WebUI.click(findTestObject('Object Repository/a_Edit'))

WebUI.click(findTestObject('Object Repository/body_Log out                               _16be5b'))

WebUI.setText(findTestObject('Object Repository/input_First Name_firstname'), 'AdminAdmin')

WebUI.setText(findTestObject('Object Repository/input_Last Name_lastname'), '100')

WebUI.selectOptionByValue(findTestObject('Object Repository/select_Normal     Administrator'), 'normal', true)

WebUI.selectOptionByValue(findTestObject('Object Repository/select_Normal     Administrator'), 'admin', true)

WebUI.click(findTestObject('Object Repository/input_Type_btn btn-success btn-sm'))

WebUI.verifyElementText(findTestObject('div_User updated (2)'), 'User updated!')

WebUI.click(findTestObject('Object Repository/i_Log out_fa fa-bars fa-3'))

WebUI.click(findTestObject('Object Repository/a_Log out'))

WebUI.navigateToUrl('localhost/login')

WebUI.setText(findTestObject('Object Repository/input_Username_username'), 'admin1')

WebUI.setEncryptedText(findTestObject('Object Repository/input_Password_password'), 'RigbBhfdqODKcAsiUrg+1Q==')

WebUI.click(findTestObject('Object Repository/input_Password_btn btn-primary'))

WebUI.click(findTestObject('Object Repository/i_Groups_fa fa-th-list'))

WebUI.verifyElementText(findTestObject('Object Repository/a_AdminAdmin 100'), 'AdminAdmin 100')

WebUI.click(findTestObject('Object Repository/a_AdminAdmin 100'))

WebUI.verifyElementText(findTestObject('Object Repository/div_AdminAdmin 100'), 'AdminAdmin 100')

WebUI.verifyElementText(findTestObject('Object Repository/div_Administrator'), 'Administrator')

WebUI.click(findTestObject('Object Repository/i_OSSN_fa fa-sort-down'))

WebUI.click(findTestObject('Object Repository/a_Log out'))

WebUI.click(findTestObject('Object Repository/a_Login'))

WebUI.setText(findTestObject('Object Repository/input_Username_username'), 'admin1')

WebUI.setEncryptedText(findTestObject('Object Repository/input_Password_password'), 'RigbBhfdqODKcAsiUrg+1Q==')

WebUI.click(findTestObject('Object Repository/input_Password_btn btn-primary'))

WebUI.setText(findTestObject('Object Repository/textarea_Post_post'), 'adminadmin 100 make post')

WebUI.click(findTestObject('Object Repository/input_Tag Friends_btn btn-primary ossn-wall-post'))

WebUI.click(findTestObject('Object Repository/i_Groups_fa fa-th-list'))

WebUI.click(findTestObject('Object Repository/a_AdminAdmin 100'))

WebUI.verifyElementText(findTestObject('Object Repository/a_AdminAdmin 100 (1)'), 'AdminAdmin 100')

WebUI.click(findTestObject('Object Repository/i_Privacy_fa fa fa-ellipsis-h'))

WebUI.click(findTestObject('Object Repository/a_Delete'))

WebUI.click(findTestObject('Object Repository/i_OSSN_fa fa-sort-down'))

WebUI.click(findTestObject('Object Repository/a_Log out_1'))

WebUI.navigateToUrl('localhost/administrator')

WebUI.setText(findTestObject('Object Repository/input_Username_username'), 'admin1')

WebUI.setEncryptedText(findTestObject('Object Repository/input_Password_password'), 'RigbBhfdqODKcAsiUrg+1Q==')

WebUI.click(findTestObject('Object Repository/input_Password_btn btn-primary'))

WebUI.verifyElementText(findTestObject('Object Repository/div_You are now logged in'), 'You are now logged in!')

WebUI.click(findTestObject('Object Repository/i_Log out_fa fa-bars'))

WebUI.click(findTestObject('Object Repository/a_User Manager'))

WebUI.click(findTestObject('Object Repository/a_List Users'))

WebUI.click(findTestObject('Object Repository/a_Edit'))

WebUI.setText(findTestObject('Object Repository/input_First Name_firstname'), 'Admin')

WebUI.setText(findTestObject('Object Repository/input_Last Name_lastname'), '1')

WebUI.selectOptionByValue(findTestObject('Object Repository/select_Normal     Administrator'), 'normal', true)

WebUI.selectOptionByValue(findTestObject('Object Repository/select_Normal     Administrator'), 'admin', true)

WebUI.click(findTestObject('Object Repository/input_Type_btn btn-success btn-sm'))

WebUI.verifyElementText(findTestObject('div_User updated (2)'), 'User updated!')

WebUI.click(findTestObject('Object Repository/i_Log out_fa fa-bars fa-3'))

WebUI.click(findTestObject('Object Repository/a_Log out_1'))

WebUI.closeBrowser()

