
## COLORS ##
CT_WHITE        = (1.000, 1.000, 1.000, 1.000)
CT_RED          = (1.000, 0.500, 0.500, 1.000)
CT_BROWN        = (0.641, 0.355, 0.270, 1.000)
CT_CANTELOPE    = (0.839, 0.651, 0.549, 1.000)
CT_TAN          = (0.996, 0.695, 0.512, 1.000)
CT_ORANGE       = (0.992, 0.480, 0.168, 1.000)
CT_CORAL        = (0.832, 0.500, 0.297, 1.000)
CT_PEACH        = (1.000, 0.820, 0.700, 1.000)
CT_BEIGE        = (1.000, 0.800, 0.600, 1.000)
CT_TAN2         = (0.808, 0.678, 0.510, 1.000)
CT_SIENNA       = (0.570, 0.449, 0.164, 1.000)
CT_YELLOW       = (0.996, 0.898, 0.320, 1.000)
CT_CREAM        = (0.996, 0.957, 0.598, 1.000)
CT_BEIGE2       = (1.000, 1.000, 0.600, 1.000)
CT_YELLOW2      = (1.000, 1.000, 0.700, 1.000)
CT_CITRINE      = (0.855, 0.934, 0.492, 1.000)
CT_FOREST_GREEN = (0.500, 0.586, 0.400, 1.000)
CT_LINE         = (0.551, 0.824, 0.324, 1.000)
CT_PALE_GREEN   = (0.789, 1.000, 0.700, 1.000)
CT_GREEN        = (0.305, 0.969, 0.402, 1.000)
CT_TEAL         = (0.600, 1.000, 0.800, 1.000)
CT_SEA_GREEN    = (0.242, 0.742, 0.516, 1.000)
CT_LIGHT_BLUE   = (0.434, 0.906, 0.836, 1.000)
CT_AQUA         = (0.348, 0.820, 0.953, 1.000)
CT_BLUE         = (0.191, 0.563, 0.773, 1.000)
CT_LIGHT_BLUE2  = (0.875, 0.937, 1.000, 1.000)
CT_PERIWINKLE   = (0.559, 0.590, 0.875, 1.000)
CT_ROYAL_BLUE   = (0.285, 0.328, 0.727, 1.000)
CT_GREY         = (0.700, 0.700, 0.800, 1.000)
CT_BLUE2        = (0.600, 0.600, 1.000, 1.000)
CT_SLATE_BLUE   = (0.461, 0.379, 0.824, 1.000)
CT_PURPLE       = (0.547, 0.281, 0.750, 1.000)
CT_LAVENDER     = (0.727, 0.473, 0.859, 1.000)
CT_PINK         = (0.898, 0.617, 0.906, 1.000)
CT_PINK2        = (1.000, 0.600, 1.000, 1.000)
CT_MAROON       = (0.711, 0.234, 0.438, 1.000)
CT_PEACH2       = (0.969, 0.691, 0.699, 1.000)
CT_RED2         = (0.863, 0.406, 0.418, 1.000)
CT_BRIGHT_RED   = (0.934, 0.266, 0.281, 1.000)

# Wood colors
CT_DARK_WOOD    = (0.690, 0.741, 0.710, 1.000)
CT_DARK_WALNUT  = (0.549, 0.412, 0.259, 1.000)
CT_GENERIC_DARK = (0.443, 0.333, 0.176, 1.000)
CT_PINE         = (1.000, 0.812, 0.490, 1.000)
CT_CHERRY       = (0.710, 0.408, 0.267, 1.000)
CT_BEECH        = (0.961, 0.659, 0.400, 1.000)

# Color tables

# To be applied to flat_wallpaper1.
CTFlatColor = [
    CT_BEIGE,
    CT_TEAL,
    CT_BLUE2,
    CT_PINK2,
    CT_BEIGE2,
    CT_RED,
    ]

CTValentinesColors = [
    CT_PINK2,
    CT_RED,
    ]

CTUnderwaterColors = [
    CT_WHITE,
    CT_TEAL,
    CT_SEA_GREEN,
    CT_LIGHT_BLUE,
    CT_PALE_GREEN,
    CT_AQUA,
    CT_CORAL,
    CT_PEACH,
    ]


# Create darkened versions of the flat colors These are useful for modlings
# and borders and such
CTFlatColorDark = []
tint = 0.75
for color in CTFlatColor:
    CTFlatColorDark.append((color[0] * tint,
                            color[1] * tint,
                            color[2] * tint,
                            1.0))

CTFlatColorAll = CTFlatColor + CTFlatColorDark

# To be applied to grayscale textures.
CTBasicWoodColorOnWhite = [
    CT_DARK_WALNUT,
    CT_GENERIC_DARK,
    CT_PINE,
    CT_CHERRY,
    CT_BEECH,
    ]

CTWhite = [CT_WHITE,]


