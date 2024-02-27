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

WebUI.maximizeWindow()

WebUI.navigateToUrl('http://localhost/login')

WebUI.setText(findTestObject('Object Repository/input_Username_username'), 'user1')

WebUI.setEncryptedText(findTestObject('Object Repository/input_Password_password'), 'RigbBhfdqODKcAsiUrg+1Q==')

WebUI.click(findTestObject('Object Repository/input_Password_btn btn-primary'))

WebUI.click(findTestObject('Object Repository/li_Groups'))

WebUI.click(findTestObject('Object Repository/li_Groups_1'))

WebUI.click(findTestObject('Object Repository/div_Groups'))

WebUI.click(findTestObject('Object Repository/li_Groups'))

WebUI.click(findTestObject('Object Repository/li_Add Group'))

WebUI.click(findTestObject('Object Repository/input_Public (Everyone can see this group a_1f6620'))

WebUI.setText(findTestObject('Object Repository/input_Group Name_groupname'), 'User1 group')

WebUI.click(findTestObject('Object Repository/a_Save'))

WebUI.setText(findTestObject('Object Repository/textarea_Post_post'), 'User1 (creator) make post')

WebUI.click(findTestObject('Object Repository/input_Post_btn btn-primary ossn-wall-post'))

WebUI.click(findTestObject('Object Repository/i_OSSN_fa fa-sort-down'))

WebUI.click(findTestObject('Object Repository/a_Log out'))

WebUI.click(findTestObject('Object Repository/a_Login'))

WebUI.setText(findTestObject('Object Repository/input_Username_username'), 'user2')

WebUI.setEncryptedText(findTestObject('Object Repository/input_Password_password'), 'RigbBhfdqODKcAsiUrg+1Q==')

WebUI.click(findTestObject('Object Repository/input_Password_btn btn-primary'))

WebUI.click(findTestObject('Object Repository/li_Groups'))

WebUI.click(findTestObject('Object Repository/li_Groups_1'))

WebUI.click(findTestObject('Object Repository/a_User1 group'))

WebUI.click(findTestObject('Object Repository/a_Join Group'))

WebUI.click(findTestObject('Object Repository/i_OSSN_fa fa-sort-down'))

WebUI.click(findTestObject('Object Repository/a_Log out_1'))

WebUI.click(findTestObject('Object Repository/a_Login'))

WebUI.setText(findTestObject('Object Repository/input_Username_username'), 'user1')

WebUI.setEncryptedText(findTestObject('Object Repository/input_Password_password'), 'RigbBhfdqODKcAsiUrg+1Q==')

WebUI.click(findTestObject('Object Repository/input_Password_btn btn-primary'))

WebUI.click(findTestObject('Object Repository/i_Log out_fa fa-globe-americas'))

WebUI.click(findTestObject('Object Repository/li_user 2 has requested to join User1 group'))

WebUI.click(findTestObject('Object Repository/a_Approve'))

WebUI.click(findTestObject('Object Repository/li_Groups'))

WebUI.click(findTestObject('Object Repository/li_User1 group'))

WebUI.verifyElementText(findTestObject('Object Repository/p_2'), '2')

WebUI.click(findTestObject('Object Repository/i_OSSN_fa fa-sort-down'))

WebUI.click(findTestObject('Object Repository/a_Log out_1_2'))

WebUI.closeBrowser()

