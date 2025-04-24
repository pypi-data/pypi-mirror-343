# Dispy - Python Discord API library for discord bots.
# Copyright (C) 2025  James French
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

# When check, using ON and ONCE will enforce using custom args
intents = {
   "-1": [
      "READY",
      "RESUMED",
      "VOICE_SERVER_UPDATE",
      "USER_UPDATE",
      "INTERACTION_CREATE",
      "ALL"
   ],
   "0": [
      "GUILD_CREATE",
      "GUILD_UPDATE",
      "GUILD_DELETE",
      "GUILD_ROLE_CREATE",
      "GUILD_ROLE_UPDATE",
      "GUILD_ROLE_DELETE",
      "CHANNEL_CREATE",
      "CHANNEL_UPDATE",
      "CHANNEL_DELETE",
      "CHANNEL_PINS_UPDATE",
      "THREAD_CREATE",
      "THREAD_UPDATE",
      "THREAD_DELETE",
      "THREAD_LIST_SYNC",
      "THREAD_MEMBER_UPDATE",
      "THREAD_MEMBERS_UPDATE",
      "STAGE_INSTANCE_CREATE",
      "STAGE_INSTANCE_UPDATE",
      "STAGE_INSTANCE_DELETE",
      "MESSAGE_CREATE",
      "MESSAGE_UPDATE",
      "MESSAGE_DELETE",
      "MESSAGE_DELETE_BULK",
      "ALL"
   ],
   "1": [
      "GUILD_MEMBER_ADD",
      "GUILD_MEMBER_UPDATE",
      "GUILD_MEMBER_REMOVE",
      "THREAD_MEMBERS_UPDATE",
      "ALL"
   ],
   "2": [
      "GUILD_AUDIT_LOG_ENTRY_CREATE",
      "GUILD_BAN_ADD",
      "GUILD_BAN_REMOVE",
      "ALL"
   ],
   "3": [
      "GUILD_EMOJIS_UPDATE",
      "GUILD_STICKERS_UPDATE",
      "GUILD_SOUNDBOARD_SOUND_CREATE",
      "GUILD_SOUNDBOARD_SOUND_UPDATE",
      "GUILD_SOUNDBOARD_SOUND_DELETE",
      "GUILD_SOUNDBOARD_SOUNDS_UPDATE",
      "ALL"
   ],
   "4": [
      "GUILD_INTEGRATIONS_UPDATE",
      "INTEGRATION_CREATE",
      "INTEGRATION_UPDATE",
      "INTEGRATION_DELETE",
      "ALL"
   ],
   "5": [
      "WEBHOOKS_UPDATE",
      "ALL"
   ],
   "6": [
      "INVITE_CREATE",
      "INVITE_DELETE",
      "ALL"
   ],
   "7": [
      "VOICE_CHANNEL_EFFECT_SEND",
      "VOICE_STATE_UPDATE",
      "ALL"
   ],
   "8": [
      "PRESENCE_UPDATE",
      "ALL"
   ],
   "9": [
      "MESSAGE_CREATE",
      "MESSAGE_UPDATE",
      "MESSAGE_DELETE",
      "MESSAGE_DELETE_BULK",
      "ALL"
   ],
   "10": [
      "MESSAGE_REACTION_ADD",
      "MESSAGE_REACTION_REMOVE",
      "MESSAGE_REACTION_REMOVE_ALL",
      "MESSAGE_REACTION_REMOVE_EMOJI",
      "ALL"
   ],
   "11": [
      "TYPING_START",
      "ALL"
   ],
   "12": [ 
      "DIRECT_MESSAGE_CREATE",
      "DIRECT_MESSAGE_UPDATE",
      "DIRECT_MESSAGE_DELETE",
      "DIRECT_CHANNEL_PINS_UPDATE",
      "ALL"
   ],
   "13": [
      "DIRECT_MESSAGE_REACTION_ADD",
      "DIRECT_MESSAGE_REACTION_REMOVE",
      "DIRECT_MESSAGE_REACTION_REMOVE_ALL",
      "DIRECT_MESSAGE_REACTION_REMOVE_EMOJI",
      "ALL"
   ],
   "14": [
      "DIRECT_TYPING_START",
      "ALL"
   ],
   "15": [
      "MESSAGE_CREATE",
      "MESSAGE_UPDATE",
      "MESSAGE_DELETE",
      "MESSAGE_DELETE_BULK",
      "MESSAGE_POLL_VOTE_ADD",
      "MESSAGE_POLL_VOTE_REMOVE",
      "ALL"
   ],
   "16": [
      "GUILD_SCHEDULED_EVENT_CREATE",
      "GUILD_SCHEDULED_EVENT_UPDATE",
      "GUILD_SCHEDULED_EVENT_DELETE",
      "GUILD_SCHEDULED_EVENT_USER_ADD",
      "GUILD_SCHEDULED_EVENT_USER_REMOVE",
      "ALL"
   ],
   "20": [
      "AUTO_MODERATION_RULE_CREATE",
      "AUTO_MODERATION_RULE_UPDATE",
      "AUTO_MODERATION_RULE_DELETE",
      "ALL"
   ],
   "21": [
      "AUTO_MODERATION_ACTION_EXECUTION",
      "ALL"
   ],
   "24": [
      "MESSAGE_POLL_VOTE_ADD",
      "MESSAGE_POLL_VOTE_REMOVE",
      "ALL"
   ],
   "25": [
      "DIRECT_MESSAGE_POLL_VOTE_ADD",
      "DIRECT_MESSAGE_POLL_VOTE_REMOVE",
      "ALL"
   ]
}