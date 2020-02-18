AUTHOR: Kacper Oreszczuk (at gmail), January 2020

OVERVIEW:

This program is dedicated for technical assistants at conferences, meetings etc., where there is need for tracking time used by speakers and for reminding audience of the name of current speaker and next item in the agenda. Program is meant do be displayed on separate monitor or projector, which is visible for speaker, audience and chairman. 

Agenda is defined for whole day in JSON-like configuration file. Operator can define stages with no time limit (such as "Announcement", "Coffee Break") or stages with time limit (presentations). 

Stages are switched to next manually by operator (return/numpad_enter/arrow_right for next and backspace/arrow_left for previous). If stage has time limit, timer starts stopped. After speaker prepares for the presentation, operator turns on counting on the timer. When counter drops below warning time defined in configuration file, clock changes color from green to yellow. When timer reaches zero, timer turns red and stops at 0:00 until operator switches to next speaker. For stages with no time limit, current time is displayed (only 24H notation).

FEATURES:

1. Option in configuration file allows to change font sizes. Default value of 100 is well suited for large TV in large audience hall. If the room is small or the timer is displayed on large projector screen, downsized font may look better.

2. Very long speaker names are resized to fit screen.

3. Unicode support. Keep config.json file in UTF-8 encoding.

4. Few shortcuts are available for live-tweaking the agenda:
    A - Operator can instantly add announcement as a next stage, when requested by the chairman. Exact name of such inserted event is defined in config.json file.
    S - Swaps current presentation with the next. Useful when there are technical problems with speaker's laptop.
    D - Deletes next stage.
	
REQUIREMENTS: 
 - Rename config.json.example file to config.json before using!
 - Requires pygame python library, if it is not launched from executable.

ATTENTION: This was tested on Windows 10. On Windows 7 there are some problems with fonts. Python library pygame detects Cambria font as needed, but fails to display it properly. Not debugged. Not tested on Linux.

NOTE: If you make some nice upgrades to this software, you may notify me. I will be glad to see them and use them.
