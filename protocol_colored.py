from opentrons import protocol_api

metadata = {
	"protocolName": "Serial Dilution with Color",
	"description": """This protocol is an extension of the dilution tutorial executed
		by protocol.py. It shows the dilution of a colored sample in a clear dilutent.""",
	"author": "Smriti Gounder"
}


# Using Flex robot,
requirements = {"robotType": "Flex", "apiLevel": "2.16"}


def run(protocol: protocol_api.ProtocolContext):
  tips = protocol.load_labware("opentrons_flex_96_tiprack_200ul", "D1")
  reservoir = protocol.load_labware("nest_12_reservoir_15ml", "D2")
  plate = protocol.load_labware("nest_96_wellplate_200ul_flat", "D3")
  trash = protocol.load_trash_bin("A3")
  left_pipette = protocol.load_instrument("flex_1channel_1000", "left", tip_racks=[tips])

  # Define liquids with colors
  dilutent = protocol.define_liquid(
    name="Diluent",
    description="Diluent buffer",
    display_color = None
  )
  sample = protocol.define_liquid(
    name="Sample",
    description="Concentrated sample solution",
    display_color= "#FF0000"
  )

  # Load liquids into wells (volume in µL)
  reservoir["A1"].load_liquid(liquid=dilutent, volume=15000)
  reservoir["A2"].load_liquid(liquid=sample, volume=15000)

  left_pipette.transfer(100, reservoir["A1"], plate.wells())

  for i in range(8):
    row = plate.rows()[i]
    left_pipette.transfer(100, reservoir["A2"], row[0], mix_after=(3, 50))
    left_pipette.transfer(100, row[:11], row[1:], mix_after=(3, 50))
