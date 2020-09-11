// Filename: dnaTester.cxx
// Created by:  shochet (28Mar00)
//
////////////////////////////////////////////////////////////////////

#include "toontownbase.h"
#include "dnaLoader.h"
#include "dnaData.h"
#include "dnaGroup.h"
#include "dnaVisGroup.h"
#include "dnaStorage.h"
#include "dnaSuitPath.h"
#include "load_dna_file.h"

#include "pandaNode.h"
#include "nodePath.h"
#include "eventHandler.h"
#include "sceneGraphReducer.h"
#include "camera.h"
#include "coordinateSystem.h"

#include <stdlib.h>

DNAStorage *dna_store;
NodePath dna_test;

static void
event_T(CPT(Event)) {
  // Set up the fov and far plane to be Toontown's settings
  NodePath camera = NodePath(cameras);
  NodePath cam = camera.find("**/+Camera");
  ((Camera*)(cam.node()))->set_far(1000.0);
  ((Camera*)(cam.node()))->set_fov(45.0);

  // Test the AI loading
  //int res = load_DNA_file_AI(dna_store, "phase_5/dna/toontown_central_2100.dna", CS_default);
  //cerr << "load_DNA_file_AI res: " << res << endl;

  // Clear the dna store
  //dna_store->reset_DNAGroups();
  //dna_store->reset_DNAVisGroups();
  //dna_store->reset_DNAVisGroupsAI();
  //dna_store->reset_suit_points();
  //dna_store->reset_battle_cells();

  // Now load the real dna
  cerr << "load_DNA_file... " << endl;
  PT(PandaNode) dna_node = load_DNA_file(dna_store,
                                   "test.dna",
                                   CS_default, 1);
  cerr << "load_DNA_file done " << endl;


  // Parent the dna data read in to render
  NodePath render_nodePath = NodePath(render);
  dna_test = render_nodePath.attach_new_node(dna_node);

  int ng = dna_store->get_num_DNAVisGroups();
  for (int i = 0; i < ng; i++) {
    string group_name = dna_store->get_DNAVisGroup_name(i);
    cerr << "Group: " << group_name << endl;
    int nv = dna_store->get_num_visibles_in_DNAVisGroup(i);
    for (int j = 0; j < nv; j++) {
      string name = dna_store->get_visible_name(i, j);
      cerr << name << endl;
    }
    cerr << endl;
  }


  int ngAI = dna_store->get_num_DNAVisGroupsAI();
  cerr << "Num AI: " << ngAI << endl;
  for (int k = 0; k < ngAI; k++) {
    PT(DNAVisGroup) group = dna_store->get_DNAVisGroupAI(k);
    cerr << "Group AI: " << k << " " << group->get_name() << endl;
  }



  //dna_test.ls();

  // Get rid of the transitions and flatten
  SceneGraphReducer gr;
  gr.apply_attribs(dna_test.node());
  gr.flatten(dna_test.node(), 0);

  // Print out some of the storage for debugging
  dna_store->print_suit_point_storage();
  dna_store->print_battle_cell_storage();

  PT(DNASuitPath) path = dna_store->get_suit_path(dna_store->get_suit_point_at_index(0),
                                                  dna_store->get_suit_point_at_index(3));
  cout << "Path from 0 to 3: " << (*path) << endl;
}

static void
event_Y(CPT(Event)) {
  // Test cleanup functions
  dna_test.remove_node();
  dna_store->reset_hood();
  dna_store->reset_DNAGroups();
  dna_store->reset_DNAVisGroups();
  dna_store->reset_DNAVisGroupsAI();
}


static void
event_B(CPT(Event)) {
  // shift-B: show/hide barriers (collision polygons).
  static bool showing_collisions = false;

  showing_collisions = !showing_collisions;
  NodePath rp(render);
  if (showing_collisions) {
    rp.show_collision_solids();
    nout << "Showing collision solids.\n";
  } else {
    rp.hide_collision_solids();
    nout << "Hiding collision solids.\n";
  }
}

void demo_keys(EventHandler&) {
  event_handler.add_hook("shift-T", event_T);
  event_handler.add_hook("shift-Y", event_Y);
  event_handler.add_hook("shift-B", event_B);
}


int main(int argc, char *argv[]) {

  // Make the dna storage
  dna_store = new DNAStorage;

  // Load the shared storage models and textures
  load_DNA_file(dna_store, "phase_4/dna/storage.dna");

  // Load the neighborhood specific models and textures
  load_DNA_file(dna_store, "phase_4/dna/storage_TT.dna");
  load_DNA_file(dna_store, "phase_5/dna/storage_town.dna");
  load_DNA_file(dna_store, "phase_5/dna/storage_TT_town.dna");

  // For testing
  dna_store->print_node_storage();
  dna_store->print_texture_storage();

  dna_store->print_catalog();

  define_keys = &demo_keys;
  return framework_main(argc, argv);
}
