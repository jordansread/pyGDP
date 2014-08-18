import os
import zipfile

def shapeToZip(inShape, outZip=None, allFiles=True):
        """Packs a shapefile to ZIP format.
        
        arguments
        -inShape -  input shape file
        
        -outZip -   output ZIP file (optional)
          default: <inShapeName>.zip in same folder as inShape
          (If full path not specified, output is written to
          to same folder as inShape)
        
        -allFiles - Include all files? (optional)
          True (default) - all shape file components
          False - just .shp,.shx,.dbf,.prj,shp.xml files
        
        reference: Esri, Inc, 1998, Esri Shapefile Technical Description
          http://www.esri.com/library/whitepapers/pdfs/shapefile.pdf
        
        author: Curtis Price, cprice@usgs.gov"""
    
        if not os.path.splitext(inShape)[1] == ".shp":
            raise Exception, "inShape must be a *.shp"
    
        if not os.path.exists(inShape):
            raise Exception, "%s not found" % inShape
    
        # get shapefile root name "path/file.shp" -> "file"
        # and shapefile path
        rootName = os.path.splitext(os.path.basename(inShape))[0]
        inShape = os.path.realpath(inShape)
        inDir = os.path.dirname(inShape)
    
        # output zip file path
        if outZip in [None,""]:
            # default output: shapefilepath/shapefilename.zip
            outDir = inDir
            outZip = os.path.join(outDir,rootName) + ".zip"
        else:
            outDir = os.path.dirname(outZip)
            if outDir.strip() in ["","."]:
                # if full path not specified, use input shapefile folder
                outDir = os.path.dirname(os.path.realpath(inShape))
            else:
                # if output path does exist, raise an exception
                if not os.path.exists(outDir):
                    raise Exception, "Output folder %s not found" % outDir
            outZip = os.path.join(outDir,outZip)
            # enforce .zip extension
            outZip = os.path.splitext(outZip)[0] + ".zip"

        if not os.access(outDir, os.W_OK):
            raise Exception, "Output directory %s not writeable" % outDir

        if os.path.exists(outZip):
            os.unlink(outZip)

        try:
            # open zipfile
            zf = zipfile.ZipFile(outZip, 'w', zipfile.ZIP_DEFLATED)
            # write shapefile parts to zipfile
            ShapeExt = ["shp","shx","dbf","prj","shp.xml"]
            if allFiles: ShapeExt += ["sbn","sbx","fbn","fbx",
                                  "ain","aih","isx","mxs","atx","cpg"]
            for f in ["%s.%s" % (os.path.join(inDir,rootName),ext)
                  for ext in ShapeExt]:
                if os.path.exists(f):
                    zf.write(f)
                    ##print f # debug print
            return outZip
        except Exception, msg:
            raise Exception, \
                "Could not write zipfile " + outZip + "\n" + str(msg)
        finally:
            try:
                # close the output file
                zf.close()
            except:
                pass
