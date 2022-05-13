from __future__ import unicode_literals
import logging
import os
import asyncio
import hikari
from songbird import ytdl
from songbird.hikari import Voicebox
from dotenv import load_dotenv
load_dotenv()



HIKARI_GUILD_ID = os.environ.get( "HIKARI_GUILD_ID" )
HIKARI_CHANNEL_VOICE_ID = os.environ.get( "HIKARI_CHANNEL_VOICE_ID" )
HIKARI_YOUTUBE_URL = os.environ.get( "HIKARI_YOUTUBE_URL" )
BOT = hikari.GatewayBot( token=os.environ.get("HIKARI_TOKEN") )
LOGGER = logging.getLogger( "hikari.bot" )


@BOT.listen()
async def hikari_on_guild_available (event: hikari.GuildAvailableEvent):
    guild = await event.fetch_guild()
    if str(guild.id) != HIKARI_GUILD_ID:
        return
    vchannel: hikari.GuildVoiceChannel = guild.get_channel( HIKARI_CHANNEL_VOICE_ID )
    if not vchannel:
        return
    voice = await Voicebox.connect( BOT, guild.id, vchannel.id )
    while True:
        voice_src = await ytdl( HIKARI_YOUTUBE_URL )
        voice_trk = await voice.play_only_source( voice_src )
        metadata = voice_trk.metadata
        LOGGER.info( f"Track title: {metadata.title}" )
        duration = metadata.duration
        LOGGER.info( f"Track duration: {duration}" )
        await asyncio.sleep( duration )


BOT.run()
