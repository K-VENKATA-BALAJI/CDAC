# Debug Checklist - Calculate Rate Contract Not Working

## ✅ Fixed Issues:

1. **Format Normalization**: 
   - Thickness: Removes "mm" suffix automatically
   - Track/Spacing: Normalizes "6/6 mil" → "6 / 6 mil"
   - Via Hole/Pad: Normalizes "12/24 mil" → "12 / 24 mil"

2. **Error Handling**: Added console logging in frontend and backend

3. **Database Query**: Tested and working - returns results correctly

## 🔍 Debugging Steps:

### 1. Check Browser Console (F12)
- Open browser developer tools (F12)
- Go to Console tab
- Click "Calculate Rate Contract"
- Look for:
  - "Sending specifications: ..."
  - "Received response: ..."
  - Any error messages

### 2. Check Backend Terminal
- Look for:
  - "Query specifications: ..."
  - "Found X vendors"
  - "Executing query: ..."
  - Any error messages

### 3. Test API Directly

Open a new terminal and test:

```bash
curl -X POST http://localhost:8888/api/calculate-rates ^
  -H "Content-Type: application/json" ^
  -d "{\"specifications\":{\"Num of Layers\":\"2\",\"Thickness\":\"1.6mm\",\"Track / Spacing\":\"6/6 mil\",\"Via Hole/Pad\":\"12/24 mil\"}}"
```

Should return JSON with vendor rates.

### 4. Check Network Tab (Browser F12)
- Go to Network tab
- Click "Calculate Rate Contract"
- Find the request to `/api/calculate-rates`
- Check:
  - Status code (should be 200)
  - Response body (should have vendor data)
  - Request payload (should have specifications)

### 5. Verify Specifications Match

The database has these formats:
- **Thickness**: "1.6", "0.8", "below 0.8", "above 3.2"
- **Track/Spacing**: "6 / 6 mil", "8 / 8 mil" (with spaces around /)
- **Via Hole/Pad**: "12 / 24 mil", "10 / 20 mil" (with spaces around /)

Frontend should send:
- Thickness can have "mm" suffix (will be removed)
- Track/Spacing can be "6/6 mil" (will be normalized)
- Via can be "12/24 mil" (will be normalized)

## Common Issues:

### Issue: "No rates found"
**Solution**: 
- Check specifications match database values
- Try: Num of Layers: 2, Thickness: 1.6mm, Track/Spacing: 6/6 mil, Via: 12/24 mil
- Check backend terminal for query details

### Issue: "Failed to calculate rates"
**Solution**:
- Check backend server is running
- Check MySQL connection
- Check browser console for CORS errors
- Verify API endpoint is correct

### Issue: Button does nothing
**Solution**:
- Check browser console for JavaScript errors
- Verify `onCalculate` is passed to PCBSpecifications
- Check if button is disabled (loading state)

## Test Commands:

```bash
# Test database query
cd backend
python test_query.py

# Test API endpoint
curl -X POST http://localhost:8888/api/calculate-rates -H "Content-Type: application/json" -d "{\"specifications\":{\"Num of Layers\":\"2\",\"Thickness\":\"1.6mm\",\"Track / Spacing\":\"6/6 mil\",\"Via Hole/Pad\":\"12/24 mil\"}}"
```

## Expected Behavior:

1. User selects specifications
2. Clicks "Calculate Rate Contract"
3. Button shows "Calculating..." (loading state)
4. Frontend sends POST to `/api/calculate-rates`
5. Backend queries MySQL database
6. Backend returns vendor rates
7. Frontend displays rates in table
8. Button returns to normal state

## Next Steps:

1. Restart backend server (to load updated code)
2. Refresh frontend browser
3. Try calculating rates again
4. Check console/terminal for debug messages

