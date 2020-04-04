import sys
import pygame
from settings import *
from os import path
pygame.init()
pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.HWSURFACE|pygame.DOUBLEBUF)

if getattr(sys, 'frozen', False): # PyInstaller adds this attribute
    # Running in a bundle
    CurrentPath = sys._MEIPASS
else:
    # Running in normal Python environment
    CurrentPath = path.dirname(__file__)

game_folder = CurrentPath
img_folder = path.join(game_folder, 'img')
map_folder = path.join(game_folder, 'map')
music_folder = path.join(game_folder, 'music')
snd_folder = path.join(game_folder, 'sound')
anim_folder = path.join(game_folder, 'anim')
###### INTRP GRPH
intro_img = pygame.image.load(path.join(img_folder, 'Rycerz z Widelcem Intro Screen.png')).convert_alpha()
game_over_img = pygame.image.load(path.join(img_folder, 'Rycerz z Widelcem Game Over Screen.png')).convert_alpha()
game_over_img = pygame.transform.scale(game_over_img, (SCREEN_WIDTH,SCREEN_HEIGHT))
setup_img = pygame.image.load(path.join(img_folder, 'Setup Screen.png')).convert_alpha()
intro_img = pygame.transform.scale(intro_img, (SCREEN_WIDTH,SCREEN_HEIGHT))
intro_but_img = pygame.image.load(path.join(img_folder, 'button_intro_red_d.png')).convert_alpha()
intro_but_h_img = pygame.image.load(path.join(img_folder, 'button_intro_red_a.png')).convert_alpha()
####### UI GRAPHS ####
dim_screen = pygame.Surface((MAP_WIDTH,MAP_HEIGHT),pygame.HWSURFACE | pygame.SRCALPHA)
dim_screen.fill((0,0,0,110))
scroll_160_img = pygame.image.load(path.join(img_folder, 'scroll_160.png')).convert_alpha()
scroll_level_up = pygame.image.load(path.join(img_folder, 'scroll_160_level_up.png')).convert_alpha()
bar = pygame.image.load(path.join(img_folder, 'bar.png')).convert_alpha()
bar = pygame.transform.scale(bar, (250, 15))
small_bar = pygame.image.load(path.join(img_folder, 'bar_small.png')).convert_alpha()
small_bar = pygame.transform.scale(small_bar, (80, 10))
silver_line = pygame.image.load(path.join(img_folder, 'silver_tray.png')).convert_alpha()
silver_line = pygame.transform.scale(silver_line, (80, 10))
red_line = pygame.image.load(path.join(img_folder, 'red_line.png')).convert_alpha()
red_line = pygame.transform.scale(red_line, (240, 5))
blue_line = pygame.image.load(path.join(img_folder, 'blue_line.png')).convert_alpha()
blue_line = pygame.transform.scale(blue_line, (240, 5))
inv_bcg_image = pygame.image.load(path.join(img_folder, 'inv_bcg.png')).convert_alpha()
info_bcg = pygame.image.load(path.join(img_folder, 'info_bcg.png')).convert_alpha()
dialogbox_img = pygame.image.load(path.join(img_folder, 'dialog_box.png')).convert_alpha()
dialogbox_img_2 = pygame.image.load(path.join(img_folder, 'dialog_box_2.png')).convert_alpha()
inv_bar = pygame.image.load(path.join(img_folder, 'inv_bottom_frame.png')).convert_alpha()
button_a_img = pygame.image.load(path.join(img_folder, 'button_128_a.png')).convert_alpha()
button_d_img = pygame.image.load(path.join(img_folder, 'button_128_d.png')).convert_alpha()
rad_pause_img = pygame.image.load(path.join(img_folder, 'button_pause_red_d.png')).convert_alpha()
rad_pause_h_img = pygame.image.load(path.join(img_folder, 'button_pause_red_a.png')).convert_alpha()
rad_pause_h_img = pygame.transform.scale(rad_pause_h_img,(148,48))
rad_pause_img = pygame.transform.scale(rad_pause_img,(148,48))
rad_exit_h_img = pygame.image.load(path.join(img_folder, 'button_exit_a.png')).convert_alpha()
rad_exit_img = pygame.image.load(path.join(img_folder, 'button_exit_d.png')).convert_alpha()
rad_back_h_img = pygame.image.load(path.join(img_folder, 'button_back_a.png')).convert_alpha()
rad_back_img = pygame.image.load(path.join(img_folder, 'button_back_d.png')).convert_alpha()
rad_but_img = pygame.image.load(path.join(img_folder, 'radio_button.png')).convert_alpha()
rad_but_h_img = pygame.image.load(path.join(img_folder, 'radio_button_a.png')).convert_alpha()
rad_add_img = pygame.image.load(path.join(img_folder, 'radio_add.png')).convert_alpha()
rad_add_h_img = pygame.image.load(path.join(img_folder, 'radio_add_a.png')).convert_alpha()
rad_subs_img = pygame.image.load(path.join(img_folder, 'radio_substr.png')).convert_alpha()
rad_subs_h_img = pygame.image.load(path.join(img_folder, 'radio_subs_a.png')).convert_alpha()
rad_use_h_img = pygame.image.load(path.join(img_folder, 'button_use_a.png')).convert_alpha()
rad_use_img = pygame.image.load(path.join(img_folder, 'button_use_d.png')).convert_alpha()
rad_open_h_img = pygame.image.load(path.join(img_folder, 'button_open_red_a.png')).convert_alpha()
rad_open_img = pygame.image.load(path.join(img_folder, 'button_open_red_d.png')).convert_alpha()
rad_ok_h_img = pygame.image.load(path.join(img_folder, 'button_ok_red_a.png')).convert_alpha()
rad_ok_img = pygame.image.load(path.join(img_folder, 'button_ok_red_d.png')).convert_alpha()
sbb_img = pygame.image.load(path.join(img_folder, 'button_spell_d.png')).convert_alpha()
sbb_h_img = pygame.image.load(path.join(img_folder, 'button_spell_a.png')).convert_alpha()
qbb_img = pygame.image.load(path.join(img_folder, 'button_quest_d.png')).convert_alpha()
qbb_h_img = pygame.image.load(path.join(img_folder, 'button_quest_a.png')).convert_alpha()
repb_img = pygame.image.load(path.join(img_folder, 'button_repair_d.png')).convert_alpha()
repb_h_img = pygame.image.load(path.join(img_folder, 'button_repair_a.png')).convert_alpha()
empty_image = pygame.image.load(path.join(img_folder, 'empty_image.png')).convert_alpha()
next_page_img = pygame.image.load(path.join(img_folder, 'next_page_img.png')).convert_alpha()
prev_page_img = pygame.image.load(path.join(img_folder, 'prev_page_img.png')).convert_alpha()
rad_cast_img = pygame.image.load(path.join(img_folder, 'button_cast_d.png')).convert_alpha()
rad_cast_h_img = pygame.image.load(path.join(img_folder, 'button_cast_a.png')).convert_alpha()
quest_bcg_img = pygame.image.load(path.join(img_folder, 'quest_image_bcg.png')).convert_alpha()
### TILESET #####
tileset_image = pygame.image.load(path.join(img_folder, 'tileset.png')).convert_alpha()
full_tileset_image = pygame.image.load(path.join(img_folder, 'full_tileset.png')).convert_alpha()
### IN GAME GRPH
pl_knight_image = pygame.image.load(path.join(img_folder, 'character_knight.png')).convert_alpha()
pl_wizard_image = pygame.image.load(path.join(img_folder, 'character_wizard.png')).convert_alpha()
pl_thief_image = pygame.image.load(path.join(img_folder, 'character_thief.png')).convert_alpha()
swing_small = pygame.image.load(path.join(img_folder, 'swing_small.png')).convert_alpha()
swing_medium = pygame.image.load(path.join(img_folder, 'swing_medium.png')).convert_alpha()
swing_big = pygame.image.load(path.join(img_folder, 'swing_big.png')).convert_alpha()
hit_image = pygame.image.load(path.join(img_folder, 'hit1.png')).convert_alpha()
attent_image = pygame.image.load(path.join(img_folder, 'attent.png')).convert_alpha()
flesh_image = pygame.image.load(path.join(img_folder, 'red_flesh.png')).convert_alpha()
gold_coin = pygame.image.load(path.join(img_folder, 'gold1_img.png')).convert_alpha()
xp_icon = pygame.image.load(path.join(img_folder, 'xp_icon.png')).convert_alpha()
arrow_icon = pygame.image.load(path.join(img_folder, 'arrow_icon.png')).convert_alpha()
arrows_icon = pygame.image.load(path.join(img_folder, 'arrows_icon.png')).convert_alpha()
slot_img = pygame.image.load(path.join(img_folder, 'slot.png')).convert_alpha()
slot_img = pygame.transform.scale(slot_img,(TILE_SIZE,TILE_SIZE))
slot_w_img = pygame.image.load(path.join(img_folder, 'slot_weapon.png')).convert_alpha()
slot_s_img = pygame.image.load(path.join(img_folder, 'slot_shield.png')).convert_alpha()
slot_a_img = pygame.image.load(path.join(img_folder, 'slot_armor.png')).convert_alpha()
slot_h_img = pygame.image.load(path.join(img_folder, 'slot_helmet.png')).convert_alpha()
slot_b_img = pygame.image.load(path.join(img_folder, 'slot_boots.png')).convert_alpha()
slot_r_img = pygame.image.load(path.join(img_folder, 'slot_ring.png')).convert_alpha()
slot_n_img = pygame.image.load(path.join(img_folder, 'slot_necklace.png')).convert_alpha()
trap1_img = pygame.image.load(path.join(img_folder, 'trap1.png')).convert_alpha()
pintrap_h_img = pygame.image.load(path.join(img_folder, 'pintrap_h.png')).convert_alpha()
pintrap_o_img = pygame.image.load(path.join(img_folder, 'pintrap_o.png')).convert_alpha()
arrow_img = pygame.image.load(path.join(img_folder, 'arrow.png')).convert_alpha()
barrel_img = pygame.image.load(path.join(img_folder, 'barrel_img.png')).convert_alpha()
barrel_damage_mask = pygame.image.load(path.join(img_folder, 'barrel_damage_mask.png')).convert_alpha()
gold1_img = pygame.image.load(path.join(img_folder, 'gold1_img.png')).convert_alpha()
goldfew_img = pygame.image.load(path.join(img_folder, 'goldfew_img.png')).convert_alpha()
goldlots_img = pygame.image.load(path.join(img_folder, 'goldlots_img.png')).convert_alpha()
treasure_chest_closed = pygame.image.load(path.join(img_folder, 'chest_closed.png')).convert_alpha()
treasure_chest_open = pygame.image.load(path.join(img_folder, 'chest_open.png')).convert_alpha()
treasure_bcg_img = pygame.image.load(path.join(img_folder, 'treasure_bcg.png')).convert_alpha()
spellbook_bcg_img = pygame.image.load(path.join(img_folder, 'spellbook_bcg.png')).convert_alpha()
ebroken_armor_img = pygame.image.load(path.join(img_folder, 'ebroken_armor.png')).convert_alpha()
default_shop_owner_img = pygame.image.load(path.join(img_folder, 'default_shop_owner_img.png')).convert_alpha()
tomato_empty_img = pygame.image.load(path.join(img_folder, 'tomato_empty.png')).convert_alpha()
tomato_img = pygame.image.load(path.join(img_folder, 'tomato.png')).convert_alpha()
paprika_empty_img = pygame.image.load(path.join(img_folder, 'paprika_empty.png')).convert_alpha()
paprika_img = pygame.image.load(path.join(img_folder, 'paprika.png')).convert_alpha()

### EFFECTS ICONS
e_fav_wea_ico = pygame.image.load(path.join(img_folder, 'e_fav_wea.png')).convert_alpha()
e_dis_wea_ico = pygame.image.load(path.join(img_folder, 'e_dis_wea.png')).convert_alpha()
e_fav_arm_ico = pygame.image.load(path.join(img_folder, 'e_fav_arm.png')).convert_alpha()
e_dis_arm_ico = pygame.image.load(path.join(img_folder, 'e_dis_arm.png')).convert_alpha()
e_stoneskin_ico = pygame.image.load(path.join(img_folder, 'e_stoneskin.png')).convert_alpha()
e_haste_ico = pygame.image.load(path.join(img_folder, 'e_haste.png')).convert_alpha()
e_invisibility_ico = pygame.image.load(path.join(img_folder, 'e_invisibility.png')).convert_alpha()
e_ironskin_ico = pygame.image.load(path.join(img_folder, 'e_ironskin.png')).convert_alpha()
e_heroism_ico = pygame.image.load(path.join(img_folder, 'e_heroism.png')).convert_alpha()
### SPELL ICONS
sb_firebolt_image = pygame.image.load(path.join(img_folder, 'sb_firebolt.png')).convert_alpha()
sb_fireball_image = pygame.image.load(path.join(img_folder, 'sb_fireball.png')).convert_alpha()
sb_icebolt_image = pygame.image.load(path.join(img_folder, 'sb_icebolt.png')).convert_alpha()
sb_tricebolt_image = pygame.image.load(path.join(img_folder, 'sb_tricebolt.png')).convert_alpha()
sb_poisoncloud_image = pygame.image.load(path.join(img_folder, 'sb_poisoncloud.png')).convert_alpha()
sb_freeze_image = pygame.image.load(path.join(img_folder, 'sb_freeze.png')).convert_alpha()
sb_cure_image = pygame.image.load(path.join(img_folder, 'sb_cure.png')).convert_alpha()
sb_stoneskin_image = pygame.image.load(path.join(img_folder, 'sb_stoneskin.png')).convert_alpha()
sb_haste_image = pygame.image.load(path.join(img_folder, 'sb_haste.png')).convert_alpha()
sb_invisibility_image = pygame.image.load(path.join(img_folder, 'sb_invisibility.png')).convert_alpha()
sb_ironskin_image = pygame.image.load(path.join(img_folder, 'sb_ironskin.png')).convert_alpha()
sb_heroism_image = pygame.image.load(path.join(img_folder, 'sb_heroism.png')).convert_alpha()
### SPELL BULLETS
bullet_firebolt_image = pygame.image.load(path.join(img_folder, 'bull_fireball.png')).convert_alpha()
bullet_fireball_image = pygame.image.load(path.join(img_folder, 'bull_fireball2.png')).convert_alpha()
bullet_icebolt_image = pygame.image.load(path.join(img_folder, 'bull_icebolt.png')).convert_alpha()
bullet_poison_image = pygame.image.load(path.join(img_folder, 'bull_poisoncloud.png')).convert_alpha()
bullet_magic_image = pygame.image.load(path.join(img_folder, 'bull_magic.png')).convert_alpha()
bullet_dart_image = pygame.image.load(path.join(img_folder, 'bull_dart.png')).convert_alpha()
bullet_rock_image = pygame.image.load(path.join(img_folder, 'bull_rock.png')).convert_alpha()
### ANIMS
torch1_img = pygame.image.load(path.join(anim_folder, 'torch1.png')).convert_alpha()
torch2_img = pygame.image.load(path.join(anim_folder, 'torch2.png')).convert_alpha()
torch3_img = pygame.image.load(path.join(anim_folder, 'torch3.png')).convert_alpha()
torch4_img = pygame.image.load(path.join(anim_folder, 'torch4.png')).convert_alpha()
torch_animation_images = [torch1_img,torch2_img,torch3_img,torch4_img]
fountain1_img = pygame.image.load(path.join(anim_folder, 'fountain1.png')).convert_alpha()
fountain2_img = pygame.image.load(path.join(anim_folder, 'fountain2.png')).convert_alpha()
fountain_animation_images = [fountain1_img,fountain2_img]
fireball1_img = pygame.image.load(path.join(anim_folder, 'fireball1.png')).convert_alpha()
fireball2_img = pygame.image.load(path.join(anim_folder, 'fireball2.png')).convert_alpha()
fireball3_img = pygame.image.load(path.join(anim_folder, 'fireball3.png')).convert_alpha()
fireball4_img = pygame.image.load(path.join(anim_folder, 'fireball4.png')).convert_alpha()
fireball_animation_images = [fireball1_img,fireball2_img,fireball3_img,fireball4_img]
poisoncloud1_img = pygame.image.load(path.join(anim_folder, 'poison_cloud1.png')).convert_alpha()
poisoncloud2_img = pygame.image.load(path.join(anim_folder, 'poison_cloud2.png')).convert_alpha()
poisoncloud3_img = pygame.image.load(path.join(anim_folder, 'poison_cloud3.png')).convert_alpha()
poisoncloud4_img = pygame.image.load(path.join(anim_folder, 'poison_cloud4.png')).convert_alpha()
poisoncloud_animation_images = [poisoncloud1_img,poisoncloud2_img,poisoncloud3_img,poisoncloud4_img]
### DEATH ANIMS
kn_d_1 = pygame.image.load(path.join(anim_folder, 'knight_d_1.png')).convert_alpha()
kn_d_2 = pygame.image.load(path.join(anim_folder, 'knight_d_2.png')).convert_alpha()
kn_d_3 = pygame.image.load(path.join(anim_folder, 'knight_d_3.png')).convert_alpha()
kn_d_4 = pygame.image.load(path.join(anim_folder, 'knight_d_4.png')).convert_alpha()
kn_d_5 = pygame.image.load(path.join(anim_folder, 'knight_d_5.png')).convert_alpha()
kn_d_6 = pygame.image.load(path.join(anim_folder, 'knight_d_6.png')).convert_alpha()
kn_d_7 = pygame.image.load(path.join(anim_folder, 'knight_d_7.png')).convert_alpha()
knight_death_anim = [kn_d_1,kn_d_2,kn_d_3,kn_d_4,kn_d_5,kn_d_6,kn_d_7]

# SOUND
wear_item_snd = pygame.mixer.Sound(path.join(snd_folder, 'wear_item.wav'))
chop_snd = pygame.mixer.Sound(path.join(snd_folder, 'chop.wav'))
smash_snd = pygame.mixer.Sound(path.join(snd_folder, 'smash.wav'))
door_open_snd = pygame.mixer.Sound(path.join(snd_folder, 'door_open_2.wav'))
try_unlock_snd = pygame.mixer.Sound(path.join(snd_folder, 'try_unlock2.wav'))
coin_snd = pygame.mixer.Sound(path.join(snd_folder, 'coin.wav'))
block_snd = pygame.mixer.Sound(path.join(snd_folder, 'block2.wav'))
firebolt_snd = pygame.mixer.Sound(path.join(snd_folder, 'firebolt_snd.wav'))
fireblow_snd = pygame.mixer.Sound(path.join(snd_folder, 'fireblow2.wav'))
icebolt_snd = pygame.mixer.Sound(path.join(snd_folder, 'icebolt_snd.wav'))
empty_spell_snd = pygame.mixer.Sound(path.join(snd_folder, 'empty_spell.wav'))
cure_snd = pygame.mixer.Sound(path.join(snd_folder, 'cure.wav'))
stoneskin_snd = pygame.mixer.Sound(path.join(snd_folder, 'stoneskin2.wav'))
bow_snd = pygame.mixer.Sound(path.join(snd_folder, 'bow.wav'))
haste_snd = pygame.mixer.Sound(path.join(snd_folder, 'haste.wav'))
death_snd = pygame.mixer.Sound(path.join(snd_folder, 'death2.wav'))
pintrap_o_snd = pygame.mixer.Sound(path.join(snd_folder, 'pintrap_open.wav'))
hurra_snd = pygame.mixer.Sound(path.join(snd_folder, 'hurra.wav'))
oink_snd = pygame.mixer.Sound(path.join(snd_folder, 'oink.wav'))
smith_snd = pygame.mixer.Sound(path.join(snd_folder, 'smith.wav'))
crunch_snd = pygame.mixer.Sound(path.join(snd_folder, 'crunch.wav'))
levelup_snd = pygame.mixer.Sound(path.join(snd_folder, 'level_up.wav'))
item_dig_snd = pygame.mixer.Sound(path.join(snd_folder, 'item_dig.wav'))
item_found_snd = pygame.mixer.Sound(path.join(snd_folder, 'item_found.wav'))