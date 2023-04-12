"""Script for applying gap filling according to specific definitions

When loading the script, a menu "My menu" is added to QTM with a submenu "Gap fill..." containing a list of
gap fill action buttons.

When pressing a gap fill action button, the action is applied to all the gaps of the target trajectory in the
current measurement.

This script is especially helpful for applying relational or virtual gap filling according to a predefined set
of relations.

The gap fill actions are compiled from a list of gap fill definitions specified by the global variable
`list_of_definitions` in this script. The list can easily be customized by editing this variable.

The list items in list_of_definitions are formatted as a dictionary with the following key-value combinations:
  display_name: Name of the definition appearing in the submenu
  target: Name of the trajectory to be filled
  method: gap fill method, corresponding to the `algorithm` variable in the QTM Common API `fill_trajectory` method
  settings: settings definition for relational and virtual gap fill, which is a dictionary with key-value combinations:
    origin: Name of trajectory to be used as origin in the gap fill relation (automatically converted to trajectory ID)
    line: Name of trajectory defining the line in the gap fill relation (automatically converted to trajectory ID)
    plane: Name of the trajectory defining the plane in the gap fill relation (automatically converted to trajectory ID)
    offset: XYZ offset (vec3f, directly passed to the `fill_trajectory` method)
    is_rigid_body (bool, directly passed to the `fill_trajectory` method)
    is_relative_offset (bool, directly passed to the `fill_trajectory` method)
  
  For more information about settings, see the QTM Common API documentation for the `fill_trajectory` method.

Current limitations of the script:
  There is no check if trajectories with the specified names exist. Applying actions containing
    non existing trajectories will produce a run time error.
  Relational and virtual gap fill methods produce a run time error when the other trajectories used
    in the relation contain gaps overlapping with parts to be filled.
"""

import qtm
in_qtm = True
if not in_qtm:
    import qtm_stub as qtm

import qtm.data.object.trajectory as traj
import qtm.data.series._3d as data_3d

import qtm.gui.timeline as tline
import qtm.gui.terminal as trm
import qtm.utilities.color as clr

import numpy as np

import copy

# list_of_definitions = [\
    # {"display_name": "WaistBack (polynomial)", "target": "WaistBack", "method": "polynomial"},\
    # {"display_name": "WaistBack (kinematic)", "target": "WaistBack", "method": "kinematic"},\
    # {"display_name": "WaistLFront (rel): WaistBack-WaistRFront-WaistL", "target": "WaistLFront", "method": "relational", "settings": {"origin": "WaistBack", "line": "WaistRFront", "plane": "WaistL"}},\
    # {"display_name": "WaistRFront (rel): WaistBack-WaistLFront-WaistR", "target": "WaistRFront", "method": "relational", "settings": {"origin": "WaistBack", "line": "WaistLFront", "plane": "WaistR"}}\
    # ]

# Edit the list of definitions for specifying the gap fill actions
list_of_definitions = [\
    {"display_name": "Q_WaistBack (polynomial)", "target": "Q_WaistBack", "method": "polynomial"},\
    {"display_name": "Q_WaistBack (kinematic)", "target": "Q_WaistBack", "method": "kinematic"},\
    {"display_name": "Q_WaistLFront (rel): WaistBack-WaistRFront-WaistL", "target": "Q_WaistLFront", "method": "relational", "settings": {"origin": "Q_WaistBack", "line": "Q_WaistRFront", "plane": "Q_WaistL"}},\
    {"display_name": "Q_WaistRFront (rel): WaistBack-WaistLFront-WaistR", "target": "Q_WaistRFront", "method": "relational", "settings": {"origin": "Q_WaistBack", "line": "Q_WaistLFront", "plane": "Q_WaistR"}}\
    ]


def _gap_fill_def(def_id):
    """Function for parsing and applying gap fill definitions"""
    #find trakectory ID of target
    gf_def = list_of_definitions[def_id]
    id_target = traj.find_trajectory(gf_def["target"])
    
    #find gap ranges:
    gap_ranges = data_3d.get_gap_ranges(id_target)
    #n_gaps = len(gap_ranges)
    #print('Number of gaps: ' + str(n_gaps))
    
    gf_method = gf_def["method"]
    if gf_method in ["relational", "virtual"]:
        # Convert settings (modify local copy of the settings definition)
        settings = copy.deepcopy(gf_def["settings"])
        if "origin" in settings.keys():
            marker_name = settings["origin"]
            settings["origin"] = traj.find_trajectory(marker_name)
        if "line" in settings.keys():
            marker_name = settings["line"]
            settings["line"] = traj.find_trajectory(marker_name)
        if "plane" in settings.keys():
            marker_name = settings["plane"]
            settings["plane"] = traj.find_trajectory(marker_name)
    else:
        settings = None
    
    gf_action = gf_def["display_name"]
    trm.write(f"Applying gap filling action {gf_action}")
    not_all_gaps_filled_flag = False
    for gap in gap_ranges:
        #print(gap)
        try:
            traj.fill_trajectory(id_target, gf_method, gap, settings) # May result in run time error when there are gaps in surrounding trajectories
        except:
            not_all_gaps_filled_flag = True
            continue
    
    if not_all_gaps_filled_flag:
        trm.write("- Not all gaps could be filled")


def add_my_commands():
    """Function for adding new commands used in this script to QTM"""
    # Add commands for 10 relations (maximum number of relations, you can add more here if you want)
    # Work around for adding commands in for-loop since Python uses call by assignment
    command_name = "gap_fill_def_0"
    qtm.gui.add_command(command_name)
    qtm.gui.set_command_execute_function(command_name, lambda:(_gap_fill_def(0)))
    
    command_name = "gap_fill_def_1"
    qtm.gui.add_command(command_name)
    qtm.gui.set_command_execute_function(command_name, lambda:(_gap_fill_def(1)))
    
    command_name = "gap_fill_def_2"
    qtm.gui.add_command(command_name)
    qtm.gui.set_command_execute_function(command_name, lambda:(_gap_fill_def(2)))
    
    command_name = "gap_fill_def_3"
    qtm.gui.add_command(command_name)
    qtm.gui.set_command_execute_function(command_name, lambda:(_gap_fill_def(3)))
    
    command_name = "gap_fill_def_4"
    qtm.gui.add_command(command_name)
    qtm.gui.set_command_execute_function(command_name, lambda:(_gap_fill_def(4)))
    
    command_name = "gap_fill_def_5"
    qtm.gui.add_command(command_name)
    qtm.gui.set_command_execute_function(command_name, lambda:(_gap_fill_def(5)))
    
    command_name = "gap_fill_def_6"
    qtm.gui.add_command(command_name)
    qtm.gui.set_command_execute_function(command_name, lambda:(_gap_fill_def(6)))
    
    command_name = "gap_fill_def_7"
    qtm.gui.add_command(command_name)
    qtm.gui.set_command_execute_function(command_name, lambda:(_gap_fill_def(7)))
    
    command_name = "gap_fill_def_8"
    qtm.gui.add_command(command_name)
    qtm.gui.set_command_execute_function(command_name, lambda:(_gap_fill_def(8)))
    
    command_name = "gap_fill_def_9"
    qtm.gui.add_command(command_name)
    qtm.gui.set_command_execute_function(command_name, lambda:(_gap_fill_def(9)))
    


def setup_my_menu():
    """Function for setting up the menu."""
    my_menu_id = qtm.gui.insert_menu_submenu(None, "My menu")
    #qtm.gui.insert_menu_button(my_menu_id, "Fill (rel) WaistLFront", "rel_fill_waistlfront")
    gf_sub_id = qtm.gui.insert_menu_submenu(my_menu_id, "Gap fill...")

    # Add buttons for respective relations
    # Alt. use set_draw_function callback for automatic update
    #qtm.gui.insert_menu_button(rfrb_id, "Update rigid body list...", "update_rb_refine_submenu")
    for i in range(len(list_of_definitions)):
        disp_name = list_of_definitions[i]["display_name"]
        command_name = "gap_fill_def_" + str(i)
        if not(any(uc == command_name for uc in qtm.gui.get_commands("user"))):
            trm.write(f"Number of gap fill definitions exceeds maximum:\n" + \
                f"- Definitions {i+1} and higher are ignored.")
            break
            
        # Add button to Refine rigid body submenu with the rigid body name and associated command
        qtm.gui.insert_menu_button(gf_sub_id, disp_name, command_name)


# Initial script actions (local 'main')
# - Add commands and set up menu
add_my_commands()
setup_my_menu()

