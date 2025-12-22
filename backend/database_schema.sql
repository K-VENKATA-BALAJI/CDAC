-- MySQL Database Schema for PCB Rate Contract System
-- Designed to handle vendor rate contracts with multiple specifications

-- Drop existing tables if they exist (for testing)
DROP TABLE IF EXISTS user_files;
DROP TABLE IF EXISTS vendor_rates;
DROP TABLE IF EXISTS vendors;
DROP TABLE IF EXISTS pcb_specification_options;

-- ============================================================================
-- VENDORS TABLE
-- Stores vendor/company information
-- ============================================================================
CREATE TABLE vendors (
    vendor_id INT AUTO_INCREMENT PRIMARY KEY,
    vendor_name VARCHAR(255) NOT NULL,
    company_name VARCHAR(255),
    address TEXT,
    phone VARCHAR(50),
    email VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_vendor_name (vendor_name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- VENDOR RATES TABLE
-- Stores the actual rate contract data from Excel
-- Each row represents a rate for a specific combination of specifications
-- ============================================================================
CREATE TABLE vendor_rates (
    rate_id INT AUTO_INCREMENT PRIMARY KEY,
    vendor_id INT NOT NULL,
    
    -- PCB Specifications
    num_layers INT NOT NULL,
    solder_mask ENUM('YES', 'NO') NOT NULL,
    thickness VARCHAR(50) NOT NULL,  -- e.g., "0.8", "1.6", "below 0.8", "above 3.2"
    
    -- Track/Spacing and Via specifications
    track_spacing VARCHAR(50) NOT NULL,  -- e.g., "8/8 mil", "6/6 mil"
    via_drill_pad VARCHAR(50) NOT NULL,  -- e.g., "12/24 mil", "10/20 mil"
    
    -- Rate information
    rate_per_sqcm DECIMAL(10, 4) NOT NULL,  -- Rate in Rs per Sq.Cm
    currency VARCHAR(10) DEFAULT 'INR',
    
    -- Additional specifications (from basic PCB spec section)
    material VARCHAR(100),  -- e.g., "Glass Epoxy (FR4)"
    surface_finish VARCHAR(100),  -- e.g., "ENIG"
    copper_thickness VARCHAR(50),  -- e.g., "35 Microns"
    min_quantity VARCHAR(50),  -- e.g., "3-5 Nos"
    bbt_charges VARCHAR(50),  -- e.g., "Inclusive"
    
    -- Metadata
    contract_period_start DATE,
    contract_period_end DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (vendor_id) REFERENCES vendors(vendor_id) ON DELETE CASCADE,
    
    -- Indexes for fast lookups
    INDEX idx_vendor_specs (vendor_id, num_layers, solder_mask, thickness),
    INDEX idx_track_via (track_spacing, via_drill_pad),
    INDEX idx_rate (rate_per_sqcm)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- PCB SPECIFICATION OPTIONS TABLE
-- Stores available options for each specification field
-- This replaces the Excel file for specification options
-- ============================================================================
CREATE TABLE pcb_specification_options (
    option_id INT AUTO_INCREMENT PRIMARY KEY,
    field_name VARCHAR(100) NOT NULL,
    option_value VARCHAR(255) NOT NULL,
    display_order INT DEFAULT 0,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    UNIQUE KEY unique_field_option (field_name, option_value),
    INDEX idx_field_name (field_name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- USER FILES TABLE
-- Stores user-saved PCB specifications and calculated rates
-- ============================================================================
CREATE TABLE user_files (
    file_id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL,
    file_name VARCHAR(255),
    file_description TEXT,
    specifications JSON,  -- Stores the selected PCB specifications
    vendors JSON,  -- Stores the calculated vendor rates
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    INDEX idx_email (email),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- SAMPLE DATA INSERTION (for testing)
-- ============================================================================

-- Insert HIQ vendor
INSERT INTO vendors (vendor_name, company_name, address, phone) VALUES
('HIQ', 'Hi-Q Electronics Private Limited', '# 9, INDUSTRIAL ESTATE, HOSUR- 635109, TAMILNADU', '8068849818');

-- Note: Actual rate data will be imported from Excel using the import script

