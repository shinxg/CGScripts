# -*- coding: utf-8 -*-
import os, re
import glob
def cleanExt(ext):
    while ext.startswith("."):
        ext = ext[1:]
    return ext

def main():
    tmpls = ["-- None --"] + lux.getMaterialTemplates()
    info = lux.getSceneInfo()
    values = [("folder", lux.DIALOG_FOLDER, "Folder to import from:", None),
              ("iext", lux.DIALOG_TEXT, "Input file format to read:", "obj"),
              ("output_folder", lux.DIALOG_FOLDER, "Folder to save to:", None),
              ("oext", lux.DIALOG_TEXT, "Output image format:", "png"),
              ("width", lux.DIALOG_INTEGER, "Output width:", info["width"]),
              ("height", lux.DIALOG_INTEGER, "Output height:", info["height"]),
              (lux.DIALOG_LABEL, "--"),
              ("template", lux.DIALOG_ITEM, "Apply material template on each import (optional):",
               tmpls[0], tmpls),
              (lux.DIALOG_LABEL, "--"),
              ("queue", lux.DIALOG_CHECK, "Add to queue", True),
              ("process", lux.DIALOG_CHECK, "Process queue after running script", False)]
    opts = lux.getInputDialog(title = "Render Images",
                              desc = "Rendes all models with a chosen input extension to images of chosen output extension.",
                              values = values,
                              id = "renderimages.py.luxion")
    output_folder = opts['output_folder']
    if not opts: return

    if len(opts["folder"]) == 0:
        raise Exception("Folder cannot be empty!")
    fld = opts["folder"]

    if len(opts["iext"]) == 0:
        raise Exception("Input extension cannot be empty!")
    iext = cleanExt(opts["iext"])
    # reFiles = re.compile(".*{}".format(iext))
    # found = False
    # for f in os.listdir(fld):
    #     if reFiles.match(f):
    #         found = True
    #         break
    # if not found:
    #     raise Exception("Could not find any input files matching the extension \"{}\" in \"{}\"!"
    #                     .format(iext, fld))

    if len(opts["oext"]) == 0:
        raise Exception("Output extension cannot be empty!")
    oext = cleanExt(opts["oext"])

    width = opts["width"]
    height = opts["height"]
    template = opts["template"]
    queue = opts["queue"]
    process = opts["process"]

    # Only set template if one was chosen.
    if template[0] == 0:
        template = None
    else:
        template = template[1]

    importopts = lux.getImportOptions()
    importopts["separate_parts"] = True

    opts = lux.getRenderOptions()
    opts.setAddToQueue(queue)

    # for f in [f for f in os.listdir(fld) if f.endswith(iext)]:
    fld = fld.replace('/', '\\')
    # print(fld)
    # print(os.path.join(fld, '*', 'model_normalized.obj'))
    print(glob.glob(os.path.join(fld, '*', 'models', 'model_normalized.obj')))
    for f in glob.glob(os.path.join(fld, '*', 'models', 'model_normalized.obj')):
        print(f)
        # path = fld + os.path.sep + f
        # raise Exception(f)
        lux.newScene()
        
        azimuth = -180.0
        lux.setBackgroundColor((0, 0, 0))
        print("Importing {}".format(f))
        lux.importFile(f, opts=importopts)

        if template:
            print("Setting material template {}".format(template))
            lux.setMaterialTemplate(template)
        for i in range(8):
            # path = path + "." + oext
            path = os.path.join(output_folder, f.split('\\')[-3]+'_'+str(i)+'.'+oext)
            print("Rendering {}".format(path))
            lux.setSphericalCamera(azimuth, 0, 0)
            lux.setCameraDistance(1.5)
            lux.renderImage(path = path, width = width, height = height, opts = opts)
            azimuth = azimuth + 45
           

    if process:
        print("Processing queue")
        lux.processQueue()

main()
