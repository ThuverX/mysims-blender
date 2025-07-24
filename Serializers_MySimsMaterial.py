from bpy.types import Material

from .Props_KeyProp import SetKeyProperty
from .MySimsFileSystem import *
from .Serializers_Serializer import Serializer
from .Props_MaterialProps import MySimsSingleMaterialProps
from .util import *
from .Shaders_ShaderNodes import register_shaders

PARAM_TYPE_COLOR = 1
PARAM_TYPE_INTEGER = 2
PARAM_TYPE_MAP = 4

PARAM_NAMES = {
    0x7fee2d1a: "diffuseColor",
    0x76f88689: "useLights",
    0x2616b09a: "highlightMultiplier",
    0x6cc0fd85: "diffuseMap",
    0x20cb22b7: "ambientMap",
    0xad528a60: "specularMap",
    0x2a20e51b: "alphaMap",
    0xf46b90ae: "shadowReceiver",
    0xb2649c2f: "blendmode",
    0x05d22fd3: "transparency",
    0x04a5daa3: "ambient",
    0x637daa05: "diffuse",
    0xd1f4cb96: "greenChannelMultiplier",
    0x7bb10c17: "blueChannelMultiplier",
    0x99bf82f6: "redChannelMultiplier",
    0x689aeffe: "nightTint",
    0xfbbbb5c2: "dayTint",
    0x1d17d10f: "overbrightDay",
    0xdb88ec28: "negativeColorBiasNight",
    0x29214c0c: "negativeColorBiasDay",
    0xb779f79b: "overbrightNight",
    0xbf2ad9b3: "specularColor",
    0x2ce11842: "specular",
    0x988403f9: "transparent",
    0xab26e148: "vNormalWaveSpeed",
    0xf303d152: "emissionMap",
    0xdb319586: "vReflectionWaveSpeed",
    0x3c45e334: "normalMapScale",
    0xa2e40eab: "jitterScale",
    0x02937388: "waveFrequency",
    0x50e0193b: "uReflectionWaveSpeed",
    0x2a93bafb: "waterColorBlue",
    0x5916ed3e: "baseAlpha",
    0xe460597b: "reflectionSharpness",
    0x933e38f4: "intensity",
    0x11efe2fd: "waveAmplitude",
    0x7fd42f11: "noiseFrequency",
    0xbd237b0d: "ShinyPower",
    0x2e18b549: "VspeedLayer2",
    0xdb5ebee7: "warpAmp",
    0x2e18b54b: "VspeedLayer0",
    0x2e18b54a: "VspeedLayer1",
    0x7eea0c2b: "UspeedLayer1",
    0x7eea0c2a: "UspeedLayer0",
    0x7eea0c28: "UspeedLayer2",
    0xd552a779: "reflectionIntensity",
    0xb32a1342: "reflectionAmount",
    0x9f63578d: "uNormalWaveSpeed",
    0xf72fca9b: "diffuseAlpha",
    0x7490c750: "contrastSubtractColor",
    0x6612378c: "contrastMultiplyColor",
    0x9038f94b: "amBodyShakespeare",
    0x1067900c: "amHeadHairLongSpikey",
    0x0923fb40: "auHeadHairBigFro",
    0x58b2f06d: "afBodyLayeredSkirt",
    0x80c83701: "afHeadHairFortune",
    0x75486bde: "amHeadHairSpikey",
    0x6c8c62c9: "afHeadHairTightBun",
    0x61f36b5b: "afHeadHatPirateGinny",
    0xe17e380c: "auHeadHatCap",
    0x0fdc6fdc: "faceSkinTones",
    0x9eda8cf5: "auHeadHairFlowerCrown",
    0xf0d0e420: "amHeadHatBellhop",
    0xc1519bcf: "amHeadHatMagician",
    0x8f0c0492: "auHeadHatPilotGoggles",
    0xc5ae022b: "afBodyLowPoofSkirt",
    0x383b9128: "afBodyMayor",
    0xd89ad4d5: "auHeadHatCapback",
    0x7255e7be: "afHeadHairLibrarian",
    0xe2498117: "afBodyTurtleneckBaggy",
    0xbcb6f07c: "auHeadHatBeenie",
    0xfcdf8c6a: "afHeadHairSmallBraids",
    0x359839d2: "afHeadHairPuffyLayers",
    0xde545f5e: "amHeadHairIvyLeague",
    0x146cb6b6: "afHeadHairMayor",
    0xe97a9352: "amHeadHairNigel",
    0xb4de4520: "auHeadHatNinja",
    0x7c22b02c: "auHeadHairMidShaggy",
    0x556e4212: "afBodyShortApron",
    0x8cbf470e: "afHeadHairCurlsRibbons",
    0x3b2679d5: "auBodyPantsJacketBag",
    0xd12b0c98: "afBodyShortSkirtSweater",
    0xcf76a1c7: "amHeadHairRay",
    0xe029e90d: "amHeadHairArcade",
    0xf434aa77: "afBodyHighPoofLongSkirt",
    0xea080c69: "afHeadHatBandanaDreads",
    0xc9314483: "auHeadHairFoxEars",
    0x7d6fdc4c: "afBodyCollarSkirt",
    0xc51bb766: "afBodyCoatSkirt",
    0xe806c452: "afHeadHairStylishPeacock",
    0x5f00b265: "afBodyKimono",
    0x16e4ca30: "auHeadHatTopHat",
    0xb7a93aa8: "amHeadHatChef",
    0x6515eb2c: "auBodyKnight",
    0xe9ca3e0b: "amHeadHairEthan",
    0x0a371797: "afHeadHairClara",
    0x6e2b178d: "afHeadHatWendalyn",
    0xa822b3e8: "amBodyHauntedHouseBoy",
    0xd59381fb: "auHeadHatMohawk",
    0xe72a5f1c: "auHeadHairSuperShortLayered",
    0xeb85d831: "amHeadHairTim",
    0x79a3b7ff: "auBodyHoodiePants",
    0xd01b0a09: "afBodyLongSleeveLongDress",
    0x4a351bdc: "afHeadHatCowgirl",
    0x9ed158ab: "auHeadHatBald",
    0xd9dfb575: "amBodyMartialArts",
    0xe2b571a9: "propBookClosed",
    0xe1a22a57: "amBodyFlipper",
    0x66ba9c80: "afBodyLongSkirtLargeCuff",
    0xe4f0d787: "auHeadHatPirate",
    0x26f07855: "auHeadHairShortFlatBangs",
    0x2836ea65: "auBodyBellhop",
    0xc800d94b: "auBodyApronBear",
    0xdd91b6b6: "afBodyKneeLengthSkirt",
    0x8d58d24f: "auHeadHatRasta",
    0x32e0ca0b: "afBodyLongSkirt",
    0x23c6d774: "auBodySkinTight",
    0x7bebdd19: "auBodyCalfLengthPants",
    0xeddcece1: "plumbobColor",
    0x455bef77: "afHeadHairDoubleBuns",
    0xc36d202b: "auHeadHairHairspraySpikey",
    0xafc8f11b: "afHeadHairRaveKimono",
    0x40a202a7: "auHeadHairBowlCut",
    0xad6d2254: "amHeadHairCruise",
    0x57059004: "auBodyLongPantsBoots",
    0x791597ca: "afHeadHatNewspaperCap",
    0x5519cfb6: "afHeadHatBandana",
    0x811f207f: "afHeadHairAlexa",
    0x37c3b76c: "afHeadHairStreakedLolita",
    0xf8404ffa: "afHeadHairPuffyLayersBunny",
    0xbe323f01: "auBodyApronTshirtPants",
    0xc34a68d0: "auBodyLongPantsShortSleeves",
    0xbcf4239b: "amBodyArcade",
    0xb3f9d3f1: "afBodyAlexa",
    0xcb6a2c62: "afBodyAsymmetricalSkirt",
    0x88b04723: "auHeadHatCadet",
    0x8157dc19: "auBodyBear",
    0x4e053dbd: "auHeadHairDisco",
    0xaf284852: "afBodyShortSleeveApron",
    0x8804b9b4: "auBodyRolledSleevesLongPants",
    0x4487e3d4: "afHeadHairPigTail",
    0xebbb243f: "afHeadHairLooseCurlsLong",
    0xbbf23c58: "afHeadHairLong",
    0xb9642ff0: "afHeadHairPigTailFlowers",
    0xaa3cd006: "afHeadHairLongBraid",
    0x804ad79a: "afHeadHairLongPigtail",
    0x608caa94: "afHeadHatBeaniePigtails",
    0xc3dd71da: "afBodyChineseDress",
    0xd987c7ad: "amHeadHatCowboy",
    0x667d4e9c: "afBodyFloristYoungerSister",
    0x1688f273: "auHeadHatEarhat",
    0x4038b561: "afHeadHairHighSalon",
    0xb857a450: "afHeadHairSoftBobBangs",
    0x16229f12: "afHeadHairKarine",
    0xe808f034: "amBodyGothCoat",
    0xebb1363d: "afHeadHairBangsHighPonyTail",
    0x10b11928: "amHeadHatMartialArts",
    0x31b41a58: "auHeadHairShortFro",
    0x32ff6934: "afBodyWendalyn",
    0x172754f2: "amHeadHatShakespeare",
    0x4cf48f41: "auBodyBackpack",
    0x5e5e0bb5: "auHeadHairLongLayered",
    0xdb272b16: "afHeadHairBee",
    0x0562a36e: "amHeadHairSlickBack",
    0xadf12cdc: "afHeadHatFedoraHeadset",
    0x206508d6: "auBodySuitBowTie",
    0x21eaeac7: "amHeadHatNewspaperCap",
    0x0568e523: "auBodyNoSleevesLongPants",
    0x4c34687c: "amHeadHairPompadour",
    0x1f8c55e8: "auBodyPirate",
    0x6293ca92: "auBodyShortPantsShortSleeves",
    0x57cffd77: "amBodyChef",
    0x9e77273b: "afBodyShortSkirtBag",
    0x407405f3: "afHeadHairPuffyLayersTiara",
    0x61ab1e17: "amHeadHairSidePart",
    0x69e3e1a7: "amBodySamurai",
    0xf67d2839: "amHeadHairShort",
    0x68592352: "amHeadHatFlipper",
    0x1437614b: "afBodyFortuneTeller",
    0xa8ec7cf0: "auBodyShortSleevApronPants",
    0x7fd2fd6d: "auHeadHatVisor",
    0x94f2a3f5: "auHeadHairMuseum",
    0xab532e19: "amHeadHatBuzzCut",
    0xeae93c5d: "auBodyShortJacketClosed",
    0x115e90e5: "afBodyHighPoofSkirt",
    0xa66e30f0: "auHeadHatHippieBandana",
    0xe042258b: "afBodySmallWings",
    0x6c25c854: "afHeadHairStylish",
    0x30872f06: "afHeadHairLayeredBangsMedium",
    0x6a7c3efc: "afHeadHatCrumplebottom",
    0x0a0bf0f7: "amHeadHatFedora",
    0x5c211319: "auHeadHairDandelion",
    0x1514f851: "auBodyNinja",
    0x018261bd: "auHeadHairSushi",
    0x2a45864c: "afHeadHairLongLayered",
    0x22df72ce: "afHeadHairLongPonytail",
    0x5a0c9575: "auHeadHairVeryShortSpiky",
    0x8d6f69f2: "afHeadHairObservatory",
    0x8637df43: "auBodyBulkySweaterLongPants",
    0x5fc9d348: "auHeadHairShortCurly",
    0x86769daf: "auBodyLongPantsLongSleeve",
    0x2344a259: "amHeadHairScientist",
    0x79dbab9e: "auHeadHatBear",
    0x1f0050d9: "amHeadHatCombOver",
    0x04985945: "afBodyMini",
    0x37a80fc1: "afHeadHairUpdoRibbons",
    0x3d88b8b3: "amHeadHatBaker",
    0xbcc02d91: "auBodyLabCoat",
    0x0a345310: "envmapAlpha",
    0x4a1a7937: "door_archedTopBar"
}

def get_param_name(param_name: str):
    if int(param_name, 16) in PARAM_NAMES:
        return PARAM_NAMES[int(param_name, 16)]
    return param_name

class MySimsMaterialParam(Serializer):

    color: tuple[float, float, float, float]
    integer: int
    map: ResourceKey

    def read(self, buf: BufferedReader, offset: int):
        self.name = uint32_t(buf)
        self.type = uint32_t(buf)
        field_count = uint32_t(buf)
        value_offset = uint32_t(buf)

        jump = buf.tell()

        buf.seek(offset + value_offset)

        if self.type == PARAM_TYPE_COLOR:
            if field_count == 1:
                value = float32_t(buf)
                self.color = (value, value, value, value)
            if field_count == 2:
                self.color = (float32_t(buf), float32_t(buf), 0, 0)
            if field_count == 3:
                self.color = (float32_t(buf), float32_t(buf), float32_t(buf), 0)
            if field_count == 4:
                self.color = (float32_t(buf), float32_t(buf), float32_t(buf), float32_t(buf))
        elif self.type == PARAM_TYPE_INTEGER:
            self.integer = uint32_t(buf)
        elif self.type == PARAM_TYPE_MAP:
            self.map = ResourceKey()
            self.map.read(buf)

        buf.seek(jump)

    def write(self, buf: BufferedWriter):
        pass

    #
    # if alpha_texture:
    #     alpha_tex_image = nodes.new(type="ShaderNodeTexImage")
    #     alpha_tex_image.image = bpy.data.images.load(alpha_texture)
    #
    # # Output and shaders
    # diffuse_shader = nodes.new(type="ShaderNodeBsdfDiffuse")
    # mix_shader = nodes.new(type="ShaderNodeMixShader")
    # transparent_shader = nodes.new(type="ShaderNodeBsdfTransparent")
    #
    # # Tint (Multiply) node
    #     # Create a "MixRGB" node to apply the tint
    #     tint_node = nodes.new(type="ShaderNodeMixRGB")
    #     tint_node.blend_type = 'MULTIPLY'
    #     tint_node.inputs['Fac'].default_value = 1.0  # Full multiply
    #     tint_node.inputs['Color2'].default_value = (
    #         diffuse_color[0],
    #         diffuse_color[1],
    #         diffuse_color[2],
    #         1.0  # Alpha (keep 1.0 for color multiplication)
    #     )
    #     # Link texture -> tint -> diffuse color
    #     links.new(tex_image.outputs["Color"], tint_node.inputs["Color1"])
    #     links.new(tint_node.outputs["Color"], diffuse_shader.inputs["Color"])
    # else:
    #     # No tint, link texture directly
    #     links.new(tex_image.outputs["Color"], diffuse_shader.inputs["Color"])
    #
    # # Alpha handling
    # if alpha_texture:
    #     links.new(alpha_tex_image.outputs["Alpha"], mix_shader.inputs["Fac"])
    # else:
    #     mix_shader.inputs["Fac"].default_value = 1.0
    #     if "alpha_tex_image" in locals():
    #         nodes.remove(alpha_tex_image)
    #
    # # Connect the shaders
    # links.new(diffuse_shader.outputs["BSDF"], mix_shader.inputs[2])
    # links.new(transparent_shader.outputs["BSDF"], mix_shader.inputs[1])
    # links.new(mix_shader.outputs["Shader"], material_output.inputs["Surface"])

class MySimsMaterial(Serializer):
    key: ResourceKey
    params: list[MySimsMaterialParam]

    def __init__(self, key: ResourceKey | None = None):
        if key:
            self.key = key

    def read(self, buf: BufferedReader):
        start_read()
        print("Loading material " + str(self.key))
        start = buf.tell()

        isKingdom = string(buf, 4) == "MATD"
        buf.seek(start)

        mtrl_offset = 0

        if not isKingdom:
            # MySims Format

            uint32_t(buf)
            uint32_t(buf)
            uint32_t(buf)
            uint32_t(buf)
            uint32_t(buf)

            self.key = ResourceKey()
            self.key.read(buf)

            header_size = uint32_t(buf)
            total_size = uint32_t(buf)
            
            string(buf, 4) # MATD
            uint32_t(buf)

            self.name = uint32_t(buf)
            self.shader = uint32_t(buf)

            mtrl_size = uint32_t(buf)
            mtrl_offset = buf.tell()
        else:
            string(buf, 4) # MATD
            uint32_t(buf)

            self.shader = uint32_t(buf)
            mtrl_size = uint32_t(buf)
            mtrl_offset = buf.tell()
            set_endianness(buf,"be")

        string(buf, 4) # MTRL
        uint32_t(buf)

        data_size = uint32_t(buf)
        num_params = uint32_t(buf)

        self.params = []

        for i in range(num_params):
            param = MySimsMaterialParam()
            param.read(buf, mtrl_offset)
            self.params.append(param)
        
        set_endianness(buf,"le")

        print("Done loading material")


    def write(self, buf: BufferedWriter):
        start_write()


    def to_node(self, material: MySimsSingleMaterialProps, parent_key = None):

        material.shader_type =  f"0x{self.shader:08X}"
        SetKeyProperty(material, 'key', self.key)
        if parent_key:
            SetKeyProperty(material, 'parent', parent_key)

        for param in self.params:
            param_prop = material.params.add()
            param_prop.name = f"0x{param.name:08X}"

            if param.type == PARAM_TYPE_MAP:
                param_prop.type = "map"
                SetKeyProperty(param_prop, 'map', str(param.map))
            elif param.type == PARAM_TYPE_COLOR:
                param_prop.type = "color"
                param_prop.color = param.color
            elif param.type == PARAM_TYPE_INTEGER:
                param_prop.type = "integer"
                param_prop.integer = param.integer

    @classmethod
    def get(cls, key: ResourceKey):
        path = MS_FILE_SYSTEM.get(key)
        if not path:
            return None
        
        if key.type == 0x01d0e75d:
            with open(path, 'rb') as file:
                mat = MySimsMaterial(key)
                mat.read(file)

                return mat
        elif key.type == 0x02019972:
            with open(path, 'rb') as file:
                mat = MySimsMaterialSet()
                mat.read(file)

                return mat
            
        return None

class MySimsMaterialSet(Serializer):
    key: ResourceKey
    materials: list[MySimsMaterial]

    blender_materials: list

    def read(self, buf: BufferedReader):
        start_read()
        start = buf.tell()

        isKingdom = string(buf, 4) == "MTST"
        buf.seek(start)

        if not isKingdom:
            uint32_t(buf)
            uint32_t(buf)
            uint32_t(buf)

            material_count = uint32_t(buf)
            uint32_t(buf)

            self.key = ResourceKey()
            self.key.read(buf)
            self.materials = []

            for i in range(material_count):
                mat_ref = ResourceKey()
                mat_ref.read(buf)
                path = MS_FILE_SYSTEM.get(mat_ref)
                if path:
                    with open(path, 'rb') as file:
                        mat = MySimsMaterial(mat_ref)
                        mat.read(file)
                        self.materials.append(mat)

            header_size = uint32_t(buf)
            mtst_size = uint32_t(buf)

            mtst_magic = string(buf, 4)

            mtst_version = uint32_t(buf)
            mtst_name = uint32_t(buf)
            mtst_start_index = uint32_t(buf)
            mtst_index_count = uint32_t(buf)

            self.indicies = []

            for i in range(mtst_index_count):
                self.indicies.append(uint32_t(buf))
        else:
            mtst_magic = string(buf, 4)
            uint32_t(buf)
            uint32_t(buf)
            material_count = uint32_t(buf)
            self.materials = []

            for i in range(material_count):
                instance = uint64_t(buf)
                mat_ref = ResourceKey(instance, 0x01d0e75d, 0)
                path = MS_FILE_SYSTEM.get(mat_ref)
                if path:
                    with open(path, 'rb') as file:
                        mat = MySimsMaterial(mat_ref)
                        mat.read(file)
                        self.materials.append(mat)

    def write(self, buf: BufferedWriter):
        start_write()

    def to_node(self, material_list, parent_key):
        for mat in self.materials:
            prop = material_list.add()
            mat.to_node(prop, parent_key)
