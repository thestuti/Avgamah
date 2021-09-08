import hikari
from hikari import Embed
from hikari.messages import ButtonStyle
import tanjun
from datetime import datetime

from itsnp.core.client import Client
from itsnp.core.models import SuggestionModel


component = tanjun.Component()

suggestion_group = tanjun.slash_command_group("suggestion", "Suggestion command group.")


@suggestion_group.with_command
@tanjun.with_str_slash_option("suggestion", "A suggestion.")
@tanjun.as_slash_command("give", "Give a suggestion for the server.")
async def add_suggestion_command(ctx: tanjun.abc.Context, *, suggestion: str) -> None:
    emojis = ["✅", "❌"]
    embed = Embed(
        color=0xF1C40F,
        timestamp=datetime.now().astimezone(),
    )
    embed.add_field(name="Suggestion", value=suggestion)
    embed.set_author(name=f"Suggestion by {ctx.author}", icon=ctx.author.avatar_url)
    msg = await ctx.respond(embed=embed, ensure_result=True)
    for emoji in emojis:
        await msg.add_reaction(emoji)


@suggestion_group.with_command
@tanjun.with_author_permission_check(hikari.Permissions.MANAGE_GUILD)
@tanjun.with_str_slash_option("message_id", "Message ID of the suggestion")
@tanjun.as_slash_command("approve", "Approve the suggestion", default_to_ephemeral=True)
async def approve_command(ctx: tanjun.abc.Context, message_id: str) -> None:
    channel = await ctx.fetch_channel()
    msg = await ctx.rest.fetch_message(channel, int(message_id))
    if not msg.embeds:
        return
    embed = msg.embeds[0]
    embed.set_footer(text=f"Approved by {ctx.author}")
    embed.color = hikari.Color(0x00FF00)
    await msg.edit(embed=embed)
    await msg.remove_all_reactions()
    response = await ctx.respond("Done :ok_hand:", ensure_result=True)
    await response.delete()


@suggestion_group.with_command
@tanjun.with_author_permission_check(hikari.Permissions.MANAGE_GUILD)
@tanjun.with_str_slash_option("message_id", "Message ID of the suggestion")
@tanjun.with_str_slash_option("reason", "Reason for denial of the suggestion")
@tanjun.as_slash_command("deny", "Deny the Suggestion.", default_to_ephemeral=True)
async def deny_command(
    ctx: tanjun.abc.Context, message_id: str, *, reason: str
) -> None:
    channel = await ctx.fetch_channel()
    msg = await ctx.rest.fetch_message(channel, int(message_id))
    if not msg.embeds:
        return
    embed = msg.embeds[0]
    embed.title = f"Denial Reason - {reason}"
    embed.set_footer(text=f"Denied by {ctx.author}")
    embed.color = hikari.Color(0xFF0000)
    await msg.edit(embed=embed)
    await msg.remove_all_reactions()
    response = await ctx.respond("Done :ok_hand:", ensure_result=True)
    await response.delete()


component.add_slash_command(suggestion_group)


@tanjun.as_loader
def load_component(client: Client) -> None:
    client.add_component(component.copy())