# Backend Server API

## Server commands

### Start server:
```sh
cd app/backend/ && docker compose up
```

### Shutdown server:
```sh
cd app/backend/ && docker compose down
```

<br>  

### **Django admin url**
(Can only be accessed when the server is running)  
`/admin/`  
<http://127.0.0.1:8000/admin/>

<http://ec2-44-214-38-103.compute-1.amazonaws.com/admin/>

Credentials :  
username: `fireflyadmin`  
password: `forscience!`  

**Note!** If these credentials are not working then you need to make a superuser:  
```sh
docker compose run --rm app sh -c "python manage.py createsuperuser"
```

<br>  

### **Swagger documentation**  
(Can only be accessed when the server is running)  
`/api/docs/`  
<http://127.0.0.1:8000/api/docs/>

<http://ec2-44-214-38-103.compute-1.amazonaws.com/api/docs/>

## **API endpoints**
Insomnia exported file path:
`/app/backend/Insomnia_*****.json`

### **Drone**
<br>  

**Register new path**  
`POST ​/api​/server​/paths/`  
`payload = {'name' : [NAME OF PATH]}`
<br>

**Upload record**  
`POST /api/server/add_record/`
```
payload = {
    "lon": lon,
    "lat": lat,
    "path_id": path_id,
    "date": date,
    "image_ir": image_file_ir,
    "image_rgb": image_file_rgb
} 
```
Example:
```
def create_record_custom(client, path_id = 3, lon=1.1, lat=2.2, date='2000-02-14T18:00:00Z'):
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
                "lon": lon,
                "lat": lat,
                "path_id": path_id,
                "date": date,
                "image_ir": image_file_ir,
                "image_rgb": image_file_rgb
            }
            res = client.post(ADD_RECORD_URL, payload, format='multipart')
            return res
```
#
### **Webapp**
<br>

**Get list of paths**  
`GET ​/api​/server​/paths/`  
<br>

**Get list of locations for specified path**  
`GET /api/server/get_locations_data_by_path/?path_id=[INTEGER]`  
<br>

**Update status for a record**  
`POST /api/server/records/{id}/update_status/`  
```
payload = {
    'status':[NEW_STATUS]
}
```
Note: {id} is the record_id from the response of /get_locations_data_by_path/ endpoint  
<br>

#
### **AI Classifier**
<br>

**Get unclassified records**  
`GET /api/server/records/get_unclassified_records/`  
<br>

**Send classification for a record**  
`POST /api/server/records/{id}/send_classification/`  
```
payload = {
    'is_hotspot': BOOL,
    'image_masked': image
}  
```

#
## **How to open images returned by the server**
To view an image use:   
[server name] + [image url]  
**Example:**  
<http://127.0.0.1:8000/static/media/uploads/image_records/f7cf6e42-ada3-4b10-bbfc-1971da99649a.png>  
Server name = `http://127.0.0.1:8000`   
Image url   = `/static/media/uploads/image_records/f7cf6e42-ada3-4b10-bbfc-1971da99649a.png`   












