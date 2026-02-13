"""ASCII art logo for Henvdall."""

LOGO = r"""                     
  	           _______  _         ‸        ______   _______  _        _       
  	 |\     /|(  ____ \( (    /|| /    \ |(  __  \ (  ___  )( \      ( \      
  	 | )   ( || (    \/|  \  ( || |   | || (  \  )| (   ) || (      | (      
  	 | (___) || (__    |   \ | || |   | || |   ) || (___) || |      | |      
  	 |  ___  ||  __)   | (\ \) |( (   ) )| |   | ||  ___  || |      | |      
  	 | (   ) || (      | | \   | \ \_/ / | |   ) || (   ) || |      | |      
  	 | )   ( || (____/\| )  \  |  \   /  | (__/  )| )   ( || (____/\| (____/\
  	 |/     \|(_______/|/    )_)   \_/   (______/ |/     \|(_______/(_______/
                                                                        
                   
"""

TAGLINE = "The Gatekeeper of Environment Variables"


def get_logo_with_tagline() -> str:
    """Return the complete logo with tagline."""
    return f"{LOGO}\n{'Henvdall':^98}\n{TAGLINE:^98}\n"
