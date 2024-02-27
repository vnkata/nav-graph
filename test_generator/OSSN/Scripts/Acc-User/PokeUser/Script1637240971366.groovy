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

WebUI.maximizeWindow()

WebUI.setText(findTestObject('Object Repository/input_Username_username'), 'user1')

WebUI.setEncryptedText(findTestObject('Object Repository/input_Password_password'), 'RigbBhfdqODKcAsiUrg+1Q==')

WebUI.click(findTestObject('Object Repository/input_Password_btn btn-primary'))

WebUI.verifyElementText(findTestObject('Object Repository/a_user 1'), 'user 1')

WebUI.click(findTestObject('Object Repository/li_Groups'))

WebUI.click(findTestObject('Object Repository/li_Groups_1'))

WebUI.click(findTestObject('Object Repository/div_People'))

WebUI.click(findTestObject('Object Repository/a_Admin 1'))

WebUI.click(findTestObject('Object Repository/a_Message_btn-action'))

WebUI.click(findTestObject('Object Repository/a_Poke'))

WebUI.verifyElementText(findTestObject('Object Repository/div_You have poked Admin 1'), 'You have poked Admin 1!')

WebUI.click(findTestObject('Object Repository/li_Groups'))

WebUI.click(findTestObject('Object Repository/li_Groups_1'))

WebUI.click(findTestObject('Object Repository/div_People'))

WebUI.click(findTestObject('Object Repository/a_user 2 (1)'))

WebUI.click(findTestObject('Object Repository/a_Message_btn-action (1)'))

WebUI.click(findTestObject('Object Repository/a_Poke (1)'))

WebUI.verifyElementText(findTestObject('Object Repository/div_You have poked user 2'), 'You have poked user 2!')

WebUI.click(findTestObject('Object Repository/li_Groups'))

WebUI.click(findTestObject('Object Repository/li_Groups_1'))

WebUI.click(findTestObject('Object Repository/div_People'))

WebUI.click(findTestObject('Object Repository/a_Admin 2'))

WebUI.click(findTestObject('Object Repository/i_Message_fa fa-sort-down'))

WebUI.click(findTestObject('Object Repository/a_Poke (2)'))

WebUI.verifyElementText(findTestObject('Object Repository/div_You have poked Admin 2'), 'You have poked Admin 2!')

WebUI.click(findTestObject('Object Repository/a'))

WebUI.click(findTestObject('Object Repository/a_Log out'))

WebUI.click(findTestObject('Object Repository/a_Login'))

WebUI.setText(findTestObject('Object Repository/input_Username_username'), 'admin1')

WebUI.setEncryptedText(findTestObject('Object Repository/input_Password_password'), 'RigbBhfdqODKcAsiUrg+1Q==')

WebUI.click(findTestObject('Object Repository/input_Password_btn btn-primary'))

WebUI.click(findTestObject('Object Repository/i_Log out_fa fa-globe-americas'))

WebUI.verifyElementText(findTestObject('Object Repository/div_user 1 has poked you'), 'user 1 has poked you!')

WebUI.click(findTestObject('Object Repository/a_Mark all as read'))

WebUI.click(findTestObject('Object Repository/i_OSSN_fa fa-sort-down'))

WebUI.click(findTestObject('Object Repository/a_Log out'))

WebUI.click(findTestObject('Object Repository/a_Login'))

WebUI.setText(findTestObject('Object Repository/input_Username_username'), 'user2')

WebUI.setEncryptedText(findTestObject('Object Repository/input_Password_password'), 'RigbBhfdqODKcAsiUrg+1Q==')

WebUI.click(findTestObject('Object Repository/input_Password_btn btn-primary'))

WebUI.verifyElementText(findTestObject('Object Repository/a_user 2'), 'user 2')

WebUI.click(findTestObject('Object Repository/i_Log out_fa fa-globe-americas'))

WebUI.verifyElementText(findTestObject('Object Repository/div_user 1 has poked you'), 'user 1 has poked you!')

WebUI.click(findTestObject('Object Repository/a_Mark all as read_1'))

WebUI.click(findTestObject('Object Repository/i_OSSN_fa fa-sort-down'))

WebUI.click(findTestObject('Object Repository/a_Log out_1'))

WebUI.click(findTestObject('Object Repository/a_Login'))

WebUI.setText(findTestObject('Object Repository/input_Username_username'), 'admin2')

WebUI.setEncryptedText(findTestObject('Object Repository/input_Password_password'), 'RigbBhfdqODKcAsiUrg+1Q==')

WebUI.click(findTestObject('Object Repository/input_Password_btn btn-primary'))

WebUI.verifyElementText(findTestObject('Object Repository/a_Admin 2'), 'Admin 2')

WebUI.click(findTestObject('Object Repository/i_Log out_fa fa-globe-americas'))

WebUI.verifyElementText(findTestObject('Object Repository/div_user 1 has poked you'), 'user 1 has poked you!')

WebUI.click(findTestObject('Object Repository/a_Mark all as read_1_2'))

WebUI.click(findTestObject('Object Repository/i_OSSN_fa fa-sort-down'))

WebUI.verifyElementText(findTestObject('Object Repository/div_Successfully marked all as read'), 'Successfully marked all as read')

WebUI.click(findTestObject('Object Repository/a_Log out_1_2'))

WebUI.closeBrowser()

