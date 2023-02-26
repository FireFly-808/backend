# Backend Server API

## <b> Server commands </b>

### Start server:
`cd app/backend/ && docker compose up`

### Shutdown server:
`cd app/backend/ && docker compose down`

### Django admin credentials 
username: `admin` \
password: `password123` 

## <b> API endpoints </b>
Insomnia exported file path:
`/app/backend/Insomnia_2023-02-26.json`

<b>Upload record (for drone)</b>\
`/api/server/add_record/`
```
payload = {
    "x_coord": x,
    "y_coord": y,
    "path_id": path_id,
    "date": date,
    "image_ir": image_file_ir,
    "image_rgb": image_file_rgb
} 
```
Example:
```
def create_record_custom(client, path_id = 3, x=1.1, y=2.2, date='2000-02-14T18:00:00Z'):
    """Create sample record with manual coordinates"""
    with tempfile.NamedTemporaryFile(suffix='.png') as image_file_ir:
        with tempfile.NamedTemporaryFile(suffix='.png') as image_file_rgb:
            img_ir = Image.new('RGB',(10,10))
            img_rgb = Image.new('RGB',(10,10))
            img_ir.save(image_file_ir, format='PNG')
            img_rgb.save(image_file_rgb, format='PNG')
            image_file_ir.seek(0)
            image_file_rgb.seek(0)
            payload = {
                "x_coord": x,
                "y_coord": y,
                "path_id": path_id,
                "date": date,
                "image_ir": image_file_ir,
                "image_rgb": image_file_rgb
            }
            res = client.post(ADD_RECORD_URL, payload, format='multipart')
            return res
```


<b>Get list distinct path id's (for webapp)</b> \
`​/api​/server​/get_distinct_path_ids​/`

<b>Get list of locations for specified path (for webapp)</b> \
`/api/server/get_locations_data_by_path/?path_id=[INTEGER]`

<b>Update status for a hotspot(for webapp)</b> \
`/api/server/hotspots/{id}/update-status/` \
Note: {id} is the hotspot_id from the response of /get_locations_data_by_path/ endpoint






