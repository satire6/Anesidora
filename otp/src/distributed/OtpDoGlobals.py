"""
Contains otp specific network message types.
"""

from direct.distributed.MsgTypes import *


#-----------------------------------------------------------------------------
# Global Distributed Object ID's:


# Distributed object IDs from 4000 to 4599 are assigned by Roger:
OTP_DO_ID_SERVER_ROOT =           4007 # The root of the whole graph
OTP_DO_ID_FRIEND_MANAGER =        4501 # Old global friend manager id
OTP_DO_ID_LEADERBOARD_MANAGER =   4502

# Distributed object or channel IDs from 4600 to 4699 are assigned by Schuyler:
OTP_DO_ID_SERVER =                4600 # Server Status

OTP_DO_ID_UBER_DOG =              4601

OTP_CHANNEL_AI_AND_UD_BROADCAST = 4602
OTP_CHANNEL_UD_BROADCAST =        4603
OTP_CHANNEL_AI_BROADCAST =        4604
# fyi, the client broadcast channel is in direct/src/ai/AIMsgTypes.py

OTP_NET_MSGR_CHANNEL_ID_ALL_AI =  4605
OTP_NET_MSGR_CHANNEL_ID_UBER_DOG =4606
OTP_NET_MSGR_CHANNEL_ID_AI_ONLY = 4607

OTP_DO_ID_COMMON =                4615 # Global objects shared across toontwon, pirates, et al.
OTP_DO_ID_GATEWAY =               4616 # Root of Gateway
OTP_DO_ID_PIRATES =               4617 # Root of Pirates
OTP_DO_ID_TOONTOWN =              4618 # Root of Toontown
OTP_DO_ID_FAIRIES =               4619 # Root of Fairies
OTP_DO_ID_CARS =                  4620 # Root of Cars

OTP_DO_ID_AVATARS =               4630 # Look under the avatarId zone for the avaatar
OTP_DO_ID_FRIENDS =               4640 # Look under the avatarId zone for friend links
OTP_DO_ID_GUILDS =                4650 # Look under a guildId zone for a guild
OTP_DO_ID_ESCROW =                4660 # Look under the avatarId zone for pending trades

OTP_DO_ID_PIRATES_AVATAR_MANAGER =    4674
OTP_DO_ID_PIRATES_CREW_MANAGER =      4675
OTP_DO_ID_PIRATES_INVENTORY_MANAGER = 4677
OTP_DO_ID_PIRATES_SPEEDCHAT_RELAY   = 4711




OTP_DO_ID_PIRATES_SHIP_MANAGER =      4678
OTP_DO_ID_PIRATES_TRAVEL_AGENT =      4679
OTP_DO_ID_PIRATES_FRIENDS_MANAGER =   4680

OTP_DO_ID_CHAT_MANAGER =              4681

OTP_DO_ID_TOONTOWN_AVATAR_MANAGER =   4682
OTP_DO_ID_TOONTOWN_DELIVERY_MANAGER = 4683
OTP_DO_ID_TOONTOWN_TEMP_STORE_MANAGER=4684 
OTP_DO_ID_TOONTOWN_SPEEDCHAT_RELAY  = 4712

OTP_DO_ID_SWITCHBOARD_MANAGER = 4685
OTP_DO_ID_AVATAR_FRIENDS_MANAGER = 4686
OTP_DO_ID_PLAYER_FRIENDS_MANAGER = 4687
OTP_DO_ID_CENTRAL_LOGGER = 4688

OTP_DO_ID_CARS_AVATAR_MANAGER =       4689

OTP_DO_ID_TOONTOWN_MAIL_MANAGER = 4690
OTP_DO_ID_TOONTOWN_PARTY_MANAGER = 4691

OTP_DO_ID_TOONTOWN_RAT_MANAGER = 4692

OTP_DO_ID_STATUS_DATABASE = 4693
OTP_DO_ID_TOONTOWN_AWARD_MANAGER = 4694

OTP_DO_ID_TOONTOWN_CODE_REDEMPTION_MANAGER = 4695
OTP_DO_ID_TOONTOWN_IN_GAME_NEWS_MANAGER = 4696

OTP_DO_ID_TOONTOWN_NON_REPEATABLE_RANDOM_SOURCE = 4697

OTP_DO_ID_AI_TRADE_AVATAR =           4698

OTP_DO_ID_PIRATES_MATCH_MAKER =       4700
OTP_DO_ID_PIRATES_GUILD_MANAGER =     4701
OTP_DO_ID_PIRATES_AWARD_MAKER =       4702
OTP_DO_ID_PIRATES_CODE_REDEMPTION =   4703
OTP_DO_ID_PIRATES_SETTINGS_MANAGER =  4704
OTP_DO_ID_PIRATES_HOLIDAY_MANAGER =   4705
OTP_DO_ID_PIRATES_CREW_MATCH_MANAGER =4706

OTP_DO_ID_PIRATES_AVATAR_ACCESSORIES_MANAGER = 4710

# Note that 4711 and 4712 are taken
OTP_DO_ID_TOONTOWN_CPU_INFO_MANAGER = 4713

# Contiguous ID space makes renderer operation easier, grabbing a block of 10 for now!
OTP_DO_ID_SNAPSHOT_DISPATCHER = 4800
OTP_DO_ID_SNAPSHOT_RENDERER = 4801
OTP_DO_ID_SNAPSHOT_RENDERER_01 = 4801
OTP_DO_ID_SNAPSHOT_RENDERER_02 = 4802
OTP_DO_ID_SNAPSHOT_RENDERER_03 = 4803
OTP_DO_ID_SNAPSHOT_RENDERER_04 = 4804
OTP_DO_ID_SNAPSHOT_RENDERER_05 = 4805
OTP_DO_ID_SNAPSHOT_RENDERER_06 = 4806
OTP_DO_ID_SNAPSHOT_RENDERER_07 = 4807
OTP_DO_ID_SNAPSHOT_RENDERER_08 = 4808
OTP_DO_ID_SNAPSHOT_RENDERER_09 = 4809
OTP_DO_ID_SNAPSHOT_RENDERER_10 = 4810
OTP_DO_ID_SNAPSHOT_RENDERER_11 = 4811
OTP_DO_ID_SNAPSHOT_RENDERER_12 = 4812
OTP_DO_ID_SNAPSHOT_RENDERER_13 = 4813
OTP_DO_ID_SNAPSHOT_RENDERER_14 = 4814
OTP_DO_ID_SNAPSHOT_RENDERER_15 = 4815
OTP_DO_ID_SNAPSHOT_RENDERER_16 = 4816
OTP_DO_ID_SNAPSHOT_RENDERER_17 = 4817
OTP_DO_ID_SNAPSHOT_RENDERER_18 = 4818
OTP_DO_ID_SNAPSHOT_RENDERER_19 = 4819
OTP_DO_ID_SNAPSHOT_RENDERER_20 = 4820


OTP_DO_ID_PIRATES_INVENTORY_MANAGER_BASE = 5001

#-----------------------------------------------------------------------------
# Zone IDs are independent from distributed object IDs (0 to 0xffffffff):
OTP_ZONE_ID_INVALID =                0 # invalid zone id (like None or NULL).
OTP_ZONE_ID_OLD_QUIET_ZONE =         1 # obsolete/depreciated
OTP_ZONE_ID_MANAGEMENT =             2 # was uber zone, serves similar role with new name
OTP_ZONE_ID_DISTRICTS =              3 # districts/shards within a game
OTP_ZONE_ID_DISTRICTS_STATS =        4 # Were the district Stats Items are located
OTP_ZONE_ID_ELEMENTS =               5 # a collection of distributed objects, e.g. members in a crew

# OTP_ZONE_ID_<each avatarId>       100000??? to ?????? # avatar ID zones
# OTP_ZONE_ID_<each guildId>        ?? to ??? # guild ID zones
# OTP_ZONE_ID_<each toontown>       ?? to ??? # old style toontown zones

#-----------------------------------------------------------------------------

OTP_NET_MESSENGER_CHANNEL = (OTP_DO_ID_UBER_DOG <<32) + OTP_ZONE_ID_MANAGEMENT

#-----------------------------------------------------------------------------
# Notes to help skyler remember how this works (not meant as readable comments):
#
# example paths to objects in zone:
# /4007,2/4616,3/dist1,zoneN/zoneObjects
# /4007,2/4616,3/dist2,zoneN/zoneObjects
# /4007,2/4616,3/dist3,zoneN/zoneObjects
# /4007,2/4616,3/dist4,zoneN/zoneObjects
# /4007,2/4616,3/dist5,zoneN/zoneObjects
#
# /4007,2/4660,avatarId/pendingTradeObject
#
# (OTP_DO_ID_SERVER_ROOT, OTP_ZONE_ID_COMMON)
#     (OTP_DO_ID_COMMON, OTP_ZONE_ID_FRIENDS)
#
# (OTP_DO_ID_SERVER_ROOT, OTP_ZONE_ID_PIRATES)
#     (OTP_DO_ID_PIRATES, OTP_ZONE_ID_DISTRICTS)
#     (OTP_DO_ID_PIRATES, OTP_ZONE_ID_GUILDS)
#     (OTP_DO_ID_PIRATES, OTP_ZONE_ID_ESCROW)
#
# ((4007, 4650), (avatarDoId, ...path to player guild is what?))
