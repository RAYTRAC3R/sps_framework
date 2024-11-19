import pygame

import ujson

from scripts.game_structure.game_essentials import game

class Sprites():
    cat_tints = {}
    white_patches_tints = {}

    def __init__(self, size=None):
        """Class that handles and hold all spritesheets. 
        Size is normall automatically determined by the size
        of the lineart. If a size is passed, it will override 
        this value. """
        self.size = None
        self.spritesheets = {}
        self.images = {}
        self.sprites = {}

        # Shared empty sprite for placeholders
        self.blank_sprite = None
        
        self.load_tints()

    def load_tints(self):
        try:
            with open("sprites/dicts/tint.json", 'r') as read_file:
                self.cat_tints = ujson.loads(read_file.read())
        except:
            print("ERROR: Reading Base Tints")

        try:
            with open("sprites/dicts/white_patches_tint.json", 'r') as read_file:
                self.white_patches_tints = ujson.loads(read_file.read())
        except:
            print("ERROR: Reading White Patches Tints")
            
        try:
            with open("sprites/dicts/marking_tint.json", 'r') as read_file:
                self.markings_tints = ujson.loads(read_file.read())
        except:
            print("ERROR: Reading Marking Tints")

        try:
            with open("sprites/dicts/marking_tint.json", 'r') as read_file:
                self.markings_tints = ujson.loads(read_file.read())
        except:
            print("ERROR: Reading Marking Tints")

        try:
            with open("sprites/dicts/eye_tint.json", 'r') as read_file:
                self.eye_tints = ujson.loads(read_file.read())
        except:
            print("ERROR: Reading Eye Tints")

        try:
            with open("sprites/dicts/accessories_tint.json", 'r') as read_file:
                self.accessory_tints = ujson.loads(read_file.read())
        except:
            print("ERROR: Reading Accessory Tints")

        self.eye_random = self.eye_tints["enable_random"]
            
    def spritesheet(self, a_file, name):
        """
        Add spritesheet called name from a_file.

        Parameters:
        a_file -- Path to the file to create a spritesheet from.
        name -- Name to call the new spritesheet.
        """
        self.spritesheets[name] = pygame.image.load(a_file).convert_alpha()

    def make_group(self,
                   spritesheet,
                   pos,
                   name,
                   sprites_x=3,
                   sprites_y=7):  # pos = ex. (2, 3), no single pixels
        """
        Divide sprites on a sprite-sheet into groups of sprites that are easily accessible.

        Parameters:
        spritesheet -- Name of spritesheet.
        pos -- (x,y) tuple of offsets. NOT pixel offset, but offset of other sprites.
        name -- Name of group to make.
        
        Keyword Arguments
        sprites_x -- Number of sprites horizontally (default: 3)
        sprites_y -- Number of sprites vertically (default: 3)
        """

        group_x_ofs = pos[0] * sprites_x * self.size
        group_y_ofs = pos[1] * sprites_y * self.size
        i = 0

        # splitting group into singular sprites and storing into self.sprites section
        for y in range(sprites_y):
            for x in range(sprites_x):
                try:
                    new_sprite = pygame.Surface.subsurface(
                        self.spritesheets[spritesheet],
                        group_x_ofs + x * self.size,
                        group_y_ofs + y * self.size,
                        self.size, self.size
                    )
                except ValueError:
                    # Fallback for non-existent sprites
                    if not self.blank_sprite:
                        self.blank_sprite = pygame.Surface(
                            (self.size, self.size),
                            pygame.HWSURFACE | pygame.SRCALPHA
                        )
                    new_sprite = self.blank_sprite
                self.sprites[f'{name}{i}'] = new_sprite
                i += 1

    def load_all(self):
        # get the width and height of the spritesheet
        lineart = pygame.image.load('sprites/lineart.png')
        width, height = lineart.get_size()
        del lineart # unneeded

        # if anyone changes lineart for whatever reason update this
        if isinstance(self.size, int):
            pass
        elif width / 3 == height / 7:
            self.size = width / 3
        else:
            self.size = 50 # default, what base clangen uses
            print(f"lineart.png is not 3x7, falling back to {self.size}")
            print(f"if you are a modder, please update scripts/cat/sprites.py and "
                  f"do a search for 'if width / 3 == height / 7:'")

        del width, height  # unneeded

        # load sprite sheets for all folders
        for f in game.sprite_folders:
            for x in [
                'lineart', 'base', 'overlays/underfur', 'overlays/overfur', 'markings/markings', 'eyes/eyes',
                'whitepatches', 'skin', 'scars', 'missingscars',
                'accessories/accessories', 'accessories/patterns', 'accessories/herbaccessories', 'accessories/wildaccessories',
                'shadersnewwhite', 'lineartdead', 'tortiepatchesmasks', 
                'medcatherbs', 'lineartdf', 'lightingnew', 'fademask',
                'fadestarclan', 'fadedarkforest',
                'symbols'
            ]:
                if 'lineart' in x and game.config['fun']['april_fools']:
                    self.spritesheet(f"sprites/{f}/aprilfools{x}.png", x)
                elif 'symbols' in x:
                    self.spritesheet(f"sprites/{x}.png", x)
                else:
                    self.spritesheet(f"sprites/{f}/{x}.png", x)

            # Line art
            self.make_group('lineart', (0, 0), f'lines{f}_')
            self.make_group('shadersnewwhite', (0, 0), f'shaders{f}_')
            self.make_group('lightingnew', (0, 0), f'lighting{f}_')

            self.make_group('lineartdead', (0, 0), f'lineartdead{f}_')
            self.make_group('lineartdf', (0, 0), f'lineartdf{f}_')
            
            # Base Color
            self.make_group('base', (0, 0), f'base{f}_')
            # Markings
            for a, i in enumerate(['Tabby', 'Masked', 'Mackerel', 'Agouti', 'Speckled', 'Classic', 'Wisp', 'Sokoke', 'Singlestripe', 'Ticked', 'Marbled', 'Bengal', 'Smoke', 'Rosette']):
                self.make_group('markings/markings', (a, 0), f'mark{f}_{i}')
            # Overlays
            for a, i in enumerate(['strong', 'medium', 'bubble', 'ash']):
                self.make_group('overlays/underfur', (a, 0), f'underfur{f}_{i}')
            for a, i in enumerate(['strong', 'medium', 'smoke', 'bubble', 'overcast', 'ash']):
                self.make_group('overlays/overfur', (a, 0), f'overfur{f}_{i}')

            # Fading Fog
            for i in range(0, 3):
                self.make_group('fademask', (i, 0), f'fademask{f}_{i}')
                self.make_group('fadestarclan', (i, 0), f'fadestarclan{f}_{i}')
                self.make_group('fadedarkforest', (i, 0), f'fadedf{f}_{i}')

            for a, i in enumerate(['base', 'shade', 'pupil']):
            self.make_group('eyes/eyes', (a, 0), f'eyes{i}')
        for a, i in enumerate(['base', 'shade', 'pupil']):
            self.make_group('eyes/eyes', (a, 1), f'eyes2{i}')

            # Define white patches
            white_patches = [
                ['FULLWHITE', 'ANY', 'TUXEDO', 'LITTLE', 'COLOURPOINT', 'VAN', 'ANYTWO', 'MOON', 'PHANTOM', 'POWDER',
                 'BLEACHED', 'SAVANNAH', 'FADESPOTS', 'PEBBLESHINE'],
                ['EXTRA', 'ONEEAR', 'BROKEN', 'LIGHTTUXEDO', 'BUZZARDFANG', 'RAGDOLL', 'LIGHTSONG', 'VITILIGO', 'BLACKSTAR',
                 'PIEBALD', 'CURVED', 'PETAL', 'SHIBAINU', 'OWL'],
                ['TIP', 'FANCY', 'FRECKLES', 'RINGTAIL', 'HALFFACE', 'PANTSTWO', 'GOATEE', 'VITILIGOTWO', 'PAWS', 'MITAINE',
                 'BROKENBLAZE', 'SCOURGE', 'DIVA', 'BEARD'],
                ['TAIL', 'BLAZE', 'PRINCE', 'BIB', 'VEE', 'UNDERS', 'HONEY', 'FAROFA', 'DAMIEN', 'MISTER', 'BELLY',
                 'TAILTIP', 'TOES', 'TOPCOVER'],
                ['APRON', 'CAPSADDLE', 'MASKMANTLE', 'SQUEAKS', 'STAR', 'TOESTAIL', 'RAVENPAW', 'PANTS', 'REVERSEPANTS',
                 'SKUNK', 'KARPATI', 'HALFWHITE', 'APPALOOSA', 'DAPPLEPAW'],
                ['HEART', 'LILTWO', 'GLASS', 'MOORISH', 'SEPIAPOINT', 'MINKPOINT', 'SEALPOINT', 'MAO', 'LUNA', 'CHESTSPECK',
                 'WINGS', 'PAINTED', 'HEARTTWO', 'WOODPECKER'],
                ['BOOTS', 'MISS', 'COW', 'COWTWO', 'BUB', 'BOWTIE', 'MUSTACHE', 'REVERSEHEART', 'SPARROW', 'VEST',
                 'LOVEBUG', 'TRIXIE', 'SAMMY', 'SPARKLE'],
                ['RIGHTEAR', 'LEFTEAR', 'ESTRELLA', 'SHOOTINGSTAR', 'EYESPOT', 'REVERSEEYE', 'FADEBELLY', 'FRONT',
                 'BLOSSOMSTEP', 'PEBBLE', 'TAILTWO', 'BUDDY', 'BACKSPOT', 'EYEBAGS'],
                ['BULLSEYE', 'FINN', 'DIGIT', 'KROPKA', 'FCTWO', 'FCONE', 'MIA', 'SCAR', 'BUSTER', 'SMOKEY', 'HAWKBLAZE',
                 'CAKE', 'ROSINA', 'PRINCESS'],
                ['LOCKET', 'BLAZEMASK', 'TEARS', 'DOUGIE']
            ]

            for row, patches in enumerate(white_patches):
                for col, patch in enumerate(patches):
                    self.make_group('whitepatches', (col, row), f'white{f}_{patch}')

            # tortiepatchesmasks
            tortiepatchesmasks = [
                ['ONE', 'TWO', 'THREE', 'FOUR', 'REDTAIL', 'DELILAH', 'HALF', 'STREAK', 'MASK', 'SMOKE'],
                ['MINIMALONE', 'MINIMALTWO', 'MINIMALTHREE', 'MINIMALFOUR', 'OREO', 'SWOOP', 'CHIMERA', 'CHEST', 'ARMTAIL',
                 'GRUMPYFACE'],
                ['MOTTLED', 'SIDEMASK', 'EYEDOT', 'BANDANA', 'PACMAN', 'STREAMSTRIKE', 'SMUDGED', 'DAUB', 'EMBER', 'BRIE'],
                ['ORIOLE', 'ROBIN', 'BRINDLE', 'PAIGE', 'ROSETAIL', 'SAFI', 'DAPPLENIGHT', 'BLANKET', 'BELOVED', 'BODY'],
                ['SHILOH', 'FRECKLED', 'HEARTBEAT']
            ]

            for row, masks in enumerate(tortiepatchesmasks):
                for col, mask in enumerate(masks):
                    self.make_group('tortiepatchesmasks', (col, row), f"tortiemask{f}_{mask}")

            # Define skin colors 
            skin_colors = [
                ['BLACK', 'RED', 'PINK', 'DARKBROWN', 'BROWN', 'LIGHTBROWN'],
                ['DARK', 'DARKGREY', 'GREY', 'DARKSALMON', 'SALMON', 'PEACH'],
                ['DARKMARBLED', 'MARBLED', 'LIGHTMARBLED', 'DARKBLUE', 'BLUE', 'LIGHTBLUE']
            ]

            for row, colors in enumerate(skin_colors):
                for col, color in enumerate(colors):
                    self.make_group('skin', (col, row), f"skin{f}_{color}")

            self.load_scars(f)
        self.load_symbols()

    def load_scars(self, f):
        """
        Loads scar sprites and puts them into groups.
        """
        for a, i in enumerate(
                ["ONE", "TWO", "THREE", "MANLEG", "BRIGHTHEART", "MANTAIL", 
                 "BRIDGE", "RIGHTBLIND", "LEFTBLIND", "BOTHBLIND", "BURNPAWS", "BURNTAIL"]):
            self.make_group('scars', (a, 0), f'scars{i}')
        for a, i in enumerate(
                ["BURNBELLY", "BEAKCHEEK", "BEAKLOWER", "BURNRUMP", "CATBITE", "RATBITE",
                 "FROSTFACE", "FROSTTAIL", "FROSTMITT", "FROSTSOCK", "QUILLCHUNK", "QUILLSCRATCH"]):
            self.make_group('scars', (a, 1), f'scars{i}')
        for a, i in enumerate(
                ["TAILSCAR", "SNOUT", "CHEEK", "SIDE", "THROAT", "TAILBASE", "BELLY", "TOETRAP", "SNAKE",
                 "LEGBITE", "NECKBITE", "FACE"]):
            self.make_group('scars', (a, 2), f'scars{i}')
        for a, i in enumerate(
                ["HINDLEG", "BACK", "QUILLSIDE", "SCRATCHSIDE", "TOE", "BEAKSIDE", "CATBITETWO", "SNAKETWO", "FOUR"]):
            self.make_group('scars', (a, 3), f'scars{i}')
        # missing parts
        for a, i in enumerate(
                ["LEFTEAR", "RIGHTEAR", "NOTAIL", "NOLEFTEAR", "NORIGHTEAR", "NOEAR", "HALFTAIL", "NOPAW"]):
            self.make_group('missingscars', (a, 0), f'scars{i}')

        # Accessories
        # accent are things like leaves and metal just to be recolored :)
        for a, i in enumerate(['base', 'shade', 'line', 'accent']):
            self.make_group('accessories/accessories', (a, 0), f'bow{i}')
        for a, i in enumerate(['base', 'shade', 'line', 'accent']):
            self.make_group('accessories/accessories', (a, 1), f'collar{i}')
        for a, i in enumerate(['base', 'shade', 'line', 'accent']):
            self.make_group('accessories/accessories', (a, 2), f'nylon{i}')
        for a, i in enumerate(['base', 'shade', 'line', 'accent']):
            self.make_group('accessories/accessories', (a, 3), f'bell{i}')

        # Natural accessories
        for a, i in enumerate(['base', 'shade', 'line', 'accent']):
            self.make_group('accessories/herbaccessories', (a, 0), f'berries{i}')
        for a, i in enumerate(['base', 'shade', 'line', 'accent']):
            self.make_group('accessories/herbaccessories', (a, 1), f'nettle{i}')
        for a, i in enumerate(['base', 'shade', 'line', 'accent']):
            self.make_group('accessories/herbaccessories', (a, 2), f'earleaves{i}')
        for a, i in enumerate(['base', 'shade', 'line', 'accent']):
            self.make_group('accessories/herbaccessories', (a, 3), f'poppy{i}')
        for a, i in enumerate(['base', 'shade', 'line', 'accent']):
            self.make_group('accessories/herbaccessories', (a, 4), f'flowers{i}')
        for a, i in enumerate(['base', 'shade', 'line', 'accent']):
            self.make_group('accessories/herbaccessories', (a, 5), f'laurel{i}')
        for a, i in enumerate(['base', 'shade', 'line', 'accent']):
            self.make_group('accessories/herbaccessories', (a, 6), f'catmint{i}')
        for a, i in enumerate(['base', 'shade', 'line', 'accent']):
            self.make_group('accessories/herbaccessories', (a, 7), f'maple{i}')
        for a, i in enumerate(['base', 'shade', 'line', 'accent']):
            self.make_group('accessories/herbaccessories', (a, 8), f'lavender{i}')
        for a, i in enumerate(['base', 'shade', 'line', 'accent']):
            self.make_group('accessories/herbaccessories', (a, 9), f'bluebells{i}')
        for a, i in enumerate(['base', 'shade', 'line', 'accent']):
            self.make_group('accessories/herbaccessories', (a, 10), f'leaves{i}')
        for a, i in enumerate(['base', 'shade', 'line', 'accent']):
            self.make_group('accessories/herbaccessories', (a, 10), f'petals{i}')
        for a, i in enumerate(['base', 'shade', 'line', 'accent']):
            self.make_group('accessories/herbaccessories', (a, 11), f'berries2{i}')
        for a, i in enumerate(['base', 'shade', 'line', 'accent']):
            self.make_group('accessories/herbaccessories', (a, 12), f'seed{i}')
        for a, i in enumerate(['base', 'shade', 'line', 'accent']):
            self.make_group('accessories/herbaccessories', (a, 13), f'stalk{i}')

        # Wild accessories
        for a, i in enumerate(['base', 'shade', 'line', 'accent']):
            self.make_group('accessories/wildaccessories', (a, 0), f'moth{i}')
        for a, i in enumerate(['base', 'shade', 'line', 'accent']):
            self.make_group('accessories/wildaccessories', (a, 1), f'cicada{i}')
        for a, i in enumerate(['base', 'shade', 'line', 'accent']):
            self.make_group('accessories/wildaccessories', (a, 2), f'feathers{i}')
        for a, i in enumerate(['base', 'shade', 'line', 'accent']):
            self.make_group('accessories/wildaccessories', (a, 3), f'largemoth{i}')

        # Accessories patterns
        for a, i in enumerate(['dots', 'stripes', 'gradient1', 'gradient2', 'gradient3', 'gradient4']):
            self.make_group('accessories/patterns', (a, 0), f'bow{i}')


        """ for a, i in enumerate([
            "MAPLE LEAF", "HOLLY", "BLUE BERRIES", "FORGET ME NOTS", "RYE STALK", "LAUREL"]):
            self.make_group('medcatherbs', (a, 0), f'acc_herbs{i}')
        for a, i in enumerate([
            "BLUEBELLS", "NETTLE", "POPPY", "LAVENDER", "HERBS", "PETALS"]):
            self.make_group('medcatherbs', (a, 1), f'acc_herbs{i}')
        for a, i in enumerate([
            "OAK LEAVES", "CATMINT", "MAPLE SEED", "JUNIPER"]):
            self.make_group('medcatherbs', (a, 3), f'acc_herbs{i}')
        self.make_group('medcatherbs', (5, 2), 'acc_herbsDRY HERBS')

        for a, i in enumerate([
            "RED FEATHERS", "BLUE FEATHERS", "JAY FEATHERS", "MOTH WINGS", "CICADA WINGS"]):
            self.make_group('medcatherbs', (a, 2), f'acc_wild{i}')
        for a, i in enumerate(["CRIMSON", "BLUE", "YELLOW", "CYAN", "RED", "LIME"]):
            self.make_group('collars', (a, 0), f'collars{i}')
        for a, i in enumerate(["GREEN", "RAINBOW", "BLACK", "SPIKES", "WHITE"]):
            self.make_group('collars', (a, 1), f'collars{i}')
        for a, i in enumerate(["PINK", "PURPLE", "MULTI", "INDIGO"]):
            self.make_group('collars', (a, 2), f'collars{i}')
        for a, i in enumerate([
            "CRIMSONBELL", "BLUEBELL", "YELLOWBELL", "CYANBELL", "REDBELL",
            "LIMEBELL"
        ]):
            self.make_group('bellcollars', (a, 0), f'collars{i}')
        for a, i in enumerate(
                ["GREENBELL", "RAINBOWBELL", "BLACKBELL", "SPIKESBELL", "WHITEBELL"]):
            self.make_group('bellcollars', (a, 1), f'collars{i}')
        for a, i in enumerate(["PINKBELL", "PURPLEBELL", "MULTIBELL", "INDIGOBELL"]):
            self.make_group('bellcollars', (a, 2), f'collars{i}')
        for a, i in enumerate([
            "CRIMSONBOW", "BLUEBOW", "YELLOWBOW", "CYANBOW", "REDBOW",
            "LIMEBOW"
        ]):
            self.make_group('bowcollars', (a, 0), f'collars{i}')
        for a, i in enumerate(
                ["GREENBOW", "RAINBOWBOW", "BLACKBOW", "SPIKESBOW", "WHITEBOW"]):
            self.make_group('bowcollars', (a, 1), f'collars{i}')
        for a, i in enumerate(["PINKBOW", "PURPLEBOW", "MULTIBOW", "INDIGOBOW"]):
            self.make_group('bowcollars', (a, 2), f'collars{i}')
        for a, i in enumerate([
            "CRIMSONNYLON", "BLUENYLON", "YELLOWNYLON", "CYANNYLON", "REDNYLON",
            "LIMENYLON"
        ]):
            self.make_group('nyloncollars', (a, 0), f'collars{i}')
        for a, i in enumerate(
                ["GREENNYLON", "RAINBOWNYLON", "BLACKNYLON", "SPIKESNYLON", "WHITENYLON"]):
            self.make_group('nyloncollars', (a, 1), f'collars{i}')
        for a, i in enumerate(["PINKNYLON", "PURPLENYLON", "MULTINYLON", "INDIGONYLON"]):
            self.make_group('nyloncollars', (a, 2), f'collars{i}') """
            

# CREATE INSTANCE 
sprites = Sprites()
