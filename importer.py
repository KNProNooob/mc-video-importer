import subprocess
import os

def CreateDatapack(datapack_path, namespace):
    with open(datapack_path + "/pack.mcmeta", "w") as f:
        f.write('{\n' \
        '  "pack": {\n' \
        '    "description": "MC Video Importer",\n' \
        '    "pack_format": 18,\n' \
        '  }\n' \
        '}')
    os.mkdir(datapack_path + "/data")
    os.mkdir(datapack_path + "/data/" + namespace)
    os.mkdir(datapack_path + "/data/" + namespace + "/function")

def CreateResourcepack(resourcepack_path, namespace):
    with open(resourcepack_path + "/pack.mcmeta", "w") as f:
        f.write('{\n' \
        '  "pack": {\n' \
        '    "description": "MC Video Importer",\n' \
        '    "pack_format": 46,\n' \
        '  }\n' \
        '}')
    os.mkdir(resourcepack_path + "/assets")
    os.mkdir(resourcepack_path + "/assets/" + namespace)
    os.mkdir(resourcepack_path + "/assets/" + namespace + "/textures")
    os.mkdir(resourcepack_path + "/assets/" + namespace + "/textures/overlays")

def ConvertVideo(video_file_path, output_folder_path):
    os.mkdir(output_folder_path)
    subprocess.run('ffmpeg -i ' + video_file_path + ' -vf "fps=20" ' + output_folder_path + '/%d.png', shell=True)

def GenerateFunctions(video_frames_path, functions_output_path, video_name, namespace):
    total_frames = len(os.listdir(video_frames_path))
    frames = []
    for i in range(total_frames):
        cam_overlay_path = namespace + ":overlays" + "/" + video_name + "/" + str(i + 1)
        frames.append('execute if score ' + video_name + ' videos matches ' + str(i + 1) + ' run item replace entity @p armor.head with glass[equippable={slot:"head", camera_overlay: "' + cam_overlay_path + '"}]\n')

    os.mkdir(functions_output_path + "/" + video_name)
    with open(functions_output_path + "/" + video_name + "/play.mcfunction", "w") as f:
        f.write("scoreboard objectives add videos dummy\n")
        f.write("scoreboard players add " + video_name + " event 1\n")
        f.writelines(frames)
        f.write("schedule function " + namespace + ":" + video_name + "/play 1t append")
