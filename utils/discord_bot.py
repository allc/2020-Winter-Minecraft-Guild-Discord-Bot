import discord
import logging


async def send_to_channels(bot: discord.Client, channel_ids, message: str):
    '''Send message to a list of Discord channels'''
    for channel_id in channel_ids:
        channel = bot.get_channel(channel_id)
        if channel:
            await channel.send(message)
        else:
            invalid_channel_id_message = f'Channel ID {channel_id} appears to be invalid.'
            print(invalid_channel_id_message)
            logging.error(invalid_channel_id_message)
