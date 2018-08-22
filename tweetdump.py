# IMPORT MODULES

import twint

# CREATE THE SEARCH PARAMETERS OBJECT

searchParameters = twint.Config()

# SET SEARCH PARAMETERS (referTo: https://github.com/twintproject/twint/wiki/Module)

searchParameters.Username = "LulaOficial"
searchParameters.Output = "LulaOficial_until2014.json"
searchParameters.Stats = True
searchParameters.Store_json = True
searchParameters.Profile_full = True
searchParameters.Until = "2014-12-31"

# RUN TWITTER SEARCH

twint.run.Search(searchParameters)
