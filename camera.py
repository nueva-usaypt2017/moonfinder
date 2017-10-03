import lensfunpy

cam_maker = 'Canon'
cam_model = 'Canon EOS Rebel T5'
mount = 'T-mount'
lens_maker = 'Canon'
lens_model = 'EFS 18-55mm Image Stabilizer'

db = lensfunpy.Database()

cam = db.find_cameras(cam_maker, cam_model)[0]
lens = db.find_lenses(cam, lens_maker, lens_model, loose_search=True)

print(cam)
print(db.find_mount(cam.mount).compat)

print(lens)
