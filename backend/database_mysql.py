"""
MySQL Database module for PCB Rate Contract System
Replaces the SQLite database.py
"""
import mysql.connector
from mysql.connector import Error
import json
from datetime import datetime

class Database:
    def __init__(self):
        # Database configuration - update these values
        self.config = {
            'host': 'localhost',
            'database': 'pcb_rate_contract',
            'user': 'root',
            'password': 'Balu@6688'  # Update with your MySQL password
        }
        self.connection = None
    
    def get_connection(self):
        """Get database connection"""
        if self.connection is None or not self.connection.is_connected():
            try:
                self.connection = mysql.connector.connect(**self.config)
            except Error as e:
                print(f"Error connecting to MySQL: {e}")
                raise
        return self.connection
    
    def close_connection(self):
        """Close database connection"""
        if self.connection and self.connection.is_connected():
            self.connection.close()
    
    def get_specification_options(self):
        """
        Get available specification options from database
        Returns a dictionary with field names as keys and lists of options as values
        """
        connection = self.get_connection()
        cursor = connection.cursor(dictionary=True)
        
        try:
            specifications = {}
            
            # Get PCB Copper Layers (mapped from num_layers)
            cursor.execute('SELECT DISTINCT num_layers FROM vendor_rates ORDER BY num_layers')
            layers = [str(r['num_layers']) for r in cursor.fetchall()]
            specifications['PCB Copper Layers'] = layers
            
            # Get Thickness (filter out non-thickness values)
            cursor.execute('SELECT DISTINCT thickness FROM vendor_rates ORDER BY thickness')
            all_thickness = [r['thickness'] for r in cursor.fetchall()]
            # Filter to only valid thickness values
            valid_thickness = [t for t in all_thickness if any(char.isdigit() for char in t) and 'nos' not in t.lower() and t not in ['Bottom', 'Top', 'Inner Layer', 'Outer Layer', 'Differential', 'Non Conductive', 'Via on pad']]
            # Add mm suffix for display
            thickness_options = []
            for t in valid_thickness:
                if t.replace('.', '').replace('-', '').isdigit() or 'below' in t.lower() or 'above' in t.lower():
                    if 'mm' not in t and not t.startswith('below') and not t.startswith('above'):
                        thickness_options.append(f"{t}mm")
                    else:
                        thickness_options.append(t)
            specifications['PCB Thickness'] = sorted(set(thickness_options), key=lambda x: (x.startswith('below'), x.startswith('above'), float(x.replace('mm', '').replace('above ', '').replace('below ', '')) if x.replace('mm', '').replace('above ', '').replace('below ', '').replace('.', '').isdigit() else 999))
            
            # Get Track/Spacings(mil)
            cursor.execute('SELECT DISTINCT track_spacing FROM vendor_rates WHERE track_spacing != "" ORDER BY track_spacing')
            track_spacing = [r['track_spacing'] for r in cursor.fetchall()]
            specifications['Track/Spacings(mil)'] = track_spacing
            
            # Get Via Drill/Finish
            cursor.execute('SELECT DISTINCT via_drill_pad FROM vendor_rates WHERE via_drill_pad != "" ORDER BY via_drill_pad')
            via = [r['via_drill_pad'] for r in cursor.fetchall()]
            specifications['Via Drill/Finish'] = via
            
            # Get Solder Mask & Legend
            cursor.execute('SELECT DISTINCT solder_mask FROM vendor_rates ORDER BY solder_mask')
            solder_mask = [r['solder_mask'] for r in cursor.fetchall()]
            specifications['Solder Mask & Legend'] = solder_mask
            
            # Get PCB Material (if available)
            cursor.execute('SELECT DISTINCT material FROM vendor_rates WHERE material IS NOT NULL AND material != ""')
            material = [r['material'] for r in cursor.fetchall()]
            if material:
                specifications['PCB Material'] = material
            else:
                # Default options if not in database
                specifications['PCB Material'] = ['Glass Epoxy', 'FR-4', 'FR-4 High Tg', 'Rogers', 'Aluminum']
            
            # Get PCB Finish
            cursor.execute('SELECT DISTINCT surface_finish FROM vendor_rates WHERE surface_finish IS NOT NULL AND surface_finish != ""')
            surface_finish = [r['surface_finish'] for r in cursor.fetchall()]
            if surface_finish:
                specifications['PCB Finish'] = surface_finish
            else:
                specifications['PCB Finish'] = ['HASL', 'ENIG', 'OSP', 'Immersion Silver', 'Immersion Tin']
            
            # Get Copper Thickness
            cursor.execute('SELECT DISTINCT copper_thickness FROM vendor_rates WHERE copper_thickness IS NOT NULL AND copper_thickness != ""')
            copper = [r['copper_thickness'] for r in cursor.fetchall()]
            if copper:
                specifications['Copper Thickness'] = copper
            else:
                specifications['Copper Thickness'] = ['35 Microns', '1 oz', '0.5 oz', '2 oz', '3 oz']
            
            # Add new fields with default options
            if 'Quantity' not in specifications:
                specifications['Quantity'] = []  # Text input, no options needed
            
            if 'Delivery Type' not in specifications:
                specifications['Delivery Type'] = ['Normal', 'Express', 'Urgent', 'Standard']
            
            return specifications
            
        except Error as e:
            print(f"Error getting specification options: {e}")
            raise e
        finally:
            cursor.close()
    
    def save_user_data(self, email, file_name, file_description, specifications, vendors):
        """Save user file data"""
        connection = self.get_connection()
        cursor = connection.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO user_files (email, file_name, file_description, specifications, vendors)
                VALUES (%s, %s, %s, %s, %s)
            ''', (
                email,
                file_name,
                file_description,
                json.dumps(specifications),
                json.dumps(vendors)
            ))
            connection.commit()
            return cursor.lastrowid
        except Error as e:
            connection.rollback()
            raise e
        finally:
            cursor.close()
    
    def get_user_data(self, email):
        """Get user file data by email"""
        connection = self.get_connection()
        cursor = connection.cursor(dictionary=True)
        
        try:
            cursor.execute('''
                SELECT file_name, file_description, specifications, vendors, created_at
                FROM user_files
                WHERE email = %s
                ORDER BY created_at DESC
            ''', (email,))
            
            rows = cursor.fetchall()
            if not rows:
                return None
            
            # Convert to list of dictionaries
            files = []
            for row in rows:
                files.append({
                    "file_name": row['file_name'],
                    "file_description": row['file_description'],
                    "specifications": json.loads(row['specifications']) if row['specifications'] else {},
                    "vendors": json.loads(row['vendors']) if row['vendors'] else [],
                    "created_at": row['created_at'].isoformat() if row['created_at'] else None
                })
            
            return files
        except Error as e:
            raise e
        finally:
            cursor.close()
    
    def get_vendor_rates(self, specifications):
        """
        Get vendor rates matching the given specifications
        
        Args:
            specifications: dict with keys like 'Num of Layers', 'Thickness', 
                          'Track / Spacing', 'Via Hole/Pad', 'Colour', etc.
        
        Returns:
            List of vendor rates matching the specifications
        """
        connection = self.get_connection()
        cursor = connection.cursor(dictionary=True)
        
        try:
            # Build query based on specifications
            query = """
                SELECT 
                    v.vendor_name,
                    v.company_name,
                    vr.rate_per_sqcm,
                    vr.num_layers,
                    vr.thickness,
                    vr.track_spacing,
                    vr.via_drill_pad,
                    vr.solder_mask
                FROM vendor_rates vr
                JOIN vendors v ON vr.vendor_id = v.vendor_id
                WHERE 1=1
            """
            params = []
            
            # Match specifications - handle both old and new field names
            # PCB Copper Layers (new) or Num of Layers (old)
            num_layers_key = 'PCB Copper Layers' if 'PCB Copper Layers' in specifications else 'Num of Layers'
            if num_layers_key in specifications:
                num_layers_str = str(specifications[num_layers_key]).strip()
                try:
                    num_layers = int(num_layers_str.split()[0])
                    query += " AND vr.num_layers = %s"
                    params.append(num_layers)
                except:
                    pass  # Skip if can't parse
            
            # PCB Thickness (new) or Thickness (old)
            thickness_key = 'PCB Thickness' if 'PCB Thickness' in specifications else 'Thickness'
            if thickness_key in specifications:
                thickness = str(specifications[thickness_key]).strip()
                # Remove "mm" suffix if present and normalize
                thickness = thickness.replace('mm', '').strip()
                # Try exact match first, then try LIKE for ranges like "below 0.8" or "above 3.2"
                # For now, use exact match - if no results, we could add fallback logic
                query += " AND vr.thickness = %s"
                params.append(thickness)
            
            # Track/Spacings(mil) (new) or Track / Spacing (old)
            track_key = 'Track/Spacings(mil)' if 'Track/Spacings(mil)' in specifications else 'Track / Spacing'
            if track_key in specifications:
                track_spacing = str(specifications[track_key]).strip()
                # Normalize format: "6/6 mil" -> "6 / 6 mil"
                if '/' in track_spacing and ' / ' not in track_spacing:
                    track_spacing = track_spacing.replace('/', ' / ')
                # Allow empty track_spacing in database to match any value
                query += " AND (vr.track_spacing = %s OR vr.track_spacing = '' OR vr.track_spacing IS NULL)"
                params.append(track_spacing)
            
            # Via Drill/Finish (new) or Via Hole/Pad (old)
            via_key = 'Via Drill/Finish' if 'Via Drill/Finish' in specifications else 'Via Hole/Pad'
            if via_key in specifications:
                via_drill_pad = str(specifications[via_key]).strip()
                # Normalize format: "12/24 mil" -> "12 / 24 mil"
                if '/' in via_drill_pad and ' / ' not in via_drill_pad:
                    via_drill_pad = via_drill_pad.replace('/', ' / ')
                query += " AND vr.via_drill_pad = %s"
                params.append(via_drill_pad)
            
            # Solder Mask & Legend (new) or Solder Mask (old)
            solder_mask_key = 'Solder Mask & Legend' if 'Solder Mask & Legend' in specifications else 'Solder Mask'
            solder_mask = specifications.get(solder_mask_key, 'YES')
            if isinstance(solder_mask, str):
                # Handle "Yes"/"No" or "YES"/"NO"
                if solder_mask.upper() in ['YES', 'Y']:
                    solder_mask = 'YES'
                elif solder_mask.upper() in ['NO', 'N']:
                    solder_mask = 'NO'
                else:
                    solder_mask = 'YES'
            else:
                solder_mask = 'YES'
            query += " AND vr.solder_mask = %s"
            params.append(solder_mask)
            
            query += " ORDER BY vr.rate_per_sqcm ASC"
            
            # Debug logging
            print(f"[DEBUG] Executing query: {query}")
            print(f"[DEBUG] With params: {params}")
            
            cursor.execute(query, params)
            results = cursor.fetchall()
            
            print(f"[DEBUG] Query returned {len(results)} rows")
            
            # Format results
            vendors = []
            for idx, row in enumerate(results, 1):
                vendors.append({
                    "vendor_name": row['vendor_name'],
                    "company_name": row.get('company_name', ''),
                    "rate": float(row['rate_per_sqcm']),
                    "sno": idx,
                    "rank": idx
                })
            
            return vendors
            
        except Error as e:
            print(f"Error querying vendor rates: {e}")
            raise e
        finally:
            cursor.close()

