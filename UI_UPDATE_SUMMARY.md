# UI Update Summary - New Field Structure

## Changes Made

### ✅ Frontend Updates

#### 1. **PCBSpecifications Component** (`frontend/src/components/PCBSpecifications.js`)
- **Updated Fields:**
  - `Num of Layers` → `PCB Copper Layers` (required *)
  - `Material` → `PCB Material` (required *)
  - `Surface Finish` → `PCB Finish` (required *)
  - `Track / Spacing` → `Track/Spacings(mil)` (required *)
  - `Via Hole/Pad` → `Via Drill/Finish` (required *)
  - `Thickness` → `PCB Thickness` (required *)
  - `Solder Mask` → `Solder Mask & Legend` (required *)
  - `Copper Thickness` (required *) - unchanged
  - `Quantity` (NEW - not required) - text input field
  - `Delivery Type` (NEW - required *) - dropdown

- **Removed Fields:**
  - Via Filling
  - Size
  - Single Ended Impedance
  - Colour
  - Differential Impedance

- **Layout:** Changed from 3 columns to 2 columns
- **Required Indicators:** Added red asterisk (*) for required fields
- **Input Types:** Quantity is a number input, others are dropdowns

#### 2. **PCBRates Component** (`frontend/src/components/PCBRates.js`)
- Updated table header: `S.NO` → `s.No`
- Updated rank display: Shows `L1`, `L2`, `L3`, `L4` instead of numbers

#### 3. **Styling Updates**
- Button color: Changed from yellow (#ffc107) to orange (#ff9800)
- Background: Added light blue gradient
- Form layout: 2-column grid instead of 3-column
- Added required field asterisk styling

### ✅ Backend Updates

#### 1. **Database Options** (`backend/database_mysql.py`)
- Updated `get_specification_options()` to return new field names:
  - `PCB Copper Layers` (from num_layers)
  - `PCB Material` (from material)
  - `PCB Finish` (from surface_finish)
  - `Track/Spacings(mil)` (from track_spacing)
  - `Via Drill/Finish` (from via_drill_pad)
  - `PCB Thickness` (from thickness)
  - `Solder Mask & Legend` (from solder_mask)
  - `Copper Thickness` (unchanged)
  - `Quantity` (empty array - text input)
  - `Delivery Type` (default options: Normal, Express, Urgent, Standard)

#### 2. **Rate Query** (`backend/database_mysql.py`)
- Updated `get_vendor_rates()` to handle both old and new field names
- Field name mapping:
  - `PCB Copper Layers` or `Num of Layers` → `num_layers`
  - `PCB Thickness` or `Thickness` → `thickness`
  - `Track/Spacings(mil)` or `Track / Spacing` → `track_spacing`
  - `Via Drill/Finish` or `Via Hole/Pad` → `via_drill_pad`
  - `Solder Mask & Legend` or `Solder Mask` → `solder_mask`
- Handles "Yes"/"No" or "YES"/"NO" for solder mask

### ✅ Default Values

- **Quantity:** Defaults to "100" if not provided
- **Delivery Type:** Uses first available option from database/defaults
- All required fields get first available option from database

## Field Mapping Reference

| UI Field Name | Database Field | Internal Mapping |
|---------------|---------------|------------------|
| PCB Material* | material | `PCB Material` |
| PCB Finish* | surface_finish | `PCB Finish` |
| Copper Thickness* | copper_thickness | `Copper Thickness` |
| PCB Copper Layers* | num_layers | `PCB Copper Layers` |
| Solder Mask & Legend* | solder_mask | `Solder Mask & Legend` |
| Track/Spacings(mil)* | track_spacing | `Track/Spacings(mil)` |
| Via Drill/Finish* | via_drill_pad | `Via Drill/Finish` |
| PCB Thickness* | thickness | `PCB Thickness` |
| Quantity | N/A | `Quantity` (not in database) |
| Delivery Type* | N/A | `Delivery Type` (not in database) |

## Required Fields

All fields marked with (*) are required:
1. PCB Material*
2. PCB Finish*
3. Copper Thickness*
4. PCB Copper Layers*
5. Solder Mask & Legend*
6. Track/Spacings(mil)*
7. Via Drill/Finish*
8. PCB Thickness*
9. Delivery Type*

**Not Required:**
- Quantity (optional number input)

## Testing Checklist

- [ ] All required fields show red asterisk (*)
- [ ] Dropdowns populate from database
- [ ] Quantity field accepts numbers
- [ ] Calculate button works with new field names
- [ ] Rates display with L1, L2, L3 format
- [ ] Save/Load functionality works
- [ ] Form validation works for required fields

## Notes

- Backend supports both old and new field names for backward compatibility
- Quantity and Delivery Type are not stored in vendor_rates table (UI-only fields)
- All database queries use the mapped field names internally
- Rank display format changed to "L1", "L2", etc. as per new UI

