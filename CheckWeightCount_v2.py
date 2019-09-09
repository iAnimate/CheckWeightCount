import maya.cmds as cmds
import maya.mel as mel
import sys

# all Maya commands are converted to cmds when possible.
# Maya commands that are in mel are only available in mel.

# def CheckWeightCount()
# global proc CheckWeightCount()

#cmds.ls 	string $currentSelection[] = `ls -selection`
## Get array of currently selected objects
string $currentSelection[] = cmds.ls(selection=True)
#string $currentSelection[] = mel.eval("ls -selection")


int $foundSkin = 0
for ($sel in $currentSelection) 

	print($sel+"\n")
	
	$flag = 0
	string $buff[]
	
	#tokenize($sel,".",$buff)
	#"head.hair.tip"
	#option 1:
	##mel.eval(`tokenize($sel,".",$buff)`)
	#option 2:
	##mel.eval(`tokenize"$sel,".",$buff"`)
	#option 3:
	$buff=$sel.split('.')
			
	#mel.findRelatedSkinCluster ??		string $sCluster = findRelatedSkinCluster($buff[0])
	#option 1:
	string $sCluster = mel.eval("findRelatedSkinCluster ($buff[0]);")
	#option 2:
	##string $sCluster = mel.findRelatedSkinCluster($buff[0])
	
	if ("" != $sCluster) 
		$foundSkin = 1
		
		#cmds.select ??		select -r $sel
		#option 1:
		cmds.select('$sel', r=true)
		#option 2:
		##mel.select(replace=true, $sel)
		
		#cmds.polyEvaluate ??		$vertcount = `polyEvaluate -v $buff[0]`
		$vertcount = `cmds.polyEvaluate -v $buff[0]`
		
		for($i=0 $i < $vertcount[0] $i++)
		
			string $cmd = ("skinPercent -q -v "+$sCluster+" "+$buff[0]+".vtx["+$i+"]")
			
			#mel.eval ??		$result = eval($cmd)
			$result = mel.eval($cmd)
			
			$count = 0
			for ($x in $result)
			
				if($x > 0)
					$count++
		
			if($count > 4)
			
				string $cmd = ("xform -q -ws -t "+$buff[0]+".vtx["+$i+"]")
				
				#mel.eval ??		$result = eval($cmd)
				$result = mel.eval($cmd)
				
				print($count+" weights at "+$result[0]+" "+$result[1]+" "+$result[2]+"\n")
				$flag = 1				
	if($flag == 1)
		print("More than 4 weights in mesh "+$buff[0]+"\n")

if($foundSkin == 0)
	print "Error, no skin found.\n"