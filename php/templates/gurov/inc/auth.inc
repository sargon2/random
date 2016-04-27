<?
        function fail_auth() {
                Header("WWW-Authenticate: Basic realm=\"Ramcon Administration\"");
                Header("HTTP/1.0 401 Unauthorized");
                print "401 Unauthorized\n";
                exit;
        }

       function userauth($user, $pwd) {
		global $DEFS;
                if (!$user || !$pwd) return 0;
                $asdf = mysql_query("select * from USERS where username='$user' and  password=PASSWORD('$pwd')");

                if (!mysql_numrows($asdf))
                	return 0;
			else {
			$DEFS = mysql_fetch_array($asdf);
                	return 1;
		}
        }



   if (!userauth($PHP_AUTH_USER, $PHP_AUTH_PW)) fail_auth();


?>
