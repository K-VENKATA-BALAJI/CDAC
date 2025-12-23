# Database Design Documentation

## Overview

The MySQL database schema is designed to efficiently store and query PCB rate contract data from multiple vendors. The design supports:

1. **Multiple Vendors**: Each vendor can have their own rate contracts
2. **Complex Specifications**: Rates are stored with detailed PCB specifications
3. **Flexible Querying**: Easy to find rates matching specific PCB requirements
4. **Scalability**: Can handle thousands of rate entries per vendor

## Database Schema

### 1. `vendors` Table
Stores vendor/company information.

**Columns:**
- `vendor_id` (INT, PRIMARY KEY, AUTO_INCREMENT)
- `vendor_name` (VARCHAR(255)) - Short name/identifier (e.g., "HIQ")
- `company_name` (VARCHAR(255)) - Full company name
- `address` (TEXT) - Company address
- `phone` (VARCHAR(50)) - Contact phone
- `email` (VARCHAR(255)) - Contact email
- `created_at`, `updated_at` (TIMESTAMP)

**Indexes:**
- `idx_vendor_name` on `vendor_name`

### 2. `vendor_rates` Table
Stores the actual rate contract data. Each row represents a rate for a specific combination of PCB specifications.

**Columns:**
- `rate_id` (INT, PRIMARY KEY, AUTO_INCREMENT)
- `vendor_id` (INT, FOREIGN KEY → vendors.vendor_id)
- **PCB Specifications:**
  - `num_layers` (INT) - Number of PCB layers (1, 2, 4, 6, etc.)
  - `solder_mask` (ENUM('YES', 'NO')) - Whether solder mask is included
  - `thickness` (VARCHAR(50)) - PCB thickness (e.g., "0.8", "1.6", "below 0.8", "above 3.2")
  - `track_spacing` (VARCHAR(50)) - Track/Spacing specification (e.g., "8/8 mil", "6/6 mil")
  - `via_drill_pad` (VARCHAR(50)) - Via drill/pad specification (e.g., "12/24 mil", "10/20 mil")
- **Rate Information:**
  - `rate_per_sqcm` (DECIMAL(10, 4)) - Rate in Rs per square centimeter
  - `currency` (VARCHAR(10)) - Default: 'INR'
- **Additional Specifications:**
  - `material` (VARCHAR(100)) - e.g., "Glass Epoxy (FR4)"
  - `surface_finish` (VARCHAR(100)) - e.g., "ENIG"
  - `copper_thickness` (VARCHAR(50)) - e.g., "35 Microns"
  - `min_quantity` (VARCHAR(50)) - e.g., "3-5 Nos"
  - `bbt_charges` (VARCHAR(50)) - e.g., "Inclusive"
- **Metadata:**
  - `contract_period_start`, `contract_period_end` (DATE)
  - `created_at`, `updated_at` (TIMESTAMP)

**Indexes:**
- `idx_vendor_specs` on (vendor_id, num_layers, solder_mask, thickness)
- `idx_track_via` on (track_spacing, via_drill_pad)
- `idx_rate` on (rate_per_sqcm)

**Foreign Keys:**
- `vendor_id` → `vendors.vendor_id` (ON DELETE CASCADE)

### 3. `user_files` Table
Stores user-saved PCB specifications and calculated rates.

**Columns:**
- `file_id` (INT, PRIMARY KEY, AUTO_INCREMENT)
- `email` (VARCHAR(255)) - User email (used as reference key)
- `file_name` (VARCHAR(255))
- `file_description` (TEXT)
- `specifications` (JSON) - Selected PCB specifications
- `vendors` (JSON) - Calculated vendor rates
- `created_at`, `updated_at` (TIMESTAMP)

**Indexes:**
- `idx_email` on `email`
- `idx_created_at` on `created_at`

### 4. `pcb_specification_options` Table
Stores available options for each specification field (replaces Excel file for options).

**Columns:**
- `option_id` (INT, PRIMARY KEY, AUTO_INCREMENT)
- `field_name` (VARCHAR(100)) - e.g., "Num of Layers", "Material"
- `option_value` (VARCHAR(255)) - e.g., "2", "FR-4"
- `display_order` (INT) - For ordering options
- `is_active` (BOOLEAN) - Whether option is currently available
- `created_at` (TIMESTAMP)

**Indexes:**
- `unique_field_option` on (field_name, option_value)
- `idx_field_name` on `field_name`

## Data Flow

### Import Process (HIQ Excel → MySQL)

1. **Parse Excel File** (`import_hiq_data.py`):
   - Extract vendor information (rows 6-8)
   - Extract basic PCB specifications (rows 11-15)
   - Extract track/spacing and via values (rows 19-20)
   - Extract rate data (rows 22+)

2. **Data Transformation**:
   - Each rate entry in Excel becomes a row in `vendor_rates`
   - Specifications are normalized and stored
   - Rates are stored with proper decimal precision

3. **Database Insertion**:
   - Insert vendor record
   - Insert all rate records with foreign key reference

### Query Process (User Request → Rates)

1. **User selects specifications** in frontend
2. **Frontend sends POST** to `/api/calculate-rates` with specifications
3. **Backend queries** `vendor_rates` table matching:
   - Number of layers
   - Thickness
   - Track/Spacing
   - Via drill/pad
   - Solder mask (default: YES)
4. **Results sorted** by rate (ascending)
5. **Ranks assigned** and returned to frontend

## Example Queries

### Get rates for 2-layer PCB, 1.6mm thickness, 6/6 mil track/spacing

```sql
SELECT 
    v.vendor_name,
    vr.rate_per_sqcm,
    vr.num_layers,
    vr.thickness,
    vr.track_spacing,
    vr.via_drill_pad
FROM vendor_rates vr
JOIN vendors v ON vr.vendor_id = v.vendor_id
WHERE vr.num_layers = 2
  AND vr.thickness = '1.6'
  AND vr.track_spacing = '6/6 mil'
  AND vr.solder_mask = 'YES'
ORDER BY vr.rate_per_sqcm ASC;
```

### Get all vendors and their rate ranges

```sql
SELECT 
    v.vendor_name,
    COUNT(*) as total_rates,
    MIN(vr.rate_per_sqcm) as min_rate,
    MAX(vr.rate_per_sqcm) as max_rate,
    AVG(vr.rate_per_sqcm) as avg_rate
FROM vendor_rates vr
JOIN vendors v ON vr.vendor_id = v.vendor_id
GROUP BY v.vendor_id, v.vendor_name;
```

## Adding New Vendors

To add a new vendor:

1. **Prepare Excel file** with same structure as HIQ file
2. **Create import script** (similar to `import_hiq_data.py`)
3. **Run import** to populate database
4. **Verify data** using SQL queries

## Advantages of This Design

1. **Normalized Structure**: Each specification combination is stored once
2. **Fast Queries**: Indexes on commonly queried fields
3. **Scalable**: Can handle multiple vendors and thousands of rates
4. **Flexible**: Easy to add new specification fields
5. **Maintainable**: Clear separation between vendors and rates

## Future Enhancements

1. **Add more specification fields** (size, color, impedance, etc.)
2. **Support rate calculations** based on PCB area
3. **Add price breaks** for quantity discounts
4. **Support multiple currencies**
5. **Add rate history** tracking (versioning)


