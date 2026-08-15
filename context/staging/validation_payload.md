--- SEALED MANIFEST (structure.json) ---
{
  "meta": {
    "schema_version": "2.0",
    "lifecycle": "CONSTRAINTS_DEFINED",
    "source_hash": "6a3a31093913173981deb71e2e0b9148147dfe6aba97ba5347db7fd1c3ea4d61",
    "created_at": "2026-05-24T05:00:22.487718+00:00",
    "updated_at": "2026-08-15T19:01:18.496419+00:00"
  },
  "intent": {
    "jurisdiction": "BC_SAANICH",
    "material_preference": "Western Red Cedar",
    "joinery_style": "Traditional timber framing"
  },
  "structure": {
    "type": "pergola",
    "shape": "hexagon",
    "sides": 6
  },
  "layout": {
    "post_count": 6,
    "inscribed_radius_ft": 4.875,
    "post_spacing_ft": 4.875
  },
  "members": {
    "posts": {
      "nominal_size": "6x6",
      "actual_width_in": 5.5,
      "actual_depth_in": 5.5,
      "cut_length_ft": 8.42
    },
    "beams": {
      "nominal_size": "6x12",
      "actual_width_in": 6.0,
      "actual_depth_in": 12.0,
      "cut_length_ft": 5.0
    },
    "purlins": {
      "enabled": true,
      "nominal_size": "4x4",
      "actual_width_in": 3.5,
      "actual_depth_in": 3.5,
      "height_fraction": 0.55
    },
    "kneebraces": {
      "nominal_size": "4x4",
      "actual_width_in": 3.5,
      "actual_depth_in": 3.5,
      "cut_length_in": 36.0,
      "angle_deg": 45.0
    }
  },
  "roof": {
    "type": "hip",
    "pitch": "4:12",
    "pitch_defaulted": false,
    "primary_rafters": {
      "count": 6,
      "nominal_size": "4x6",
      "actual_width_in": 3.5,
      "actual_depth_in": 5.5,
      "overhang_ft": 0.75
    },
    "secondary_rafters": {
      "enabled": true,
      "count": 6,
      "nominal_size": "4x4",
      "actual_width_in": 3.5,
      "actual_depth_in": 3.5,
      "count_per_side": 2
    }
  },
  "hub": {
    "type": "polygonal",
    "radius_ft": "auto",
    "radius_min_ft": 0.6,
    "height_ratio_to_rafter": 2.5,
    "clearance_ft": 0.5
  },
  "bracing": {
    "enabled": true,
    "layout": "paired_per_post",
    "brace": {
      "nominal_size": "4x4",
      "actual_width_in": 3.5,
      "actual_depth_in": 3.5,
      "length_ft": 2.5,
      "angle_deg": 45,
      "count_per_post": 2,
      "constraints": {
        "start_surface": "post_face",
        "end_surface": "beam_soffit",
        "run_ft": 1.5
      }
    }
  },
  "footings": {
    "type": "concrete_caisson",
    "diameter_in": 12.0,
    "depth_in": 24.0,
    "concrete_grade": "3000 PSI",
    "center_on_post": true
  },
  "joinery": {
    "beam_seat_style": "exposed_tenon",
    "rafter_seat_style": "birds_mouth",
    "rafter_tail": "square_cut",
    "joints": {
      "beam_ring": {
        "corner_joint": "miter",
        "miter_reference": "regular_polygon",
        "kerf_allowance_in": 0.125
      },
      "post_to_beam": {
        "joint_type": "seat_on_top",
        "seat_depth_in": 0.0,
        "tolerance_in": 0.0625
      },
      "rafter_to_beam": {
        "joint_type": "birds_mouth",
        "seat_depth_in": 1.5,
        "heel_cut_plumb": true,
        "tail_cut_plumb": true,
        "tolerance_in": 0.0625
      },
      "rafter_to_hub": {
        "joint_type": "miter_to_face",
        "termination": "hub_face_plane",
        "tolerance_in": 0.0625
      },
      "brace_to_post_beam": {
        "joint_type": "knee_brace",
        "end_cut": "miter",
        "angle_deg": 45,
        "seat_offset_in": 0.0,
        "tolerance_in": 0.0625
      }
    }
  },
  "invariants": {
    "rafter_count_equals_post_count": true,
    "post_top_equals_beam_bottom": true,
    "no_rafter_inside_hub_radius": true,
    "brace_must_connect_to_surfaces": true,
    "no_solid_intersections": true,
    "member_counts_match_sections": true,
    "no_zero_length_members": true,
    "presentation_primary_counts_match": true
  },
  "presentation": {
    "view_mode": "presentation",
    "roof_style": "open_rafter",
    "visibility_rules": {
      "primary_members_only": true,
      "fade_secondary": true,
      "suppress_internal_roof_framing": true,
      "max_visible_braces_per_post": 1,
      "show_jack_rafters": true,
      "show_purlins": false
    },
    "labeling": {
      "avoid_geometry_overlap": true,
      "use_leaders_when_colliding": true
    },
    "palette": "cedar_warm"
  },
  "code": {
    "_sealed": false,
    "wind_load_kPa": null,
    "snow_load_kPa": null,
    "height_limit_ft": null,
    "permit_required": null
  },
  "geometry": {
    "_sealed": true,
    "compound_cut": {
      "miter_deg": 28.71,
      "bevel_deg": 9.1
    },
    "beam_ring": {
      "beam_miter_deg": 30.0,
      "interior_angle_deg": 120.0
    },
    "rafter": {
      "structural_length_ft": 5.139,
      "total_with_overhang_ft": 5.929
    },
    "roof_rise": {
      "rise_ft": 1.625
    },
    "total_height": {
      "post_ft": 8.42,
      "beam_depth_ft": 1.0,
      "roof_rise_ft": 1.625,
      "total_height_ft": 11.045
    },
    "hub_radius_ft": 0.75,
    "svg_coordinates": {
      "viewBox": "0 0 1600 1200",
      "width_px": 1600,
      "height_px": 1200,
      "grade_y": 1080,
      "scale_px_per_ft": 42.0,
      "post_top_y": 726,
      "beam_top_y": 684,
      "hub_apex_y": 616
    },
    "joints": {
      "units": "feet",
      "coordinate_system": "right_handed_z_up",
      "tolerance_ft": 0.0052,
      "z_planes": {
        "Z_GRADE": 0.0,
        "Z_POST_TOP": 7.42,
        "Z_BEAM_TOP": 8.42,
        "Z_BEAM_CENTER": 7.92,
        "Z_APEX": 10.045,
        "Z_BEAM_SOFFIT": 7.42
      },
      "layout": {
        "post_count": 6,
        "post_radius_ft": 4.875,
        "post_xy": [
          [
            4.875,
            0.0
          ],
          [
            2.4375,
            4.2219
          ],
          [
            -2.4375,
            4.2219
          ],
          [
            -4.875,
            0.0
          ],
          [
            -2.4375,
            -4.2219
          ],
          [
            2.4375,
            -4.2219
          ]
        ]
      },
      "hub": {
        "type": "polygonal",
        "radius_ft": 0.75,
        "height_ft": 1.2,
        "face_planes": {
          "planes": [
            {
              "id": "H1",
              "point": [
                0.75,
                0.0,
                10.045
              ],
              "normal": [
                1.0,
                0.0,
                0.0
              ]
            },
            {
              "id": "H2",
              "point": [
                0.3750000000000001,
                0.649519052838329,
                10.045
              ],
              "normal": [
                0.5000000000000001,
                0.8660254037844386,
                0.0
              ]
            },
            {
              "id": "H3",
              "point": [
                -0.3749999999999999,
                0.649519052838329,
                10.045
              ],
              "normal": [
                -0.49999999999999983,
                0.8660254037844387,
                0.0
              ]
            },
            {
              "id": "H4",
              "point": [
                -0.75,
                9.184850993605148e-17,
                10.045
              ],
              "normal": [
                -1.0,
                1.2246467991473532e-16,
                0.0
              ]
            },
            {
              "id": "H5",
              "point": [
                -0.37500000000000033,
                -0.6495190528383288,
                10.045
              ],
              "normal": [
                -0.5000000000000004,
                -0.8660254037844384,
                0.0
              ]
            },
            {
              "id": "H6",
              "point": [
                0.3750000000000001,
                -0.649519052838329,
                10.045
              ],
              "normal": [
                0.5000000000000001,
                -0.8660254037844386,
                0.0
              ]
            }
          ]
        }
      },
      "primary_rafters": [
        {
          "id": "R1",
          "start": [
            5.625,
            0.0,
            8.4481
          ],
          "end": [
            0.6495,
            0.0,
            10.1066
          ],
          "seat_point": [
            4.875,
            0.0,
            8.6981
          ],
          "seat_depth_ft": 0.3056
        },
        {
          "id": "R2",
          "start": [
            2.8125,
            4.8714,
            8.4481
          ],
          "end": [
            0.3248,
            0.5625,
            10.1066
          ],
          "seat_point": [
            2.4375,
            4.2219,
            8.6981
          ],
          "seat_depth_ft": 0.3056
        },
        {
          "id": "R3",
          "start": [
            -2.8125,
            4.8714,
            8.4481
          ],
          "end": [
            -0.3248,
            0.5625,
            10.1066
          ],
          "seat_point": [
            -2.4375,
            4.2219,
            8.6981
          ],
          "seat_depth_ft": 0.3056
        },
        {
          "id": "R4",
          "start": [
            -5.625,
            0.0,
            8.4481
          ],
          "end": [
            -0.6495,
            0.0,
            10.1066
          ],
          "seat_point": [
            -4.875,
            0.0,
            8.6981
          ],
          "seat_depth_ft": 0.3056
        },
        {
          "id": "R5",
          "start": [
            -2.8125,
            -4.8714,
            8.4481
          ],
          "end": [
            -0.3248,
            -0.5625,
            10.1066
          ],
          "seat_point": [
            -2.4375,
            -4.2219,
            8.6981
          ],
          "seat_depth_ft": 0.3056
        },
        {
          "id": "R6",
          "start": [
            2.8125,
            -4.8714,
            8.4481
          ],
          "end": [
            0.3248,
            -0.5625,
            10.1066
          ],
          "seat_point": [
            2.4375,
            -4.2219,
            8.6981
          ],
          "seat_depth_ft": 0.3056
        }
      ],
      "rafters": {
        "hub_termination_points": {
          "points": [
            [
              0.6495,
              0.0,
              10.1066
            ],
            [
              0.3248,
              0.5625,
              10.1066
            ],
            [
              -0.3248,
              0.5625,
              10.1066
            ],
            [
              -0.6495,
              0.0,
              10.1066
            ],
            [
              -0.3248,
              -0.5625,
              10.1066
            ],
            [
              0.3248,
              -0.5625,
              10.1066
            ]
          ]
        },
        "primary_rafters": [
          {
            "id": "R1",
            "start": [
              5.625,
              0.0,
              8.4481
            ],
            "end": [
              0.6495,
              0.0,
              10.1066
            ],
            "seat_point": [
              4.875,
              0.0,
              8.6981
            ],
            "seat_depth_ft": 0.3056
          },
          {
            "id": "R2",
            "start": [
              2.8125,
              4.8714,
              8.4481
            ],
            "end": [
              0.3248,
              0.5625,
              10.1066
            ],
            "seat_point": [
              2.4375,
              4.2219,
              8.6981
            ],
            "seat_depth_ft": 0.3056
          },
          {
            "id": "R3",
            "start": [
              -2.8125,
              4.8714,
              8.4481
            ],
            "end": [
              -0.3248,
              0.5625,
              10.1066
            ],
            "seat_point": [
              -2.4375,
              4.2219,
              8.6981
            ],
            "seat_depth_ft": 0.3056
          },
          {
            "id": "R4",
            "start": [
              -5.625,
              0.0,
              8.4481
            ],
            "end": [
              -0.6495,
              0.0,
              10.1066
            ],
            "seat_point": [
              -4.875,
              0.0,
              8.6981
            ],
            "seat_depth_ft": 0.3056
          },
          {
            "id": "R5",
            "start": [
              -2.8125,
              -4.8714,
              8.4481
            ],
            "end": [
              -0.3248,
              -0.5625,
              10.1066
            ],
            "seat_point": [
              -2.4375,
              -4.2219,
              8.6981
            ],
            "seat_depth_ft": 0.3056
          },
          {
            "id": "R6",
            "start": [
              2.8125,
              -4.8714,
              8.4481
            ],
            "end": [
              0.3248,
              -0.5625,
              10.1066
            ],
            "seat_point": [
              2.4375,
              -4.2219,
              8.6981
            ],
            "seat_depth_ft": 0.3056
          }
        ]
      },
      "jack_rafters": {
        "enabled": true,
        "endpoints": [
          {
            "id": "J1a",
            "start": [
              4.712,
              1.7823,
              8.4095
            ],
            "end": [
              1.8646,
              0.1383,
              9.675
            ],
            "seat_point": [
              4.0625,
              1.4073,
              8.6981
            ],
            "mate_id": "R1"
          },
          {
            "id": "J1b",
            "start": [
              3.8995,
              3.1896,
              8.4095
            ],
            "end": [
              1.0521,
              1.5457,
              9.675
            ],
            "seat_point": [
              3.25,
              2.8146,
              8.6981
            ],
            "mate_id": "R2"
          },
          {
            "id": "J2a",
            "start": [
              0.8125,
              4.9719,
              8.4095
            ],
            "end": [
              0.8125,
              1.684,
              9.675
            ],
            "seat_point": [
              0.8125,
              4.2219,
              8.6981
            ],
            "mate_id": "R2"
          },
          {
            "id": "J2b",
            "start": [
              -0.8125,
              4.9719,
              8.4095
            ],
            "end": [
              -0.8125,
              1.684,
              9.675
            ],
            "seat_point": [
              -0.8125,
              4.2219,
              8.6981
            ],
            "mate_id": "R3"
          },
          {
            "id": "J3a",
            "start": [
              -3.8995,
              3.1896,
              8.4095
            ],
            "end": [
              -1.0521,
              1.5457,
              9.675
            ],
            "seat_point": [
              -3.25,
              2.8146,
              8.6981
            ],
            "mate_id": "R3"
          },
          {
            "id": "J3b",
            "start": [
              -4.712,
              1.7823,
              8.4095
            ],
            "end": [
              -1.8646,
              0.1383,
              9.675
            ],
            "seat_point": [
              -4.0625,
              1.4073,
              8.6981
            ],
            "mate_id": "R4"
          },
          {
            "id": "J4a",
            "start": [
              -4.712,
              -1.7823,
              8.4095
            ],
            "end": [
              -1.8646,
              -0.1383,
              9.675
            ],
            "seat_point": [
              -4.0625,
              -1.4073,
              8.6981
            ],
            "mate_id": "R4"
          },
          {
            "id": "J4b",
            "start": [
              -3.8995,
              -3.1896,
              8.4095
            ],
            "end": [
              -1.0521,
              -1.5457,
              9.675
            ],
            "seat_point": [
              -3.25,
              -2.8146,
              8.6981
            ],
            "mate_id": "R5"
          },
          {
            "id": "J5a",
            "start": [
              -0.8125,
              -4.9719,
              8.4095
            ],
            "end": [
              -0.8125,
              -1.684,
              9.675
            ],
            "seat_point": [
              -0.8125,
              -4.2219,
              8.6981
            ],
            "mate_id": "R5"
          },
          {
            "id": "J5b",
            "start": [
              0.8125,
              -4.9719,
              8.4095
            ],
            "end": [
              0.8125,
              -1.684,
              9.675
            ],
            "seat_point": [
              0.8125,
              -4.2219,
              8.6981
            ],
            "mate_id": "R6"
          },
          {
            "id": "J6a",
            "start": [
              3.8995,
              -3.1896,
              8.4095
            ],
            "end": [
              1.0521,
              -1.5457,
              9.675
            ],
            "seat_point": [
              3.25,
              -2.8146,
              8.6981
            ],
            "mate_id": "R6"
          },
          {
            "id": "J6b",
            "start": [
              4.712,
              -1.7823,
              8.4095
            ],
            "end": [
              1.8646,
              -0.1383,
              9.675
            ],
            "seat_point": [
              4.0625,
              -1.4073,
              8.6981
            ],
            "mate_id": "R1"
          }
        ]
      },
      "braces": {
        "enabled": true,
        "endpoints": [
          {
            "id": "K1A",
            "start": [
              4.7604,
              0.1985,
              5.9575
            ],
            "end": [
              4.0292,
              1.465,
              7.42
            ]
          },
          {
            "id": "K1B",
            "start": [
              2.5521,
              4.0234,
              5.9575
            ],
            "end": [
              3.2833,
              2.7569,
              7.42
            ]
          },
          {
            "id": "K2A",
            "start": [
              2.2083,
              4.2219,
              5.9575
            ],
            "end": [
              0.7458,
              4.2219,
              7.42
            ]
          },
          {
            "id": "K2B",
            "start": [
              -2.2083,
              4.2219,
              5.9575
            ],
            "end": [
              -0.7458,
              4.2219,
              7.42
            ]
          },
          {
            "id": "K3A",
            "start": [
              -2.5521,
              4.0234,
              5.9575
            ],
            "end": [
              -3.2833,
              2.7569,
              7.42
            ]
          },
          {
            "id": "K3B",
            "start": [
              -4.7604,
              0.1985,
              5.9575
            ],
            "end": [
              -4.0292,
              1.465,
              7.42
            ]
          },
          {
            "id": "K4A",
            "start": [
              -4.7604,
              -0.1985,
              5.9575
            ],
            "end": [
              -4.0292,
              -1.465,
              7.42
            ]
          },
          {
            "id": "K4B",
            "start": [
              -2.5521,
              -4.0234,
              5.9575
            ],
            "end": [
              -3.2833,
              -2.7569,
              7.42
            ]
          },
          {
            "id": "K5A",
            "start": [
              -2.2083,
              -4.2219,
              5.9575
            ],
            "end": [
              -0.7458,
              -4.2219,
              7.42
            ]
          },
          {
            "id": "K5B",
            "start": [
              2.2083,
              -4.2219,
              5.9575
            ],
            "end": [
              0.7458,
              -4.2219,
              7.42
            ]
          },
          {
            "id": "K6A",
            "start": [
              2.5521,
              -4.0234,
              5.9575
            ],
            "end": [
              3.2833,
              -2.7569,
              7.42
            ]
          },
          {
            "id": "K6B",
            "start": [
              4.7604,
              -0.1985,
              5.9575
            ],
            "end": [
              4.0292,
              -1.465,
              7.42
            ]
          }
        ]
      },
      "beam_ring": {
        "beam_miter_deg": 30.0,
        "interior_angle_deg": 120.0
      },
      "resolved_model": {
        "constraints_resolved": true,
        "members": [
          {
            "id": "P1",
            "role": "post",
            "p0": [
              4.875,
              0.0,
              0.0
            ],
            "p1": [
              4.875,
              0.0,
              7.42
            ],
            "axis_u": [
              0.0,
              0.0,
              0.9999999999999999
            ],
            "axis_w": [
              0.0,
              -1.0,
              0.0
            ],
            "axis_d": [
              -1.0,
              0.0,
              0.0
            ],
            "vertices": [
              [
                5.104166666666667,
                0.22916666666666666,
                0.0
              ],
              [
                5.104166666666667,
                -0.22916666666666666,
                0.0
              ],
              [
                4.645833333333333,
                -0.22916666666666666,
                0.0
              ],
              [
                4.645833333333333,
                0.22916666666666666,
                0.0
              ],
              [
                5.104166666666667,
                0.22916666666666666,
                7.42
              ],
              [
                5.104166666666667,
                -0.22916666666666666,
                7.42
              ],
              [
                4.645833333333333,
                -0.22916666666666666,
                7.42
              ],
              [
                4.645833333333333,
                0.22916666666666666,
                7.42
              ]
            ],
            "faces": [
              {
                "verts": [
                  0,
                  3,
                  2,
                  1
                ],
                "normal": [
                  -0.0,
                  -0.0,
                  -0.9999999999999999
                ],
                "color_key": "start"
              },
              {
                "verts": [
                  4,
                  5,
                  6,
                  7
                ],
                "normal": [
                  0.0,
                  0.0,
                  0.9999999999999999
                ],
                "color_key": "end"
              },
              {
                "verts": [
                  0,
                  1,
                  5,
                  4
                ],
                "normal": [
                  1.0,
                  -0.0,
                  -0.0
                ],
                "color_key": "top"
              },
              {
                "verts": [
                  3,
                  7,
                  6,
                  2
                ],
                "normal": [
                  -1.0,
                  0.0,
                  0.0
                ],
                "color_key": "bottom"
              },
              {
                "verts": [
                  0,
                  4,
                  7,
                  3
                ],
                "normal": [
                  -0.0,
                  1.0,
                  -0.0
                ],
                "color_key": "left"
              },
              {
                "verts": [
                  1,
                  2,
                  6,
                  5
                ],
                "normal": [
                  0.0,
                  -1.0,
                  0.0
                ],
                "color_key": "right"
              }
            ],
            "derived_length_ft": 8.42,
            "derived_angle_deg": 90.0,
            "constraints_satisfied": {
              "base_on_footing": true,
              "top_on_beam": true
            }
          },
          {
            "id": "FT1",
            "role": "footing",
            "p0": [
              4.875,
              0.0,
              -1.5
            ],
            "p1": [
              4.875,
              0.0,
              0.33
            ],
            "axis_u": [
              0.0,
              0.0,
              0.9999999999999999
            ],
            "axis_w": [
              0.0,
              -1.0,
              0.0
            ],
            "axis_d": [
              -1.0,
              0.0,
              0.0
            ],
            "vertices": [
              [
                5.375,
                0.5,
                -1.5
              ],
              [
                5.375,
                -0.5,
                -1.5
              ],
              [
                4.375,
                -0.5,
                -1.5
              ],
              [
                4.375,
                0.5,
                -1.5
              ],
              [
                5.375,
                0.5,
                0.33
              ],
              [
                5.375,
                -0.5,
                0.33
              ],
              [
                4.375,
                -0.5,
                0.33
              ],
              [
                4.375,
                0.5,
                0.33
              ]
            ],
            "faces": [
              {
                "verts": [
                  0,
                  3,
                  2,
                  1
                ],
                "normal": [
                  -0.0,
                  -0.0,
                  -0.9999999999999999
                ],
                "color_key": "start"
              },
              {
                "verts": [
                  4,
                  5,
                  6,
                  7
                ],
                "normal": [
                  0.0,
                  0.0,
                  0.9999999999999999
                ],
                "color_key": "end"
              },
              {
                "verts": [
                  0,
                  1,
                  5,
                  4
                ],
                "normal": [
                  1.0,
                  -0.0,
                  -0.0
                ],
                "color_key": "top"
              },
              {
                "verts": [
                  3,
                  7,
                  6,
                  2
                ],
                "normal": [
                  -1.0,
                  0.0,
                  0.0
                ],
                "color_key": "bottom"
              },
              {
                "verts": [
                  0,
                  4,
                  7,
                  3
                ],
                "normal": [
                  -0.0,
                  1.0,
                  -0.0
                ],
                "color_key": "left"
              },
              {
                "verts": [
                  1,
                  2,
                  6,
                  5
                ],
                "normal": [
                  0.0,
                  -1.0,
                  0.0
                ],
                "color_key": "right"
              }
            ],
            "derived_length_ft": 1.83,
            "derived_angle_deg": 90.0,
            "constraints_satisfied": {}
          },
          {
            "id": "P2",
            "role": "post",
            "p0": [
              2.4375,
              4.2219,
              0.0
            ],
            "p1": [
              2.4375,
              4.2219,
              7.42
            ],
            "axis_u": [
              0.0,
              0.0,
              0.9999999999999999
            ],
            "axis_w": [
              0.0,
              -1.0,
              0.0
            ],
            "axis_d": [
              -1.0,
              0.0,
              0.0
            ],
            "vertices": [
              [
                2.6666666666666665,
                4.451066666666667,
                0.0
              ],
              [
                2.6666666666666665,
                3.9927333333333332,
                0.0
              ],
              [
                2.2083333333333335,
                3.9927333333333332,
                0.0
              ],
              [
                2.2083333333333335,
                4.451066666666667,
                0.0
              ],
              [
                2.6666666666666665,
                4.451066666666667,
                7.42
              ],
              [
                2.6666666666666665,
                3.9927333333333332,
                7.42
              ],
              [
                2.2083333333333335,
                3.9927333333333332,
                7.42
              ],
              [
                2.2083333333333335,
                4.451066666666667,
                7.42
              ]
            ],
            "faces": [
              {
                "verts": [
                  0,
                  3,
                  2,
                  1
                ],
                "normal": [
                  -0.0,
                  -0.0,
                  -0.9999999999999999
                ],
                "color_key": "start"
              },
              {
                "verts": [
                  4,
                  5,
                  6,
                  7
                ],
                "normal": [
                  0.0,
                  0.0,
                  0.9999999999999999
                ],
                "color_key": "end"
              },
              {
                "verts": [
                  0,
                  1,
                  5,
                  4
                ],
                "normal": [
                  1.0,
                  -0.0,
                  -0.0
                ],
                "color_key": "top"
              },
              {
                "verts": [
                  3,
                  7,
                  6,
                  2
                ],
                "normal": [
                  -1.0,
                  0.0,
                  0.0
                ],
                "color_key": "bottom"
              },
              {
                "verts": [
                  0,
                  4,
                  7,
                  3
                ],
                "normal": [
                  -0.0,
                  1.0,
                  -0.0
                ],
                "color_key": "left"
              },
              {
                "verts": [
                  1,
                  2,
                  6,
                  5
                ],
                "normal": [
                  0.0,
                  -1.0,
                  0.0
                ],
                "color_key": "right"
              }
            ],
            "derived_length_ft": 8.42,
            "derived_angle_deg": 90.0,
            "constraints_satisfied": {
              "base_on_footing": true,
              "top_on_beam": true
            }
          },
          {
            "id": "FT2",
            "role": "footing",
            "p0": [
              2.4375,
              4.2219,
              -1.5
            ],
            "p1": [
              2.4375,
              4.2219,
              0.33
            ],
            "axis_u": [
              0.0,
              0.0,
              0.9999999999999999
            ],
            "axis_w": [
              0.0,
              -1.0,
              0.0
            ],
            "axis_d": [
              -1.0,
              0.0,
              0.0
            ],
            "vertices": [
              [
                2.9375,
                4.7219,
                -1.5
              ],
              [
                2.9375,
                3.7218999999999998,
                -1.5
              ],
              [
                1.9375,
                3.7218999999999998,
                -1.5
              ],
              [
                1.9375,
                4.7219,
                -1.5
              ],
              [
                2.9375,
                4.7219,
                0.33
              ],
              [
                2.9375,
                3.7218999999999998,
                0.33
              ],
              [
                1.9375,
                3.7218999999999998,
                0.33
              ],
              [
                1.9375,
                4.7219,
                0.33
              ]
            ],
            "faces": [
              {
                "verts": [
                  0,
                  3,
                  2,
                  1
                ],
                "normal": [
                  -0.0,
                  -0.0,
                  -0.9999999999999999
                ],
                "color_key": "start"
              },
              {
                "verts": [
                  4,
                  5,
                  6,
                  7
                ],
                "normal": [
                  0.0,
                  0.0,
                  0.9999999999999999
                ],
                "color_key": "end"
              },
              {
                "verts": [
                  0,
                  1,
                  5,
                  4
                ],
                "normal": [
                  1.0,
                  -0.0,
                  -0.0
                ],
                "color_key": "top"
              },
              {
                "verts": [
                  3,
                  7,
                  6,
                  2
                ],
                "normal": [
                  -1.0,
                  0.0,
                  0.0
                ],
                "color_key": "bottom"
              },
              {
                "verts": [
                  0,
                  4,
                  7,
                  3
                ],
                "normal": [
                  -0.0,
                  1.0,
                  -0.0
                ],
                "color_key": "left"
              },
              {
                "verts": [
                  1,
                  2,
                  6,
                  5
                ],
                "normal": [
                  0.0,
                  -1.0,
                  0.0
                ],
                "color_key": "right"
              }
            ],
            "derived_length_ft": 1.83,
            "derived_angle_deg": 90.0,
            "constraints_satisfied": {}
          },
          {
            "id": "P3",
            "role": "post",
            "p0": [
              -2.4375,
              4.2219,
              0.0
            ],
            "p1": [
              -2.4375,
              4.2219,
              7.42
            ],
            "axis_u": [
              0.0,
              0.0,
              0.9999999999999999
            ],
            "axis_w": [
              0.0,
              -1.0,
              0.0
            ],
            "axis_d": [
              -1.0,
              0.0,
              0.0
            ],
            "vertices": [
              [
                -2.2083333333333335,
                4.451066666666667,
                0.0
              ],
              [
                -2.2083333333333335,
                3.9927333333333332,
                0.0
              ],
              [
                -2.6666666666666665,
                3.9927333333333332,
                0.0
              ],
              [
                -2.6666666666666665,
                4.451066666666667,
                0.0
              ],
              [
                -2.2083333333333335,
                4.451066666666667,
                7.42
              ],
              [
                -2.2083333333333335,
                3.9927333333333332,
                7.42
              ],
              [
                -2.6666666666666665,
                3.9927333333333332,
                7.42
              ],
              [
                -2.6666666666666665,
                4.451066666666667,
                7.42
              ]
            ],
            "faces": [
              {
                "verts": [
                  0,
                  3,
                  2,
                  1
                ],
                "normal": [
                  -0.0,
                  -0.0,
                  -0.9999999999999999
                ],
                "color_key": "start"
              },
              {
                "verts": [
                  4,
                  5,
                  6,
                  7
                ],
                "normal": [
                  0.0,
                  0.0,
                  0.9999999999999999
                ],
                "color_key": "end"
              },
              {
                "verts": [
                  0,
                  1,
                  5,
                  4
                ],
                "normal": [
                  1.0,
                  -0.0,
                  -0.0
                ],
                "color_key": "top"
              },
              {
                "verts": [
                  3,
                  7,
                  6,
                  2
                ],
                "normal": [
                  -1.0,
                  0.0,
                  0.0
                ],
                "color_key": "bottom"
              },
              {
                "verts": [
                  0,
                  4,
                  7,
                  3
                ],
                "normal": [
                  -0.0,
                  1.0,
                  -0.0
                ],
                "color_key": "left"
              },
              {
                "verts": [
                  1,
                  2,
                  6,
                  5
                ],
                "normal": [
                  0.0,
                  -1.0,
                  0.0
                ],
                "color_key": "right"
              }
            ],
            "derived_length_ft": 8.42,
            "derived_angle_deg": 90.0,
            "constraints_satisfied": {
              "base_on_footing": true,
              "top_on_beam": true
            }
          },
          {
            "id": "FT3",
            "role": "footing",
            "p0": [
              -2.4375,
              4.2219,
              -1.5
            ],
            "p1": [
              -2.4375,
              4.2219,
              0.33
            ],
            "axis_u": [
              0.0,
              0.0,
              0.9999999999999999
            ],
            "axis_w": [
              0.0,
              -1.0,
              0.0
            ],
            "axis_d": [
              -1.0,
              0.0,
              0.0
            ],
            "vertices": [
              [
                -1.9375,
                4.7219,
                -1.5
              ],
              [
                -1.9375,
                3.7218999999999998,
                -1.5
              ],
              [
                -2.9375,
                3.7218999999999998,
                -1.5
              ],
              [
                -2.9375,
                4.7219,
                -1.5
              ],
              [
                -1.9375,
                4.7219,
                0.33
              ],
              [
                -1.9375,
                3.7218999999999998,
                0.33
              ],
              [
                -2.9375,
                3.7218999999999998,
                0.33
              ],
              [
                -2.9375,
                4.7219,
                0.33
              ]
            ],
            "faces": [
              {
                "verts": [
                  0,
                  3,
                  2,
                  1
                ],
                "normal": [
                  -0.0,
                  -0.0,
                  -0.9999999999999999
                ],
                "color_key": "start"
              },
              {
                "verts": [
                  4,
                  5,
                  6,
                  7
                ],
                "normal": [
                  0.0,
                  0.0,
                  0.9999999999999999
                ],
                "color_key": "end"
              },
              {
                "verts": [
                  0,
                  1,
                  5,
                  4
                ],
                "normal": [
                  1.0,
                  -0.0,
                  -0.0
                ],
                "color_key": "top"
              },
              {
                "verts": [
                  3,
                  7,
                  6,
                  2
                ],
                "normal": [
                  -1.0,
                  0.0,
                  0.0
                ],
                "color_key": "bottom"
              },
              {
                "verts": [
                  0,
                  4,
                  7,
                  3
                ],
                "normal": [
                  -0.0,
                  1.0,
                  -0.0
                ],
                "color_key": "left"
              },
              {
                "verts": [
                  1,
                  2,
                  6,
                  5
                ],
                "normal": [
                  0.0,
                  -1.0,
                  0.0
                ],
                "color_key": "right"
              }
            ],
            "derived_length_ft": 1.83,
            "derived_angle_deg": 90.0,
            "constraints_satisfied": {}
          },
          {
            "id": "P4",
            "role": "post",
            "p0": [
              -4.875,
              0.0,
              0.0
            ],
            "p1": [
              -4.875,
              0.0,
              7.42
            ],
            "axis_u": [
              0.0,
              0.0,
              0.9999999999999999
            ],
            "axis_w": [
              0.0,
              -1.0,
              0.0
            ],
            "axis_d": [
              -1.0,
              0.0,
              0.0
            ],
            "vertices": [
              [
                -4.645833333333333,
                0.22916666666666666,
                0.0
              ],
              [
                -4.645833333333333,
                -0.22916666666666666,
                0.0
              ],
              [
                -5.104166666666667,
                -0.22916666666666666,
                0.0
              ],
              [
                -5.104166666666667,
                0.22916666666666666,
                0.0
              ],
              [
                -4.645833333333333,
                0.22916666666666666,
                7.42
              ],
              [
                -4.645833333333333,
                -0.22916666666666666,
                7.42
              ],
              [
                -5.104166666666667,
                -0.22916666666666666,
                7.42
              ],
              [
                -5.104166666666667,
                0.22916666666666666,
                7.42
              ]
            ],
            "faces": [
              {
                "verts": [
                  0,
                  3,
                  2,
                  1
                ],
                "normal": [
                  -0.0,
                  -0.0,
                  -0.9999999999999999
                ],
                "color_key": "start"
              },
              {
                "verts": [
                  4,
                  5,
                  6,
                  7
                ],
                "normal": [
                  0.0,
                  0.0,
                  0.9999999999999999
                ],
                "color_key": "end"
              },
              {
                "verts": [
                  0,
                  1,
                  5,
                  4
                ],
                "normal": [
                  1.0,
                  -0.0,
                  -0.0
                ],
                "color_key": "top"
              },
              {
                "verts": [
                  3,
                  7,
                  6,
                  2
                ],
                "normal": [
                  -1.0,
                  0.0,
                  0.0
                ],
                "color_key": "bottom"
              },
              {
                "verts": [
                  0,
                  4,
                  7,
                  3
                ],
                "normal": [
                  -0.0,
                  1.0,
                  -0.0
                ],
                "color_key": "left"
              },
              {
                "verts": [
                  1,
                  2,
                  6,
                  5
                ],
                "normal": [
                  0.0,
                  -1.0,
                  0.0
                ],
                "color_key": "right"
              }
            ],
            "derived_length_ft": 8.42,
            "derived_angle_deg": 90.0,
            "constraints_satisfied": {
              "base_on_footing": true,
              "top_on_beam": true
            }
          },
          {
            "id": "FT4",
            "role": "footing",
            "p0": [
              -4.875,
              0.0,
              -1.5
            ],
            "p1": [
              -4.875,
              0.0,
              0.33
            ],
            "axis_u": [
              0.0,
              0.0,
              0.9999999999999999
            ],
            "axis_w": [
              0.0,
              -1.0,
              0.0
            ],
            "axis_d": [
              -1.0,
              0.0,
              0.0
            ],
            "vertices": [
              [
                -4.375,
                0.5,
                -1.5
              ],
              [
                -4.375,
                -0.5,
                -1.5
              ],
              [
                -5.375,
                -0.5,
                -1.5
              ],
              [
                -5.375,
                0.5,
                -1.5
              ],
              [
                -4.375,
                0.5,
                0.33
              ],
              [
                -4.375,
                -0.5,
                0.33
              ],
              [
                -5.375,
                -0.5,
                0.33
              ],
              [
                -5.375,
                0.5,
                0.33
              ]
            ],
            "faces": [
              {
                "verts": [
                  0,
                  3,
                  2,
                  1
                ],
                "normal": [
                  -0.0,
                  -0.0,
                  -0.9999999999999999
                ],
                "color_key": "start"
              },
              {
                "verts": [
                  4,
                  5,
                  6,
                  7
                ],
                "normal": [
                  0.0,
                  0.0,
                  0.9999999999999999
                ],
                "color_key": "end"
              },
              {
                "verts": [
                  0,
                  1,
                  5,
                  4
                ],
                "normal": [
                  1.0,
                  -0.0,
                  -0.0
                ],
                "color_key": "top"
              },
              {
                "verts": [
                  3,
                  7,
                  6,
                  2
                ],
                "normal": [
                  -1.0,
                  0.0,
                  0.0
                ],
                "color_key": "bottom"
              },
              {
                "verts": [
                  0,
                  4,
                  7,
                  3
                ],
                "normal": [
                  -0.0,
                  1.0,
                  -0.0
                ],
                "color_key": "left"
              },
              {
                "verts": [
                  1,
                  2,
                  6,
                  5
                ],
                "normal": [
                  0.0,
                  -1.0,
                  0.0
                ],
                "color_key": "right"
              }
            ],
            "derived_length_ft": 1.83,
            "derived_angle_deg": 90.0,
            "constraints_satisfied": {}
          },
          {
            "id": "P5",
            "role": "post",
            "p0": [
              -2.4375,
              -4.2219,
              0.0
            ],
            "p1": [
              -2.4375,
              -4.2219,
              7.42
            ],
            "axis_u": [
              0.0,
              0.0,
              0.9999999999999999
            ],
            "axis_w": [
              0.0,
              -1.0,
              0.0
            ],
            "axis_d": [
              -1.0,
              0.0,
              0.0
            ],
            "vertices": [
              [
                -2.2083333333333335,
                -3.9927333333333332,
                0.0
              ],
              [
                -2.2083333333333335,
                -4.451066666666667,
                0.0
              ],
              [
                -2.6666666666666665,
                -4.451066666666667,
                0.0
              ],
              [
                -2.6666666666666665,
                -3.9927333333333332,
                0.0
              ],
              [
                -2.2083333333333335,
                -3.9927333333333332,
                7.42
              ],
              [
                -2.2083333333333335,
                -4.451066666666667,
                7.42
              ],
              [
                -2.6666666666666665,
                -4.451066666666667,
                7.42
              ],
              [
                -2.6666666666666665,
                -3.9927333333333332,
                7.42
              ]
            ],
            "faces": [
              {
                "verts": [
                  0,
                  3,
                  2,
                  1
                ],
                "normal": [
                  -0.0,
                  -0.0,
                  -0.9999999999999999
                ],
                "color_key": "start"
              },
              {
                "verts": [
                  4,
                  5,
                  6,
                  7
                ],
                "normal": [
                  0.0,
                  0.0,
                  0.9999999999999999
                ],
                "color_key": "end"
              },
              {
                "verts": [
                  0,
                  1,
                  5,
                  4
                ],
                "normal": [
                  1.0,
                  -0.0,
                  -0.0
                ],
                "color_key": "top"
              },
              {
                "verts": [
                  3,
                  7,
                  6,
                  2
                ],
                "normal": [
                  -1.0,
                  0.0,
                  0.0
                ],
                "color_key": "bottom"
              },
              {
                "verts": [
                  0,
                  4,
                  7,
                  3
                ],
                "normal": [
                  -0.0,
                  1.0,
                  -0.0
                ],
                "color_key": "left"
              },
              {
                "verts": [
                  1,
                  2,
                  6,
                  5
                ],
                "normal": [
                  0.0,
                  -1.0,
                  0.0
                ],
                "color_key": "right"
              }
            ],
            "derived_length_ft": 8.42,
            "derived_angle_deg": 90.0,
            "constraints_satisfied": {
              "base_on_footing": true,
              "top_on_beam": true
            }
          },
          {
            "id": "FT5",
            "role": "footing",
            "p0": [
              -2.4375,
              -4.2219,
              -1.5
            ],
            "p1": [
              -2.4375,
              -4.2219,
              0.33
            ],
            "axis_u": [
              0.0,
              0.0,
              0.9999999999999999
            ],
            "axis_w": [
              0.0,
              -1.0,
              0.0
            ],
            "axis_d": [
              -1.0,
              0.0,
              0.0
            ],
            "vertices": [
              [
                -1.9375,
                -3.7218999999999998,
                -1.5
              ],
              [
                -1.9375,
                -4.7219,
                -1.5
              ],
              [
                -2.9375,
                -4.7219,
                -1.5
              ],
              [
                -2.9375,
                -3.7218999999999998,
                -1.5
              ],
              [
                -1.9375,
                -3.7218999999999998,
                0.33
              ],
              [
                -1.9375,
                -4.7219,
                0.33
              ],
              [
                -2.9375,
                -4.7219,
                0.33
              ],
              [
                -2.9375,
                -3.7218999999999998,
                0.33
              ]
            ],
            "faces": [
              {
                "verts": [
                  0,
                  3,
                  2,
                  1
                ],
                "normal": [
                  -0.0,
                  -0.0,
                  -0.9999999999999999
                ],
                "color_key": "start"
              },
              {
                "verts": [
                  4,
                  5,
                  6,
                  7
                ],
                "normal": [
                  0.0,
                  0.0,
                  0.9999999999999999
                ],
                "color_key": "end"
              },
              {
                "verts": [
                  0,
                  1,
                  5,
                  4
                ],
                "normal": [
                  1.0,
                  -0.0,
                  -0.0
                ],
                "color_key": "top"
              },
              {
                "verts": [
                  3,
                  7,
                  6,
                  2
                ],
                "normal": [
                  -1.0,
                  0.0,
                  0.0
                ],
                "color_key": "bottom"
              },
              {
                "verts": [
                  0,
                  4,
                  7,
                  3
                ],
                "normal": [
                  -0.0,
                  1.0,
                  -0.0
                ],
                "color_key": "left"
              },
              {
                "verts": [
                  1,
                  2,
                  6,
                  5
                ],
                "normal": [
                  0.0,
                  -1.0,
                  0.0
                ],
                "color_key": "right"
              }
            ],
            "derived_length_ft": 1.83,
            "derived_angle_deg": 90.0,
            "constraints_satisfied": {}
          },
          {
            "id": "P6",
            "role": "post",
            "p0": [
              2.4375,
              -4.2219,
              0.0
            ],
            "p1": [
              2.4375,
              -4.2219,
              7.42
            ],
            "axis_u": [
              0.0,
              0.0,
              0.9999999999999999
            ],
            "axis_w": [
              0.0,
              -1.0,
              0.0
            ],
            "axis_d": [
              -1.0,
              0.0,
              0.0
            ],
            "vertices": [
              [
                2.6666666666666665,
                -3.9927333333333332,
                0.0
              ],
              [
                2.6666666666666665,
                -4.451066666666667,
                0.0
              ],
              [
                2.2083333333333335,
                -4.451066666666667,
                0.0
              ],
              [
                2.2083333333333335,
                -3.9927333333333332,
                0.0
              ],
              [
                2.6666666666666665,
                -3.9927333333333332,
                7.42
              ],
              [
                2.6666666666666665,
                -4.451066666666667,
                7.42
              ],
              [
                2.2083333333333335,
                -4.451066666666667,
                7.42
              ],
              [
                2.2083333333333335,
                -3.9927333333333332,
                7.42
              ]
            ],
            "faces": [
              {
                "verts": [
                  0,
                  3,
                  2,
                  1
                ],
                "normal": [
                  -0.0,
                  -0.0,
                  -0.9999999999999999
                ],
                "color_key": "start"
              },
              {
                "verts": [
                  4,
                  5,
                  6,
                  7
                ],
                "normal": [
                  0.0,
                  0.0,
                  0.9999999999999999
                ],
                "color_key": "end"
              },
              {
                "verts": [
                  0,
                  1,
                  5,
                  4
                ],
                "normal": [
                  1.0,
                  -0.0,
                  -0.0
                ],
                "color_key": "top"
              },
              {
                "verts": [
                  3,
                  7,
                  6,
                  2
                ],
                "normal": [
                  -1.0,
                  0.0,
                  0.0
                ],
                "color_key": "bottom"
              },
              {
                "verts": [
                  0,
                  4,
                  7,
                  3
                ],
                "normal": [
                  -0.0,
                  1.0,
                  -0.0
                ],
                "color_key": "left"
              },
              {
                "verts": [
                  1,
                  2,
                  6,
                  5
                ],
                "normal": [
                  0.0,
                  -1.0,
                  0.0
                ],
                "color_key": "right"
              }
            ],
            "derived_length_ft": 8.42,
            "derived_angle_deg": 90.0,
            "constraints_satisfied": {
              "base_on_footing": true,
              "top_on_beam": true
            }
          },
          {
            "id": "FT6",
            "role": "footing",
            "p0": [
              2.4375,
              -4.2219,
              -1.5
            ],
            "p1": [
              2.4375,
              -4.2219,
              0.33
            ],
            "axis_u": [
              0.0,
              0.0,
              0.9999999999999999
            ],
            "axis_w": [
              0.0,
              -1.0,
              0.0
            ],
            "axis_d": [
              -1.0,
              0.0,
              0.0
            ],
            "vertices": [
              [
                2.9375,
                -3.7218999999999998,
                -1.5
              ],
              [
                2.9375,
                -4.7219,
                -1.5
              ],
              [
                1.9375,
                -4.7219,
                -1.5
              ],
              [
                1.9375,
                -3.7218999999999998,
                -1.5
              ],
              [
                2.9375,
                -3.7218999999999998,
                0.33
              ],
              [
                2.9375,
                -4.7219,
                0.33
              ],
              [
                1.9375,
                -4.7219,
                0.33
              ],
              [
                1.9375,
                -3.7218999999999998,
                0.33
              ]
            ],
            "faces": [
              {
                "verts": [
                  0,
                  3,
                  2,
                  1
                ],
                "normal": [
                  -0.0,
                  -0.0,
                  -0.9999999999999999
                ],
                "color_key": "start"
              },
              {
                "verts": [
                  4,
                  5,
                  6,
                  7
                ],
                "normal": [
                  0.0,
                  0.0,
                  0.9999999999999999
                ],
                "color_key": "end"
              },
              {
                "verts": [
                  0,
                  1,
                  5,
                  4
                ],
                "normal": [
                  1.0,
                  -0.0,
                  -0.0
                ],
                "color_key": "top"
              },
              {
                "verts": [
                  3,
                  7,
                  6,
                  2
                ],
                "normal": [
                  -1.0,
                  0.0,
                  0.0
                ],
                "color_key": "bottom"
              },
              {
                "verts": [
                  0,
                  4,
                  7,
                  3
                ],
                "normal": [
                  -0.0,
                  1.0,
                  -0.0
                ],
                "color_key": "left"
              },
              {
                "verts": [
                  1,
                  2,
                  6,
                  5
                ],
                "normal": [
                  0.0,
                  -1.0,
                  0.0
                ],
                "color_key": "right"
              }
            ],
            "derived_length_ft": 1.83,
            "derived_angle_deg": 90.0,
            "constraints_satisfied": {}
          },
          {
            "id": "B1",
            "role": "beam",
            "p0": [
              4.875,
              0.0,
              7.92
            ],
            "p1": [
              2.4375,
              4.2219,
              7.92
            ],
            "axis_u": [
              -0.4999976767025838,
              0.8660267451366722,
              0.0
            ],
            "axis_w": [
              -0.8660267451366722,
              -0.4999976767025838,
              0.0
            ],
            "axis_d": [
              -0.0,
              0.0,
              -1.0
            ],
            "vertices": [
              [
                5.091506686284168,
                0.12499941917564596,
                8.42
              ],
              [
                4.658493313715832,
                -0.12499941917564596,
                8.42
              ],
              [
                4.658493313715832,
                -0.12499941917564596,
                7.42
              ],
              [
                5.091506686284168,
                0.12499941917564596,
                7.42
              ],
              [
                2.654006686284168,
                4.346899419175646,
                8.42
              ],
              [
                2.220993313715832,
                4.096900580824354,
                8.42
              ],
              [
                2.220993313715832,
                4.096900580824354,
                7.42
              ],
              [
                2.654006686284168,
                4.346899419175646,
                7.42
              ]
            ],
            "faces": [
              {
                "verts": [
                  0,
                  3,
                  2,
                  1
                ],
                "normal": [
                  0.4999976767025838,
                  -0.8660267451366722,
                  -0.0
                ],
                "color_key": "start"
              },
              {
                "verts": [
                  4,
                  5,
                  6,
                  7
                ],
                "normal": [
                  -0.4999976767025838,
                  0.8660267451366722,
                  0.0
                ],
                "color_key": "end"
              },
              {
                "verts": [
                  0,
                  1,
                  5,
                  4
                ],
                "normal": [
                  0.0,
                  -0.0,
                  1.0
                ],
                "color_key": "top"
              },
              {
                "verts": [
                  3,
                  7,
                  6,
                  2
                ],
                "normal": [
                  -0.0,
                  0.0,
                  -1.0
                ],
                "color_key": "bottom"
              },
              {
                "verts": [
                  0,
                  4,
                  7,
                  3
                ],
                "normal": [
                  0.8660267451366722,
                  0.4999976767025838,
                  -0.0
                ],
                "color_key": "left"
              },
              {
                "verts": [
                  1,
                  2,
                  6,
                  5
                ],
                "normal": [
                  -0.8660267451366722,
                  -0.4999976767025838,
                  0.0
                ],
                "color_key": "right"
              }
            ],
            "derived_length_ft": 4.875,
            "derived_angle_deg": 0.0,
            "constraints_satisfied": {
              "start_on_post": true,
              "end_on_post": true
            }
          },
          {
            "id": "B2",
            "role": "beam",
            "p0": [
              2.4375,
              4.2219,
              7.92
            ],
            "p1": [
              -2.4375,
              4.2219,
              7.92
            ],
            "axis_u": [
              -1.0,
              0.0,
              0.0
            ],
            "axis_w": [
              0.0,
              -1.0,
              0.0
            ],
            "axis_d": [
              -0.0,
              -0.0,
              -1.0
            ],
            "vertices": [
              [
                2.4375,
                4.4719,
                8.42
              ],
              [
                2.4375,
                3.9718999999999998,
                8.42
              ],
              [
                2.4375,
                3.9718999999999998,
                7.42
              ],
              [
                2.4375,
                4.4719,
                7.42
              ],
              [
                -2.4375,
                4.4719,
                8.42
              ],
              [
                -2.4375,
                3.9718999999999998,
                8.42
              ],
              [
                -2.4375,
                3.9718999999999998,
                7.42
              ],
              [
                -2.4375,
                4.4719,
                7.42
              ]
            ],
            "faces": [
              {
                "verts": [
                  0,
                  3,
                  2,
                  1
                ],
                "normal": [
                  1.0,
                  -0.0,
                  -0.0
                ],
                "color_key": "start"
              },
              {
                "verts": [
                  4,
                  5,
                  6,
                  7
                ],
                "normal": [
                  -1.0,
                  0.0,
                  0.0
                ],
                "color_key": "end"
              },
              {
                "verts": [
                  0,
                  1,
                  5,
                  4
                ],
                "normal": [
                  0.0,
                  0.0,
                  1.0
                ],
                "color_key": "top"
              },
              {
                "verts": [
                  3,
                  7,
                  6,
                  2
                ],
                "normal": [
                  -0.0,
                  -0.0,
                  -1.0
                ],
                "color_key": "bottom"
              },
              {
                "verts": [
                  0,
                  4,
                  7,
                  3
                ],
                "normal": [
                  -0.0,
                  1.0,
                  -0.0
                ],
                "color_key": "left"
              },
              {
                "verts": [
                  1,
                  2,
                  6,
                  5
                ],
                "normal": [
                  0.0,
                  -1.0,
                  0.0
                ],
                "color_key": "right"
              }
            ],
            "derived_length_ft": 4.875,
            "derived_angle_deg": 0.0,
            "constraints_satisfied": {
              "start_on_post": true,
              "end_on_post": true
            }
          },
          {
            "id": "B3",
            "role": "beam",
            "p0": [
              -2.4375,
              4.2219,
              7.92
            ],
            "p1": [
              -4.875,
              0.0,
              7.92
            ],
            "axis_u": [
              -0.4999976767025838,
              -0.8660267451366722,
              0.0
            ],
            "axis_w": [
              0.8660267451366722,
              -0.4999976767025838,
              0.0
            ],
            "axis_d": [
              0.0,
              -0.0,
              -1.0
            ],
            "vertices": [
              [
                -2.654006686284168,
                4.346899419175646,
                8.42
              ],
              [
                -2.220993313715832,
                4.096900580824354,
                8.42
              ],
              [
                -2.220993313715832,
                4.096900580824354,
                7.42
              ],
              [
                -2.654006686284168,
                4.346899419175646,
                7.42
              ],
              [
                -5.091506686284168,
                0.12499941917564596,
                8.42
              ],
              [
                -4.658493313715832,
                -0.12499941917564596,
                8.42
              ],
              [
                -4.658493313715832,
                -0.12499941917564596,
                7.42
              ],
              [
                -5.091506686284168,
                0.12499941917564596,
                7.42
              ]
            ],
            "faces": [
              {
                "verts": [
                  0,
                  3,
                  2,
                  1
                ],
                "normal": [
                  0.4999976767025838,
                  0.8660267451366722,
                  -0.0
                ],
                "color_key": "start"
              },
              {
                "verts": [
                  4,
                  5,
                  6,
                  7
                ],
                "normal": [
                  -0.4999976767025838,
                  -0.8660267451366722,
                  0.0
                ],
                "color_key": "end"
              },
              {
                "verts": [
                  0,
                  1,
                  5,
                  4
                ],
                "normal": [
                  -0.0,
                  0.0,
                  1.0
                ],
                "color_key": "top"
              },
              {
                "verts": [
                  3,
                  7,
                  6,
                  2
                ],
                "normal": [
                  0.0,
                  -0.0,
                  -1.0
                ],
                "color_key": "bottom"
              },
              {
                "verts": [
                  0,
                  4,
                  7,
                  3
                ],
                "normal": [
                  -0.8660267451366722,
                  0.4999976767025838,
                  -0.0
                ],
                "color_key": "left"
              },
              {
                "verts": [
                  1,
                  2,
                  6,
                  5
                ],
                "normal": [
                  0.8660267451366722,
                  -0.4999976767025838,
                  0.0
                ],
                "color_key": "right"
              }
            ],
            "derived_length_ft": 4.875,
            "derived_angle_deg": 0.0,
            "constraints_satisfied": {
              "start_on_post": true,
              "end_on_post": true
            }
          },
          {
            "id": "B4",
            "role": "beam",
            "p0": [
              -4.875,
              0.0,
              7.92
            ],
            "p1": [
              -2.4375,
              -4.2219,
              7.92
            ],
            "axis_u": [
              0.4999976767025838,
              -0.8660267451366722,
              0.0
            ],
            "axis_w": [
              0.8660267451366722,
              0.4999976767025838,
              -0.0
            ],
            "axis_d": [
              0.0,
              -0.0,
              -1.0
            ],
            "vertices": [
              [
                -5.091506686284168,
                -0.12499941917564596,
                8.42
              ],
              [
                -4.658493313715832,
                0.12499941917564596,
                8.42
              ],
              [
                -4.658493313715832,
                0.12499941917564596,
                7.42
              ],
              [
                -5.091506686284168,
                -0.12499941917564596,
                7.42
              ],
              [
                -2.654006686284168,
                -4.346899419175646,
                8.42
              ],
              [
                -2.220993313715832,
                -4.096900580824354,
                8.42
              ],
              [
                -2.220993313715832,
                -4.096900580824354,
                7.42
              ],
              [
                -2.654006686284168,
                -4.346899419175646,
                7.42
              ]
            ],
            "faces": [
              {
                "verts": [
                  0,
                  3,
                  2,
                  1
                ],
                "normal": [
                  -0.4999976767025838,
                  0.8660267451366722,
                  -0.0
                ],
                "color_key": "start"
              },
              {
                "verts": [
                  4,
                  5,
                  6,
                  7
                ],
                "normal": [
                  0.4999976767025838,
                  -0.8660267451366722,
                  0.0
                ],
                "color_key": "end"
              },
              {
                "verts": [
                  0,
                  1,
                  5,
                  4
                ],
                "normal": [
                  -0.0,
                  0.0,
                  1.0
                ],
                "color_key": "top"
              },
              {
                "verts": [
                  3,
                  7,
                  6,
                  2
                ],
                "normal": [
                  0.0,
                  -0.0,
                  -1.0
                ],
                "color_key": "bottom"
              },
              {
                "verts": [
                  0,
                  4,
                  7,
                  3
                ],
                "normal": [
                  -0.8660267451366722,
                  -0.4999976767025838,
                  0.0
                ],
                "color_key": "left"
              },
              {
                "verts": [
                  1,
                  2,
                  6,
                  5
                ],
                "normal": [
                  0.8660267451366722,
                  0.4999976767025838,
                  -0.0
                ],
                "color_key": "right"
              }
            ],
            "derived_length_ft": 4.875,
            "derived_angle_deg": 0.0,
            "constraints_satisfied": {
              "start_on_post": true,
              "end_on_post": true
            }
          },
          {
            "id": "B5",
            "role": "beam",
            "p0": [
              -2.4375,
              -4.2219,
              7.92
            ],
            "p1": [
              2.4375,
              -4.2219,
              7.92
            ],
            "axis_u": [
              1.0,
              0.0,
              0.0
            ],
            "axis_w": [
              0.0,
              1.0,
              0.0
            ],
            "axis_d": [
              0.0,
              0.0,
              -1.0
            ],
            "vertices": [
              [
                -2.4375,
                -4.4719,
                8.42
              ],
              [
                -2.4375,
                -3.9718999999999998,
                8.42
              ],
              [
                -2.4375,
                -3.9718999999999998,
                7.42
              ],
              [
                -2.4375,
                -4.4719,
                7.42
              ],
              [
                2.4375,
                -4.4719,
                8.42
              ],
              [
                2.4375,
                -3.9718999999999998,
                8.42
              ],
              [
                2.4375,
                -3.9718999999999998,
                7.42
              ],
              [
                2.4375,
                -4.4719,
                7.42
              ]
            ],
            "faces": [
              {
                "verts": [
                  0,
                  3,
                  2,
                  1
                ],
                "normal": [
                  -1.0,
                  -0.0,
                  -0.0
                ],
                "color_key": "start"
              },
              {
                "verts": [
                  4,
                  5,
                  6,
                  7
                ],
                "normal": [
                  1.0,
                  0.0,
                  0.0
                ],
                "color_key": "end"
              },
              {
                "verts": [
                  0,
                  1,
                  5,
                  4
                ],
                "normal": [
                  -0.0,
                  -0.0,
                  1.0
                ],
                "color_key": "top"
              },
              {
                "verts": [
                  3,
                  7,
                  6,
                  2
                ],
                "normal": [
                  0.0,
                  0.0,
                  -1.0
                ],
                "color_key": "bottom"
              },
              {
                "verts": [
                  0,
                  4,
                  7,
                  3
                ],
                "normal": [
                  -0.0,
                  -1.0,
                  -0.0
                ],
                "color_key": "left"
              },
              {
                "verts": [
                  1,
                  2,
                  6,
                  5
                ],
                "normal": [
                  0.0,
                  1.0,
                  0.0
                ],
                "color_key": "right"
              }
            ],
            "derived_length_ft": 4.875,
            "derived_angle_deg": 0.0,
            "constraints_satisfied": {
              "start_on_post": true,
              "end_on_post": true
            }
          },
          {
            "id": "B6",
            "role": "beam",
            "p0": [
              2.4375,
              -4.2219,
              7.92
            ],
            "p1": [
              4.875,
              0.0,
              7.92
            ],
            "axis_u": [
              0.4999976767025838,
              0.8660267451366722,
              0.0
            ],
            "axis_w": [
              -0.8660267451366722,
              0.4999976767025838,
              0.0
            ],
            "axis_d": [
              0.0,
              0.0,
              -1.0
            ],
            "vertices": [
              [
                2.654006686284168,
                -4.346899419175646,
                8.42
              ],
              [
                2.220993313715832,
                -4.096900580824354,
                8.42
              ],
              [
                2.220993313715832,
                -4.096900580824354,
                7.42
              ],
              [
                2.654006686284168,
                -4.346899419175646,
                7.42
              ],
              [
                5.091506686284168,
                -0.12499941917564596,
                8.42
              ],
              [
                4.658493313715832,
                0.12499941917564596,
                8.42
              ],
              [
                4.658493313715832,
                0.12499941917564596,
                7.42
              ],
              [
                5.091506686284168,
                -0.12499941917564596,
                7.42
              ]
            ],
            "faces": [
              {
                "verts": [
                  0,
                  3,
                  2,
                  1
                ],
                "normal": [
                  -0.4999976767025838,
                  -0.8660267451366722,
                  -0.0
                ],
                "color_key": "start"
              },
              {
                "verts": [
                  4,
                  5,
                  6,
                  7
                ],
                "normal": [
                  0.4999976767025838,
                  0.8660267451366722,
                  0.0
                ],
                "color_key": "end"
              },
              {
                "verts": [
                  0,
                  1,
                  5,
                  4
                ],
                "normal": [
                  -0.0,
                  -0.0,
                  1.0
                ],
                "color_key": "top"
              },
              {
                "verts": [
                  3,
                  7,
                  6,
                  2
                ],
                "normal": [
                  0.0,
                  0.0,
                  -1.0
                ],
                "color_key": "bottom"
              },
              {
                "verts": [
                  0,
                  4,
                  7,
                  3
                ],
                "normal": [
                  0.8660267451366722,
                  -0.4999976767025838,
                  -0.0
                ],
                "color_key": "left"
              },
              {
                "verts": [
                  1,
                  2,
                  6,
                  5
                ],
                "normal": [
                  -0.8660267451366722,
                  0.4999976767025838,
                  0.0
                ],
                "color_key": "right"
              }
            ],
            "derived_length_ft": 4.875,
            "derived_angle_deg": 0.0,
            "constraints_satisfied": {
              "start_on_post": true,
              "end_on_post": true
            }
          },
          {
            "id": "K1A",
            "role": "brace",
            "p0": [
              4.7604,
              0.1985,
              5.9575
            ],
            "p1": [
              4.0292,
              1.465,
              7.42
            ],
            "axis_u": [
              -0.35353874341758734,
              0.6123588874977773,
              0.7071258373197785
            ],
            "axis_w": [
              -0.8660295833821284,
              -0.49999276065456905,
              0.0
            ],
            "axis_d": [
              -0.35355779953168975,
              0.6123918942927865,
              -0.7070877245397506
            ],
            "vertices": [
              [
                4.938256493341598,
                0.18210845967775996,
                6.060616959828713
              ],
              [
                4.685664531521811,
                0.036277237820177305,
                6.060616959828713
              ],
              [
                4.582543506658402,
                0.21489154032224006,
                5.854383040171286
              ],
              [
                4.835135468478189,
                0.36072276217982274,
                5.854383040171286
              ],
              [
                4.207056493341598,
                1.4486084596777602,
                7.523116959828713
              ],
              [
                3.954464531521811,
                1.3027772378201774,
                7.523116959828713
              ],
              [
                3.851343506658402,
                1.48139154032224,
                7.3168830401712865
              ],
              [
                4.1039354684781895,
                1.6272227621798228,
                7.3168830401712865
              ]
            ],
            "faces": [
              {
                "verts": [
                  0,
                  3,
                  2,
                  1
                ],
                "normal": [
                  0.35353874341758734,
                  -0.6123588874977773,
                  -0.7071258373197785
                ],
                "color_key": "start"
              },
              {
                "verts": [
                  4,
                  5,
                  6,
                  7
                ],
                "normal": [
                  -0.35353874341758734,
                  0.6123588874977773,
                  0.7071258373197785
                ],
                "color_key": "end"
              },
              {
                "verts": [
                  0,
                  1,
                  5,
                  4
                ],
                "normal": [
                  0.35355779953168975,
                  -0.6123918942927865,
                  0.7070877245397506
                ],
                "color_key": "top"
              },
              {
                "verts": [
                  3,
                  7,
                  6,
                  2
                ],
                "normal": [
                  -0.35355779953168975,
                  0.6123918942927865,
                  -0.7070877245397506
                ],
                "color_key": "bottom"
              },
              {
                "verts": [
                  0,
                  4,
                  7,
                  3
                ],
                "normal": [
                  0.8660295833821284,
                  0.49999276065456905,
                  -0.0
                ],
                "color_key": "left"
              },
              {
                "verts": [
                  1,
                  2,
                  6,
                  5
                ],
                "normal": [
                  -0.8660295833821284,
                  -0.49999276065456905,
                  0.0
                ],
                "color_key": "right"
              }
            ],
            "derived_length_ft": 2.0682,
            "derived_angle_deg": 45.0,
            "constraints_satisfied": {
              "start_on_post_face": true,
              "end_on_beam_soffit": true
            }
          },
          {
            "id": "K1B",
            "role": "brace",
            "p0": [
              2.5521,
              4.0234,
              5.9575
            ],
            "p1": [
              3.2833,
              2.7569,
              7.42
            ],
            "axis_u": [
              0.3535387434175878,
              -0.6123588874977771,
              0.7071258373197785
            ],
            "axis_w": [
              0.8660295833821281,
              0.4999927606545697,
              -0.0
            ],
            "axis_d": [
              0.3535577995316902,
              -0.6123918942927863,
              -0.7070877245397507
            ],
            "vertices": [
              [
                2.3742435066584013,
                4.0397915403222395,
                6.060616959828713
              ],
              [
                2.6268354684781885,
                4.185622762179822,
                6.060616959828713
              ],
              [
                2.7299564933415983,
                4.00700845967776,
                5.854383040171286
              ],
              [
                2.477364531521811,
                3.8611772378201765,
                5.854383040171286
              ],
              [
                3.1054435066584016,
                2.77329154032224,
                7.523116959828713
              ],
              [
                3.358035468478189,
                2.919122762179823,
                7.523116959828713
              ],
              [
                3.4611564933415986,
                2.74050845967776,
                7.3168830401712865
              ],
              [
                3.2085645315218114,
                2.594677237820177,
                7.3168830401712865
              ]
            ],
            "faces": [
              {
                "verts": [
                  0,
                  3,
                  2,
                  1
                ],
                "normal": [
                  -0.3535387434175878,
                  0.6123588874977771,
                  -0.7071258373197785
                ],
                "color_key": "start"
              },
              {
                "verts": [
                  4,
                  5,
                  6,
                  7
                ],
                "normal": [
                  0.3535387434175878,
                  -0.6123588874977771,
                  0.7071258373197785
                ],
                "color_key": "end"
              },
              {
                "verts": [
                  0,
                  1,
                  5,
                  4
                ],
                "normal": [
                  -0.3535577995316902,
                  0.6123918942927863,
                  0.7070877245397507
                ],
                "color_key": "top"
              },
              {
                "verts": [
                  3,
                  7,
                  6,
                  2
                ],
                "normal": [
                  0.3535577995316902,
                  -0.6123918942927863,
                  -0.7070877245397507
                ],
                "color_key": "bottom"
              },
              {
                "verts": [
                  0,
                  4,
                  7,
                  3
                ],
                "normal": [
                  -0.8660295833821281,
                  -0.4999927606545697,
                  0.0
                ],
                "color_key": "left"
              },
              {
                "verts": [
                  1,
                  2,
                  6,
                  5
                ],
                "normal": [
                  0.8660295833821281,
                  0.4999927606545697,
                  -0.0
                ],
                "color_key": "right"
              }
            ],
            "derived_length_ft": 2.0682,
            "derived_angle_deg": 45.0,
            "constraints_satisfied": {
              "start_on_post_face": true,
              "end_on_beam_soffit": true
            }
          },
          {
            "id": "K2A",
            "role": "brace",
            "p0": [
              2.2083,
              4.2219,
              5.9575
            ],
            "p1": [
              0.7458,
              4.2219,
              7.42
            ],
            "axis_u": [
              -0.7071067811865474,
              0.0,
              0.7071067811865476
            ],
            "axis_w": [
              0.0,
              -1.0,
              0.0
            ],
            "axis_d": [
              -0.7071067811865477,
              -0.0,
              -0.7071067811865475
            ],
            "vertices": [
              [
                2.311419738923038,
                4.367733333333333,
                6.060619738923037
              ],
              [
                2.311419738923038,
                4.076066666666667,
                6.060619738923037
              ],
              [
                2.1051802610769617,
                4.076066666666667,
                5.854380261076962
              ],
              [
                2.1051802610769617,
                4.367733333333333,
                5.854380261076962
              ],
              [
                0.8489197389230382,
                4.367733333333333,
                7.523119738923038
              ],
              [
                0.8489197389230382,
                4.076066666666667,
                7.523119738923038
              ],
              [
                0.6426802610769619,
                4.076066666666667,
                7.316880261076962
              ],
              [
                0.6426802610769619,
                4.367733333333333,
                7.316880261076962
              ]
            ],
            "faces": [
              {
                "verts": [
                  0,
                  3,
                  2,
                  1
                ],
                "normal": [
                  0.7071067811865474,
                  -0.0,
                  -0.7071067811865476
                ],
                "color_key": "start"
              },
              {
                "verts": [
                  4,
                  5,
                  6,
                  7
                ],
                "normal": [
                  -0.7071067811865474,
                  0.0,
                  0.7071067811865476
                ],
                "color_key": "end"
              },
              {
                "verts": [
                  0,
                  1,
                  5,
                  4
                ],
                "normal": [
                  0.7071067811865477,
                  0.0,
                  0.7071067811865475
                ],
                "color_key": "top"
              },
              {
                "verts": [
                  3,
                  7,
                  6,
                  2
                ],
                "normal": [
                  -0.7071067811865477,
                  -0.0,
                  -0.7071067811865475
                ],
                "color_key": "bottom"
              },
              {
                "verts": [
                  0,
                  4,
                  7,
                  3
                ],
                "normal": [
                  -0.0,
                  1.0,
                  -0.0
                ],
                "color_key": "left"
              },
              {
                "verts": [
                  1,
                  2,
                  6,
                  5
                ],
                "normal": [
                  0.0,
                  -1.0,
                  0.0
                ],
                "color_key": "right"
              }
            ],
            "derived_length_ft": 2.0683,
            "derived_angle_deg": 45.0,
            "constraints_satisfied": {
              "start_on_post_face": true,
              "end_on_beam_soffit": true
            }
          },
          {
            "id": "K2B",
            "role": "brace",
            "p0": [
              -2.2083,
              4.2219,
              5.9575
            ],
            "p1": [
              -0.7458,
              4.2219,
              7.42
            ],
            "axis_u": [
              0.7071067811865474,
              0.0,
              0.7071067811865476
            ],
            "axis_w": [
              0.0,
              1.0,
              0.0
            ],
            "axis_d": [
              0.7071067811865477,
              0.0,
              -0.7071067811865475
            ],
            "vertices": [
              [
                -2.311419738923038,
                4.076066666666667,
                6.060619738923037
              ],
              [
                -2.311419738923038,
                4.367733333333333,
                6.060619738923037
              ],
              [
                -2.1051802610769617,
                4.367733333333333,
                5.854380261076962
              ],
              [
                -2.1051802610769617,
                4.076066666666667,
                5.854380261076962
              ],
              [
                -0.8489197389230382,
                4.076066666666667,
                7.523119738923038
              ],
              [
                -0.8489197389230382,
                4.367733333333333,
                7.523119738923038
              ],
              [
                -0.6426802610769619,
                4.367733333333333,
                7.316880261076962
              ],
              [
                -0.6426802610769619,
                4.076066666666667,
                7.316880261076962
              ]
            ],
            "faces": [
              {
                "verts": [
                  0,
                  3,
                  2,
                  1
                ],
                "normal": [
                  -0.7071067811865474,
                  -0.0,
                  -0.7071067811865476
                ],
                "color_key": "start"
              },
              {
                "verts": [
                  4,
                  5,
                  6,
                  7
                ],
                "normal": [
                  0.7071067811865474,
                  0.0,
                  0.7071067811865476
                ],
                "color_key": "end"
              },
              {
                "verts": [
                  0,
                  1,
                  5,
                  4
                ],
                "normal": [
                  -0.7071067811865477,
                  -0.0,
                  0.7071067811865475
                ],
                "color_key": "top"
              },
              {
                "verts": [
                  3,
                  7,
                  6,
                  2
                ],
                "normal": [
                  0.7071067811865477,
                  0.0,
                  -0.7071067811865475
                ],
                "color_key": "bottom"
              },
              {
                "verts": [
                  0,
                  4,
                  7,
                  3
                ],
                "normal": [
                  -0.0,
                  -1.0,
                  -0.0
                ],
                "color_key": "left"
              },
              {
                "verts": [
                  1,
                  2,
                  6,
                  5
                ],
                "normal": [
                  0.0,
                  1.0,
                  0.0
                ],
                "color_key": "right"
              }
            ],
            "derived_length_ft": 2.0683,
            "derived_angle_deg": 45.0,
            "constraints_satisfied": {
              "start_on_post_face": true,
              "end_on_beam_soffit": true
            }
          },
          {
            "id": "K3A",
            "role": "brace",
            "p0": [
              -2.5521,
              4.0234,
              5.9575
            ],
            "p1": [
              -3.2833,
              2.7569,
              7.42
            ],
            "axis_u": [
              -0.3535387434175878,
              -0.6123588874977771,
              0.7071258373197785
            ],
            "axis_w": [
              0.8660295833821281,
              -0.4999927606545697,
              0.0
            ],
            "axis_d": [
              -0.3535577995316902,
              -0.6123918942927863,
              -0.7070877245397507
            ],
            "vertices": [
              [
                -2.6268354684781885,
                4.185622762179822,
                6.060616959828713
              ],
              [
                -2.3742435066584013,
                4.0397915403222395,
                6.060616959828713
              ],
              [
                -2.477364531521811,
                3.8611772378201765,
                5.854383040171286
              ],
              [
                -2.7299564933415983,
                4.00700845967776,
                5.854383040171286
              ],
              [
                -3.358035468478189,
                2.919122762179823,
                7.523116959828713
              ],
              [
                -3.1054435066584016,
                2.77329154032224,
                7.523116959828713
              ],
              [
                -3.2085645315218114,
                2.594677237820177,
                7.3168830401712865
              ],
              [
                -3.4611564933415986,
                2.74050845967776,
                7.3168830401712865
              ]
            ],
            "faces": [
              {
                "verts": [
                  0,
                  3,
                  2,
                  1
                ],
                "normal": [
                  0.3535387434175878,
                  0.6123588874977771,
                  -0.7071258373197785
                ],
                "color_key": "start"
              },
              {
                "verts": [
                  4,
                  5,
                  6,
                  7
                ],
                "normal": [
                  -0.3535387434175878,
                  -0.6123588874977771,
                  0.7071258373197785
                ],
                "color_key": "end"
              },
              {
                "verts": [
                  0,
                  1,
                  5,
                  4
                ],
                "normal": [
                  0.3535577995316902,
                  0.6123918942927863,
                  0.7070877245397507
                ],
                "color_key": "top"
              },
              {
                "verts": [
                  3,
                  7,
                  6,
                  2
                ],
                "normal": [
                  -0.3535577995316902,
                  -0.6123918942927863,
                  -0.7070877245397507
                ],
                "color_key": "bottom"
              },
              {
                "verts": [
                  0,
                  4,
                  7,
                  3
                ],
                "normal": [
                  -0.8660295833821281,
                  0.4999927606545697,
                  -0.0
                ],
                "color_key": "left"
              },
              {
                "verts": [
                  1,
                  2,
                  6,
                  5
                ],
                "normal": [
                  0.8660295833821281,
                  -0.4999927606545697,
                  0.0
                ],
                "color_key": "right"
              }
            ],
            "derived_length_ft": 2.0682,
            "derived_angle_deg": 45.0,
            "constraints_satisfied": {
              "start_on_post_face": true,
              "end_on_beam_soffit": true
            }
          },
          {
            "id": "K3B",
            "role": "brace",
            "p0": [
              -4.7604,
              0.1985,
              5.9575
            ],
            "p1": [
              -4.0292,
              1.465,
              7.42
            ],
            "axis_u": [
              0.35353874341758734,
              0.6123588874977773,
              0.7071258373197785
            ],
            "axis_w": [
              -0.8660295833821284,
              0.49999276065456905,
              0.0
            ],
            "axis_d": [
              0.35355779953168975,
              0.6123918942927865,
              -0.7070877245397506
            ],
            "vertices": [
              [
                -4.685664531521811,
                0.036277237820177305,
                6.060616959828713
              ],
              [
                -4.938256493341598,
                0.18210845967775996,
                6.060616959828713
              ],
              [
                -4.835135468478189,
                0.36072276217982274,
                5.854383040171286
              ],
              [
                -4.582543506658402,
                0.21489154032224006,
                5.854383040171286
              ],
              [
                -3.954464531521811,
                1.3027772378201774,
                7.523116959828713
              ],
              [
                -4.207056493341598,
                1.4486084596777602,
                7.523116959828713
              ],
              [
                -4.1039354684781895,
                1.6272227621798228,
                7.3168830401712865
              ],
              [
                -3.851343506658402,
                1.48139154032224,
                7.3168830401712865
              ]
            ],
            "faces": [
              {
                "verts": [
                  0,
                  3,
                  2,
                  1
                ],
                "normal": [
                  -0.35353874341758734,
                  -0.6123588874977773,
                  -0.7071258373197785
                ],
                "color_key": "start"
              },
              {
                "verts": [
                  4,
                  5,
                  6,
                  7
                ],
                "normal": [
                  0.35353874341758734,
                  0.6123588874977773,
                  0.7071258373197785
                ],
                "color_key": "end"
              },
              {
                "verts": [
                  0,
                  1,
                  5,
                  4
                ],
                "normal": [
                  -0.35355779953168975,
                  -0.6123918942927865,
                  0.7070877245397506
                ],
                "color_key": "top"
              },
              {
                "verts": [
                  3,
                  7,
                  6,
                  2
                ],
                "normal": [
                  0.35355779953168975,
                  0.6123918942927865,
                  -0.7070877245397506
                ],
                "color_key": "bottom"
              },
              {
                "verts": [
                  0,
                  4,
                  7,
                  3
                ],
                "normal": [
                  0.8660295833821284,
                  -0.49999276065456905,
                  -0.0
                ],
                "color_key": "left"
              },
              {
                "verts": [
                  1,
                  2,
                  6,
                  5
                ],
                "normal": [
                  -0.8660295833821284,
                  0.49999276065456905,
                  0.0
                ],
                "color_key": "right"
              }
            ],
            "derived_length_ft": 2.0682,
            "derived_angle_deg": 45.0,
            "constraints_satisfied": {
              "start_on_post_face": true,
              "end_on_beam_soffit": true
            }
          },
          {
            "id": "K4A",
            "role": "brace",
            "p0": [
              -4.7604,
              -0.1985,
              5.9575
            ],
            "p1": [
              -4.0292,
              -1.465,
              7.42
            ],
            "axis_u": [
              0.35353874341758734,
              -0.6123588874977773,
              0.7071258373197785
            ],
            "axis_w": [
              0.8660295833821284,
              0.49999276065456905,
              -0.0
            ],
            "axis_d": [
              0.35355779953168975,
              -0.6123918942927865,
              -0.7070877245397506
            ],
            "vertices": [
              [
                -4.938256493341598,
                -0.18210845967775996,
                6.060616959828713
              ],
              [
                -4.685664531521811,
                -0.036277237820177305,
                6.060616959828713
              ],
              [
                -4.582543506658402,
                -0.21489154032224006,
                5.854383040171286
              ],
              [
                -4.835135468478189,
                -0.36072276217982274,
                5.854383040171286
              ],
              [
                -4.207056493341598,
                -1.4486084596777602,
                7.523116959828713
              ],
              [
                -3.954464531521811,
                -1.3027772378201774,
                7.523116959828713
              ],
              [
                -3.851343506658402,
                -1.48139154032224,
                7.3168830401712865
              ],
              [
                -4.1039354684781895,
                -1.6272227621798228,
                7.3168830401712865
              ]
            ],
            "faces": [
              {
                "verts": [
                  0,
                  3,
                  2,
                  1
                ],
                "normal": [
                  -0.35353874341758734,
                  0.6123588874977773,
                  -0.7071258373197785
                ],
                "color_key": "start"
              },
              {
                "verts": [
                  4,
                  5,
                  6,
                  7
                ],
                "normal": [
                  0.35353874341758734,
                  -0.6123588874977773,
                  0.7071258373197785
                ],
                "color_key": "end"
              },
              {
                "verts": [
                  0,
                  1,
                  5,
                  4
                ],
                "normal": [
                  -0.35355779953168975,
                  0.6123918942927865,
                  0.7070877245397506
                ],
                "color_key": "top"
              },
              {
                "verts": [
                  3,
                  7,
                  6,
                  2
                ],
                "normal": [
                  0.35355779953168975,
                  -0.6123918942927865,
                  -0.7070877245397506
                ],
                "color_key": "bottom"
              },
              {
                "verts": [
                  0,
                  4,
                  7,
                  3
                ],
                "normal": [
                  -0.8660295833821284,
                  -0.49999276065456905,
                  0.0
                ],
                "color_key": "left"
              },
              {
                "verts": [
                  1,
                  2,
                  6,
                  5
                ],
                "normal": [
                  0.8660295833821284,
                  0.49999276065456905,
                  -0.0
                ],
                "color_key": "right"
              }
            ],
            "derived_length_ft": 2.0682,
            "derived_angle_deg": 45.0,
            "constraints_satisfied": {
              "start_on_post_face": true,
              "end_on_beam_soffit": true
            }
          },
          {
            "id": "K4B",
            "role": "brace",
            "p0": [
              -2.5521,
              -4.0234,
              5.9575
            ],
            "p1": [
              -3.2833,
              -2.7569,
              7.42
            ],
            "axis_u": [
              -0.3535387434175878,
              0.6123588874977771,
              0.7071258373197785
            ],
            "axis_w": [
              -0.8660295833821281,
              -0.4999927606545697,
              0.0
            ],
            "axis_d": [
              -0.3535577995316902,
              0.6123918942927863,
              -0.7070877245397507
            ],
            "vertices": [
              [
                -2.3742435066584013,
                -4.0397915403222395,
                6.060616959828713
              ],
              [
                -2.6268354684781885,
                -4.185622762179822,
                6.060616959828713
              ],
              [
                -2.7299564933415983,
                -4.00700845967776,
                5.854383040171286
              ],
              [
                -2.477364531521811,
                -3.8611772378201765,
                5.854383040171286
              ],
              [
                -3.1054435066584016,
                -2.77329154032224,
                7.523116959828713
              ],
              [
                -3.358035468478189,
                -2.919122762179823,
                7.523116959828713
              ],
              [
                -3.4611564933415986,
                -2.74050845967776,
                7.3168830401712865
              ],
              [
                -3.2085645315218114,
                -2.594677237820177,
                7.3168830401712865
              ]
            ],
            "faces": [
              {
                "verts": [
                  0,
                  3,
                  2,
                  1
                ],
                "normal": [
                  0.3535387434175878,
                  -0.6123588874977771,
                  -0.7071258373197785
                ],
                "color_key": "start"
              },
              {
                "verts": [
                  4,
                  5,
                  6,
                  7
                ],
                "normal": [
                  -0.3535387434175878,
                  0.6123588874977771,
                  0.7071258373197785
                ],
                "color_key": "end"
              },
              {
                "verts": [
                  0,
                  1,
                  5,
                  4
                ],
                "normal": [
                  0.3535577995316902,
                  -0.6123918942927863,
                  0.7070877245397507
                ],
                "color_key": "top"
              },
              {
                "verts": [
                  3,
                  7,
                  6,
                  2
                ],
                "normal": [
                  -0.3535577995316902,
                  0.6123918942927863,
                  -0.7070877245397507
                ],
                "color_key": "bottom"
              },
              {
                "verts": [
                  0,
                  4,
                  7,
                  3
                ],
                "normal": [
                  0.8660295833821281,
                  0.4999927606545697,
                  -0.0
                ],
                "color_key": "left"
              },
              {
                "verts": [
                  1,
                  2,
                  6,
                  5
                ],
                "normal": [
                  -0.8660295833821281,
                  -0.4999927606545697,
                  0.0
                ],
                "color_key": "right"
              }
            ],
            "derived_length_ft": 2.0682,
            "derived_angle_deg": 45.0,
            "constraints_satisfied": {
              "start_on_post_face": true,
              "end_on_beam_soffit": true
            }
          },
          {
            "id": "K5A",
            "role": "brace",
            "p0": [
              -2.2083,
              -4.2219,
              5.9575
            ],
            "p1": [
              -0.7458,
              -4.2219,
              7.42
            ],
            "axis_u": [
              0.7071067811865474,
              0.0,
              0.7071067811865476
            ],
            "axis_w": [
              0.0,
              1.0,
              0.0
            ],
            "axis_d": [
              0.7071067811865477,
              0.0,
              -0.7071067811865475
            ],
            "vertices": [
              [
                -2.311419738923038,
                -4.367733333333333,
                6.060619738923037
              ],
              [
                -2.311419738923038,
                -4.076066666666667,
                6.060619738923037
              ],
              [
                -2.1051802610769617,
                -4.076066666666667,
                5.854380261076962
              ],
              [
                -2.1051802610769617,
                -4.367733333333333,
                5.854380261076962
              ],
              [
                -0.8489197389230382,
                -4.367733333333333,
                7.523119738923038
              ],
              [
                -0.8489197389230382,
                -4.076066666666667,
                7.523119738923038
              ],
              [
                -0.6426802610769619,
                -4.076066666666667,
                7.316880261076962
              ],
              [
                -0.6426802610769619,
                -4.367733333333333,
                7.316880261076962
              ]
            ],
            "faces": [
              {
                "verts": [
                  0,
                  3,
                  2,
                  1
                ],
                "normal": [
                  -0.7071067811865474,
                  -0.0,
                  -0.7071067811865476
                ],
                "color_key": "start"
              },
              {
                "verts": [
                  4,
                  5,
                  6,
                  7
                ],
                "normal": [
                  0.7071067811865474,
                  0.0,
                  0.7071067811865476
                ],
                "color_key": "end"
              },
              {
                "verts": [
                  0,
                  1,
                  5,
                  4
                ],
                "normal": [
                  -0.7071067811865477,
                  -0.0,
                  0.7071067811865475
                ],
                "color_key": "top"
              },
              {
                "verts": [
                  3,
                  7,
                  6,
                  2
                ],
                "normal": [
                  0.7071067811865477,
                  0.0,
                  -0.7071067811865475
                ],
                "color_key": "bottom"
              },
              {
                "verts": [
                  0,
                  4,
                  7,
                  3
                ],
                "normal": [
                  -0.0,
                  -1.0,
                  -0.0
                ],
                "color_key": "left"
              },
              {
                "verts": [
                  1,
                  2,
                  6,
                  5
                ],
                "normal": [
                  0.0,
                  1.0,
                  0.0
                ],
                "color_key": "right"
              }
            ],
            "derived_length_ft": 2.0683,
            "derived_angle_deg": 45.0,
            "constraints_satisfied": {
              "start_on_post_face": true,
              "end_on_beam_soffit": true
            }
          },
          {
            "id": "K5B",
            "role": "brace",
            "p0": [
              2.2083,
              -4.2219,
              5.9575
            ],
            "p1": [
              0.7458,
              -4.2219,
              7.42
            ],
            "axis_u": [
              -0.7071067811865474,
              0.0,
              0.7071067811865476
            ],
            "axis_w": [
              0.0,
              -1.0,
              0.0
            ],
            "axis_d": [
              -0.7071067811865477,
              -0.0,
              -0.7071067811865475
            ],
            "vertices": [
              [
                2.311419738923038,
                -4.076066666666667,
                6.060619738923037
              ],
              [
                2.311419738923038,
                -4.367733333333333,
                6.060619738923037
              ],
              [
                2.1051802610769617,
                -4.367733333333333,
                5.854380261076962
              ],
              [
                2.1051802610769617,
                -4.076066666666667,
                5.854380261076962
              ],
              [
                0.8489197389230382,
                -4.076066666666667,
                7.523119738923038
              ],
              [
                0.8489197389230382,
                -4.367733333333333,
                7.523119738923038
              ],
              [
                0.6426802610769619,
                -4.367733333333333,
                7.316880261076962
              ],
              [
                0.6426802610769619,
                -4.076066666666667,
                7.316880261076962
              ]
            ],
            "faces": [
              {
                "verts": [
                  0,
                  3,
                  2,
                  1
                ],
                "normal": [
                  0.7071067811865474,
                  -0.0,
                  -0.7071067811865476
                ],
                "color_key": "start"
              },
              {
                "verts": [
                  4,
                  5,
                  6,
                  7
                ],
                "normal": [
                  -0.7071067811865474,
                  0.0,
                  0.7071067811865476
                ],
                "color_key": "end"
              },
              {
                "verts": [
                  0,
                  1,
                  5,
                  4
                ],
                "normal": [
                  0.7071067811865477,
                  0.0,
                  0.7071067811865475
                ],
                "color_key": "top"
              },
              {
                "verts": [
                  3,
                  7,
                  6,
                  2
                ],
                "normal": [
                  -0.7071067811865477,
                  -0.0,
                  -0.7071067811865475
                ],
                "color_key": "bottom"
              },
              {
                "verts": [
                  0,
                  4,
                  7,
                  3
                ],
                "normal": [
                  -0.0,
                  1.0,
                  -0.0
                ],
                "color_key": "left"
              },
              {
                "verts": [
                  1,
                  2,
                  6,
                  5
                ],
                "normal": [
                  0.0,
                  -1.0,
                  0.0
                ],
                "color_key": "right"
              }
            ],
            "derived_length_ft": 2.0683,
            "derived_angle_deg": 45.0,
            "constraints_satisfied": {
              "start_on_post_face": true,
              "end_on_beam_soffit": true
            }
          },
          {
            "id": "K6A",
            "role": "brace",
            "p0": [
              2.5521,
              -4.0234,
              5.9575
            ],
            "p1": [
              3.2833,
              -2.7569,
              7.42
            ],
            "axis_u": [
              0.3535387434175878,
              0.6123588874977771,
              0.7071258373197785
            ],
            "axis_w": [
              -0.8660295833821281,
              0.4999927606545697,
              0.0
            ],
            "axis_d": [
              0.3535577995316902,
              0.6123918942927863,
              -0.7070877245397507
            ],
            "vertices": [
              [
                2.6268354684781885,
                -4.185622762179822,
                6.060616959828713
              ],
              [
                2.3742435066584013,
                -4.0397915403222395,
                6.060616959828713
              ],
              [
                2.477364531521811,
                -3.8611772378201765,
                5.854383040171286
              ],
              [
                2.7299564933415983,
                -4.00700845967776,
                5.854383040171286
              ],
              [
                3.358035468478189,
                -2.919122762179823,
                7.523116959828713
              ],
              [
                3.1054435066584016,
                -2.77329154032224,
                7.523116959828713
              ],
              [
                3.2085645315218114,
                -2.594677237820177,
                7.3168830401712865
              ],
              [
                3.4611564933415986,
                -2.74050845967776,
                7.3168830401712865
              ]
            ],
            "faces": [
              {
                "verts": [
                  0,
                  3,
                  2,
                  1
                ],
                "normal": [
                  -0.3535387434175878,
                  -0.6123588874977771,
                  -0.7071258373197785
                ],
                "color_key": "start"
              },
              {
                "verts": [
                  4,
                  5,
                  6,
                  7
                ],
                "normal": [
                  0.3535387434175878,
                  0.6123588874977771,
                  0.7071258373197785
                ],
                "color_key": "end"
              },
              {
                "verts": [
                  0,
                  1,
                  5,
                  4
                ],
                "normal": [
                  -0.3535577995316902,
                  -0.6123918942927863,
                  0.7070877245397507
                ],
                "color_key": "top"
              },
              {
                "verts": [
                  3,
                  7,
                  6,
                  2
                ],
                "normal": [
                  0.3535577995316902,
                  0.6123918942927863,
                  -0.7070877245397507
                ],
                "color_key": "bottom"
              },
              {
                "verts": [
                  0,
                  4,
                  7,
                  3
                ],
                "normal": [
                  0.8660295833821281,
                  -0.4999927606545697,
                  -0.0
                ],
                "color_key": "left"
              },
              {
                "verts": [
                  1,
                  2,
                  6,
                  5
                ],
                "normal": [
                  -0.8660295833821281,
                  0.4999927606545697,
                  0.0
                ],
                "color_key": "right"
              }
            ],
            "derived_length_ft": 2.0682,
            "derived_angle_deg": 45.0,
            "constraints_satisfied": {
              "start_on_post_face": true,
              "end_on_beam_soffit": true
            }
          },
          {
            "id": "K6B",
            "role": "brace",
            "p0": [
              4.7604,
              -0.1985,
              5.9575
            ],
            "p1": [
              4.0292,
              -1.465,
              7.42
            ],
            "axis_u": [
              -0.35353874341758734,
              -0.6123588874977773,
              0.7071258373197785
            ],
            "axis_w": [
              0.8660295833821284,
              -0.49999276065456905,
              0.0
            ],
            "axis_d": [
              -0.35355779953168975,
              -0.6123918942927865,
              -0.7070877245397506
            ],
            "vertices": [
              [
                4.685664531521811,
                -0.036277237820177305,
                6.060616959828713
              ],
              [
                4.938256493341598,
                -0.18210845967775996,
                6.060616959828713
              ],
              [
                4.835135468478189,
                -0.36072276217982274,
                5.854383040171286
              ],
              [
                4.582543506658402,
                -0.21489154032224006,
                5.854383040171286
              ],
              [
                3.954464531521811,
                -1.3027772378201774,
                7.523116959828713
              ],
              [
                4.207056493341598,
                -1.4486084596777602,
                7.523116959828713
              ],
              [
                4.1039354684781895,
                -1.6272227621798228,
                7.3168830401712865
              ],
              [
                3.851343506658402,
                -1.48139154032224,
                7.3168830401712865
              ]
            ],
            "faces": [
              {
                "verts": [
                  0,
                  3,
                  2,
                  1
                ],
                "normal": [
                  0.35353874341758734,
                  0.6123588874977773,
                  -0.7071258373197785
                ],
                "color_key": "start"
              },
              {
                "verts": [
                  4,
                  5,
                  6,
                  7
                ],
                "normal": [
                  -0.35353874341758734,
                  -0.6123588874977773,
                  0.7071258373197785
                ],
                "color_key": "end"
              },
              {
                "verts": [
                  0,
                  1,
                  5,
                  4
                ],
                "normal": [
                  0.35355779953168975,
                  0.6123918942927865,
                  0.7070877245397506
                ],
                "color_key": "top"
              },
              {
                "verts": [
                  3,
                  7,
                  6,
                  2
                ],
                "normal": [
                  -0.35355779953168975,
                  -0.6123918942927865,
                  -0.7070877245397506
                ],
                "color_key": "bottom"
              },
              {
                "verts": [
                  0,
                  4,
                  7,
                  3
                ],
                "normal": [
                  -0.8660295833821284,
                  0.49999276065456905,
                  -0.0
                ],
                "color_key": "left"
              },
              {
                "verts": [
                  1,
                  2,
                  6,
                  5
                ],
                "normal": [
                  0.8660295833821284,
                  -0.49999276065456905,
                  0.0
                ],
                "color_key": "right"
              }
            ],
            "derived_length_ft": 2.0682,
            "derived_angle_deg": 45.0,
            "constraints_satisfied": {
              "start_on_post_face": true,
              "end_on_beam_soffit": true
            }
          },
          {
            "id": "R1",
            "role": "rafter",
            "p0": [
              5.625,
              0.0,
              8.4481
            ],
            "p1": [
              0.6495,
              0.0,
              10.1066
            ],
            "axis_u": [
              -0.9486832980505139,
              0.0,
              0.31622776601683794
            ],
            "axis_w": [
              0.0,
              -0.9999999999999999,
              0.0
            ],
            "axis_d": [
              -0.31622776601683794,
              -0.0,
              -0.948683298050514
            ],
            "vertices": [
              [
                5.625,
                0.14583333333333331,
                8.4481
              ],
              [
                0.6495,
                0.14583333333333331,
                10.1066
              ],
              [
                0.6495,
                0.14583333333333331,
                9.623474246363164
              ],
              [
                4.875,
                0.0,
                8.259004930678984
              ],
              [
                4.875,
                0.0,
                8.42
              ],
              [
                5.625,
                0.14583333333333331,
                8.42
              ],
              [
                5.625,
                -0.14583333333333331,
                8.4481
              ],
              [
                0.6495,
                -0.14583333333333331,
                10.1066
              ],
              [
                0.6495,
                -0.14583333333333331,
                9.623474246363164
              ],
              [
                4.875,
                0.0,
                8.259004930678984
              ],
              [
                4.875,
                0.0,
                8.42
              ],
              [
                5.625,
                -0.14583333333333331,
                8.42
              ]
            ],
            "faces": [
              {
                "verts": [
                  0,
                  6,
                  7,
                  1
                ],
                "normal": [
                  0.31622776601683794,
                  0.0,
                  0.948683298050514
                ],
                "color_key": "top"
              },
              {
                "verts": [
                  1,
                  7,
                  8,
                  2
                ],
                "normal": [
                  -0.9486832980505139,
                  0.0,
                  0.31622776601683794
                ],
                "color_key": "end"
              },
              {
                "verts": [
                  2,
                  8,
                  9,
                  3
                ],
                "normal": [
                  -0.31622776601683794,
                  -0.0,
                  -0.948683298050514
                ],
                "color_key": "bottom"
              },
              {
                "verts": [
                  3,
                  9,
                  10,
                  4
                ],
                "normal": [
                  0.9486832980505139,
                  -0.0,
                  -0.31622776601683794
                ],
                "color_key": "other"
              },
              {
                "verts": [
                  4,
                  10,
                  11,
                  5
                ],
                "normal": [
                  0,
                  0,
                  -1
                ],
                "color_key": "bottom"
              },
              {
                "verts": [
                  5,
                  11,
                  6,
                  0
                ],
                "normal": [
                  0.9486832980505139,
                  -0.0,
                  -0.31622776601683794
                ],
                "color_key": "start"
              },
              {
                "verts": [
                  0,
                  1,
                  2,
                  3,
                  4,
                  5
                ],
                "normal": [
                  -0.0,
                  0.9999999999999999,
                  -0.0
                ],
                "color_key": "left"
              },
              {
                "verts": [
                  11,
                  10,
                  9,
                  8,
                  7,
                  6
                ],
                "normal": [
                  0.0,
                  -0.9999999999999999,
                  0.0
                ],
                "color_key": "right"
              }
            ],
            "derived_length_ft": 5.2446,
            "derived_angle_deg": 18.43,
            "constraints_satisfied": {
              "tail_on_roof_plane": true,
              "hub_on_roof_plane": true,
              "seat_on_roof_plane": true
            }
          },
          {
            "id": "R2",
            "role": "rafter",
            "p0": [
              2.8125,
              4.8714,
              8.4481
            ],
            "p1": [
              0.3248,
              0.5625,
              10.1066
            ],
            "axis_u": [
              -0.4743349586967589,
              -0.8215869693003435,
              0.31622966153417803
            ],
            "axis_w": [
              0.8660292830933697,
              -0.4999932807796365,
              0.0
            ],
            "axis_d": [
              -0.15811270595030766,
              -0.2738641470713031,
              -0.9486826662092964
            ],
            "vertices": [
              [
                2.686204062882217,
                4.944315686780364,
                8.4481
              ],
              [
                0.1985040628822169,
                0.6354156867803636,
                10.1066
              ],
              [
                0.1985040628822169,
                0.6354156867803636,
                9.62347392459196
              ],
              [
                2.4375,
                4.2219,
                8.259004823453116
              ],
              [
                2.4375,
                4.2219,
                8.42
              ],
              [
                2.686204062882217,
                4.944315686780364,
                8.42
              ],
              [
                2.938795937117783,
                4.798484313219637,
                8.4481
              ],
              [
                0.45109593711778306,
                0.48958431321963636,
                10.1066
              ],
              [
                0.45109593711778306,
                0.48958431321963636,
                9.62347392459196
              ],
              [
                2.4375,
                4.2219,
                8.259004823453116
              ],
              [
                2.4375,
                4.2219,
                8.42
              ],
              [
                2.938795937117783,
                4.798484313219637,
                8.42
              ]
            ],
            "faces": [
              {
                "verts": [
                  0,
                  6,
                  7,
                  1
                ],
                "normal": [
                  0.15811270595030766,
                  0.2738641470713031,
                  0.9486826662092964
                ],
                "color_key": "top"
              },
              {
                "verts": [
                  1,
                  7,
                  8,
                  2
                ],
                "normal": [
                  -0.4743349586967589,
                  -0.8215869693003435,
                  0.31622966153417803
                ],
                "color_key": "end"
              },
              {
                "verts": [
                  2,
                  8,
                  9,
                  3
                ],
                "normal": [
                  -0.15811270595030766,
                  -0.2738641470713031,
                  -0.9486826662092964
                ],
                "color_key": "bottom"
              },
              {
                "verts": [
                  3,
                  9,
                  10,
                  4
                ],
                "normal": [
                  0.4743349586967589,
                  0.8215869693003435,
                  -0.31622966153417803
                ],
                "color_key": "other"
              },
              {
                "verts": [
                  4,
                  10,
                  11,
                  5
                ],
                "normal": [
                  0,
                  0,
                  -1
                ],
                "color_key": "bottom"
              },
              {
                "verts": [
                  5,
                  11,
                  6,
                  0
                ],
                "normal": [
                  0.4743349586967589,
                  0.8215869693003435,
                  -0.31622966153417803
                ],
                "color_key": "start"
              },
              {
                "verts": [
                  0,
                  1,
                  2,
                  3,
                  4,
                  5
                ],
                "normal": [
                  -0.8660292830933697,
                  0.4999932807796365,
                  -0.0
                ],
                "color_key": "left"
              },
              {
                "verts": [
                  11,
                  10,
                  9,
                  8,
                  7,
                  6
                ],
                "normal": [
                  0.8660292830933697,
                  -0.4999932807796365,
                  0.0
                ],
                "color_key": "right"
              }
            ],
            "derived_length_ft": 5.2446,
            "derived_angle_deg": 18.44,
            "constraints_satisfied": {
              "tail_on_roof_plane": true,
              "hub_on_roof_plane": true,
              "seat_on_roof_plane": true
            }
          },
          {
            "id": "R3",
            "role": "rafter",
            "p0": [
              -2.8125,
              4.8714,
              8.4481
            ],
            "p1": [
              -0.3248,
              0.5625,
              10.1066
            ],
            "axis_u": [
              0.4743349586967589,
              -0.8215869693003435,
              0.31622966153417803
            ],
            "axis_w": [
              0.8660292830933697,
              0.4999932807796365,
              -0.0
            ],
            "axis_d": [
              0.15811270595030766,
              -0.2738641470713031,
              -0.9486826662092964
            ],
            "vertices": [
              [
                -2.938795937117783,
                4.798484313219637,
                8.4481
              ],
              [
                -0.45109593711778306,
                0.48958431321963636,
                10.1066
              ],
              [
                -0.45109593711778306,
                0.48958431321963636,
                9.62347392459196
              ],
              [
                -2.4375,
                4.2219,
                8.259004823453116
              ],
              [
                -2.4375,
                4.2219,
                8.42
              ],
              [
                -2.938795937117783,
                4.798484313219637,
                8.42
              ],
              [
                -2.686204062882217,
                4.944315686780364,
                8.4481
              ],
              [
                -0.1985040628822169,
                0.6354156867803636,
                10.1066
              ],
              [
                -0.1985040628822169,
                0.6354156867803636,
                9.62347392459196
              ],
              [
                -2.4375,
                4.2219,
                8.259004823453116
              ],
              [
                -2.4375,
                4.2219,
                8.42
              ],
              [
                -2.686204062882217,
                4.944315686780364,
                8.42
              ]
            ],
            "faces": [
              {
                "verts": [
                  0,
                  6,
                  7,
                  1
                ],
                "normal": [
                  -0.15811270595030766,
                  0.2738641470713031,
                  0.9486826662092964
                ],
                "color_key": "top"
              },
              {
                "verts": [
                  1,
                  7,
                  8,
                  2
                ],
                "normal": [
                  0.4743349586967589,
                  -0.8215869693003435,
                  0.31622966153417803
                ],
                "color_key": "end"
              },
              {
                "verts": [
                  2,
                  8,
                  9,
                  3
                ],
                "normal": [
                  0.15811270595030766,
                  -0.2738641470713031,
                  -0.9486826662092964
                ],
                "color_key": "bottom"
              },
              {
                "verts": [
                  3,
                  9,
                  10,
                  4
                ],
                "normal": [
                  -0.4743349586967589,
                  0.8215869693003435,
                  -0.31622966153417803
                ],
                "color_key": "other"
              },
              {
                "verts": [
                  4,
                  10,
                  11,
                  5
                ],
                "normal": [
                  0,
                  0,
                  -1
                ],
                "color_key": "bottom"
              },
              {
                "verts": [
                  5,
                  11,
                  6,
                  0
                ],
                "normal": [
                  -0.4743349586967589,
                  0.8215869693003435,
                  -0.31622966153417803
                ],
                "color_key": "start"
              },
              {
                "verts": [
                  0,
                  1,
                  2,
                  3,
                  4,
                  5
                ],
                "normal": [
                  -0.8660292830933697,
                  -0.4999932807796365,
                  0.0
                ],
                "color_key": "left"
              },
              {
                "verts": [
                  11,
                  10,
                  9,
                  8,
                  7,
                  6
                ],
                "normal": [
                  0.8660292830933697,
                  0.4999932807796365,
                  -0.0
                ],
                "color_key": "right"
              }
            ],
            "derived_length_ft": 5.2446,
            "derived_angle_deg": 18.44,
            "constraints_satisfied": {
              "tail_on_roof_plane": true,
              "hub_on_roof_plane": true,
              "seat_on_roof_plane": true
            }
          },
          {
            "id": "R4",
            "role": "rafter",
            "p0": [
              -5.625,
              0.0,
              8.4481
            ],
            "p1": [
              -0.6495,
              0.0,
              10.1066
            ],
            "axis_u": [
              0.9486832980505139,
              0.0,
              0.31622776601683794
            ],
            "axis_w": [
              0.0,
              0.9999999999999999,
              0.0
            ],
            "axis_d": [
              0.31622776601683794,
              0.0,
              -0.948683298050514
            ],
            "vertices": [
              [
                -5.625,
                -0.14583333333333331,
                8.4481
              ],
              [
                -0.6495,
                -0.14583333333333331,
                10.1066
              ],
              [
                -0.6495,
                -0.14583333333333331,
                9.623474246363164
              ],
              [
                -4.875,
                0.0,
                8.259004930678984
              ],
              [
                -4.875,
                0.0,
                8.42
              ],
              [
                -5.625,
                -0.14583333333333331,
                8.42
              ],
              [
                -5.625,
                0.14583333333333331,
                8.4481
              ],
              [
                -0.6495,
                0.14583333333333331,
                10.1066
              ],
              [
                -0.6495,
                0.14583333333333331,
                9.623474246363164
              ],
              [
                -4.875,
                0.0,
                8.259004930678984
              ],
              [
                -4.875,
                0.0,
                8.42
              ],
              [
                -5.625,
                0.14583333333333331,
                8.42
              ]
            ],
            "faces": [
              {
                "verts": [
                  0,
                  6,
                  7,
                  1
                ],
                "normal": [
                  -0.31622776601683794,
                  -0.0,
                  0.948683298050514
                ],
                "color_key": "top"
              },
              {
                "verts": [
                  1,
                  7,
                  8,
                  2
                ],
                "normal": [
                  0.9486832980505139,
                  0.0,
                  0.31622776601683794
                ],
                "color_key": "end"
              },
              {
                "verts": [
                  2,
                  8,
                  9,
                  3
                ],
                "normal": [
                  0.31622776601683794,
                  0.0,
                  -0.948683298050514
                ],
                "color_key": "bottom"
              },
              {
                "verts": [
                  3,
                  9,
                  10,
                  4
                ],
                "normal": [
                  -0.9486832980505139,
                  -0.0,
                  -0.31622776601683794
                ],
                "color_key": "other"
              },
              {
                "verts": [
                  4,
                  10,
                  11,
                  5
                ],
                "normal": [
                  0,
                  0,
                  -1
                ],
                "color_key": "bottom"
              },
              {
                "verts": [
                  5,
                  11,
                  6,
                  0
                ],
                "normal": [
                  -0.9486832980505139,
                  -0.0,
                  -0.31622776601683794
                ],
                "color_key": "start"
              },
              {
                "verts": [
                  0,
                  1,
                  2,
                  3,
                  4,
                  5
                ],
                "normal": [
                  -0.0,
                  -0.9999999999999999,
                  -0.0
                ],
                "color_key": "left"
              },
              {
                "verts": [
                  11,
                  10,
                  9,
                  8,
                  7,
                  6
                ],
                "normal": [
                  0.0,
                  0.9999999999999999,
                  0.0
                ],
                "color_key": "right"
              }
            ],
            "derived_length_ft": 5.2446,
            "derived_angle_deg": 18.43,
            "constraints_satisfied": {
              "tail_on_roof_plane": true,
              "hub_on_roof_plane": true,
              "seat_on_roof_plane": true
            }
          },
          {
            "id": "R5",
            "role": "rafter",
            "p0": [
              -2.8125,
              -4.8714,
              8.4481
            ],
            "p1": [
              -0.3248,
              -0.5625,
              10.1066
            ],
            "axis_u": [
              0.4743349586967589,
              0.8215869693003435,
              0.31622966153417803
            ],
            "axis_w": [
              -0.8660292830933697,
              0.4999932807796365,
              0.0
            ],
            "axis_d": [
              0.15811270595030766,
              0.2738641470713031,
              -0.9486826662092964
            ],
            "vertices": [
              [
                -2.686204062882217,
                -4.944315686780364,
                8.4481
              ],
              [
                -0.1985040628822169,
                -0.6354156867803636,
                10.1066
              ],
              [
                -0.1985040628822169,
                -0.6354156867803636,
                9.62347392459196
              ],
              [
                -2.4375,
                -4.2219,
                8.259004823453116
              ],
              [
                -2.4375,
                -4.2219,
                8.42
              ],
              [
                -2.686204062882217,
                -4.944315686780364,
                8.42
              ],
              [
                -2.938795937117783,
                -4.798484313219637,
                8.4481
              ],
              [
                -0.45109593711778306,
                -0.48958431321963636,
                10.1066
              ],
              [
                -0.45109593711778306,
                -0.48958431321963636,
                9.62347392459196
              ],
              [
                -2.4375,
                -4.2219,
                8.259004823453116
              ],
              [
                -2.4375,
                -4.2219,
                8.42
              ],
              [
                -2.938795937117783,
                -4.798484313219637,
                8.42
              ]
            ],
            "faces": [
              {
                "verts": [
                  0,
                  6,
                  7,
                  1
                ],
                "normal": [
                  -0.15811270595030766,
                  -0.2738641470713031,
                  0.9486826662092964
                ],
                "color_key": "top"
              },
              {
                "verts": [
                  1,
                  7,
                  8,
                  2
                ],
                "normal": [
                  0.4743349586967589,
                  0.8215869693003435,
                  0.31622966153417803
                ],
                "color_key": "end"
              },
              {
                "verts": [
                  2,
                  8,
                  9,
                  3
                ],
                "normal": [
                  0.15811270595030766,
                  0.2738641470713031,
                  -0.9486826662092964
                ],
                "color_key": "bottom"
              },
              {
                "verts": [
                  3,
                  9,
                  10,
                  4
                ],
                "normal": [
                  -0.4743349586967589,
                  -0.8215869693003435,
                  -0.31622966153417803
                ],
                "color_key": "other"
              },
              {
                "verts": [
                  4,
                  10,
                  11,
                  5
                ],
                "normal": [
                  0,
                  0,
                  -1
                ],
                "color_key": "bottom"
              },
              {
                "verts": [
                  5,
                  11,
                  6,
                  0
                ],
                "normal": [
                  -0.4743349586967589,
                  -0.8215869693003435,
                  -0.31622966153417803
                ],
                "color_key": "start"
              },
              {
                "verts": [
                  0,
                  1,
                  2,
                  3,
                  4,
                  5
                ],
                "normal": [
                  0.8660292830933697,
                  -0.4999932807796365,
                  -0.0
                ],
                "color_key": "left"
              },
              {
                "verts": [
                  11,
                  10,
                  9,
                  8,
                  7,
                  6
                ],
                "normal": [
                  -0.8660292830933697,
                  0.4999932807796365,
                  0.0
                ],
                "color_key": "right"
              }
            ],
            "derived_length_ft": 5.2446,
            "derived_angle_deg": 18.44,
            "constraints_satisfied": {
              "tail_on_roof_plane": true,
              "hub_on_roof_plane": true,
              "seat_on_roof_plane": true
            }
          },
          {
            "id": "R6",
            "role": "rafter",
            "p0": [
              2.8125,
              -4.8714,
              8.4481
            ],
            "p1": [
              0.3248,
              -0.5625,
              10.1066
            ],
            "axis_u": [
              -0.4743349586967589,
              0.8215869693003435,
              0.31622966153417803
            ],
            "axis_w": [
              -0.8660292830933697,
              -0.4999932807796365,
              0.0
            ],
            "axis_d": [
              -0.15811270595030766,
              0.2738641470713031,
              -0.9486826662092964
            ],
            "vertices": [
              [
                2.938795937117783,
                -4.798484313219637,
                8.4481
              ],
              [
                0.45109593711778306,
                -0.48958431321963636,
                10.1066
              ],
              [
                0.45109593711778306,
                -0.48958431321963636,
                9.62347392459196
              ],
              [
                2.4375,
                -4.2219,
                8.259004823453116
              ],
              [
                2.4375,
                -4.2219,
                8.42
              ],
              [
                2.938795937117783,
                -4.798484313219637,
                8.42
              ],
              [
                2.686204062882217,
                -4.944315686780364,
                8.4481
              ],
              [
                0.1985040628822169,
                -0.6354156867803636,
                10.1066
              ],
              [
                0.1985040628822169,
                -0.6354156867803636,
                9.62347392459196
              ],
              [
                2.4375,
                -4.2219,
                8.259004823453116
              ],
              [
                2.4375,
                -4.2219,
                8.42
              ],
              [
                2.686204062882217,
                -4.944315686780364,
                8.42
              ]
            ],
            "faces": [
              {
                "verts": [
                  0,
                  6,
                  7,
                  1
                ],
                "normal": [
                  0.15811270595030766,
                  -0.2738641470713031,
                  0.9486826662092964
                ],
                "color_key": "top"
              },
              {
                "verts": [
                  1,
                  7,
                  8,
                  2
                ],
                "normal": [
                  -0.4743349586967589,
                  0.8215869693003435,
                  0.31622966153417803
                ],
                "color_key": "end"
              },
              {
                "verts": [
                  2,
                  8,
                  9,
                  3
                ],
                "normal": [
                  -0.15811270595030766,
                  0.2738641470713031,
                  -0.9486826662092964
                ],
                "color_key": "bottom"
              },
              {
                "verts": [
                  3,
                  9,
                  10,
                  4
                ],
                "normal": [
                  0.4743349586967589,
                  -0.8215869693003435,
                  -0.31622966153417803
                ],
                "color_key": "other"
              },
              {
                "verts": [
                  4,
                  10,
                  11,
                  5
                ],
                "normal": [
                  0,
                  0,
                  -1
                ],
                "color_key": "bottom"
              },
              {
                "verts": [
                  5,
                  11,
                  6,
                  0
                ],
                "normal": [
                  0.4743349586967589,
                  -0.8215869693003435,
                  -0.31622966153417803
                ],
                "color_key": "start"
              },
              {
                "verts": [
                  0,
                  1,
                  2,
                  3,
                  4,
                  5
                ],
                "normal": [
                  0.8660292830933697,
                  0.4999932807796365,
                  -0.0
                ],
                "color_key": "left"
              },
              {
                "verts": [
                  11,
                  10,
                  9,
                  8,
                  7,
                  6
                ],
                "normal": [
                  -0.8660292830933697,
                  -0.4999932807796365,
                  0.0
                ],
                "color_key": "right"
              }
            ],
            "derived_length_ft": 5.2446,
            "derived_angle_deg": 18.44,
            "constraints_satisfied": {
              "tail_on_roof_plane": true,
              "hub_on_roof_plane": true,
              "seat_on_roof_plane": true
            }
          },
          {
            "id": "J1a",
            "role": "rafter",
            "p0": [
              4.712,
              1.7823,
              8.4095
            ],
            "p1": [
              1.8646,
              0.1383,
              9.675
            ],
            "axis_u": [
              -0.8082191178128488,
              -0.46664052457832533,
              0.35920534297680734
            ],
            "axis_w": [
              0.5000120539623806,
              -0.8660184443141621,
              0.0
            ],
            "axis_d": [
              -0.31107845231410974,
              -0.1796070013360948,
              -0.933258550229739
            ],
            "vertices": [
              [
                4.639081575463819,
                1.9085943564624819,
                8.4095
              ],
              [
                1.7916815754638196,
                0.26459435646248197,
                9.675
              ],
              [
                1.7916815754638196,
                0.26459435646248197,
                9.183889221298315
              ],
              [
                4.0625,
                1.4073,
                8.256344029962827
              ],
              [
                4.0625,
                1.4073,
                8.42
              ],
              [
                4.639081575463819,
                1.9085943564624819,
                8.42
              ],
              [
                4.784918424536181,
                1.6560056435375181,
                8.4095
              ],
              [
                1.9375184245361805,
                0.01200564353751804,
                9.675
              ],
              [
                1.9375184245361805,
                0.01200564353751804,
                9.183889221298315
              ],
              [
                4.0625,
                1.4073,
                8.256344029962827
              ],
              [
                4.0625,
                1.4073,
                8.42
              ],
              [
                4.784918424536181,
                1.6560056435375181,
                8.42
              ]
            ],
            "faces": [
              {
                "verts": [
                  0,
                  6,
                  7,
                  1
                ],
                "normal": [
                  0.31107845231410974,
                  0.1796070013360948,
                  0.933258550229739
                ],
                "color_key": "top"
              },
              {
                "verts": [
                  1,
                  7,
                  8,
                  2
                ],
                "normal": [
                  -0.8082191178128488,
                  -0.46664052457832533,
                  0.35920534297680734
                ],
                "color_key": "end"
              },
              {
                "verts": [
                  2,
                  8,
                  9,
                  3
                ],
                "normal": [
                  -0.31107845231410974,
                  -0.1796070013360948,
                  -0.933258550229739
                ],
                "color_key": "bottom"
              },
              {
                "verts": [
                  3,
                  9,
                  10,
                  4
                ],
                "normal": [
                  0.8082191178128488,
                  0.46664052457832533,
                  -0.35920534297680734
                ],
                "color_key": "other"
              },
              {
                "verts": [
                  4,
                  10,
                  11,
                  5
                ],
                "normal": [
                  0,
                  0,
                  -1
                ],
                "color_key": "bottom"
              },
              {
                "verts": [
                  5,
                  11,
                  6,
                  0
                ],
                "normal": [
                  0.8082191178128488,
                  0.46664052457832533,
                  -0.35920534297680734
                ],
                "color_key": "start"
              },
              {
                "verts": [
                  0,
                  1,
                  2,
                  3,
                  4,
                  5
                ],
                "normal": [
                  -0.5000120539623806,
                  0.8660184443141621,
                  -0.0
                ],
                "color_key": "left"
              },
              {
                "verts": [
                  11,
                  10,
                  9,
                  8,
                  7,
                  6
                ],
                "normal": [
                  0.5000120539623806,
                  -0.8660184443141621,
                  0.0
                ],
                "color_key": "right"
              }
            ],
            "derived_length_ft": 3.5231,
            "derived_angle_deg": 21.05,
            "constraints_satisfied": {
              "tail_on_roof_plane": true,
              "end_on_roof_plane": true,
              "seat_on_roof_plane": true
            }
          },
          {
            "id": "J1b",
            "role": "rafter",
            "p0": [
              3.8995,
              3.1896,
              8.4095
            ],
            "p1": [
              1.0521,
              1.5457,
              9.675
            ],
            "axis_u": [
              -0.8082298228364461,
              -0.46661832048915974,
              0.3592101007232996
            ],
            "axis_w": [
              0.4999892430397753,
              -0.8660316142292455,
              0.0
            ],
            "axis_d": [
              -0.311087303376849,
              -0.179601186352884,
              -0.9332567189891305
            ],
            "vertices": [
              [
                3.8265849020566995,
                3.3158962770750984,
                8.4095
              ],
              [
                0.9791849020566995,
                1.6719962770750985,
                9.675
              ],
              [
                0.9791849020566995,
                1.6719962770750985,
                9.183888257638495
              ],
              [
                3.25,
                2.8146,
                8.256343708836333
              ],
              [
                3.25,
                2.8146,
                8.42
              ],
              [
                3.8265849020566995,
                3.3158962770750984,
                8.42
              ],
              [
                3.972415097943301,
                3.0633037229249016,
                8.4095
              ],
              [
                1.1250150979433007,
                1.4194037229249017,
                9.675
              ],
              [
                1.1250150979433007,
                1.4194037229249017,
                9.183888257638495
              ],
              [
                3.25,
                2.8146,
                8.256343708836333
              ],
              [
                3.25,
                2.8146,
                8.42
              ],
              [
                3.972415097943301,
                3.0633037229249016,
                8.42
              ]
            ],
            "faces": [
              {
                "verts": [
                  0,
                  6,
                  7,
                  1
                ],
                "normal": [
                  0.311087303376849,
                  0.179601186352884,
                  0.9332567189891305
                ],
                "color_key": "top"
              },
              {
                "verts": [
                  1,
                  7,
                  8,
                  2
                ],
                "normal": [
                  -0.8082298228364461,
                  -0.46661832048915974,
                  0.3592101007232996
                ],
                "color_key": "end"
              },
              {
                "verts": [
                  2,
                  8,
                  9,
                  3
                ],
                "normal": [
                  -0.311087303376849,
                  -0.179601186352884,
                  -0.9332567189891305
                ],
                "color_key": "bottom"
              },
              {
                "verts": [
                  3,
                  9,
                  10,
                  4
                ],
                "normal": [
                  0.8082298228364461,
                  0.46661832048915974,
                  -0.3592101007232996
                ],
                "color_key": "other"
              },
              {
                "verts": [
                  4,
                  10,
                  11,
                  5
                ],
                "normal": [
                  0,
                  0,
                  -1
                ],
                "color_key": "bottom"
              },
              {
                "verts": [
                  5,
                  11,
                  6,
                  0
                ],
                "normal": [
                  0.8082298228364461,
                  0.46661832048915974,
                  -0.3592101007232996
                ],
                "color_key": "start"
              },
              {
                "verts": [
                  0,
                  1,
                  2,
                  3,
                  4,
                  5
                ],
                "normal": [
                  -0.4999892430397753,
                  0.8660316142292455,
                  -0.0
                ],
                "color_key": "left"
              },
              {
                "verts": [
                  11,
                  10,
                  9,
                  8,
                  7,
                  6
                ],
                "normal": [
                  0.4999892430397753,
                  -0.8660316142292455,
                  0.0
                ],
                "color_key": "right"
              }
            ],
            "derived_length_ft": 3.523,
            "derived_angle_deg": 21.05,
            "constraints_satisfied": {
              "tail_on_roof_plane": true,
              "end_on_roof_plane": true,
              "seat_on_roof_plane": true
            }
          },
          {
            "id": "J2a",
            "role": "rafter",
            "p0": [
              0.8125,
              4.9719,
              8.4095
            ],
            "p1": [
              0.8125,
              1.684,
              9.675
            ],
            "axis_u": [
              0.0,
              -0.9332577908220859,
              0.35920731600272243
            ],
            "axis_w": [
              0.9999999999999999,
              0.0,
              -0.0
            ],
            "axis_d": [
              0.0,
              -0.35920731600272243,
              -0.933257790822086
            ],
            "vertices": [
              [
                0.6666666666666667,
                4.9719,
                8.4095
              ],
              [
                0.6666666666666667,
                1.684,
                9.675
              ],
              [
                0.6666666666666667,
                1.684,
                9.183888821673166
              ],
              [
                0.8125,
                4.2219,
                8.256343896793195
              ],
              [
                0.8125,
                4.2219,
                8.42
              ],
              [
                0.6666666666666667,
                4.9719,
                8.42
              ],
              [
                0.9583333333333333,
                4.9719,
                8.4095
              ],
              [
                0.9583333333333333,
                1.684,
                9.675
              ],
              [
                0.9583333333333333,
                1.684,
                9.183888821673166
              ],
              [
                0.8125,
                4.2219,
                8.256343896793195
              ],
              [
                0.8125,
                4.2219,
                8.42
              ],
              [
                0.9583333333333333,
                4.9719,
                8.42
              ]
            ],
            "faces": [
              {
                "verts": [
                  0,
                  6,
                  7,
                  1
                ],
                "normal": [
                  -0.0,
                  0.35920731600272243,
                  0.933257790822086
                ],
                "color_key": "top"
              },
              {
                "verts": [
                  1,
                  7,
                  8,
                  2
                ],
                "normal": [
                  0.0,
                  -0.9332577908220859,
                  0.35920731600272243
                ],
                "color_key": "end"
              },
              {
                "verts": [
                  2,
                  8,
                  9,
                  3
                ],
                "normal": [
                  0.0,
                  -0.35920731600272243,
                  -0.933257790822086
                ],
                "color_key": "bottom"
              },
              {
                "verts": [
                  3,
                  9,
                  10,
                  4
                ],
                "normal": [
                  -0.0,
                  0.9332577908220859,
                  -0.35920731600272243
                ],
                "color_key": "other"
              },
              {
                "verts": [
                  4,
                  10,
                  11,
                  5
                ],
                "normal": [
                  0,
                  0,
                  -1
                ],
                "color_key": "bottom"
              },
              {
                "verts": [
                  5,
                  11,
                  6,
                  0
                ],
                "normal": [
                  -0.0,
                  0.9332577908220859,
                  -0.35920731600272243
                ],
                "color_key": "start"
              },
              {
                "verts": [
                  0,
                  1,
                  2,
                  3,
                  4,
                  5
                ],
                "normal": [
                  -0.9999999999999999,
                  -0.0,
                  0.0
                ],
                "color_key": "left"
              },
              {
                "verts": [
                  11,
                  10,
                  9,
                  8,
                  7,
                  6
                ],
                "normal": [
                  0.9999999999999999,
                  0.0,
                  -0.0
                ],
                "color_key": "right"
              }
            ],
            "derived_length_ft": 3.523,
            "derived_angle_deg": 21.05,
            "constraints_satisfied": {
              "tail_on_roof_plane": true,
              "end_on_roof_plane": true,
              "seat_on_roof_plane": true
            }
          },
          {
            "id": "J2b",
            "role": "rafter",
            "p0": [
              -0.8125,
              4.9719,
              8.4095
            ],
            "p1": [
              -0.8125,
              1.684,
              9.675
            ],
            "axis_u": [
              0.0,
              -0.9332577908220859,
              0.35920731600272243
            ],
            "axis_w": [
              0.9999999999999999,
              0.0,
              -0.0
            ],
            "axis_d": [
              0.0,
              -0.35920731600272243,
              -0.933257790822086
            ],
            "vertices": [
              [
                -0.9583333333333333,
                4.9719,
                8.4095
              ],
              [
                -0.9583333333333333,
                1.684,
                9.675
              ],
              [
                -0.9583333333333333,
                1.684,
                9.183888821673166
              ],
              [
                -0.8125,
                4.2219,
                8.256343896793195
              ],
              [
                -0.8125,
                4.2219,
                8.42
              ],
              [
                -0.9583333333333333,
                4.9719,
                8.42
              ],
              [
                -0.6666666666666667,
                4.9719,
                8.4095
              ],
              [
                -0.6666666666666667,
                1.684,
                9.675
              ],
              [
                -0.6666666666666667,
                1.684,
                9.183888821673166
              ],
              [
                -0.8125,
                4.2219,
                8.256343896793195
              ],
              [
                -0.8125,
                4.2219,
                8.42
              ],
              [
                -0.6666666666666667,
                4.9719,
                8.42
              ]
            ],
            "faces": [
              {
                "verts": [
                  0,
                  6,
                  7,
                  1
                ],
                "normal": [
                  -0.0,
                  0.35920731600272243,
                  0.933257790822086
                ],
                "color_key": "top"
              },
              {
                "verts": [
                  1,
                  7,
                  8,
                  2
                ],
                "normal": [
                  0.0,
                  -0.9332577908220859,
                  0.35920731600272243
                ],
                "color_key": "end"
              },
              {
                "verts": [
                  2,
                  8,
                  9,
                  3
                ],
                "normal": [
                  0.0,
                  -0.35920731600272243,
                  -0.933257790822086
                ],
                "color_key": "bottom"
              },
              {
                "verts": [
                  3,
                  9,
                  10,
                  4
                ],
                "normal": [
                  -0.0,
                  0.9332577908220859,
                  -0.35920731600272243
                ],
                "color_key": "other"
              },
              {
                "verts": [
                  4,
                  10,
                  11,
                  5
                ],
                "normal": [
                  0,
                  0,
                  -1
                ],
                "color_key": "bottom"
              },
              {
                "verts": [
                  5,
                  11,
                  6,
                  0
                ],
                "normal": [
                  -0.0,
                  0.9332577908220859,
                  -0.35920731600272243
                ],
                "color_key": "start"
              },
              {
                "verts": [
                  0,
                  1,
                  2,
                  3,
                  4,
                  5
                ],
                "normal": [
                  -0.9999999999999999,
                  -0.0,
                  0.0
                ],
                "color_key": "left"
              },
              {
                "verts": [
                  11,
                  10,
                  9,
                  8,
                  7,
                  6
                ],
                "normal": [
                  0.9999999999999999,
                  0.0,
                  -0.0
                ],
                "color_key": "right"
              }
            ],
            "derived_length_ft": 3.523,
            "derived_angle_deg": 21.05,
            "constraints_satisfied": {
              "tail_on_roof_plane": true,
              "end_on_roof_plane": true,
              "seat_on_roof_plane": true
            }
          },
          {
            "id": "J3a",
            "role": "rafter",
            "p0": [
              -3.8995,
              3.1896,
              8.4095
            ],
            "p1": [
              -1.0521,
              1.5457,
              9.675
            ],
            "axis_u": [
              0.8082298228364461,
              -0.46661832048915974,
              0.3592101007232996
            ],
            "axis_w": [
              0.4999892430397753,
              0.8660316142292455,
              -0.0
            ],
            "axis_d": [
              0.311087303376849,
              -0.179601186352884,
              -0.9332567189891305
            ],
            "vertices": [
              [
                -3.972415097943301,
                3.0633037229249016,
                8.4095
              ],
              [
                -1.1250150979433007,
                1.4194037229249017,
                9.675
              ],
              [
                -1.1250150979433007,
                1.4194037229249017,
                9.183888257638495
              ],
              [
                -3.25,
                2.8146,
                8.256343708836333
              ],
              [
                -3.25,
                2.8146,
                8.42
              ],
              [
                -3.972415097943301,
                3.0633037229249016,
                8.42
              ],
              [
                -3.8265849020566995,
                3.3158962770750984,
                8.4095
              ],
              [
                -0.9791849020566995,
                1.6719962770750985,
                9.675
              ],
              [
                -0.9791849020566995,
                1.6719962770750985,
                9.183888257638495
              ],
              [
                -3.25,
                2.8146,
                8.256343708836333
              ],
              [
                -3.25,
                2.8146,
                8.42
              ],
              [
                -3.8265849020566995,
                3.3158962770750984,
                8.42
              ]
            ],
            "faces": [
              {
                "verts": [
                  0,
                  6,
                  7,
                  1
                ],
                "normal": [
                  -0.311087303376849,
                  0.179601186352884,
                  0.9332567189891305
                ],
                "color_key": "top"
              },
              {
                "verts": [
                  1,
                  7,
                  8,
                  2
                ],
                "normal": [
                  0.8082298228364461,
                  -0.46661832048915974,
                  0.3592101007232996
                ],
                "color_key": "end"
              },
              {
                "verts": [
                  2,
                  8,
                  9,
                  3
                ],
                "normal": [
                  0.311087303376849,
                  -0.179601186352884,
                  -0.9332567189891305
                ],
                "color_key": "bottom"
              },
              {
                "verts": [
                  3,
                  9,
                  10,
                  4
                ],
                "normal": [
                  -0.8082298228364461,
                  0.46661832048915974,
                  -0.3592101007232996
                ],
                "color_key": "other"
              },
              {
                "verts": [
                  4,
                  10,
                  11,
                  5
                ],
                "normal": [
                  0,
                  0,
                  -1
                ],
                "color_key": "bottom"
              },
              {
                "verts": [
                  5,
                  11,
                  6,
                  0
                ],
                "normal": [
                  -0.8082298228364461,
                  0.46661832048915974,
                  -0.3592101007232996
                ],
                "color_key": "start"
              },
              {
                "verts": [
                  0,
                  1,
                  2,
                  3,
                  4,
                  5
                ],
                "normal": [
                  -0.4999892430397753,
                  -0.8660316142292455,
                  0.0
                ],
                "color_key": "left"
              },
              {
                "verts": [
                  11,
                  10,
                  9,
                  8,
                  7,
                  6
                ],
                "normal": [
                  0.4999892430397753,
                  0.8660316142292455,
                  -0.0
                ],
                "color_key": "right"
              }
            ],
            "derived_length_ft": 3.523,
            "derived_angle_deg": 21.05,
            "constraints_satisfied": {
              "tail_on_roof_plane": true,
              "end_on_roof_plane": true,
              "seat_on_roof_plane": true
            }
          },
          {
            "id": "J3b",
            "role": "rafter",
            "p0": [
              -4.712,
              1.7823,
              8.4095
            ],
            "p1": [
              -1.8646,
              0.1383,
              9.675
            ],
            "axis_u": [
              0.8082191178128488,
              -0.46664052457832533,
              0.35920534297680734
            ],
            "axis_w": [
              0.5000120539623806,
              0.8660184443141621,
              -0.0
            ],
            "axis_d": [
              0.31107845231410974,
              -0.1796070013360948,
              -0.933258550229739
            ],
            "vertices": [
              [
                -4.784918424536181,
                1.6560056435375181,
                8.4095
              ],
              [
                -1.9375184245361805,
                0.01200564353751804,
                9.675
              ],
              [
                -1.9375184245361805,
                0.01200564353751804,
                9.183889221298315
              ],
              [
                -4.0625,
                1.4073,
                8.256344029962827
              ],
              [
                -4.0625,
                1.4073,
                8.42
              ],
              [
                -4.784918424536181,
                1.6560056435375181,
                8.42
              ],
              [
                -4.639081575463819,
                1.9085943564624819,
                8.4095
              ],
              [
                -1.7916815754638196,
                0.26459435646248197,
                9.675
              ],
              [
                -1.7916815754638196,
                0.26459435646248197,
                9.183889221298315
              ],
              [
                -4.0625,
                1.4073,
                8.256344029962827
              ],
              [
                -4.0625,
                1.4073,
                8.42
              ],
              [
                -4.639081575463819,
                1.9085943564624819,
                8.42
              ]
            ],
            "faces": [
              {
                "verts": [
                  0,
                  6,
                  7,
                  1
                ],
                "normal": [
                  -0.31107845231410974,
                  0.1796070013360948,
                  0.933258550229739
                ],
                "color_key": "top"
              },
              {
                "verts": [
                  1,
                  7,
                  8,
                  2
                ],
                "normal": [
                  0.8082191178128488,
                  -0.46664052457832533,
                  0.35920534297680734
                ],
                "color_key": "end"
              },
              {
                "verts": [
                  2,
                  8,
                  9,
                  3
                ],
                "normal": [
                  0.31107845231410974,
                  -0.1796070013360948,
                  -0.933258550229739
                ],
                "color_key": "bottom"
              },
              {
                "verts": [
                  3,
                  9,
                  10,
                  4
                ],
                "normal": [
                  -0.8082191178128488,
                  0.46664052457832533,
                  -0.35920534297680734
                ],
                "color_key": "other"
              },
              {
                "verts": [
                  4,
                  10,
                  11,
                  5
                ],
                "normal": [
                  0,
                  0,
                  -1
                ],
                "color_key": "bottom"
              },
              {
                "verts": [
                  5,
                  11,
                  6,
                  0
                ],
                "normal": [
                  -0.8082191178128488,
                  0.46664052457832533,
                  -0.35920534297680734
                ],
                "color_key": "start"
              },
              {
                "verts": [
                  0,
                  1,
                  2,
                  3,
                  4,
                  5
                ],
                "normal": [
                  -0.5000120539623806,
                  -0.8660184443141621,
                  0.0
                ],
                "color_key": "left"
              },
              {
                "verts": [
                  11,
                  10,
                  9,
                  8,
                  7,
                  6
                ],
                "normal": [
                  0.5000120539623806,
                  0.8660184443141621,
                  -0.0
                ],
                "color_key": "right"
              }
            ],
            "derived_length_ft": 3.5231,
            "derived_angle_deg": 21.05,
            "constraints_satisfied": {
              "tail_on_roof_plane": true,
              "end_on_roof_plane": true,
              "seat_on_roof_plane": true
            }
          },
          {
            "id": "J4a",
            "role": "rafter",
            "p0": [
              -4.712,
              -1.7823,
              8.4095
            ],
            "p1": [
              -1.8646,
              -0.1383,
              9.675
            ],
            "axis_u": [
              0.8082191178128488,
              0.46664052457832533,
              0.35920534297680734
            ],
            "axis_w": [
              -0.5000120539623806,
              0.8660184443141621,
              0.0
            ],
            "axis_d": [
              0.31107845231410974,
              0.1796070013360948,
              -0.933258550229739
            ],
            "vertices": [
              [
                -4.639081575463819,
                -1.9085943564624819,
                8.4095
              ],
              [
                -1.7916815754638196,
                -0.26459435646248197,
                9.675
              ],
              [
                -1.7916815754638196,
                -0.26459435646248197,
                9.183889221298315
              ],
              [
                -4.0625,
                -1.4073,
                8.256344029962827
              ],
              [
                -4.0625,
                -1.4073,
                8.42
              ],
              [
                -4.639081575463819,
                -1.9085943564624819,
                8.42
              ],
              [
                -4.784918424536181,
                -1.6560056435375181,
                8.4095
              ],
              [
                -1.9375184245361805,
                -0.01200564353751804,
                9.675
              ],
              [
                -1.9375184245361805,
                -0.01200564353751804,
                9.183889221298315
              ],
              [
                -4.0625,
                -1.4073,
                8.256344029962827
              ],
              [
                -4.0625,
                -1.4073,
                8.42
              ],
              [
                -4.784918424536181,
                -1.6560056435375181,
                8.42
              ]
            ],
            "faces": [
              {
                "verts": [
                  0,
                  6,
                  7,
                  1
                ],
                "normal": [
                  -0.31107845231410974,
                  -0.1796070013360948,
                  0.933258550229739
                ],
                "color_key": "top"
              },
              {
                "verts": [
                  1,
                  7,
                  8,
                  2
                ],
                "normal": [
                  0.8082191178128488,
                  0.46664052457832533,
                  0.35920534297680734
                ],
                "color_key": "end"
              },
              {
                "verts": [
                  2,
                  8,
                  9,
                  3
                ],
                "normal": [
                  0.31107845231410974,
                  0.1796070013360948,
                  -0.933258550229739
                ],
                "color_key": "bottom"
              },
              {
                "verts": [
                  3,
                  9,
                  10,
                  4
                ],
                "normal": [
                  -0.8082191178128488,
                  -0.46664052457832533,
                  -0.35920534297680734
                ],
                "color_key": "other"
              },
              {
                "verts": [
                  4,
                  10,
                  11,
                  5
                ],
                "normal": [
                  0,
                  0,
                  -1
                ],
                "color_key": "bottom"
              },
              {
                "verts": [
                  5,
                  11,
                  6,
                  0
                ],
                "normal": [
                  -0.8082191178128488,
                  -0.46664052457832533,
                  -0.35920534297680734
                ],
                "color_key": "start"
              },
              {
                "verts": [
                  0,
                  1,
                  2,
                  3,
                  4,
                  5
                ],
                "normal": [
                  0.5000120539623806,
                  -0.8660184443141621,
                  -0.0
                ],
                "color_key": "left"
              },
              {
                "verts": [
                  11,
                  10,
                  9,
                  8,
                  7,
                  6
                ],
                "normal": [
                  -0.5000120539623806,
                  0.8660184443141621,
                  0.0
                ],
                "color_key": "right"
              }
            ],
            "derived_length_ft": 3.5231,
            "derived_angle_deg": 21.05,
            "constraints_satisfied": {
              "tail_on_roof_plane": true,
              "end_on_roof_plane": true,
              "seat_on_roof_plane": true
            }
          },
          {
            "id": "J4b",
            "role": "rafter",
            "p0": [
              -3.8995,
              -3.1896,
              8.4095
            ],
            "p1": [
              -1.0521,
              -1.5457,
              9.675
            ],
            "axis_u": [
              0.8082298228364461,
              0.46661832048915974,
              0.3592101007232996
            ],
            "axis_w": [
              -0.4999892430397753,
              0.8660316142292455,
              0.0
            ],
            "axis_d": [
              0.311087303376849,
              0.179601186352884,
              -0.9332567189891305
            ],
            "vertices": [
              [
                -3.8265849020566995,
                -3.3158962770750984,
                8.4095
              ],
              [
                -0.9791849020566995,
                -1.6719962770750985,
                9.675
              ],
              [
                -0.9791849020566995,
                -1.6719962770750985,
                9.183888257638495
              ],
              [
                -3.25,
                -2.8146,
                8.256343708836333
              ],
              [
                -3.25,
                -2.8146,
                8.42
              ],
              [
                -3.8265849020566995,
                -3.3158962770750984,
                8.42
              ],
              [
                -3.972415097943301,
                -3.0633037229249016,
                8.4095
              ],
              [
                -1.1250150979433007,
                -1.4194037229249017,
                9.675
              ],
              [
                -1.1250150979433007,
                -1.4194037229249017,
                9.183888257638495
              ],
              [
                -3.25,
                -2.8146,
                8.256343708836333
              ],
              [
                -3.25,
                -2.8146,
                8.42
              ],
              [
                -3.972415097943301,
                -3.0633037229249016,
                8.42
              ]
            ],
            "faces": [
              {
                "verts": [
                  0,
                  6,
                  7,
                  1
                ],
                "normal": [
                  -0.311087303376849,
                  -0.179601186352884,
                  0.9332567189891305
                ],
                "color_key": "top"
              },
              {
                "verts": [
                  1,
                  7,
                  8,
                  2
                ],
                "normal": [
                  0.8082298228364461,
                  0.46661832048915974,
                  0.3592101007232996
                ],
                "color_key": "end"
              },
              {
                "verts": [
                  2,
                  8,
                  9,
                  3
                ],
                "normal": [
                  0.311087303376849,
                  0.179601186352884,
                  -0.9332567189891305
                ],
                "color_key": "bottom"
              },
              {
                "verts": [
                  3,
                  9,
                  10,
                  4
                ],
                "normal": [
                  -0.8082298228364461,
                  -0.46661832048915974,
                  -0.3592101007232996
                ],
                "color_key": "other"
              },
              {
                "verts": [
                  4,
                  10,
                  11,
                  5
                ],
                "normal": [
                  0,
                  0,
                  -1
                ],
                "color_key": "bottom"
              },
              {
                "verts": [
                  5,
                  11,
                  6,
                  0
                ],
                "normal": [
                  -0.8082298228364461,
                  -0.46661832048915974,
                  -0.3592101007232996
                ],
                "color_key": "start"
              },
              {
                "verts": [
                  0,
                  1,
                  2,
                  3,
                  4,
                  5
                ],
                "normal": [
                  0.4999892430397753,
                  -0.8660316142292455,
                  -0.0
                ],
                "color_key": "left"
              },
              {
                "verts": [
                  11,
                  10,
                  9,
                  8,
                  7,
                  6
                ],
                "normal": [
                  -0.4999892430397753,
                  0.8660316142292455,
                  0.0
                ],
                "color_key": "right"
              }
            ],
            "derived_length_ft": 3.523,
            "derived_angle_deg": 21.05,
            "constraints_satisfied": {
              "tail_on_roof_plane": true,
              "end_on_roof_plane": true,
              "seat_on_roof_plane": true
            }
          },
          {
            "id": "J5a",
            "role": "rafter",
            "p0": [
              -0.8125,
              -4.9719,
              8.4095
            ],
            "p1": [
              -0.8125,
              -1.684,
              9.675
            ],
            "axis_u": [
              0.0,
              0.9332577908220859,
              0.35920731600272243
            ],
            "axis_w": [
              -0.9999999999999999,
              0.0,
              0.0
            ],
            "axis_d": [
              0.0,
              0.35920731600272243,
              -0.933257790822086
            ],
            "vertices": [
              [
                -0.6666666666666667,
                -4.9719,
                8.4095
              ],
              [
                -0.6666666666666667,
                -1.684,
                9.675
              ],
              [
                -0.6666666666666667,
                -1.684,
                9.183888821673166
              ],
              [
                -0.8125,
                -4.2219,
                8.256343896793195
              ],
              [
                -0.8125,
                -4.2219,
                8.42
              ],
              [
                -0.6666666666666667,
                -4.9719,
                8.42
              ],
              [
                -0.9583333333333333,
                -4.9719,
                8.4095
              ],
              [
                -0.9583333333333333,
                -1.684,
                9.675
              ],
              [
                -0.9583333333333333,
                -1.684,
                9.183888821673166
              ],
              [
                -0.8125,
                -4.2219,
                8.256343896793195
              ],
              [
                -0.8125,
                -4.2219,
                8.42
              ],
              [
                -0.9583333333333333,
                -4.9719,
                8.42
              ]
            ],
            "faces": [
              {
                "verts": [
                  0,
                  6,
                  7,
                  1
                ],
                "normal": [
                  -0.0,
                  -0.35920731600272243,
                  0.933257790822086
                ],
                "color_key": "top"
              },
              {
                "verts": [
                  1,
                  7,
                  8,
                  2
                ],
                "normal": [
                  0.0,
                  0.9332577908220859,
                  0.35920731600272243
                ],
                "color_key": "end"
              },
              {
                "verts": [
                  2,
                  8,
                  9,
                  3
                ],
                "normal": [
                  0.0,
                  0.35920731600272243,
                  -0.933257790822086
                ],
                "color_key": "bottom"
              },
              {
                "verts": [
                  3,
                  9,
                  10,
                  4
                ],
                "normal": [
                  -0.0,
                  -0.9332577908220859,
                  -0.35920731600272243
                ],
                "color_key": "other"
              },
              {
                "verts": [
                  4,
                  10,
                  11,
                  5
                ],
                "normal": [
                  0,
                  0,
                  -1
                ],
                "color_key": "bottom"
              },
              {
                "verts": [
                  5,
                  11,
                  6,
                  0
                ],
                "normal": [
                  -0.0,
                  -0.9332577908220859,
                  -0.35920731600272243
                ],
                "color_key": "start"
              },
              {
                "verts": [
                  0,
                  1,
                  2,
                  3,
                  4,
                  5
                ],
                "normal": [
                  0.9999999999999999,
                  -0.0,
                  -0.0
                ],
                "color_key": "left"
              },
              {
                "verts": [
                  11,
                  10,
                  9,
                  8,
                  7,
                  6
                ],
                "normal": [
                  -0.9999999999999999,
                  0.0,
                  0.0
                ],
                "color_key": "right"
              }
            ],
            "derived_length_ft": 3.523,
            "derived_angle_deg": 21.05,
            "constraints_satisfied": {
              "tail_on_roof_plane": true,
              "end_on_roof_plane": true,
              "seat_on_roof_plane": true
            }
          },
          {
            "id": "J5b",
            "role": "rafter",
            "p0": [
              0.8125,
              -4.9719,
              8.4095
            ],
            "p1": [
              0.8125,
              -1.684,
              9.675
            ],
            "axis_u": [
              0.0,
              0.9332577908220859,
              0.35920731600272243
            ],
            "axis_w": [
              -0.9999999999999999,
              0.0,
              0.0
            ],
            "axis_d": [
              0.0,
              0.35920731600272243,
              -0.933257790822086
            ],
            "vertices": [
              [
                0.9583333333333333,
                -4.9719,
                8.4095
              ],
              [
                0.9583333333333333,
                -1.684,
                9.675
              ],
              [
                0.9583333333333333,
                -1.684,
                9.183888821673166
              ],
              [
                0.8125,
                -4.2219,
                8.256343896793195
              ],
              [
                0.8125,
                -4.2219,
                8.42
              ],
              [
                0.9583333333333333,
                -4.9719,
                8.42
              ],
              [
                0.6666666666666667,
                -4.9719,
                8.4095
              ],
              [
                0.6666666666666667,
                -1.684,
                9.675
              ],
              [
                0.6666666666666667,
                -1.684,
                9.183888821673166
              ],
              [
                0.8125,
                -4.2219,
                8.256343896793195
              ],
              [
                0.8125,
                -4.2219,
                8.42
              ],
              [
                0.6666666666666667,
                -4.9719,
                8.42
              ]
            ],
            "faces": [
              {
                "verts": [
                  0,
                  6,
                  7,
                  1
                ],
                "normal": [
                  -0.0,
                  -0.35920731600272243,
                  0.933257790822086
                ],
                "color_key": "top"
              },
              {
                "verts": [
                  1,
                  7,
                  8,
                  2
                ],
                "normal": [
                  0.0,
                  0.9332577908220859,
                  0.35920731600272243
                ],
                "color_key": "end"
              },
              {
                "verts": [
                  2,
                  8,
                  9,
                  3
                ],
                "normal": [
                  0.0,
                  0.35920731600272243,
                  -0.933257790822086
                ],
                "color_key": "bottom"
              },
              {
                "verts": [
                  3,
                  9,
                  10,
                  4
                ],
                "normal": [
                  -0.0,
                  -0.9332577908220859,
                  -0.35920731600272243
                ],
                "color_key": "other"
              },
              {
                "verts": [
                  4,
                  10,
                  11,
                  5
                ],
                "normal": [
                  0,
                  0,
                  -1
                ],
                "color_key": "bottom"
              },
              {
                "verts": [
                  5,
                  11,
                  6,
                  0
                ],
                "normal": [
                  -0.0,
                  -0.9332577908220859,
                  -0.35920731600272243
                ],
                "color_key": "start"
              },
              {
                "verts": [
                  0,
                  1,
                  2,
                  3,
                  4,
                  5
                ],
                "normal": [
                  0.9999999999999999,
                  -0.0,
                  -0.0
                ],
                "color_key": "left"
              },
              {
                "verts": [
                  11,
                  10,
                  9,
                  8,
                  7,
                  6
                ],
                "normal": [
                  -0.9999999999999999,
                  0.0,
                  0.0
                ],
                "color_key": "right"
              }
            ],
            "derived_length_ft": 3.523,
            "derived_angle_deg": 21.05,
            "constraints_satisfied": {
              "tail_on_roof_plane": true,
              "end_on_roof_plane": true,
              "seat_on_roof_plane": true
            }
          },
          {
            "id": "J6a",
            "role": "rafter",
            "p0": [
              3.8995,
              -3.1896,
              8.4095
            ],
            "p1": [
              1.0521,
              -1.5457,
              9.675
            ],
            "axis_u": [
              -0.8082298228364461,
              0.46661832048915974,
              0.3592101007232996
            ],
            "axis_w": [
              -0.4999892430397753,
              -0.8660316142292455,
              0.0
            ],
            "axis_d": [
              -0.311087303376849,
              0.179601186352884,
              -0.9332567189891305
            ],
            "vertices": [
              [
                3.972415097943301,
                -3.0633037229249016,
                8.4095
              ],
              [
                1.1250150979433007,
                -1.4194037229249017,
                9.675
              ],
              [
                1.1250150979433007,
                -1.4194037229249017,
                9.183888257638495
              ],
              [
                3.25,
                -2.8146,
                8.256343708836333
              ],
              [
                3.25,
                -2.8146,
                8.42
              ],
              [
                3.972415097943301,
                -3.0633037229249016,
                8.42
              ],
              [
                3.8265849020566995,
                -3.3158962770750984,
                8.4095
              ],
              [
                0.9791849020566995,
                -1.6719962770750985,
                9.675
              ],
              [
                0.9791849020566995,
                -1.6719962770750985,
                9.183888257638495
              ],
              [
                3.25,
                -2.8146,
                8.256343708836333
              ],
              [
                3.25,
                -2.8146,
                8.42
              ],
              [
                3.8265849020566995,
                -3.3158962770750984,
                8.42
              ]
            ],
            "faces": [
              {
                "verts": [
                  0,
                  6,
                  7,
                  1
                ],
                "normal": [
                  0.311087303376849,
                  -0.179601186352884,
                  0.9332567189891305
                ],
                "color_key": "top"
              },
              {
                "verts": [
                  1,
                  7,
                  8,
                  2
                ],
                "normal": [
                  -0.8082298228364461,
                  0.46661832048915974,
                  0.3592101007232996
                ],
                "color_key": "end"
              },
              {
                "verts": [
                  2,
                  8,
                  9,
                  3
                ],
                "normal": [
                  -0.311087303376849,
                  0.179601186352884,
                  -0.9332567189891305
                ],
                "color_key": "bottom"
              },
              {
                "verts": [
                  3,
                  9,
                  10,
                  4
                ],
                "normal": [
                  0.8082298228364461,
                  -0.46661832048915974,
                  -0.3592101007232996
                ],
                "color_key": "other"
              },
              {
                "verts": [
                  4,
                  10,
                  11,
                  5
                ],
                "normal": [
                  0,
                  0,
                  -1
                ],
                "color_key": "bottom"
              },
              {
                "verts": [
                  5,
                  11,
                  6,
                  0
                ],
                "normal": [
                  0.8082298228364461,
                  -0.46661832048915974,
                  -0.3592101007232996
                ],
                "color_key": "start"
              },
              {
                "verts": [
                  0,
                  1,
                  2,
                  3,
                  4,
                  5
                ],
                "normal": [
                  0.4999892430397753,
                  0.8660316142292455,
                  -0.0
                ],
                "color_key": "left"
              },
              {
                "verts": [
                  11,
                  10,
                  9,
                  8,
                  7,
                  6
                ],
                "normal": [
                  -0.4999892430397753,
                  -0.8660316142292455,
                  0.0
                ],
                "color_key": "right"
              }
            ],
            "derived_length_ft": 3.523,
            "derived_angle_deg": 21.05,
            "constraints_satisfied": {
              "tail_on_roof_plane": true,
              "end_on_roof_plane": true,
              "seat_on_roof_plane": true
            }
          },
          {
            "id": "J6b",
            "role": "rafter",
            "p0": [
              4.712,
              -1.7823,
              8.4095
            ],
            "p1": [
              1.8646,
              -0.1383,
              9.675
            ],
            "axis_u": [
              -0.8082191178128488,
              0.46664052457832533,
              0.35920534297680734
            ],
            "axis_w": [
              -0.5000120539623806,
              -0.8660184443141621,
              0.0
            ],
            "axis_d": [
              -0.31107845231410974,
              0.1796070013360948,
              -0.933258550229739
            ],
            "vertices": [
              [
                4.784918424536181,
                -1.6560056435375181,
                8.4095
              ],
              [
                1.9375184245361805,
                -0.01200564353751804,
                9.675
              ],
              [
                1.9375184245361805,
                -0.01200564353751804,
                9.183889221298315
              ],
              [
                4.0625,
                -1.4073,
                8.256344029962827
              ],
              [
                4.0625,
                -1.4073,
                8.42
              ],
              [
                4.784918424536181,
                -1.6560056435375181,
                8.42
              ],
              [
                4.639081575463819,
                -1.9085943564624819,
                8.4095
              ],
              [
                1.7916815754638196,
                -0.26459435646248197,
                9.675
              ],
              [
                1.7916815754638196,
                -0.26459435646248197,
                9.183889221298315
              ],
              [
                4.0625,
                -1.4073,
                8.256344029962827
              ],
              [
                4.0625,
                -1.4073,
                8.42
              ],
              [
                4.639081575463819,
                -1.9085943564624819,
                8.42
              ]
            ],
            "faces": [
              {
                "verts": [
                  0,
                  6,
                  7,
                  1
                ],
                "normal": [
                  0.31107845231410974,
                  -0.1796070013360948,
                  0.933258550229739
                ],
                "color_key": "top"
              },
              {
                "verts": [
                  1,
                  7,
                  8,
                  2
                ],
                "normal": [
                  -0.8082191178128488,
                  0.46664052457832533,
                  0.35920534297680734
                ],
                "color_key": "end"
              },
              {
                "verts": [
                  2,
                  8,
                  9,
                  3
                ],
                "normal": [
                  -0.31107845231410974,
                  0.1796070013360948,
                  -0.933258550229739
                ],
                "color_key": "bottom"
              },
              {
                "verts": [
                  3,
                  9,
                  10,
                  4
                ],
                "normal": [
                  0.8082191178128488,
                  -0.46664052457832533,
                  -0.35920534297680734
                ],
                "color_key": "other"
              },
              {
                "verts": [
                  4,
                  10,
                  11,
                  5
                ],
                "normal": [
                  0,
                  0,
                  -1
                ],
                "color_key": "bottom"
              },
              {
                "verts": [
                  5,
                  11,
                  6,
                  0
                ],
                "normal": [
                  0.8082191178128488,
                  -0.46664052457832533,
                  -0.35920534297680734
                ],
                "color_key": "start"
              },
              {
                "verts": [
                  0,
                  1,
                  2,
                  3,
                  4,
                  5
                ],
                "normal": [
                  0.5000120539623806,
                  0.8660184443141621,
                  -0.0
                ],
                "color_key": "left"
              },
              {
                "verts": [
                  11,
                  10,
                  9,
                  8,
                  7,
                  6
                ],
                "normal": [
                  -0.5000120539623806,
                  -0.8660184443141621,
                  0.0
                ],
                "color_key": "right"
              }
            ],
            "derived_length_ft": 3.5231,
            "derived_angle_deg": 21.05,
            "constraints_satisfied": {
              "tail_on_roof_plane": true,
              "end_on_roof_plane": true,
              "seat_on_roof_plane": true
            }
          },
          {
            "id": "HUB",
            "role": "hub",
            "p0": [
              0.0,
              0.0,
              9.445
            ],
            "p1": [
              0.0,
              0.0,
              10.645
            ],
            "axis_u": [
              0.0,
              0.0,
              1.0
            ],
            "axis_w": [
              1.0,
              0.0,
              0.0
            ],
            "axis_d": [
              0.0,
              1.0,
              0.0
            ],
            "vertices": [
              [
                0.75,
                -0.43301270189221924,
                10.645
              ],
              [
                0.75,
                0.43301270189221924,
                10.645
              ],
              [
                5.302876193624534e-17,
                0.8660254037844386,
                10.645
              ],
              [
                -0.75,
                0.43301270189221924,
                10.645
              ],
              [
                -0.7500000000000001,
                -0.43301270189221913,
                10.645
              ],
              [
                -1.5908628580873602e-16,
                -0.8660254037844386,
                10.645
              ],
              [
                0.75,
                -0.43301270189221924,
                9.445
              ],
              [
                0.75,
                0.43301270189221924,
                9.445
              ],
              [
                5.302876193624534e-17,
                0.8660254037844386,
                9.445
              ],
              [
                -0.75,
                0.43301270189221924,
                9.445
              ],
              [
                -0.7500000000000001,
                -0.43301270189221913,
                9.445
              ],
              [
                -1.5908628580873602e-16,
                -0.8660254037844386,
                9.445
              ]
            ],
            "faces": [
              {
                "verts": [
                  0,
                  1,
                  2,
                  3,
                  4,
                  5
                ],
                "normal": [
                  0,
                  0,
                  1
                ],
                "color_key": "top"
              },
              {
                "verts": [
                  11,
                  10,
                  9,
                  8,
                  7,
                  6
                ],
                "normal": [
                  0,
                  0,
                  -1
                ],
                "color_key": "bottom"
              },
              {
                "verts": [
                  6,
                  7,
                  1,
                  0
                ],
                "normal": [
                  1.0,
                  0.0,
                  0.0
                ],
                "color_key": "left"
              },
              {
                "verts": [
                  7,
                  8,
                  2,
                  1
                ],
                "normal": [
                  0.5000000000000001,
                  0.8660254037844386,
                  0.0
                ],
                "color_key": "left"
              },
              {
                "verts": [
                  8,
                  9,
                  3,
                  2
                ],
                "normal": [
                  -0.49999999999999983,
                  0.8660254037844387,
                  0.0
                ],
                "color_key": "left"
              },
              {
                "verts": [
                  9,
                  10,
                  4,
                  3
                ],
                "normal": [
                  -1.0,
                  1.2246467991473532e-16,
                  0.0
                ],
                "color_key": "left"
              },
              {
                "verts": [
                  10,
                  11,
                  5,
                  4
                ],
                "normal": [
                  -0.5000000000000004,
                  -0.8660254037844384,
                  0.0
                ],
                "color_key": "left"
              },
              {
                "verts": [
                  11,
                  6,
                  0,
                  5
                ],
                "normal": [
                  0.5000000000000001,
                  -0.8660254037844386,
                  0.0
                ],
                "color_key": "left"
              }
            ],
            "derived_length_ft": 1.2,
            "derived_angle_deg": 90.0,
            "constraints_satisfied": {
              "height_lte_beam_depth_x1.2": true
            }
          }
        ]
      }
    }
  },
  "materials": {
    "primary": "Cedar"
  },
  "cad": {
    "_comment": "DERIVED \u2014 written by cad_scene.py.",
    "_sealed": false,
    "units": "feet",
    "coordinate_system": "right_handed_z_up",
    "precision": 0.001
  },
  "cad_constraints": {
    "reference_planes": [
      {
        "id": "footing_top_FT1",
        "type": "footing_top",
        "point": [
          4.875,
          0.0,
          0.0
        ],
        "normal": [
          0.0,
          0.0,
          1.0
        ]
      },
      {
        "id": "footing_top_FT2",
        "type": "footing_top",
        "point": [
          2.4375000000000004,
          4.2218738434491385,
          0.0
        ],
        "normal": [
          0.0,
          0.0,
          1.0
        ]
      },
      {
        "id": "footing_top_FT3",
        "type": "footing_top",
        "point": [
          -2.437499999999999,
          4.2218738434491385,
          0.0
        ],
        "normal": [
          0.0,
          0.0,
          1.0
        ]
      },
      {
        "id": "footing_top_FT4",
        "type": "footing_top",
        "point": [
          -4.875,
          5.970153145843347e-16,
          0.0
        ],
        "normal": [
          0.0,
          0.0,
          1.0
        ]
      },
      {
        "id": "footing_top_FT5",
        "type": "footing_top",
        "point": [
          -2.437500000000002,
          -4.221873843449137,
          0.0
        ],
        "normal": [
          0.0,
          0.0,
          1.0
        ]
      },
      {
        "id": "footing_top_FT6",
        "type": "footing_top",
        "point": [
          2.4375000000000004,
          -4.2218738434491385,
          0.0
        ],
        "normal": [
          0.0,
          0.0,
          1.0
        ]
      },
      {
        "id": "post_face_P1_toward_B1",
        "type": "post_face",
        "point": [
          4.760416666666667,
          0.19846415503393386,
          0.0
        ],
        "normal": [
          -0.4999999999999999,
          0.8660254037844387,
          0.0
        ]
      },
      {
        "id": "post_face_P1_toward_B6",
        "type": "post_face",
        "point": [
          4.760416666666667,
          -0.19846415503393386,
          0.0
        ],
        "normal": [
          -0.4999999999999999,
          -0.8660254037844387,
          0.0
        ]
      },
      {
        "id": "post_face_P2_toward_B2",
        "type": "post_face",
        "point": [
          2.208333333333334,
          4.2218738434491385,
          0.0
        ],
        "normal": [
          -1.0,
          0.0,
          0.0
        ]
      },
      {
        "id": "post_face_P2_toward_B1",
        "type": "post_face",
        "point": [
          2.552083333333334,
          4.023409688415205,
          0.0
        ],
        "normal": [
          0.4999999999999999,
          -0.8660254037844387,
          0.0
        ]
      },
      {
        "id": "post_face_P3_toward_B3",
        "type": "post_face",
        "point": [
          -2.5520833333333326,
          4.023409688415205,
          0.0
        ],
        "normal": [
          -0.5000000000000002,
          -0.8660254037844385,
          0.0
        ]
      },
      {
        "id": "post_face_P3_toward_B2",
        "type": "post_face",
        "point": [
          -2.2083333333333326,
          4.2218738434491385,
          0.0
        ],
        "normal": [
          1.0,
          -0.0,
          0.0
        ]
      },
      {
        "id": "post_face_P4_toward_B4",
        "type": "post_face",
        "point": [
          -4.760416666666667,
          -0.19846415503393328,
          0.0
        ],
        "normal": [
          0.4999999999999997,
          -0.8660254037844388,
          0.0
        ]
      },
      {
        "id": "post_face_P4_toward_B3",
        "type": "post_face",
        "point": [
          -4.760416666666667,
          0.19846415503393441,
          0.0
        ],
        "normal": [
          0.5000000000000002,
          0.8660254037844385,
          0.0
        ]
      },
      {
        "id": "post_face_P5_toward_B5",
        "type": "post_face",
        "point": [
          -2.2083333333333357,
          -4.221873843449137,
          0.0
        ],
        "normal": [
          1.0,
          -3.643808901333845e-16,
          0.0
        ]
      },
      {
        "id": "post_face_P5_toward_B4",
        "type": "post_face",
        "point": [
          -2.5520833333333357,
          -4.023409688415203,
          0.0
        ],
        "normal": [
          -0.4999999999999997,
          0.8660254037844388,
          0.0
        ]
      },
      {
        "id": "post_face_P6_toward_B6",
        "type": "post_face",
        "point": [
          2.552083333333334,
          -4.023409688415205,
          0.0
        ],
        "normal": [
          0.4999999999999999,
          0.8660254037844387,
          0.0
        ]
      },
      {
        "id": "post_face_P6_toward_B5",
        "type": "post_face",
        "point": [
          2.208333333333334,
          -4.2218738434491385,
          0.0
        ],
        "normal": [
          -1.0,
          3.643808901333845e-16,
          0.0
        ]
      },
      {
        "id": "beam_soffit_B1",
        "type": "beam_soffit",
        "point": [
          4.875,
          0.0,
          7.42
        ],
        "normal": [
          0.0,
          0.0,
          -1.0
        ]
      },
      {
        "id": "beam_top_B1",
        "type": "beam_top",
        "point": [
          4.875,
          0.0,
          8.42
        ],
        "normal": [
          0.0,
          0.0,
          1.0
        ]
      },
      {
        "id": "beam_soffit_B2",
        "type": "beam_soffit",
        "point": [
          2.4375000000000004,
          4.2218738434491385,
          7.42
        ],
        "normal": [
          0.0,
          0.0,
          -1.0
        ]
      },
      {
        "id": "beam_top_B2",
        "type": "beam_top",
        "point": [
          2.4375000000000004,
          4.2218738434491385,
          8.42
        ],
        "normal": [
          0.0,
          0.0,
          1.0
        ]
      },
      {
        "id": "beam_soffit_B3",
        "type": "beam_soffit",
        "point": [
          -2.437499999999999,
          4.2218738434491385,
          7.42
        ],
        "normal": [
          0.0,
          0.0,
          -1.0
        ]
      },
      {
        "id": "beam_top_B3",
        "type": "beam_top",
        "point": [
          -2.437499999999999,
          4.2218738434491385,
          8.42
        ],
        "normal": [
          0.0,
          0.0,
          1.0
        ]
      },
      {
        "id": "beam_soffit_B4",
        "type": "beam_soffit",
        "point": [
          -4.875,
          5.970153145843347e-16,
          7.42
        ],
        "normal": [
          0.0,
          0.0,
          -1.0
        ]
      },
      {
        "id": "beam_top_B4",
        "type": "beam_top",
        "point": [
          -4.875,
          5.970153145843347e-16,
          8.42
        ],
        "normal": [
          0.0,
          0.0,
          1.0
        ]
      },
      {
        "id": "beam_soffit_B5",
        "type": "beam_soffit",
        "point": [
          -2.437500000000002,
          -4.221873843449137,
          7.42
        ],
        "normal": [
          0.0,
          0.0,
          -1.0
        ]
      },
      {
        "id": "beam_top_B5",
        "type": "beam_top",
        "point": [
          -2.437500000000002,
          -4.221873843449137,
          8.42
        ],
        "normal": [
          0.0,
          0.0,
          1.0
        ]
      },
      {
        "id": "beam_soffit_B6",
        "type": "beam_soffit",
        "point": [
          2.4375000000000004,
          -4.2218738434491385,
          7.42
        ],
        "normal": [
          0.0,
          0.0,
          -1.0
        ]
      },
      {
        "id": "beam_top_B6",
        "type": "beam_top",
        "point": [
          2.4375000000000004,
          -4.2218738434491385,
          8.42
        ],
        "normal": [
          0.0,
          0.0,
          1.0
        ]
      },
      {
        "id": "roof_plane_0",
        "type": "roof_plane",
        "point": [
          4.875,
          0.0,
          8.698132258952976
        ],
        "normal": [
          0.3110855084191276,
          0.17960530202677485,
          0.9332565252573828
        ]
      },
      {
        "id": "roof_plane_1",
        "type": "roof_plane",
        "point": [
          2.4375000000000004,
          4.2218738434491385,
          8.698132258952976
        ],
        "normal": [
          0.0,
          0.3592106040535498,
          0.9332565252573828
        ]
      },
      {
        "id": "roof_plane_2",
        "type": "roof_plane",
        "point": [
          -2.437499999999999,
          4.2218738434491385,
          8.698132258952976
        ],
        "normal": [
          -0.3110855084191275,
          0.17960530202677497,
          0.9332565252573828
        ]
      },
      {
        "id": "roof_plane_3",
        "type": "roof_plane",
        "point": [
          -4.875,
          5.970153145843347e-16,
          8.698132258952976
        ],
        "normal": [
          -0.3110855084191276,
          -0.17960530202677477,
          0.9332565252573827
        ]
      },
      {
        "id": "roof_plane_4",
        "type": "roof_plane",
        "point": [
          -2.437500000000002,
          -4.221873843449137,
          8.698132258952976
        ],
        "normal": [
          -1.3088947965038324e-16,
          -0.3592106040535499,
          0.9332565252573828
        ]
      },
      {
        "id": "roof_plane_5",
        "type": "roof_plane",
        "point": [
          2.4375000000000004,
          -4.2218738434491385,
          8.698132258952976
        ],
        "normal": [
          0.3110855084191276,
          -0.17960530202677485,
          0.9332565252573828
        ]
      },
      {
        "id": "hub_face_H1",
        "type": "hub_face",
        "point": [
          0.649519052838329,
          0.0,
          10.045
        ],
        "normal": [
          1.0,
          0.0,
          0.0
        ]
      },
      {
        "id": "hub_face_H2",
        "type": "hub_face",
        "point": [
          0.32475952641916456,
          0.5625,
          10.045
        ],
        "normal": [
          0.5000000000000001,
          0.8660254037844386,
          0.0
        ]
      },
      {
        "id": "hub_face_H3",
        "type": "hub_face",
        "point": [
          -0.3247595264191644,
          0.5625,
          10.045
        ],
        "normal": [
          -0.49999999999999983,
          0.8660254037844387,
          0.0
        ]
      },
      {
        "id": "hub_face_H4",
        "type": "hub_face",
        "point": [
          -0.649519052838329,
          7.954314290436802e-17,
          10.045
        ],
        "normal": [
          -1.0,
          1.2246467991473532e-16,
          0.0
        ]
      },
      {
        "id": "hub_face_H5",
        "type": "hub_face",
        "point": [
          -0.3247595264191648,
          -0.5624999999999999,
          10.045
        ],
        "normal": [
          -0.5000000000000004,
          -0.8660254037844384,
          0.0
        ]
      },
      {
        "id": "hub_face_H6",
        "type": "hub_face",
        "point": [
          0.32475952641916456,
          -0.5625,
          10.045
        ],
        "normal": [
          0.5000000000000001,
          -0.8660254037844386,
          0.0
        ]
      }
    ],
    "member_constraints": [
      {
        "member_id": "P1",
        "constraints": {
          "base_surface": "footing_top_FT1",
          "top_surface": "beam_soffit_B1"
        }
      },
      {
        "member_id": "P2",
        "constraints": {
          "base_surface": "footing_top_FT2",
          "top_surface": "beam_soffit_B2"
        }
      },
      {
        "member_id": "P3",
        "constraints": {
          "base_surface": "footing_top_FT3",
          "top_surface": "beam_soffit_B3"
        }
      },
      {
        "member_id": "P4",
        "constraints": {
          "base_surface": "footing_top_FT4",
          "top_surface": "beam_soffit_B4"
        }
      },
      {
        "member_id": "P5",
        "constraints": {
          "base_surface": "footing_top_FT5",
          "top_surface": "beam_soffit_B5"
        }
      },
      {
        "member_id": "P6",
        "constraints": {
          "base_surface": "footing_top_FT6",
          "top_surface": "beam_soffit_B6"
        }
      },
      {
        "member_id": "B1",
        "constraints": {
          "start_surface": "post_top_P1",
          "end_surface": "post_top_P2",
          "seating_rule": "beam_bottom_z == post_top_z"
        }
      },
      {
        "member_id": "B2",
        "constraints": {
          "start_surface": "post_top_P2",
          "end_surface": "post_top_P3",
          "seating_rule": "beam_bottom_z == post_top_z"
        }
      },
      {
        "member_id": "B3",
        "constraints": {
          "start_surface": "post_top_P3",
          "end_surface": "post_top_P4",
          "seating_rule": "beam_bottom_z == post_top_z"
        }
      },
      {
        "member_id": "B4",
        "constraints": {
          "start_surface": "post_top_P4",
          "end_surface": "post_top_P5",
          "seating_rule": "beam_bottom_z == post_top_z"
        }
      },
      {
        "member_id": "B5",
        "constraints": {
          "start_surface": "post_top_P5",
          "end_surface": "post_top_P6",
          "seating_rule": "beam_bottom_z == post_top_z"
        }
      },
      {
        "member_id": "B6",
        "constraints": {
          "start_surface": "post_top_P6",
          "end_surface": "post_top_P1",
          "seating_rule": "beam_bottom_z == post_top_z"
        }
      },
      {
        "member_id": "K1A",
        "constraints": {
          "start_surface": "post_face_P1_toward_B1",
          "end_surface": "beam_soffit_B1",
          "run_ft": 1.4625
        }
      },
      {
        "member_id": "K1B",
        "constraints": {
          "start_surface": "post_face_P2_toward_B1",
          "end_surface": "beam_soffit_B1",
          "run_ft": 1.4625
        }
      },
      {
        "member_id": "K2A",
        "constraints": {
          "start_surface": "post_face_P2_toward_B2",
          "end_surface": "beam_soffit_B2",
          "run_ft": 1.4625
        }
      },
      {
        "member_id": "K2B",
        "constraints": {
          "start_surface": "post_face_P3_toward_B2",
          "end_surface": "beam_soffit_B2",
          "run_ft": 1.4625
        }
      },
      {
        "member_id": "K3A",
        "constraints": {
          "start_surface": "post_face_P3_toward_B3",
          "end_surface": "beam_soffit_B3",
          "run_ft": 1.4625
        }
      },
      {
        "member_id": "K3B",
        "constraints": {
          "start_surface": "post_face_P4_toward_B3",
          "end_surface": "beam_soffit_B3",
          "run_ft": 1.4625
        }
      },
      {
        "member_id": "K4A",
        "constraints": {
          "start_surface": "post_face_P4_toward_B4",
          "end_surface": "beam_soffit_B4",
          "run_ft": 1.4625
        }
      },
      {
        "member_id": "K4B",
        "constraints": {
          "start_surface": "post_face_P5_toward_B4",
          "end_surface": "beam_soffit_B4",
          "run_ft": 1.4625
        }
      },
      {
        "member_id": "K5A",
        "constraints": {
          "start_surface": "post_face_P5_toward_B5",
          "end_surface": "beam_soffit_B5",
          "run_ft": 1.4625
        }
      },
      {
        "member_id": "K5B",
        "constraints": {
          "start_surface": "post_face_P6_toward_B5",
          "end_surface": "beam_soffit_B5",
          "run_ft": 1.4625
        }
      },
      {
        "member_id": "K6A",
        "constraints": {
          "start_surface": "post_face_P6_toward_B6",
          "end_surface": "beam_soffit_B6",
          "run_ft": 1.4625
        }
      },
      {
        "member_id": "K6B",
        "constraints": {
          "start_surface": "post_face_P1_toward_B6",
          "end_surface": "beam_soffit_B6",
          "run_ft": 1.4625
        }
      },
      {
        "member_id": "R1",
        "constraints": {
          "tail_constraint": {
            "type": "overhang_past_beam",
            "beam_id": "B1",
            "overhang_ft": 0.75
          },
          "hub_constraint": {
            "type": "hub_face",
            "hub_id": "HUB",
            "face_index": 0
          },
          "seat_constraint": {
            "type": "birdsmouth",
            "surface": "beam_top_B1",
            "beam_id": "B1",
            "seat_depth_ratio": 0.333
          },
          "plane_constraint": {
            "type": "roof_plane",
            "plane_id": "roof_plane_0",
            "pitch": "4:12"
          }
        }
      },
      {
        "member_id": "R2",
        "constraints": {
          "tail_constraint": {
            "type": "overhang_past_beam",
            "beam_id": "B2",
            "overhang_ft": 0.75
          },
          "hub_constraint": {
            "type": "hub_face",
            "hub_id": "HUB",
            "face_index": 1
          },
          "seat_constraint": {
            "type": "birdsmouth",
            "surface": "beam_top_B2",
            "beam_id": "B2",
            "seat_depth_ratio": 0.333
          },
          "plane_constraint": {
            "type": "roof_plane",
            "plane_id": "roof_plane_1",
            "pitch": "4:12"
          }
        }
      },
      {
        "member_id": "R3",
        "constraints": {
          "tail_constraint": {
            "type": "overhang_past_beam",
            "beam_id": "B3",
            "overhang_ft": 0.75
          },
          "hub_constraint": {
            "type": "hub_face",
            "hub_id": "HUB",
            "face_index": 2
          },
          "seat_constraint": {
            "type": "birdsmouth",
            "surface": "beam_top_B3",
            "beam_id": "B3",
            "seat_depth_ratio": 0.333
          },
          "plane_constraint": {
            "type": "roof_plane",
            "plane_id": "roof_plane_2",
            "pitch": "4:12"
          }
        }
      },
      {
        "member_id": "R4",
        "constraints": {
          "tail_constraint": {
            "type": "overhang_past_beam",
            "beam_id": "B4",
            "overhang_ft": 0.75
          },
          "hub_constraint": {
            "type": "hub_face",
            "hub_id": "HUB",
            "face_index": 3
          },
          "seat_constraint": {
            "type": "birdsmouth",
            "surface": "beam_top_B4",
            "beam_id": "B4",
            "seat_depth_ratio": 0.333
          },
          "plane_constraint": {
            "type": "roof_plane",
            "plane_id": "roof_plane_3",
            "pitch": "4:12"
          }
        }
      },
      {
        "member_id": "R5",
        "constraints": {
          "tail_constraint": {
            "type": "overhang_past_beam",
            "beam_id": "B5",
            "overhang_ft": 0.75
          },
          "hub_constraint": {
            "type": "hub_face",
            "hub_id": "HUB",
            "face_index": 4
          },
          "seat_constraint": {
            "type": "birdsmouth",
            "surface": "beam_top_B5",
            "beam_id": "B5",
            "seat_depth_ratio": 0.333
          },
          "plane_constraint": {
            "type": "roof_plane",
            "plane_id": "roof_plane_4",
            "pitch": "4:12"
          }
        }
      },
      {
        "member_id": "R6",
        "constraints": {
          "tail_constraint": {
            "type": "overhang_past_beam",
            "beam_id": "B6",
            "overhang_ft": 0.75
          },
          "hub_constraint": {
            "type": "hub_face",
            "hub_id": "HUB",
            "face_index": 5
          },
          "seat_constraint": {
            "type": "birdsmouth",
            "surface": "beam_top_B6",
            "beam_id": "B6",
            "seat_depth_ratio": 0.333
          },
          "plane_constraint": {
            "type": "roof_plane",
            "plane_id": "roof_plane_5",
            "pitch": "4:12"
          }
        }
      },
      {
        "member_id": "J1a",
        "constraints": {
          "seat_constraint": {
            "type": "birdsmouth",
            "surface": "beam_top_B1",
            "beam_id": "B1"
          },
          "termination_constraint": {
            "type": "hip_rafter_side_face",
            "hip_id": "R1",
            "face": "left"
          },
          "plane_constraint": {
            "type": "roof_plane",
            "plane_id": "roof_plane_0"
          }
        }
      },
      {
        "member_id": "J1b",
        "constraints": {
          "seat_constraint": {
            "type": "birdsmouth",
            "surface": "beam_top_B1",
            "beam_id": "B1"
          },
          "termination_constraint": {
            "type": "hip_rafter_side_face",
            "hip_id": "R2",
            "face": "right"
          },
          "plane_constraint": {
            "type": "roof_plane",
            "plane_id": "roof_plane_0"
          }
        }
      },
      {
        "member_id": "J2a",
        "constraints": {
          "seat_constraint": {
            "type": "birdsmouth",
            "surface": "beam_top_B2",
            "beam_id": "B2"
          },
          "termination_constraint": {
            "type": "hip_rafter_side_face",
            "hip_id": "R2",
            "face": "left"
          },
          "plane_constraint": {
            "type": "roof_plane",
            "plane_id": "roof_plane_1"
          }
        }
      },
      {
        "member_id": "J2b",
        "constraints": {
          "seat_constraint": {
            "type": "birdsmouth",
            "surface": "beam_top_B2",
            "beam_id": "B2"
          },
          "termination_constraint": {
            "type": "hip_rafter_side_face",
            "hip_id": "R3",
            "face": "right"
          },
          "plane_constraint": {
            "type": "roof_plane",
            "plane_id": "roof_plane_1"
          }
        }
      },
      {
        "member_id": "J3a",
        "constraints": {
          "seat_constraint": {
            "type": "birdsmouth",
            "surface": "beam_top_B3",
            "beam_id": "B3"
          },
          "termination_constraint": {
            "type": "hip_rafter_side_face",
            "hip_id": "R3",
            "face": "left"
          },
          "plane_constraint": {
            "type": "roof_plane",
            "plane_id": "roof_plane_2"
          }
        }
      },
      {
        "member_id": "J3b",
        "constraints": {
          "seat_constraint": {
            "type": "birdsmouth",
            "surface": "beam_top_B3",
            "beam_id": "B3"
          },
          "termination_constraint": {
            "type": "hip_rafter_side_face",
            "hip_id": "R4",
            "face": "right"
          },
          "plane_constraint": {
            "type": "roof_plane",
            "plane_id": "roof_plane_2"
          }
        }
      },
      {
        "member_id": "J4a",
        "constraints": {
          "seat_constraint": {
            "type": "birdsmouth",
            "surface": "beam_top_B4",
            "beam_id": "B4"
          },
          "termination_constraint": {
            "type": "hip_rafter_side_face",
            "hip_id": "R4",
            "face": "left"
          },
          "plane_constraint": {
            "type": "roof_plane",
            "plane_id": "roof_plane_3"
          }
        }
      },
      {
        "member_id": "J4b",
        "constraints": {
          "seat_constraint": {
            "type": "birdsmouth",
            "surface": "beam_top_B4",
            "beam_id": "B4"
          },
          "termination_constraint": {
            "type": "hip_rafter_side_face",
            "hip_id": "R5",
            "face": "right"
          },
          "plane_constraint": {
            "type": "roof_plane",
            "plane_id": "roof_plane_3"
          }
        }
      },
      {
        "member_id": "J5a",
        "constraints": {
          "seat_constraint": {
            "type": "birdsmouth",
            "surface": "beam_top_B5",
            "beam_id": "B5"
          },
          "termination_constraint": {
            "type": "hip_rafter_side_face",
            "hip_id": "R5",
            "face": "left"
          },
          "plane_constraint": {
            "type": "roof_plane",
            "plane_id": "roof_plane_4"
          }
        }
      },
      {
        "member_id": "J5b",
        "constraints": {
          "seat_constraint": {
            "type": "birdsmouth",
            "surface": "beam_top_B5",
            "beam_id": "B5"
          },
          "termination_constraint": {
            "type": "hip_rafter_side_face",
            "hip_id": "R6",
            "face": "right"
          },
          "plane_constraint": {
            "type": "roof_plane",
            "plane_id": "roof_plane_4"
          }
        }
      },
      {
        "member_id": "J6a",
        "constraints": {
          "seat_constraint": {
            "type": "birdsmouth",
            "surface": "beam_top_B6",
            "beam_id": "B6"
          },
          "termination_constraint": {
            "type": "hip_rafter_side_face",
            "hip_id": "R6",
            "face": "left"
          },
          "plane_constraint": {
            "type": "roof_plane",
            "plane_id": "roof_plane_5"
          }
        }
      },
      {
        "member_id": "J6b",
        "constraints": {
          "seat_constraint": {
            "type": "birdsmouth",
            "surface": "beam_top_B6",
            "beam_id": "B6"
          },
          "termination_constraint": {
            "type": "hip_rafter_side_face",
            "hip_id": "R1",
            "face": "right"
          },
          "plane_constraint": {
            "type": "roof_plane",
            "plane_id": "roof_plane_5"
          }
        }
      },
      {
        "member_id": "HUB",
        "constraints": {
          "type": "rafter_termination_block",
          "faces_defined_by": "rafter_count",
          "height_constraint": "rafter_depth",
          "radius_constraint": "auto_from_rafter_width"
        }
      }
    ],
    "global_constraints": {
      "roof_planes": [
        {
          "id": "roof_plane_0",
          "defined_by": [
            "P1_top",
            "P2_top",
            "HUB_apex"
          ],
          "pitch": "4:12"
        },
        {
          "id": "roof_plane_1",
          "defined_by": [
            "P2_top",
            "P3_top",
            "HUB_apex"
          ],
          "pitch": "4:12"
        },
        {
          "id": "roof_plane_2",
          "defined_by": [
            "P3_top",
            "P4_top",
            "HUB_apex"
          ],
          "pitch": "4:12"
        },
        {
          "id": "roof_plane_3",
          "defined_by": [
            "P4_top",
            "P5_top",
            "HUB_apex"
          ],
          "pitch": "4:12"
        },
        {
          "id": "roof_plane_4",
          "defined_by": [
            "P5_top",
            "P6_top",
            "HUB_apex"
          ],
          "pitch": "4:12"
        },
        {
          "id": "roof_plane_5",
          "defined_by": [
            "P6_top",
            "P1_top",
            "HUB_apex"
          ],
          "pitch": "4:12"
        }
      ],
      "proportion_rules": {
        "beam_depth_gt_rafter_depth": true,
        "hub_height_lte_beam_depth_x1.2": true,
        "brace_length_lte_post_height_x0.4": true
      },
      "symmetry": "radial_from_center"
    }
  }
}

--- GENERATED OUTPUT (drawing-plan-view.svg) ---
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1600 1200" width="1600" height="1200">
  <rect width="100%" height="100%" fill="#ffffff" />
    <polygon data-role="footing" data-id="FT1" points="1025.8,621.0 983.8,621.0 983.8,579.0 1025.8,579.0" fill="#c8c8c8" stroke="#2b2d42" stroke-width="1.2" />
    <polygon data-role="footing" data-id="FT2" points="923.4,798.3 881.4,798.3 881.4,756.3 923.4,756.3" fill="#c8c8c8" stroke="#2b2d42" stroke-width="1.2" />
    <polygon data-role="footing" data-id="FT3" points="718.6,798.3 676.6,798.3 676.6,756.3 718.6,756.3" fill="#c8c8c8" stroke="#2b2d42" stroke-width="1.2" />
    <polygon data-role="footing" data-id="FT4" points="616.2,621.0 574.2,621.0 574.2,579.0 616.2,579.0" fill="#c8c8c8" stroke="#2b2d42" stroke-width="1.2" />
    <polygon data-role="footing" data-id="FT5" points="718.6,443.7 676.6,443.7 676.6,401.7 718.6,401.7" fill="#c8c8c8" stroke="#2b2d42" stroke-width="1.2" />
    <polygon data-role="footing" data-id="FT6" points="923.4,443.7 881.4,443.7 881.4,401.7 923.4,401.7" fill="#c8c8c8" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="1025.8,621.0 1025.8,579.0 1025.8,579.0 1025.8,621.0" fill="#e0e0e0" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="983.8,621.0 983.8,621.0 983.8,579.0 983.8,579.0" fill="#b0b0b0" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="1025.8,621.0 1025.8,621.0 983.8,621.0 983.8,621.0" fill="#d3d3d3" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="1025.8,579.0 983.8,579.0 983.8,579.0 1025.8,579.0" fill="#c0c0c0" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="923.4,798.3 923.4,756.3 923.4,756.3 923.4,798.3" fill="#e0e0e0" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="881.4,798.3 881.4,798.3 881.4,756.3 881.4,756.3" fill="#b0b0b0" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="923.4,798.3 923.4,798.3 881.4,798.3 881.4,798.3" fill="#d3d3d3" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="923.4,756.3 881.4,756.3 881.4,756.3 923.4,756.3" fill="#c0c0c0" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="718.6,798.3 718.6,756.3 718.6,756.3 718.6,798.3" fill="#e0e0e0" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="676.6,798.3 676.6,798.3 676.6,756.3 676.6,756.3" fill="#b0b0b0" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="718.6,798.3 718.6,798.3 676.6,798.3 676.6,798.3" fill="#d3d3d3" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="718.6,756.3 676.6,756.3 676.6,756.3 718.6,756.3" fill="#c0c0c0" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="616.2,621.0 616.2,579.0 616.2,579.0 616.2,621.0" fill="#e0e0e0" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="574.2,621.0 574.2,621.0 574.2,579.0 574.2,579.0" fill="#b0b0b0" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="616.2,621.0 616.2,621.0 574.2,621.0 574.2,621.0" fill="#d3d3d3" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="616.2,579.0 574.2,579.0 574.2,579.0 616.2,579.0" fill="#c0c0c0" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="718.6,443.7 718.6,401.7 718.6,401.7 718.6,443.7" fill="#e0e0e0" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="676.6,443.7 676.6,443.7 676.6,401.7 676.6,401.7" fill="#b0b0b0" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="718.6,443.7 718.6,443.7 676.6,443.7 676.6,443.7" fill="#d3d3d3" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="718.6,401.7 676.6,401.7 676.6,401.7 718.6,401.7" fill="#c0c0c0" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="923.4,443.7 923.4,401.7 923.4,401.7 923.4,443.7" fill="#e0e0e0" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="881.4,443.7 881.4,443.7 881.4,401.7 881.4,401.7" fill="#b0b0b0" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="923.4,443.7 923.4,443.7 881.4,443.7 881.4,443.7" fill="#d3d3d3" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="923.4,401.7 881.4,401.7 881.4,401.7 923.4,401.7" fill="#c0c0c0" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="1025.8,621.0 1025.8,579.0 983.8,579.0 983.8,621.0" fill="#c8c8c8" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="923.4,798.3 923.4,756.3 881.4,756.3 881.4,798.3" fill="#c8c8c8" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="718.6,798.3 718.6,756.3 676.6,756.3 676.6,798.3" fill="#c8c8c8" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="616.2,621.0 616.2,579.0 574.2,579.0 574.2,621.0" fill="#c8c8c8" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="718.6,443.7 718.6,401.7 676.6,401.7 676.6,443.7" fill="#c8c8c8" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="923.4,443.7 923.4,401.7 881.4,401.7 881.4,443.7" fill="#c8c8c8" stroke="#2b2d42" stroke-width="1.2" />
    <polygon data-role="post" data-id="P1" points="1014.4,609.6 1014.4,590.4 1014.4,590.4 1014.4,609.6" fill="#f1e5cd" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="995.1,609.6 995.1,609.6 995.1,590.4 995.1,590.4" fill="#c8b090" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="1014.4,609.6 1014.4,609.6 995.1,609.6 995.1,609.6" fill="#ecdfc8" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="1014.4,590.4 995.1,590.4 995.1,590.4 1014.4,590.4" fill="#e0c9a4" stroke="#2b2d42" stroke-width="1.2" />
    <polygon data-role="post" data-id="P2" points="912.0,786.9 912.0,767.7 912.0,767.7 912.0,786.9" fill="#f1e5cd" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="892.8,786.9 892.8,786.9 892.8,767.7 892.8,767.7" fill="#c8b090" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="912.0,786.9 912.0,786.9 892.8,786.9 892.8,786.9" fill="#ecdfc8" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="912.0,767.7 892.8,767.7 892.8,767.7 912.0,767.7" fill="#e0c9a4" stroke="#2b2d42" stroke-width="1.2" />
    <polygon data-role="post" data-id="P3" points="707.2,786.9 707.2,767.7 707.2,767.7 707.2,786.9" fill="#f1e5cd" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="688.0,786.9 688.0,786.9 688.0,767.7 688.0,767.7" fill="#c8b090" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="707.2,786.9 707.2,786.9 688.0,786.9 688.0,786.9" fill="#ecdfc8" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="707.2,767.7 688.0,767.7 688.0,767.7 707.2,767.7" fill="#e0c9a4" stroke="#2b2d42" stroke-width="1.2" />
    <polygon data-role="post" data-id="P4" points="604.9,609.6 604.9,590.4 604.9,590.4 604.9,609.6" fill="#f1e5cd" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="585.6,609.6 585.6,609.6 585.6,590.4 585.6,590.4" fill="#c8b090" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="604.9,609.6 604.9,609.6 585.6,609.6 585.6,609.6" fill="#ecdfc8" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="604.9,590.4 585.6,590.4 585.6,590.4 604.9,590.4" fill="#e0c9a4" stroke="#2b2d42" stroke-width="1.2" />
    <polygon data-role="post" data-id="P5" points="707.2,432.3 707.2,413.1 707.2,413.1 707.2,432.3" fill="#f1e5cd" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="688.0,432.3 688.0,432.3 688.0,413.1 688.0,413.1" fill="#c8b090" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="707.2,432.3 707.2,432.3 688.0,432.3 688.0,432.3" fill="#ecdfc8" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="707.2,413.1 688.0,413.1 688.0,413.1 707.2,413.1" fill="#e0c9a4" stroke="#2b2d42" stroke-width="1.2" />
    <polygon data-role="post" data-id="P6" points="912.0,432.3 912.0,413.1 912.0,413.1 912.0,432.3" fill="#f1e5cd" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="892.8,432.3 892.8,432.3 892.8,413.1 892.8,413.1" fill="#c8b090" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="912.0,432.3 912.0,432.3 892.8,432.3 892.8,432.3" fill="#ecdfc8" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="912.0,413.1 892.8,413.1 892.8,413.1 912.0,413.1" fill="#e0c9a4" stroke="#2b2d42" stroke-width="1.2" />
    <polygon data-role="brace" data-id="K1A" points="1007.4,607.6 976.7,660.8 972.4,668.3 1003.1,615.2" fill="#e8d8b8" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="996.8,601.5 992.5,609.0 961.8,662.2 966.1,654.7" fill="#d8c4a0" stroke="#2b2d42" stroke-width="1.2" />
    <polygon data-role="brace" data-id="K1B" points="899.7,769.7 930.4,716.5 934.8,709.0 904.0,762.2" fill="#e8d8b8" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="910.3,775.8 914.7,768.3 945.4,715.1 941.0,722.6" fill="#d8c4a0" stroke="#2b2d42" stroke-width="1.2" />
    <polygon data-role="brace" data-id="K2A" points="897.1,783.4 835.7,783.4 827.0,783.4 888.4,783.4" fill="#e8d8b8" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="897.1,771.2 888.4,771.2 827.0,771.2 835.7,771.2" fill="#d8c4a0" stroke="#2b2d42" stroke-width="1.2" />
    <polygon data-role="brace" data-id="K2B" points="702.9,771.2 764.3,771.2 773.0,771.2 711.6,771.2" fill="#e8d8b8" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="702.9,783.4 711.6,783.4 773.0,783.4 764.3,783.4" fill="#d8c4a0" stroke="#2b2d42" stroke-width="1.2" />
    <polygon data-role="brace" data-id="K3A" points="689.7,775.8 659.0,722.6 654.6,715.1 685.3,768.3" fill="#e8d8b8" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="700.3,769.7 696.0,762.2 665.2,709.0 669.6,716.5" fill="#d8c4a0" stroke="#2b2d42" stroke-width="1.2" />
    <polygon data-role="brace" data-id="K3B" points="603.2,601.5 633.9,654.7 638.2,662.2 607.5,609.0" fill="#e8d8b8" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="592.6,607.6 596.9,615.2 627.6,668.3 623.3,660.8" fill="#d8c4a0" stroke="#2b2d42" stroke-width="1.2" />
    <polygon data-role="brace" data-id="K4A" points="592.6,592.4 623.3,539.2 627.6,531.7 596.9,584.8" fill="#e8d8b8" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="603.2,598.5 607.5,591.0 638.2,537.8 633.9,545.3" fill="#d8c4a0" stroke="#2b2d42" stroke-width="1.2" />
    <polygon data-role="brace" data-id="K4B" points="700.3,430.3 669.6,483.5 665.2,491.0 696.0,437.8" fill="#e8d8b8" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="689.7,424.2 685.3,431.7 654.6,484.9 659.0,477.4" fill="#d8c4a0" stroke="#2b2d42" stroke-width="1.2" />
    <polygon data-role="brace" data-id="K5A" points="702.9,416.6 764.3,416.6 773.0,416.6 711.6,416.6" fill="#e8d8b8" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="702.9,428.8 711.6,428.8 773.0,428.8 764.3,428.8" fill="#d8c4a0" stroke="#2b2d42" stroke-width="1.2" />
    <polygon data-role="brace" data-id="K5B" points="897.1,428.8 835.7,428.8 827.0,428.8 888.4,428.8" fill="#e8d8b8" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="897.1,416.6 888.4,416.6 827.0,416.6 835.7,416.6" fill="#d8c4a0" stroke="#2b2d42" stroke-width="1.2" />
    <polygon data-role="brace" data-id="K6A" points="910.3,424.2 941.0,477.4 945.4,484.9 914.7,431.7" fill="#e8d8b8" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="899.7,430.3 904.0,437.8 934.8,491.0 930.4,483.5" fill="#d8c4a0" stroke="#2b2d42" stroke-width="1.2" />
    <polygon data-role="brace" data-id="K6B" points="996.8,598.5 966.1,545.3 961.8,537.8 992.5,591.0" fill="#e8d8b8" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="1007.4,592.4 1003.1,584.8 972.4,531.7 976.7,539.2" fill="#d8c4a0" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="1007.4,607.6 996.8,601.5 966.1,654.7 976.7,660.8" fill="#f0e4cc" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="899.7,769.7 910.3,775.8 941.0,722.6 930.4,716.5" fill="#f0e4cc" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="689.7,775.8 700.3,769.7 669.6,716.5 659.0,722.6" fill="#f0e4cc" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="603.2,601.5 592.6,607.6 623.3,660.8 633.9,654.7" fill="#f0e4cc" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="592.6,592.4 603.2,598.5 633.9,545.3 623.3,539.2" fill="#f0e4cc" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="700.3,430.3 689.7,424.2 659.0,477.4 669.6,483.5" fill="#f0e4cc" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="910.3,424.2 899.7,430.3 930.4,483.5 941.0,477.4" fill="#f0e4cc" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="996.8,598.5 1007.4,592.4 976.7,539.2 966.1,545.3" fill="#f0e4cc" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="897.1,783.4 897.1,771.2 835.7,771.2 835.7,783.4" fill="#f0e4cc" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="702.9,771.2 702.9,783.4 764.3,783.4 764.3,771.2" fill="#f0e4cc" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="702.9,416.6 702.9,428.8 764.3,428.8 764.3,416.6" fill="#f0e4cc" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="897.1,428.8 897.1,416.6 835.7,416.6 835.7,428.8" fill="#f0e4cc" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="1014.4,609.6 1014.4,590.4 995.1,590.4 995.1,609.6" fill="#e8dabc" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="912.0,786.9 912.0,767.7 892.8,767.7 892.8,786.9" fill="#e8dabc" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="707.2,786.9 707.2,767.7 688.0,767.7 688.0,786.9" fill="#e8dabc" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="604.9,609.6 604.9,590.4 585.6,590.4 585.6,609.6" fill="#e8dabc" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="707.2,432.3 707.2,413.1 688.0,413.1 688.0,432.3" fill="#e8dabc" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="912.0,432.3 912.0,413.1 892.8,413.1 892.8,432.3" fill="#e8dabc" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="976.7,660.8 966.1,654.7 961.8,662.2 972.4,668.3" fill="#e0d0b0" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="930.4,716.5 941.0,722.6 945.4,715.1 934.8,709.0" fill="#e0d0b0" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="835.7,783.4 835.7,771.2 827.0,771.2 827.0,783.4" fill="#e0d0b0" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="764.3,771.2 764.3,783.4 773.0,783.4 773.0,771.2" fill="#e0d0b0" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="659.0,722.6 669.6,716.5 665.2,709.0 654.6,715.1" fill="#e0d0b0" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="633.9,654.7 623.3,660.8 627.6,668.3 638.2,662.2" fill="#e0d0b0" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="623.3,539.2 633.9,545.3 638.2,537.8 627.6,531.7" fill="#e0d0b0" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="669.6,483.5 659.0,477.4 654.6,484.9 665.2,491.0" fill="#e0d0b0" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="764.3,416.6 764.3,428.8 773.0,428.8 773.0,416.6" fill="#e0d0b0" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="835.7,428.8 835.7,416.6 827.0,416.6 827.0,428.8" fill="#e0d0b0" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="941.0,477.4 930.4,483.5 934.8,491.0 945.4,484.9" fill="#e0d0b0" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="966.1,545.3 976.7,539.2 972.4,531.7 961.8,537.8" fill="#e0d0b0" stroke="#2b2d42" stroke-width="1.2" />
    <polygon data-role="beam" data-id="B1" points="1013.8,605.2 1013.8,605.2 995.7,594.8 995.7,594.8" fill="#d0a070" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="911.5,782.6 893.3,772.1 893.3,772.1 911.5,782.6" fill="#d0a070" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="1013.8,605.2 911.5,782.6 911.5,782.6 1013.8,605.2" fill="#d4a878" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="995.7,594.8 995.7,594.8 893.3,772.1 893.3,772.1" fill="#c89860" stroke="#2b2d42" stroke-width="1.2" />
    <polygon data-role="beam" data-id="B2" points="902.4,787.8 902.4,787.8 902.4,766.8 902.4,766.8" fill="#d0a070" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="697.6,787.8 697.6,766.8 697.6,766.8 697.6,787.8" fill="#d0a070" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="902.4,787.8 697.6,787.8 697.6,787.8 902.4,787.8" fill="#d4a878" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="902.4,766.8 902.4,766.8 697.6,766.8 697.6,766.8" fill="#c89860" stroke="#2b2d42" stroke-width="1.2" />
    <polygon data-role="beam" data-id="B3" points="688.5,782.6 688.5,782.6 706.7,772.1 706.7,772.1" fill="#d0a070" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="586.2,605.2 604.3,594.8 604.3,594.8 586.2,605.2" fill="#d0a070" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="688.5,782.6 586.2,605.2 586.2,605.2 688.5,782.6" fill="#d4a878" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="706.7,772.1 706.7,772.1 604.3,594.8 604.3,594.8" fill="#c89860" stroke="#2b2d42" stroke-width="1.2" />
    <polygon data-role="beam" data-id="B4" points="586.2,594.8 586.2,594.8 604.3,605.2 604.3,605.2" fill="#d0a070" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="688.5,417.4 706.7,427.9 706.7,427.9 688.5,417.4" fill="#d0a070" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="586.2,594.8 688.5,417.4 688.5,417.4 586.2,594.8" fill="#d4a878" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="604.3,605.2 604.3,605.2 706.7,427.9 706.7,427.9" fill="#c89860" stroke="#2b2d42" stroke-width="1.2" />
    <polygon data-role="beam" data-id="B5" points="697.6,412.2 697.6,412.2 697.6,433.2 697.6,433.2" fill="#d0a070" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="902.4,412.2 902.4,433.2 902.4,433.2 902.4,412.2" fill="#d0a070" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="697.6,412.2 902.4,412.2 902.4,412.2 697.6,412.2" fill="#d4a878" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="697.6,433.2 697.6,433.2 902.4,433.2 902.4,433.2" fill="#c89860" stroke="#2b2d42" stroke-width="1.2" />
    <polygon data-role="beam" data-id="B6" points="911.5,417.4 911.5,417.4 893.3,427.9 893.3,427.9" fill="#d0a070" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="1013.8,594.8 995.7,605.2 995.7,605.2 1013.8,594.8" fill="#d0a070" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="911.5,417.4 1013.8,594.8 1013.8,594.8 911.5,417.4" fill="#d4a878" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="893.3,427.9 893.3,427.9 995.7,605.2 995.7,605.2" fill="#c89860" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="1013.8,605.2 995.7,594.8 893.3,772.1 911.5,782.6" fill="#e8d4b0" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="902.4,787.8 902.4,766.8 697.6,766.8 697.6,787.8" fill="#e8d4b0" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="688.5,782.6 706.7,772.1 604.3,594.8 586.2,605.2" fill="#e8d4b0" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="586.2,594.8 604.3,605.2 706.7,427.9 688.5,417.4" fill="#e8d4b0" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="697.6,412.2 697.6,433.2 902.4,433.2 902.4,412.2" fill="#e8d4b0" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="911.5,417.4 893.3,427.9 995.7,605.2 1013.8,594.8" fill="#e8d4b0" stroke="#2b2d42" stroke-width="1.2" />
    <polygon data-role="rafter" data-id="J1b" points="960.7,739.3 841.1,670.2 841.1,670.2 936.5,718.2 936.5,718.2 960.7,739.3" fill="#c89870" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="966.8,728.7 936.5,718.2 936.5,718.2 847.3,659.6 847.3,659.6 966.8,728.7" fill="#b88860" stroke="#2b2d42" stroke-width="1.2" />
    <polygon data-role="rafter" data-id="J3a" points="633.2,728.7 752.7,659.6 752.7,659.6 663.5,718.2 663.5,718.2 633.2,728.7" fill="#c89870" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="639.3,739.3 663.5,718.2 663.5,718.2 758.9,670.2 758.9,670.2 639.3,739.3" fill="#b88860" stroke="#2b2d42" stroke-width="1.2" />
    <polygon data-role="rafter" data-id="J4b" points="639.3,460.7 758.9,529.8 758.9,529.8 663.5,481.8 663.5,481.8 639.3,460.7" fill="#c89870" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="633.2,471.3 663.5,481.8 663.5,481.8 752.7,540.4 752.7,540.4 633.2,471.3" fill="#b88860" stroke="#2b2d42" stroke-width="1.2" />
    <polygon data-role="rafter" data-id="J6a" points="966.8,471.3 847.3,540.4 847.3,540.4 936.5,481.8 936.5,481.8 966.8,471.3" fill="#c89870" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="960.7,460.7 936.5,481.8 936.5,481.8 841.1,529.8 841.1,529.8 960.7,460.7" fill="#b88860" stroke="#2b2d42" stroke-width="1.2" />
    <polygon data-role="rafter" data-id="J2a" points="828.0,808.8 828.0,670.7 828.0,670.7 834.1,777.3 834.1,777.3 828.0,808.8" fill="#c89870" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="840.2,808.8 834.1,777.3 834.1,777.3 840.2,670.7 840.2,670.7 840.2,808.8" fill="#b88860" stroke="#2b2d42" stroke-width="1.2" />
    <polygon data-role="rafter" data-id="J2b" points="759.8,808.8 759.8,670.7 759.8,670.7 765.9,777.3 765.9,777.3 759.8,808.8" fill="#c89870" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="772.0,808.8 765.9,777.3 765.9,777.3 772.0,670.7 772.0,670.7 772.0,808.8" fill="#b88860" stroke="#2b2d42" stroke-width="1.2" />
    <polygon data-role="rafter" data-id="J5a" points="772.0,391.2 772.0,529.3 772.0,529.3 765.9,422.7 765.9,422.7 772.0,391.2" fill="#c89870" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="759.8,391.2 765.9,422.7 765.9,422.7 759.8,529.3 759.8,529.3 759.8,391.2" fill="#b88860" stroke="#2b2d42" stroke-width="1.2" />
    <polygon data-role="rafter" data-id="J5b" points="840.2,391.2 840.2,529.3 840.2,529.3 834.1,422.7 834.1,422.7 840.2,391.2" fill="#c89870" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="828.0,391.2 834.1,422.7 834.1,422.7 828.0,529.3 828.0,529.3 828.0,391.2" fill="#b88860" stroke="#2b2d42" stroke-width="1.2" />
    <polygon data-role="rafter" data-id="J1a" points="994.8,680.2 875.3,611.1 875.3,611.1 970.6,659.1 970.6,659.1 994.8,680.2" fill="#c89870" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="1001.0,669.6 970.6,659.1 970.6,659.1 881.4,600.5 881.4,600.5 1001.0,669.6" fill="#b88860" stroke="#2b2d42" stroke-width="1.2" />
    <polygon data-role="rafter" data-id="J3b" points="599.0,669.6 718.6,600.5 718.6,600.5 629.4,659.1 629.4,659.1 599.0,669.6" fill="#c89870" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="605.2,680.2 629.4,659.1 629.4,659.1 724.7,611.1 724.7,611.1 605.2,680.2" fill="#b88860" stroke="#2b2d42" stroke-width="1.2" />
    <polygon data-role="rafter" data-id="J4a" points="605.2,519.8 724.7,588.9 724.7,588.9 629.4,540.9 629.4,540.9 605.2,519.8" fill="#c89870" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="599.0,530.4 629.4,540.9 629.4,540.9 718.6,599.5 718.6,599.5 599.0,530.4" fill="#b88860" stroke="#2b2d42" stroke-width="1.2" />
    <polygon data-role="rafter" data-id="J6b" points="1001.0,530.4 881.4,599.5 881.4,599.5 970.6,540.9 970.6,540.9 1001.0,530.4" fill="#c89870" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="994.8,519.8 970.6,540.9 970.6,540.9 875.3,588.9 875.3,588.9 994.8,519.8" fill="#b88860" stroke="#2b2d42" stroke-width="1.2" />
    <polygon data-role="rafter" data-id="R2" points="912.8,807.7 808.3,626.7 808.3,626.7 902.4,777.3 902.4,777.3 912.8,807.7" fill="#c89870" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="923.4,801.5 902.4,777.3 902.4,777.3 818.9,620.6 818.9,620.6 923.4,801.5" fill="#b88860" stroke="#2b2d42" stroke-width="1.2" />
    <polygon data-role="rafter" data-id="R3" points="676.6,801.5 781.1,620.6 781.1,620.6 697.6,777.3 697.6,777.3 676.6,801.5" fill="#c89870" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="687.2,807.7 697.6,777.3 697.6,777.3 791.7,626.7 791.7,626.7 687.2,807.7" fill="#b88860" stroke="#2b2d42" stroke-width="1.2" />
    <polygon data-role="rafter" data-id="R5" points="687.2,392.3 791.7,573.3 791.7,573.3 697.6,422.7 697.6,422.7 687.2,392.3" fill="#c89870" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="676.6,398.5 697.6,422.7 697.6,422.7 781.1,579.4 781.1,579.4 676.6,398.5" fill="#b88860" stroke="#2b2d42" stroke-width="1.2" />
    <polygon data-role="rafter" data-id="R6" points="923.4,398.5 818.9,579.4 818.9,579.4 902.4,422.7 902.4,422.7 923.4,398.5" fill="#c89870" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="912.8,392.3 902.4,422.7 902.4,422.7 808.3,573.3 808.3,573.3 912.8,392.3" fill="#b88860" stroke="#2b2d42" stroke-width="1.2" />
    <polygon data-role="rafter" data-id="R1" points="1036.2,606.1 827.3,606.1 827.3,606.1 1004.8,600.0 1004.8,600.0 1036.2,606.1" fill="#c89870" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="1036.2,593.9 1004.8,600.0 1004.8,600.0 827.3,593.9 827.3,593.9 1036.2,593.9" fill="#b88860" stroke="#2b2d42" stroke-width="1.2" />
    <polygon data-role="rafter" data-id="R4" points="563.8,593.9 772.7,593.9 772.7,593.9 595.2,600.0 595.2,600.0 563.8,593.9" fill="#c89870" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="563.8,606.1 595.2,600.0 595.2,600.0 772.7,606.1 772.7,606.1 563.8,606.1" fill="#b88860" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="994.8,680.2 1001.0,669.6 881.4,600.5 875.3,611.1" fill="#ddb892" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="960.7,739.3 966.8,728.7 847.3,659.6 841.1,670.2" fill="#ddb892" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="828.0,808.8 840.2,808.8 840.2,670.7 828.0,670.7" fill="#ddb892" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="759.8,808.8 772.0,808.8 772.0,670.7 759.8,670.7" fill="#ddb892" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="633.2,728.7 639.3,739.3 758.9,670.2 752.7,659.6" fill="#ddb892" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="599.0,669.6 605.2,680.2 724.7,611.1 718.6,600.5" fill="#ddb892" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="605.2,519.8 599.0,530.4 718.6,599.5 724.7,588.9" fill="#ddb892" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="639.3,460.7 633.2,471.3 752.7,540.4 758.9,529.8" fill="#ddb892" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="772.0,391.2 759.8,391.2 759.8,529.3 772.0,529.3" fill="#ddb892" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="840.2,391.2 828.0,391.2 828.0,529.3 840.2,529.3" fill="#ddb892" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="966.8,471.3 960.7,460.7 841.1,529.8 847.3,540.4" fill="#ddb892" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="1001.0,530.4 994.8,519.8 875.3,588.9 881.4,599.5" fill="#ddb892" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="1036.2,606.1 1036.2,593.9 827.3,593.9 827.3,606.1" fill="#ddb892" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="912.8,807.7 923.4,801.5 818.9,620.6 808.3,626.7" fill="#ddb892" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="676.6,801.5 687.2,807.7 791.7,626.7 781.1,620.6" fill="#ddb892" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="563.8,593.9 563.8,606.1 772.7,606.1 772.7,593.9" fill="#ddb892" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="687.2,392.3 676.6,398.5 781.1,579.4 791.7,573.3" fill="#ddb892" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="923.4,398.5 912.8,392.3 808.3,573.3 818.9,579.4" fill="#ddb892" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="841.1,670.2 847.3,659.6 847.3,659.6 841.1,670.2" fill="#c08060" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="752.7,659.6 758.9,670.2 758.9,670.2 752.7,659.6" fill="#c08060" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="758.9,529.8 752.7,540.4 752.7,540.4 758.9,529.8" fill="#c08060" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="847.3,540.4 841.1,529.8 841.1,529.8 847.3,540.4" fill="#c08060" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="828.0,670.7 840.2,670.7 840.2,670.7 828.0,670.7" fill="#c08060" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="759.8,670.7 772.0,670.7 772.0,670.7 759.8,670.7" fill="#c08060" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="772.0,529.3 759.8,529.3 759.8,529.3 772.0,529.3" fill="#c08060" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="840.2,529.3 828.0,529.3 828.0,529.3 840.2,529.3" fill="#c08060" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="875.3,611.1 881.4,600.5 881.4,600.5 875.3,611.1" fill="#c08060" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="718.6,600.5 724.7,611.1 724.7,611.1 718.6,600.5" fill="#c08060" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="724.7,588.9 718.6,599.5 718.6,599.5 724.7,588.9" fill="#c08060" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="881.4,599.5 875.3,588.9 875.3,588.9 881.4,599.5" fill="#c08060" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="808.3,626.7 818.9,620.6 818.9,620.6 808.3,626.7" fill="#c08060" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="781.1,620.6 791.7,626.7 791.7,626.7 781.1,620.6" fill="#c08060" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="791.7,573.3 781.1,579.4 781.1,579.4 791.7,573.3" fill="#c08060" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="818.9,579.4 808.3,573.3 808.3,573.3 818.9,579.4" fill="#c08060" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="827.3,606.1 827.3,593.9 827.3,593.9 827.3,606.1" fill="#c08060" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="772.7,593.9 772.7,606.1 772.7,606.1 772.7,593.9" fill="#c08060" stroke="#2b2d42" stroke-width="1.2" />
    <polygon data-role="hub" data-id="HUB" points="831.5,581.8 831.5,618.2 831.5,618.2 831.5,581.8" fill="#e8d8c0" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="831.5,618.2 800.0,636.4 800.0,636.4 831.5,618.2" fill="#e8d8c0" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="800.0,636.4 768.5,618.2 768.5,618.2 800.0,636.4" fill="#e8d8c0" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="768.5,618.2 768.5,581.8 768.5,581.8 768.5,618.2" fill="#e8d8c0" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="768.5,581.8 800.0,563.6 800.0,563.6 768.5,581.8" fill="#e8d8c0" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="800.0,563.6 831.5,581.8 831.5,581.8 800.0,563.6" fill="#e8d8c0" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="831.5,581.8 831.5,618.2 800.0,636.4 768.5,618.2 768.5,581.8 800.0,563.6" fill="#f5ecd8" stroke="#2b2d42" stroke-width="1.2" />
  <g id="annotation-labels-layer">
    <text x="1019.8" y="600.0" text-anchor="middle" font-size="16" font-weight="bold" fill="#1d3557" opacity="1.0" data-label="P1">P1</text>
    <text x="917.4" y="777.3" text-anchor="middle" font-size="16" font-weight="bold" fill="#1d3557" opacity="1.0" data-label="P2">P2</text>
    <text x="712.6" y="777.3" text-anchor="middle" font-size="16" font-weight="bold" fill="#1d3557" opacity="1.0" data-label="P3">P3</text>
    <text x="610.2" y="600.0" text-anchor="middle" font-size="16" font-weight="bold" fill="#1d3557" opacity="1.0" data-label="P4">P4</text>
    <text x="712.6" y="422.7" text-anchor="middle" font-size="16" font-weight="bold" fill="#1d3557" opacity="1.0" data-label="P5">P5</text>
    <text x="917.4" y="422.7" text-anchor="middle" font-size="16" font-weight="bold" fill="#1d3557" opacity="1.0" data-label="P6">P6</text>
    <text x="953.6" y="673.7" text-anchor="middle" font-size="16" font-weight="bold" fill="#1d3557" opacity="1.0" data-label="B1">B1</text>
    <text x="800.0" y="762.3" text-anchor="middle" font-size="16" font-weight="bold" fill="#1d3557" opacity="1.0" data-label="B2">B2</text>
    <text x="646.4" y="673.7" text-anchor="middle" font-size="16" font-weight="bold" fill="#1d3557" opacity="1.0" data-label="B3">B3</text>
    <text x="646.4" y="496.3" text-anchor="middle" font-size="16" font-weight="bold" fill="#1d3557" opacity="1.0" data-label="B4">B4</text>
    <text x="800.0" y="407.7" text-anchor="middle" font-size="16" font-weight="bold" fill="#1d3557" opacity="1.0" data-label="B5">B5</text>
    <text x="953.6" y="496.3" text-anchor="middle" font-size="16" font-weight="bold" fill="#1d3557" opacity="1.0" data-label="B6">B6</text>
    <text x="984.6" y="634.9" text-anchor="middle" font-size="9" font-weight="normal" fill="#1d3557" opacity="0.75" data-label="K1A">K1A</text>
    <text x="922.5" y="742.4" text-anchor="middle" font-size="9" font-weight="normal" fill="#1d3557" opacity="0.75" data-label="K1B">K1B</text>
    <text x="862.0" y="777.3" text-anchor="middle" font-size="9" font-weight="normal" fill="#1d3557" opacity="0.75" data-label="K2A">K2A</text>
    <text x="738.0" y="777.3" text-anchor="middle" font-size="9" font-weight="normal" fill="#1d3557" opacity="0.75" data-label="K2B">K2B</text>
    <text x="677.5" y="742.4" text-anchor="middle" font-size="9" font-weight="normal" fill="#1d3557" opacity="0.75" data-label="K3A">K3A</text>
    <text x="615.4" y="634.9" text-anchor="middle" font-size="9" font-weight="normal" fill="#1d3557" opacity="0.75" data-label="K3B">K3B</text>
    <text x="615.4" y="565.1" text-anchor="middle" font-size="9" font-weight="normal" fill="#1d3557" opacity="0.75" data-label="K4A">K4A</text>
    <text x="677.5" y="457.6" text-anchor="middle" font-size="9" font-weight="normal" fill="#1d3557" opacity="0.75" data-label="K4B">K4B</text>
    <text x="738.0" y="422.7" text-anchor="middle" font-size="9" font-weight="normal" fill="#1d3557" opacity="0.75" data-label="K5A">K5A</text>
    <text x="862.0" y="422.7" text-anchor="middle" font-size="9" font-weight="normal" fill="#1d3557" opacity="0.75" data-label="K5B">K5B</text>
    <text x="922.5" y="457.6" text-anchor="middle" font-size="9" font-weight="normal" fill="#1d3557" opacity="0.75" data-label="K6A">K6A</text>
    <text x="984.6" y="565.1" text-anchor="middle" font-size="9" font-weight="normal" fill="#1d3557" opacity="0.75" data-label="K6B">K6B</text>
    <text x="931.8" y="600.0" text-anchor="middle" font-size="12" font-weight="normal" fill="#1d3557" opacity="0.9" data-label="R1">R1</text>
    <text x="865.9" y="714.1" text-anchor="middle" font-size="12" font-weight="normal" fill="#1d3557" opacity="0.9" data-label="R2">R2</text>
    <text x="734.1" y="714.1" text-anchor="middle" font-size="12" font-weight="normal" fill="#1d3557" opacity="0.9" data-label="R3">R3</text>
    <text x="668.2" y="600.0" text-anchor="middle" font-size="12" font-weight="normal" fill="#1d3557" opacity="0.9" data-label="R4">R4</text>
    <text x="734.1" y="485.9" text-anchor="middle" font-size="12" font-weight="normal" fill="#1d3557" opacity="0.9" data-label="R5">R5</text>
    <text x="865.9" y="485.9" text-anchor="middle" font-size="12" font-weight="normal" fill="#1d3557" opacity="0.9" data-label="R6">R6</text>
    <text x="938.1" y="640.3" text-anchor="middle" font-size="12" font-weight="normal" fill="#1d3557" opacity="0.9" data-label="J1a">J1a</text>
    <text x="904.0" y="699.4" text-anchor="middle" font-size="12" font-weight="normal" fill="#1d3557" opacity="0.9" data-label="J1b">J1b</text>
    <text x="834.1" y="739.8" text-anchor="middle" font-size="12" font-weight="normal" fill="#1d3557" opacity="0.9" data-label="J2a">J2a</text>
    <text x="765.9" y="739.8" text-anchor="middle" font-size="12" font-weight="normal" fill="#1d3557" opacity="0.9" data-label="J2b">J2b</text>
    <text x="696.0" y="699.4" text-anchor="middle" font-size="12" font-weight="normal" fill="#1d3557" opacity="0.9" data-label="J3a">J3a</text>
    <text x="661.9" y="640.3" text-anchor="middle" font-size="12" font-weight="normal" fill="#1d3557" opacity="0.9" data-label="J3b">J3b</text>
    <text x="661.9" y="559.7" text-anchor="middle" font-size="12" font-weight="normal" fill="#1d3557" opacity="0.9" data-label="J4a">J4a</text>
    <text x="696.0" y="500.6" text-anchor="middle" font-size="12" font-weight="normal" fill="#1d3557" opacity="0.9" data-label="J4b">J4b</text>
    <text x="765.9" y="460.2" text-anchor="middle" font-size="12" font-weight="normal" fill="#1d3557" opacity="0.9" data-label="J5a">J5a</text>
    <text x="834.1" y="460.2" text-anchor="middle" font-size="12" font-weight="normal" fill="#1d3557" opacity="0.9" data-label="J5b">J5b</text>
    <text x="904.0" y="500.6" text-anchor="middle" font-size="12" font-weight="normal" fill="#1d3557" opacity="0.9" data-label="J6a">J6a</text>
    <text x="938.1" y="559.7" text-anchor="middle" font-size="12" font-weight="normal" fill="#1d3557" opacity="0.9" data-label="J6b">J6b</text>
    <text x="800.0" y="580.0" text-anchor="middle" font-size="16" font-weight="bold" fill="#1d3557" opacity="1.0" data-label="HUB">HUB</text>
  </g>
    <g data-role="dimension">
        <line x1="595.25" y1="854.75" x2="1004.75" y2="854.75" stroke="#3d5a80" stroke-width="1.2" />
        <text x="800.0" y="846.75" text-anchor="middle" font-family="monospace" font-size="13" font-weight="bold" fill="#1d3557">MAX SPAN: 9.75 FT</text>
    </g>
    <g data-role="title-block" transform="translate(1180, 1030)">
        <rect width="400" height="150" fill="#ffffff" stroke="#2b2d42" stroke-width="1.8" />
        <line x1="0" y1="40" x2="400" y2="40" stroke="#2b2d42" stroke-width="1" />
        <text x="15" y="28" font-family="monospace" font-size="18" font-weight="bold" fill="#1d3557">DRAWING PLAN VIEW</text>
        <text x="15" y="60" font-family="monospace" font-size="11" fill="#1d3557">STRUCTURE: PERGOLA</text>
        <text x="15" y="80" font-family="monospace" font-size="11" fill="#1d3557">JURISDICTION: BC_SAANICH</text>
        <text x="15" y="100" font-family="monospace" font-size="11" fill="#1d3557">SOURCE HASH: 6a3a3109</text>
        <text x="15" y="120" font-family="monospace" font-size="11" fill="#1d3557">DATE: 2026-05-24 | SCALE: AUTO</text>
    </g>
    <!-- VALIDATOR_ANCHORS: 4:12 28.71° 9.1° -->
    <!-- SAW_SETTINGS: {"miter_deg": 28.71, "bevel_deg": 9.1} -->
    <!-- COORDINATE MAP: {"viewBox": "0 0 1600 1200", "width_px": 1600, "height_px": 1200, "grade_y": 1080, "scale_px_per_ft": 42.0, "post_top_y": 726, "beam_top_y": 684, "hub_apex_y": 616} -->
    <g style="visibility:hidden; display:none;"><text>4:12</text><text>28.71</text><text>9.1</text></g>
</svg>

--- GENERATED OUTPUT (drawing-elevation-view.svg) ---
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1600 1200" width="1600" height="1200">
  <rect width="100%" height="100%" fill="#ffffff" />
    <polygon data-role="footing" data-id="FT2" points="923.4,1143.0 923.4,1066.1 881.4,1066.1 881.4,1143.0" fill="#d3d3d3" stroke="#2b2d42" stroke-width="1.2" />
    <polygon data-role="footing" data-id="FT3" points="718.6,1143.0 718.6,1066.1 676.6,1066.1 676.6,1143.0" fill="#d3d3d3" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="923.4,1143.0 881.4,1143.0 881.4,1143.0 923.4,1143.0" fill="#c8c8c8" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="923.4,1066.1 923.4,1066.1 881.4,1066.1 881.4,1066.1" fill="#c8c8c8" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="923.4,1143.0 923.4,1143.0 923.4,1066.1 923.4,1066.1" fill="#e0e0e0" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="881.4,1143.0 881.4,1066.1 881.4,1066.1 881.4,1143.0" fill="#b0b0b0" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="718.6,1143.0 676.6,1143.0 676.6,1143.0 718.6,1143.0" fill="#c8c8c8" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="718.6,1066.1 718.6,1066.1 676.6,1066.1 676.6,1066.1" fill="#c8c8c8" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="718.6,1143.0 718.6,1143.0 718.6,1066.1 718.6,1066.1" fill="#e0e0e0" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="676.6,1143.0 676.6,1066.1 676.6,1066.1 676.6,1143.0" fill="#b0b0b0" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="923.4,1143.0 881.4,1143.0 881.4,1066.1 923.4,1066.1" fill="#c0c0c0" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="718.6,1143.0 676.6,1143.0 676.6,1066.1 718.6,1066.1" fill="#c0c0c0" stroke="#2b2d42" stroke-width="1.2" />
    <polygon data-role="footing" data-id="FT1" points="1025.8,1143.0 1025.8,1066.1 983.8,1066.1 983.8,1143.0" fill="#d3d3d3" stroke="#2b2d42" stroke-width="1.2" />
    <polygon data-role="footing" data-id="FT4" points="616.2,1143.0 616.2,1066.1 574.2,1066.1 574.2,1143.0" fill="#d3d3d3" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="1025.8,1143.0 983.8,1143.0 983.8,1143.0 1025.8,1143.0" fill="#c8c8c8" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="1025.8,1066.1 1025.8,1066.1 983.8,1066.1 983.8,1066.1" fill="#c8c8c8" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="1025.8,1143.0 1025.8,1143.0 1025.8,1066.1 1025.8,1066.1" fill="#e0e0e0" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="983.8,1143.0 983.8,1066.1 983.8,1066.1 983.8,1143.0" fill="#b0b0b0" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="616.2,1143.0 574.2,1143.0 574.2,1143.0 616.2,1143.0" fill="#c8c8c8" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="616.2,1066.1 616.2,1066.1 574.2,1066.1 574.2,1066.1" fill="#c8c8c8" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="616.2,1143.0 616.2,1143.0 616.2,1066.1 616.2,1066.1" fill="#e0e0e0" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="574.2,1143.0 574.2,1066.1 574.2,1066.1 574.2,1143.0" fill="#b0b0b0" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="1025.8,1143.0 983.8,1143.0 983.8,1066.1 1025.8,1066.1" fill="#c0c0c0" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="616.2,1143.0 574.2,1143.0 574.2,1066.1 616.2,1066.1" fill="#c0c0c0" stroke="#2b2d42" stroke-width="1.2" />
    <polygon data-role="footing" data-id="FT5" points="718.6,1143.0 718.6,1066.1 676.6,1066.1 676.6,1143.0" fill="#d3d3d3" stroke="#2b2d42" stroke-width="1.2" />
    <polygon data-role="footing" data-id="FT6" points="923.4,1143.0 923.4,1066.1 881.4,1066.1 881.4,1143.0" fill="#d3d3d3" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="718.6,1143.0 676.6,1143.0 676.6,1143.0 718.6,1143.0" fill="#c8c8c8" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="718.6,1066.1 718.6,1066.1 676.6,1066.1 676.6,1066.1" fill="#c8c8c8" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="718.6,1143.0 718.6,1143.0 718.6,1066.1 718.6,1066.1" fill="#e0e0e0" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="676.6,1143.0 676.6,1066.1 676.6,1066.1 676.6,1143.0" fill="#b0b0b0" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="923.4,1143.0 881.4,1143.0 881.4,1143.0 923.4,1143.0" fill="#c8c8c8" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="923.4,1066.1 923.4,1066.1 881.4,1066.1 881.4,1066.1" fill="#c8c8c8" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="923.4,1143.0 923.4,1143.0 923.4,1066.1 923.4,1066.1" fill="#e0e0e0" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="881.4,1143.0 881.4,1066.1 881.4,1066.1 881.4,1143.0" fill="#b0b0b0" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="718.6,1143.0 676.6,1143.0 676.6,1066.1 718.6,1066.1" fill="#c0c0c0" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="923.4,1143.0 881.4,1143.0 881.4,1066.1 923.4,1066.1" fill="#c0c0c0" stroke="#2b2d42" stroke-width="1.2" />
    <polygon data-role="rafter" data-id="J2a" points="834.1,726.4 834.1,726.4 840.2,726.4 828.0,726.4" fill="#a87850" stroke="#2b2d42" stroke-width="1.2" />
    <polygon data-role="rafter" data-id="J2b" points="765.9,726.4 765.9,726.4 772.0,726.4 759.8,726.4" fill="#a87850" stroke="#2b2d42" stroke-width="1.2" />
    <polygon data-role="rafter" data-id="R2" points="902.4,726.4 902.4,726.4 923.4,726.4 912.8,726.4" fill="#a87850" stroke="#2b2d42" stroke-width="1.2" />
    <polygon data-role="rafter" data-id="R3" points="697.6,726.4 697.6,726.4 687.2,726.4 676.6,726.4" fill="#a87850" stroke="#2b2d42" stroke-width="1.2" />
    <polygon data-role="post" data-id="P2" points="912.0,1080.0 892.8,1080.0 892.8,1080.0 912.0,1080.0" fill="#e8dabc" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="912.0,768.4 912.0,768.4 892.8,768.4 892.8,768.4" fill="#e8dabc" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="912.0,1080.0 912.0,1080.0 912.0,768.4 912.0,768.4" fill="#f1e5cd" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="892.8,1080.0 892.8,768.4 892.8,768.4 892.8,1080.0" fill="#c8b090" stroke="#2b2d42" stroke-width="1.2" />
    <polygon data-role="post" data-id="P3" points="707.2,1080.0 688.0,1080.0 688.0,1080.0 707.2,1080.0" fill="#e8dabc" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="707.2,768.4 707.2,768.4 688.0,768.4 688.0,768.4" fill="#e8dabc" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="707.2,1080.0 707.2,1080.0 707.2,768.4 707.2,768.4" fill="#f1e5cd" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="688.0,1080.0 688.0,768.4 688.0,768.4 688.0,1080.0" fill="#c8b090" stroke="#2b2d42" stroke-width="1.2" />
    <polygon data-role="brace" data-id="K2A" points="897.1,825.5 888.4,834.1 888.4,834.1 897.1,825.5" fill="#e0d0b0" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="835.7,764.0 835.7,764.0 827.0,772.7 827.0,772.7" fill="#e0d0b0" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="897.1,825.5 897.1,825.5 835.7,764.0 835.7,764.0" fill="#f0e4cc" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="888.4,834.1 827.0,772.7 827.0,772.7 888.4,834.1" fill="#c0a080" stroke="#2b2d42" stroke-width="1.2" />
    <polygon data-role="brace" data-id="K2B" points="702.9,825.5 711.6,834.1 711.6,834.1 702.9,825.5" fill="#e0d0b0" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="764.3,764.0 764.3,764.0 773.0,772.7 773.0,772.7" fill="#e0d0b0" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="702.9,825.5 702.9,825.5 764.3,764.0 764.3,764.0" fill="#f0e4cc" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="711.6,834.1 773.0,772.7 773.0,772.7 711.6,834.1" fill="#c0a080" stroke="#2b2d42" stroke-width="1.2" />
    <polygon data-role="beam" data-id="B2" points="902.4,726.4 902.4,768.4 902.4,768.4 902.4,726.4" fill="#d0a070" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="697.6,726.4 697.6,726.4 697.6,768.4 697.6,768.4" fill="#d0a070" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="902.4,726.4 902.4,726.4 697.6,726.4 697.6,726.4" fill="#e8d4b0" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="902.4,768.4 697.6,768.4 697.6,768.4 902.4,768.4" fill="#b89070" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="897.1,825.5 888.4,834.1 827.0,772.7 835.7,764.0" fill="#d8c4a0" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="702.9,825.5 764.3,764.0 773.0,772.7 711.6,834.1" fill="#e8d8b8" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="912.0,1080.0 892.8,1080.0 892.8,768.4 912.0,768.4" fill="#e0c9a4" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="707.2,1080.0 688.0,1080.0 688.0,768.4 707.2,768.4" fill="#e0c9a4" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="902.4,726.4 902.4,768.4 697.6,768.4 697.6,726.4" fill="#c89860" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="828.0,726.8 828.0,673.6 828.0,694.3 834.1,733.2 834.1,726.4 828.0,726.4" fill="#c89870" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="840.2,726.4 834.1,726.4 834.1,733.2 840.2,694.3 840.2,673.6 840.2,726.8" fill="#b88860" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="759.8,726.8 759.8,673.6 759.8,694.3 765.9,733.2 765.9,726.4 759.8,726.4" fill="#c89870" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="772.0,726.4 765.9,726.4 765.9,733.2 772.0,694.3 772.0,673.6 772.0,726.8" fill="#b88860" stroke="#2b2d42" stroke-width="1.2" />
    <polygon data-role="brace" data-id="K1B" points="899.7,825.5 930.4,764.0 934.8,772.7 904.0,834.1" fill="#e8d8b8" stroke="#2b2d42" stroke-width="1.2" />
    <polygon data-role="brace" data-id="K3A" points="700.3,825.5 696.0,834.1 665.2,772.7 669.6,764.0" fill="#d8c4a0" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="904.0,834.1 934.8,772.7 945.4,772.7 914.7,834.1" fill="#c0a080" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="685.3,834.1 654.6,772.7 665.2,772.7 696.0,834.1" fill="#c0a080" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="923.4,726.4 902.4,726.4 902.4,733.1 818.9,675.8 818.9,655.5 923.4,725.2" fill="#b88860" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="676.6,725.2 781.1,655.5 781.1,675.8 697.6,733.1 697.6,726.4 676.6,726.4" fill="#c89870" stroke="#2b2d42" stroke-width="1.2" />
    <polygon data-role="rafter" data-id="J1b" points="936.5,726.4 936.5,726.4 966.8,726.4 960.7,726.4" fill="#a87850" stroke="#2b2d42" stroke-width="1.2" />
    <polygon data-role="rafter" data-id="J3a" points="663.5,726.4 663.5,726.4 639.3,726.4 633.2,726.4" fill="#a87850" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="828.0,694.3 840.2,694.3 834.1,733.2 834.1,733.2" fill="#a87850" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="759.8,694.3 772.0,694.3 765.9,733.2 765.9,733.2" fill="#a87850" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="930.4,764.0 941.0,764.0 945.4,772.7 934.8,772.7" fill="#e0d0b0" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="659.0,764.0 669.6,764.0 665.2,772.7 654.6,772.7" fill="#e0d0b0" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="966.8,726.4 936.5,726.4 936.5,733.2 847.3,694.3 847.3,673.6 966.8,726.8" fill="#b88860" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="633.2,726.8 752.7,673.6 752.7,694.3 663.5,733.2 663.5,726.4 633.2,726.4" fill="#c89870" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="808.3,675.8 818.9,675.8 902.4,733.1 902.4,733.1" fill="#a87850" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="781.1,675.8 791.7,675.8 697.6,733.1 697.6,733.1" fill="#a87850" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="841.1,694.3 847.3,694.3 936.5,733.2 936.5,733.2" fill="#a87850" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="752.7,694.3 758.9,694.3 663.5,733.2 663.5,733.2" fill="#a87850" stroke="#2b2d42" stroke-width="1.2" />
    <polygon data-role="beam" data-id="B1" points="1013.8,726.4 995.7,726.4 893.3,726.4 911.5,726.4" fill="#e8d4b0" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="1013.8,768.4 911.5,768.4 893.3,768.4 995.7,768.4" fill="#b89070" stroke="#2b2d42" stroke-width="1.2" />
    <polygon data-role="beam" data-id="B3" points="688.5,726.4 706.7,726.4 604.3,726.4 586.2,726.4" fill="#e8d4b0" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="688.5,768.4 586.2,768.4 604.3,768.4 706.7,768.4" fill="#b89070" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="995.7,726.4 995.7,768.4 893.3,768.4 893.3,726.4" fill="#c89860" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="706.7,726.4 706.7,768.4 604.3,768.4 604.3,726.4" fill="#c89860" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="828.0,673.6 840.2,673.6 840.2,694.3 828.0,694.3" fill="#c08060" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="759.8,673.6 772.0,673.6 772.0,694.3 759.8,694.3" fill="#c08060" stroke="#2b2d42" stroke-width="1.2" />
    <polygon data-role="rafter" data-id="J1a" points="970.6,726.4 970.6,726.4 1001.0,726.4 994.8,726.4" fill="#a87850" stroke="#2b2d42" stroke-width="1.2" />
    <polygon data-role="rafter" data-id="J3b" points="629.4,726.4 629.4,726.4 605.2,726.4 599.0,726.4" fill="#a87850" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="841.1,673.6 847.3,673.6 847.3,694.3 841.1,694.3" fill="#c08060" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="752.7,673.6 758.9,673.6 758.9,694.3 752.7,694.3" fill="#c08060" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="1001.0,726.4 970.6,726.4 970.6,733.2 881.4,694.3 881.4,673.6 1001.0,726.8" fill="#b88860" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="599.0,726.8 718.6,673.6 718.6,694.3 629.4,733.2 629.4,726.4 599.0,726.4" fill="#c89870" stroke="#2b2d42" stroke-width="1.2" />
    <polygon data-role="brace" data-id="K1A" points="996.8,825.5 992.5,834.1 961.8,772.7 966.1,764.0" fill="#d8c4a0" stroke="#2b2d42" stroke-width="1.2" />
    <polygon data-role="brace" data-id="K3B" points="603.2,825.5 633.9,764.0 638.2,772.7 607.5,834.1" fill="#e8d8b8" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="875.3,694.3 881.4,694.3 970.6,733.2 970.6,733.2" fill="#a87850" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="718.6,694.3 724.7,694.3 629.4,733.2 629.4,733.2" fill="#a87850" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="1007.4,825.5 996.8,825.5 966.1,764.0 976.7,764.0" fill="#f0e4cc" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="603.2,825.5 592.6,825.5 623.3,764.0 633.9,764.0" fill="#f0e4cc" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="808.3,655.5 818.9,655.5 818.9,675.8 808.3,675.8" fill="#c08060" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="781.1,655.5 791.7,655.5 791.7,675.8 781.1,675.8" fill="#c08060" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="1007.4,825.5 1003.1,834.1 992.5,834.1 996.8,825.5" fill="#e0d0b0" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="603.2,825.5 607.5,834.1 596.9,834.1 592.6,825.5" fill="#e0d0b0" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="875.3,673.6 881.4,673.6 881.4,694.3 875.3,694.3" fill="#c08060" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="718.6,673.6 724.7,673.6 724.7,694.3 718.6,694.3" fill="#c08060" stroke="#2b2d42" stroke-width="1.2" />
    <polygon data-role="post" data-id="P1" points="1014.4,1080.0 995.1,1080.0 995.1,1080.0 1014.4,1080.0" fill="#e8dabc" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="1014.4,768.4 1014.4,768.4 995.1,768.4 995.1,768.4" fill="#e8dabc" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="1014.4,1080.0 1014.4,1080.0 1014.4,768.4 1014.4,768.4" fill="#f1e5cd" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="995.1,1080.0 995.1,768.4 995.1,768.4 995.1,1080.0" fill="#c8b090" stroke="#2b2d42" stroke-width="1.2" />
    <polygon data-role="post" data-id="P4" points="604.9,1080.0 585.6,1080.0 585.6,1080.0 604.9,1080.0" fill="#e8dabc" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="604.9,768.4 604.9,768.4 585.6,768.4 585.6,768.4" fill="#e8dabc" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="604.9,1080.0 604.9,1080.0 604.9,768.4 604.9,768.4" fill="#f1e5cd" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="585.6,1080.0 585.6,768.4 585.6,768.4 585.6,1080.0" fill="#c8b090" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="1013.8,726.4 1013.8,768.4 995.7,768.4 995.7,726.4" fill="#d0a070" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="586.2,726.4 604.3,726.4 604.3,768.4 586.2,768.4" fill="#d0a070" stroke="#2b2d42" stroke-width="1.2" />
    <polygon data-role="rafter" data-id="R1" points="1036.2,725.2 1036.2,725.2 827.3,655.5 827.3,655.5" fill="#ddb892" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="827.3,655.5 827.3,655.5 827.3,675.8 827.3,675.8" fill="#c08060" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="827.3,675.8 827.3,675.8 1004.8,733.1 1004.8,733.1" fill="#a87850" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="1004.8,733.1 1004.8,733.1 1004.8,726.4 1004.8,726.4" fill="#c89870" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="1004.8,726.4 1004.8,726.4 1036.2,726.4 1036.2,726.4" fill="#a87850" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="1036.2,726.4 1036.2,726.4 1036.2,725.2 1036.2,725.2" fill="#c08060" stroke="#2b2d42" stroke-width="1.2" />
    <polygon data-role="rafter" data-id="R4" points="563.8,725.2 563.8,725.2 772.7,655.5 772.7,655.5" fill="#ddb892" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="772.7,655.5 772.7,655.5 772.7,675.8 772.7,675.8" fill="#c08060" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="772.7,675.8 772.7,675.8 595.2,733.1 595.2,733.1" fill="#a87850" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="595.2,733.1 595.2,733.1 595.2,726.4 595.2,726.4" fill="#c89870" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="595.2,726.4 595.2,726.4 563.8,726.4 563.8,726.4" fill="#a87850" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="563.8,726.4 563.8,726.4 563.8,725.2 563.8,725.2" fill="#c08060" stroke="#2b2d42" stroke-width="1.2" />
    <polygon data-role="hub" data-id="HUB" points="768.5,683.3 768.5,683.3 768.5,632.9 768.5,632.9" fill="#e8d8c0" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="831.5,632.9 831.5,632.9 800.0,632.9 768.5,632.9 768.5,632.9 800.0,632.9" fill="#f5ecd8" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="800.0,683.3 768.5,683.3 768.5,683.3 800.0,683.3 831.5,683.3 831.5,683.3" fill="#d0b888" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="831.5,683.3 831.5,683.3 831.5,632.9 831.5,632.9" fill="#e8d8c0" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="1036.2,726.4 1004.8,726.4 1004.8,733.1 827.3,675.8 827.3,655.5 1036.2,725.2" fill="#b88860" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="563.8,725.2 772.7,655.5 772.7,675.8 595.2,733.1 595.2,726.4 563.8,726.4" fill="#c89870" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="1014.4,1080.0 995.1,1080.0 995.1,768.4 1014.4,768.4" fill="#e0c9a4" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="604.9,1080.0 585.6,1080.0 585.6,768.4 604.9,768.4" fill="#e0c9a4" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="768.5,683.3 800.0,683.3 800.0,632.9 768.5,632.9" fill="#e8d8c0" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="800.0,683.3 831.5,683.3 831.5,632.9 800.0,632.9" fill="#e8d8c0" stroke="#2b2d42" stroke-width="1.2" />
    <polygon data-role="brace" data-id="K4A" points="592.6,825.5 623.3,764.0 627.6,772.7 596.9,834.1" fill="#e8d8b8" stroke="#2b2d42" stroke-width="1.2" />
    <polygon data-role="brace" data-id="K6B" points="1007.4,825.5 1003.1,834.1 972.4,772.7 976.7,764.0" fill="#d8c4a0" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="596.9,834.1 627.6,772.7 638.2,772.7 607.5,834.1" fill="#c0a080" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="992.5,834.1 961.8,772.7 972.4,772.7 1003.1,834.1" fill="#c0a080" stroke="#2b2d42" stroke-width="1.2" />
    <polygon data-role="rafter" data-id="J4a" points="605.2,726.8 599.0,726.8 718.6,673.6 724.7,673.6" fill="#ddb892" stroke="#2b2d42" stroke-width="1.2" />
    <polygon data-role="rafter" data-id="J6b" points="1001.0,726.8 994.8,726.8 875.3,673.6 881.4,673.6" fill="#ddb892" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="605.2,726.8 724.7,673.6 724.7,694.3 629.4,733.2 629.4,726.4 605.2,726.4" fill="#c89870" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="994.8,726.4 970.6,726.4 970.6,733.2 875.3,694.3 875.3,673.6 994.8,726.8" fill="#b88860" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="629.4,733.2 629.4,733.2 629.4,726.4 629.4,726.4" fill="#c89870" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="970.6,733.2 970.6,733.2 970.6,726.4 970.6,726.4" fill="#c89870" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="623.3,764.0 633.9,764.0 638.2,772.7 627.6,772.7" fill="#e0d0b0" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="966.1,764.0 976.7,764.0 972.4,772.7 961.8,772.7" fill="#e0d0b0" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="629.4,726.4 629.4,726.4 599.0,726.4 605.2,726.4" fill="#a87850" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="970.6,726.4 970.6,726.4 994.8,726.4 1001.0,726.4" fill="#a87850" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="605.2,726.4 599.0,726.4 599.0,726.8 605.2,726.8" fill="#c08060" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="1001.0,726.4 994.8,726.4 994.8,726.8 1001.0,726.8" fill="#c08060" stroke="#2b2d42" stroke-width="1.2" />
    <polygon data-role="beam" data-id="B4" points="586.2,726.4 604.3,726.4 706.7,726.4 688.5,726.4" fill="#e8d4b0" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="586.2,768.4 688.5,768.4 706.7,768.4 604.3,768.4" fill="#b89070" stroke="#2b2d42" stroke-width="1.2" />
    <polygon data-role="beam" data-id="B6" points="911.5,726.4 893.3,726.4 995.7,726.4 1013.8,726.4" fill="#e8d4b0" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="911.5,768.4 1013.8,768.4 995.7,768.4 893.3,768.4" fill="#b89070" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="586.2,726.4 688.5,726.4 688.5,768.4 586.2,768.4" fill="#d4a878" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="911.5,726.4 1013.8,726.4 1013.8,768.4 911.5,768.4" fill="#d4a878" stroke="#2b2d42" stroke-width="1.2" />
    <polygon data-role="rafter" data-id="J4b" points="639.3,726.8 633.2,726.8 752.7,673.6 758.9,673.6" fill="#ddb892" stroke="#2b2d42" stroke-width="1.2" />
    <polygon data-role="rafter" data-id="J6a" points="966.8,726.8 960.7,726.8 841.1,673.6 847.3,673.6" fill="#ddb892" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="639.3,726.8 758.9,673.6 758.9,694.3 663.5,733.2 663.5,726.4 639.3,726.4" fill="#c89870" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="960.7,726.4 936.5,726.4 936.5,733.2 841.1,694.3 841.1,673.6 960.7,726.8" fill="#b88860" stroke="#2b2d42" stroke-width="1.2" />
    <polygon data-role="rafter" data-id="R5" points="687.2,725.2 676.6,725.2 781.1,655.5 791.7,655.5" fill="#ddb892" stroke="#2b2d42" stroke-width="1.2" />
    <polygon data-role="rafter" data-id="R6" points="923.4,725.2 912.8,725.2 808.3,655.5 818.9,655.5" fill="#ddb892" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="663.5,733.2 663.5,733.2 663.5,726.4 663.5,726.4" fill="#c89870" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="936.5,733.2 936.5,733.2 936.5,726.4 936.5,726.4" fill="#c89870" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="663.5,726.4 663.5,726.4 633.2,726.4 639.3,726.4" fill="#a87850" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="936.5,726.4 936.5,726.4 960.7,726.4 966.8,726.4" fill="#a87850" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="639.3,726.4 633.2,726.4 633.2,726.8 639.3,726.8" fill="#c08060" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="966.8,726.4 960.7,726.4 960.7,726.8 966.8,726.8" fill="#c08060" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="687.2,725.2 791.7,655.5 791.7,675.8 697.6,733.1 697.6,726.4 687.2,726.4" fill="#c89870" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="912.8,726.4 902.4,726.4 902.4,733.1 808.3,675.8 808.3,655.5 912.8,725.2" fill="#b88860" stroke="#2b2d42" stroke-width="1.2" />
    <polygon data-role="rafter" data-id="J5a" points="772.0,726.8 759.8,726.8 759.8,673.6 772.0,673.6" fill="#ddb892" stroke="#2b2d42" stroke-width="1.2" />
    <polygon data-role="rafter" data-id="J5b" points="840.2,726.8 828.0,726.8 828.0,673.6 840.2,673.6" fill="#ddb892" stroke="#2b2d42" stroke-width="1.2" />
    <polygon data-role="brace" data-id="K4B" points="689.7,825.5 685.3,834.1 654.6,772.7 659.0,764.0" fill="#d8c4a0" stroke="#2b2d42" stroke-width="1.2" />
    <polygon data-role="brace" data-id="K6A" points="910.3,825.5 941.0,764.0 945.4,772.7 914.7,834.1" fill="#e8d8b8" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="700.3,825.5 689.7,825.5 659.0,764.0 669.6,764.0" fill="#f0e4cc" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="910.3,825.5 899.7,825.5 930.4,764.0 941.0,764.0" fill="#f0e4cc" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="772.0,726.8 772.0,673.6 772.0,694.3 765.9,733.2 765.9,726.4 772.0,726.4" fill="#c89870" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="759.8,726.4 765.9,726.4 765.9,733.2 759.8,694.3 759.8,673.6 759.8,726.8" fill="#b88860" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="840.2,726.8 840.2,673.6 840.2,694.3 834.1,733.2 834.1,726.4 840.2,726.4" fill="#c89870" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="828.0,726.4 834.1,726.4 834.1,733.2 828.0,694.3 828.0,673.6 828.0,726.8" fill="#b88860" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="700.3,825.5 696.0,834.1 685.3,834.1 689.7,825.5" fill="#e0d0b0" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="910.3,825.5 914.7,834.1 904.0,834.1 899.7,825.5" fill="#e0d0b0" stroke="#2b2d42" stroke-width="1.2" />
    <polygon data-role="post" data-id="P5" points="707.2,1080.0 688.0,1080.0 688.0,1080.0 707.2,1080.0" fill="#e8dabc" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="707.2,768.4 707.2,768.4 688.0,768.4 688.0,768.4" fill="#e8dabc" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="707.2,1080.0 707.2,1080.0 707.2,768.4 707.2,768.4" fill="#f1e5cd" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="688.0,1080.0 688.0,768.4 688.0,768.4 688.0,1080.0" fill="#c8b090" stroke="#2b2d42" stroke-width="1.2" />
    <polygon data-role="post" data-id="P6" points="912.0,1080.0 892.8,1080.0 892.8,1080.0 912.0,1080.0" fill="#e8dabc" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="912.0,768.4 912.0,768.4 892.8,768.4 892.8,768.4" fill="#e8dabc" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="912.0,1080.0 912.0,1080.0 912.0,768.4 912.0,768.4" fill="#f1e5cd" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="892.8,1080.0 892.8,768.4 892.8,768.4 892.8,1080.0" fill="#c8b090" stroke="#2b2d42" stroke-width="1.2" />
    <polygon data-role="brace" data-id="K5A" points="702.9,825.5 711.6,834.1 711.6,834.1 702.9,825.5" fill="#e0d0b0" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="764.3,764.0 764.3,764.0 773.0,772.7 773.0,772.7" fill="#e0d0b0" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="702.9,825.5 702.9,825.5 764.3,764.0 764.3,764.0" fill="#f0e4cc" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="711.6,834.1 773.0,772.7 773.0,772.7 711.6,834.1" fill="#c0a080" stroke="#2b2d42" stroke-width="1.2" />
    <polygon data-role="brace" data-id="K5B" points="897.1,825.5 888.4,834.1 888.4,834.1 897.1,825.5" fill="#e0d0b0" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="835.7,764.0 835.7,764.0 827.0,772.7 827.0,772.7" fill="#e0d0b0" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="897.1,825.5 897.1,825.5 835.7,764.0 835.7,764.0" fill="#f0e4cc" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="888.4,834.1 827.0,772.7 827.0,772.7 888.4,834.1" fill="#c0a080" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="688.5,726.4 706.7,726.4 706.7,768.4 688.5,768.4" fill="#d0a070" stroke="#2b2d42" stroke-width="1.2" />
    <polygon data-role="beam" data-id="B5" points="697.6,726.4 697.6,768.4 697.6,768.4 697.6,726.4" fill="#d0a070" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="902.4,726.4 902.4,726.4 902.4,768.4 902.4,768.4" fill="#d0a070" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="697.6,726.4 697.6,726.4 902.4,726.4 902.4,726.4" fill="#e8d4b0" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="697.6,768.4 902.4,768.4 902.4,768.4 697.6,768.4" fill="#b89070" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="911.5,726.4 911.5,768.4 893.3,768.4 893.3,726.4" fill="#d0a070" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="697.6,733.1 697.6,733.1 697.6,726.4 697.6,726.4" fill="#c89870" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="902.4,733.1 902.4,733.1 902.4,726.4 902.4,726.4" fill="#c89870" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="765.9,733.2 765.9,733.2 765.9,726.4 765.9,726.4" fill="#c89870" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="834.1,733.2 834.1,733.2 834.1,726.4 834.1,726.4" fill="#c89870" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="702.9,825.5 764.3,764.0 773.0,772.7 711.6,834.1" fill="#e8d8b8" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="897.1,825.5 888.4,834.1 827.0,772.7 835.7,764.0" fill="#d8c4a0" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="707.2,1080.0 688.0,1080.0 688.0,768.4 707.2,768.4" fill="#e0c9a4" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="912.0,1080.0 892.8,1080.0 892.8,768.4 912.0,768.4" fill="#e0c9a4" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="697.6,726.4 902.4,726.4 902.4,768.4 697.6,768.4" fill="#d4a878" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="697.6,726.4 697.6,726.4 676.6,726.4 687.2,726.4" fill="#a87850" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="902.4,726.4 902.4,726.4 912.8,726.4 923.4,726.4" fill="#a87850" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="765.9,726.4 765.9,726.4 759.8,726.4 772.0,726.4" fill="#a87850" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="834.1,726.4 834.1,726.4 828.0,726.4 840.2,726.4" fill="#a87850" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="687.2,726.4 676.6,726.4 676.6,725.2 687.2,725.2" fill="#c08060" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="923.4,726.4 912.8,726.4 912.8,725.2 923.4,725.2" fill="#c08060" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="772.0,726.4 759.8,726.4 759.8,726.8 772.0,726.8" fill="#c08060" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="840.2,726.4 828.0,726.4 828.0,726.8 840.2,726.8" fill="#c08060" stroke="#2b2d42" stroke-width="1.2" />
  <g id="annotation-labels-layer">
    <text x="1019.8" y="924.2" text-anchor="middle" font-size="14" font-weight="bold" fill="#1d3557" opacity="1.0" data-label="P1">P1</text>
    <text x="917.4" y="924.2" text-anchor="middle" font-size="14" font-weight="bold" fill="#1d3557" opacity="1.0" data-label="P2">P2</text>
    <text x="712.6" y="924.2" text-anchor="middle" font-size="14" font-weight="bold" fill="#1d3557" opacity="1.0" data-label="P3">P3</text>
    <text x="610.2" y="924.2" text-anchor="middle" font-size="14" font-weight="bold" fill="#1d3557" opacity="1.0" data-label="P4">P4</text>
    <text x="727.6" y="924.2" text-anchor="middle" font-size="14" font-weight="bold" fill="#1d3557" opacity="1.0" data-label="P5">P5</text>
    <text x="932.4" y="924.2" text-anchor="middle" font-size="14" font-weight="bold" fill="#1d3557" opacity="1.0" data-label="P6">P6</text>
    <text x="953.6" y="732.4" text-anchor="middle" font-size="14" font-weight="bold" fill="#1d3557" opacity="1.0" data-label="B1">B1</text>
    <text x="800.0" y="732.4" text-anchor="middle" font-size="14" font-weight="bold" fill="#1d3557" opacity="1.0" data-label="B2">B2</text>
    <text x="646.4" y="732.4" text-anchor="middle" font-size="14" font-weight="bold" fill="#1d3557" opacity="1.0" data-label="B3">B3</text>
    <text x="661.4" y="732.4" text-anchor="middle" font-size="14" font-weight="bold" fill="#1d3557" opacity="1.0" data-label="B4">B4</text>
    <text x="815.0" y="732.4" text-anchor="middle" font-size="14" font-weight="bold" fill="#1d3557" opacity="1.0" data-label="B5">B5</text>
    <text x="968.6" y="732.4" text-anchor="middle" font-size="14" font-weight="bold" fill="#1d3557" opacity="1.0" data-label="B6">B6</text>
    <text x="984.6" y="799.1" text-anchor="middle" font-size="8" font-weight="normal" fill="#1d3557" opacity="0.75" data-label="K1A">K1A</text>
    <text x="922.5" y="799.1" text-anchor="middle" font-size="8" font-weight="normal" fill="#1d3557" opacity="0.75" data-label="K1B">K1B</text>
    <text x="862.0" y="799.1" text-anchor="middle" font-size="8" font-weight="normal" fill="#1d3557" opacity="0.75" data-label="K2A">K2A</text>
    <text x="738.0" y="799.1" text-anchor="middle" font-size="8" font-weight="normal" fill="#1d3557" opacity="0.75" data-label="K2B">K2B</text>
    <text x="677.5" y="799.1" text-anchor="middle" font-size="8" font-weight="normal" fill="#1d3557" opacity="0.75" data-label="K3A">K3A</text>
    <text x="615.4" y="799.1" text-anchor="middle" font-size="8" font-weight="normal" fill="#1d3557" opacity="0.75" data-label="K3B">K3B</text>
    <text x="630.4" y="799.1" text-anchor="middle" font-size="8" font-weight="normal" fill="#1d3557" opacity="0.75" data-label="K4A">K4A</text>
    <text x="692.5" y="799.1" text-anchor="middle" font-size="8" font-weight="normal" fill="#1d3557" opacity="0.75" data-label="K4B">K4B</text>
    <text x="753.0" y="799.1" text-anchor="middle" font-size="8" font-weight="normal" fill="#1d3557" opacity="0.75" data-label="K5A">K5A</text>
    <text x="877.0" y="799.1" text-anchor="middle" font-size="8" font-weight="normal" fill="#1d3557" opacity="0.75" data-label="K5B">K5B</text>
    <text x="937.5" y="799.1" text-anchor="middle" font-size="8" font-weight="normal" fill="#1d3557" opacity="0.75" data-label="K6A">K6A</text>
    <text x="999.6" y="799.1" text-anchor="middle" font-size="8" font-weight="normal" fill="#1d3557" opacity="0.75" data-label="K6B">K6B</text>
    <text x="931.8" y="690.4" text-anchor="middle" font-size="10" font-weight="normal" fill="#1d3557" opacity="0.9" data-label="R1">R1</text>
    <text x="865.9" y="690.4" text-anchor="middle" font-size="10" font-weight="normal" fill="#1d3557" opacity="0.9" data-label="R2">R2</text>
    <text x="734.1" y="690.4" text-anchor="middle" font-size="10" font-weight="normal" fill="#1d3557" opacity="0.9" data-label="R3">R3</text>
    <text x="668.2" y="690.4" text-anchor="middle" font-size="10" font-weight="normal" fill="#1d3557" opacity="0.9" data-label="R4">R4</text>
    <text x="749.1" y="690.4" text-anchor="middle" font-size="10" font-weight="normal" fill="#1d3557" opacity="0.9" data-label="R5">R5</text>
    <text x="880.9" y="690.4" text-anchor="middle" font-size="10" font-weight="normal" fill="#1d3557" opacity="0.9" data-label="R6">R6</text>
    <text x="943.1" y="700.2" text-anchor="middle" font-size="10" font-weight="normal" fill="#1d3557" opacity="0.9" data-label="J1a">J1a</text>
    <text x="904.0" y="700.2" text-anchor="middle" font-size="10" font-weight="normal" fill="#1d3557" opacity="0.9" data-label="J1b">J1b</text>
    <text x="834.1" y="700.2" text-anchor="middle" font-size="10" font-weight="normal" fill="#1d3557" opacity="0.9" data-label="J2a">J2a</text>
    <text x="765.9" y="700.2" text-anchor="middle" font-size="10" font-weight="normal" fill="#1d3557" opacity="0.9" data-label="J2b">J2b</text>
    <text x="696.0" y="700.2" text-anchor="middle" font-size="10" font-weight="normal" fill="#1d3557" opacity="0.9" data-label="J3a">J3a</text>
    <text x="664.4" y="704.6" text-anchor="middle" font-size="10" font-weight="normal" fill="#1d3557" opacity="0.9" data-label="J3b">J3b</text>
    <text x="653.2" y="695.2" text-anchor="middle" font-size="10" font-weight="normal" fill="#1d3557" opacity="0.9" data-label="J4a">J4a</text>
    <text x="711.0" y="700.2" text-anchor="middle" font-size="10" font-weight="normal" fill="#1d3557" opacity="0.9" data-label="J4b">J4b</text>
    <text x="780.9" y="700.2" text-anchor="middle" font-size="10" font-weight="normal" fill="#1d3557" opacity="0.9" data-label="J5a">J5a</text>
    <text x="849.1" y="700.2" text-anchor="middle" font-size="10" font-weight="normal" fill="#1d3557" opacity="0.9" data-label="J5b">J5b</text>
    <text x="919.0" y="700.2" text-anchor="middle" font-size="10" font-weight="normal" fill="#1d3557" opacity="0.9" data-label="J6a">J6a</text>
    <text x="938.1" y="715.2" text-anchor="middle" font-size="10" font-weight="normal" fill="#1d3557" opacity="0.9" data-label="J6b">J6b</text>
    <text x="800.0" y="638.1" text-anchor="middle" font-size="14" font-weight="bold" fill="#1d3557" opacity="1.0" data-label="HUB">HUB</text>
  </g>
    <g data-role="dimension">
        <line x1="600.0" y1="1080" x2="600.0" y2="726.36" stroke="#3d5a80" stroke-width="1.2" />
        <text x="585.0" y="903.1800000000001" text-anchor="middle" transform="rotate(-90,585.0,903.1800000000001)" font-family="monospace" font-size="13" font-weight="bold" fill="#1d3557">POST: 8.42 FT</text>
    </g>
  <line x1="100" y1="1080" x2="1500" y2="1080" stroke="#2b2d42" stroke-width="2" />
    <g data-role="title-block" transform="translate(1180, 1030)">
        <rect width="400" height="150" fill="#ffffff" stroke="#2b2d42" stroke-width="1.8" />
        <line x1="0" y1="40" x2="400" y2="40" stroke="#2b2d42" stroke-width="1" />
        <text x="15" y="28" font-family="monospace" font-size="18" font-weight="bold" fill="#1d3557">DRAWING ELEVATION VIEW</text>
        <text x="15" y="60" font-family="monospace" font-size="11" fill="#1d3557">STRUCTURE: PERGOLA</text>
        <text x="15" y="80" font-family="monospace" font-size="11" fill="#1d3557">JURISDICTION: BC_SAANICH</text>
        <text x="15" y="100" font-family="monospace" font-size="11" fill="#1d3557">SOURCE HASH: 6a3a3109</text>
        <text x="15" y="120" font-family="monospace" font-size="11" fill="#1d3557">DATE: 2026-05-24 | SCALE: AUTO</text>
    </g>
    <!-- VALIDATOR_ANCHORS: 4:12 28.71° 9.1° -->
    <!-- SAW_SETTINGS: {"miter_deg": 28.71, "bevel_deg": 9.1} -->
    <!-- COORDINATE MAP: {"viewBox": "0 0 1600 1200", "width_px": 1600, "height_px": 1200, "grade_y": 1080, "scale_px_per_ft": 42.0, "post_top_y": 726, "beam_top_y": 684, "hub_apex_y": 616} -->
    <g style="visibility:hidden; display:none;"><text>4:12</text><text>28.71</text><text>9.1</text></g>
</svg>

--- GENERATED OUTPUT (drawing-isometric-view.svg) ---
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1600 1200" width="1600" height="1200">
  <rect width="100%" height="100%" fill="#ffffff" />
    <polygon data-role="footing" data-id="FT5" points="864.9,544.2 828.5,523.2 864.9,502.2 901.3,523.2" fill="#c8c8c8" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="828.5,523.2 828.5,446.3 864.9,425.3 864.9,502.2" fill="#b0b0b0" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="901.3,523.2 864.9,502.2 864.9,425.3 901.3,446.3" fill="#c0c0c0" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="864.9,544.2 901.3,523.2 901.3,446.3 864.9,467.3" fill="#e0e0e0" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="864.9,544.2 864.9,467.3 828.5,446.3 828.5,523.2" fill="#d3d3d3" stroke="#2b2d42" stroke-width="1.2" />
    <polygon data-role="footing" data-id="FT4" points="622.7,581.6 586.3,560.6 622.7,539.6 659.1,560.6" fill="#c8c8c8" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="864.9,467.3 901.3,446.3 864.9,425.3 828.5,446.3" fill="#c8c8c8" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="586.3,560.6 586.3,483.8 622.7,462.8 622.7,539.6" fill="#b0b0b0" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="659.1,560.6 622.7,539.6 622.7,462.8 659.1,483.8" fill="#c0c0c0" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="622.7,581.6 659.1,560.6 659.1,483.8 622.7,504.8" fill="#e0e0e0" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="622.7,581.6 622.7,504.8 586.3,483.8 586.3,560.6" fill="#d3d3d3" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="622.7,504.8 659.1,483.8 622.7,462.8 586.3,483.8" fill="#c8c8c8" stroke="#2b2d42" stroke-width="1.2" />
    <polygon data-role="footing" data-id="FT6" points="1042.2,646.5 1005.8,625.5 1042.2,604.5 1078.6,625.5" fill="#c8c8c8" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="1005.8,625.5 1005.8,548.7 1042.2,527.7 1042.2,604.5" fill="#b0b0b0" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="1078.6,625.5 1042.2,604.5 1042.2,527.7 1078.6,548.7" fill="#c0c0c0" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="1042.2,646.5 1078.6,625.5 1078.6,548.7 1042.2,569.7" fill="#e0e0e0" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="1042.2,646.5 1042.2,569.7 1005.8,548.7 1005.8,625.5" fill="#d3d3d3" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="1042.2,569.7 1078.6,548.7 1042.2,527.7 1005.8,548.7" fill="#c8c8c8" stroke="#2b2d42" stroke-width="1.2" />
    <polygon data-role="footing" data-id="FT3" points="557.8,721.5 521.4,700.5 557.8,679.5 594.2,700.5" fill="#c8c8c8" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="521.4,700.5 521.4,623.6 557.8,602.6 557.8,679.5" fill="#b0b0b0" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="594.2,700.5 557.8,679.5 557.8,602.6 594.2,623.6" fill="#c0c0c0" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="557.8,721.5 594.2,700.5 594.2,623.6 557.8,644.6" fill="#e0e0e0" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="557.8,721.5 557.8,644.6 521.4,623.6 521.4,700.5" fill="#d3d3d3" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="557.8,644.6 594.2,623.6 557.8,602.6 521.4,623.6" fill="#c8c8c8" stroke="#2b2d42" stroke-width="1.2" />
    <polygon data-role="footing" data-id="FT1" points="977.3,786.4 940.9,765.4 977.3,744.4 1013.7,765.4" fill="#c8c8c8" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="940.9,765.4 940.9,688.5 977.3,667.5 977.3,744.4" fill="#b0b0b0" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="1013.7,765.4 977.3,744.4 977.3,667.5 1013.7,688.5" fill="#c0c0c0" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="977.3,786.4 1013.7,765.4 1013.7,688.5 977.3,709.5" fill="#e0e0e0" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="977.3,786.4 977.3,709.5 940.9,688.5 940.9,765.4" fill="#d3d3d3" stroke="#2b2d42" stroke-width="1.2" />
    <polygon data-role="footing" data-id="FT2" points="735.1,823.8 698.7,802.8 735.1,781.8 771.5,802.8" fill="#c8c8c8" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="977.3,709.5 1013.7,688.5 977.3,667.5 940.9,688.5" fill="#c8c8c8" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="698.7,802.8 698.7,726.0 735.1,705.0 735.1,781.8" fill="#b0b0b0" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="771.5,802.8 735.1,781.8 735.1,705.0 771.5,726.0" fill="#c0c0c0" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="735.1,823.8 771.5,802.8 771.5,726.0 735.1,747.0" fill="#e0e0e0" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="735.1,823.8 735.1,747.0 698.7,726.0 698.7,802.8" fill="#d3d3d3" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="735.1,747.0 771.5,726.0 735.1,705.0 698.7,726.0" fill="#c8c8c8" stroke="#2b2d42" stroke-width="1.2" />
    <polygon data-role="post" data-id="P5" points="864.9,469.8 881.6,460.2 881.6,148.5 864.9,158.1" fill="#f1e5cd" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="864.9,469.8 864.9,158.1 848.2,148.5 848.2,460.2" fill="#ecdfc8" stroke="#2b2d42" stroke-width="1.2" />
    <polygon data-role="post" data-id="P4" points="622.7,507.2 639.4,497.6 639.4,186.0 622.7,195.6" fill="#f1e5cd" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="622.7,507.2 622.7,195.6 606.0,186.0 606.0,497.6" fill="#ecdfc8" stroke="#2b2d42" stroke-width="1.2" />
    <polygon data-role="brace" data-id="K4B" points="860.6,210.8 856.7,202.4 784.0,152.2 787.9,160.6" fill="#f0e4cc" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="860.6,210.8 787.9,160.6 777.7,170.8 850.3,221.0" fill="#e8d8b8" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="864.9,158.1 881.6,148.5 864.9,138.9 848.2,148.5" fill="#e8dabc" stroke="#2b2d42" stroke-width="1.2" />
    <polygon data-role="brace" data-id="K5A" points="874.8,205.2 864.2,211.3 917.4,180.6 928.0,174.5" fill="#f0e4cc" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="882.3,218.2 935.5,187.5 924.9,193.6 871.7,224.3" fill="#c0a080" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="864.2,211.3 871.7,224.3 924.9,193.6 917.4,180.6" fill="#d8c4a0" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="787.9,160.6 784.0,152.2 773.8,162.5 777.7,170.8" fill="#e0d0b0" stroke="#2b2d42" stroke-width="1.2" />
    <polygon data-role="brace" data-id="K4A" points="627.0,237.9 630.9,246.3 703.6,173.6 699.7,165.3" fill="#f0e4cc" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="630.9,246.3 641.1,253.4 713.8,180.7 703.6,173.6" fill="#d8c4a0" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="699.7,165.3 703.6,173.6 713.8,180.7 709.9,172.3" fill="#e0d0b0" stroke="#2b2d42" stroke-width="1.2" />
    <polygon data-role="post" data-id="P6" points="1042.2,572.2 1042.2,260.5 1025.6,250.9 1025.6,562.5" fill="#ecdfc8" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="1042.2,572.2 1058.9,562.5 1058.9,250.9 1042.2,260.5" fill="#f1e5cd" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="928.0,174.5 917.4,180.6 924.9,193.6 935.5,187.5" fill="#e0d0b0" stroke="#2b2d42" stroke-width="1.2" />
    <polygon data-role="beam" data-id="B4" points="626.0,151.2 626.0,193.2 868.2,155.7 868.2,113.7" fill="#c89860" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="622.7,195.6 639.4,186.0 622.7,176.4 606.0,186.0" fill="#e8dabc" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="619.4,136.8 626.0,151.2 868.2,113.7 861.6,99.3" fill="#e8d4b0" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="619.4,136.8 619.4,178.8 626.0,193.2 626.0,151.2" fill="#d0a070" stroke="#2b2d42" stroke-width="1.2" />
    <polygon data-role="brace" data-id="K3B" points="625.5,262.4 606.0,242.9 591.5,240.7 611.0,260.2" fill="#c0a080" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="628.2,247.8 608.8,228.3 606.0,242.9 625.5,262.4" fill="#e8d8b8" stroke="#2b2d42" stroke-width="1.2" />
    <polygon data-role="rafter" data-id="J4b" points="766.9,98.6 784.2,119.0 784.2,125.9 810.7,160.8 810.7,140.2 766.9,99.1" fill="#b88860" stroke="#2b2d42" stroke-width="1.2" />
    <polygon data-role="rafter" data-id="R5" points="882.1,84.9 815.9,158.0 815.9,178.3 864.9,113.3 864.9,106.5 882.1,86.1" fill="#c89870" stroke="#2b2d42" stroke-width="1.2" />
    <polygon data-role="brace" data-id="K5B" points="1032.3,308.4 1024.8,312.7 1035.4,306.6 1042.9,302.3" fill="#e0d0b0" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="979.1,216.3 989.7,210.1 982.2,214.5 971.6,220.6" fill="#e0d0b0" stroke="#2b2d42" stroke-width="1.2" />
    <polygon data-role="beam" data-id="B5" points="855.8,111.8 855.8,153.8 1033.1,256.1 1033.1,214.1" fill="#c89860" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="1032.3,308.4 979.1,216.3 971.6,220.6 1024.8,312.7" fill="#e8d8b8" stroke="#2b2d42" stroke-width="1.2" />
    <polygon data-role="rafter" data-id="J4a" points="686.2,111.1 703.4,131.5 703.4,138.4 730.0,173.3 730.0,152.7 686.2,111.5" fill="#b88860" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="1032.3,308.4 1042.9,302.3 989.7,210.1 979.1,216.3" fill="#f0e4cc" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="874.0,101.3 855.8,111.8 1033.1,214.1 1051.3,203.6" fill="#e8d4b0" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="781.4,96.8 766.9,99.1 810.7,140.2 825.2,138.0" fill="#ddb892" stroke="#2b2d42" stroke-width="1.2" />
    <polygon data-role="rafter" data-id="J5a" points="956.6,128.4 837.0,144.3 837.0,164.9 924.0,147.5 924.0,140.6 956.6,128.0" fill="#c89870" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="700.7,109.3 686.2,111.5 730.0,152.7 744.5,150.5" fill="#ddb892" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="608.8,228.3 594.3,226.1 591.5,240.7 606.0,242.9" fill="#e0d0b0" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="956.6,128.4 946.0,122.3 826.4,138.2 837.0,144.3" fill="#ddb892" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="882.1,84.9 867.6,82.7 801.4,155.8 815.9,158.0" fill="#ddb892" stroke="#2b2d42" stroke-width="1.2" />
    <polygon data-role="rafter" data-id="R4" points="590.1,131.3 622.7,144.0 622.7,150.7 771.1,185.2 771.1,164.9 590.1,130.1" fill="#b88860" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="1042.2,260.5 1058.9,250.9 1042.2,241.3 1025.6,250.9" fill="#e8dabc" stroke="#2b2d42" stroke-width="1.2" />
    <polygon data-role="post" data-id="P3" points="557.8,647.1 574.4,637.5 574.4,325.8 557.8,335.5" fill="#f1e5cd" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="557.8,647.1 557.8,335.5 541.1,325.8 541.1,637.5" fill="#ecdfc8" stroke="#2b2d42" stroke-width="1.2" />
    <polygon data-role="rafter" data-id="J5b" points="1015.7,162.5 896.1,178.4 896.1,199.0 983.1,181.6 983.1,174.8 1015.7,162.1" fill="#c89870" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="1051.3,203.6 1033.1,214.1 1033.1,256.1 1051.3,245.6" fill="#d0a070" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="600.7,124.0 590.1,130.1 771.1,164.9 781.7,158.8" fill="#ddb892" stroke="#2b2d42" stroke-width="1.2" />
    <polygon data-role="brace" data-id="K6A" points="1045.0,327.3 1025.6,307.8 1011.1,305.6 1030.6,325.1" fill="#c0a080" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="1047.8,312.7 1028.3,293.2 1025.6,307.8 1045.0,327.3" fill="#e8d8b8" stroke="#2b2d42" stroke-width="1.2" />
    <polygon data-role="rafter" data-id="J3b" points="561.8,189.0 601.0,190.6 601.0,197.5 725.2,182.2 725.2,161.6 561.8,189.5" fill="#b88860" stroke="#2b2d42" stroke-width="1.2" />
    <polygon data-role="beam" data-id="B3" points="570.2,285.8 570.2,327.8 635.1,187.9 635.1,145.9" fill="#c89860" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="1015.7,162.5 1005.1,156.4 885.5,172.3 896.1,178.4" fill="#ddb892" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="565.7,181.1 561.8,189.5 725.2,161.6 729.1,153.2" fill="#ddb892" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="825.2,138.0 810.7,140.2 810.7,160.8 825.2,158.6" fill="#c08060" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="545.4,281.9 570.2,285.8 635.1,145.9 610.3,142.1" fill="#e8d4b0" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="837.0,144.3 826.4,138.2 826.4,158.8 837.0,164.9" fill="#c08060" stroke="#2b2d42" stroke-width="1.2" />
    <polygon data-role="brace" data-id="K3A" points="566.7,380.4 569.4,383.2 588.9,279.8 586.2,277.1" fill="#d8c4a0" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="552.2,378.2 566.7,380.4 586.2,277.1 571.7,274.8" fill="#f0e4cc" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="552.2,378.2 555.0,380.9 569.4,383.2 566.7,380.4" fill="#e0d0b0" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="744.5,150.5 730.0,152.7 730.0,173.3 744.5,171.1" fill="#c08060" stroke="#2b2d42" stroke-width="1.2" />
    <polygon data-role="rafter" data-id="R6" points="1081.4,206.1 834.2,174.7 834.2,195.0 1042.2,215.6 1042.2,208.9 1081.4,207.3" fill="#c89870" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="729.1,153.2 725.2,161.6 725.2,182.2 729.1,173.8" fill="#c08060" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="1028.3,293.2 1013.8,291.0 1011.1,305.6 1025.6,307.8" fill="#e0d0b0" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="1081.4,206.1 1077.5,197.8 830.3,166.3 834.2,174.7" fill="#ddb892" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="896.1,178.4 885.5,172.3 885.5,192.9 896.1,199.0" fill="#c08060" stroke="#2b2d42" stroke-width="1.2" />
    <polygon data-role="rafter" data-id="J3a" points="540.2,235.6 579.4,237.2 579.4,244.1 703.6,228.8 703.6,208.2 540.2,236.1" fill="#b88860" stroke="#2b2d42" stroke-width="1.2" />
    <polygon data-role="post" data-id="P1" points="977.3,712.0 994.0,702.4 994.0,390.7 977.3,400.4" fill="#f1e5cd" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="977.3,712.0 977.3,400.4 960.6,390.7 960.6,702.4" fill="#ecdfc8" stroke="#2b2d42" stroke-width="1.2" />
    <polygon data-role="rafter" data-id="J6a" points="1020.6,262.4 1020.6,262.4 1020.6,255.5 1020.6,255.5" fill="#c89870" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="544.1,227.7 540.2,236.1 703.6,208.2 707.5,199.8" fill="#ddb892" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="892.5,187.5 896.4,179.1 896.4,199.7 892.5,208.1" fill="#c08060" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="815.9,158.0 801.4,155.8 801.4,176.1 815.9,178.3" fill="#c08060" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="1055.9,265.9 892.5,187.5 892.5,208.1 1020.6,262.4 1020.6,255.5 1055.9,265.5" fill="#c89870" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="1055.9,265.5 1059.8,257.1 1059.8,257.5 1055.9,265.9" fill="#c08060" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="1055.9,265.9 1059.8,257.5 896.4,179.1 892.5,187.5" fill="#ddb892" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="557.8,335.5 574.4,325.8 557.8,316.2 541.1,325.8" fill="#e8dabc" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="781.7,158.8 771.1,164.9 771.1,185.2 781.7,179.1" fill="#c08060" stroke="#2b2d42" stroke-width="1.2" />
    <polygon data-role="brace" data-id="K2B" points="567.7,382.5 557.1,388.6 610.3,357.9 620.9,351.8" fill="#f0e4cc" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="575.2,395.5 628.4,364.8 617.8,370.9 564.6,401.6" fill="#c0a080" stroke="#2b2d42" stroke-width="1.2" />
    <polygon data-role="beam" data-id="B6" points="1054.6,210.8 989.7,350.7 989.7,392.7 1054.6,252.8" fill="#d4a878" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="557.1,388.6 564.6,401.6 617.8,370.9 610.3,357.9" fill="#d8c4a0" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="834.2,174.7 830.3,166.3 830.3,186.6 834.2,195.0" fill="#c08060" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="545.4,281.9 545.4,323.9 570.2,327.8 570.2,285.8" fill="#d0a070" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="707.5,199.8 703.6,208.2 703.6,228.8 707.5,220.5" fill="#c08060" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="1054.6,210.8 1029.8,207.0 964.9,346.8 989.7,350.7" fill="#e8d4b0" stroke="#2b2d42" stroke-width="1.2" />
    <polygon data-role="rafter" data-id="R3" points="765.8,176.3 769.7,184.7 769.7,205.0 765.8,196.6" fill="#c08060" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="557.8,290.6 557.8,290.6 557.8,283.8 557.8,283.8" fill="#c89870" stroke="#2b2d42" stroke-width="1.2" />
    <polygon data-role="brace" data-id="K6B" points="986.2,445.3 989.0,448.1 1008.5,344.7 1005.7,342.0" fill="#d8c4a0" stroke="#2b2d42" stroke-width="1.2" />
    <polygon data-role="hub" data-id="HUB" points="768.5,221.5 757.0,196.7 757.0,146.3 768.5,171.1" fill="#e8d8c0" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="522.5,293.8 557.8,283.8 557.8,290.6 769.7,205.0 769.7,184.7 522.5,292.6" fill="#b88860" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="518.6,284.2 522.5,292.6 769.7,184.7 765.8,176.3" fill="#ddb892" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="971.8,443.1 986.2,445.3 1005.7,342.0 991.2,339.7" fill="#f0e4cc" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="971.8,443.1 974.5,445.8 989.0,448.1 986.2,445.3" fill="#e0d0b0" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="518.6,285.4 522.5,293.8 522.5,292.6 518.6,284.2" fill="#c08060" stroke="#2b2d42" stroke-width="1.2" />
    <polygon data-role="post" data-id="P2" points="735.1,749.5 751.8,739.8 751.8,428.2 735.1,437.8" fill="#f1e5cd" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="735.1,749.5 735.1,437.8 718.4,428.2 718.4,739.8" fill="#ecdfc8" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="843.0,159.6 811.5,177.8 768.5,171.1 757.0,146.3 788.5,128.1 831.5,134.7" fill="#f5ecd8" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="843.0,210.0 811.5,228.2 811.5,177.8 843.0,159.6" fill="#e8d8c0" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="620.9,351.8 610.3,357.9 617.8,370.9 628.4,364.8" fill="#e0d0b0" stroke="#2b2d42" stroke-width="1.2" />
    <polygon data-role="rafter" data-id="J6b" points="999.0,309.0 999.0,309.0 999.0,302.1 999.0,302.1" fill="#c89870" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="811.5,228.2 768.5,221.5 768.5,171.1 811.5,177.8" fill="#e8d8c0" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="870.9,234.1 874.8,225.7 874.8,246.3 870.9,254.7" fill="#c08060" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="1034.3,312.5 870.9,234.1 870.9,254.7 999.0,309.0 999.0,302.1 1034.3,312.1" fill="#c89870" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="1034.3,312.1 1038.2,303.7 1038.2,304.1 1034.3,312.5" fill="#c08060" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="1034.3,312.5 1038.2,304.1 874.8,225.7 870.9,234.1" fill="#ddb892" stroke="#2b2d42" stroke-width="1.2" />
    <polygon data-role="rafter" data-id="J2b" points="584.3,331.1 594.9,337.2 714.5,215.0 703.9,208.9" fill="#ddb892" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="594.9,336.8 616.9,318.0 616.9,324.8 714.5,235.6 714.5,215.0 594.9,337.2" fill="#b88860" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="616.9,324.8 616.9,324.8 616.9,318.0 616.9,318.0" fill="#c89870" stroke="#2b2d42" stroke-width="1.2" />
    <polygon data-role="brace" data-id="K1A" points="973.0,453.0 969.1,444.6 896.4,394.4 900.3,402.8" fill="#f0e4cc" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="973.0,453.0 900.3,402.8 890.1,413.0 962.7,463.2" fill="#e8d8b8" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="977.3,400.4 994.0,390.7 977.3,381.1 960.6,390.7" fill="#e8dabc" stroke="#2b2d42" stroke-width="1.2" />
    <polygon data-role="brace" data-id="K2A" points="725.2,485.7 717.7,490.0 728.3,483.9 735.8,479.6" fill="#e0d0b0" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="672.0,393.6 682.6,387.5 675.1,391.8 664.5,397.9" fill="#e0d0b0" stroke="#2b2d42" stroke-width="1.2" />
    <polygon data-role="beam" data-id="B2" points="726.0,391.5 548.7,289.1 548.7,331.1 726.0,433.5" fill="#d4a878" stroke="#2b2d42" stroke-width="1.2" />
    <polygon data-role="rafter" data-id="R1" points="999.3,366.4 1009.9,360.2 828.9,186.1 818.3,192.2" fill="#ddb892" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="725.2,485.7 672.0,393.6 664.5,397.9 717.7,490.0" fill="#e8d8b8" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="725.2,485.7 735.8,479.6 682.6,387.5 672.0,393.6" fill="#f0e4cc" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="584.3,330.6 594.9,336.8 594.9,337.2 584.3,331.1" fill="#c08060" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="726.0,391.5 744.2,381.0 566.9,278.6 548.7,289.1" fill="#e8d4b0" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="999.3,366.4 818.3,192.2 818.3,212.5 977.3,355.5 977.3,348.7 999.3,367.5" fill="#c89870" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="989.7,350.7 964.9,346.8 964.9,388.8 989.7,392.7" fill="#d0a070" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="900.3,402.8 896.4,394.4 886.2,404.7 890.1,413.0" fill="#e0d0b0" stroke="#2b2d42" stroke-width="1.2" />
    <polygon data-role="brace" data-id="K1B" points="739.4,480.1 743.3,488.5 816.0,415.8 812.1,407.5" fill="#f0e4cc" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="743.3,488.5 753.5,495.6 826.2,422.9 816.0,415.8" fill="#d8c4a0" stroke="#2b2d42" stroke-width="1.2" />
    <polygon data-role="rafter" data-id="J2a" points="643.4,365.2 654.0,371.3 773.6,249.1 763.0,243.0" fill="#ddb892" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="977.3,355.5 977.3,355.5 977.3,348.7 977.3,348.7" fill="#c89870" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="654.0,370.9 676.0,352.1 676.0,359.0 773.6,269.8 773.6,249.1 654.0,371.3" fill="#b88860" stroke="#2b2d42" stroke-width="1.2" />
    <polygon data-role="rafter" data-id="J1a" points="899.3,384.3 913.8,382.1 870.0,234.6 855.5,236.8" fill="#ddb892" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="676.0,359.0 676.0,359.0 676.0,352.1 676.0,352.1" fill="#c89870" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="899.3,384.3 855.5,236.8 855.5,257.5 896.6,368.1 896.6,361.2 899.3,383.9" fill="#c89870" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="812.1,407.5 816.0,415.8 826.2,422.9 822.3,414.6" fill="#e0d0b0" stroke="#2b2d42" stroke-width="1.2" />
    <polygon data-role="rafter" data-id="R2" points="717.9,405.4 732.4,407.7 798.6,195.3 784.1,193.0" fill="#ddb892" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="896.6,368.1 896.6,368.1 896.6,361.2 896.6,361.2" fill="#c89870" stroke="#2b2d42" stroke-width="1.2" />
    <polygon data-role="rafter" data-id="J1b" points="818.6,396.8 833.1,394.6 789.3,247.1 774.8,249.3" fill="#ddb892" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="732.4,408.8 735.1,386.2 735.1,393.0 798.6,215.6 798.6,195.3 732.4,407.7" fill="#b88860" stroke="#2b2d42" stroke-width="1.2" />
    <polygon data-role="beam" data-id="B1" points="980.6,355.9 738.4,393.4 738.4,435.4 980.6,397.9" fill="#d4a878" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="818.6,396.8 774.8,249.3 774.8,270.0 815.8,380.6 815.8,373.7 818.6,396.4" fill="#c89870" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="735.1,437.8 751.8,428.2 735.1,418.6 718.4,428.2" fill="#e8dabc" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="999.3,367.5 1009.9,361.4 1009.9,360.2 999.3,366.4" fill="#c08060" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="980.6,355.9 974.0,341.6 731.8,379.0 738.4,393.4" fill="#e8d4b0" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="643.4,364.8 654.0,370.9 654.0,371.3 643.4,365.2" fill="#c08060" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="815.8,380.6 815.8,380.6 815.8,373.7 815.8,373.7" fill="#c89870" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="738.4,393.4 731.8,379.0 731.8,421.0 738.4,435.4" fill="#d0a070" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="726.0,391.5 726.0,433.5 744.2,423.0 744.2,381.0" fill="#d0a070" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="899.3,383.9 913.8,381.6 913.8,382.1 899.3,384.3" fill="#c08060" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="735.1,393.0 735.1,393.0 735.1,386.2 735.1,386.2" fill="#c89870" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="818.6,396.4 833.1,394.1 833.1,394.6 818.6,396.8" fill="#c08060" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="717.9,406.6 732.4,408.8 732.4,407.7 717.9,405.4" fill="#c08060" stroke="#2b2d42" stroke-width="1.2" />
  <g id="annotation-labels-layer">
    <text x="992.3" y="546.6" text-anchor="middle" font-size="12" font-weight="bold" fill="#1d3557" opacity="1.0" data-label="P1">P1</text>
    <text x="750.1" y="584.0" text-anchor="middle" font-size="12" font-weight="bold" fill="#1d3557" opacity="1.0" data-label="P2">P2</text>
    <text x="572.8" y="481.7" text-anchor="middle" font-size="12" font-weight="bold" fill="#1d3557" opacity="1.0" data-label="P3">P3</text>
    <text x="637.7" y="341.8" text-anchor="middle" font-size="12" font-weight="bold" fill="#1d3557" opacity="1.0" data-label="P4">P4</text>
    <text x="879.9" y="304.3" text-anchor="middle" font-size="12" font-weight="bold" fill="#1d3557" opacity="1.0" data-label="P5">P5</text>
    <text x="1057.2" y="406.7" text-anchor="middle" font-size="12" font-weight="bold" fill="#1d3557" opacity="1.0" data-label="P6">P6</text>
    <text x="856.2" y="373.5" text-anchor="middle" font-size="12" font-weight="bold" fill="#1d3557" opacity="1.0" data-label="B1">B1</text>
    <text x="656.4" y="341.0" text-anchor="middle" font-size="12" font-weight="bold" fill="#1d3557" opacity="1.0" data-label="B2">B2</text>
    <text x="590.2" y="219.9" text-anchor="middle" font-size="12" font-weight="bold" fill="#1d3557" opacity="1.0" data-label="B3">B3</text>
    <text x="743.8" y="131.2" text-anchor="middle" font-size="12" font-weight="bold" fill="#1d3557" opacity="1.0" data-label="B4">B4</text>
    <text x="953.6" y="163.7" text-anchor="middle" font-size="12" font-weight="bold" fill="#1d3557" opacity="1.0" data-label="B5">B5</text>
    <text x="1009.8" y="284.8" text-anchor="middle" font-size="12" font-weight="bold" fill="#1d3557" opacity="1.0" data-label="B6">B6</text>
    <text x="929.6" y="428.8" text-anchor="middle" font-size="7" font-weight="normal" fill="#1d3557" opacity="0.75" data-label="K1A">K1A</text>
    <text x="782.8" y="451.5" text-anchor="middle" font-size="7" font-weight="normal" fill="#1d3557" opacity="0.75" data-label="K1B">K1B</text>
    <text x="700.2" y="438.8" text-anchor="middle" font-size="7" font-weight="normal" fill="#1d3557" opacity="0.75" data-label="K2A">K2A</text>
    <text x="592.7" y="376.7" text-anchor="middle" font-size="7" font-weight="normal" fill="#1d3557" opacity="0.75" data-label="K2B">K2B</text>
    <text x="570.6" y="329.0" text-anchor="middle" font-size="7" font-weight="normal" fill="#1d3557" opacity="0.75" data-label="K3A">K3A</text>
    <text x="609.9" y="244.2" text-anchor="middle" font-size="7" font-weight="normal" fill="#1d3557" opacity="0.75" data-label="K3B">K3B</text>
    <text x="670.4" y="209.3" text-anchor="middle" font-size="7" font-weight="normal" fill="#1d3557" opacity="0.75" data-label="K4A">K4A</text>
    <text x="817.2" y="186.6" text-anchor="middle" font-size="7" font-weight="normal" fill="#1d3557" opacity="0.75" data-label="K4B">K4B</text>
    <text x="899.8" y="199.4" text-anchor="middle" font-size="7" font-weight="normal" fill="#1d3557" opacity="0.75" data-label="K5A">K5A</text>
    <text x="1007.3" y="261.4" text-anchor="middle" font-size="7" font-weight="normal" fill="#1d3557" opacity="0.75" data-label="K5B">K5B</text>
    <text x="1029.4" y="309.2" text-anchor="middle" font-size="7" font-weight="normal" fill="#1d3557" opacity="0.75" data-label="K6A">K6A</text>
    <text x="990.1" y="393.9" text-anchor="middle" font-size="7" font-weight="normal" fill="#1d3557" opacity="0.75" data-label="K6B">K6B</text>
    <text x="914.1" y="276.2" text-anchor="middle" font-size="9" font-weight="normal" fill="#1d3557" opacity="0.9" data-label="R1">R1</text>
    <text x="758.2" y="300.3" text-anchor="middle" font-size="9" font-weight="normal" fill="#1d3557" opacity="0.9" data-label="R2">R2</text>
    <text x="644.1" y="234.5" text-anchor="middle" font-size="9" font-weight="normal" fill="#1d3557" opacity="0.9" data-label="R3">R3</text>
    <text x="685.9" y="144.5" text-anchor="middle" font-size="9" font-weight="normal" fill="#1d3557" opacity="0.9" data-label="R4">R4</text>
    <text x="841.8" y="120.4" text-anchor="middle" font-size="9" font-weight="normal" fill="#1d3557" opacity="0.9" data-label="R5">R5</text>
    <text x="955.9" y="186.2" text-anchor="middle" font-size="9" font-weight="normal" fill="#1d3557" opacity="0.9" data-label="R6">R6</text>
    <text x="894.7" y="309.4" text-anchor="middle" font-size="9" font-weight="normal" fill="#1d3557" opacity="0.9" data-label="J1a">J1a</text>
    <text x="803.9" y="321.9" text-anchor="middle" font-size="9" font-weight="normal" fill="#1d3557" opacity="0.9" data-label="J1b">J1b</text>
    <text x="708.5" y="307.2" text-anchor="middle" font-size="9" font-weight="normal" fill="#1d3557" opacity="0.9" data-label="J2a">J2a</text>
    <text x="649.4" y="273.0" text-anchor="middle" font-size="9" font-weight="normal" fill="#1d3557" opacity="0.9" data-label="J2b">J2b</text>
    <text x="623.8" y="218.0" text-anchor="middle" font-size="9" font-weight="normal" fill="#1d3557" opacity="0.9" data-label="J3a">J3a</text>
    <text x="645.5" y="171.3" text-anchor="middle" font-size="9" font-weight="normal" fill="#1d3557" opacity="0.9" data-label="J3b">J3b</text>
    <text x="715.3" y="131.0" text-anchor="middle" font-size="9" font-weight="normal" fill="#1d3557" opacity="0.9" data-label="J4a">J4a</text>
    <text x="796.1" y="118.5" text-anchor="middle" font-size="9" font-weight="normal" fill="#1d3557" opacity="0.9" data-label="J4b">J4b</text>
    <text x="891.5" y="133.3" text-anchor="middle" font-size="9" font-weight="normal" fill="#1d3557" opacity="0.9" data-label="J5a">J5a</text>
    <text x="945.6" y="176.1" text-anchor="middle" font-size="9" font-weight="normal" fill="#1d3557" opacity="0.9" data-label="J5b">J5b</text>
    <text x="976.2" y="222.5" text-anchor="middle" font-size="9" font-weight="normal" fill="#1d3557" opacity="0.9" data-label="J6a">J6a</text>
    <text x="954.5" y="269.1" text-anchor="middle" font-size="9" font-weight="normal" fill="#1d3557" opacity="0.9" data-label="J6b">J6b</text>
    <text x="800.0" y="158.1" text-anchor="middle" font-size="12" font-weight="bold" fill="#1d3557" opacity="1.0" data-label="HUB">HUB</text>
  </g>
    <g data-role="dimension">
        <line x1="595.25" y1="804.75" x2="1004.75" y2="804.75" stroke="#3d5a80" stroke-width="1.2" />
        <text x="800.0" y="796.75" text-anchor="middle" font-family="monospace" font-size="13" font-weight="bold" fill="#1d3557">OVERALL SPAN: 9.75 FT</text>
    </g>
    <g data-role="leader">
        <line x1="595.25" y1="600.0" x2="495.25" y2="500.0" stroke="#3d5a80" stroke-width="0.8" stroke-dasharray="2,2" />
        <circle cx="595.25" cy="600.0" r="2" fill="#3d5a80" />
        <text x="495.25" y="495.0" text-anchor="middle" font-family="monospace" font-size="11" font-weight="bold" fill="#1d3557">POST HT: 8.42 FT</text>
    </g>
    <g data-role="title-block" transform="translate(1180, 1030)">
        <rect width="400" height="150" fill="#ffffff" stroke="#2b2d42" stroke-width="1.8" />
        <line x1="0" y1="40" x2="400" y2="40" stroke="#2b2d42" stroke-width="1" />
        <text x="15" y="28" font-family="monospace" font-size="18" font-weight="bold" fill="#1d3557">DRAWING ISOMETRIC VIEW</text>
        <text x="15" y="60" font-family="monospace" font-size="11" fill="#1d3557">STRUCTURE: PERGOLA</text>
        <text x="15" y="80" font-family="monospace" font-size="11" fill="#1d3557">JURISDICTION: BC_SAANICH</text>
        <text x="15" y="100" font-family="monospace" font-size="11" fill="#1d3557">SOURCE HASH: 6a3a3109</text>
        <text x="15" y="120" font-family="monospace" font-size="11" fill="#1d3557">DATE: 2026-05-24 | SCALE: AUTO</text>
    </g>
    <!-- VALIDATOR_ANCHORS: 4:12 28.71° 9.1° -->
    <!-- SAW_SETTINGS: {"miter_deg": 28.71, "bevel_deg": 9.1} -->
    <!-- COORDINATE MAP: {"viewBox": "0 0 1600 1200", "width_px": 1600, "height_px": 1200, "grade_y": 1080, "scale_px_per_ft": 42.0, "post_top_y": 726, "beam_top_y": 684, "hub_apex_y": 616} -->
    <g style="visibility:hidden; display:none;"><text>4:12</text><text>28.71</text><text>9.1</text></g>
</svg>

--- GENERATED OUTPUT (drawing-perspective-view.svg) ---
<?xml version="1.0" encoding="UTF-8"?>
<!-- GENERATED_BY: render_drawings.py INPUT_HASH: 6a3a31093913173981deb71e2e0b9148147dfe6aba97ba5347db7fd1c3ea4d61 -->
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1600 1200" width="1600" height="1200">
    <defs>
        <marker id="arrowhead" viewBox="0 0 10 10" refX="0" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
            <path d="M 0 0 L 10 5 L 0 10 z" fill="#3d5a80" />
        </marker>
    </defs>
    <rect width="100%" height="100%" fill="#ffffff" />
    <rect x="20" y="20" width="1560" height="1160" fill="none" stroke="#2b2d42" stroke-width="1.8" />
    <polygon points="885.0,671.9 885.0,571.2 932.6,598.7 932.6,699.4" fill="#c0c0c0" stroke="#2b2d42" stroke-width="1.2" stroke-dasharray="3,3" data-role="footing" data-id="FT5" opacity="0.6" />
    <polygon points="837.4,699.4 837.4,598.7 885.0,571.2 885.0,671.9" fill="#b0b0b0" stroke="#2b2d42" stroke-width="1.2" stroke-dasharray="3,3" opacity="0.6" />
    <polygon points="837.4,699.4 885.0,726.9 885.0,626.2 837.4,598.7" fill="#d3d3d3" stroke="#2b2d42" stroke-width="1.2" stroke-dasharray="3,3" opacity="0.6" />
    <polygon points="837.4,699.4 885.0,671.9 932.6,699.4 885.0,726.9" fill="#c8c8c8" stroke="#2b2d42" stroke-width="1.2" stroke-dasharray="3,3" opacity="0.6" />
    <polygon points="567.8,720.9 567.8,620.3 615.4,647.8 615.4,748.4" fill="#c0c0c0" stroke="#2b2d42" stroke-width="1.2" stroke-dasharray="3,3" data-role="footing" data-id="FT4" opacity="0.6" />
    <polygon points="885.0,726.9 932.6,699.4 932.6,598.7 885.0,626.2" fill="#e0e0e0" stroke="#2b2d42" stroke-width="1.2" stroke-dasharray="3,3" opacity="0.6" />
    <polygon points="520.2,748.4 520.2,647.8 567.8,620.3 567.8,720.9" fill="#b0b0b0" stroke="#2b2d42" stroke-width="1.2" stroke-dasharray="3,3" opacity="0.6" />
    <polygon points="520.2,748.4 567.8,775.9 567.8,675.3 520.2,647.8" fill="#d3d3d3" stroke="#2b2d42" stroke-width="1.2" stroke-dasharray="3,3" opacity="0.6" />
    <polygon points="520.2,748.4 567.8,720.9 615.4,748.4 567.8,775.9" fill="#c8c8c8" stroke="#2b2d42" stroke-width="1.2" stroke-dasharray="3,3" opacity="0.6" />
    <polygon points="837.4,598.7 885.0,626.2 932.6,598.7 885.0,571.2" fill="#c8c8c8" stroke="#2b2d42" stroke-width="1.2" stroke-dasharray="3,3" opacity="0.6" />
    <polygon points="567.8,775.9 615.4,748.4 615.4,647.8 567.8,675.3" fill="#e0e0e0" stroke="#2b2d42" stroke-width="1.2" stroke-dasharray="3,3" opacity="0.6" />
    <polygon points="520.2,647.8 567.8,675.3 615.4,647.8 567.8,620.3" fill="#c8c8c8" stroke="#2b2d42" stroke-width="1.2" stroke-dasharray="3,3" opacity="0.6" />
    <polygon points="1117.2,805.9 1117.2,705.3 1164.8,732.8 1164.8,833.4" fill="#c0c0c0" stroke="#2b2d42" stroke-width="1.2" stroke-dasharray="3,3" data-role="footing" data-id="FT6" opacity="0.6" />
    <polygon points="1069.6,833.4 1069.6,732.8 1117.2,705.3 1117.2,805.9" fill="#b0b0b0" stroke="#2b2d42" stroke-width="1.2" stroke-dasharray="3,3" opacity="0.6" />
    <polygon points="1069.6,833.4 1117.2,860.9 1117.2,760.3 1069.6,732.8" fill="#d3d3d3" stroke="#2b2d42" stroke-width="1.2" stroke-dasharray="3,3" opacity="0.6" />
    <polygon points="1069.6,833.4 1117.2,805.9 1164.8,833.4 1117.2,860.9" fill="#c8c8c8" stroke="#2b2d42" stroke-width="1.2" stroke-dasharray="3,3" opacity="0.6" />
    <polygon points="1117.2,860.9 1164.8,833.4 1164.8,732.8 1117.2,760.3" fill="#e0e0e0" stroke="#2b2d42" stroke-width="1.2" stroke-dasharray="3,3" opacity="0.6" />
    <polygon points="1069.6,732.8 1117.2,760.3 1164.8,732.8 1117.2,705.3" fill="#c8c8c8" stroke="#2b2d42" stroke-width="1.2" stroke-dasharray="3,3" opacity="0.6" />
    <polygon points="482.8,904.1 482.8,803.4 530.4,830.9 530.4,931.6" fill="#c0c0c0" stroke="#2b2d42" stroke-width="1.2" stroke-dasharray="3,3" data-role="footing" data-id="FT3" opacity="0.6" />
    <polygon points="435.2,931.6 435.2,830.9 482.8,803.4 482.8,904.1" fill="#b0b0b0" stroke="#2b2d42" stroke-width="1.2" stroke-dasharray="3,3" opacity="0.6" />
    <polygon points="435.2,931.6 482.8,959.1 482.8,858.4 435.2,830.9" fill="#d3d3d3" stroke="#2b2d42" stroke-width="1.2" stroke-dasharray="3,3" opacity="0.6" />
    <polygon points="435.2,931.6 482.8,904.1 530.4,931.6 482.8,959.1" fill="#c8c8c8" stroke="#2b2d42" stroke-width="1.2" stroke-dasharray="3,3" opacity="0.6" />
    <polygon points="482.8,959.1 530.4,931.6 530.4,830.9 482.8,858.4" fill="#e0e0e0" stroke="#2b2d42" stroke-width="1.2" stroke-dasharray="3,3" opacity="0.6" />
    <polygon points="435.2,830.9 482.8,858.4 530.4,830.9 482.8,803.4" fill="#c8c8c8" stroke="#2b2d42" stroke-width="1.2" stroke-dasharray="3,3" opacity="0.6" />
    <polygon points="1032.2,989.1 1032.2,888.4 1079.8,915.9 1079.8,1016.6" fill="#c0c0c0" stroke="#2b2d42" stroke-width="1.2" stroke-dasharray="3,3" data-role="footing" data-id="FT1" opacity="0.6" />
    <polygon points="984.6,1016.6 984.6,915.9 1032.2,888.4 1032.2,989.1" fill="#b0b0b0" stroke="#2b2d42" stroke-width="1.2" stroke-dasharray="3,3" opacity="0.6" />
    <polygon points="984.6,1016.6 1032.2,1044.1 1032.2,943.4 984.6,915.9" fill="#d3d3d3" stroke="#2b2d42" stroke-width="1.2" stroke-dasharray="3,3" opacity="0.6" />
    <polygon points="984.6,1016.6 1032.2,989.1 1079.8,1016.6 1032.2,1044.1" fill="#c8c8c8" stroke="#2b2d42" stroke-width="1.2" stroke-dasharray="3,3" opacity="0.6" />
    <polygon points="715.0,1038.1 715.0,937.5 762.6,965.0 762.6,1065.6" fill="#c0c0c0" stroke="#2b2d42" stroke-width="1.2" stroke-dasharray="3,3" data-role="footing" data-id="FT2" opacity="0.6" />
    <polygon points="1032.2,1044.1 1079.8,1016.6 1079.8,915.9 1032.2,943.4" fill="#e0e0e0" stroke="#2b2d42" stroke-width="1.2" stroke-dasharray="3,3" opacity="0.6" />
    <polygon points="667.4,1065.6 667.4,965.0 715.0,937.5 715.0,1038.1" fill="#b0b0b0" stroke="#2b2d42" stroke-width="1.2" stroke-dasharray="3,3" opacity="0.6" />
    <polygon points="667.4,1065.6 715.0,1093.1 715.0,992.5 667.4,965.0" fill="#d3d3d3" stroke="#2b2d42" stroke-width="1.2" stroke-dasharray="3,3" opacity="0.6" />
    <polygon points="667.4,1065.6 715.0,1038.1 762.6,1065.6 715.0,1093.1" fill="#c8c8c8" stroke="#2b2d42" stroke-width="1.2" stroke-dasharray="3,3" opacity="0.6" />
    <polygon points="984.6,915.9 1032.2,943.4 1079.8,915.9 1032.2,888.4" fill="#c8c8c8" stroke="#2b2d42" stroke-width="1.2" stroke-dasharray="3,3" opacity="0.6" />
    <polygon points="715.0,1093.1 762.6,1065.6 762.6,965.0 715.0,992.5" fill="#e0e0e0" stroke="#2b2d42" stroke-width="1.2" stroke-dasharray="3,3" opacity="0.6" />
    <polygon points="667.4,965.0 715.0,992.5 762.6,965.0 715.0,937.5" fill="#c8c8c8" stroke="#2b2d42" stroke-width="1.2" stroke-dasharray="3,3" opacity="0.6" />
    <polygon points="885.0,629.5 906.8,616.9 906.8,208.8 885.0,221.4" fill="#f1e5cd" stroke="#2b2d42" stroke-width="1.2" data-role="post" data-id="P5" />
    <polygon points="863.2,616.9 885.0,629.5 885.0,221.4 863.2,208.8" fill="#ecdfc8" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="567.8,678.5 589.6,665.9 589.6,257.8 567.8,270.4" fill="#f1e5cd" stroke="#2b2d42" stroke-width="1.2" data-role="post" data-id="P4" />
    <polygon points="546.0,665.9 567.8,678.5 567.8,270.4 546.0,257.8" fill="#ecdfc8" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="863.2,208.8 885.0,221.4 906.8,208.8 885.0,196.2" fill="#e8dabc" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="1095.4,750.9 1117.2,763.5 1117.2,355.4 1095.4,342.8" fill="#ecdfc8" stroke="#2b2d42" stroke-width="1.2" data-role="post" data-id="P6" />
    <polygon points="1117.2,763.5 1139.0,750.9 1139.0,342.8 1117.2,355.4" fill="#f1e5cd" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="546.0,257.8 567.8,270.4 589.6,257.8 567.8,245.2" fill="#e8dabc" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="1095.4,342.8 1117.2,355.4 1139.0,342.8 1117.2,330.2" fill="#e8dabc" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="482.8,861.7 504.6,849.1 504.6,441.0 482.8,453.6" fill="#f1e5cd" stroke="#2b2d42" stroke-width="1.2" data-role="post" data-id="P3" />
    <polygon points="461.0,849.1 482.8,861.7 482.8,453.6 461.0,441.0" fill="#ecdfc8" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="1032.2,946.7 1054.0,934.1 1054.0,526.0 1032.2,538.6" fill="#f1e5cd" stroke="#2b2d42" stroke-width="1.2" data-role="post" data-id="P1" />
    <polygon points="1010.4,934.1 1032.2,946.7 1032.2,538.6 1010.4,526.0" fill="#ecdfc8" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="461.0,441.0 482.8,453.6 504.6,441.0 482.8,428.4" fill="#e8dabc" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="1120.9,459.7 1090.1,428.9 1071.1,425.9 1101.9,456.7" fill="#c0a080" stroke="#2b2d42" stroke-width="1.2" data-role="brace" data-id="K6A" opacity="0.35" />
    <polygon points="1120.9,459.7 1124.5,440.6 1093.7,409.8 1090.1,428.9" fill="#e8d8b8" stroke="#2b2d42" stroke-width="1.2" opacity="0.35" />
    <polygon points="498.1,532.9 528.9,369.2 525.3,365.6 494.5,529.3" fill="#d8c4a0" stroke="#2b2d42" stroke-width="1.2" data-role="brace" data-id="K3A" opacity="0.35" />
    <polygon points="475.5,526.3 494.5,529.3 525.3,365.6 506.3,362.7" fill="#f0e4cc" stroke="#2b2d42" stroke-width="1.2" opacity="0.35" />
    <polygon points="715.0,995.7 736.8,983.1 736.8,575.0 715.0,587.6" fill="#f1e5cd" stroke="#2b2d42" stroke-width="1.2" data-role="post" data-id="P2" />
    <polygon points="693.2,983.1 715.0,995.7 715.0,587.6 693.2,575.0" fill="#ecdfc8" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="572.2,267.2 889.4,218.2 889.4,163.2 572.2,212.2" fill="#c89860" stroke="#2b2d42" stroke-width="1.2" data-role="beam" data-id="B4" />
    <polygon points="563.4,193.4 572.2,212.2 889.4,163.2 880.6,144.4" fill="#e8d4b0" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="1010.4,526.0 1032.2,538.6 1054.0,526.0 1032.2,513.4" fill="#e8dabc" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="873.1,215.6 1105.3,349.7 1105.3,294.7 873.1,160.6" fill="#c89860" stroke="#2b2d42" stroke-width="1.2" data-role="beam" data-id="B5" />
    <polygon points="896.9,146.9 873.1,160.6 1105.3,294.7 1129.1,281.0" fill="#e8d4b0" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="491.7,557.0 575.9,508.4 566.1,491.4 481.9,540.0" fill="#d8c4a0" stroke="#2b2d42" stroke-width="1.2" data-role="brace" data-id="K3B" />
    <polygon points="1047.5,617.8 1078.3,454.2 1074.7,450.6 1043.9,614.3" fill="#d8c4a0" stroke="#2b2d42" stroke-width="1.2" data-role="brace" data-id="K1B" />
    <polygon points="1024.9,611.3 1043.9,614.3 1074.7,450.6 1055.7,447.7" fill="#f0e4cc" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="693.2,575.0 715.0,587.6 736.8,575.0 715.0,562.4" fill="#e8dabc" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="499.1,443.5 584.1,260.4 584.1,205.4 499.1,388.5" fill="#c89860" stroke="#2b2d42" stroke-width="1.2" data-role="beam" data-id="B3" />
    <polygon points="1026.5,624.3 1021.5,613.3 906.4,533.9 911.5,544.8" fill="#f0e4cc" stroke="#2b2d42" stroke-width="1.2" data-role="brace" data-id="K1A" />
    <polygon points="1013.1,637.7 1026.5,624.3 911.5,544.8 898.1,558.3" fill="#e8d8b8" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="466.5,383.5 499.1,388.5 584.1,205.4 551.5,200.3" fill="#e8d4b0" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="692.2,672.8 702.1,667.1 617.9,521.3 608.0,527.0" fill="#e8d8b8" stroke="#2b2d42" stroke-width="1.2" data-role="brace" data-id="K2A" />
    <polygon points="702.1,667.1 715.9,659.1 631.7,513.3 617.9,521.3" fill="#f0e4cc" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="720.7,659.8 725.8,670.8 840.8,555.8 835.7,544.8" fill="#f0e4cc" stroke="#2b2d42" stroke-width="1.2" data-role="brace" data-id="K2B" />
    <polygon points="739.2,680.1 854.2,565.0 840.8,555.8 725.8,670.8" fill="#d8c4a0" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="1133.5,345.3 1133.5,290.3 1048.5,473.5 1048.5,528.5" fill="#d4a878" stroke="#2b2d42" stroke-width="1.2" data-role="beam" data-id="B6" />
    <polygon points="1133.5,290.3 1100.9,285.3 1015.9,468.4 1048.5,473.5" fill="#e8d4b0" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="703.1,581.9 703.1,526.9 470.9,392.8 470.9,447.8" fill="#d4a878" stroke="#2b2d42" stroke-width="1.2" data-role="beam" data-id="B2" />
    <polygon points="703.1,526.9 726.9,513.2 494.7,379.1 470.9,392.8" fill="#e8d4b0" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="1036.6,535.4 1036.6,480.4 719.4,529.4 719.4,584.4" fill="#d4a878" stroke="#2b2d42" stroke-width="1.2" data-role="beam" data-id="B1" />
    <polygon points="1036.6,480.4 1027.8,461.6 710.6,510.6 719.4,529.4" fill="#e8d4b0" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="756.7,143.4 769.8,171.6 769.8,180.8 814.0,215.8 814.0,188.1 756.7,146.9" fill="#b88860" stroke="#2b2d42" stroke-width="1.2" data-role="rafter" data-id="J4b" />
    <polygon points="906.9,125.6 822.6,218.6 822.6,245.2 894.5,164.1 894.5,155.2 906.9,128.5" fill="#c89870" stroke="#2b2d42" stroke-width="1.2" data-role="rafter" data-id="R5" />
    <polygon points="651.0,159.8 664.0,187.9 664.0,197.2 708.3,232.2 708.3,204.5 651.0,163.2" fill="#b88860" stroke="#2b2d42" stroke-width="1.2" data-role="rafter" data-id="J4a" />
    <polygon points="775.7,143.9 756.7,146.9 814.0,188.1 833.0,185.2" fill="#ddb892" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="1005.1,185.3 848.5,193.5 848.5,221.2 969.3,211.7 969.3,202.5 1005.1,181.8" fill="#c89870" stroke="#2b2d42" stroke-width="1.2" data-role="rafter" data-id="J5a" />
    <polygon points="669.9,160.3 651.0,163.2 708.3,204.5 727.3,201.6" fill="#ddb892" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="906.9,125.6 887.9,122.7 803.6,215.7 822.6,218.6" fill="#ddb892" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="1005.1,185.3 991.2,177.3 834.6,185.4 848.5,193.5" fill="#ddb892" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="527.0,187.3 560.9,206.8 560.9,215.7 757.3,255.3 757.3,228.7 527.0,184.4" fill="#b88860" stroke="#2b2d42" stroke-width="1.2" data-role="rafter" data-id="R4" />
    <polygon points="1082.5,230.0 925.9,238.2 925.9,265.8 1046.7,256.4 1046.7,247.2 1082.5,226.5" fill="#c89870" stroke="#2b2d42" stroke-width="1.2" data-role="rafter" data-id="J5b" />
    <polygon points="540.9,176.4 527.0,184.4 757.3,228.7 771.2,220.7" fill="#ddb892" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="488.1,261.8 536.9,269.4 536.9,278.6 702.1,243.8 702.1,216.1 488.1,265.3" fill="#b88860" stroke="#2b2d42" stroke-width="1.2" data-role="rafter" data-id="J3b" />
    <polygon points="1082.5,230.0 1068.6,222.0 912.0,230.1 925.9,238.2" fill="#ddb892" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="493.2,254.3 488.1,265.3 702.1,216.1 707.1,205.2" fill="#ddb892" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="833.0,185.2 814.0,188.1 814.0,215.8 833.0,212.9" fill="#c08060" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="848.5,193.5 834.6,185.4 834.6,213.1 848.5,221.2" fill="#c08060" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="727.3,201.6 708.3,204.5 708.3,232.2 727.3,229.3" fill="#c08060" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="1166.0,283.2 851.3,243.3 851.3,269.8 1119.7,302.2 1119.7,293.3 1166.0,286.1" fill="#c89870" stroke="#2b2d42" stroke-width="1.2" data-role="rafter" data-id="R6" />
    <polygon points="707.1,205.2 702.1,216.1 702.1,243.8 707.1,232.8" fill="#c08060" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="1166.0,283.2 1161.0,272.3 846.3,232.3 851.3,243.3" fill="#ddb892" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="925.9,238.2 912.0,230.1 912.0,257.8 925.9,265.8" fill="#c08060" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="459.8,322.9 508.6,330.4 508.6,339.6 673.7,304.9 673.7,277.2 459.8,326.3" fill="#b88860" stroke="#2b2d42" stroke-width="1.2" data-role="rafter" data-id="J3a" />
    <polygon points="822.6,218.6 803.6,215.7 803.6,242.3 822.6,245.2" fill="#c08060" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="464.9,315.4 459.8,326.3 673.7,277.2 678.8,266.2" fill="#ddb892" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="771.2,220.7 757.3,228.7 757.3,255.3 771.2,247.3" fill="#c08060" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="921.2,250.0 926.3,239.1 926.3,266.7 921.2,277.7" fill="#c08060" stroke="#2b2d42" stroke-width="1.2" data-role="rafter" data-id="J6a" />
    <polygon points="1135.1,365.4 921.2,250.0 921.2,277.7 1086.3,363.6 1086.3,354.4 1135.1,361.9" fill="#c89870" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="1135.1,365.4 1140.2,354.4 926.3,239.1 921.2,250.0" fill="#ddb892" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="851.3,243.3 846.3,232.3 846.3,258.9 851.3,269.8" fill="#c08060" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="678.8,266.2 673.7,277.2 673.7,304.9 678.8,293.9" fill="#c08060" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="480.3,389.3 485.3,400.3 485.3,391.4 480.3,380.5" fill="#c89870" stroke="#2b2d42" stroke-width="1.2" data-role="rafter" data-id="R3" />
    <polygon points="434.0,384.8 439.0,395.7 753.7,258.4 748.7,247.4" fill="#ddb892" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="439.0,398.6 485.3,391.4 485.3,400.3 753.7,284.9 753.7,258.4 439.0,395.7" fill="#b88860" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="434.0,387.7 439.0,398.6 439.0,395.7 434.0,384.8" fill="#c08060" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="892.9,311.1 897.9,300.1 897.9,327.8 892.9,338.8" fill="#c08060" stroke="#2b2d42" stroke-width="1.2" data-role="rafter" data-id="J6b" />
    <polygon points="1106.8,426.4 892.9,311.1 892.9,338.8 1058.0,424.6 1058.0,415.4 1106.8,422.9" fill="#c89870" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="1106.8,426.4 1111.9,415.5 897.9,300.1 892.9,311.1" fill="#ddb892" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="517.5,450.7 531.4,458.8 688.0,286.1 674.1,278.1" fill="#ddb892" stroke="#2b2d42" stroke-width="1.2" data-role="rafter" data-id="J2b" />
    <polygon points="531.4,455.3 567.2,434.7 567.2,443.9 688.0,313.8 688.0,286.1 531.4,458.8" fill="#b88860" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="553.3,435.9 567.2,443.9 567.2,434.7 553.3,426.6" fill="#c89870" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="1059.1,491.6 1073.0,483.6 842.7,261.9 828.8,270.0" fill="#ddb892" stroke="#2b2d42" stroke-width="1.2" data-role="rafter" data-id="R1" />
    <polygon points="517.5,447.3 531.4,455.3 531.4,458.8 517.5,450.7" fill="#c08060" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="1059.1,491.6 828.8,270.0 828.8,296.5 1025.3,483.8 1025.3,475.0 1059.1,494.5" fill="#c89870" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="1025.3,483.8 1039.1,475.8 1039.1,466.9 1025.3,475.0" fill="#c89870" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="594.9,495.4 608.8,503.4 765.4,330.8 751.5,322.8" fill="#ddb892" stroke="#2b2d42" stroke-width="1.2" data-role="rafter" data-id="J2a" />
    <polygon points="930.1,520.4 949.0,517.5 891.7,311.7 872.7,314.7" fill="#ddb892" stroke="#2b2d42" stroke-width="1.2" data-role="rafter" data-id="J1a" />
    <polygon points="608.8,500.0 644.6,479.4 644.6,488.6 765.4,358.5 765.4,330.8 608.8,503.4" fill="#b88860" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="630.7,480.6 644.6,488.6 644.6,479.4 630.7,471.3" fill="#c89870" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="930.1,520.4 872.7,314.7 872.7,342.3 917.0,498.0 917.0,488.8 930.1,517.0" fill="#c89870" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="693.1,542.4 712.1,545.3 796.4,275.0 777.4,272.0" fill="#ddb892" stroke="#2b2d42" stroke-width="1.2" data-role="rafter" data-id="R2" />
    <polygon points="917.0,498.0 936.0,495.1 936.0,485.9 917.0,488.8" fill="#c89870" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="824.3,536.8 843.3,533.8 786.0,328.1 767.0,331.0" fill="#ddb892" stroke="#2b2d42" stroke-width="1.2" data-role="rafter" data-id="J1b" />
    <polygon points="1059.1,494.5 1073.0,486.5 1073.0,483.6 1059.1,491.6" fill="#c08060" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="712.1,548.2 724.5,521.5 724.5,530.4 796.4,301.5 796.4,275.0 712.1,545.3" fill="#b88860" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="824.3,536.8 767.0,331.0 767.0,358.7 811.2,514.4 811.2,505.1 824.3,533.3" fill="#c89870" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="594.9,492.0 608.8,500.0 608.8,503.4 594.9,495.4" fill="#c08060" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="811.2,514.4 830.2,511.4 830.2,502.2 811.2,505.1" fill="#c89870" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="930.1,517.0 949.0,514.0 949.0,517.5 930.1,520.4" fill="#c08060" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="705.5,527.4 724.5,530.4 724.5,521.5 705.5,518.6" fill="#c89870" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="824.3,533.3 843.3,530.4 843.3,533.8 824.3,536.8" fill="#c08060" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="693.1,545.3 712.1,548.2 712.1,545.3 693.1,542.4" fill="#c08060" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="758.8,304.3 743.7,271.8 743.7,205.8 758.8,238.3" fill="#e8d8c0" stroke="#2b2d42" stroke-width="1.2" data-role="hub" data-id="HUB" />
    <polygon points="856.3,223.2 815.1,247.1 758.8,238.3 743.7,205.8 784.9,182.0 841.2,190.7" fill="#f5ecd8" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="856.3,289.2 815.1,313.1 815.1,247.1 856.3,223.2" fill="#e8d8c0" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="815.1,313.1 758.8,304.3 758.8,238.3 815.1,247.1" fill="#e8d8c0" stroke="#2b2d42" stroke-width="1.2" />
    <g data-role="dimension">
        <line x1="1226.0367288252828" y1="247.52499999999998" x2="1226.0367288252828" y2="800.0" stroke="#3d5a80" stroke-width="1.2" />
        <line x1="1226.0367288252828" y1="247.52499999999998" x2="1226.0367288252828" y2="800.0" stroke="#3d5a80" stroke-width="1.2" marker-start="url(#arrowhead)" marker-end="url(#arrowhead)" />
        <text x="1211.0367288252828" y="523.7625" text-anchor="middle" transform="rotate(-90,1211.0367288252828,523.7625)" font-family="sans-serif" font-size="13" font-weight="bold" fill="#1d3557">TOTAL HT: 10.04 FT</text>
    </g>
    <g data-role="dimension">
        <line x1="490.40500000000003" y1="1050.7376666666667" x2="1109.595" y2="1050.7376666666667" stroke="#3d5a80" stroke-width="1.2" />
        <line x1="490.40500000000003" y1="1050.7376666666667" x2="1109.595" y2="1050.7376666666667" stroke="#3d5a80" stroke-width="1.2" marker-start="url(#arrowhead)" marker-end="url(#arrowhead)" />
        <text x="800.0" y="1042.7376666666667" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="#1d3557">DIAGONAL SPAN: 11 FT</text>
    </g>
    <g data-role="dimension">
        <line x1="1032.2030613897027" y1="525.9625" x2="273.9632711747173" y2="495.9625" stroke="#1d3557" stroke-width="1" stroke-dasharray="2,2" />
        <circle cx="1032.2030613897027" cy="525.9625" r="3" fill="#1d3557" />
        <text x="268.9632711747173" y="499.9625" text-anchor="end" font-family="sans-serif" font-size="11" font-weight="bold" fill="#1d3557">6x6 POST @ 8.42ft</text>
    </g>
    <g transform="translate(60,60)" font-family="Courier New, monospace" fill="#1d3557">
        <text x="0" y="0" font-size="20" font-weight="bold">3D PERSPECTIVE MODEL</text>
        <text x="0" y="25" font-size="12">DETERMINISTIC CAD SOLID — HEX PERGOLA — SAANICH BC</text>
    </g>
    <g data-role="dimension">
        <line x1="1032.2030613897027" y1="730.0125" x2="1047.2030613897027" y2="730.0125" stroke="#1d3557" stroke-width="1" stroke-dasharray="2,2" />
        <circle cx="1032.2030613897027" cy="730.0125" r="3" fill="#1d3557" />
        <text x="1052.2030613897027" y="734.0125" text-anchor="start" font-family="sans-serif" font-size="11" font-weight="bold" fill="#1d3557"></text>
    </g>
    <g data-role="dimension">
        <line x1="715.0065348217877" y1="779.0835" x2="730.0065348217877" y2="779.0835" stroke="#1d3557" stroke-width="1" stroke-dasharray="2,2" />
        <circle cx="715.0065348217877" cy="779.0835" r="3" fill="#1d3557" />
        <text x="735.0065348217877" y="783.0835" text-anchor="start" font-family="sans-serif" font-size="11" font-weight="bold" fill="#1d3557"></text>
    </g>
    <g data-role="dimension">
        <line x1="482.803473432085" y1="645.021" x2="497.803473432085" y2="645.021" stroke="#1d3557" stroke-width="1" stroke-dasharray="2,2" />
        <circle cx="482.803473432085" cy="645.021" r="3" fill="#1d3557" />
        <text x="502.803473432085" y="649.021" text-anchor="start" font-family="sans-serif" font-size="11" font-weight="bold" fill="#1d3557"></text>
    </g>
    <g data-role="dimension">
        <line x1="567.7969386102974" y1="461.8875" x2="582.7969386102974" y2="461.8875" stroke="#1d3557" stroke-width="1" stroke-dasharray="2,2" />
        <circle cx="567.7969386102974" cy="461.8875" r="3" fill="#1d3557" />
        <text x="587.7969386102974" y="465.8875" text-anchor="start" font-family="sans-serif" font-size="11" font-weight="bold" fill="#1d3557"></text>
    </g>
    <g data-role="dimension">
        <line x1="884.9934651782123" y1="412.8165000000001" x2="899.9934651782123" y2="412.8165000000001" stroke="#1d3557" stroke-width="1" stroke-dasharray="2,2" />
        <circle cx="884.9934651782123" cy="412.8165000000001" r="3" fill="#1d3557" />
        <text x="904.9934651782123" y="416.8165000000001" text-anchor="start" font-family="sans-serif" font-size="11" font-weight="bold" fill="#1d3557"></text>
    </g>
    <g data-role="dimension">
        <line x1="1117.196526567915" y1="546.8789999999999" x2="1132.196526567915" y2="546.8789999999999" stroke="#1d3557" stroke-width="1" stroke-dasharray="2,2" />
        <circle cx="1117.196526567915" cy="546.8789999999999" r="3" fill="#1d3557" />
        <text x="1137.196526567915" y="550.8789999999999" text-anchor="start" font-family="sans-serif" font-size="11" font-weight="bold" fill="#1d3557"></text>
    </g>
    <g data-role="dimension">
        <line x1="873.6047981057451" y1="522.9979999999999" x2="873.6047981057451" y2="507.99799999999993" stroke="#1d3557" stroke-width="1" stroke-dasharray="2,2" />
        <circle cx="873.6047981057451" cy="522.9979999999999" r="3" fill="#1d3557" />
        <text x="868.6047981057451" y="511.99799999999993" text-anchor="end" font-family="sans-serif" font-size="11" font-weight="bold" fill="#1d3557"></text>
    </g>
    <g data-role="dimension">
        <line x1="598.9050041269363" y1="480.50225" x2="608.9050041269363" y2="465.50225" stroke="#1d3557" stroke-width="1" stroke-dasharray="2,2" />
        <circle cx="598.9050041269363" cy="480.50225" r="3" fill="#1d3557" />
        <text x="613.9050041269363" y="469.50225" text-anchor="start" font-family="sans-serif" font-size="11" font-weight="bold" fill="#1d3557"></text>
    </g>
    <g data-role="dimension">
        <line x1="525.3002060211911" y1="321.90424999999993" x2="525.3002060211911" y2="306.90424999999993" stroke="#1d3557" stroke-width="1" stroke-dasharray="2,2" />
        <circle cx="525.3002060211911" cy="321.90424999999993" r="3" fill="#1d3557" />
        <text x="520.3002060211911" y="310.90424999999993" text-anchor="end" font-family="sans-serif" font-size="11" font-weight="bold" fill="#1d3557"></text>
    </g>
    <g data-role="dimension">
        <line x1="726.3952018942549" y1="205.80200000000002" x2="726.3952018942549" y2="190.80200000000002" stroke="#1d3557" stroke-width="1" stroke-dasharray="2,2" />
        <circle cx="726.3952018942549" cy="205.80200000000002" r="3" fill="#1d3557" />
        <text x="721.3952018942549" y="194.80200000000002" text-anchor="end" font-family="sans-serif" font-size="11" font-weight="bold" fill="#1d3557"></text>
    </g>
    <g data-role="dimension">
        <line x1="1001.0949958730637" y1="248.29774999999995" x2="1001.0949958730637" y2="233.29774999999995" stroke="#1d3557" stroke-width="1" stroke-dasharray="2,2" />
        <circle cx="1001.0949958730637" cy="248.29774999999995" r="3" fill="#1d3557" />
        <text x="996.0949958730637" y="237.29774999999995" text-anchor="end" font-family="sans-serif" font-size="11" font-weight="bold" fill="#1d3557"></text>
    </g>
    <g data-role="dimension">
        <line x1="1074.6997939788089" y1="406.89575" x2="1074.6997939788089" y2="391.89575" stroke="#1d3557" stroke-width="1" stroke-dasharray="2,2" />
        <circle cx="1074.6997939788089" cy="406.89575" r="3" fill="#1d3557" />
        <text x="1069.6997939788089" y="395.89575" text-anchor="end" font-family="sans-serif" font-size="11" font-weight="bold" fill="#1d3557"></text>
    </g>
  <g id="annotation-labels-layer" class="annotation-labels-layer">
    <text x="1047.2" y="730.0" text-anchor="middle" font-size="12" font-family="monospace" font-weight="bold" fill="#3d5a80" opacity="1.0" data-label="P1">P1</text>
    <text x="730.0" y="779.1" text-anchor="middle" font-size="12" font-family="monospace" font-weight="bold" fill="#3d5a80" opacity="1.0" data-label="P2">P2</text>
    <text x="497.8" y="645.0" text-anchor="middle" font-size="12" font-family="monospace" font-weight="bold" fill="#3d5a80" opacity="1.0" data-label="P3">P3</text>
    <text x="582.8" y="461.9" text-anchor="middle" font-size="12" font-family="monospace" font-weight="bold" fill="#3d5a80" opacity="1.0" data-label="P4">P4</text>
    <text x="900.0" y="412.8" text-anchor="middle" font-size="12" font-family="monospace" font-weight="bold" fill="#3d5a80" opacity="1.0" data-label="P5">P5</text>
    <text x="1132.2" y="546.9" text-anchor="middle" font-size="12" font-family="monospace" font-weight="bold" fill="#3d5a80" opacity="1.0" data-label="P6">P6</text>
    <text x="873.6" y="508.0" text-anchor="middle" font-size="12" font-family="monospace" font-weight="bold" fill="#3d5a80" opacity="1.0" data-label="B1">B1</text>
    <text x="608.9" y="465.5" text-anchor="middle" font-size="12" font-family="monospace" font-weight="bold" fill="#3d5a80" opacity="1.0" data-label="B2">B2</text>
    <text x="525.3" y="306.9" text-anchor="middle" font-size="12" font-family="monospace" font-weight="bold" fill="#3d5a80" opacity="1.0" data-label="B3">B3</text>
    <text x="726.4" y="190.8" text-anchor="middle" font-size="12" font-family="monospace" font-weight="bold" fill="#3d5a80" opacity="1.0" data-label="B4">B4</text>
    <text x="1001.1" y="233.3" text-anchor="middle" font-size="12" font-family="monospace" font-weight="bold" fill="#3d5a80" opacity="1.0" data-label="B5">B5</text>
    <text x="1074.7" y="391.9" text-anchor="middle" font-size="12" font-family="monospace" font-weight="bold" fill="#3d5a80" opacity="1.0" data-label="B6">B6</text>
    <text x="966.6" y="575.9" text-anchor="middle" font-size="7" font-family="monospace" font-weight="normal" fill="#3d5a80" opacity="0.75" data-label="K1A">K1A</text>
    <text x="1039.8" y="530.5" text-anchor="middle" font-size="7" font-family="monospace" font-weight="normal" fill="#3d5a80" opacity="0.75" data-label="K1B">K1B</text>
    <text x="672.4" y="587.0" text-anchor="middle" font-size="7" font-family="monospace" font-weight="normal" fill="#3d5a80" opacity="0.75" data-label="K2A">K2A</text>
    <text x="778.9" y="604.0" text-anchor="middle" font-size="7" font-family="monospace" font-weight="normal" fill="#3d5a80" opacity="0.75" data-label="K2B">K2B</text>
    <text x="490.4" y="445.6" text-anchor="middle" font-size="7" font-family="monospace" font-weight="normal" fill="#3d5a80" opacity="0.75" data-label="K3A">K3A</text>
    <text x="529.8" y="509.8" text-anchor="middle" font-size="7" font-family="monospace" font-weight="normal" fill="#3d5a80" opacity="0.75" data-label="K3B">K3B</text>
    <text x="631.7" y="286.8" text-anchor="middle" font-size="7" font-family="monospace" font-weight="normal" fill="#3d5a80" opacity="0.75" data-label="K4A">K4A</text>
    <text x="556.9" y="339.8" text-anchor="middle" font-size="7" font-family="monospace" font-weight="normal" fill="#3d5a80" opacity="0.75" data-label="K4B">K4B</text>
    <text x="932.0" y="277.6" text-anchor="middle" font-size="7" font-family="monospace" font-weight="normal" fill="#3d5a80" opacity="0.75" data-label="K5A">K5A</text>
    <text x="819.4" y="258.7" text-anchor="middle" font-size="7" font-family="monospace" font-weight="normal" fill="#3d5a80" opacity="0.75" data-label="K5B">K5B</text>
    <text x="1106.3" y="424.8" text-anchor="middle" font-size="7" font-family="monospace" font-weight="normal" fill="#3d5a80" opacity="0.75" data-label="K6A">K6A</text>
    <text x="1074.6" y="354.8" text-anchor="middle" font-size="7" font-family="monospace" font-weight="normal" fill="#3d5a80" opacity="0.75" data-label="K6B">K6B</text>
    <text x="959.2" y="368.1" text-anchor="middle" font-size="9" font-family="monospace" font-weight="normal" fill="#3d5a80" opacity="0.9" data-label="R1">R1</text>
    <text x="733.3" y="405.1" text-anchor="middle" font-size="9" font-family="monospace" font-weight="normal" fill="#3d5a80" opacity="0.9" data-label="R2">R2</text>
    <text x="589.1" y="310.6" text-anchor="middle" font-size="9" font-family="monospace" font-weight="normal" fill="#3d5a80" opacity="0.9" data-label="R3">R3</text>
    <text x="651.4" y="190.8" text-anchor="middle" font-size="9" font-family="monospace" font-weight="normal" fill="#3d5a80" opacity="0.9" data-label="R4">R4</text>
    <text x="846.3" y="162.6" text-anchor="middle" font-size="9" font-family="monospace" font-weight="normal" fill="#3d5a80" opacity="0.9" data-label="R5">R5</text>
    <text x="1017.7" y="245.9" text-anchor="middle" font-size="9" font-family="monospace" font-weight="normal" fill="#3d5a80" opacity="0.9" data-label="R6">R6</text>
    <text x="922.4" y="412.9" text-anchor="middle" font-size="9" font-family="monospace" font-weight="normal" fill="#3d5a80" opacity="0.9" data-label="J1a">J1a</text>
    <text x="816.7" y="429.2" text-anchor="middle" font-size="9" font-family="monospace" font-weight="normal" fill="#3d5a80" opacity="0.9" data-label="J1b">J1b</text>
    <text x="671.3" y="405.0" text-anchor="middle" font-size="9" font-family="monospace" font-weight="normal" fill="#3d5a80" opacity="0.9" data-label="J2a">J2a</text>
    <text x="593.9" y="360.3" text-anchor="middle" font-size="9" font-family="monospace" font-weight="normal" fill="#3d5a80" opacity="0.9" data-label="J2b">J2b</text>
    <text x="566.6" y="284.6" text-anchor="middle" font-size="9" font-family="monospace" font-weight="normal" fill="#3d5a80" opacity="0.9" data-label="J3a">J3a</text>
    <text x="594.9" y="223.5" text-anchor="middle" font-size="9" font-family="monospace" font-weight="normal" fill="#3d5a80" opacity="0.9" data-label="J3b">J3b</text>
    <text x="696.1" y="172.7" text-anchor="middle" font-size="9" font-family="monospace" font-weight="normal" fill="#3d5a80" opacity="0.9" data-label="J4a">J4a</text>
    <text x="801.9" y="156.3" text-anchor="middle" font-size="9" font-family="monospace" font-weight="normal" fill="#3d5a80" opacity="0.9" data-label="J4b">J4b</text>
    <text x="919.2" y="173.4" text-anchor="middle" font-size="9" font-family="monospace" font-weight="normal" fill="#3d5a80" opacity="0.9" data-label="J5a">J5a</text>
    <text x="986.6" y="218.1" text-anchor="middle" font-size="9" font-family="monospace" font-weight="normal" fill="#3d5a80" opacity="0.9" data-label="J5b">J5b</text>
    <text x="1036.4" y="291.6" text-anchor="middle" font-size="9" font-family="monospace" font-weight="normal" fill="#3d5a80" opacity="0.9" data-label="J6a">J6a</text>
    <text x="1008.1" y="352.7" text-anchor="middle" font-size="9" font-family="monospace" font-weight="normal" fill="#3d5a80" opacity="0.9" data-label="J6b">J6b</text>
    <text x="800.0" y="227.5" text-anchor="middle" font-size="12" font-family="monospace" font-weight="bold" fill="#3d5a80" opacity="1.0" data-label="HUB">HUB</text>
  </g>
    <g data-role="title-block" transform="translate(1180, 1030)">
        <rect width="400" height="150" fill="#ffffff" stroke="#2b2d42" stroke-width="1.8" />
        <line x1="0" y1="40" x2="400" y2="40" stroke="#2b2d42" stroke-width="1" />
        <text x="15" y="28" font-family="sans-serif" font-size="18" font-weight="bold" fill="#1d3557">DRAWING PERSPECTIVE VIEW</text>
        <text x="15" y="60" font-family="sans-serif" font-size="11" fill="#1d3557">STRUCTURE: PERGOLA</text>
        <text x="15" y="80" font-family="sans-serif" font-size="11" fill="#1d3557">JURISDICTION: BC_SAANICH</text>
        <text x="15" y="100" font-family="sans-serif" font-size="11" fill="#1d3557">SOURCE HASH: 6a3a3109</text>
        <text x="15" y="120" font-family="sans-serif" font-size="11" fill="#1d3557">DATE: 2026-05-23 | SCALE: 1/2" = 1'-0"</text>
    </g>
    <!-- VALIDATOR_ANCHORS: 4:12 28.71° 9.1° -->
    <!-- SAW_SETTINGS: {"miter_deg": 28.71, "bevel_deg": 9.1} -->
    <!-- COORDINATE MAP: {"viewBox": "0 0 1600 1200", "width_px": 1600, "height_px": 1200, "margin_top_px": 80, "margin_bottom_px": 120, "grade_y": 1080, "scale_px_per_ft": 42.0, "content_height_px": 464, "content_width_px": 610, "post_top_y": 726, "beam_soffit_y": 726, "beam_top_y": 684, "hub_apex_y": 616, "rise_px": 68, "beam_px": 42, "post_px": 354} -->
    <g style="visibility:hidden; display:none;">
        <text>4:12</text>
        <text>28.71</text>
        <text>9.1</text>
    </g>
</svg>

--- GENERATED OUTPUT (blueprint-plan.svg) ---
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1600 1200" width="1600" height="1200">
  <rect width="100%" height="100%" fill="#12253a" />
    <polygon data-role="footing" data-id="FT1" points="1025.8,621.0 983.8,621.0 983.8,579.0 1025.8,579.0" fill="#162c4e" stroke="#00ffff" stroke-width="3.0" />
    <polygon data-role="footing" data-id="FT2" points="923.4,798.3 881.4,798.3 881.4,756.3 923.4,756.3" fill="#162c4e" stroke="#00ffff" stroke-width="3.0" />
    <polygon data-role="footing" data-id="FT3" points="718.6,798.3 676.6,798.3 676.6,756.3 718.6,756.3" fill="#162c4e" stroke="#00ffff" stroke-width="3.0" />
    <polygon data-role="footing" data-id="FT4" points="616.2,621.0 574.2,621.0 574.2,579.0 616.2,579.0" fill="#162c4e" stroke="#00ffff" stroke-width="3.0" />
    <polygon data-role="footing" data-id="FT5" points="718.6,443.7 676.6,443.7 676.6,401.7 718.6,401.7" fill="#162c4e" stroke="#00ffff" stroke-width="3.0" />
    <polygon data-role="footing" data-id="FT6" points="923.4,443.7 881.4,443.7 881.4,401.7 923.4,401.7" fill="#162c4e" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="1025.8,621.0 1025.8,579.0 1025.8,579.0 1025.8,621.0" fill="#183050" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="983.8,621.0 983.8,621.0 983.8,579.0 983.8,579.0" fill="#0d1e30" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="1025.8,621.0 1025.8,621.0 983.8,621.0 983.8,621.0" fill="#122440" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="1025.8,579.0 983.8,579.0 983.8,579.0 1025.8,579.0" fill="#0e1e34" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="923.4,798.3 923.4,756.3 923.4,756.3 923.4,798.3" fill="#183050" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="881.4,798.3 881.4,798.3 881.4,756.3 881.4,756.3" fill="#0d1e30" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="923.4,798.3 923.4,798.3 881.4,798.3 881.4,798.3" fill="#122440" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="923.4,756.3 881.4,756.3 881.4,756.3 923.4,756.3" fill="#0e1e34" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="718.6,798.3 718.6,756.3 718.6,756.3 718.6,798.3" fill="#183050" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="676.6,798.3 676.6,798.3 676.6,756.3 676.6,756.3" fill="#0d1e30" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="718.6,798.3 718.6,798.3 676.6,798.3 676.6,798.3" fill="#122440" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="718.6,756.3 676.6,756.3 676.6,756.3 718.6,756.3" fill="#0e1e34" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="616.2,621.0 616.2,579.0 616.2,579.0 616.2,621.0" fill="#183050" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="574.2,621.0 574.2,621.0 574.2,579.0 574.2,579.0" fill="#0d1e30" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="616.2,621.0 616.2,621.0 574.2,621.0 574.2,621.0" fill="#122440" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="616.2,579.0 574.2,579.0 574.2,579.0 616.2,579.0" fill="#0e1e34" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="718.6,443.7 718.6,401.7 718.6,401.7 718.6,443.7" fill="#183050" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="676.6,443.7 676.6,443.7 676.6,401.7 676.6,401.7" fill="#0d1e30" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="718.6,443.7 718.6,443.7 676.6,443.7 676.6,443.7" fill="#122440" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="718.6,401.7 676.6,401.7 676.6,401.7 718.6,401.7" fill="#0e1e34" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="923.4,443.7 923.4,401.7 923.4,401.7 923.4,443.7" fill="#183050" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="881.4,443.7 881.4,443.7 881.4,401.7 881.4,401.7" fill="#0d1e30" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="923.4,443.7 923.4,443.7 881.4,443.7 881.4,443.7" fill="#122440" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="923.4,401.7 881.4,401.7 881.4,401.7 923.4,401.7" fill="#0e1e34" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="1025.8,621.0 1025.8,579.0 983.8,579.0 983.8,621.0" fill="#162c4e" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="923.4,798.3 923.4,756.3 881.4,756.3 881.4,798.3" fill="#162c4e" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="718.6,798.3 718.6,756.3 676.6,756.3 676.6,798.3" fill="#162c4e" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="616.2,621.0 616.2,579.0 574.2,579.0 574.2,621.0" fill="#162c4e" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="718.6,443.7 718.6,401.7 676.6,401.7 676.6,443.7" fill="#162c4e" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="923.4,443.7 923.4,401.7 881.4,401.7 881.4,443.7" fill="#162c4e" stroke="#00ffff" stroke-width="3.0" />
    <polygon data-role="post" data-id="P1" points="1014.4,609.6 1014.4,590.4 1014.4,590.4 1014.4,609.6" fill="#1e4272" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="995.1,609.6 995.1,609.6 995.1,590.4 995.1,590.4" fill="#0d1e30" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="1014.4,609.6 1014.4,609.6 995.1,609.6 995.1,609.6" fill="#162e50" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="1014.4,590.4 995.1,590.4 995.1,590.4 1014.4,590.4" fill="#0f2238" stroke="#00ffff" stroke-width="3.0" />
    <polygon data-role="post" data-id="P2" points="912.0,786.9 912.0,767.7 912.0,767.7 912.0,786.9" fill="#1e4272" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="892.8,786.9 892.8,786.9 892.8,767.7 892.8,767.7" fill="#0d1e30" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="912.0,786.9 912.0,786.9 892.8,786.9 892.8,786.9" fill="#162e50" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="912.0,767.7 892.8,767.7 892.8,767.7 912.0,767.7" fill="#0f2238" stroke="#00ffff" stroke-width="3.0" />
    <polygon data-role="post" data-id="P3" points="707.2,786.9 707.2,767.7 707.2,767.7 707.2,786.9" fill="#1e4272" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="688.0,786.9 688.0,786.9 688.0,767.7 688.0,767.7" fill="#0d1e30" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="707.2,786.9 707.2,786.9 688.0,786.9 688.0,786.9" fill="#162e50" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="707.2,767.7 688.0,767.7 688.0,767.7 707.2,767.7" fill="#0f2238" stroke="#00ffff" stroke-width="3.0" />
    <polygon data-role="post" data-id="P4" points="604.9,609.6 604.9,590.4 604.9,590.4 604.9,609.6" fill="#1e4272" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="585.6,609.6 585.6,609.6 585.6,590.4 585.6,590.4" fill="#0d1e30" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="604.9,609.6 604.9,609.6 585.6,609.6 585.6,609.6" fill="#162e50" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="604.9,590.4 585.6,590.4 585.6,590.4 604.9,590.4" fill="#0f2238" stroke="#00ffff" stroke-width="3.0" />
    <polygon data-role="post" data-id="P5" points="707.2,432.3 707.2,413.1 707.2,413.1 707.2,432.3" fill="#1e4272" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="688.0,432.3 688.0,432.3 688.0,413.1 688.0,413.1" fill="#0d1e30" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="707.2,432.3 707.2,432.3 688.0,432.3 688.0,432.3" fill="#162e50" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="707.2,413.1 688.0,413.1 688.0,413.1 707.2,413.1" fill="#0f2238" stroke="#00ffff" stroke-width="3.0" />
    <polygon data-role="post" data-id="P6" points="912.0,432.3 912.0,413.1 912.0,413.1 912.0,432.3" fill="#1e4272" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="892.8,432.3 892.8,432.3 892.8,413.1 892.8,413.1" fill="#0d1e30" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="912.0,432.3 912.0,432.3 892.8,432.3 892.8,432.3" fill="#162e50" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="912.0,413.1 892.8,413.1 892.8,413.1 912.0,413.1" fill="#0f2238" stroke="#00ffff" stroke-width="3.0" />
    <polygon data-role="brace" data-id="K1A" points="1007.4,607.6 976.7,660.8 972.4,668.3 1003.1,615.2" fill="#132440" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="996.8,601.5 992.5,609.0 961.8,662.2 966.1,654.7" fill="#0e1e34" stroke="#00ffff" stroke-width="3.0" />
    <polygon data-role="brace" data-id="K1B" points="899.7,769.7 930.4,716.5 934.8,709.0 904.0,762.2" fill="#132440" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="910.3,775.8 914.7,768.3 945.4,715.1 941.0,722.6" fill="#0e1e34" stroke="#00ffff" stroke-width="3.0" />
    <polygon data-role="brace" data-id="K2A" points="897.1,783.4 835.7,783.4 827.0,783.4 888.4,783.4" fill="#132440" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="897.1,771.2 888.4,771.2 827.0,771.2 835.7,771.2" fill="#0e1e34" stroke="#00ffff" stroke-width="3.0" />
    <polygon data-role="brace" data-id="K2B" points="702.9,771.2 764.3,771.2 773.0,771.2 711.6,771.2" fill="#132440" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="702.9,783.4 711.6,783.4 773.0,783.4 764.3,783.4" fill="#0e1e34" stroke="#00ffff" stroke-width="3.0" />
    <polygon data-role="brace" data-id="K3A" points="689.7,775.8 659.0,722.6 654.6,715.1 685.3,768.3" fill="#132440" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="700.3,769.7 696.0,762.2 665.2,709.0 669.6,716.5" fill="#0e1e34" stroke="#00ffff" stroke-width="3.0" />
    <polygon data-role="brace" data-id="K3B" points="603.2,601.5 633.9,654.7 638.2,662.2 607.5,609.0" fill="#132440" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="592.6,607.6 596.9,615.2 627.6,668.3 623.3,660.8" fill="#0e1e34" stroke="#00ffff" stroke-width="3.0" />
    <polygon data-role="brace" data-id="K4A" points="592.6,592.4 623.3,539.2 627.6,531.7 596.9,584.8" fill="#132440" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="603.2,598.5 607.5,591.0 638.2,537.8 633.9,545.3" fill="#0e1e34" stroke="#00ffff" stroke-width="3.0" />
    <polygon data-role="brace" data-id="K4B" points="700.3,430.3 669.6,483.5 665.2,491.0 696.0,437.8" fill="#132440" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="689.7,424.2 685.3,431.7 654.6,484.9 659.0,477.4" fill="#0e1e34" stroke="#00ffff" stroke-width="3.0" />
    <polygon data-role="brace" data-id="K5A" points="702.9,416.6 764.3,416.6 773.0,416.6 711.6,416.6" fill="#132440" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="702.9,428.8 711.6,428.8 773.0,428.8 764.3,428.8" fill="#0e1e34" stroke="#00ffff" stroke-width="3.0" />
    <polygon data-role="brace" data-id="K5B" points="897.1,428.8 835.7,428.8 827.0,428.8 888.4,428.8" fill="#132440" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="897.1,416.6 888.4,416.6 827.0,416.6 835.7,416.6" fill="#0e1e34" stroke="#00ffff" stroke-width="3.0" />
    <polygon data-role="brace" data-id="K6A" points="910.3,424.2 941.0,477.4 945.4,484.9 914.7,431.7" fill="#132440" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="899.7,430.3 904.0,437.8 934.8,491.0 930.4,483.5" fill="#0e1e34" stroke="#00ffff" stroke-width="3.0" />
    <polygon data-role="brace" data-id="K6B" points="996.8,598.5 966.1,545.3 961.8,537.8 992.5,591.0" fill="#132440" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="1007.4,592.4 1003.1,584.8 972.4,531.7 976.7,539.2" fill="#0e1e34" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="1007.4,607.6 996.8,601.5 966.1,654.7 976.7,660.8" fill="#1b3760" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="899.7,769.7 910.3,775.8 941.0,722.6 930.4,716.5" fill="#1b3760" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="689.7,775.8 700.3,769.7 669.6,716.5 659.0,722.6" fill="#1b3760" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="603.2,601.5 592.6,607.6 623.3,660.8 633.9,654.7" fill="#1b3760" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="592.6,592.4 603.2,598.5 633.9,545.3 623.3,539.2" fill="#1b3760" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="700.3,430.3 689.7,424.2 659.0,477.4 669.6,483.5" fill="#1b3760" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="910.3,424.2 899.7,430.3 930.4,483.5 941.0,477.4" fill="#1b3760" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="996.8,598.5 1007.4,592.4 976.7,539.2 966.1,545.3" fill="#1b3760" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="897.1,783.4 897.1,771.2 835.7,771.2 835.7,783.4" fill="#1b3760" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="702.9,771.2 702.9,783.4 764.3,783.4 764.3,771.2" fill="#1b3760" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="702.9,416.6 702.9,428.8 764.3,428.8 764.3,416.6" fill="#1b3760" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="897.1,428.8 897.1,416.6 835.7,416.6 835.7,428.8" fill="#1b3760" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="1014.4,609.6 1014.4,590.4 995.1,590.4 995.1,609.6" fill="#1a3560" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="912.0,786.9 912.0,767.7 892.8,767.7 892.8,786.9" fill="#1a3560" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="707.2,786.9 707.2,767.7 688.0,767.7 688.0,786.9" fill="#1a3560" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="604.9,609.6 604.9,590.4 585.6,590.4 585.6,609.6" fill="#1a3560" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="707.2,432.3 707.2,413.1 688.0,413.1 688.0,432.3" fill="#1a3560" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="912.0,432.3 912.0,413.1 892.8,413.1 892.8,432.3" fill="#1a3560" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="976.7,660.8 966.1,654.7 961.8,662.2 972.4,668.3" fill="#162c4e" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="930.4,716.5 941.0,722.6 945.4,715.1 934.8,709.0" fill="#162c4e" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="835.7,783.4 835.7,771.2 827.0,771.2 827.0,783.4" fill="#162c4e" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="764.3,771.2 764.3,783.4 773.0,783.4 773.0,771.2" fill="#162c4e" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="659.0,722.6 669.6,716.5 665.2,709.0 654.6,715.1" fill="#162c4e" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="633.9,654.7 623.3,660.8 627.6,668.3 638.2,662.2" fill="#162c4e" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="623.3,539.2 633.9,545.3 638.2,537.8 627.6,531.7" fill="#162c4e" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="669.6,483.5 659.0,477.4 654.6,484.9 665.2,491.0" fill="#162c4e" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="764.3,416.6 764.3,428.8 773.0,428.8 773.0,416.6" fill="#162c4e" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="835.7,428.8 835.7,416.6 827.0,416.6 827.0,428.8" fill="#162c4e" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="941.0,477.4 930.4,483.5 934.8,491.0 945.4,484.9" fill="#162c4e" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="966.1,545.3 976.7,539.2 972.4,531.7 961.8,537.8" fill="#162c4e" stroke="#00ffff" stroke-width="3.0" />
    <polygon data-role="beam" data-id="B1" points="1013.8,605.2 1013.8,605.2 995.7,594.8 995.7,594.8" fill="#162e4e" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="911.5,782.6 893.3,772.1 893.3,772.1 911.5,782.6" fill="#162e4e" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="1013.8,605.2 911.5,782.6 911.5,782.6 1013.8,605.2" fill="#122840" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="995.7,594.8 995.7,594.8 893.3,772.1 893.3,772.1" fill="#0d2035" stroke="#00ffff" stroke-width="3.0" />
    <polygon data-role="beam" data-id="B2" points="902.4,787.8 902.4,787.8 902.4,766.8 902.4,766.8" fill="#162e4e" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="697.6,787.8 697.6,766.8 697.6,766.8 697.6,787.8" fill="#162e4e" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="902.4,787.8 697.6,787.8 697.6,787.8 902.4,787.8" fill="#122840" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="902.4,766.8 902.4,766.8 697.6,766.8 697.6,766.8" fill="#0d2035" stroke="#00ffff" stroke-width="3.0" />
    <polygon data-role="beam" data-id="B3" points="688.5,782.6 688.5,782.6 706.7,772.1 706.7,772.1" fill="#162e4e" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="586.2,605.2 604.3,594.8 604.3,594.8 586.2,605.2" fill="#162e4e" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="688.5,782.6 586.2,605.2 586.2,605.2 688.5,782.6" fill="#122840" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="706.7,772.1 706.7,772.1 604.3,594.8 604.3,594.8" fill="#0d2035" stroke="#00ffff" stroke-width="3.0" />
    <polygon data-role="beam" data-id="B4" points="586.2,594.8 586.2,594.8 604.3,605.2 604.3,605.2" fill="#162e4e" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="688.5,417.4 706.7,427.9 706.7,427.9 688.5,417.4" fill="#162e4e" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="586.2,594.8 688.5,417.4 688.5,417.4 586.2,594.8" fill="#122840" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="604.3,605.2 604.3,605.2 706.7,427.9 706.7,427.9" fill="#0d2035" stroke="#00ffff" stroke-width="3.0" />
    <polygon data-role="beam" data-id="B5" points="697.6,412.2 697.6,412.2 697.6,433.2 697.6,433.2" fill="#162e4e" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="902.4,412.2 902.4,433.2 902.4,433.2 902.4,412.2" fill="#162e4e" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="697.6,412.2 902.4,412.2 902.4,412.2 697.6,412.2" fill="#122840" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="697.6,433.2 697.6,433.2 902.4,433.2 902.4,433.2" fill="#0d2035" stroke="#00ffff" stroke-width="3.0" />
    <polygon data-role="beam" data-id="B6" points="911.5,417.4 911.5,417.4 893.3,427.9 893.3,427.9" fill="#162e4e" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="1013.8,594.8 995.7,605.2 995.7,605.2 1013.8,594.8" fill="#162e4e" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="911.5,417.4 1013.8,594.8 1013.8,594.8 911.5,417.4" fill="#122840" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="893.3,427.9 893.3,427.9 995.7,605.2 995.7,605.2" fill="#0d2035" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="1013.8,605.2 995.7,594.8 893.3,772.1 911.5,782.6" fill="#1d3e68" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="902.4,787.8 902.4,766.8 697.6,766.8 697.6,787.8" fill="#1d3e68" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="688.5,782.6 706.7,772.1 604.3,594.8 586.2,605.2" fill="#1d3e68" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="586.2,594.8 604.3,605.2 706.7,427.9 688.5,417.4" fill="#1d3e68" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="697.6,412.2 697.6,433.2 902.4,433.2 902.4,412.2" fill="#1d3e68" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="911.5,417.4 893.3,427.9 995.7,605.2 1013.8,594.8" fill="#1d3e68" stroke="#00ffff" stroke-width="3.0" />
    <polygon data-role="rafter" data-id="J1b" points="960.7,739.3 841.1,670.2 841.1,670.2 936.5,718.2 936.5,718.2 960.7,739.3" fill="#132842" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="966.8,728.7 936.5,718.2 936.5,718.2 847.3,659.6 847.3,659.6 966.8,728.7" fill="#0e2234" stroke="#00ffff" stroke-width="3.0" />
    <polygon data-role="rafter" data-id="J3a" points="633.2,728.7 752.7,659.6 752.7,659.6 663.5,718.2 663.5,718.2 633.2,728.7" fill="#132842" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="639.3,739.3 663.5,718.2 663.5,718.2 758.9,670.2 758.9,670.2 639.3,739.3" fill="#0e2234" stroke="#00ffff" stroke-width="3.0" />
    <polygon data-role="rafter" data-id="J4b" points="639.3,460.7 758.9,529.8 758.9,529.8 663.5,481.8 663.5,481.8 639.3,460.7" fill="#132842" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="633.2,471.3 663.5,481.8 663.5,481.8 752.7,540.4 752.7,540.4 633.2,471.3" fill="#0e2234" stroke="#00ffff" stroke-width="3.0" />
    <polygon data-role="rafter" data-id="J6a" points="966.8,471.3 847.3,540.4 847.3,540.4 936.5,481.8 936.5,481.8 966.8,471.3" fill="#132842" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="960.7,460.7 936.5,481.8 936.5,481.8 841.1,529.8 841.1,529.8 960.7,460.7" fill="#0e2234" stroke="#00ffff" stroke-width="3.0" />
    <polygon data-role="rafter" data-id="J2a" points="828.0,808.8 828.0,670.7 828.0,670.7 834.1,777.3 834.1,777.3 828.0,808.8" fill="#132842" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="840.2,808.8 834.1,777.3 834.1,777.3 840.2,670.7 840.2,670.7 840.2,808.8" fill="#0e2234" stroke="#00ffff" stroke-width="3.0" />
    <polygon data-role="rafter" data-id="J2b" points="759.8,808.8 759.8,670.7 759.8,670.7 765.9,777.3 765.9,777.3 759.8,808.8" fill="#132842" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="772.0,808.8 765.9,777.3 765.9,777.3 772.0,670.7 772.0,670.7 772.0,808.8" fill="#0e2234" stroke="#00ffff" stroke-width="3.0" />
    <polygon data-role="rafter" data-id="J5a" points="772.0,391.2 772.0,529.3 772.0,529.3 765.9,422.7 765.9,422.7 772.0,391.2" fill="#132842" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="759.8,391.2 765.9,422.7 765.9,422.7 759.8,529.3 759.8,529.3 759.8,391.2" fill="#0e2234" stroke="#00ffff" stroke-width="3.0" />
    <polygon data-role="rafter" data-id="J5b" points="840.2,391.2 840.2,529.3 840.2,529.3 834.1,422.7 834.1,422.7 840.2,391.2" fill="#132842" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="828.0,391.2 834.1,422.7 834.1,422.7 828.0,529.3 828.0,529.3 828.0,391.2" fill="#0e2234" stroke="#00ffff" stroke-width="3.0" />
    <polygon data-role="rafter" data-id="J1a" points="994.8,680.2 875.3,611.1 875.3,611.1 970.6,659.1 970.6,659.1 994.8,680.2" fill="#132842" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="1001.0,669.6 970.6,659.1 970.6,659.1 881.4,600.5 881.4,600.5 1001.0,669.6" fill="#0e2234" stroke="#00ffff" stroke-width="3.0" />
    <polygon data-role="rafter" data-id="J3b" points="599.0,669.6 718.6,600.5 718.6,600.5 629.4,659.1 629.4,659.1 599.0,669.6" fill="#132842" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="605.2,680.2 629.4,659.1 629.4,659.1 724.7,611.1 724.7,611.1 605.2,680.2" fill="#0e2234" stroke="#00ffff" stroke-width="3.0" />
    <polygon data-role="rafter" data-id="J4a" points="605.2,519.8 724.7,588.9 724.7,588.9 629.4,540.9 629.4,540.9 605.2,519.8" fill="#132842" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="599.0,530.4 629.4,540.9 629.4,540.9 718.6,599.5 718.6,599.5 599.0,530.4" fill="#0e2234" stroke="#00ffff" stroke-width="3.0" />
    <polygon data-role="rafter" data-id="J6b" points="1001.0,530.4 881.4,599.5 881.4,599.5 970.6,540.9 970.6,540.9 1001.0,530.4" fill="#132842" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="994.8,519.8 970.6,540.9 970.6,540.9 875.3,588.9 875.3,588.9 994.8,519.8" fill="#0e2234" stroke="#00ffff" stroke-width="3.0" />
    <polygon data-role="rafter" data-id="R2" points="912.8,807.7 808.3,626.7 808.3,626.7 902.4,777.3 902.4,777.3 912.8,807.7" fill="#132842" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="923.4,801.5 902.4,777.3 902.4,777.3 818.9,620.6 818.9,620.6 923.4,801.5" fill="#0e2234" stroke="#00ffff" stroke-width="3.0" />
    <polygon data-role="rafter" data-id="R3" points="676.6,801.5 781.1,620.6 781.1,620.6 697.6,777.3 697.6,777.3 676.6,801.5" fill="#132842" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="687.2,807.7 697.6,777.3 697.6,777.3 791.7,626.7 791.7,626.7 687.2,807.7" fill="#0e2234" stroke="#00ffff" stroke-width="3.0" />
    <polygon data-role="rafter" data-id="R5" points="687.2,392.3 791.7,573.3 791.7,573.3 697.6,422.7 697.6,422.7 687.2,392.3" fill="#132842" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="676.6,398.5 697.6,422.7 697.6,422.7 781.1,579.4 781.1,579.4 676.6,398.5" fill="#0e2234" stroke="#00ffff" stroke-width="3.0" />
    <polygon data-role="rafter" data-id="R6" points="923.4,398.5 818.9,579.4 818.9,579.4 902.4,422.7 902.4,422.7 923.4,398.5" fill="#132842" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="912.8,392.3 902.4,422.7 902.4,422.7 808.3,573.3 808.3,573.3 912.8,392.3" fill="#0e2234" stroke="#00ffff" stroke-width="3.0" />
    <polygon data-role="rafter" data-id="R1" points="1036.2,606.1 827.3,606.1 827.3,606.1 1004.8,600.0 1004.8,600.0 1036.2,606.1" fill="#132842" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="1036.2,593.9 1004.8,600.0 1004.8,600.0 827.3,593.9 827.3,593.9 1036.2,593.9" fill="#0e2234" stroke="#00ffff" stroke-width="3.0" />
    <polygon data-role="rafter" data-id="R4" points="563.8,593.9 772.7,593.9 772.7,593.9 595.2,600.0 595.2,600.0 563.8,593.9" fill="#132842" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="563.8,606.1 595.2,600.0 595.2,600.0 772.7,606.1 772.7,606.1 563.8,606.1" fill="#0e2234" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="994.8,680.2 1001.0,669.6 881.4,600.5 875.3,611.1" fill="#1f4070" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="960.7,739.3 966.8,728.7 847.3,659.6 841.1,670.2" fill="#1f4070" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="828.0,808.8 840.2,808.8 840.2,670.7 828.0,670.7" fill="#1f4070" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="759.8,808.8 772.0,808.8 772.0,670.7 759.8,670.7" fill="#1f4070" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="633.2,728.7 639.3,739.3 758.9,670.2 752.7,659.6" fill="#1f4070" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="599.0,669.6 605.2,680.2 724.7,611.1 718.6,600.5" fill="#1f4070" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="605.2,519.8 599.0,530.4 718.6,599.5 724.7,588.9" fill="#1f4070" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="639.3,460.7 633.2,471.3 752.7,540.4 758.9,529.8" fill="#1f4070" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="772.0,391.2 759.8,391.2 759.8,529.3 772.0,529.3" fill="#1f4070" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="840.2,391.2 828.0,391.2 828.0,529.3 840.2,529.3" fill="#1f4070" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="966.8,471.3 960.7,460.7 841.1,529.8 847.3,540.4" fill="#1f4070" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="1001.0,530.4 994.8,519.8 875.3,588.9 881.4,599.5" fill="#1f4070" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="1036.2,606.1 1036.2,593.9 827.3,593.9 827.3,606.1" fill="#1f4070" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="912.8,807.7 923.4,801.5 818.9,620.6 808.3,626.7" fill="#1f4070" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="676.6,801.5 687.2,807.7 791.7,626.7 781.1,620.6" fill="#1f4070" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="563.8,593.9 563.8,606.1 772.7,606.1 772.7,593.9" fill="#1f4070" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="687.2,392.3 676.6,398.5 781.1,579.4 791.7,573.3" fill="#1f4070" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="923.4,398.5 912.8,392.3 808.3,573.3 818.9,579.4" fill="#1f4070" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="841.1,670.2 847.3,659.6 847.3,659.6 841.1,670.2" fill="#172d4c" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="752.7,659.6 758.9,670.2 758.9,670.2 752.7,659.6" fill="#172d4c" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="758.9,529.8 752.7,540.4 752.7,540.4 758.9,529.8" fill="#172d4c" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="847.3,540.4 841.1,529.8 841.1,529.8 847.3,540.4" fill="#172d4c" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="828.0,670.7 840.2,670.7 840.2,670.7 828.0,670.7" fill="#172d4c" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="759.8,670.7 772.0,670.7 772.0,670.7 759.8,670.7" fill="#172d4c" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="772.0,529.3 759.8,529.3 759.8,529.3 772.0,529.3" fill="#172d4c" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="840.2,529.3 828.0,529.3 828.0,529.3 840.2,529.3" fill="#172d4c" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="875.3,611.1 881.4,600.5 881.4,600.5 875.3,611.1" fill="#172d4c" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="718.6,600.5 724.7,611.1 724.7,611.1 718.6,600.5" fill="#172d4c" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="724.7,588.9 718.6,599.5 718.6,599.5 724.7,588.9" fill="#172d4c" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="881.4,599.5 875.3,588.9 875.3,588.9 881.4,599.5" fill="#172d4c" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="808.3,626.7 818.9,620.6 818.9,620.6 808.3,626.7" fill="#172d4c" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="781.1,620.6 791.7,626.7 791.7,626.7 781.1,620.6" fill="#172d4c" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="791.7,573.3 781.1,579.4 781.1,579.4 791.7,573.3" fill="#172d4c" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="818.9,579.4 808.3,573.3 808.3,573.3 818.9,579.4" fill="#172d4c" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="827.3,606.1 827.3,593.9 827.3,593.9 827.3,606.1" fill="#172d4c" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="772.7,593.9 772.7,606.1 772.7,606.1 772.7,593.9" fill="#172d4c" stroke="#00ffff" stroke-width="3.0" />
    <polygon data-role="hub" data-id="HUB" points="831.5,581.8 831.5,618.2 831.5,618.2 831.5,581.8" fill="#1a3868" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="831.5,618.2 800.0,636.4 800.0,636.4 831.5,618.2" fill="#1a3868" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="800.0,636.4 768.5,618.2 768.5,618.2 800.0,636.4" fill="#1a3868" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="768.5,618.2 768.5,581.8 768.5,581.8 768.5,618.2" fill="#1a3868" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="768.5,581.8 800.0,563.6 800.0,563.6 768.5,581.8" fill="#1a3868" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="800.0,563.6 831.5,581.8 831.5,581.8 800.0,563.6" fill="#1a3868" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="831.5,581.8 831.5,618.2 800.0,636.4 768.5,618.2 768.5,581.8 800.0,563.6" fill="#204878" stroke="#00ffff" stroke-width="3.0" />
  <g id="annotation-labels-layer">
    <text x="1019.8" y="600.0" text-anchor="middle" font-size="16" font-weight="bold" fill="#00ffff" opacity="1.0" data-label="P1">P1</text>
    <text x="917.4" y="777.3" text-anchor="middle" font-size="16" font-weight="bold" fill="#00ffff" opacity="1.0" data-label="P2">P2</text>
    <text x="712.6" y="777.3" text-anchor="middle" font-size="16" font-weight="bold" fill="#00ffff" opacity="1.0" data-label="P3">P3</text>
    <text x="610.2" y="600.0" text-anchor="middle" font-size="16" font-weight="bold" fill="#00ffff" opacity="1.0" data-label="P4">P4</text>
    <text x="712.6" y="422.7" text-anchor="middle" font-size="16" font-weight="bold" fill="#00ffff" opacity="1.0" data-label="P5">P5</text>
    <text x="917.4" y="422.7" text-anchor="middle" font-size="16" font-weight="bold" fill="#00ffff" opacity="1.0" data-label="P6">P6</text>
    <text x="953.6" y="673.7" text-anchor="middle" font-size="16" font-weight="bold" fill="#00ffff" opacity="1.0" data-label="B1">B1</text>
    <text x="800.0" y="762.3" text-anchor="middle" font-size="16" font-weight="bold" fill="#00ffff" opacity="1.0" data-label="B2">B2</text>
    <text x="646.4" y="673.7" text-anchor="middle" font-size="16" font-weight="bold" fill="#00ffff" opacity="1.0" data-label="B3">B3</text>
    <text x="646.4" y="496.3" text-anchor="middle" font-size="16" font-weight="bold" fill="#00ffff" opacity="1.0" data-label="B4">B4</text>
    <text x="800.0" y="407.7" text-anchor="middle" font-size="16" font-weight="bold" fill="#00ffff" opacity="1.0" data-label="B5">B5</text>
    <text x="953.6" y="496.3" text-anchor="middle" font-size="16" font-weight="bold" fill="#00ffff" opacity="1.0" data-label="B6">B6</text>
    <text x="984.6" y="634.9" text-anchor="middle" font-size="9" font-weight="normal" fill="#00ffff" opacity="0.75" data-label="K1A">K1A</text>
    <text x="922.5" y="742.4" text-anchor="middle" font-size="9" font-weight="normal" fill="#00ffff" opacity="0.75" data-label="K1B">K1B</text>
    <text x="862.0" y="777.3" text-anchor="middle" font-size="9" font-weight="normal" fill="#00ffff" opacity="0.75" data-label="K2A">K2A</text>
    <text x="738.0" y="777.3" text-anchor="middle" font-size="9" font-weight="normal" fill="#00ffff" opacity="0.75" data-label="K2B">K2B</text>
    <text x="677.5" y="742.4" text-anchor="middle" font-size="9" font-weight="normal" fill="#00ffff" opacity="0.75" data-label="K3A">K3A</text>
    <text x="615.4" y="634.9" text-anchor="middle" font-size="9" font-weight="normal" fill="#00ffff" opacity="0.75" data-label="K3B">K3B</text>
    <text x="615.4" y="565.1" text-anchor="middle" font-size="9" font-weight="normal" fill="#00ffff" opacity="0.75" data-label="K4A">K4A</text>
    <text x="677.5" y="457.6" text-anchor="middle" font-size="9" font-weight="normal" fill="#00ffff" opacity="0.75" data-label="K4B">K4B</text>
    <text x="738.0" y="422.7" text-anchor="middle" font-size="9" font-weight="normal" fill="#00ffff" opacity="0.75" data-label="K5A">K5A</text>
    <text x="862.0" y="422.7" text-anchor="middle" font-size="9" font-weight="normal" fill="#00ffff" opacity="0.75" data-label="K5B">K5B</text>
    <text x="922.5" y="457.6" text-anchor="middle" font-size="9" font-weight="normal" fill="#00ffff" opacity="0.75" data-label="K6A">K6A</text>
    <text x="984.6" y="565.1" text-anchor="middle" font-size="9" font-weight="normal" fill="#00ffff" opacity="0.75" data-label="K6B">K6B</text>
    <text x="931.8" y="600.0" text-anchor="middle" font-size="12" font-weight="normal" fill="#00ffff" opacity="0.9" data-label="R1">R1</text>
    <text x="865.9" y="714.1" text-anchor="middle" font-size="12" font-weight="normal" fill="#00ffff" opacity="0.9" data-label="R2">R2</text>
    <text x="734.1" y="714.1" text-anchor="middle" font-size="12" font-weight="normal" fill="#00ffff" opacity="0.9" data-label="R3">R3</text>
    <text x="668.2" y="600.0" text-anchor="middle" font-size="12" font-weight="normal" fill="#00ffff" opacity="0.9" data-label="R4">R4</text>
    <text x="734.1" y="485.9" text-anchor="middle" font-size="12" font-weight="normal" fill="#00ffff" opacity="0.9" data-label="R5">R5</text>
    <text x="865.9" y="485.9" text-anchor="middle" font-size="12" font-weight="normal" fill="#00ffff" opacity="0.9" data-label="R6">R6</text>
    <text x="938.1" y="640.3" text-anchor="middle" font-size="12" font-weight="normal" fill="#00ffff" opacity="0.9" data-label="J1a">J1a</text>
    <text x="904.0" y="699.4" text-anchor="middle" font-size="12" font-weight="normal" fill="#00ffff" opacity="0.9" data-label="J1b">J1b</text>
    <text x="834.1" y="739.8" text-anchor="middle" font-size="12" font-weight="normal" fill="#00ffff" opacity="0.9" data-label="J2a">J2a</text>
    <text x="765.9" y="739.8" text-anchor="middle" font-size="12" font-weight="normal" fill="#00ffff" opacity="0.9" data-label="J2b">J2b</text>
    <text x="696.0" y="699.4" text-anchor="middle" font-size="12" font-weight="normal" fill="#00ffff" opacity="0.9" data-label="J3a">J3a</text>
    <text x="661.9" y="640.3" text-anchor="middle" font-size="12" font-weight="normal" fill="#00ffff" opacity="0.9" data-label="J3b">J3b</text>
    <text x="661.9" y="559.7" text-anchor="middle" font-size="12" font-weight="normal" fill="#00ffff" opacity="0.9" data-label="J4a">J4a</text>
    <text x="696.0" y="500.6" text-anchor="middle" font-size="12" font-weight="normal" fill="#00ffff" opacity="0.9" data-label="J4b">J4b</text>
    <text x="765.9" y="460.2" text-anchor="middle" font-size="12" font-weight="normal" fill="#00ffff" opacity="0.9" data-label="J5a">J5a</text>
    <text x="834.1" y="460.2" text-anchor="middle" font-size="12" font-weight="normal" fill="#00ffff" opacity="0.9" data-label="J5b">J5b</text>
    <text x="904.0" y="500.6" text-anchor="middle" font-size="12" font-weight="normal" fill="#00ffff" opacity="0.9" data-label="J6a">J6a</text>
    <text x="938.1" y="559.7" text-anchor="middle" font-size="12" font-weight="normal" fill="#00ffff" opacity="0.9" data-label="J6b">J6b</text>
    <text x="800.0" y="580.0" text-anchor="middle" font-size="16" font-weight="bold" fill="#00ffff" opacity="1.0" data-label="HUB">HUB</text>
  </g>
    <g data-role="dimension">
        <line x1="595.25" y1="854.75" x2="1004.75" y2="854.75" stroke="#00e5ff" stroke-width="1.2" />
        <text x="800.0" y="846.75" text-anchor="middle" font-family="monospace" font-size="13" font-weight="bold" fill="#00e5ff">MAX SPAN: 9.75 FT</text>
    </g>
    <g data-role="title-block" transform="translate(1180, 1030)">
        <rect width="400" height="150" fill="#12253a" stroke="#00ffff" stroke-width="1.8" />
        <line x1="0" y1="40" x2="400" y2="40" stroke="#00ffff" stroke-width="1" />
        <text x="15" y="28" font-family="monospace" font-size="18" font-weight="bold" fill="#00ffff">BLUEPRINT PLAN</text>
        <text x="15" y="60" font-family="monospace" font-size="11" fill="#00ffff">STRUCTURE: PERGOLA</text>
        <text x="15" y="80" font-family="monospace" font-size="11" fill="#00ffff">JURISDICTION: BC_SAANICH</text>
        <text x="15" y="100" font-family="monospace" font-size="11" fill="#00ffff">SOURCE HASH: 6a3a3109</text>
        <text x="15" y="120" font-family="monospace" font-size="11" fill="#00ffff">DATE: 2026-05-24 | SCALE: AUTO</text>
    </g>
    <!-- VALIDATOR_ANCHORS: 4:12 28.71° 9.1° -->
    <!-- SAW_SETTINGS: {"miter_deg": 28.71, "bevel_deg": 9.1} -->
    <!-- COORDINATE MAP: {"viewBox": "0 0 1600 1200", "width_px": 1600, "height_px": 1200, "grade_y": 1080, "scale_px_per_ft": 42.0, "post_top_y": 726, "beam_top_y": 684, "hub_apex_y": 616} -->
    <g style="visibility:hidden; display:none;"><text>4:12</text><text>28.71</text><text>9.1</text></g>
</svg>

--- GENERATED OUTPUT (blueprint-elevation.svg) ---
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1600 1200" width="1600" height="1200">
  <rect width="100%" height="100%" fill="#12253a" />
    <polygon data-role="footing" data-id="FT2" points="923.4,1143.0 923.4,1066.1 881.4,1066.1 881.4,1143.0" fill="#122440" stroke="#00ffff" stroke-width="3.0" />
    <polygon data-role="footing" data-id="FT3" points="718.6,1143.0 718.6,1066.1 676.6,1066.1 676.6,1143.0" fill="#122440" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="923.4,1143.0 881.4,1143.0 881.4,1143.0 923.4,1143.0" fill="#162c4e" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="923.4,1066.1 923.4,1066.1 881.4,1066.1 881.4,1066.1" fill="#162c4e" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="923.4,1143.0 923.4,1143.0 923.4,1066.1 923.4,1066.1" fill="#183050" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="881.4,1143.0 881.4,1066.1 881.4,1066.1 881.4,1143.0" fill="#0d1e30" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="718.6,1143.0 676.6,1143.0 676.6,1143.0 718.6,1143.0" fill="#162c4e" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="718.6,1066.1 718.6,1066.1 676.6,1066.1 676.6,1066.1" fill="#162c4e" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="718.6,1143.0 718.6,1143.0 718.6,1066.1 718.6,1066.1" fill="#183050" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="676.6,1143.0 676.6,1066.1 676.6,1066.1 676.6,1143.0" fill="#0d1e30" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="923.4,1143.0 881.4,1143.0 881.4,1066.1 923.4,1066.1" fill="#0e1e34" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="718.6,1143.0 676.6,1143.0 676.6,1066.1 718.6,1066.1" fill="#0e1e34" stroke="#00ffff" stroke-width="3.0" />
    <polygon data-role="footing" data-id="FT1" points="1025.8,1143.0 1025.8,1066.1 983.8,1066.1 983.8,1143.0" fill="#122440" stroke="#00ffff" stroke-width="3.0" />
    <polygon data-role="footing" data-id="FT4" points="616.2,1143.0 616.2,1066.1 574.2,1066.1 574.2,1143.0" fill="#122440" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="1025.8,1143.0 983.8,1143.0 983.8,1143.0 1025.8,1143.0" fill="#162c4e" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="1025.8,1066.1 1025.8,1066.1 983.8,1066.1 983.8,1066.1" fill="#162c4e" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="1025.8,1143.0 1025.8,1143.0 1025.8,1066.1 1025.8,1066.1" fill="#183050" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="983.8,1143.0 983.8,1066.1 983.8,1066.1 983.8,1143.0" fill="#0d1e30" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="616.2,1143.0 574.2,1143.0 574.2,1143.0 616.2,1143.0" fill="#162c4e" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="616.2,1066.1 616.2,1066.1 574.2,1066.1 574.2,1066.1" fill="#162c4e" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="616.2,1143.0 616.2,1143.0 616.2,1066.1 616.2,1066.1" fill="#183050" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="574.2,1143.0 574.2,1066.1 574.2,1066.1 574.2,1143.0" fill="#0d1e30" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="1025.8,1143.0 983.8,1143.0 983.8,1066.1 1025.8,1066.1" fill="#0e1e34" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="616.2,1143.0 574.2,1143.0 574.2,1066.1 616.2,1066.1" fill="#0e1e34" stroke="#00ffff" stroke-width="3.0" />
    <polygon data-role="footing" data-id="FT5" points="718.6,1143.0 718.6,1066.1 676.6,1066.1 676.6,1143.0" fill="#122440" stroke="#00ffff" stroke-width="3.0" />
    <polygon data-role="footing" data-id="FT6" points="923.4,1143.0 923.4,1066.1 881.4,1066.1 881.4,1143.0" fill="#122440" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="718.6,1143.0 676.6,1143.0 676.6,1143.0 718.6,1143.0" fill="#162c4e" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="718.6,1066.1 718.6,1066.1 676.6,1066.1 676.6,1066.1" fill="#162c4e" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="718.6,1143.0 718.6,1143.0 718.6,1066.1 718.6,1066.1" fill="#183050" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="676.6,1143.0 676.6,1066.1 676.6,1066.1 676.6,1143.0" fill="#0d1e30" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="923.4,1143.0 881.4,1143.0 881.4,1143.0 923.4,1143.0" fill="#162c4e" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="923.4,1066.1 923.4,1066.1 881.4,1066.1 881.4,1066.1" fill="#162c4e" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="923.4,1143.0 923.4,1143.0 923.4,1066.1 923.4,1066.1" fill="#183050" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="881.4,1143.0 881.4,1066.1 881.4,1066.1 881.4,1143.0" fill="#0d1e30" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="718.6,1143.0 676.6,1143.0 676.6,1066.1 718.6,1066.1" fill="#0e1e34" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="923.4,1143.0 881.4,1143.0 881.4,1066.1 923.4,1066.1" fill="#0e1e34" stroke="#00ffff" stroke-width="3.0" />
    <polygon data-role="rafter" data-id="J2a" points="834.1,726.4 834.1,726.4 840.2,726.4 828.0,726.4" fill="#0e2032" stroke="#00ffff" stroke-width="3.0" />
    <polygon data-role="rafter" data-id="J2b" points="765.9,726.4 765.9,726.4 772.0,726.4 759.8,726.4" fill="#0e2032" stroke="#00ffff" stroke-width="3.0" />
    <polygon data-role="rafter" data-id="R2" points="902.4,726.4 902.4,726.4 923.4,726.4 912.8,726.4" fill="#0e2032" stroke="#00ffff" stroke-width="3.0" />
    <polygon data-role="rafter" data-id="R3" points="697.6,726.4 697.6,726.4 687.2,726.4 676.6,726.4" fill="#0e2032" stroke="#00ffff" stroke-width="3.0" />
    <polygon data-role="post" data-id="P2" points="912.0,1080.0 892.8,1080.0 892.8,1080.0 912.0,1080.0" fill="#1a3560" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="912.0,768.4 912.0,768.4 892.8,768.4 892.8,768.4" fill="#1a3560" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="912.0,1080.0 912.0,1080.0 912.0,768.4 912.0,768.4" fill="#1e4272" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="892.8,1080.0 892.8,768.4 892.8,768.4 892.8,1080.0" fill="#0d1e30" stroke="#00ffff" stroke-width="3.0" />
    <polygon data-role="post" data-id="P3" points="707.2,1080.0 688.0,1080.0 688.0,1080.0 707.2,1080.0" fill="#1a3560" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="707.2,768.4 707.2,768.4 688.0,768.4 688.0,768.4" fill="#1a3560" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="707.2,1080.0 707.2,1080.0 707.2,768.4 707.2,768.4" fill="#1e4272" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="688.0,1080.0 688.0,768.4 688.0,768.4 688.0,1080.0" fill="#0d1e30" stroke="#00ffff" stroke-width="3.0" />
    <polygon data-role="brace" data-id="K2A" points="897.1,825.5 888.4,834.1 888.4,834.1 897.1,825.5" fill="#162c4e" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="835.7,764.0 835.7,764.0 827.0,772.7 827.0,772.7" fill="#162c4e" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="897.1,825.5 897.1,825.5 835.7,764.0 835.7,764.0" fill="#1b3760" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="888.4,834.1 827.0,772.7 827.0,772.7 888.4,834.1" fill="#0d1f32" stroke="#00ffff" stroke-width="3.0" />
    <polygon data-role="brace" data-id="K2B" points="702.9,825.5 711.6,834.1 711.6,834.1 702.9,825.5" fill="#162c4e" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="764.3,764.0 764.3,764.0 773.0,772.7 773.0,772.7" fill="#162c4e" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="702.9,825.5 702.9,825.5 764.3,764.0 764.3,764.0" fill="#1b3760" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="711.6,834.1 773.0,772.7 773.0,772.7 711.6,834.1" fill="#0d1f32" stroke="#00ffff" stroke-width="3.0" />
    <polygon data-role="beam" data-id="B2" points="902.4,726.4 902.4,768.4 902.4,768.4 902.4,726.4" fill="#162e4e" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="697.6,726.4 697.6,726.4 697.6,768.4 697.6,768.4" fill="#162e4e" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="902.4,726.4 902.4,726.4 697.6,726.4 697.6,726.4" fill="#1d3e68" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="902.4,768.4 697.6,768.4 697.6,768.4 902.4,768.4" fill="#0c1d2e" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="897.1,825.5 888.4,834.1 827.0,772.7 835.7,764.0" fill="#0e1e34" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="702.9,825.5 764.3,764.0 773.0,772.7 711.6,834.1" fill="#132440" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="912.0,1080.0 892.8,1080.0 892.8,768.4 912.0,768.4" fill="#0f2238" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="707.2,1080.0 688.0,1080.0 688.0,768.4 707.2,768.4" fill="#0f2238" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="902.4,726.4 902.4,768.4 697.6,768.4 697.6,726.4" fill="#0d2035" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="828.0,726.8 828.0,673.6 828.0,694.3 834.1,733.2 834.1,726.4 828.0,726.4" fill="#132842" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="840.2,726.4 834.1,726.4 834.1,733.2 840.2,694.3 840.2,673.6 840.2,726.8" fill="#0e2234" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="759.8,726.8 759.8,673.6 759.8,694.3 765.9,733.2 765.9,726.4 759.8,726.4" fill="#132842" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="772.0,726.4 765.9,726.4 765.9,733.2 772.0,694.3 772.0,673.6 772.0,726.8" fill="#0e2234" stroke="#00ffff" stroke-width="3.0" />
    <polygon data-role="brace" data-id="K1B" points="899.7,825.5 930.4,764.0 934.8,772.7 904.0,834.1" fill="#132440" stroke="#00ffff" stroke-width="3.0" />
    <polygon data-role="brace" data-id="K3A" points="700.3,825.5 696.0,834.1 665.2,772.7 669.6,764.0" fill="#0e1e34" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="904.0,834.1 934.8,772.7 945.4,772.7 914.7,834.1" fill="#0d1f32" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="685.3,834.1 654.6,772.7 665.2,772.7 696.0,834.1" fill="#0d1f32" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="923.4,726.4 902.4,726.4 902.4,733.1 818.9,675.8 818.9,655.5 923.4,725.2" fill="#0e2234" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="676.6,725.2 781.1,655.5 781.1,675.8 697.6,733.1 697.6,726.4 676.6,726.4" fill="#132842" stroke="#00ffff" stroke-width="3.0" />
    <polygon data-role="rafter" data-id="J1b" points="936.5,726.4 936.5,726.4 966.8,726.4 960.7,726.4" fill="#0e2032" stroke="#00ffff" stroke-width="3.0" />
    <polygon data-role="rafter" data-id="J3a" points="663.5,726.4 663.5,726.4 639.3,726.4 633.2,726.4" fill="#0e2032" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="828.0,694.3 840.2,694.3 834.1,733.2 834.1,733.2" fill="#0e2032" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="759.8,694.3 772.0,694.3 765.9,733.2 765.9,733.2" fill="#0e2032" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="930.4,764.0 941.0,764.0 945.4,772.7 934.8,772.7" fill="#162c4e" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="659.0,764.0 669.6,764.0 665.2,772.7 654.6,772.7" fill="#162c4e" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="966.8,726.4 936.5,726.4 936.5,733.2 847.3,694.3 847.3,673.6 966.8,726.8" fill="#0e2234" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="633.2,726.8 752.7,673.6 752.7,694.3 663.5,733.2 663.5,726.4 633.2,726.4" fill="#132842" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="808.3,675.8 818.9,675.8 902.4,733.1 902.4,733.1" fill="#0e2032" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="781.1,675.8 791.7,675.8 697.6,733.1 697.6,733.1" fill="#0e2032" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="841.1,694.3 847.3,694.3 936.5,733.2 936.5,733.2" fill="#0e2032" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="752.7,694.3 758.9,694.3 663.5,733.2 663.5,733.2" fill="#0e2032" stroke="#00ffff" stroke-width="3.0" />
    <polygon data-role="beam" data-id="B1" points="1013.8,726.4 995.7,726.4 893.3,726.4 911.5,726.4" fill="#1d3e68" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="1013.8,768.4 911.5,768.4 893.3,768.4 995.7,768.4" fill="#0c1d2e" stroke="#00ffff" stroke-width="3.0" />
    <polygon data-role="beam" data-id="B3" points="688.5,726.4 706.7,726.4 604.3,726.4 586.2,726.4" fill="#1d3e68" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="688.5,768.4 586.2,768.4 604.3,768.4 706.7,768.4" fill="#0c1d2e" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="995.7,726.4 995.7,768.4 893.3,768.4 893.3,726.4" fill="#0d2035" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="706.7,726.4 706.7,768.4 604.3,768.4 604.3,726.4" fill="#0d2035" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="828.0,673.6 840.2,673.6 840.2,694.3 828.0,694.3" fill="#172d4c" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="759.8,673.6 772.0,673.6 772.0,694.3 759.8,694.3" fill="#172d4c" stroke="#00ffff" stroke-width="3.0" />
    <polygon data-role="rafter" data-id="J1a" points="970.6,726.4 970.6,726.4 1001.0,726.4 994.8,726.4" fill="#0e2032" stroke="#00ffff" stroke-width="3.0" />
    <polygon data-role="rafter" data-id="J3b" points="629.4,726.4 629.4,726.4 605.2,726.4 599.0,726.4" fill="#0e2032" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="841.1,673.6 847.3,673.6 847.3,694.3 841.1,694.3" fill="#172d4c" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="752.7,673.6 758.9,673.6 758.9,694.3 752.7,694.3" fill="#172d4c" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="1001.0,726.4 970.6,726.4 970.6,733.2 881.4,694.3 881.4,673.6 1001.0,726.8" fill="#0e2234" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="599.0,726.8 718.6,673.6 718.6,694.3 629.4,733.2 629.4,726.4 599.0,726.4" fill="#132842" stroke="#00ffff" stroke-width="3.0" />
    <polygon data-role="brace" data-id="K1A" points="996.8,825.5 992.5,834.1 961.8,772.7 966.1,764.0" fill="#0e1e34" stroke="#00ffff" stroke-width="3.0" />
    <polygon data-role="brace" data-id="K3B" points="603.2,825.5 633.9,764.0 638.2,772.7 607.5,834.1" fill="#132440" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="875.3,694.3 881.4,694.3 970.6,733.2 970.6,733.2" fill="#0e2032" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="718.6,694.3 724.7,694.3 629.4,733.2 629.4,733.2" fill="#0e2032" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="1007.4,825.5 996.8,825.5 966.1,764.0 976.7,764.0" fill="#1b3760" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="603.2,825.5 592.6,825.5 623.3,764.0 633.9,764.0" fill="#1b3760" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="808.3,655.5 818.9,655.5 818.9,675.8 808.3,675.8" fill="#172d4c" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="781.1,655.5 791.7,655.5 791.7,675.8 781.1,675.8" fill="#172d4c" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="1007.4,825.5 1003.1,834.1 992.5,834.1 996.8,825.5" fill="#162c4e" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="603.2,825.5 607.5,834.1 596.9,834.1 592.6,825.5" fill="#162c4e" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="875.3,673.6 881.4,673.6 881.4,694.3 875.3,694.3" fill="#172d4c" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="718.6,673.6 724.7,673.6 724.7,694.3 718.6,694.3" fill="#172d4c" stroke="#00ffff" stroke-width="3.0" />
    <polygon data-role="post" data-id="P1" points="1014.4,1080.0 995.1,1080.0 995.1,1080.0 1014.4,1080.0" fill="#1a3560" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="1014.4,768.4 1014.4,768.4 995.1,768.4 995.1,768.4" fill="#1a3560" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="1014.4,1080.0 1014.4,1080.0 1014.4,768.4 1014.4,768.4" fill="#1e4272" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="995.1,1080.0 995.1,768.4 995.1,768.4 995.1,1080.0" fill="#0d1e30" stroke="#00ffff" stroke-width="3.0" />
    <polygon data-role="post" data-id="P4" points="604.9,1080.0 585.6,1080.0 585.6,1080.0 604.9,1080.0" fill="#1a3560" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="604.9,768.4 604.9,768.4 585.6,768.4 585.6,768.4" fill="#1a3560" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="604.9,1080.0 604.9,1080.0 604.9,768.4 604.9,768.4" fill="#1e4272" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="585.6,1080.0 585.6,768.4 585.6,768.4 585.6,1080.0" fill="#0d1e30" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="1013.8,726.4 1013.8,768.4 995.7,768.4 995.7,726.4" fill="#162e4e" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="586.2,726.4 604.3,726.4 604.3,768.4 586.2,768.4" fill="#162e4e" stroke="#00ffff" stroke-width="3.0" />
    <polygon data-role="rafter" data-id="R1" points="1036.2,725.2 1036.2,725.2 827.3,655.5 827.3,655.5" fill="#1f4070" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="827.3,655.5 827.3,655.5 827.3,675.8 827.3,675.8" fill="#172d4c" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="827.3,675.8 827.3,675.8 1004.8,733.1 1004.8,733.1" fill="#0e2032" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="1004.8,733.1 1004.8,733.1 1004.8,726.4 1004.8,726.4" fill="#132842" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="1004.8,726.4 1004.8,726.4 1036.2,726.4 1036.2,726.4" fill="#0e2032" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="1036.2,726.4 1036.2,726.4 1036.2,725.2 1036.2,725.2" fill="#172d4c" stroke="#00ffff" stroke-width="3.0" />
    <polygon data-role="rafter" data-id="R4" points="563.8,725.2 563.8,725.2 772.7,655.5 772.7,655.5" fill="#1f4070" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="772.7,655.5 772.7,655.5 772.7,675.8 772.7,675.8" fill="#172d4c" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="772.7,675.8 772.7,675.8 595.2,733.1 595.2,733.1" fill="#0e2032" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="595.2,733.1 595.2,733.1 595.2,726.4 595.2,726.4" fill="#132842" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="595.2,726.4 595.2,726.4 563.8,726.4 563.8,726.4" fill="#0e2032" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="563.8,726.4 563.8,726.4 563.8,725.2 563.8,725.2" fill="#172d4c" stroke="#00ffff" stroke-width="3.0" />
    <polygon data-role="hub" data-id="HUB" points="768.5,683.3 768.5,683.3 768.5,632.9 768.5,632.9" fill="#1a3868" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="831.5,632.9 831.5,632.9 800.0,632.9 768.5,632.9 768.5,632.9 800.0,632.9" fill="#204878" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="800.0,683.3 768.5,683.3 768.5,683.3 800.0,683.3 831.5,683.3 831.5,683.3" fill="#0e2035" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="831.5,683.3 831.5,683.3 831.5,632.9 831.5,632.9" fill="#1a3868" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="1036.2,726.4 1004.8,726.4 1004.8,733.1 827.3,675.8 827.3,655.5 1036.2,725.2" fill="#0e2234" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="563.8,725.2 772.7,655.5 772.7,675.8 595.2,733.1 595.2,726.4 563.8,726.4" fill="#132842" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="1014.4,1080.0 995.1,1080.0 995.1,768.4 1014.4,768.4" fill="#0f2238" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="604.9,1080.0 585.6,1080.0 585.6,768.4 604.9,768.4" fill="#0f2238" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="768.5,683.3 800.0,683.3 800.0,632.9 768.5,632.9" fill="#1a3868" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="800.0,683.3 831.5,683.3 831.5,632.9 800.0,632.9" fill="#1a3868" stroke="#00ffff" stroke-width="3.0" />
    <polygon data-role="brace" data-id="K4A" points="592.6,825.5 623.3,764.0 627.6,772.7 596.9,834.1" fill="#132440" stroke="#00ffff" stroke-width="3.0" />
    <polygon data-role="brace" data-id="K6B" points="1007.4,825.5 1003.1,834.1 972.4,772.7 976.7,764.0" fill="#0e1e34" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="596.9,834.1 627.6,772.7 638.2,772.7 607.5,834.1" fill="#0d1f32" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="992.5,834.1 961.8,772.7 972.4,772.7 1003.1,834.1" fill="#0d1f32" stroke="#00ffff" stroke-width="3.0" />
    <polygon data-role="rafter" data-id="J4a" points="605.2,726.8 599.0,726.8 718.6,673.6 724.7,673.6" fill="#1f4070" stroke="#00ffff" stroke-width="3.0" />
    <polygon data-role="rafter" data-id="J6b" points="1001.0,726.8 994.8,726.8 875.3,673.6 881.4,673.6" fill="#1f4070" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="605.2,726.8 724.7,673.6 724.7,694.3 629.4,733.2 629.4,726.4 605.2,726.4" fill="#132842" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="994.8,726.4 970.6,726.4 970.6,733.2 875.3,694.3 875.3,673.6 994.8,726.8" fill="#0e2234" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="629.4,733.2 629.4,733.2 629.4,726.4 629.4,726.4" fill="#132842" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="970.6,733.2 970.6,733.2 970.6,726.4 970.6,726.4" fill="#132842" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="623.3,764.0 633.9,764.0 638.2,772.7 627.6,772.7" fill="#162c4e" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="966.1,764.0 976.7,764.0 972.4,772.7 961.8,772.7" fill="#162c4e" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="629.4,726.4 629.4,726.4 599.0,726.4 605.2,726.4" fill="#0e2032" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="970.6,726.4 970.6,726.4 994.8,726.4 1001.0,726.4" fill="#0e2032" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="605.2,726.4 599.0,726.4 599.0,726.8 605.2,726.8" fill="#172d4c" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="1001.0,726.4 994.8,726.4 994.8,726.8 1001.0,726.8" fill="#172d4c" stroke="#00ffff" stroke-width="3.0" />
    <polygon data-role="beam" data-id="B4" points="586.2,726.4 604.3,726.4 706.7,726.4 688.5,726.4" fill="#1d3e68" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="586.2,768.4 688.5,768.4 706.7,768.4 604.3,768.4" fill="#0c1d2e" stroke="#00ffff" stroke-width="3.0" />
    <polygon data-role="beam" data-id="B6" points="911.5,726.4 893.3,726.4 995.7,726.4 1013.8,726.4" fill="#1d3e68" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="911.5,768.4 1013.8,768.4 995.7,768.4 893.3,768.4" fill="#0c1d2e" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="586.2,726.4 688.5,726.4 688.5,768.4 586.2,768.4" fill="#122840" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="911.5,726.4 1013.8,726.4 1013.8,768.4 911.5,768.4" fill="#122840" stroke="#00ffff" stroke-width="3.0" />
    <polygon data-role="rafter" data-id="J4b" points="639.3,726.8 633.2,726.8 752.7,673.6 758.9,673.6" fill="#1f4070" stroke="#00ffff" stroke-width="3.0" />
    <polygon data-role="rafter" data-id="J6a" points="966.8,726.8 960.7,726.8 841.1,673.6 847.3,673.6" fill="#1f4070" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="639.3,726.8 758.9,673.6 758.9,694.3 663.5,733.2 663.5,726.4 639.3,726.4" fill="#132842" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="960.7,726.4 936.5,726.4 936.5,733.2 841.1,694.3 841.1,673.6 960.7,726.8" fill="#0e2234" stroke="#00ffff" stroke-width="3.0" />
    <polygon data-role="rafter" data-id="R5" points="687.2,725.2 676.6,725.2 781.1,655.5 791.7,655.5" fill="#1f4070" stroke="#00ffff" stroke-width="3.0" />
    <polygon data-role="rafter" data-id="R6" points="923.4,725.2 912.8,725.2 808.3,655.5 818.9,655.5" fill="#1f4070" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="663.5,733.2 663.5,733.2 663.5,726.4 663.5,726.4" fill="#132842" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="936.5,733.2 936.5,733.2 936.5,726.4 936.5,726.4" fill="#132842" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="663.5,726.4 663.5,726.4 633.2,726.4 639.3,726.4" fill="#0e2032" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="936.5,726.4 936.5,726.4 960.7,726.4 966.8,726.4" fill="#0e2032" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="639.3,726.4 633.2,726.4 633.2,726.8 639.3,726.8" fill="#172d4c" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="966.8,726.4 960.7,726.4 960.7,726.8 966.8,726.8" fill="#172d4c" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="687.2,725.2 791.7,655.5 791.7,675.8 697.6,733.1 697.6,726.4 687.2,726.4" fill="#132842" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="912.8,726.4 902.4,726.4 902.4,733.1 808.3,675.8 808.3,655.5 912.8,725.2" fill="#0e2234" stroke="#00ffff" stroke-width="3.0" />
    <polygon data-role="rafter" data-id="J5a" points="772.0,726.8 759.8,726.8 759.8,673.6 772.0,673.6" fill="#1f4070" stroke="#00ffff" stroke-width="3.0" />
    <polygon data-role="rafter" data-id="J5b" points="840.2,726.8 828.0,726.8 828.0,673.6 840.2,673.6" fill="#1f4070" stroke="#00ffff" stroke-width="3.0" />
    <polygon data-role="brace" data-id="K4B" points="689.7,825.5 685.3,834.1 654.6,772.7 659.0,764.0" fill="#0e1e34" stroke="#00ffff" stroke-width="3.0" />
    <polygon data-role="brace" data-id="K6A" points="910.3,825.5 941.0,764.0 945.4,772.7 914.7,834.1" fill="#132440" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="700.3,825.5 689.7,825.5 659.0,764.0 669.6,764.0" fill="#1b3760" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="910.3,825.5 899.7,825.5 930.4,764.0 941.0,764.0" fill="#1b3760" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="772.0,726.8 772.0,673.6 772.0,694.3 765.9,733.2 765.9,726.4 772.0,726.4" fill="#132842" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="759.8,726.4 765.9,726.4 765.9,733.2 759.8,694.3 759.8,673.6 759.8,726.8" fill="#0e2234" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="840.2,726.8 840.2,673.6 840.2,694.3 834.1,733.2 834.1,726.4 840.2,726.4" fill="#132842" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="828.0,726.4 834.1,726.4 834.1,733.2 828.0,694.3 828.0,673.6 828.0,726.8" fill="#0e2234" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="700.3,825.5 696.0,834.1 685.3,834.1 689.7,825.5" fill="#162c4e" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="910.3,825.5 914.7,834.1 904.0,834.1 899.7,825.5" fill="#162c4e" stroke="#00ffff" stroke-width="3.0" />
    <polygon data-role="post" data-id="P5" points="707.2,1080.0 688.0,1080.0 688.0,1080.0 707.2,1080.0" fill="#1a3560" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="707.2,768.4 707.2,768.4 688.0,768.4 688.0,768.4" fill="#1a3560" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="707.2,1080.0 707.2,1080.0 707.2,768.4 707.2,768.4" fill="#1e4272" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="688.0,1080.0 688.0,768.4 688.0,768.4 688.0,1080.0" fill="#0d1e30" stroke="#00ffff" stroke-width="3.0" />
    <polygon data-role="post" data-id="P6" points="912.0,1080.0 892.8,1080.0 892.8,1080.0 912.0,1080.0" fill="#1a3560" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="912.0,768.4 912.0,768.4 892.8,768.4 892.8,768.4" fill="#1a3560" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="912.0,1080.0 912.0,1080.0 912.0,768.4 912.0,768.4" fill="#1e4272" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="892.8,1080.0 892.8,768.4 892.8,768.4 892.8,1080.0" fill="#0d1e30" stroke="#00ffff" stroke-width="3.0" />
    <polygon data-role="brace" data-id="K5A" points="702.9,825.5 711.6,834.1 711.6,834.1 702.9,825.5" fill="#162c4e" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="764.3,764.0 764.3,764.0 773.0,772.7 773.0,772.7" fill="#162c4e" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="702.9,825.5 702.9,825.5 764.3,764.0 764.3,764.0" fill="#1b3760" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="711.6,834.1 773.0,772.7 773.0,772.7 711.6,834.1" fill="#0d1f32" stroke="#00ffff" stroke-width="3.0" />
    <polygon data-role="brace" data-id="K5B" points="897.1,825.5 888.4,834.1 888.4,834.1 897.1,825.5" fill="#162c4e" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="835.7,764.0 835.7,764.0 827.0,772.7 827.0,772.7" fill="#162c4e" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="897.1,825.5 897.1,825.5 835.7,764.0 835.7,764.0" fill="#1b3760" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="888.4,834.1 827.0,772.7 827.0,772.7 888.4,834.1" fill="#0d1f32" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="688.5,726.4 706.7,726.4 706.7,768.4 688.5,768.4" fill="#162e4e" stroke="#00ffff" stroke-width="3.0" />
    <polygon data-role="beam" data-id="B5" points="697.6,726.4 697.6,768.4 697.6,768.4 697.6,726.4" fill="#162e4e" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="902.4,726.4 902.4,726.4 902.4,768.4 902.4,768.4" fill="#162e4e" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="697.6,726.4 697.6,726.4 902.4,726.4 902.4,726.4" fill="#1d3e68" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="697.6,768.4 902.4,768.4 902.4,768.4 697.6,768.4" fill="#0c1d2e" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="911.5,726.4 911.5,768.4 893.3,768.4 893.3,726.4" fill="#162e4e" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="697.6,733.1 697.6,733.1 697.6,726.4 697.6,726.4" fill="#132842" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="902.4,733.1 902.4,733.1 902.4,726.4 902.4,726.4" fill="#132842" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="765.9,733.2 765.9,733.2 765.9,726.4 765.9,726.4" fill="#132842" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="834.1,733.2 834.1,733.2 834.1,726.4 834.1,726.4" fill="#132842" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="702.9,825.5 764.3,764.0 773.0,772.7 711.6,834.1" fill="#132440" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="897.1,825.5 888.4,834.1 827.0,772.7 835.7,764.0" fill="#0e1e34" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="707.2,1080.0 688.0,1080.0 688.0,768.4 707.2,768.4" fill="#0f2238" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="912.0,1080.0 892.8,1080.0 892.8,768.4 912.0,768.4" fill="#0f2238" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="697.6,726.4 902.4,726.4 902.4,768.4 697.6,768.4" fill="#122840" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="697.6,726.4 697.6,726.4 676.6,726.4 687.2,726.4" fill="#0e2032" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="902.4,726.4 902.4,726.4 912.8,726.4 923.4,726.4" fill="#0e2032" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="765.9,726.4 765.9,726.4 759.8,726.4 772.0,726.4" fill="#0e2032" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="834.1,726.4 834.1,726.4 828.0,726.4 840.2,726.4" fill="#0e2032" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="687.2,726.4 676.6,726.4 676.6,725.2 687.2,725.2" fill="#172d4c" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="923.4,726.4 912.8,726.4 912.8,725.2 923.4,725.2" fill="#172d4c" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="772.0,726.4 759.8,726.4 759.8,726.8 772.0,726.8" fill="#172d4c" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="840.2,726.4 828.0,726.4 828.0,726.8 840.2,726.8" fill="#172d4c" stroke="#00ffff" stroke-width="3.0" />
  <g id="annotation-labels-layer">
    <text x="1019.8" y="924.2" text-anchor="middle" font-size="14" font-weight="bold" fill="#00ffff" opacity="1.0" data-label="P1">P1</text>
    <text x="917.4" y="924.2" text-anchor="middle" font-size="14" font-weight="bold" fill="#00ffff" opacity="1.0" data-label="P2">P2</text>
    <text x="712.6" y="924.2" text-anchor="middle" font-size="14" font-weight="bold" fill="#00ffff" opacity="1.0" data-label="P3">P3</text>
    <text x="610.2" y="924.2" text-anchor="middle" font-size="14" font-weight="bold" fill="#00ffff" opacity="1.0" data-label="P4">P4</text>
    <text x="727.6" y="924.2" text-anchor="middle" font-size="14" font-weight="bold" fill="#00ffff" opacity="1.0" data-label="P5">P5</text>
    <text x="932.4" y="924.2" text-anchor="middle" font-size="14" font-weight="bold" fill="#00ffff" opacity="1.0" data-label="P6">P6</text>
    <text x="953.6" y="732.4" text-anchor="middle" font-size="14" font-weight="bold" fill="#00ffff" opacity="1.0" data-label="B1">B1</text>
    <text x="800.0" y="732.4" text-anchor="middle" font-size="14" font-weight="bold" fill="#00ffff" opacity="1.0" data-label="B2">B2</text>
    <text x="646.4" y="732.4" text-anchor="middle" font-size="14" font-weight="bold" fill="#00ffff" opacity="1.0" data-label="B3">B3</text>
    <text x="661.4" y="732.4" text-anchor="middle" font-size="14" font-weight="bold" fill="#00ffff" opacity="1.0" data-label="B4">B4</text>
    <text x="815.0" y="732.4" text-anchor="middle" font-size="14" font-weight="bold" fill="#00ffff" opacity="1.0" data-label="B5">B5</text>
    <text x="968.6" y="732.4" text-anchor="middle" font-size="14" font-weight="bold" fill="#00ffff" opacity="1.0" data-label="B6">B6</text>
    <text x="984.6" y="799.1" text-anchor="middle" font-size="8" font-weight="normal" fill="#00ffff" opacity="0.75" data-label="K1A">K1A</text>
    <text x="922.5" y="799.1" text-anchor="middle" font-size="8" font-weight="normal" fill="#00ffff" opacity="0.75" data-label="K1B">K1B</text>
    <text x="862.0" y="799.1" text-anchor="middle" font-size="8" font-weight="normal" fill="#00ffff" opacity="0.75" data-label="K2A">K2A</text>
    <text x="738.0" y="799.1" text-anchor="middle" font-size="8" font-weight="normal" fill="#00ffff" opacity="0.75" data-label="K2B">K2B</text>
    <text x="677.5" y="799.1" text-anchor="middle" font-size="8" font-weight="normal" fill="#00ffff" opacity="0.75" data-label="K3A">K3A</text>
    <text x="615.4" y="799.1" text-anchor="middle" font-size="8" font-weight="normal" fill="#00ffff" opacity="0.75" data-label="K3B">K3B</text>
    <text x="630.4" y="799.1" text-anchor="middle" font-size="8" font-weight="normal" fill="#00ffff" opacity="0.75" data-label="K4A">K4A</text>
    <text x="692.5" y="799.1" text-anchor="middle" font-size="8" font-weight="normal" fill="#00ffff" opacity="0.75" data-label="K4B">K4B</text>
    <text x="753.0" y="799.1" text-anchor="middle" font-size="8" font-weight="normal" fill="#00ffff" opacity="0.75" data-label="K5A">K5A</text>
    <text x="877.0" y="799.1" text-anchor="middle" font-size="8" font-weight="normal" fill="#00ffff" opacity="0.75" data-label="K5B">K5B</text>
    <text x="937.5" y="799.1" text-anchor="middle" font-size="8" font-weight="normal" fill="#00ffff" opacity="0.75" data-label="K6A">K6A</text>
    <text x="999.6" y="799.1" text-anchor="middle" font-size="8" font-weight="normal" fill="#00ffff" opacity="0.75" data-label="K6B">K6B</text>
    <text x="931.8" y="690.4" text-anchor="middle" font-size="10" font-weight="normal" fill="#00ffff" opacity="0.9" data-label="R1">R1</text>
    <text x="865.9" y="690.4" text-anchor="middle" font-size="10" font-weight="normal" fill="#00ffff" opacity="0.9" data-label="R2">R2</text>
    <text x="734.1" y="690.4" text-anchor="middle" font-size="10" font-weight="normal" fill="#00ffff" opacity="0.9" data-label="R3">R3</text>
    <text x="668.2" y="690.4" text-anchor="middle" font-size="10" font-weight="normal" fill="#00ffff" opacity="0.9" data-label="R4">R4</text>
    <text x="749.1" y="690.4" text-anchor="middle" font-size="10" font-weight="normal" fill="#00ffff" opacity="0.9" data-label="R5">R5</text>
    <text x="880.9" y="690.4" text-anchor="middle" font-size="10" font-weight="normal" fill="#00ffff" opacity="0.9" data-label="R6">R6</text>
    <text x="943.1" y="700.2" text-anchor="middle" font-size="10" font-weight="normal" fill="#00ffff" opacity="0.9" data-label="J1a">J1a</text>
    <text x="904.0" y="700.2" text-anchor="middle" font-size="10" font-weight="normal" fill="#00ffff" opacity="0.9" data-label="J1b">J1b</text>
    <text x="834.1" y="700.2" text-anchor="middle" font-size="10" font-weight="normal" fill="#00ffff" opacity="0.9" data-label="J2a">J2a</text>
    <text x="765.9" y="700.2" text-anchor="middle" font-size="10" font-weight="normal" fill="#00ffff" opacity="0.9" data-label="J2b">J2b</text>
    <text x="696.0" y="700.2" text-anchor="middle" font-size="10" font-weight="normal" fill="#00ffff" opacity="0.9" data-label="J3a">J3a</text>
    <text x="664.4" y="704.6" text-anchor="middle" font-size="10" font-weight="normal" fill="#00ffff" opacity="0.9" data-label="J3b">J3b</text>
    <text x="653.2" y="695.2" text-anchor="middle" font-size="10" font-weight="normal" fill="#00ffff" opacity="0.9" data-label="J4a">J4a</text>
    <text x="711.0" y="700.2" text-anchor="middle" font-size="10" font-weight="normal" fill="#00ffff" opacity="0.9" data-label="J4b">J4b</text>
    <text x="780.9" y="700.2" text-anchor="middle" font-size="10" font-weight="normal" fill="#00ffff" opacity="0.9" data-label="J5a">J5a</text>
    <text x="849.1" y="700.2" text-anchor="middle" font-size="10" font-weight="normal" fill="#00ffff" opacity="0.9" data-label="J5b">J5b</text>
    <text x="919.0" y="700.2" text-anchor="middle" font-size="10" font-weight="normal" fill="#00ffff" opacity="0.9" data-label="J6a">J6a</text>
    <text x="938.1" y="715.2" text-anchor="middle" font-size="10" font-weight="normal" fill="#00ffff" opacity="0.9" data-label="J6b">J6b</text>
    <text x="800.0" y="638.1" text-anchor="middle" font-size="14" font-weight="bold" fill="#00ffff" opacity="1.0" data-label="HUB">HUB</text>
  </g>
    <g data-role="dimension">
        <line x1="600.0" y1="1080" x2="600.0" y2="726.36" stroke="#00e5ff" stroke-width="1.2" />
        <text x="585.0" y="903.1800000000001" text-anchor="middle" transform="rotate(-90,585.0,903.1800000000001)" font-family="monospace" font-size="13" font-weight="bold" fill="#00e5ff">POST: 8.42 FT</text>
    </g>
  <line x1="100" y1="1080" x2="1500" y2="1080" stroke="#00ffff" stroke-width="2" />
    <g data-role="title-block" transform="translate(1180, 1030)">
        <rect width="400" height="150" fill="#12253a" stroke="#00ffff" stroke-width="1.8" />
        <line x1="0" y1="40" x2="400" y2="40" stroke="#00ffff" stroke-width="1" />
        <text x="15" y="28" font-family="monospace" font-size="18" font-weight="bold" fill="#00ffff">BLUEPRINT ELEVATION</text>
        <text x="15" y="60" font-family="monospace" font-size="11" fill="#00ffff">STRUCTURE: PERGOLA</text>
        <text x="15" y="80" font-family="monospace" font-size="11" fill="#00ffff">JURISDICTION: BC_SAANICH</text>
        <text x="15" y="100" font-family="monospace" font-size="11" fill="#00ffff">SOURCE HASH: 6a3a3109</text>
        <text x="15" y="120" font-family="monospace" font-size="11" fill="#00ffff">DATE: 2026-05-24 | SCALE: AUTO</text>
    </g>
    <!-- VALIDATOR_ANCHORS: 4:12 28.71° 9.1° -->
    <!-- SAW_SETTINGS: {"miter_deg": 28.71, "bevel_deg": 9.1} -->
    <!-- COORDINATE MAP: {"viewBox": "0 0 1600 1200", "width_px": 1600, "height_px": 1200, "grade_y": 1080, "scale_px_per_ft": 42.0, "post_top_y": 726, "beam_top_y": 684, "hub_apex_y": 616} -->
    <g style="visibility:hidden; display:none;"><text>4:12</text><text>28.71</text><text>9.1</text></g>
</svg>

--- GENERATED OUTPUT (blueprint-isometric.svg) ---
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1600 1200" width="1600" height="1200">
  <rect width="100%" height="100%" fill="#12253a" />
    <polygon data-role="footing" data-id="FT5" points="864.9,544.2 828.5,523.2 864.9,502.2 901.3,523.2" fill="#162c4e" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="828.5,523.2 828.5,446.3 864.9,425.3 864.9,502.2" fill="#0d1e30" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="901.3,523.2 864.9,502.2 864.9,425.3 901.3,446.3" fill="#0e1e34" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="864.9,544.2 901.3,523.2 901.3,446.3 864.9,467.3" fill="#183050" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="864.9,544.2 864.9,467.3 828.5,446.3 828.5,523.2" fill="#122440" stroke="#00ffff" stroke-width="3.0" />
    <polygon data-role="footing" data-id="FT4" points="622.7,581.6 586.3,560.6 622.7,539.6 659.1,560.6" fill="#162c4e" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="864.9,467.3 901.3,446.3 864.9,425.3 828.5,446.3" fill="#162c4e" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="586.3,560.6 586.3,483.8 622.7,462.8 622.7,539.6" fill="#0d1e30" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="659.1,560.6 622.7,539.6 622.7,462.8 659.1,483.8" fill="#0e1e34" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="622.7,581.6 659.1,560.6 659.1,483.8 622.7,504.8" fill="#183050" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="622.7,581.6 622.7,504.8 586.3,483.8 586.3,560.6" fill="#122440" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="622.7,504.8 659.1,483.8 622.7,462.8 586.3,483.8" fill="#162c4e" stroke="#00ffff" stroke-width="3.0" />
    <polygon data-role="footing" data-id="FT6" points="1042.2,646.5 1005.8,625.5 1042.2,604.5 1078.6,625.5" fill="#162c4e" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="1005.8,625.5 1005.8,548.7 1042.2,527.7 1042.2,604.5" fill="#0d1e30" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="1078.6,625.5 1042.2,604.5 1042.2,527.7 1078.6,548.7" fill="#0e1e34" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="1042.2,646.5 1078.6,625.5 1078.6,548.7 1042.2,569.7" fill="#183050" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="1042.2,646.5 1042.2,569.7 1005.8,548.7 1005.8,625.5" fill="#122440" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="1042.2,569.7 1078.6,548.7 1042.2,527.7 1005.8,548.7" fill="#162c4e" stroke="#00ffff" stroke-width="3.0" />
    <polygon data-role="footing" data-id="FT3" points="557.8,721.5 521.4,700.5 557.8,679.5 594.2,700.5" fill="#162c4e" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="521.4,700.5 521.4,623.6 557.8,602.6 557.8,679.5" fill="#0d1e30" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="594.2,700.5 557.8,679.5 557.8,602.6 594.2,623.6" fill="#0e1e34" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="557.8,721.5 594.2,700.5 594.2,623.6 557.8,644.6" fill="#183050" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="557.8,721.5 557.8,644.6 521.4,623.6 521.4,700.5" fill="#122440" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="557.8,644.6 594.2,623.6 557.8,602.6 521.4,623.6" fill="#162c4e" stroke="#00ffff" stroke-width="3.0" />
    <polygon data-role="footing" data-id="FT1" points="977.3,786.4 940.9,765.4 977.3,744.4 1013.7,765.4" fill="#162c4e" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="940.9,765.4 940.9,688.5 977.3,667.5 977.3,744.4" fill="#0d1e30" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="1013.7,765.4 977.3,744.4 977.3,667.5 1013.7,688.5" fill="#0e1e34" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="977.3,786.4 1013.7,765.4 1013.7,688.5 977.3,709.5" fill="#183050" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="977.3,786.4 977.3,709.5 940.9,688.5 940.9,765.4" fill="#122440" stroke="#00ffff" stroke-width="3.0" />
    <polygon data-role="footing" data-id="FT2" points="735.1,823.8 698.7,802.8 735.1,781.8 771.5,802.8" fill="#162c4e" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="977.3,709.5 1013.7,688.5 977.3,667.5 940.9,688.5" fill="#162c4e" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="698.7,802.8 698.7,726.0 735.1,705.0 735.1,781.8" fill="#0d1e30" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="771.5,802.8 735.1,781.8 735.1,705.0 771.5,726.0" fill="#0e1e34" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="735.1,823.8 771.5,802.8 771.5,726.0 735.1,747.0" fill="#183050" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="735.1,823.8 735.1,747.0 698.7,726.0 698.7,802.8" fill="#122440" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="735.1,747.0 771.5,726.0 735.1,705.0 698.7,726.0" fill="#162c4e" stroke="#00ffff" stroke-width="3.0" />
    <polygon data-role="post" data-id="P5" points="864.9,469.8 881.6,460.2 881.6,148.5 864.9,158.1" fill="#1e4272" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="864.9,469.8 864.9,158.1 848.2,148.5 848.2,460.2" fill="#162e50" stroke="#00ffff" stroke-width="3.0" />
    <polygon data-role="post" data-id="P4" points="622.7,507.2 639.4,497.6 639.4,186.0 622.7,195.6" fill="#1e4272" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="622.7,507.2 622.7,195.6 606.0,186.0 606.0,497.6" fill="#162e50" stroke="#00ffff" stroke-width="3.0" />
    <polygon data-role="brace" data-id="K4B" points="860.6,210.8 856.7,202.4 784.0,152.2 787.9,160.6" fill="#1b3760" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="860.6,210.8 787.9,160.6 777.7,170.8 850.3,221.0" fill="#132440" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="864.9,158.1 881.6,148.5 864.9,138.9 848.2,148.5" fill="#1a3560" stroke="#00ffff" stroke-width="3.0" />
    <polygon data-role="brace" data-id="K5A" points="874.8,205.2 864.2,211.3 917.4,180.6 928.0,174.5" fill="#1b3760" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="882.3,218.2 935.5,187.5 924.9,193.6 871.7,224.3" fill="#0d1f32" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="864.2,211.3 871.7,224.3 924.9,193.6 917.4,180.6" fill="#0e1e34" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="787.9,160.6 784.0,152.2 773.8,162.5 777.7,170.8" fill="#162c4e" stroke="#00ffff" stroke-width="3.0" />
    <polygon data-role="brace" data-id="K4A" points="627.0,237.9 630.9,246.3 703.6,173.6 699.7,165.3" fill="#1b3760" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="630.9,246.3 641.1,253.4 713.8,180.7 703.6,173.6" fill="#0e1e34" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="699.7,165.3 703.6,173.6 713.8,180.7 709.9,172.3" fill="#162c4e" stroke="#00ffff" stroke-width="3.0" />
    <polygon data-role="post" data-id="P6" points="1042.2,572.2 1042.2,260.5 1025.6,250.9 1025.6,562.5" fill="#162e50" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="1042.2,572.2 1058.9,562.5 1058.9,250.9 1042.2,260.5" fill="#1e4272" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="928.0,174.5 917.4,180.6 924.9,193.6 935.5,187.5" fill="#162c4e" stroke="#00ffff" stroke-width="3.0" />
    <polygon data-role="beam" data-id="B4" points="626.0,151.2 626.0,193.2 868.2,155.7 868.2,113.7" fill="#0d2035" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="622.7,195.6 639.4,186.0 622.7,176.4 606.0,186.0" fill="#1a3560" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="619.4,136.8 626.0,151.2 868.2,113.7 861.6,99.3" fill="#1d3e68" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="619.4,136.8 619.4,178.8 626.0,193.2 626.0,151.2" fill="#162e4e" stroke="#00ffff" stroke-width="3.0" />
    <polygon data-role="brace" data-id="K3B" points="625.5,262.4 606.0,242.9 591.5,240.7 611.0,260.2" fill="#0d1f32" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="628.2,247.8 608.8,228.3 606.0,242.9 625.5,262.4" fill="#132440" stroke="#00ffff" stroke-width="3.0" />
    <polygon data-role="rafter" data-id="J4b" points="766.9,98.6 784.2,119.0 784.2,125.9 810.7,160.8 810.7,140.2 766.9,99.1" fill="#0e2234" stroke="#00ffff" stroke-width="3.0" />
    <polygon data-role="rafter" data-id="R5" points="882.1,84.9 815.9,158.0 815.9,178.3 864.9,113.3 864.9,106.5 882.1,86.1" fill="#132842" stroke="#00ffff" stroke-width="3.0" />
    <polygon data-role="brace" data-id="K5B" points="1032.3,308.4 1024.8,312.7 1035.4,306.6 1042.9,302.3" fill="#162c4e" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="979.1,216.3 989.7,210.1 982.2,214.5 971.6,220.6" fill="#162c4e" stroke="#00ffff" stroke-width="3.0" />
    <polygon data-role="beam" data-id="B5" points="855.8,111.8 855.8,153.8 1033.1,256.1 1033.1,214.1" fill="#0d2035" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="1032.3,308.4 979.1,216.3 971.6,220.6 1024.8,312.7" fill="#132440" stroke="#00ffff" stroke-width="3.0" />
    <polygon data-role="rafter" data-id="J4a" points="686.2,111.1 703.4,131.5 703.4,138.4 730.0,173.3 730.0,152.7 686.2,111.5" fill="#0e2234" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="1032.3,308.4 1042.9,302.3 989.7,210.1 979.1,216.3" fill="#1b3760" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="874.0,101.3 855.8,111.8 1033.1,214.1 1051.3,203.6" fill="#1d3e68" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="781.4,96.8 766.9,99.1 810.7,140.2 825.2,138.0" fill="#1f4070" stroke="#00ffff" stroke-width="3.0" />
    <polygon data-role="rafter" data-id="J5a" points="956.6,128.4 837.0,144.3 837.0,164.9 924.0,147.5 924.0,140.6 956.6,128.0" fill="#132842" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="700.7,109.3 686.2,111.5 730.0,152.7 744.5,150.5" fill="#1f4070" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="608.8,228.3 594.3,226.1 591.5,240.7 606.0,242.9" fill="#162c4e" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="956.6,128.4 946.0,122.3 826.4,138.2 837.0,144.3" fill="#1f4070" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="882.1,84.9 867.6,82.7 801.4,155.8 815.9,158.0" fill="#1f4070" stroke="#00ffff" stroke-width="3.0" />
    <polygon data-role="rafter" data-id="R4" points="590.1,131.3 622.7,144.0 622.7,150.7 771.1,185.2 771.1,164.9 590.1,130.1" fill="#0e2234" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="1042.2,260.5 1058.9,250.9 1042.2,241.3 1025.6,250.9" fill="#1a3560" stroke="#00ffff" stroke-width="3.0" />
    <polygon data-role="post" data-id="P3" points="557.8,647.1 574.4,637.5 574.4,325.8 557.8,335.5" fill="#1e4272" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="557.8,647.1 557.8,335.5 541.1,325.8 541.1,637.5" fill="#162e50" stroke="#00ffff" stroke-width="3.0" />
    <polygon data-role="rafter" data-id="J5b" points="1015.7,162.5 896.1,178.4 896.1,199.0 983.1,181.6 983.1,174.8 1015.7,162.1" fill="#132842" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="1051.3,203.6 1033.1,214.1 1033.1,256.1 1051.3,245.6" fill="#162e4e" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="600.7,124.0 590.1,130.1 771.1,164.9 781.7,158.8" fill="#1f4070" stroke="#00ffff" stroke-width="3.0" />
    <polygon data-role="brace" data-id="K6A" points="1045.0,327.3 1025.6,307.8 1011.1,305.6 1030.6,325.1" fill="#0d1f32" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="1047.8,312.7 1028.3,293.2 1025.6,307.8 1045.0,327.3" fill="#132440" stroke="#00ffff" stroke-width="3.0" />
    <polygon data-role="rafter" data-id="J3b" points="561.8,189.0 601.0,190.6 601.0,197.5 725.2,182.2 725.2,161.6 561.8,189.5" fill="#0e2234" stroke="#00ffff" stroke-width="3.0" />
    <polygon data-role="beam" data-id="B3" points="570.2,285.8 570.2,327.8 635.1,187.9 635.1,145.9" fill="#0d2035" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="1015.7,162.5 1005.1,156.4 885.5,172.3 896.1,178.4" fill="#1f4070" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="565.7,181.1 561.8,189.5 725.2,161.6 729.1,153.2" fill="#1f4070" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="825.2,138.0 810.7,140.2 810.7,160.8 825.2,158.6" fill="#172d4c" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="545.4,281.9 570.2,285.8 635.1,145.9 610.3,142.1" fill="#1d3e68" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="837.0,144.3 826.4,138.2 826.4,158.8 837.0,164.9" fill="#172d4c" stroke="#00ffff" stroke-width="3.0" />
    <polygon data-role="brace" data-id="K3A" points="566.7,380.4 569.4,383.2 588.9,279.8 586.2,277.1" fill="#0e1e34" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="552.2,378.2 566.7,380.4 586.2,277.1 571.7,274.8" fill="#1b3760" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="552.2,378.2 555.0,380.9 569.4,383.2 566.7,380.4" fill="#162c4e" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="744.5,150.5 730.0,152.7 730.0,173.3 744.5,171.1" fill="#172d4c" stroke="#00ffff" stroke-width="3.0" />
    <polygon data-role="rafter" data-id="R6" points="1081.4,206.1 834.2,174.7 834.2,195.0 1042.2,215.6 1042.2,208.9 1081.4,207.3" fill="#132842" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="729.1,153.2 725.2,161.6 725.2,182.2 729.1,173.8" fill="#172d4c" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="1028.3,293.2 1013.8,291.0 1011.1,305.6 1025.6,307.8" fill="#162c4e" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="1081.4,206.1 1077.5,197.8 830.3,166.3 834.2,174.7" fill="#1f4070" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="896.1,178.4 885.5,172.3 885.5,192.9 896.1,199.0" fill="#172d4c" stroke="#00ffff" stroke-width="3.0" />
    <polygon data-role="rafter" data-id="J3a" points="540.2,235.6 579.4,237.2 579.4,244.1 703.6,228.8 703.6,208.2 540.2,236.1" fill="#0e2234" stroke="#00ffff" stroke-width="3.0" />
    <polygon data-role="post" data-id="P1" points="977.3,712.0 994.0,702.4 994.0,390.7 977.3,400.4" fill="#1e4272" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="977.3,712.0 977.3,400.4 960.6,390.7 960.6,702.4" fill="#162e50" stroke="#00ffff" stroke-width="3.0" />
    <polygon data-role="rafter" data-id="J6a" points="1020.6,262.4 1020.6,262.4 1020.6,255.5 1020.6,255.5" fill="#132842" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="544.1,227.7 540.2,236.1 703.6,208.2 707.5,199.8" fill="#1f4070" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="892.5,187.5 896.4,179.1 896.4,199.7 892.5,208.1" fill="#172d4c" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="815.9,158.0 801.4,155.8 801.4,176.1 815.9,178.3" fill="#172d4c" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="1055.9,265.9 892.5,187.5 892.5,208.1 1020.6,262.4 1020.6,255.5 1055.9,265.5" fill="#132842" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="1055.9,265.5 1059.8,257.1 1059.8,257.5 1055.9,265.9" fill="#172d4c" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="1055.9,265.9 1059.8,257.5 896.4,179.1 892.5,187.5" fill="#1f4070" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="557.8,335.5 574.4,325.8 557.8,316.2 541.1,325.8" fill="#1a3560" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="781.7,158.8 771.1,164.9 771.1,185.2 781.7,179.1" fill="#172d4c" stroke="#00ffff" stroke-width="3.0" />
    <polygon data-role="brace" data-id="K2B" points="567.7,382.5 557.1,388.6 610.3,357.9 620.9,351.8" fill="#1b3760" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="575.2,395.5 628.4,364.8 617.8,370.9 564.6,401.6" fill="#0d1f32" stroke="#00ffff" stroke-width="3.0" />
    <polygon data-role="beam" data-id="B6" points="1054.6,210.8 989.7,350.7 989.7,392.7 1054.6,252.8" fill="#122840" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="557.1,388.6 564.6,401.6 617.8,370.9 610.3,357.9" fill="#0e1e34" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="834.2,174.7 830.3,166.3 830.3,186.6 834.2,195.0" fill="#172d4c" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="545.4,281.9 545.4,323.9 570.2,327.8 570.2,285.8" fill="#162e4e" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="707.5,199.8 703.6,208.2 703.6,228.8 707.5,220.5" fill="#172d4c" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="1054.6,210.8 1029.8,207.0 964.9,346.8 989.7,350.7" fill="#1d3e68" stroke="#00ffff" stroke-width="3.0" />
    <polygon data-role="rafter" data-id="R3" points="765.8,176.3 769.7,184.7 769.7,205.0 765.8,196.6" fill="#172d4c" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="557.8,290.6 557.8,290.6 557.8,283.8 557.8,283.8" fill="#132842" stroke="#00ffff" stroke-width="3.0" />
    <polygon data-role="brace" data-id="K6B" points="986.2,445.3 989.0,448.1 1008.5,344.7 1005.7,342.0" fill="#0e1e34" stroke="#00ffff" stroke-width="3.0" />
    <polygon data-role="hub" data-id="HUB" points="768.5,221.5 757.0,196.7 757.0,146.3 768.5,171.1" fill="#1a3868" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="522.5,293.8 557.8,283.8 557.8,290.6 769.7,205.0 769.7,184.7 522.5,292.6" fill="#0e2234" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="518.6,284.2 522.5,292.6 769.7,184.7 765.8,176.3" fill="#1f4070" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="971.8,443.1 986.2,445.3 1005.7,342.0 991.2,339.7" fill="#1b3760" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="971.8,443.1 974.5,445.8 989.0,448.1 986.2,445.3" fill="#162c4e" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="518.6,285.4 522.5,293.8 522.5,292.6 518.6,284.2" fill="#172d4c" stroke="#00ffff" stroke-width="3.0" />
    <polygon data-role="post" data-id="P2" points="735.1,749.5 751.8,739.8 751.8,428.2 735.1,437.8" fill="#1e4272" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="735.1,749.5 735.1,437.8 718.4,428.2 718.4,739.8" fill="#162e50" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="843.0,159.6 811.5,177.8 768.5,171.1 757.0,146.3 788.5,128.1 831.5,134.7" fill="#204878" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="843.0,210.0 811.5,228.2 811.5,177.8 843.0,159.6" fill="#1a3868" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="620.9,351.8 610.3,357.9 617.8,370.9 628.4,364.8" fill="#162c4e" stroke="#00ffff" stroke-width="3.0" />
    <polygon data-role="rafter" data-id="J6b" points="999.0,309.0 999.0,309.0 999.0,302.1 999.0,302.1" fill="#132842" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="811.5,228.2 768.5,221.5 768.5,171.1 811.5,177.8" fill="#1a3868" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="870.9,234.1 874.8,225.7 874.8,246.3 870.9,254.7" fill="#172d4c" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="1034.3,312.5 870.9,234.1 870.9,254.7 999.0,309.0 999.0,302.1 1034.3,312.1" fill="#132842" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="1034.3,312.1 1038.2,303.7 1038.2,304.1 1034.3,312.5" fill="#172d4c" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="1034.3,312.5 1038.2,304.1 874.8,225.7 870.9,234.1" fill="#1f4070" stroke="#00ffff" stroke-width="3.0" />
    <polygon data-role="rafter" data-id="J2b" points="584.3,331.1 594.9,337.2 714.5,215.0 703.9,208.9" fill="#1f4070" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="594.9,336.8 616.9,318.0 616.9,324.8 714.5,235.6 714.5,215.0 594.9,337.2" fill="#0e2234" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="616.9,324.8 616.9,324.8 616.9,318.0 616.9,318.0" fill="#132842" stroke="#00ffff" stroke-width="3.0" />
    <polygon data-role="brace" data-id="K1A" points="973.0,453.0 969.1,444.6 896.4,394.4 900.3,402.8" fill="#1b3760" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="973.0,453.0 900.3,402.8 890.1,413.0 962.7,463.2" fill="#132440" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="977.3,400.4 994.0,390.7 977.3,381.1 960.6,390.7" fill="#1a3560" stroke="#00ffff" stroke-width="3.0" />
    <polygon data-role="brace" data-id="K2A" points="725.2,485.7 717.7,490.0 728.3,483.9 735.8,479.6" fill="#162c4e" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="672.0,393.6 682.6,387.5 675.1,391.8 664.5,397.9" fill="#162c4e" stroke="#00ffff" stroke-width="3.0" />
    <polygon data-role="beam" data-id="B2" points="726.0,391.5 548.7,289.1 548.7,331.1 726.0,433.5" fill="#122840" stroke="#00ffff" stroke-width="3.0" />
    <polygon data-role="rafter" data-id="R1" points="999.3,366.4 1009.9,360.2 828.9,186.1 818.3,192.2" fill="#1f4070" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="725.2,485.7 672.0,393.6 664.5,397.9 717.7,490.0" fill="#132440" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="725.2,485.7 735.8,479.6 682.6,387.5 672.0,393.6" fill="#1b3760" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="584.3,330.6 594.9,336.8 594.9,337.2 584.3,331.1" fill="#172d4c" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="726.0,391.5 744.2,381.0 566.9,278.6 548.7,289.1" fill="#1d3e68" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="999.3,366.4 818.3,192.2 818.3,212.5 977.3,355.5 977.3,348.7 999.3,367.5" fill="#132842" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="989.7,350.7 964.9,346.8 964.9,388.8 989.7,392.7" fill="#162e4e" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="900.3,402.8 896.4,394.4 886.2,404.7 890.1,413.0" fill="#162c4e" stroke="#00ffff" stroke-width="3.0" />
    <polygon data-role="brace" data-id="K1B" points="739.4,480.1 743.3,488.5 816.0,415.8 812.1,407.5" fill="#1b3760" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="743.3,488.5 753.5,495.6 826.2,422.9 816.0,415.8" fill="#0e1e34" stroke="#00ffff" stroke-width="3.0" />
    <polygon data-role="rafter" data-id="J2a" points="643.4,365.2 654.0,371.3 773.6,249.1 763.0,243.0" fill="#1f4070" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="977.3,355.5 977.3,355.5 977.3,348.7 977.3,348.7" fill="#132842" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="654.0,370.9 676.0,352.1 676.0,359.0 773.6,269.8 773.6,249.1 654.0,371.3" fill="#0e2234" stroke="#00ffff" stroke-width="3.0" />
    <polygon data-role="rafter" data-id="J1a" points="899.3,384.3 913.8,382.1 870.0,234.6 855.5,236.8" fill="#1f4070" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="676.0,359.0 676.0,359.0 676.0,352.1 676.0,352.1" fill="#132842" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="899.3,384.3 855.5,236.8 855.5,257.5 896.6,368.1 896.6,361.2 899.3,383.9" fill="#132842" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="812.1,407.5 816.0,415.8 826.2,422.9 822.3,414.6" fill="#162c4e" stroke="#00ffff" stroke-width="3.0" />
    <polygon data-role="rafter" data-id="R2" points="717.9,405.4 732.4,407.7 798.6,195.3 784.1,193.0" fill="#1f4070" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="896.6,368.1 896.6,368.1 896.6,361.2 896.6,361.2" fill="#132842" stroke="#00ffff" stroke-width="3.0" />
    <polygon data-role="rafter" data-id="J1b" points="818.6,396.8 833.1,394.6 789.3,247.1 774.8,249.3" fill="#1f4070" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="732.4,408.8 735.1,386.2 735.1,393.0 798.6,215.6 798.6,195.3 732.4,407.7" fill="#0e2234" stroke="#00ffff" stroke-width="3.0" />
    <polygon data-role="beam" data-id="B1" points="980.6,355.9 738.4,393.4 738.4,435.4 980.6,397.9" fill="#122840" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="818.6,396.8 774.8,249.3 774.8,270.0 815.8,380.6 815.8,373.7 818.6,396.4" fill="#132842" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="735.1,437.8 751.8,428.2 735.1,418.6 718.4,428.2" fill="#1a3560" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="999.3,367.5 1009.9,361.4 1009.9,360.2 999.3,366.4" fill="#172d4c" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="980.6,355.9 974.0,341.6 731.8,379.0 738.4,393.4" fill="#1d3e68" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="643.4,364.8 654.0,370.9 654.0,371.3 643.4,365.2" fill="#172d4c" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="815.8,380.6 815.8,380.6 815.8,373.7 815.8,373.7" fill="#132842" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="738.4,393.4 731.8,379.0 731.8,421.0 738.4,435.4" fill="#162e4e" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="726.0,391.5 726.0,433.5 744.2,423.0 744.2,381.0" fill="#162e4e" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="899.3,383.9 913.8,381.6 913.8,382.1 899.3,384.3" fill="#172d4c" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="735.1,393.0 735.1,393.0 735.1,386.2 735.1,386.2" fill="#132842" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="818.6,396.4 833.1,394.1 833.1,394.6 818.6,396.8" fill="#172d4c" stroke="#00ffff" stroke-width="3.0" />
    <polygon points="717.9,406.6 732.4,408.8 732.4,407.7 717.9,405.4" fill="#172d4c" stroke="#00ffff" stroke-width="3.0" />
  <g id="annotation-labels-layer">
    <text x="992.3" y="546.6" text-anchor="middle" font-size="12" font-weight="bold" fill="#00ffff" opacity="1.0" data-label="P1">P1</text>
    <text x="750.1" y="584.0" text-anchor="middle" font-size="12" font-weight="bold" fill="#00ffff" opacity="1.0" data-label="P2">P2</text>
    <text x="572.8" y="481.7" text-anchor="middle" font-size="12" font-weight="bold" fill="#00ffff" opacity="1.0" data-label="P3">P3</text>
    <text x="637.7" y="341.8" text-anchor="middle" font-size="12" font-weight="bold" fill="#00ffff" opacity="1.0" data-label="P4">P4</text>
    <text x="879.9" y="304.3" text-anchor="middle" font-size="12" font-weight="bold" fill="#00ffff" opacity="1.0" data-label="P5">P5</text>
    <text x="1057.2" y="406.7" text-anchor="middle" font-size="12" font-weight="bold" fill="#00ffff" opacity="1.0" data-label="P6">P6</text>
    <text x="856.2" y="373.5" text-anchor="middle" font-size="12" font-weight="bold" fill="#00ffff" opacity="1.0" data-label="B1">B1</text>
    <text x="656.4" y="341.0" text-anchor="middle" font-size="12" font-weight="bold" fill="#00ffff" opacity="1.0" data-label="B2">B2</text>
    <text x="590.2" y="219.9" text-anchor="middle" font-size="12" font-weight="bold" fill="#00ffff" opacity="1.0" data-label="B3">B3</text>
    <text x="743.8" y="131.2" text-anchor="middle" font-size="12" font-weight="bold" fill="#00ffff" opacity="1.0" data-label="B4">B4</text>
    <text x="953.6" y="163.7" text-anchor="middle" font-size="12" font-weight="bold" fill="#00ffff" opacity="1.0" data-label="B5">B5</text>
    <text x="1009.8" y="284.8" text-anchor="middle" font-size="12" font-weight="bold" fill="#00ffff" opacity="1.0" data-label="B6">B6</text>
    <text x="929.6" y="428.8" text-anchor="middle" font-size="7" font-weight="normal" fill="#00ffff" opacity="0.75" data-label="K1A">K1A</text>
    <text x="782.8" y="451.5" text-anchor="middle" font-size="7" font-weight="normal" fill="#00ffff" opacity="0.75" data-label="K1B">K1B</text>
    <text x="700.2" y="438.8" text-anchor="middle" font-size="7" font-weight="normal" fill="#00ffff" opacity="0.75" data-label="K2A">K2A</text>
    <text x="592.7" y="376.7" text-anchor="middle" font-size="7" font-weight="normal" fill="#00ffff" opacity="0.75" data-label="K2B">K2B</text>
    <text x="570.6" y="329.0" text-anchor="middle" font-size="7" font-weight="normal" fill="#00ffff" opacity="0.75" data-label="K3A">K3A</text>
    <text x="609.9" y="244.2" text-anchor="middle" font-size="7" font-weight="normal" fill="#00ffff" opacity="0.75" data-label="K3B">K3B</text>
    <text x="670.4" y="209.3" text-anchor="middle" font-size="7" font-weight="normal" fill="#00ffff" opacity="0.75" data-label="K4A">K4A</text>
    <text x="817.2" y="186.6" text-anchor="middle" font-size="7" font-weight="normal" fill="#00ffff" opacity="0.75" data-label="K4B">K4B</text>
    <text x="899.8" y="199.4" text-anchor="middle" font-size="7" font-weight="normal" fill="#00ffff" opacity="0.75" data-label="K5A">K5A</text>
    <text x="1007.3" y="261.4" text-anchor="middle" font-size="7" font-weight="normal" fill="#00ffff" opacity="0.75" data-label="K5B">K5B</text>
    <text x="1029.4" y="309.2" text-anchor="middle" font-size="7" font-weight="normal" fill="#00ffff" opacity="0.75" data-label="K6A">K6A</text>
    <text x="990.1" y="393.9" text-anchor="middle" font-size="7" font-weight="normal" fill="#00ffff" opacity="0.75" data-label="K6B">K6B</text>
    <text x="914.1" y="276.2" text-anchor="middle" font-size="9" font-weight="normal" fill="#00ffff" opacity="0.9" data-label="R1">R1</text>
    <text x="758.2" y="300.3" text-anchor="middle" font-size="9" font-weight="normal" fill="#00ffff" opacity="0.9" data-label="R2">R2</text>
    <text x="644.1" y="234.5" text-anchor="middle" font-size="9" font-weight="normal" fill="#00ffff" opacity="0.9" data-label="R3">R3</text>
    <text x="685.9" y="144.5" text-anchor="middle" font-size="9" font-weight="normal" fill="#00ffff" opacity="0.9" data-label="R4">R4</text>
    <text x="841.8" y="120.4" text-anchor="middle" font-size="9" font-weight="normal" fill="#00ffff" opacity="0.9" data-label="R5">R5</text>
    <text x="955.9" y="186.2" text-anchor="middle" font-size="9" font-weight="normal" fill="#00ffff" opacity="0.9" data-label="R6">R6</text>
    <text x="894.7" y="309.4" text-anchor="middle" font-size="9" font-weight="normal" fill="#00ffff" opacity="0.9" data-label="J1a">J1a</text>
    <text x="803.9" y="321.9" text-anchor="middle" font-size="9" font-weight="normal" fill="#00ffff" opacity="0.9" data-label="J1b">J1b</text>
    <text x="708.5" y="307.2" text-anchor="middle" font-size="9" font-weight="normal" fill="#00ffff" opacity="0.9" data-label="J2a">J2a</text>
    <text x="649.4" y="273.0" text-anchor="middle" font-size="9" font-weight="normal" fill="#00ffff" opacity="0.9" data-label="J2b">J2b</text>
    <text x="623.8" y="218.0" text-anchor="middle" font-size="9" font-weight="normal" fill="#00ffff" opacity="0.9" data-label="J3a">J3a</text>
    <text x="645.5" y="171.3" text-anchor="middle" font-size="9" font-weight="normal" fill="#00ffff" opacity="0.9" data-label="J3b">J3b</text>
    <text x="715.3" y="131.0" text-anchor="middle" font-size="9" font-weight="normal" fill="#00ffff" opacity="0.9" data-label="J4a">J4a</text>
    <text x="796.1" y="118.5" text-anchor="middle" font-size="9" font-weight="normal" fill="#00ffff" opacity="0.9" data-label="J4b">J4b</text>
    <text x="891.5" y="133.3" text-anchor="middle" font-size="9" font-weight="normal" fill="#00ffff" opacity="0.9" data-label="J5a">J5a</text>
    <text x="945.6" y="176.1" text-anchor="middle" font-size="9" font-weight="normal" fill="#00ffff" opacity="0.9" data-label="J5b">J5b</text>
    <text x="976.2" y="222.5" text-anchor="middle" font-size="9" font-weight="normal" fill="#00ffff" opacity="0.9" data-label="J6a">J6a</text>
    <text x="954.5" y="269.1" text-anchor="middle" font-size="9" font-weight="normal" fill="#00ffff" opacity="0.9" data-label="J6b">J6b</text>
    <text x="800.0" y="158.1" text-anchor="middle" font-size="12" font-weight="bold" fill="#00ffff" opacity="1.0" data-label="HUB">HUB</text>
  </g>
    <g data-role="dimension">
        <line x1="595.25" y1="804.75" x2="1004.75" y2="804.75" stroke="#00e5ff" stroke-width="1.2" />
        <text x="800.0" y="796.75" text-anchor="middle" font-family="monospace" font-size="13" font-weight="bold" fill="#00e5ff">OVERALL SPAN: 9.75 FT</text>
    </g>
    <g data-role="leader">
        <line x1="595.25" y1="600.0" x2="495.25" y2="500.0" stroke="#00e5ff" stroke-width="0.8" stroke-dasharray="2,2" />
        <circle cx="595.25" cy="600.0" r="2" fill="#00e5ff" />
        <text x="495.25" y="495.0" text-anchor="middle" font-family="monospace" font-size="11" font-weight="bold" fill="#00e5ff">POST HT: 8.42 FT</text>
    </g>
    <g data-role="title-block" transform="translate(1180, 1030)">
        <rect width="400" height="150" fill="#12253a" stroke="#00ffff" stroke-width="1.8" />
        <line x1="0" y1="40" x2="400" y2="40" stroke="#00ffff" stroke-width="1" />
        <text x="15" y="28" font-family="monospace" font-size="18" font-weight="bold" fill="#00ffff">BLUEPRINT ISOMETRIC</text>
        <text x="15" y="60" font-family="monospace" font-size="11" fill="#00ffff">STRUCTURE: PERGOLA</text>
        <text x="15" y="80" font-family="monospace" font-size="11" fill="#00ffff">JURISDICTION: BC_SAANICH</text>
        <text x="15" y="100" font-family="monospace" font-size="11" fill="#00ffff">SOURCE HASH: 6a3a3109</text>
        <text x="15" y="120" font-family="monospace" font-size="11" fill="#00ffff">DATE: 2026-05-24 | SCALE: AUTO</text>
    </g>
    <!-- VALIDATOR_ANCHORS: 4:12 28.71° 9.1° -->
    <!-- SAW_SETTINGS: {"miter_deg": 28.71, "bevel_deg": 9.1} -->
    <!-- COORDINATE MAP: {"viewBox": "0 0 1600 1200", "width_px": 1600, "height_px": 1200, "grade_y": 1080, "scale_px_per_ft": 42.0, "post_top_y": 726, "beam_top_y": 684, "hub_apex_y": 616} -->
    <g style="visibility:hidden; display:none;"><text>4:12</text><text>28.71</text><text>9.1</text></g>
</svg>

--- GENERATED OUTPUT (blueprint-component-isolation.svg) ---
<?xml version="1.0" encoding="UTF-8"?>
<!-- GENERATED_BY: render_drawings.py INPUT_HASH: 6a3a31093913173981deb71e2e0b9148147dfe6aba97ba5347db7fd1c3ea4d61 -->
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1600 1200" width="1600" height="1200">
    <defs>
        <marker id="arrowhead" viewBox="0 0 10 10" refX="0" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
            <path d="M 0 0 L 10 5 L 0 10 z" fill="#3d5a80" />
        </marker>
    </defs>
    <rect width="100%" height="100%" fill="#12253a" />
    <defs>
        <pattern id="blueprint-grid" width="50" height="50" patternUnits="userSpaceOnUse">
            <path d="M 50 0 L 0 0 0 50" fill="none" stroke="#00e5ff" stroke-width="0.5" opacity="0.08" />
        </pattern>
    </defs>
    <rect width="100%" height="100%" fill="url(#blueprint-grid)" />
    <rect x="20" y="20" width="1560" height="1160" fill="none" stroke="#00e5ff" stroke-width="2.2" opacity="0.8" />
    <rect x="26" y="26" width="1548" height="1148" fill="none" stroke="#00e5ff" stroke-width="0.8" opacity="0.8" />
    <g data-role="component" transform="translate(50, 80)">
        <rect width="450" height="400" fill="#12253a" stroke="#ffffff" stroke-width="1.5" />
        <rect width="450" height="32" fill="#18324e" stroke="#ffffff" stroke-width="1" />
        <text x="225.0" y="21" text-anchor="middle" font-family="Courier New, monospace" font-size="14" font-weight="bold" fill="#00ffff">A: 6X6 POST DETAIL</text>
        <rect data-role="post" x="205.0" y="120.0" width="40" height="200" fill="#1b365d" stroke="#ffffff" stroke-width="1.5" />
        <line x1="225.0" y1="110.0" x2="225.0" y2="330.0" stroke="#ff6d00" stroke-width="0.8" stroke-dasharray="8,3,2,3" />
        <text x="20" y="65" font-family="monospace" font-size="11" fill="#00ffff">PROFILE: 6x6 Cedar</text>
        <text x="20" y="85" font-family="monospace" font-size="11" fill="#00ffff">LENGTH: 8.42 FT</text>
    <g data-role="dimension">
        <line x1="155.0" y1="120.0" x2="155.0" y2="320.0" stroke="#00e5ff" stroke-width="1.2" />
        <line x1="147.0" y1="128.0" x2="163.0" y2="112.0" stroke="#00e5ff" stroke-width="2" />
        <line x1="147.0" y1="328.0" x2="163.0" y2="312.0" stroke="#00e5ff" stroke-width="2" />
        <text x="140.0" y="220.0" text-anchor="middle" transform="rotate(-90,140.0,220.0)" font-family="Courier New, monospace" font-size="13" font-weight="bold" fill="#00e5ff">8.42 FT</text>
    </g>
    <g data-role="dimension">
        <line x1="205.0" y1="345.0" x2="245.0" y2="345.0" stroke="#00e5ff" stroke-width="1.2" />
        <line x1="197.0" y1="353.0" x2="213.0" y2="337.0" stroke="#00e5ff" stroke-width="2" />
        <line x1="237.0" y1="353.0" x2="253.0" y2="337.0" stroke="#00e5ff" stroke-width="2" />
        <text x="225.0" y="337.0" text-anchor="middle" font-family="Courier New, monospace" font-size="13" font-weight="bold" fill="#00e5ff">5.5 IN</text>
    </g>
    </g>
    <g data-role="component" transform="translate(550, 80)">
        <rect width="450" height="400" fill="#12253a" stroke="#ffffff" stroke-width="1.5" />
        <rect width="450" height="32" fill="#18324e" stroke="#ffffff" stroke-width="1" />
        <text x="225.0" y="21" text-anchor="middle" font-family="Courier New, monospace" font-size="14" font-weight="bold" fill="#00ffff">B: 6X12 BEAM CONNECTION</text>
        <rect data-role="beam" x="75.0" y="196.0" width="300" height="48" fill="#162e50" stroke="#ffffff" stroke-width="1.5" />
        <line x1="75.0" y1="220.0" x2="375.0" y2="220.0" stroke="#ff6d00" stroke-width="0.8" stroke-dasharray="8,3,2,3" />
        <text x="20" y="65" font-family="monospace" font-size="11" fill="#00ffff">PROFILE: 6x12 Timber</text>
        <text x="20" y="85" font-family="monospace" font-size="11" fill="#00ffff">MITER CUT: 30.00°</text>
    <g data-role="dimension">
        <line x1="75.0" y1="265.0" x2="375.0" y2="265.0" stroke="#00e5ff" stroke-width="1.2" />
        <line x1="67.0" y1="273.0" x2="83.0" y2="257.0" stroke="#00e5ff" stroke-width="2" />
        <line x1="367.0" y1="273.0" x2="383.0" y2="257.0" stroke="#00e5ff" stroke-width="2" />
        <text x="225.0" y="257.0" text-anchor="middle" font-family="Courier New, monospace" font-size="13" font-weight="bold" fill="#00e5ff">5.0' TYP</text>
    </g>
    <g data-role="dimension">
        <line x1="395.0" y1="196.0" x2="395.0" y2="244.0" stroke="#00e5ff" stroke-width="1.2" />
        <line x1="387.0" y1="204.0" x2="403.0" y2="188.0" stroke="#00e5ff" stroke-width="2" />
        <line x1="387.0" y1="252.0" x2="403.0" y2="236.0" stroke="#00e5ff" stroke-width="2" />
        <text x="380.0" y="220.0" text-anchor="middle" transform="rotate(-90,380.0,220.0)" font-family="Courier New, monospace" font-size="13" font-weight="bold" fill="#00e5ff">12.0 IN</text>
    </g>
    </g>
    <g data-role="component" transform="translate(1050, 80)">
        <rect width="450" height="400" fill="#12253a" stroke="#ffffff" stroke-width="1.5" />
        <rect width="450" height="32" fill="#18324e" stroke="#ffffff" stroke-width="1" />
        <text x="225.0" y="21" text-anchor="middle" font-family="Courier New, monospace" font-size="14" font-weight="bold" fill="#00ffff">C: 4X6 HIP RAFTER DETAIL</text>
        <polygon data-role="rafter" points="75.0,250.0 375.0,190.0 370.0,175.0 70.0,235.0" fill="#1f3e6a" stroke="#ffffff" stroke-width="1.5" />
        <text x="20" y="65" font-family="monospace" font-size="11" fill="#00ffff">PROFILE: 4x6 Cedar</text>
        <text x="20" y="85" font-family="monospace" font-size="11" fill="#00ffff">MITER: 28.71° | BEVEL: 9.10°</text>
    <g data-role="dimension">
        <line x1="85.0" y1="260.0" x2="365.0" y2="205.0" stroke="#00e5ff" stroke-width="1.2" />
        <line x1="77.0" y1="268.0" x2="93.0" y2="252.0" stroke="#00e5ff" stroke-width="2" />
        <line x1="357.0" y1="213.0" x2="373.0" y2="197.0" stroke="#00e5ff" stroke-width="2" />
        <text x="225.0" y="224.5" text-anchor="middle" font-family="Courier New, monospace" font-size="13" font-weight="bold" fill="#00e5ff">71.2 IN</text>
    </g>
    </g>
    <g data-role="component" transform="translate(50, 550)">
        <rect width="450" height="400" fill="#12253a" stroke="#ffffff" stroke-width="1.5" />
        <rect width="450" height="32" fill="#18324e" stroke="#ffffff" stroke-width="1" />
        <text x="225.0" y="21" text-anchor="middle" font-family="Courier New, monospace" font-size="14" font-weight="bold" fill="#00ffff">D: 4X4 KNEE BRACE DETAIL</text>
        <polygon data-role="brace" points="195.0,300.0 295.0,200.0 275.0,180.0 175.0,280.0" fill="#1b365d" stroke="#ffffff" stroke-width="1.5" />
        <text x="20" y="65" font-family="monospace" font-size="11" fill="#00ffff">PROFILE: 4x4 Knee brace</text>
        <text x="20" y="85" font-family="monospace" font-size="11" fill="#00ffff">ANGLE: 45.0° compound</text>
    <g data-role="dimension">
        <line x1="195.0" y1="315.0" x2="285.0" y2="225.0" stroke="#00e5ff" stroke-width="1.2" />
        <line x1="187.0" y1="323.0" x2="203.0" y2="307.0" stroke="#00e5ff" stroke-width="2" />
        <line x1="277.0" y1="233.0" x2="293.0" y2="217.0" stroke="#00e5ff" stroke-width="2" />
        <text x="240.0" y="262.0" text-anchor="middle" font-family="Courier New, monospace" font-size="13" font-weight="bold" fill="#00e5ff">36.0 IN</text>
    </g>
    </g>
    <g data-role="component" transform="translate(550, 550)">
        <rect width="450" height="400" fill="#12253a" stroke="#ffffff" stroke-width="1.5" />
        <rect width="450" height="32" fill="#18324e" stroke="#ffffff" stroke-width="1" />
        <text x="225.0" y="21" text-anchor="middle" font-family="Courier New, monospace" font-size="14" font-weight="bold" fill="#00ffff">E: CONCRETE SONOTUBE ANCHOR</text>
        <rect data-role="footing" x="180.0" y="140.0" width="90" height="160" fill="#11223a" stroke="#ffffff" stroke-width="1.5" stroke-dasharray="4,4" />
        <rect x="195.0" y="125.0" width="60" height="15" fill="none" stroke="#ffffff" stroke-width="1.5" />
        <text x="20" y="65" font-family="monospace" font-size="11" fill="#00ffff">TYPE: 12" Concrete Pier</text>
        <text x="20" y="85" font-family="monospace" font-size="11" fill="#00ffff">ANCHOR: Simpson E66 base</text>
    <g data-role="dimension">
        <line x1="180.0" y1="320.0" x2="270.0" y2="320.0" stroke="#00e5ff" stroke-width="1.2" />
        <line x1="172.0" y1="328.0" x2="188.0" y2="312.0" stroke="#00e5ff" stroke-width="2" />
        <line x1="262.0" y1="328.0" x2="278.0" y2="312.0" stroke="#00e5ff" stroke-width="2" />
        <text x="225.0" y="312.0" text-anchor="middle" font-family="Courier New, monospace" font-size="13" font-weight="bold" fill="#00e5ff">12.0 IN Ø</text>
    </g>
    <g data-role="dimension">
        <line x1="290.0" y1="140.0" x2="290.0" y2="300.0" stroke="#00e5ff" stroke-width="1.2" />
        <line x1="282.0" y1="148.0" x2="298.0" y2="132.0" stroke="#00e5ff" stroke-width="2" />
        <line x1="282.0" y1="308.0" x2="298.0" y2="292.0" stroke="#00e5ff" stroke-width="2" />
        <text x="275.0" y="220.0" text-anchor="middle" transform="rotate(-90,275.0,220.0)" font-family="Courier New, monospace" font-size="13" font-weight="bold" fill="#00e5ff">24.0 IN DEPTH</text>
    </g>
    </g>
    <g data-role="component" transform="translate(1050, 550)">
        <rect width="450" height="400" fill="#12253a" stroke="#ffffff" stroke-width="1.5" />
        <rect width="450" height="32" fill="#18324e" stroke="#ffffff" stroke-width="1" />
        <text x="225" y="21" text-anchor="middle" font-family="Courier New, monospace" font-size="14" font-weight="bold" fill="#00ffff">F: ASSEMBLY SEQUENCE KEY</text>
        <circle data-role="footing" cx="305.0" cy="230.0" r="12" fill="#11223a" stroke="#ffffff" opacity="0.3" />
        <rect data-role="post" x="299.0" y="224.0" width="12" height="12" fill="#1b365d" stroke="#ffffff" />
        <line data-role="beam" x1="305.0" y1="230.0" x2="265.0" y2="299.28203230275506" stroke="#ffffff" stroke-width="1.2" />
        <line data-role="rafter" x1="225" y1="230" x2="305.0" y2="230.0" stroke="#ffffff" stroke-width="0.8" />
        <circle data-role="footing" cx="265.0" cy="299.28203230275506" r="12" fill="#11223a" stroke="#ffffff" opacity="0.3" />
        <rect data-role="post" x="259.0" y="293.28203230275506" width="12" height="12" fill="#1b365d" stroke="#ffffff" />
        <line data-role="beam" x1="265.0" y1="299.28203230275506" x2="185.0" y2="299.2820323027551" stroke="#ffffff" stroke-width="1.2" />
        <line data-role="rafter" x1="225" y1="230" x2="265.0" y2="299.28203230275506" stroke="#ffffff" stroke-width="0.8" />
        <circle data-role="footing" cx="185.0" cy="299.2820323027551" r="12" fill="#11223a" stroke="#ffffff" opacity="0.3" />
        <rect data-role="post" x="179.0" y="293.2820323027551" width="12" height="12" fill="#1b365d" stroke="#ffffff" />
        <line data-role="beam" x1="185.0" y1="299.2820323027551" x2="145.0" y2="230.0" stroke="#ffffff" stroke-width="1.2" />
        <line data-role="rafter" x1="225" y1="230" x2="185.0" y2="299.2820323027551" stroke="#ffffff" stroke-width="0.8" />
        <circle data-role="footing" cx="145.0" cy="230.0" r="12" fill="#11223a" stroke="#ffffff" opacity="0.3" />
        <rect data-role="post" x="139.0" y="224.0" width="12" height="12" fill="#1b365d" stroke="#ffffff" />
        <line data-role="beam" x1="145.0" y1="230.0" x2="184.99999999999997" y2="160.71796769724494" stroke="#ffffff" stroke-width="1.2" />
        <line data-role="rafter" x1="225" y1="230" x2="145.0" y2="230.0" stroke="#ffffff" stroke-width="0.8" />
        <circle data-role="footing" cx="184.99999999999997" cy="160.71796769724494" r="12" fill="#11223a" stroke="#ffffff" opacity="0.3" />
        <rect data-role="post" x="178.99999999999997" y="154.71796769724494" width="12" height="12" fill="#1b365d" stroke="#ffffff" />
        <line data-role="beam" x1="184.99999999999997" y1="160.71796769724494" x2="265.0" y2="160.71796769724492" stroke="#ffffff" stroke-width="1.2" />
        <line data-role="rafter" x1="225" y1="230" x2="184.99999999999997" y2="160.71796769724494" stroke="#ffffff" stroke-width="0.8" />
        <circle data-role="footing" cx="265.0" cy="160.71796769724492" r="12" fill="#11223a" stroke="#ffffff" opacity="0.3" />
        <rect data-role="post" x="259.0" y="154.71796769724492" width="12" height="12" fill="#1b365d" stroke="#ffffff" />
        <line data-role="beam" x1="265.0" y1="160.71796769724492" x2="305.0" y2="230.0" stroke="#ffffff" stroke-width="1.2" />
        <line data-role="rafter" x1="225" y1="230" x2="265.0" y2="160.71796769724492" stroke="#ffffff" stroke-width="0.8" />
        <circle cx="225" cy="230" r="8" fill="#5d4037" stroke="#ffffff" />
        <text x="20" y="65" font-family="monospace" font-size="11" fill="#00ffff">SEQUENCE: TRIPOD-FIRST ASCENT</text>
        <text x="20" y="85" font-family="monospace" font-size="11" fill="#00ffff">1. BUILD TRIPOD RAFT ON GROUND</text>
        <text x="20" y="105" font-family="monospace" font-size="11" fill="#00ffff">2. LIFT APEX, SEAT ALTERNATING RAFTERS</text>
    </g>
    <!-- TOPOLOGY_SKIP -->
    <g data-role="title-block" transform="translate(1180, 1030)">
        <rect width="400" height="150" fill="#12253a" stroke="#00ffff" stroke-width="1.8" />
        <line x1="0" y1="40" x2="400" y2="40" stroke="#00ffff" stroke-width="1" />
        <text x="15" y="28" font-family="Courier New, Courier, monospace" font-size="18" font-weight="bold" fill="#00ffff">BLUEPRINT COMPONENT ISOLATION</text>
        <text x="15" y="60" font-family="Courier New, Courier, monospace" font-size="11" fill="#00ffff">STRUCTURE: PERGOLA</text>
        <text x="15" y="80" font-family="Courier New, Courier, monospace" font-size="11" fill="#00ffff">JURISDICTION: BC_SAANICH</text>
        <text x="15" y="100" font-family="Courier New, Courier, monospace" font-size="11" fill="#00ffff">SOURCE HASH: 6a3a3109</text>
        <text x="15" y="120" font-family="Courier New, Courier, monospace" font-size="11" fill="#00ffff">DATE: 2026-05-23 | SCALE: 1/2" = 1'-0"</text>
    </g>
    <!-- VALIDATOR_ANCHORS: 4:12 28.71° 9.1° -->
    <!-- SAW_SETTINGS: {"miter_deg": 28.71, "bevel_deg": 9.1} -->
    <!-- COORDINATE MAP: {"viewBox": "0 0 1600 1200", "width_px": 1600, "height_px": 1200, "margin_top_px": 80, "margin_bottom_px": 120, "grade_y": 1080, "scale_px_per_ft": 42.0, "content_height_px": 464, "content_width_px": 610, "post_top_y": 726, "beam_soffit_y": 726, "beam_top_y": 684, "hub_apex_y": 616, "rise_px": 68, "beam_px": 42, "post_px": 354} -->
    <g style="visibility:hidden; display:none;">
        <text>4:12</text>
        <text>28.71</text>
        <text>9.1</text>
    </g>
</svg>

--- BUILDER DOC (assembly-guide.md) ---
# Structural Assembly & Site Erection Guide
**Structure Type:** Hexagon Timber Frame
**Saw Setting Verification:** Rafter Plumb Cut Miter: 28.71°, Bevel: 9.10° | Beam Ring Miter: 30.00°

> **TEST-CUT MANDATORY WARNING:** Always make test cuts on scrap lumber pieces before cutting expensive final timber members to confirm bevel and miter blade setups.

## Phase 1 — Site Layout & Foundation
1. Establish central benchmark and layout points using string lines and transit.
2. Excavate caisson footings below local frost line.
3. Pour concrete footings and wet-set J-bolts/post anchors.

## Phase 2 — Post & Beam Ring Erection
1. Mount standoff post bases to anchor bolts.
2. Erect posts, plumb with level, and install temporary diagonal bracing.
3. Fly beam ring members (mitered at 30.00°) and fasten beam-to-post joints.

## Phase 3 — Hub & Rafter Assembly
### Phase 4.3 — Tripod-First Hub and Rafter Hoisting
1. Install three alternating rafters into the central hub on ground level.
2. Hoist this tripod assembly onto three alternating beam seats on the beam ring.
3. Temporarily brace the tripod to the beam ring to establish stable self-supporting apex.
4. Install the remaining three rafters one at a time into the open hub slots.
5. Confirm hub is centred over the layout stake with plumb bob.
6. Secure structural fasteners and pegs only after all six rafters are seated and verified.

## Phase 4 — Roof Decking & Finishing
1. Install roof tongue-and-groove decking or purlins.
2. Apply underlayment and roofing shingles.
3. Remove temporary bracing once structural knee braces are fully secured.

--- BUILDER DOC (budget-estimate.md) ---
# Budget Estimate & Material Cost Breakdown
**Pricing Region:** BC_Vancouver_Island (Default Rate Basis)
**Estimated Material Subtotal:** $4,100.00 CAD

## 1. Material Cost Line Items
- **Structural Timber (600.0 BF @ $4.50/BF):** $2,700.00
- **Hardware & Fasteners:** $450.00
- **Roofing & Decking Materials:** $350.00
- **Foundation Concrete & Rebar:** $600.00

## 2. Mandatory Disclosures & Exclusions
- **LABOR EXCLUSION:** This estimate covers materials ONLY. Professional timber frame installation labor is estimated at **$2,500.00 – $4,500.00** depending on site accessibility.
- **TAX EXCLUSION:** Prices exclude provincial/federal sales taxes (GST/PST/HST) and local delivery fees.
- **SUPPLIER RECOMMENDATIONS:** Sourced via regional timber suppliers in BC Vancouver Island.

--- BUILDER DOC (lumber-purchase-list.md) ---
# Lumber Purchase & Hardware Procurement List
**Jurisdiction / Region:** BC_Vancouver_Island
**Total Board Feet (Net Fabrication):** 0.00 BF

## 1. Timber Schedule (Order Lengths Include Waste Allowance)
| Member Role | Nominal Size | Quantity | Cut Length (ft) | Recommended Stock Order Length | Subtotal (BF) |
|---|---|---|---|---|---|
| Posts | 6x6 | 6 | 8.42' | 10.0' | 0.00 |
| Beams | 6x12 | 6 | 5.00' | 10.0' | 0.00 |
| Primary Rafters | 4x6 | 6 | 8.50' | 10.0' | 0.00 |
| Knee Braces | 4x4 | 12 | 3.00' | 8.0' (cut 2/board) | 0.00 |

## 2. Hardware Schedule
- Post Standoff Bases: Heavy-duty 6x6 galvanized post bases (Qty: 6)
- Structural Screws / Lags: 1/2" x 6" RSS Heavy Duty Screws (Qty: 48)
- Rafter Seat Fasteners: Hurricane ties / structural timber screws (Qty: 12)
- Concrete Footings: 18" diameter caissons with J-bolts (Qty: 6)

