<?
	$title = "Circumventing HTTP Referrer checking with Internet Explorer 5/6";
	print "<html><head><title>$title</title></head><body bgcolor=\"#FFFFFF\">";
	print "<h2>$title</h2><hr size=\"1\" width=\"800\" color=\"black\" align=\"left\">";
?><table width="800"><tr><td>We've all seen it.<br><br>
Someone sends you an URL via email, Instant Messaging, IRC, or the like.  You click on it with the intention to see the funny picture
or glean that fragment of oh-so-needed information.<br>
But instead, you get something like this:<br><br>
<table border="0" style="border: 1px solid black"><tr><td>
<h2>HTTP/1.1 403 Forbidden</h2><br><h3>This site does not allow offsite or "hot" linking.</h3></td></tr></table><br>
<br>
The link worked fine for the person who sent it to you.  What happened?<br>
<br>
It turns out that this is caused by uninformed sysadmins trying to lower their bandwidth costs by disallowing linking.  Why this doesn't defeat the purpose of serving content I don't know, but it seems to be a popular trend.<br><br>
They try to stop linking by checking something called HTTP Referrer.  This is something your browser sends to the server every time you go to
a web page as part of the HTTP protocol.<br>
<br>
What most people don't realize is how incredibly easy it is to circumvent this little piece of RFC abuse.<br>
(The <a href="http://www.ietf.org/rfc/rfc2616.txt">RFC</a> states that HTTP Referer[sic] was intended to help sysadmins track down broken links on their site or generate backreferences, not for security or traffic management.)<br>
<br>
Some browsers (like <a href="http://opera.com">Opera</a>) offer built-in control of HTTP Referrer, allowing users to unset it as they wish.<br>
This is a step in the right direction, but a lot of people don't know that it's almost as easy to get around this problem in IE.<br>
<br>
I've set up a script that checks referrer and spits out a simple error if it's incorrect.  It functions in the same way that all referrer checking scripts do.<br>
<a href="http://referrer.xem.us/check-referrer.php">http://referrer.xem.us/check-referrer.php</a><br>
Go ahead and try it.  If you're like me and using standard Internet Explorer, it will give you an annoying error.<br>
<br>
Now, for the magic.  Your window should look similar to this:<br>
<img src="pre.gif"><br><br>
See that little icon next to the URL? Simply drag it into the page itself:<br>
<img src="action.gif"><br>
<br>
And viola!  This makes IE think you typed the URL in yourself, and it sends an empty referrer.  The page loads fine, you get the information you need, and everyone's happy (except that bandwidth-miser sysadmin, but he's not fit to admin a fish tank).<br>
Try it with my script.  It works wonders.<br>
(If it doesn't, try hitting f5 or control-f5).<br>
<img src="post.gif"><br>
<br>
-- sargon</td></tr></table>
