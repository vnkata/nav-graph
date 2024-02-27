WebUI.callTestCase(this.findTestCase(tCC Components/tCC tsv Open For Edit), [:], FailureHandling.STOP_ON_FAILURE)
WebUI.delay(1)
if ((WebUI.getElementHeight(this.findTestObject(Page_tCC translationNotes/div_Icon_Toolbar)) != 48)) {
	this.println(((((ERROR: The icon bar height is  + WebUI.getElementHeight(this.findTestObject(Page_tCC translationNotes/div_Icon_Toolbar))) +  pixels and ) + 48) +  was expected.))
	CustomKeywords.'unfoldingWord_Keywords.SendMessage.SendFailMessage'(((((Test failed because the icon bar height is  + WebUI.getElementHeight(this.findTestObject(Page_tCC translationNotes/div_Icon_Toolbar))) +  pixels and ) + 48) +  was expected.))
}
WebUI.click(this.findTestObject(Page_tCC translationNotes/button_ViewColumns))
WebUI.click(this.findTestObject(Page_tCC translationNotes/columns_Parmed, [column:ID]))
WebUI.click(this.findTestObject(Page_tCC translationNotes/btnX_CloseColumns))
if (((WebUI.getText(this.findTestObject(Page_tCC translationNotes/p_IdRow2)) != rtc9) || (WebUI.getText(this.findTestObject(Page_tCC translationNotes/p_IdRow3)) != xyz8))) {
	this.println('ERROR: Rows are not in the expected order')
	this.println((rtc9: + WebUI.getText(this.findTestObject(Page_tCC translationNotes/p_IdRow2))))
	this.println((xyz8: + WebUI.getText(this.findTestObject(Page_tCC translationNotes/p_IdRow3))))
	CustomKeywords.'unfoldingWord_Keywords.SendMessage.SendFailMessage'('Test failed because the rows are not in the expected order.')
	WebUI.delay(10)
}
else {
	this.println('Rows are in expected order when project is opened')
}
WebUI.scrollToElement(this.findTestObject(Page_tCC translationNotes/button_MoveRow_xyz8Up), 1)
WebUI.click(this.findTestObject(Page_tCC translationNotes/button_MoveRow_xyz8Up))
if (((WebUI.getText(this.findTestObject(Page_tCC translationNotes/p_IdRow2)) != xyz8) || (WebUI.getText(this.findTestObject(Page_tCC translationNotes/p_IdRow3)) != rtc9))) {
	this.println('ERROR: Rows do not appear to have been moved')
	this.println((rtc9: + WebUI.getText(this.findTestObject(Page_tCC translationNotes/p_IdRow2))))
	this.println((xyz8: + WebUI.getText(this.findTestObject(Page_tCC translationNotes/p_IdRow3))))
	CustomKeywords.'unfoldingWord_Keywords.SendMessage.SendFailMessage'('Test failed because the rows do not appear to have been moved.')
	WebUI.delay(10)
}
else {
	this.println('Rows appear to have been moved as expected')
}
WebUI.delay(1)
WebUI.scrollToPosition(0, 2800)
WebUI.delay(1)
WebUI.click(this.findTestObject(Page_tCC translationNotes/button_MoveRow_xyz8Down))
if (((WebUI.getText(this.findTestObject(Page_tCC translationNotes/p_IdRow2)) != rtc9) || (WebUI.getText(this.findTestObject(Page_tCC translationNotes/p_IdRow3)) != xyz8))) {
	this.println('ERROR: Rows were not returned to the original order')
	this.println((rtc9: + WebUI.getText(this.findTestObject(Page_tCC translationNotes/p_IdRow2))))
	this.println((xyz8: + WebUI.getText(this.findTestObject(Page_tCC translationNotes/p_IdRow3))))
	CustomKeywords.'unfoldingWord_Keywords.SendMessage.SendFailMessage'('Test failed because the rows were not returned to the original order.')
	WebUI.delay(10)
}
else {
	this.println('Rows were returned to their original positions')
}
WebUI.scrollToElement(this.findTestObject(Page_tCC translationNotes/button_MoveRow_xyz8Up), 1)
WebUI.click(this.findTestObject(Page_tCC translationNotes/button_MoveRow_xyz8Up))
WebUI.click(this.findTestObject(Page_tCC translationNotes/button_SaveEnabled - xPath))
WebUI.delay(1)
WebUI.closeBrowser()
WebUI.callTestCase(this.findTestCase(tCC Components/tCC tsv Open For Edit), [:], FailureHandling.STOP_ON_FAILURE)
WebUI.delay(1)
WebUI.click(this.findTestObject(Page_tCC translationNotes/button_ViewColumns))
WebUI.click(this.findTestObject(Page_tCC translationNotes/columns_Parmed, [column:ID]))
WebUI.click(this.findTestObject(Page_tCC translationNotes/btnX_CloseColumns))
if (((WebUI.getText(this.findTestObject(Page_tCC translationNotes/p_IdRow2)) != xyz8) || (WebUI.getText(this.findTestObject(Page_tCC translationNotes/p_IdRow3)) != rtc9))) {
	this.println('ERROR: Rows do not appear to have been moved before the Save')
	this.println((rtc9: + WebUI.getText(this.findTestObject(Page_tCC translationNotes/p_IdRow2))))
	this.println((xyz8: + WebUI.getText(this.findTestObject(Page_tCC translationNotes/p_IdRow3))))
	CustomKeywords.'unfoldingWord_Keywords.SendMessage.SendFailMessage'('Test failed because the rows do not appear to have been moved before the Save.')
	WebUI.delay(10)
}
else {
	this.println('Rows were moved and saved as expected')
}
WebUI.delay(1)
WebUI.scrollToPosition(0, 2800)
WebUI.click(this.findTestObject(Page_tCC translationNotes/button_MoveRow_xyz8Down))
if (((WebUI.getText(this.findTestObject(Page_tCC translationNotes/p_IdRow2)) != rtc9) || (WebUI.getText(this.findTestObject(Page_tCC translationNotes/p_IdRow3)) != xyz8))) {
	this.println('ERROR: Rows were not returned to the original order')
	this.println((rtc9: + WebUI.getText(this.findTestObject(Page_tCC translationNotes/p_IdRow2))))
	this.println((xyz8: + WebUI.getText(this.findTestObject(Page_tCC translationNotes/p_IdRow3))))
	CustomKeywords.'unfoldingWord_Keywords.SendMessage.SendFailMessage'('Test failed because the rows were not returned to the original order.')
	WebUI.delay(10)
}
else {
	this.println('Rows have been returned to their original positions after save')
}
WebUI.click(this.findTestObject(Page_tCC translationNotes/button_SaveEnabled - xPath))
WebUI.delay(1)
WebUI.closeBrowser()
