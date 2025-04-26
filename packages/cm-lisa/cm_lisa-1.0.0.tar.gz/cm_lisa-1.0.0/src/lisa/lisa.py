from __future__ import annotations

from matplotlib import colormaps
from matplotlib.colors import LinearSegmentedColormap

# Converted from https://github.com/tylerlittlefield/lisa/blob/master/inst/extdata/palettes.yml
_palettes = {
    "Albers"         : ( '#D77186', '#61A2DA', '#6CB7DA', '#b5b5b3', '#D75725' ),
    "Albers_1"       : ( '#C00559', '#DE1F6C', '#F3A20D', '#F07A13', '#DE6716' ),
    "Albrecht"       : ( '#171635', '#00225D', '#763262', '#CA7508', '#E9A621' ),
    "Apple"          : ( '#F24D98', '#813B7C', '#59D044', '#F3A002', '#F2F44D' ),
    "Arnoldi"        : ( '#C2151B', '#2021A0', '#3547B3', '#E2C43F', '#E0DCDD' ),
    "Avery"          : ( '#F3C937', '#7B533E', '#BFA588', '#604847', '#552723' ),
    "Avery_1"        : ( '#E2CACD', '#2E7CA8', '#F1C061', '#DA7338', '#741D13' ),
    "Klint"          : ( '#D6CFC4', '#466CA6', '#D1AE45', '#87240E', '#040204' ),
    "Basquiat"       : ( '#8CABD9', '#F6A7B8', '#F1EC7A', '#1D4D9F', '#F08838' ),
    "Basquiat_1"     : ( '#C11432', '#009ADA', '#66A64F', '#FDD10A', '#070707' ),
    "Beckmann"       : ( '#4B3A51', '#A77A4B', '#ECC6A2', '#A43020', '#722D24' ),
    "Botero"         : ( '#99B6BD', '#B3A86A', '#ECC9A0', '#D4613E', '#BB9568' ),
    "Botticelli"     : ( '#7A989A', '#849271', '#C1AE8D', '#CF9546', '#C67052' ),
    "Botticelli_1"   : ( '#272725', '#DDBD85', '#DA694F', '#A54A48', '#FDFFE5' ),
    "Bruegel"        : ( '#BFBED5', '#7F9086', '#A29A68', '#676A4F', '#A63C24' ),
    "Bush"           : ( '#529DCB', '#ECA063', '#71BF50', '#F3CC4F', '#D46934' ),
    "Bush_1"         : ( '#A1D8B6', '#D2C48E', '#F45F40', '#F9AE8D', '#80B9CE' ),
    "Cassatt"        : ( '#1C5679', '#BBB592', '#CAC3B2', '#808C5C', '#5F4B3B' ),
    "Cezanne"        : ( '#8399B3', '#697A55', '#C4AA88', '#B68E52', '#8C5B28' ),
    "Chagall"        : ( '#3F6F76', '#69B7CE', '#C65840', '#F4CE4B', '#62496F' ),
    "Coolidge"       : ( '#204035', '#4A7169', '#BEB59C', '#735231', '#49271B' ),
    "Dali"           : ( '#40798C', '#bca455', '#bfb37f', '#805730', '#514A2E' ),
    "Dali_1"         : ( '#9BC0CC', '#CAD8D8', '#D0CE9F', '#806641', '#534832' ),
    "daVinci"        : ( '#C8B272', '#a88b4c', '#a0a584', '#697153', '#43362a' ),
    "Davis"          : ( '#293757', '#568D4B', '#D5BB56', '#D26A1B', '#A41D1A' ),
    "deChirico"      : ( '#27403D', '#48725C', '#212412', '#F3E4C2', '#D88F2E' ),
    "deChirico_1"    : ( '#2992BF', '#4CBED9', '#292C17', '#F9F6EF', '#F0742A' ),
    "Degas"          : ( '#BDB592', '#ACBBC5', '#9E8D3D', '#8C4F36', '#2C2D2C' ),
    "Delaunay"       : ( '#4368B6', '#78A153', '#DEC23B', '#E4930A', '#C53211' ),
    "Delaunay_1"     : ( '#A4B7E1', '#B8B87A', '#EFDE80', '#EFBD37', '#A85E5E' ),
    "Demuth"         : ( '#e4af79', '#df9c41', '#af7231', '#923621', '#2D2A28' ),
    "Diebenkorn"     : ( '#2677A5', '#639BC1', '#639BC1', '#90A74A', '#5D8722' ),
    "Dix"            : ( '#1E1D20', '#B66636', '#547A56', '#BDAE5B', '#515A7C' ),
    "Dix_1"          : ( '#E0DBC8', '#C9BE90', '#76684B', '#CDAB7E', '#3C2B23' ),
    "Duchamp"        : ( '#d0cec2', '#7baa80', '#4b6b5e', '#bf9a41', '#980019' ),
    "Durer"          : ( '#657359', '#9AA582', '#8B775F', '#D7C9BE', '#F1E4DB' ),
    "Ernst"          : ( '#91323A', '#3A4960', '#D7C969', '#6D7345', '#554540' ),
    "Escher"         : ( '#C1395E', '#AEC17B', '#F0CA50', '#E07B42', '#89A7C2' ),
    "Feeley"         : ( '#2C458D', '#E4DFD9', '#425B4F', '#EBAD30', '#BF2124' ),
    "Feitelson"      : ( '#202221', '#661E2A', '#AB381B', '#EAD4A3', '#E3DED8' ),
    "Frankenthaler"  : ( '#5D7342', '#D7AE04', '#ECD7B8', '#A58B8C', '#272727' ),
    "Freud"          : ( '#e1d2bd', '#a77e5e', '#2d291d', '#85868b', '#83774d' ),
    "Frost"          : ( '#EF5950', '#8D5A78', '#C66F26', '#FB6B22', '#DC2227' ),
    "Gauguin"        : ( '#21344F', '#8AAD05', '#E2CE1B', '#DF5D22', '#E17976' ),
    "Geiger"         : ( '#FF62A9', '#F77177', '#FA9849', '#FE6E3A', '#FD5A35' ),
    "Hofmann"        : ( '#1A6DED', '#2C7CE6', '#145CBF', '#162B3D', '#F9ECE4' ),
    "Hokusai"        : ( '#1F284C', '#2D4472', '#6E6352', '#D9CCAC', '#ECE2C6' ),
    "Homer"          : ( '#A9944A', '#F2D9B3', '#725435', '#8E9DBF', '#BD483C' ),
    "Hopper"         : ( '#67161C', '#3F6148', '#DBD3A4', '#A4804C', '#4B5F80' ),
    "Indiana"        : ( '#2659D8', '#1C6FF3', '#5EBC4E', '#53A946', '#F24534' ),
    "Jean"           : ( '#51394E', '#F6DE7D', '#C8AF8A', '#658385', '#B04838' ),
    "Johns"          : ( '#4B6892', '#F9E583', '#FED43F', '#F6BD28', '#BE4C46' ),
    "Kahlo"          : ( '#121510', '#6D8325', '#D6CFB7', '#E5AD4F', '#BD5630' ),
    "Kandinsky"      : ( '#5D7388', '#A08F27', '#E5A729', '#4F4D1D', '#8AAE8A' ),
    "Kandinsky_1"    : ( '#d2981a', '#a53e1f', '#457277', '#8dcee2', '#8f657d' ),
    "Kandinsky_2"    : ( '#C13C53', '#DA73A8', '#4052BD', '#EFE96D', '#D85143' ),
    "Klee"           : ( '#A7B3CD', '#E6DA9E', '#676155', '#CDB296', '#CCD7AD' ),
    "Klee_1"         : ( '#4F51FE', '#8C1E92', '#FF4E0B', '#CD2019', '#441C21' ),
    "Klein"          : ( '#344CB9', '#1B288A', '#0F185B', '#D7C99A', '#F2E4C7' ),
    "Klimt"          : ( '#4A5FAB', '#609F5C', '#E3C454', '#A27CBA', '#B85031' ),
    "Koons"          : ( '#D6AABE', '#B69F7F', '#ECD9AD', '#76A9A2', '#A26775' ),
    "Krasner"        : ( '#333333', '#D1B817', '#2A2996', '#B34325', '#C8CCC6' ),
    "Lawrence"       : ( '#614671', '#BE994A', '#C8B595', '#BD4335', '#8B3834' ),
    "Lawrence_1"     : ( '#5E3194', '#9870B9', '#F1B02F', '#EA454C', '#CC0115' ),
    "LeWitt"         : ( '#0A71B6', '#F9C40A', '#190506', '#EB5432', '#EAF2F0' ),
    "Lichtenstein"   : ( '#3229ad', '#bc000e', '#e7cfb7', '#ffec04', '#090109' ),
    "Lichtenstein_1" : ( '#00020E', '#FFDE01', '#A5BAD6', '#F1C9C7', '#BD0304' ),
    "Lichtenstein_2" : ( '#c7991f', '#c63d33', '#23254c', '#e0c4ae', '#d5d0b2' ),
    "Malevich"       : ( '#151817', '#001A56', '#197C3F', '#D4A821', '#C74C25' ),
    "Manet"          : ( '#6486AD', '#2D345D', '#D9BE7F', '#5A3A26', '#C6A490' ),
    "Magritte"       : ( '#B60614', '#3A282F', '#909018', '#E3BFA1', '#EE833E' ),
    "Magritte_1"     : ( '#B6B3BB', '#697D8E', '#B8B87E', '#6F5F4B', '#292A2D' ),
    "Masaccio"       : ( '#0e2523', '#324028', '#c26b61', '#5a788d', '#de7944' ),
    "Michelangelo"   : ( '#42819F', '#86AA7D', '#CBB396', '#555234', '#4D280F' ),
    "Miro"           : ( '#C04759', '#3B6C73', '#383431', '#F1D87F', '#EDE5D2' ),
    "Modigliani"     : ( '#1d2025', '#45312a', '#7e2f28', '#202938', '#d58e40' ),
    "Mondrian"       : ( '#314290', '#4A71C0', '#F1F2ED', '#F0D32D', '#AB3A2C' ),
    "Monet"          : ( '#184430', '#548150', '#DEB738', '#734321', '#852419' ),
    "Monet_1"        : ( '#9F4640', '#4885A4', '#395A92', '#7EA860', '#B985BA' ),
    "Monet_2"        : ( '#82A4BC', '#4C7899', '#2F5136', '#B1B94C', '#E5DCBE' ),
    "Munch"          : ( '#5059A1', '#EFC337', '#1F386E', '#D1AE82', '#BE3B2C' ),
    "Munch_1"        : ( '#272A2A', '#E69253', '#EDB931', '#E4502E', '#4378A0' ),
    "Newman"         : ( '#442327', '#C0BC98', '#A6885D', '#8A3230', '#973B2B' ),
    "Noland"         : ( '#D0D8CD', '#586180', '#E2AC29', '#1A1915', '#E6E1CE' ),
    "O'Keeffe"       : ( '#0E122D', '#182044', '#51628E', '#91A1BA', '#AFD0C9' ),
    "Oldenburg"      : ( '#95B1C9', '#263656', '#698946', '#F8D440', '#C82720' ),
    "Picasso"        : ( '#CD6C74', '#566C7D', '#DD9D91', '#A1544B', '#D5898D' ),
    "Picasso_1"      : ( '#4E7989', '#A9011B', '#E4A826', '#80944E', '#DCD6B2' ),
    "Pollock"        : ( '#D89CA9', '#1962A0', '#F1ECD7', '#E8C051', '#1A1C23' ),
    "Prince"         : ( '#735bcc', '#6650b4', '#59449c', '#4b3984', '#3e2d6c' ),
    "Quidor"         : ( '#B79A59', '#826C37', '#54442F', '#DBCEAF', '#C4AA52' ),
    "Ramos"          : ( '#C13E43', '#376EA5', '#565654', '#F9D502', '#E7CA6B' ),
    "Redon"          : ( '#695B8F', '#B26C61', '#C2AF46', '#4D5E30', '#8B1F1D' ),
    "Rembrandt"      : ( '#DBC99A', '#A68329', '#5B5224', '#8A350C', '#090A04' ),
    "Renoir"         : ( '#2B5275', '#A69F55', '#F1D395', '#FFFBDD', '#D16647' ),
    "Renoir_1"       : ( '#303241', '#B7A067', '#C8C2B2', '#686D4F', '#4D3930' ),
    "Riley"          : ( '#FAB9AC', '#7BBC53', '#DE6736', '#67C1EC', '#E6B90D' ),
    "Rosenquist"     : ( '#E25D75', '#3F4C8C', '#6A79B0', '#D7BC1F', '#DCCFAB' ),
    "Rothko"         : ( '#E49A16', '#E19713', '#D67629', '#DA6E2E', '#D85434' ),
    "Rothko_1"       : ( '#D5D6D1', '#BEC0BF', '#5B382C', '#39352C', '#1B1B1B' ),
    "SingerSargent"  : ( '#b43a35', '#3e501e', '#f8f2f4', '#6b381d', '#20242d' ),
    "SingerSargent_1": ( '#778BD0', '#E2D76B', '#95BF78', '#4E6A3D', '#5F4F38' ),
    "SingerSargent_2": ( '#EEC7A0', '#EAA69C', '#BD7C96', '#A1A481', '#D97669' ),
    "Schlemmer"      : ( '#3A488A', '#8785B2', '#DABD61', '#D95F30', '#BE3428' ),
    "Seurat"         : ( '#3F3F63', '#808EB7', '#465946', '#8C9355', '#925E48' ),
    "Skoglund"       : ( '#d7f96e', '#457d24', '#879387', '#e1c39f', '#394835' ),
    "Tchelitchew"    : ( '#ac2527', '#f8cc5a', '#5c8447', '#61221a', '#2b4868' ),
    "Turner"         : ( '#F1ECCE', '#9EA3B5', '#E9D688', '#A85835', '#AE8045' ),
    "Twombly"        : ( '#F2788F', '#F591EA', '#F0C333', '#F5C2AF', '#F23B3F' ),
    "JacobUlrich"    : ( '#FDDDAB', '#E7A974', '#A87250', '#7B533D', '#6A4531' ),
    "Doesburg"       : ( '#BD748F', '#3D578E', '#BFAB68', '#DAD7D0', '#272928' ),
    "Doesburg_1"     : ( '#53628D', '#B8B45B', '#C1C3B6', '#984F48', '#2E3432' ),
    "vanEyck"        : ( '#3C490C', '#3B5B71', '#262121', '#7C6C4E', '#6C2B23' ),
    "vanGogh"        : ( '#1a3431', '#2b41a7', '#6283c8', '#ccc776', '#c7ad24' ),
    "vanGogh_1"      : ( '#FBDC30', '#A7A651', '#E0BA7A', '#9BA7B0', '#5A5F80' ),
    "vanGogh_2"      : ( '#374D8D', '#93A0CB', '#82A866', '#C4B743', '#A35029' ),
    "Varo"           : ( '#C8DAAD', '#989E53', '#738D60', '#DEBC31', '#9D471A' ),
    "Velazquez"      : ( '#413A2C', '#241F1A', '#C5B49B', '#A57F5B', '#5C351E' ),
    "Vermeer"        : ( '#0C0B10', '#707DA6', '#CCAD9D', '#B08E4A', '#863B34' ),
    "Vermeer_1"      : ( '#022F69', '#D6C17A', '#D8D0BE', '#6B724B', '#7C3E2F' ),
    "Warhol"         : ( '#F26386', '#F588AF', '#A4D984', '#FCBC52', '#FD814E' ),
    "Warhol_1"       : ( '#FD0C81', '#FFED4D', '#C34582', '#EBA49E', '#272324' ),
    "Warhol_2"       : ( '#D32934', '#2F191B', '#2BAA92', '#D12E6C', '#F4BCB9' ),
    "Warhol_3"       : ( '#a99364', '#da95aa', '#f4f0e4', '#b74954', '#c2ddb2' ),
    "Wood"           : ( '#A6BDB0', '#8B842F', '#41240B', '#9C4823', '#D6AA7E' ),
    "Xanto"          : ( '#2C6AA5', '#D9AE2C', '#DDC655', '#D88C27', '#64894D' ),
    "Youngerman"     : ( '#59A55D', '#EFDB56', '#7D9DC6', '#ECA23F', '#CA4D2A' ),
    "Zerbe"          : ( '#46734F', '#CAAB6C', '#D0CCAF', '#617F97', '#9A352D' ),
}

def get_cmap(name: str) -> LinearSegmentedColormap:
    """
    Get a colormap by name.

    Parameters
    ----------
    name : str
        The name of the colormap to get.

    Returns
    -------
    matplotlib.colors.LinearSegmentedColormap
        The colormap.
    """

    reverse = name.endswith("_r")
    if reverse:
        key = name[:-2]
    else:
        key = name

    if key not in _palettes:
        raise ValueError(f"Key {key} not found in lisa.")

    colors = _palettes[key]
    if reverse:
        colors = colors[::-1]

    return LinearSegmentedColormap.from_list(name, colors)

def _register_all():
    """
    Register all colormaps with matplotlib.
    """
    for name, colors in _palettes.items():
        for suffix in ("", "_r"):
            colormaps.register(get_cmap(name+suffix))

def list_cmaps():
    """
    List all available colormaps.

    Returns
    -------
    list
        A list of colormap names.
    """
    return list(_palettes.keys())
