"""Check available values in database"""
import mysql.connector

conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='Balu@6688',
    database='pcb_rate_contract'
)
cursor = conn.cursor(dictionary=True)

print("=" * 60)
print("Available Values in Database")
print("=" * 60)

# Layers
cursor.execute('SELECT DISTINCT num_layers FROM vendor_rates ORDER BY num_layers')
layers = [str(r['num_layers']) for r in cursor.fetchall()]
print(f"\nLayers: {layers}")

# Thickness
cursor.execute('SELECT DISTINCT thickness FROM vendor_rates ORDER BY thickness')
thickness = [r['thickness'] for r in cursor.fetchall()]
print(f"\nThickness: {thickness}")

# Track/Spacing
cursor.execute('SELECT DISTINCT track_spacing FROM vendor_rates WHERE track_spacing != "" ORDER BY track_spacing')
track_spacing = [r['track_spacing'] for r in cursor.fetchall()]
print(f"\nTrack/Spacing: {track_spacing}")

# Via
cursor.execute('SELECT DISTINCT via_drill_pad FROM vendor_rates WHERE via_drill_pad != "" ORDER BY via_drill_pad')
via = [r['via_drill_pad'] for r in cursor.fetchall()]
print(f"\nVia Hole/Pad: {via}")

# Solder Mask
cursor.execute('SELECT DISTINCT solder_mask FROM vendor_rates')
solder_mask = [r['solder_mask'] for r in cursor.fetchall()]
print(f"\nSolder Mask: {solder_mask}")

# Material
cursor.execute('SELECT DISTINCT material FROM vendor_rates WHERE material IS NOT NULL AND material != ""')
material = [r['material'] for r in cursor.fetchall()]
print(f"\nMaterial: {material}")

# Surface Finish
cursor.execute('SELECT DISTINCT surface_finish FROM vendor_rates WHERE surface_finish IS NOT NULL AND surface_finish != ""')
surface_finish = [r['surface_finish'] for r in cursor.fetchall()]
print(f"\nSurface Finish: {surface_finish}")

# Copper Thickness
cursor.execute('SELECT DISTINCT copper_thickness FROM vendor_rates WHERE copper_thickness IS NOT NULL AND copper_thickness != ""')
copper = [r['copper_thickness'] for r in cursor.fetchall()]
print(f"\nCopper Thickness: {copper}")

conn.close()


