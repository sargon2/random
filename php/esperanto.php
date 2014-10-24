<html><body>
	<script type="text/javascript" language="JavaScript"><!--
	function Process(e) {
		if (document.layers)
			Key = e.which;
		else
			Key = window.event.keyCode;
		if(Key == 120 || Key == 88) { <? // x ?>
			len = String(myform.asdf.value).length;
			lastchar = String(myform.asdf.value).substr(len-1, len);
			if(lastchar == "c") {
				myform.asdf.value = String(myform.asdf.value).substr(0,len-1) + 'c^';
			}
			<? // Cancel the keystroke by moving focus, we lose the cursor position here ?>
			myform.asdf2.focus();
		}
	}

	function focusasdf() {
		myform.asdf.focus();
		myform.asdf.value = myform.asdf.value; <? //hack to move cursor ?>
	}

	function clearasdf2() {
		myform.asdf2.value = "";
	}
	//--></script>
	
	<form id="myform">
	<textarea name="asdf" rows="25" cols="80" onKeyPress="Process()" onKeyDown="Process()"></textarea>
	<textarea name="asdf2" rows="1" cols="1" style="overflow: hidden" onfocus="focusasdf()" onchange="clearasdf2()"></textarea>
	</form>
</body></html>
