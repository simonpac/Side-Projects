tell application "System Preferences"
	
	quit
	delay 1
	launch
	activate
	
	-- Tells System Events which ten presses option and command keys
	tell application "System Events"
		key down {option, command}
	end tell
	
	-- Opens up the display settings
	reveal pane id "com.apple.preference.displays"
	
	-- Tells System Events which ten presses option and command keys
	tell application "System Events"
		key up {option, command}
		
		-- Opens up display settings for my specific monitor 'DELL U2312 HM' and rotates the monitor horizontally
		-- Finally, the display settings closes, then system prefences closes, the program then stops.
		tell process "System Preferences"
			tell window "DELL U2312HM"
				click pop up button "Rotation:" of tab group 1
				keystroke "Standard" & return
				tell application "System Preferences"
					quit
				end tell
			end tell
		end tell
	end tell
end tell

