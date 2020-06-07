json = require "json"

controller = {
	"P1 Right":false,
	"P1 Left":false,
	"P1 Up":false,
	"P1 Down":false,
	"P1 A":false,
	"P1 B":false
}

function startClient()
	local romName = gameinfo.getromname()
	print("Playing " .. romName)
	comm.socketServerSend(romName)
	savestate.loadslot(1)
end

function frameLoop()
	while true do
		-- Update our training Data
			--MegaMan Data
				--Hp 
				--Postion
			--Objects
				--Position
				--Size
				--HP
			--Tiles
		-- Send the triaing Data

		-- Recieve Controller Data

		-- Send Controller Data into Bizhawk
		joypad.set(controller)
		-- Advance the frame
		emu.frameadvance()
	end
end

startClient()
frameLoop()