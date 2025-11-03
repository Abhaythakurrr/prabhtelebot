# Bug Fix - Image URL Error

## Issue
```
telegram.error.BadRequest: Invalid file http url specified: unsupported url protocol
```

## Root Cause
The Bytez API returns a `Response` object with an `output` attribute containing the URL, but the code was trying to convert the entire Response object to a string, which resulted in an invalid URL format.

## Solution
Updated `src/ai/generator.py` to properly extract URLs from Bytez Response objects:

```python
# Before:
if isinstance(result, list) and result:
    image_url = result[0]
elif isinstance(result, str):
    image_url = result
else:
    image_url = str(result)  # This was converting Response object incorrectly

# After:
if hasattr(result, 'output'):
    image_url = result.output  # Extract URL from Response object
elif isinstance(result, list) and result:
    image_url = result[0]
elif isinstance(result, str):
    image_url = result
else:
    image_url = str(result)

# Ensure it's a string
if not isinstance(image_url, str):
    image_url = str(image_url)
```

## Files Modified
- `src/ai/generator.py` - Fixed URL extraction for images, videos, and audio

## Testing
After restart, test:
```
/start
Click "Create Image"
Select style (anime/normal/realistic)
Enter prompt: "anime couple under cherry blossoms"
```

Should now successfully send the image!

## Other Issue in Logs
**Multiple bot instances running**: 
```
Conflict: terminated by other getUpdates request; make sure that only one bot instance is running
```

**Solution**: Stop all other bot instances before starting:
```bash
# Find and kill other instances
ps aux | grep python
kill <process_id>

# Or restart the service
```

## Status
✅ Fixed - Ready to deploy
