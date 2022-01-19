import json
import superannotate as sa
from PIL import Image


token_path = "/home/ubuntu/.superannotate/config.json"
token = "ad6a396fec1ce8c31e652b28dc993fef05306b4033595351994eb31614dab52c6557998375ce290et=15477"

with open(token_path, "w") as tf:
    json.dump({"token": token}, tf)


sa.init(token_path)

proj_name = 'Project_via_SDK'


filepath = "eifel.jpg"
img = Image.open(filepath)

width_prcnt = img.width/100
height_prcnt = img.height/100

width_centre = width_prcnt * 50

left_x1 = width_centre
left_x2 = width_centre

annot_points = list()


for yl in range(64, 34, -5):
	left_x1 -= width_prcnt * 5
	annot_points.append(left_x1)
	annot_points.append(yl * height_prcnt )
	left_x2 -= width_prcnt * 2.5
	annot_points.append(left_x2)
	annot_points.append(yl * height_prcnt)

right_x1 = 2 * width_centre - left_x1
right_x2 = 2 * width_centre - left_x2



for yr in range(34, 64, 5):
	right_x2 -= width_prcnt * 2.5
	annot_points.append(right_x2)
	annot_points.append(yr * height_prcnt)
	right_x1 -= width_prcnt * 5
	annot_points.append(right_x1)
	annot_points.append(yr * height_prcnt)

an = {
     "eifel":[{
        "type": "polygon",
        "classId": 1,
        "probability": 100,
        "points": annot_points,
        "groupId": 0,
        "pointLabels": {},
        "locked": False,
        "visible": True,
        "attributes": []
    }, {
        "type": "meta",
        "name": "no-mask",
        "timestamp": 1600628979793
   }],
     "metadata":{
        "name": "eifel",
        "annotation_status": "Not Started",
        "prediction_status": 1,
	"project_id": 73295,
        "segmentation_status": 1,
        "createdAt": "2022-01-18T07:30:06.117Z",
        "is_pinned": 0,
	}

}


cl = [{
	"attribute_groups": [],
        "color": "#32a852",
        "id": 1,
        "name": "no-mask",
        "opened": True
}]


with open('eifel___objects.json', 'w', encoding='utf-8') as ann:
   json.dump(an, ann, ensure_ascii=False, indent=4)
with open('classes', 'w', encoding='utf-8') as classes:
   json.dump(cl, classes, ensure_ascii=False, indent=4)


sa.create_project( project_name = proj_name, project_description = 'Decribed', project_type = 'Vector')
sa.create_annotation_class( project = proj_name, name = 'Class_via_SDK', color = "#15ff00")
sa.upload_image_to_project(project = proj_name,  img = filepath, image_name="eifel", annotation_status='NotStarted')
sa.create_annotation_classes_from_classes_json(project = proj_name, classes_json = "./classes.json")
sa.validate_annotations(project_type = "Vector", annotations_json ="./eifel___objects.json" )
sa.upload_annotations_from_folder_to_project(project = proj_name, folder_path = "./")
annotations = sa.get_image_annotations(
    project = proj_name,
    image_name = "eifel")
with open('finish', 'w', encoding='utf-8') as fin:
   json.dump(annotations["annotation_json"], fin, ensure_ascii=False, indent=4)


