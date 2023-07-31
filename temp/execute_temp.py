

import nuke

print('Iniciando execute.py')

########################################
# raiz del proyecto
root_node = nuke.root()

# Obtiene el primer y ultimo fotograma
first_frame = int(root_node['first_frame'].value())
last_frame = int(root_node['last_frame'].value())
frame_range = last_frame - first_frame

print('last frame:', frame_range)

# Obtener el nombre del script
shot_name = nuke.tcl('file rootname [file tail [value root.name]]')
print('shot name:', shot_name)

######################################
#Renderizar
node_name = "Write1"
if nuke.exists(node_name):
    write_node = nuke.toNode(node_name)
    render_path = nuke.filename(write_node)
    print('render_path is:', render_path)
    nuke.execute(write_node, continueOnError = True)
else:
    print(f"El nodo {node_name} no existe")

#################
quit()
        