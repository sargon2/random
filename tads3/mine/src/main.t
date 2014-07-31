#charset "us-ascii"

#include <adv3.h>
#include <en_us.h>

versionInfo: GameID
    name = 'TADS 3 Starter Game'
    byline = 'by An Author'
    htmlByline = 'by <a href="mailto:your-email@your-address.com">
                  YOUR NAME</a>'
    version = '1.0'
    authorEmail = 'YOUR NAME <your-email@your-address.com>'
    desc = 'CUSTOMIZE - this should provide a brief description of
            the game, in plain text format.'
    htmlDesc = 'CUSTOMIZE - this should provide a brief description
                of the game, in <b>HTML</b> format.'

    showCredit()
    {
        /* show our credits */
        "Put credits for the game here. ";

        "\b";
    }
    showAbout()
    {
        "Put information for players here.  Many authors like to mention
        any unusual commands here, along with background information on
        the game (for example, the author might mention that the game
        was created as an entry for a particular competition). ";
    }
;

me: Actor
	/* the initial location */
	location = FieldS
	referralPerson = FirstPerson
;

gameMain: GameMainDef
	/* the initial player character is 'me' */
	initialPlayerChar = me

	showIntro()
	{
		"Welcome to the TADS 3 Starter Game!\b";
	}

	showGoodbye()
	{
		"<.p>Thanks for playing!\b";
	}
;
