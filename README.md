# Backend Server API

## **Server commands**

### Start server:
`cd app/backend/ && docker compose up`

### Shutdown server:
`cd app/backend/ && docker compose down`

### Django admin url
(Can only be accessed when the server is running)  
`/admin/`  
<http://127.0.0.1:8000/admin/>

Credentials:  
username: `admin`  
password: `password123`  

Note! If these credentials are not working then you need to make a superuser:  
`docker compose run --rm app sh -c "python manage.py createsuperuser"`  
and make a new username and password
#
## **API endpoints**
Insomnia exported file path:
`/app/backend/Insomnia_2023-02-26.json`

**Upload record (for drone)**  
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


**Get list distinct path id's (for webapp)**  
`​/api​/server​/get_distinct_path_ids​/`

**Get list of locations for specified path (for webapp)**  
`/api/server/get_locations_data_by_path/?path_id=[INTEGER]`

**Update status for a hotspot(for webapp)**  
`/api/server/records/{id}/update_status/`  
payload = {'status':[NEW_STATUS]}  
Note: {id} is the hotspot_id from the response of /get_locations_data_by_path/ endpoint  

**Swagger documentation**  
(Can only be accessed when the server is running)  
`/api/docs/`  
<http://127.0.0.1:8000/api/docs/>









