def do_nodeview_theme():
import bpy
current_theme = bpy.context.user_preferences.themes.items()[0][0]
node_editor = bpy.context.user_preferences.themes[current_theme].node_editor

types = """\
  color_node 
  converter_node 
  distor_node 
  filter_node 
  frame_node 
  gp_vertex 
  gp_vertex_select 
  gp_vertex_size 
  group_node 
  group_socket_node 
  input_node 
  layout_node 
  matte_node 
  node_active 
  node_backdrop 
  node_selected 
  noodle_curving 
  output_node 
  pattern_node 
  script_node 
  selected_text 
  shader_node 
  texture_node 
  vector_node 
  wire 
  wire_inner 
  wire_select
"""