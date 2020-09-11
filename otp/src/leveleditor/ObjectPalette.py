"""
This is just a sample code.

LevelEditor, ObjectHandler, ObjectPalette should be rewritten
to be game specific.

You can define object template class inheriting ObjectBase
to define properties shared by multiple object types.
When you are defining properties
you should specify their name, UI type, data type,
update function, default value, and value range.

Then you need implement ObjectPalette class inheriting ObjectPaletteBase,
and in the populate function you can define ObjectPalette tree structure.
"""

from direct.leveleditor.ObjectPaletteBase import *

class ObjectProp(ObjectBase):
    def __init__(self, *args, **kw):
        ObjectBase.__init__(self, *args, **kw)
        self.properties['Abc'] =[OG.PROP_UI_RADIO, # UI type
                                 OG.PROP_STR,      # data type
                                 None,             # update function
                                 'a',              # default value
                                 ['a', 'b', 'c']]  # value range


class ObjectSmiley(ObjectProp):
    def __init__(self, *args, **kw):
        ObjectProp.__init__(self, *args, **kw)
        self.properties['123'] = [OG.PROP_UI_COMBO,
                                  OG.PROP_INT,
                                  None,
                                  1,
                                  [1, 2, 3]]


class ObjectDoubleSmileys(ObjectProp):
    def __init__(self, *args, **kw):
        ObjectProp.__init__(self, *args, **kw)
        self.properties['Distance'] = [OG.PROP_UI_SLIDE,
                                                    OG.PROP_FLOAT,
                                                    ('.updateDoubleSmiley',
                                                     {'val':OG.ARG_VAL, 'obj':OG.ARG_OBJ}),
                                                    # In this case, an update function for property is defined
                                                    # so whenever you change the value of this property from UI
                                                    # this update function will be called with these arguments.
                                                    # OG.ARG_VAL will be replaced by the value from UI.
                                                    # OG.ARG_OBJ will be replaced by object data structure.
                                                    # When an update function is starting with .
                                                    # it means this function belongs to the default objectHandler.
                                                    1.0, [0, 10, 0.1]]

        
class ObjectPalette(ObjectPaletteBase):
    def __init__(self):
        ObjectPaletteBase.__init__(self)

    def populate(self):
        # Create a group called 'Prop' in the ObjectPalette tree
        self.add('Prop')

        self.add('Pirates', 'Prop')
        for propName in ['barrel', 'basket', 'bench', 'bottle_brown', 'bucket',
                         'candle', 'cart_broken', 'cart_flat', 'cart_reg', 'chair_bar', 'crate', 'cup_tin',
                         'ham', 'jug', 'lamp_candle', 'pir_m_prp_fnc_woodfenceGate', 'pitcher_brown',
                         'rock_1_floor', 'treasureChest' ]:
            self.add(ObjectBase(name=propName, model='models/props/%s.bam'%propName), 'Pirates')


        self.add('Toontown', 'Prop')
        for propName in [
            'mailbox_TT', 'phone', 'receiver', 'shredder', 'spray', 'tart', 'big_planter'
            ]:
            self.add(ObjectBase(name=propName, model='phase_3.5/models/props/%s.bam'%propName), 'Toontown')        

        for propName in [
            'mickey_on_horse',
            'toontown_central_fountain',
            'piers_tt',
            ]:
            self.add(ObjectBase(name=propName, model='phase_4/models/props/%s.bam'%propName), 'Toontown')     

        for propName in ['baseball', 'dagger', 'lawbook', 'safe', 'trashcan_TT', 'TT_hydrant']:
            self.add(ObjectBase(name=propName, model='phase_5/models/props/%s.bam'%propName), 'Toontown')

        self.add(ObjectBase(name='tree',
                            createFunction = ('.createToontownTree', {}),
                            properties={'Tree Type':[OG.PROP_UI_COMBO,
                                                     OG.PROP_STR,
                                                     ('.updateToontownTree',
                                                      {'val':OG.ARG_VAL, 'obj':OG.ARG_OBJ}),
                                                     'prop_tree_fat_no_box_ul',
                                                     ['prop_tree_fat_no_box_ul',
                                                      'prop_tree_fat_brickbox_ul',
                                                      'prop_tree_fat_no_box_ur',
                                                      'prop_tree_fat_brickbox_ur',
                                                      'prop_tree_large_no_box_ul',
                                                      'prop_tree_large_woodbox_ul',
                                                      'prop_tree_large_brickbox_ul',
                                                      'prop_tree_large_no_box_ur',
                                                      'prop_tree_large_woodbox_ur',
                                                      'prop_tree_large_brickbox_ur',
                                                      'prop_tree_small_no_box_ul',
                                                      'prop_tree_small_woodbox_ul',
                                                      'prop_tree_small_brickbox_ul',
                                                      'prop_tree_small_nobox_ur',
                                                      'prop_tree_small_woodbox_ur',
                                                      'prop_tree_small_brickbox_ur',
                                                      ],
                                                     ],
                                        }),
                 'Toontown')

        self.add(ObjectBase(name='streetlight_TT',
                            createFunction = ('.createStreetlightTT', {}),
                            properties={'Light Type':[OG.PROP_UI_COMBO,
                                                      OG.PROP_STR,
                                                      ('.updateStreetlightTT',
                                                       {'val':OG.ARG_VAL, 'obj':OG.ARG_OBJ}),
                                                      'prop_post_one_light',
                                                      ['prop_post_one_light',
                                                       'prop_post_three_light',
                                                       'prop_post_sign'
                                                       ],
                                                      ],
                                        }),
                 'Toontown')
            
        # Create a group called 'Double Smileys' under 'Prop' group
        self.add('Double Smileys', 'Prop')

        # Add an object type 'Smiley' which is inheriting ObjectSmiley template
        # and have following properties.
        self.add(ObjectSmiley(name='Smiley',
                              model='models/smiley.egg',
                              models=['models/smiley.egg',
                                      'models/frowney.egg',
                                      'models/jack.egg'],
                              # when an object is just a simple geometry, you can define
                              # model, and models like this
                              # instead of defining createFunction
                              properties={'Happy':[OG.PROP_UI_CHECK,
                                                   OG.PROP_BOOL,
                                                   None,
                                                   True],
                                          'Number':[OG.PROP_UI_SPIN,
                                                    OG.PROP_INT,
                                                    ('.updateSmiley',
                                                     {'val':OG.ARG_VAL, 'obj':OG.ARG_OBJ}),
                                                    1, [1, 10]],
                                        }),
                 'Prop') # This object type will be added under the 'Prop' group.        
        self.add(ObjectDoubleSmileys(name='H Double Smiley',
                                     createFunction = ('.createDoubleSmiley', {})),
                                     # When the createFunction is defined like this,
                                     # this function will be called to create the object.
                                     # When a create function is starting with .
                                     # it means this function belongs to the default objectHandler.
                 'Double Smileys')

        self.add(ObjectDoubleSmileys(name='V Double Smiley',
                                     createFunction = ('.createDoubleSmiley', {'horizontal':False})),
                                     # You can specify argument for the create function, too
                 'Double Smileys')

        self.add('Animal')
        self.add(ObjectBase(name='Panda',
                            createFunction = ('.createPanda', {}),
                            anims = ['models/panda-walk4.egg',],
                            properties = {}),
                 'Animal')

        self.add(ObjectBase(name='dog', model='models/char/dog_hi.bam',
                            anims=['models/char/dog_idle_sitting.bam',
                                   'models/char/dog_idle_standing.bam',
                                   'models/char/dog_bark_sitting.bam',
                                   'models/char/dog_walk.bam'], actor=True),
                 'Animal')

        self.add('BG')
        self.add(ObjectBase(name='Grass',
                            createFunction = ('.createGrass', {}),
                            properties = {}),
                 'BG')

        self.add(ObjectBase(name='HQ_interior', model='phase_3.5/models/modules/HQ_interior.bam'), 'BG')
        self.add(ObjectBase(name='Toontown_Central', model='phase_4/models/neighborhoods/toontown_central.bam'), 'BG')
        self.add(ObjectBase(name='tortuga',
                            createFunction = ('.createTortuga', {}),
                            ),
                 'BG')

        self.add('Buildings')
        self.add('ToonBuildings', 'Buildings')
        for modelName in [
            'partyGate_TT',
            'trolley_station_TT',
            'safe_zone_tunnel_TT',
            'Speedway_Tunnel',
            'bank',
            'library',
            'school_house',
            'mercantile',
            'gagShop_TT',
            'PetShopExterior_TT',
            'clothshopTT',
            'gazebo',
            'toonhall',
            ]:
            self.add(ObjectBase(name=modelName, model='phase_4/models/modules/%s.bam'%modelName), 'ToonBuildings')

        self.add(ObjectBase(name='hqTT', model='phase_3.5/models/modules/hqTT.bam'), 'ToonBuildings')

        self.add('PiratesBuildings', 'Buildings')
        self.add(ObjectBase(name='Pier', model='models/islands/pier_platform.bam',
                            models=['models/islands/pier_platform',
                                    'models/islands/pier_port_royal_2deck',
                                    'models/islands/pier_1_kings',
                                    'models/islands/pier_2_kings',
                                    'models/islands/pier_port_royal_1deck',
                                    'models/islands/pier_walkway',
                                    'models/props/ship_parking_booth',
                                    'models/props/ship_valet',
                                    'models/islands/pier_midisland',]),
                 'PiratesBuildings')

        self.add(ObjectBase(name='Building Exterior',
                            model='models/buildings/jail_exterior',
                            models=['models/buildings/jail_exterior',
                                    'models/buildings/fort_door',
                                    'models/buildings/shanty_cellar_door',
                                    'models/buildings/shanty_guildhall_exterior',
                                    'models/buildings/shanty_gypsywagon_exterior',
                                    'models/buildings/shanty_tavern_exterior',
                                    'models/buildings/shanty_repairshop_exterior',
                                    'models/buildings/shanty_leanto_A',
                                    'models/buildings/shanty_leanto_B',
                                    'models/buildings/shanty_npc_house_a_exterior',
                                    'models/buildings/shanty_npc_house_combo_A',
                                    'models/buildings/shanty_npc_house_combo_B',
                                    'models/buildings/shanty_npc_house_combo_C',
                                    'models/buildings/shanty_npc_house_combo_D',
                                    'models/buildings/shanty_npc_house_combo_E',
                                    'models/buildings/shanty_npc_house_combo_F',
                                    'models/buildings/shanty_npc_house_combo_G',
                                    'models/buildings/shanty_npc_house_combo_H',
                                    'models/buildings/shanty_npc_house_combo_I',
                                    'models/buildings/shanty_npc_house_combo_J',
                                    'models/buildings/shanty_npc_house_combo_Platform',
                                    'models/buildings/shanty_signpost',
                                    'models/buildings/spanish_npc_house_a_exterior',
                                    'models/buildings/spanish_npc_house_b_exterior',
                                    'models/buildings/spanish_npc_house_c_exterior',
                                    'models/buildings/spanish_npc_house_d_exterior',
                                    'models/buildings/spanish_npc_house_e_exterior',
                                    'models/buildings/spanish_npc_house_f_exterior',
                                    'models/buildings/spanish_npc_house_g_exterior',
                                    'models/buildings/spanish_npc_house_i_exterior',
                                    'models/buildings/spanish_npc_house_j_exterior',
                                    'models/buildings/spanish_npc_house_k_exterior',
                                    'models/buildings/spanish_npc_house_l_exterior',
                                    'models/buildings/spanish_npc_house_n_exterior',
                                    'models/buildings/spanish_npc_house_o_exterior',
                                    'models/buildings/spanish_npc_house_p_exterior',
                                    'models/buildings/spanish_npc_house_q_exterior',
                                    'models/buildings/spanish_tavern_exterior',
                                    'models/buildings/pir_m_bld_spn_tavern',
                                    'models/buildings/pir_m_bld_spn_tavern_burned',
                                    'models/buildings/pir_m_bld_spn_tavern_door',
                                    'models/town/bar_exterior',
                                    'models/buildings/spanish_npc_attach_fullarchL',
                                    'models/buildings/spanish_npc_attach_fullarchR',
                                    'models/buildings/spanish_npc_attach_fullnostonearchL',
                                    'models/buildings/spanish_npc_attach_fullnostonearchR',
                                    'models/buildings/spanish_npc_attach_halfarchL',
                                    'models/buildings/spanish_npc_attach_halfarchR',
                                    'models/buildings/spanish_npc_attach_halfarchflatL',
                                    'models/buildings/spanish_npc_attach_halfarchflatR',
                                    'models/buildings/spanish_npc_attach_halfarchwindowL',
                                    'models/buildings/spanish_npc_attach_halfarchwindowR',
                                    'models/buildings/spanish_npc_attach_halfporchL',
                                    'models/buildings/spanish_npc_attach_halfporchR',
                                    'models/buildings/burned_gate',
                                    'models/buildings/burned_half_house',
                                    'models/buildings/burned_house',
                                    'models/buildings/burned_woods',
                                    'models/buildings/english_a',
                                    'models/buildings/english_b',
                                    'models/buildings/english_c',
                                    'models/buildings/english_d',
                                    'models/buildings/english_e',
                                    'models/buildings/english_f',
                                    'models/buildings/english_g',
                                    'models/buildings/english_h',
                                    'models/buildings/english_i',
                                    'models/buildings/english_j',
                                    'models/buildings/english_k',
                                    'models/buildings/english_k_tutorial',
                                    'models/buildings/english_l',
                                    'models/buildings/english_m',
                                    'models/buildings/english_n',
                                    'models/buildings/english_corner_a',
                                    'models/buildings/english_corner_b',
                                    'models/buildings/english_corner_c',
                                    'models/buildings/english_corner_c2',
                                    'models/buildings/english_corner_d',
                                    'models/buildings/english_corner_e',
                                    'models/buildings/english_corner_f',
                                    'models/buildings/english_mansion',
                                    'models/buildings/pir_m_bld_eng_mansion',
                                    'models/buildings/pir_m_bld_eng_mansion_burned',
                                    'models/buildings/pir_m_bld_eng_mansion_door',
                                    'models/buildings/fort_eitc',
                                    'models/buildings/fort_small_cave',
                                    'models/islands/kingshead_zero',
                                    'models/buildings/pir_m_bld_frt_innerWall_gate',
                                    ]),
                 'PiratesBuildings')
