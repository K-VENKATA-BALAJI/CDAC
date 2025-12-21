from openpyxl import Workbook
import os

# Create data directory if it doesn't exist
data_dir = os.path.join(os.path.dirname(__file__), 'data')
os.makedirs(data_dir, exist_ok=True)

# Create PCB Specifications Excel file
wb_specs = Workbook()
ws_specs = wb_specs.active
ws_specs.title = "PCB Specifications"

# Headers
ws_specs.append(["Field", "Option1", "Option2", "Option3", "Option4", "Option5", "Option6"])

# Specification options
specs_data = [
    ["Num of Layers", "2", "4", "6", "8", "10", "12"],
    ["Material", "FR-4", "FR-4 High Tg", "Rogers", "Aluminum", "Flex", "Rigid-Flex"],
    ["Surface Finish", "HASL", "ENIG", "OSP", "Immersion Silver", "Immersion Tin", "Hard Gold"],
    ["Track / Spacing", "6/6 mil", "5/5 mil", "4/4 mil", "3/3 mil", "2/2 mil", "1/1 mil"],
    ["Via Filling", "Tented", "Filled", "Non-filled", "Via in Pad", "Blind Via", "Buried Via"],
    ["Via Hole/Pad", "0.3/0.6", "0.2/0.5", "0.15/0.4", "0.1/0.3", "0.25/0.55", "0.35/0.65"],
    ["Thickness", "1.6mm", "1.0mm", "0.8mm", "2.0mm", "1.2mm", "1.4mm"],
    ["Copper Thickness", "1 oz", "0.5 oz", "2 oz", "3 oz", "4 oz", "0.25 oz"],
    ["Size", "100x100mm", "50x50mm", "150x150mm", "200x200mm", "75x75mm", "125x125mm"],
    ["Single Ended Impedance", "Yes", "No"],
    ["Colour", "Green", "Blue", "Red", "Yellow", "White", "Black"],
    ["Differential Impedance", "Yes", "No"],
]

for row in specs_data:
    ws_specs.append(row)

wb_specs.save(os.path.join(data_dir, 'pcb_specifications.xlsx'))
print("Created pcb_specifications.xlsx")

# Create PCB Vendors Excel file
wb_vendors = Workbook()
ws_vendors = wb_vendors.active
ws_vendors.title = "PCB Vendors"

# Headers
ws_vendors.append(["Vendor Name", "Base Rate", "Layer Multiplier", "Material Multiplier", "Size Multiplier"])

# Vendor data with base rates and multipliers
vendors_data = [
    ["VendorTech Inc", 25.00, 1.0, 1.2, 1.0],
    ["CircuitPro Ltd", 22.50, 1.1, 1.1, 1.1],
    ["PCB Masters", 50.00, 1.3, 1.5, 1.2],
    ["ElectroBoards Co", 20.00, 1.2, 1.0, 1.1],
    ["QuickPCB Solutions", 28.00, 1.0, 1.3, 1.0],
    ["Advanced Circuits", 35.00, 1.1, 1.2, 1.1],
]

for row in vendors_data:
    ws_vendors.append(row)

wb_vendors.save(os.path.join(data_dir, 'pcb_vendors.xlsx'))
print("Created pcb_vendors.xlsx")

print("Excel files created successfully!")


