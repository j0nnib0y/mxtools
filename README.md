# mxtools
Tools for messing around with Mania-Exchange.com

### downloader.py
Downloads all maps with the specified attributes from sm.mania-exchange.com or tm.mania-exchange.com.

**Usage:**

*downloader.py*    *tm* or *sm*    *arg1=val1 arg2=val2*

**Possible arguments:**
- path (download path, must exist already)
- limit (number of maps which get downloaded)

... and all arguments from this site at Track Search: https://api.mania-exchange.com/documents/reference

**Examples:**
- `python3 downloader.py tm path=./Nadeo author=nadeo gv=1` (downloads all Nadeo maps which are already updated to ManiaPlanet 4 to the directory `Nadeo`)
- `python3 downloader.py tm limit=50 environments=4 gv=1` (downloads 50 first found Lagoon maps which are updated to ManiaPlanet 4)
